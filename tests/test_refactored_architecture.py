#!/usr/bin/env python3
"""
Comprehensive Test Suite for IntelliScript Refactored Architecture
Tests all major components and functionality
"""

import os
import sys
import unittest
import tempfile
import json
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Add src to path for imports
test_dir = Path(__file__).parent
project_root = test_dir.parent
src_dir = project_root / 'src'
sys.path.insert(0, str(src_dir))
sys.path.insert(0, str(project_root))

# Import from refactored architecture
try:
    from src.core.intelliscript_refactored import (
        LLMProvider, OpenAIProvider, GeminiProvider, ClaudeProvider,
        ConfigurationManager, ConversationHistory, CommandResult
    )
    from src.core.intelliscript_main import IntelliScript
    from src.utils.error_handler import IntelliScriptErrorHandler, validate_api_keys
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running from the project root directory")
    sys.exit(1)


class TestCommandResult(unittest.TestCase):
    """Test CommandResult dataclass"""
    
    def test_command_result_creation(self):
        """Test CommandResult can be created with required fields"""
        result = CommandResult(
            success=True,
            response="ls -la",
            explanation="List files in detail"
        )
        
        self.assertTrue(result.success)
        self.assertEqual(result.response, "ls -la")
        self.assertEqual(result.explanation, "List files in detail")
        self.assertEqual(result.tokens_used, 0)  # Default value
    
    def test_command_result_with_error(self):
        """Test CommandResult with error information"""
        result = CommandResult(
            success=False,
            response="",
            explanation="",
            error="API key invalid"
        )
        
        self.assertFalse(result.success)
        self.assertEqual(result.error, "API key invalid")


class TestConfigurationManager(unittest.TestCase):
    """Test ConfigurationManager functionality"""
    
    def setUp(self):
        """Set up test configuration manager with temporary file"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, 'test_config.json')
        self.config_manager = ConfigurationManager(self.config_path)
    
    def tearDown(self):
        """Clean up temporary files"""
        if os.path.exists(self.config_path):
            os.remove(self.config_path)
        os.rmdir(self.temp_dir)
    
    def test_default_config_creation(self):
        """Test default configuration is created properly"""
        config = self.config_manager.config
        
        # Check required sections exist
        self.assertIn('openai', config)
        self.assertIn('anthropic', config) 
        self.assertIn('google', config)
        self.assertIn('default_provider', config)
        
        # Check default values
        self.assertEqual(config['default_provider'], 'anthropic')
        self.assertEqual(config['temperature'], 0.2)
    
    def test_get_nested_config(self):
        """Test getting nested configuration values"""
        # Test default value
        api_key = self.config_manager.get('openai.api_key')
        self.assertEqual(api_key, '')
        
        # Test with default fallback
        missing_value = self.config_manager.get('missing.key', 'default')
        self.assertEqual(missing_value, 'default')
    
    def test_set_nested_config(self):
        """Test setting nested configuration values"""
        self.config_manager.set('openai.api_key', 'sk-test123')
        
        api_key = self.config_manager.get('openai.api_key')
        self.assertEqual(api_key, 'sk-test123')
    
    def test_config_save_and_load(self):
        """Test saving and loading configuration"""
        # Set some values
        self.config_manager.set('openai.api_key', 'sk-test123')
        self.config_manager.set('default_provider', 'openai')
        
        # Save configuration
        self.config_manager.save()
        
        # Create new manager and verify values loaded
        new_manager = ConfigurationManager(self.config_path)
        self.assertEqual(new_manager.get('openai.api_key'), 'sk-test123')
        self.assertEqual(new_manager.get('default_provider'), 'openai')


class TestConversationHistory(unittest.TestCase):
    """Test ConversationHistory functionality"""
    
    def setUp(self):
        """Set up conversation history"""
        self.history = ConversationHistory(max_entries=3)
    
    def test_add_entry(self):
        """Test adding entries to history"""
        self.history.add_entry(
            query="test query",
            command="test command", 
            explanation="test explanation"
        )
        
        self.assertEqual(len(self.history.history), 1)
        self.assertEqual(self.history.history[0]['query'], "test query")
    
    def test_max_entries_limit(self):
        """Test history respects max entries limit"""
        # Add more entries than limit
        for i in range(5):
            self.history.add_entry(f"query {i}", f"command {i}", f"explanation {i}")
        
        # Should only keep last 3 entries
        self.assertEqual(len(self.history.history), 3)
        self.assertEqual(self.history.history[0]['query'], "query 2")
        self.assertEqual(self.history.history[-1]['query'], "query 4")
    
    def test_get_context_string(self):
        """Test context string generation"""
        self.history.add_entry("query1", "command1", "explanation1")
        self.history.add_entry("query2", "command2", "explanation2")
        
        context = self.history.get_context_string(entries=2)
        
        self.assertIn("Q: query1", context)
        self.assertIn("A: command1", context)
        self.assertIn("Q: query2", context)
        self.assertIn("A: command2", context)
    
    def test_clear_history(self):
        """Test clearing history"""
        self.history.add_entry("query", "command", "explanation")
        self.assertEqual(len(self.history.history), 1)
        
        self.history.clear()
        self.assertEqual(len(self.history.history), 0)


class TestLLMProviders(unittest.TestCase):
    """Test LLM Provider implementations"""
    
    def test_openai_provider_init(self):
        """Test OpenAI provider initialization"""
        config = {'openai_model': 'gpt-4', 'temperature': 0.3}
        provider = OpenAIProvider('sk-test123', config)
        
        self.assertEqual(provider.api_key, 'sk-test123')
        self.assertEqual(provider.model, 'gpt-4')
        self.assertEqual(provider.temperature, 0.3)
    
    def test_claude_provider_init(self):
        """Test Claude provider initialization"""
        config = {'claude_model': 'claude-3-opus', 'max_tokens': 2048}
        provider = ClaudeProvider('sk-ant-test123', config)
        
        self.assertEqual(provider.api_key, 'sk-ant-test123')
        self.assertEqual(provider.model, 'claude-3-opus')
        self.assertEqual(provider.max_tokens, 2048)
    
    def test_gemini_provider_init(self):
        """Test Gemini provider initialization"""
        config = {'gemini_model': 'gemini-pro-vision', 'temperature': 0.1}
        provider = GeminiProvider('test-api-key', config)
        
        self.assertEqual(provider.api_key, 'test-api-key')
        self.assertEqual(provider.model, 'gemini-pro-vision')
        self.assertEqual(provider.temperature, 0.1)
    
    def test_provider_availability_check(self):
        """Test provider availability checking"""
        # Valid OpenAI key
        openai_provider = OpenAIProvider('sk-validkey123', {})
        self.assertTrue(openai_provider.is_available())
        
        # Invalid OpenAI key
        invalid_openai = OpenAIProvider('invalid-key', {})
        self.assertFalse(invalid_openai.is_available())
        
        # Valid Claude key
        claude_provider = ClaudeProvider('sk-ant-validkey123', {})
        self.assertTrue(claude_provider.is_available())
        
        # Invalid Claude key  
        invalid_claude = ClaudeProvider('invalid-key', {})
        self.assertFalse(invalid_claude.is_available())


class TestErrorHandler(unittest.TestCase):
    """Test IntelliScriptErrorHandler functionality"""
    
    def setUp(self):
        """Set up error handler"""
        self.handler = IntelliScriptErrorHandler(debug_mode=True)
    
    def test_api_key_missing_error(self):
        """Test API key missing error handling"""
        error = Exception("Invalid API key")
        error_info = self.handler.handle_error(error)
        
        self.assertIn("Authentication", error_info.title)
        self.assertTrue(len(error_info.suggestions) > 0)
    
    def test_network_error_handling(self):
        """Test network error handling"""
        import requests
        error = requests.exceptions.ConnectionError("Connection failed")
        error_info = self.handler.handle_error(error)
        
        self.assertIn("Connection", error_info.title)
        self.assertIn("Check your internet connection", ' '.join(error_info.suggestions))
    
    def test_configuration_error_handling(self):
        """Test configuration error handling"""
        error = KeyError("missing_config_key")
        error_info = self.handler.handle_error(error)
        
        self.assertIn("Configuration", error_info.title)
        self.assertTrue(len(error_info.suggestions) > 0)


class TestAPIKeyValidation(unittest.TestCase):
    """Test API key validation functionality"""
    
    def test_openai_key_validation(self):
        """Test OpenAI key validation"""
        config = {
            'openai': {'api_key': 'sk-validkeyformat123'},
            'anthropic': {'api_key': ''},
            'google': {'api_key': ''}
        }
        
        results = validate_api_keys(config)
        
        self.assertIn("✅", results['openai'])
        self.assertIn("❌", results['anthropic'])
        self.assertIn("❌", results['google'])
    
    def test_claude_key_validation(self):
        """Test Claude key validation"""
        config = {
            'openai': {'api_key': ''},
            'anthropic': {'api_key': 'sk-ant-validkeyformat123'},
            'google': {'api_key': ''}
        }
        
        results = validate_api_keys(config)
        
        self.assertIn("❌", results['openai'])
        self.assertIn("✅", results['anthropic'])
        self.assertIn("❌", results['google'])
    
    def test_google_key_validation(self):
        """Test Google key validation"""
        config = {
            'openai': {'api_key': ''},
            'anthropic': {'api_key': ''},
            'google': {'api_key': 'validgooglekeyformat123456'}
        }
        
        results = validate_api_keys(config)
        
        self.assertIn("❌", results['openai'])
        self.assertIn("❌", results['anthropic'])
        self.assertIn("✅", results['google'])


class TestIntelliScriptMainClass(unittest.TestCase):
    """Test main IntelliScript class"""
    
    def setUp(self):
        """Set up test IntelliScript instance"""
        # Create temporary config
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, 'test_config.json')
        
        # Mock config with test API key
        test_config = {
            'openai': {'api_key': 'sk-test123', 'model': 'gpt-4'},
            'anthropic': {'api_key': 'sk-ant-test123', 'model': 'claude-3-sonnet'},
            'google': {'api_key': 'test-google-key', 'model': 'gemini-pro'},
            'default_provider': 'openai',
            'temperature': 0.2,
            'security': {'enabled': True},
            'history': {'max_entries': 5, 'enabled': True}
        }
        
        with open(self.config_path, 'w') as f:
            json.dump(test_config, f)
        
        self.intelliscript = IntelliScript(self.config_path)
    
    def tearDown(self):
        """Clean up temporary files"""
        if os.path.exists(self.config_path):
            os.remove(self.config_path)
        os.rmdir(self.temp_dir)
    
    def test_provider_initialization(self):
        """Test providers are initialized correctly"""
        # Should have providers for all configured keys
        self.assertIn('openai', self.intelliscript.providers)
        self.assertIn('anthropic', self.intelliscript.providers) 
        self.assertIn('google', self.intelliscript.providers)
        
        # Should have current provider set
        self.assertIsNotNone(self.intelliscript.current_provider)
    
    def test_parse_arguments(self):
        """Test argument parsing"""
        test_args = ['--provider', 'openai', '--temperature', '0.5', 'find all python files']
        parsed = self.intelliscript._parse_arguments(test_args)
        
        self.assertEqual(parsed['provider'], 'openai')
        self.assertEqual(parsed['temperature'], 0.5)
        self.assertEqual(parsed['query'], 'find all python files')
    
    def test_api_key_retrieval(self):
        """Test API key retrieval for different providers"""
        openai_key = self.intelliscript._get_api_key('openai')
        claude_key = self.intelliscript._get_api_key('anthropic')
        google_key = self.intelliscript._get_api_key('google')
        
        self.assertEqual(openai_key, 'sk-test123')
        self.assertEqual(claude_key, 'sk-ant-test123')
        self.assertEqual(google_key, 'test-google-key')
    
    def test_prompt_building(self):
        """Test prompt building with context"""
        # Test without context
        context = self.intelliscript._build_prompt("test query", "Linux", use_context=False)
        
        self.assertEqual(context['query'], "test query")
        self.assertEqual(context['os_info'], "Linux")
        self.assertNotIn('history', context)
        
        # Add some history and test with context
        self.intelliscript.conversation_history.add_entry(
            "previous query", "previous command", "previous explanation"
        )
        
        context_with_history = self.intelliscript._build_prompt(
            "follow up query", "Linux", use_context=True
        )
        
        self.assertIn('history', context_with_history)
        self.assertIn('previous query', context_with_history['history'])
    
    @patch('subprocess.run')
    def test_command_execution(self):
        """Test command execution with mocked subprocess"""
        # Mock successful execution
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "Command executed successfully"
        mock_result.stderr = ""
        
        with patch('subprocess.run', return_value=mock_result):
            result = self.intelliscript._execute_command("ls -la")
            self.assertIn("successfully", result)
    
    @patch('pyperclip.copy')
    def test_copy_command(self):
        """Test copying command to clipboard"""
        with patch('pyperclip.copy') as mock_copy:
            result = self.intelliscript._copy_command("test command")
            mock_copy.assert_called_once_with("test command")
            self.assertIn("copied", result)


class TestIntegrationScenarios(unittest.TestCase):
    """Test integration scenarios and workflows"""
    
    def setUp(self):
        """Set up for integration tests"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, 'integration_config.json')
        
        # Create minimal valid config
        test_config = {
            'openai': {'api_key': 'sk-test123'},
            'default_provider': 'openai',
            'security': {'enabled': True}
        }
        
        with open(self.config_path, 'w') as f:
            json.dump(test_config, f)
    
    def tearDown(self):
        """Clean up"""
        if os.path.exists(self.config_path):
            os.remove(self.config_path)
        os.rmdir(self.temp_dir)
    
    @patch('core.intelliscript_refactored.openai')
    def test_end_to_end_query_processing(self):
        """Test complete query processing workflow"""
        # Mock OpenAI response
        mock_response = Mock()
        mock_response.choices[0].message.content = "Command: ls -la\nExplanation: List files"
        mock_response.usage.total_tokens = 50
        
        with patch('core.intelliscript_refactored.openai.ChatCompletion.create', 
                  return_value=mock_response):
            
            app = IntelliScript(self.config_path)
            
            # Test calling LLM
            result = app._call_llm("show me files", provider='openai')
            
            self.assertTrue(result.success)
            self.assertEqual(result.response, "ls -la")
            self.assertEqual(result.explanation, "List files")
            self.assertEqual(result.tokens_used, 50)


def run_manual_tests():
    """Run manual tests that require user interaction or real API calls"""
    print("🧪 Running Manual Tests (for development)")
    print("=" * 50)
    
    # Test configuration loading
    print("1. Testing configuration loading...")
    try:
        config_manager = ConfigurationManager()
        print(f"   ✅ Config loaded from: {config_manager.config_path}")
        print(f"   ✅ Default provider: {config_manager.get('default_provider')}")
    except Exception as e:
        print(f"   ❌ Config loading failed: {e}")
    
    # Test error handler
    print("\n2. Testing error handler...")
    try:
        handler = IntelliScriptErrorHandler(debug_mode=True)
        test_error = Exception("Test error")
        error_info = handler.handle_error(test_error)
        print(f"   ✅ Error handled: {error_info.title}")
    except Exception as e:
        print(f"   ❌ Error handler failed: {e}")
    
    # Test conversation history
    print("\n3. Testing conversation history...")
    try:
        history = ConversationHistory()
        history.add_entry("test query", "test command", "test explanation")
        context = history.get_context_string()
        print(f"   ✅ History working: {len(history.history)} entries")
    except Exception as e:
        print(f"   ❌ History failed: {e}")
    
    print("\n✅ Manual tests completed!")


if __name__ == '__main__':
    print("🚀 IntelliScript Refactored Architecture Test Suite")
    print("=" * 60)
    
    # Run unit tests
    print("\n🧪 Running Unit Tests...")
    unittest.main(verbosity=2, exit=False)
    
    # Run manual tests
    print("\n" + "=" * 60)
    run_manual_tests()
