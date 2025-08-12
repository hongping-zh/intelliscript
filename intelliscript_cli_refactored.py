#!/usr/bin/env python3
"""
IntelliScript CLI - Refactored Version  
Enhanced with improved architecture, error handling, and multi-provider support
Replaces the original intelliscript_cli_enhanced.py with better structure
"""

import os
import sys
import time
import platform
from pathlib import Path

# Add src to path for imports
current_dir = Path(__file__).parent
src_dir = current_dir / 'src'
sys.path.insert(0, str(src_dir))

# Import refactored components
try:
    from src.core.intelliscript_main import IntelliScript
    from src.utils.error_handler import IntelliScriptErrorHandler, validate_api_keys, check_system_requirements
    from src.core.intelliscript_refactored import ConfigurationManager
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running from the IntelliScript directory")
    sys.exit(1)


def setup_configuration():
    """Interactive configuration setup for first-time users"""
    print("🚀 Welcome to IntelliScript!")
    print("Let's set up your configuration...\n")
    
    config_manager = ConfigurationManager()
    
    # Check current configuration
    print("📋 Checking current configuration...")
    validation_results = validate_api_keys(config_manager.config)
    
    has_valid_key = any("✅" in result for result in validation_results.values())
    
    if has_valid_key:
        print("✅ You already have some API keys configured!")
        for provider, status in validation_results.items():
            print(f"   {provider}: {status}")
        
        proceed = input("\nWould you like to update your configuration? (y/n): ").strip().lower()
        if proceed != 'y':
            return config_manager
    else:
        print("⚠️ No valid API keys found. Let's set one up!")
    
    print("\n🔑 API Key Setup")
    print("You need at least one API key from these providers:")
    print("1. OpenAI (GPT-4, ChatGPT) - https://platform.openai.com/api-keys")
    print("2. Anthropic (Claude) - https://console.anthropic.com")  
    print("3. Google (Gemini) - https://console.cloud.google.com")
    
    # OpenAI setup
    setup_openai = input("\nSet up OpenAI API key? (y/n): ").strip().lower() == 'y'
    if setup_openai:
        openai_key = input("Enter your OpenAI API key (sk-...): ").strip()
        if openai_key and openai_key.startswith('sk-'):
            config_manager.set('openai.api_key', openai_key)
            print("✅ OpenAI key saved!")
        else:
            print("⚠️ Invalid OpenAI key format")
    
    # Anthropic setup  
    setup_claude = input("Set up Anthropic Claude API key? (y/n): ").strip().lower() == 'y'
    if setup_claude:
        claude_key = input("Enter your Claude API key (sk-ant-...): ").strip()
        if claude_key and claude_key.startswith('sk-ant-'):
            config_manager.set('anthropic.api_key', claude_key)
            print("✅ Claude key saved!")
        else:
            print("⚠️ Invalid Claude key format")
    
    # Google setup
    setup_google = input("Set up Google Gemini API key? (y/n): ").strip().lower() == 'y'
    if setup_google:
        google_key = input("Enter your Google API key: ").strip()
        if google_key and len(google_key) > 20:
            config_manager.set('google.api_key', google_key)
            print("✅ Google key saved!")
        else:
            print("⚠️ Key seems too short")
    
    # Default provider selection
    available_providers = []
    if config_manager.get('openai.api_key'):
        available_providers.append('openai')
    if config_manager.get('anthropic.api_key'):
        available_providers.append('anthropic')
    if config_manager.get('google.api_key'):
        available_providers.append('google')
    
    if available_providers:
        print(f"\n🎯 Choose default provider:")
        for i, provider in enumerate(available_providers, 1):
            print(f"{i}. {provider.title()}")
        
        try:
            choice = int(input("Enter choice (number): ")) - 1
            if 0 <= choice < len(available_providers):
                config_manager.set('default_provider', available_providers[choice])
                print(f"✅ Default provider set to {available_providers[choice]}")
        except (ValueError, IndexError):
            print("⚠️ Invalid choice, keeping current default")
    
    # Save configuration
    config_manager.save()
    print(f"\n💾 Configuration saved to: {config_manager.config_path}")
    
    return config_manager


def run_diagnostics():
    """Run system diagnostics and show status"""
    print("🔧 IntelliScript System Diagnostics\n")
    
    # Check system requirements
    print("📋 System Requirements:")
    sys_requirements = check_system_requirements()
    for component, status in sys_requirements.items():
        print(f"   {component}: {status}")
    
    # Check configuration
    print("\n⚙️ Configuration Status:")
    config_manager = ConfigurationManager()
    
    if os.path.exists(config_manager.config_path):
        print(f"   ✅ Config file: {config_manager.config_path}")
    else:
        print(f"   ❌ Config file not found: {config_manager.config_path}")
        print("   Run 'intelliscript config' to create one")
    
    # Check API keys
    print("\n🔑 API Key Status:")
    validation_results = validate_api_keys(config_manager.config)
    for provider, status in validation_results.items():
        print(f"   {provider}: {status}")
    
    # Check permissions
    print("\n🔒 Permissions:")
    config_dir = os.path.dirname(config_manager.config_path)
    if os.access(config_dir, os.W_OK):
        print("   ✅ Config directory writable")
    else:
        print("   ❌ Config directory not writable")
    
    print(f"\n🖥️ System Info:")
    print(f"   OS: {platform.system()} {platform.release()}")
    print(f"   Python: {sys.version.split()[0]}")
    print(f"   IntelliScript: 2.0.0 (Refactored)")


def main():
    """Main CLI entry point with comprehensive error handling"""
    error_handler = IntelliScriptErrorHandler(debug_mode='--debug' in sys.argv)
    
    try:
        # Handle special commands first
        if len(sys.argv) > 1:
            first_arg = sys.argv[1].lower()
            
            if first_arg in ['config', 'setup', 'configure']:
                setup_configuration()
                return 0
            
            elif first_arg in ['diag', 'diagnostics', 'doctor', 'check']:
                run_diagnostics() 
                return 0
            
            elif first_arg in ['help', '--help', '-h']:
                print_help()
                return 0
            
            elif first_arg in ['version', '--version', '-v']:
                print("IntelliScript 2.0.0 (Refactored)")
                print("AI-powered shell command assistant")
                return 0
        
        # Initialize main application
        app = IntelliScript()
        
        # Check if any providers are available
        if not app.providers:
            print("❌ No AI providers configured!")
            print("\nTo get started:")
            print("1. Run: intelliscript config")
            print("2. Or set environment variables:")
            print("   export OPENAI_API_KEY='your-key-here'")
            print("   export ANTHROPIC_API_KEY='your-key-here'") 
            print("   export GOOGLE_API_KEY='your-key-here'")
            return 1
        
        # Run main application
        return app.run(sys.argv[1:])
        
    except KeyboardInterrupt:
        print("\n❌ Interrupted by user")
        return 1
        
    except Exception as e:
        error_info = error_handler.handle_error(e, "main application")
        error_handler.print_error(error_info)
        
        if error_handler.debug_mode:
            import traceback
            print(f"\n🔧 Full traceback:")
            traceback.print_exc()
        
        return 1


def print_help():
    """Print comprehensive help information"""
    help_text = """
🚀 IntelliScript 2.0.0 - AI-Powered Shell Command Assistant

USAGE:
  intelliscript [OPTIONS] <query>
  intelliscript <command>

COMMANDS:
  config, setup       Interactive configuration setup
  diag, doctor       Run system diagnostics  
  help               Show this help message
  version            Show version information

QUERY OPTIONS:
  --provider PROVIDER    Choose AI provider: openai, anthropic, google
  --model MODEL         Specific model name (e.g., gpt-4-turbo)
  --temperature TEMP    Creativity level (0.0-2.0)
  --save FILE           Save command to script file
  --context             Use conversation history as context
  --no-safety          Disable safety checks (dangerous!)
  --debug              Enable debug mode

EXAMPLES:
  Basic usage:
    intelliscript "find all python files"
    intelliscript "show disk usage"
    
  With specific provider:
    intelliscript "list docker containers" --provider openai
    intelliscript "compress this folder" --provider anthropic
    
  Save to script:
    intelliscript "backup all logs" --save backup.sh
    
  With context (follow-up questions):
    intelliscript "show running processes" --context
    intelliscript "now kill the python ones" --context

CONFIGURATION:
  Config file: ~/.config/intelliscript/config.toml
  Environment variables: OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY
  
  Run 'intelliscript config' for interactive setup

SAFETY:
  IntelliScript includes built-in safety checks to prevent dangerous commands.
  Commands like 'rm -rf /', 'mkfs', 'dd if=/dev/zero' are blocked by default.
  Use --no-safety to disable (NOT recommended).

MORE INFO:
  Documentation: https://github.com/your-repo/intelliscript
  Issues: https://github.com/your-repo/intelliscript/issues
"""
    print(help_text)


# Legacy compatibility - redirect old imports
def cli():
    """Legacy CLI function for backwards compatibility"""
    return main()


if __name__ == '__main__':
    exit(main())
