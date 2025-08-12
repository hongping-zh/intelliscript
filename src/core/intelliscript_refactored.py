#!/usr/bin/env python3
"""
Refactored IntelliScript Core - Improved structure and maintainability
Implements the requested architectural improvements:
- Single responsibility functions
- IntelliScript class encapsulation
- Multi-provider LLM support
- Enhanced configuration management
- Robust error handling
"""

import os
import sys
import json
import argparse
import platform
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from abc import ABC, abstractmethod

# Import existing modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.model_handler import ModelHandler
from security.command_safety import check_command_safety, analyze_command_risks


@dataclass
class CommandResult:
    """Result of a command execution"""
    success: bool
    response: str
    explanation: str
    tokens_used: int = 0
    response_time: int = 0
    error: Optional[str] = None


class LLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    def __init__(self, api_key: str, config: Dict[str, Any]):
        self.api_key = api_key
        self.config = config
    
    @abstractmethod
    def get_command(self, query: str, context: Dict[str, Any]) -> CommandResult:
        """Get command suggestion from the LLM provider"""
        pass
    
    @abstractmethod
    def get_model_name(self) -> str:
        """Get the model name"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the provider is available (has valid API key, etc.)"""
        pass


class OpenAIProvider(LLMProvider):
    """OpenAI GPT provider implementation"""
    
    def __init__(self, api_key: str, config: Dict[str, Any]):
        super().__init__(api_key, config)
        self.model = config.get('openai_model', 'gpt-4-turbo')
        self.temperature = config.get('temperature', 0.2)
    
    def get_command(self, query: str, context: Dict[str, Any]) -> CommandResult:
        try:
            import openai
            openai.api_key = self.api_key
            
            system_prompt = self._build_system_prompt(context)
            user_prompt = self._build_user_prompt(query, context)
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=self.temperature,
                max_tokens=1024
            )
            
            content = response.choices[0].message.content.strip()
            command, explanation = self._parse_response(content)
            
            return CommandResult(
                success=True,
                response=command,
                explanation=explanation,
                tokens_used=response.usage.total_tokens
            )
            
        except Exception as e:
            return CommandResult(
                success=False,
                response="",
                explanation="",
                error=str(e)
            )
    
    def get_model_name(self) -> str:
        return f"OpenAI {self.model}"
    
    def is_available(self) -> bool:
        return bool(self.api_key and self.api_key.startswith('sk-'))
    
    def _build_system_prompt(self, context: Dict[str, Any]) -> str:
        os_info = context.get('os_info', platform.system())
        custom_prompt = self.config.get('system_message')
        
        if custom_prompt:
            return custom_prompt.format(os=os_info)
        
        return f"""You are a shell command expert for {os_info}. 
        Generate precise, safe commands based on user queries.
        
        RESPONSE FORMAT:
        Command: <the exact command>
        Explanation: <brief one-sentence explanation>
        
        SAFETY RULES:
        - Never generate destructive commands (rm -rf, mkfs, dd, etc.)
        - Prefer safe, read-only operations when possible
        - Always include safety flags where appropriate"""
    
    def _build_user_prompt(self, query: str, context: Dict[str, Any]) -> str:
        prompt = f"Query: {query}"
        
        # Add conversation history if available
        if 'history' in context and context['history']:
            prompt = f"Previous context:\n{context['history']}\n\nNew query: {query}"
        
        return prompt
    
    def _parse_response(self, content: str) -> tuple[str, str]:
        """Parse AI response into command and explanation"""
        lines = content.strip().split('\n')
        command = ""
        explanation = ""
        
        for line in lines:
            if line.startswith('Command:'):
                command = line.replace('Command:', '').strip()
            elif line.startswith('Explanation:'):
                explanation = line.replace('Explanation:', '').strip()
        
        if not command and not explanation:
            # Fallback: treat entire response as command
            command = content.strip()
            explanation = "AI-generated command"
        
        return command, explanation


class OllamaProvider(LLMProvider):
    """Ollama local model provider implementation"""
    
    def __init__(self, api_key: str, config: Dict[str, Any]):
        super().__init__(api_key, config)  # For Ollama, api_key can be empty
        self.model = config.get('ollama_model', 'llama3')
        self.temperature = config.get('temperature', 0.2)
        self.base_url = config.get('ollama_url', 'http://localhost:11434')
    
    def get_command(self, query: str, context: Dict[str, Any]) -> CommandResult:
        try:
            import requests
            import json
            from time import time
            
            start_time = time()
            
            system_prompt = self._build_system_prompt(context)
            user_prompt = self._build_user_prompt(query, context)
            
            # Ollama API request payload
            payload = {
                "model": self.model,
                "prompt": f"{system_prompt}\n\nUser: {user_prompt}\nAssistant:",
                "stream": False,
                "options": {
                    "temperature": self.temperature,
                    "top_p": 0.9,
                    "max_tokens": 1000
                }
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=60,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result.get('response', '').strip()
                
                command, explanation = self._parse_response(content)
                response_time = int((time() - start_time) * 1000)
                
                return CommandResult(
                    success=True,
                    response=command,
                    explanation=explanation,
                    tokens_used=result.get('eval_count', 0),
                    response_time=response_time
                )
            else:
                return CommandResult(
                    success=False,
                    response="",
                    explanation="",
                    error=f"Ollama API error: {response.status_code} - {response.text}"
                )
                
        except ImportError:
            return CommandResult(
                success=False,
                response="",
                explanation="",
                error="requests library not found. Install with: pip install requests"
            )
        except requests.exceptions.ConnectionError:
            return CommandResult(
                success=False,
                response="",
                explanation="",
                error=f"Cannot connect to Ollama at {self.base_url}. Make sure Ollama is running: 'ollama serve'"
            )
        except Exception as e:
            return CommandResult(
                success=False,
                response="",
                explanation="",
                error=f"Ollama error: {str(e)}"
            )
    
    def get_model_name(self) -> str:
        return f"Ollama {self.model}"
    
    def is_available(self) -> bool:
        try:
            import requests
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                return any(model.get('name', '').startswith(self.model) for model in models)
            return False
        except:
            return False
    
    def _build_system_prompt(self, context: Dict[str, Any]) -> str:
        os_info = context.get('os_info', 'Unknown OS')
        shell_info = context.get('shell_info', 'Unknown shell')
        
        return f"""You are IntelliScript, an intelligent command-line assistant running on {os_info} with {shell_info}.

Your role is to translate natural language queries into precise, safe, and executable shell commands.

IMPORTANT GUIDELINES:
1. Generate ONLY the command, no explanations unless asked
2. Use the most appropriate and safe command for the task
3. For dangerous operations, suggest safer alternatives
4. Consider the current operating system and shell environment
5. Provide clear, executable commands

Format your response as:
Command: [your command here]
Explanation: [brief explanation of what the command does]

Current environment: {os_info} ({shell_info})"""

    def _build_user_prompt(self, query: str, context: Dict[str, Any]) -> str:
        prompt = f"Query: {query}"
        
        # Add conversation history if available
        if 'history' in context and context['history']:
            prompt = f"Previous context:\n{context['history']}\n\nNew query: {query}"
        
        return prompt
    
    def _parse_response(self, content: str) -> tuple[str, str]:
        """Parse AI response into command and explanation"""
        lines = content.strip().split('\n')
        command = ""
        explanation = ""
        
        for line in lines:
            if line.startswith('Command:'):
                command = line.replace('Command:', '').strip()
            elif line.startswith('Explanation:'):
                explanation = line.replace('Explanation:', '').strip()
        
        if not command and not explanation:
            # Fallback: treat entire response as command
            command = content.strip()
            explanation = f"Command generated by {self.model}"
        
        return command, explanation


class GeminiProvider(LLMProvider):
    """Google Gemini provider implementation"""
    
    def __init__(self, api_key: str, config: Dict[str, Any]):
        super().__init__(api_key, config)
        self.model = config.get('gemini_model', 'gemini-pro')
        self.temperature = config.get('temperature', 0.2)
    
    def get_command(self, query: str, context: Dict[str, Any]) -> CommandResult:
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel(self.model)
            
            system_prompt = self._build_system_prompt(context)
            user_prompt = self._build_user_prompt(query, context)
            full_prompt = f"{system_prompt}\n\n{user_prompt}"
            
            response = model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=self.temperature,
                    max_output_tokens=1024,
                )
            )
            
            content = response.text.strip()
            command, explanation = self._parse_response(content)
            
            return CommandResult(
                success=True,
                response=command,
                explanation=explanation,
                tokens_used=len(content.split())  # Approximate
            )
            
        except Exception as e:
            return CommandResult(
                success=False,
                response="",
                explanation="",
                error=str(e)
            )
    
    def get_model_name(self) -> str:
        return f"Google {self.model}"
    
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    def _build_system_prompt(self, context: Dict[str, Any]) -> str:
        os_info = context.get('os_info', platform.system())
        custom_prompt = self.config.get('system_message')
        
        if custom_prompt:
            return custom_prompt.format(os=os_info)
        
        return f"""You are a shell command expert for {os_info}. 
        Generate precise, safe commands based on user queries.
        
        RESPONSE FORMAT:
        Command: <the exact command>
        Explanation: <brief one-sentence explanation>"""
    
    def _build_user_prompt(self, query: str, context: Dict[str, Any]) -> str:
        prompt = f"Query: {query}"
        
        if 'history' in context and context['history']:
            prompt = f"Previous context:\n{context['history']}\n\nNew query: {query}"
        
        return prompt
    
    def _parse_response(self, content: str) -> tuple[str, str]:
        """Parse AI response into command and explanation"""
        lines = content.strip().split('\n')
        command = ""
        explanation = ""
        
        for line in lines:
            if line.startswith('Command:'):
                command = line.replace('Command:', '').strip()
            elif line.startswith('Explanation:'):
                explanation = line.replace('Explanation:', '').strip()
        
        if not command and not explanation:
            command = content.strip()
            explanation = "AI-generated command"
        
        return command, explanation


class ClaudeProvider(LLMProvider):
    """Anthropic Claude provider implementation"""
    
    def __init__(self, api_key: str, config: Dict[str, Any]):
        super().__init__(api_key, config)
        self.model = config.get('claude_model', 'claude-3-5-sonnet-20241022')
        self.temperature = config.get('temperature', 0.2)
        self.max_tokens = config.get('max_tokens', 1024)
    
    def get_command(self, query: str, context: Dict[str, Any]) -> CommandResult:
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=self.api_key)
            
            system_prompt = self._build_system_prompt(context)
            user_prompt = self._build_user_prompt(query, context)
            
            response = client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            content = response.content[0].text.strip()
            command, explanation = self._parse_response(content)
            
            return CommandResult(
                success=True,
                response=command,
                explanation=explanation,
                tokens_used=response.usage.input_tokens + response.usage.output_tokens
            )
            
        except Exception as e:
            return CommandResult(
                success=False,
                response="",
                explanation="",
                error=str(e)
            )
    
    def get_model_name(self) -> str:
        return f"Anthropic {self.model}"
    
    def is_available(self) -> bool:
        return bool(self.api_key and self.api_key.startswith('sk-'))
    
    def _build_system_prompt(self, context: Dict[str, Any]) -> str:
        os_info = context.get('os_info', platform.system())
        custom_prompt = self.config.get('system_message')
        
        if custom_prompt:
            return custom_prompt.format(os=os_info)
        
        return f"""You are a shell command expert for {os_info}. 
        Generate precise, safe commands based on user queries.
        
        RESPONSE FORMAT:
        Command: <the exact command>
        Explanation: <brief one-sentence explanation>
        
        SAFETY RULES:
        - Never generate destructive commands
        - Prefer safe operations
        - Include safety flags where appropriate"""
    
    def _build_user_prompt(self, query: str, context: Dict[str, Any]) -> str:
        prompt = f"Query: {query}"
        
        if 'history' in context and context['history']:
            prompt = f"Previous context:\n{context['history']}\n\nNew query: {query}"
        
        return prompt
    
    def _parse_response(self, content: str) -> tuple[str, str]:
        """Parse AI response into command and explanation"""
        lines = content.strip().split('\n')
        command = ""
        explanation = ""
        
        for line in lines:
            if line.startswith('Command:'):
                command = line.replace('Command:', '').strip()
            elif line.startswith('Explanation:'):
                explanation = line.replace('Explanation:', '').strip()
        
        if not command and not explanation:
            command = content.strip()
            explanation = "AI-generated command"
        
        return command, explanation


class ConfigurationManager:
    """Enhanced configuration management with TOML support"""
    
    def __init__(self, config_path: Optional[str] = None):
        if config_path is None:
            config_dir = os.path.expanduser('~/.config/intelliscript')
            os.makedirs(config_dir, exist_ok=True)
            self.config_path = os.path.join(config_dir, 'config.toml')
        else:
            self.config_path = config_path
        
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from TOML file with fallback to JSON and environment"""
        config = self._get_default_config()
        
        # Try to load from TOML file first
        if os.path.exists(self.config_path):
            try:
                if self.config_path.endswith('.toml'):
                    import tomllib
                    with open(self.config_path, 'rb') as f:
                        file_config = tomllib.load(f)
                else:
                    with open(self.config_path, 'r') as f:
                        file_config = json.load(f)
                
                config.update(file_config)
            except Exception as e:
                print(f"Warning: Could not load config file: {e}")
        
        # Override with environment variables
        env_mappings = {
            'OPENAI_API_KEY': ['openai', 'api_key'],
            'ANTHROPIC_API_KEY': ['anthropic', 'api_key'], 
            'GOOGLE_API_KEY': ['google', 'api_key'],
            'INTELLISCRIPT_MODEL': ['default_provider'],
            'INTELLISCRIPT_TEMPERATURE': ['temperature']
        }
        
        for env_var, config_path in env_mappings.items():
            value = os.getenv(env_var)
            if value:
                self._set_nested_config(config, config_path, value)
        
        return config
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            'openai': {
                'api_key': '',
                'model': 'gpt-4-turbo',
                'temperature': 0.2
            },
            'anthropic': {
                'api_key': '',
                'model': 'claude-3-5-sonnet-20241022',
                'temperature': 0.2,
                'max_tokens': 1024
            },
            'google': {
                'api_key': '',
                'model': 'gemini-pro',
                'temperature': 0.2
            },
            'default_provider': 'anthropic',
            'temperature': 0.2,
            'prompt': {
                'system_message': 'You are a shell command expert for {os}. Provide only the command and a one-sentence explanation.'
            },
            'security': {
                'enabled': True,
                'strict_mode': False
            },
            'history': {
                'enabled': True,
                'max_entries': 10
            }
        }
    
    def _set_nested_config(self, config: Dict[str, Any], path: List[str], value: Any):
        """Set nested configuration value"""
        current = config
        for key in path[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        current[path[-1]] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value with dot notation support"""
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value with dot notation support"""
        keys = key.split('.')
        self._set_nested_config(self.config, keys, value)
    
    def save(self) -> None:
        """Save configuration to file"""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            
            if self.config_path.endswith('.toml'):
                import tomli_w
                with open(self.config_path, 'wb') as f:
                    tomli_w.dump(self.config, f)
            else:
                with open(self.config_path, 'w') as f:
                    json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save config: {e}")


class ConversationHistory:
    """Manage conversation history and context"""
    
    def __init__(self, max_entries: int = 10):
        self.max_entries = max_entries
        self.history: List[Dict[str, Any]] = []
    
    def add_entry(self, query: str, command: str, explanation: str) -> None:
        """Add an entry to conversation history"""
        entry = {
            'query': query,
            'command': command,
            'explanation': explanation,
            'timestamp': datetime.now().isoformat()
        }
        
        self.history.append(entry)
        
        # Keep only last max_entries
        if len(self.history) > self.max_entries:
            self.history = self.history[-self.max_entries:]
    
    def get_context_string(self, entries: int = 3) -> str:
        """Get recent history as context string"""
        recent = self.history[-entries:] if self.history else []
        
        if not recent:
            return ""
        
        context_parts = []
        for entry in recent:
            context_parts.append(f"Q: {entry['query']}")
            context_parts.append(f"A: {entry['command']} ({entry['explanation']})")
        
        return '\n'.join(context_parts)
    
    def clear(self) -> None:
        """Clear conversation history"""
        self.history.clear()


if __name__ == '__main__':
    # This file provides the refactored classes
    # The main CLI interface will be in a separate file
    pass
