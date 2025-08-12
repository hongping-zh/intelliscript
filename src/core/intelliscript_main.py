#!/usr/bin/env python3
"""
IntelliScript Main Class - Refactored with single responsibility functions
Implements clean separation of concerns as requested
"""

import os
import sys
import time
import platform
import subprocess
from typing import Dict, Any, Optional, Tuple
from datetime import datetime

# Import the refactored components
from .intelliscript_refactored import (
    LLMProvider, OpenAIProvider, ClaudeProvider, GeminiProvider, OllamaProvider,
    ConfigurationManager, ConversationHistory, CommandResult
)

# Import existing security module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from security.command_safety import check_command_safety, analyze_command_risks


class IntelliScript:
    """
    Main IntelliScript application class
    Encapsulates all application state and logic with clean separation of concerns
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize IntelliScript with configuration"""
        self.config_manager = ConfigurationManager(config_path)
        self.conversation_history = ConversationHistory(
            max_entries=self.config_manager.get('history.max_entries', 10)
        )
        self.providers: Dict[str, LLMProvider] = {}
        self.current_provider: Optional[LLMProvider] = None
        self.last_command: str = ""
        self.last_explanation: str = ""
        
        # Initialize providers
        self._initialize_providers()
    
    def _initialize_providers(self) -> None:
        """Initialize available LLM providers"""
        # OpenAI Provider
        openai_key = self.config_manager.get('openai.api_key')
        if openai_key:
            self.providers['openai'] = OpenAIProvider(openai_key, self.config_manager.config)
        
        # Anthropic Claude Provider
        claude_key = self.config_manager.get('anthropic.api_key')
        if claude_key:
            self.providers['anthropic'] = ClaudeProvider(claude_key, self.config_manager.config)
        
        # Google Gemini Provider
        gemini_key = self.config_manager.get('google.api_key')
        if gemini_key:
            self.providers['google'] = GeminiProvider(gemini_key, self.config_manager.config)
        
        # Ollama Provider (local models - no API key required)
        if self.config_manager.get('ollama.enabled', True):
            self.providers['ollama'] = OllamaProvider('', self.config_manager.config)
        
        # Set default provider
        default_provider = self.config_manager.get('default_provider', 'anthropic')
        if default_provider in self.providers:
            self.current_provider = self.providers[default_provider]
        elif self.providers:
            # Use first available provider
            self.current_provider = list(self.providers.values())[0]
    
    def _parse_arguments(self, args: list) -> Dict[str, Any]:
        """Parse command line arguments - single responsibility function"""
        import argparse
        
        parser = argparse.ArgumentParser(
            description='IntelliScript - AI-powered shell command assistant',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  is "find all python files"
  is "show disk usage" --provider openai
  is "compress folder" --save backup.sh
  is "list docker containers" --context
            """
        )
        
        parser.add_argument('query', nargs='*', help='Natural language query')
        parser.add_argument('--provider', choices=['openai', 'anthropic', 'google', 'ollama'], 
                          help='LLM provider to use')
        parser.add_argument('--model', help='Specific model name')
        parser.add_argument('--temperature', type=float, help='Temperature for AI responses')
        parser.add_argument('--save', metavar='FILE', help='Save command to script file')
        parser.add_argument('--context', action='store_true', 
                          help='Use conversation history as context')
        parser.add_argument('--config', help='Path to config file')
        parser.add_argument('--no-safety', action='store_true', 
                          help='Disable safety checks (dangerous)')
        parser.add_argument('--version', action='version', version='IntelliScript 2.0.0')
        
        parsed_args = parser.parse_args(args)
        
        # Join query parts into single string
        if parsed_args.query:
            parsed_args.query = ' '.join(parsed_args.query)
        
        return vars(parsed_args)
    
    def _get_api_key(self, provider: str) -> Optional[str]:
        """Get and validate API key for provider - single responsibility function"""
        key_mapping = {
            'openai': 'openai.api_key',
            'anthropic': 'anthropic.api_key', 
            'google': 'google.api_key'
        }
        
        if provider not in key_mapping:
            return None
        
        api_key = self.config_manager.get(key_mapping[provider])
        
        if not api_key:
            # Try environment variables as fallback
            env_vars = {
                'openai': 'OPENAI_API_KEY',
                'anthropic': 'ANTHROPIC_API_KEY',
                'google': 'GOOGLE_API_KEY'
            }
            api_key = os.getenv(env_vars.get(provider, ''))
        
        return api_key
    
    def _build_prompt(self, query: str, os_info: str, use_context: bool = False) -> Dict[str, Any]:
        """Build prompt context for LLM - single responsibility function"""
        context = {
            'os_info': os_info,
            'query': query,
            'timestamp': datetime.now().isoformat()
        }
        
        if use_context and self.conversation_history.history:
            context['history'] = self.conversation_history.get_context_string()
        
        return context
    
    def _call_llm(self, query: str, provider: Optional[str] = None, 
                  use_context: bool = False) -> CommandResult:
        """Call LLM and get command - single responsibility function"""
        # Determine which provider to use
        if provider and provider in self.providers:
            llm_provider = self.providers[provider]
        elif self.current_provider:
            llm_provider = self.current_provider
        else:
            return CommandResult(
                success=False,
                response="",
                explanation="",
                error="No LLM provider available. Please configure API keys."
            )
        
        # Get system information
        os_info = platform.system()
        
        # Build context
        context = self._build_prompt(query, os_info, use_context)
        
        # Record start time for metrics
        start_time = time.time()
        
        try:
            # Call the LLM provider
            result = llm_provider.get_command(query, context)
            result.response_time = int((time.time() - start_time) * 1000)
            
            # Store for potential revision
            if result.success:
                self.last_command = result.response
                self.last_explanation = result.explanation
            
            return result
            
        except Exception as e:
            return CommandResult(
                success=False,
                response="",
                explanation="",
                error=f"Error calling {llm_provider.get_model_name()}: {str(e)}",
                response_time=int((time.time() - start_time) * 1000)
            )
    
    def _check_command_safety(self, command: str, strict_mode: bool = False) -> Tuple[bool, str]:
        """Check command safety - single responsibility function"""
        if not self.config_manager.get('security.enabled', True):
            return True, "Safety checks disabled"
        
        try:
            # Use existing security module
            is_safe = check_command_safety(command)
            
            if not is_safe:
                risk_info = analyze_command_risks(command)
                risk_level = risk_info.get('level', 'HIGH')
                risk_reason = risk_info.get('reason', 'Potentially dangerous command detected')
                
                return False, f"🛡️ {risk_level} RISK: {risk_reason}"
            
            return True, "Command passed safety checks"
            
        except Exception as e:
            # If security check fails, err on the side of caution
            return False, f"Safety check failed: {str(e)}"
    
    def _handle_user_interaction(self, command: str, explanation: str, 
                                save_file: Optional[str] = None) -> str:
        """Handle user interaction for command execution - single responsibility function"""
        print(f"\n🤖 Generated Command:")
        print(f"📋 {command}")
        print(f"💡 Explanation: {explanation}\n")
        
        while True:
            choice = input("Choose action: [E]xecute, [C]opy, [R]evise, [S]ave, [A]bort: ").strip().lower()
            
            if choice in ['e', 'execute']:
                return self._execute_command(command)
            
            elif choice in ['c', 'copy']:
                return self._copy_command(command)
            
            elif choice in ['r', 'revise']:
                return self._revise_command()
            
            elif choice in ['s', 'save']:
                return self._save_command(command, explanation, save_file)
            
            elif choice in ['a', 'abort']:
                return "❌ Command aborted by user"
            
            else:
                print("Invalid choice. Please enter E, C, R, S, or A.")
    
    def _execute_command(self, command: str) -> str:
        """Execute command safely"""
        try:
            print(f"🚀 Executing: {command}")
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            
            if result.returncode == 0:
                print(f"✅ Command executed successfully")
                if result.stdout:
                    print(f"Output:\n{result.stdout}")
                return "Command executed successfully"
            else:
                print(f"❌ Command failed with exit code {result.returncode}")
                if result.stderr:
                    print(f"Error:\n{result.stderr}")
                return f"Command failed: {result.stderr}"
                
        except subprocess.TimeoutExpired:
            return "❌ Command timed out after 30 seconds"
        except Exception as e:
            return f"❌ Execution error: {str(e)}"
    
    def _copy_command(self, command: str) -> str:
        """Copy command to clipboard"""
        try:
            import pyperclip
            pyperclip.copy(command)
            return "📋 Command copied to clipboard"
        except ImportError:
            print(f"📋 Copy this command manually: {command}")
            return "Command ready to copy (pyperclip not available)"
        except Exception as e:
            return f"❌ Copy failed: {str(e)}"
    
    def _revise_command(self) -> str:
        """Handle command revision"""
        revision_query = input("\n🔄 Enter revision request: ").strip()
        if not revision_query:
            return "❌ No revision specified"
        
        # Use the revision as a follow-up query with context
        print("\n🔄 Revising command...")
        result = self._call_llm(revision_query, use_context=True)
        
        if result.success:
            # Check safety of revised command
            is_safe, safety_msg = self._check_command_safety(result.response)
            
            if not is_safe:
                print(f"\n{safety_msg}")
                confirm = input("Continue anyway? (type 'YES' to confirm): ")
                if confirm != 'YES':
                    return "❌ Revised command blocked for safety"
            
            return self._handle_user_interaction(result.response, result.explanation)
        else:
            return f"❌ Revision failed: {result.error}"
    
    def _save_command(self, command: str, explanation: str, 
                     save_file: Optional[str] = None) -> str:
        """Save command to script file"""
        if not save_file:
            save_file = input("Enter filename (or press Enter for auto-name): ").strip()
        
        if not save_file:
            # Auto-generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_file = f"intelliscript_{timestamp}.sh"
        
        try:
            script_content = f"""#!/bin/bash
# Generated by IntelliScript
# Date: {datetime.now().isoformat()}
# Explanation: {explanation}

{command}
"""
            
            with open(save_file, 'w') as f:
                f.write(script_content)
            
            # Make executable on Unix systems
            if os.name != 'nt':
                os.chmod(save_file, 0o755)
            
            return f"💾 Command saved to {save_file}"
            
        except Exception as e:
            return f"❌ Save failed: {str(e)}"
    
    def run(self, args: list) -> int:
        """Main application entry point"""
        try:
            # Parse arguments
            parsed_args = self._parse_arguments(args)
            
            # Handle config file override
            if parsed_args.get('config'):
                self.config_manager = ConfigurationManager(parsed_args['config'])
                self._initialize_providers()
            
            # Check if we have any providers
            if not self.providers:
                print("❌ No LLM providers configured!")
                print("Please set up API keys in config file or environment variables:")
                print("  - OPENAI_API_KEY for OpenAI GPT models")
                print("  - ANTHROPIC_API_KEY for Claude models")
                print("  - GOOGLE_API_KEY for Gemini models")
                return 1
            
            # Get query
            query = parsed_args.get('query')
            if not query:
                query = input("🤖 Enter your command request: ").strip()
                if not query:
                    print("❌ No query provided")
                    return 1
            
            print(f"\n🔍 Processing: {query}")
            
            # Call LLM
            result = self._call_llm(
                query=query,
                provider=parsed_args.get('provider'),
                use_context=parsed_args.get('context', False)
            )
            
            if not result.success:
                print(f"❌ Failed to get command: {result.error}")
                return 1
            
            # Check command safety (unless disabled)
            if not parsed_args.get('no_safety', False):
                is_safe, safety_msg = self._check_command_safety(result.response)
                
                if not is_safe:
                    print(f"\n{safety_msg}")
                    confirm = input("Execute anyway? (type 'YES' to confirm): ")
                    if confirm != 'YES':
                        print("❌ Command blocked for safety")
                        return 1
            
            # Handle user interaction
            interaction_result = self._handle_user_interaction(
                result.response, 
                result.explanation,
                parsed_args.get('save')
            )
            
            # Add to conversation history
            self.conversation_history.add_entry(query, result.response, result.explanation)
            
            print(f"\n{interaction_result}")
            return 0
            
        except KeyboardInterrupt:
            print("\n❌ Interrupted by user")
            return 1
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
            return 1


def main():
    """CLI entry point"""
    import sys
    app = IntelliScript()
    return app.run(sys.argv[1:])


if __name__ == '__main__':
    exit(main())
