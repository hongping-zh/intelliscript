#!/usr/bin/env python3
"""
Enhanced Error Handling for IntelliScript
Provides comprehensive error handling with user-friendly messages
"""

import os
import sys
import traceback
from typing import Optional, Dict, Any, Callable
from dataclasses import dataclass
from enum import Enum


class ErrorType(Enum):
    """Error type categories"""
    API_KEY_MISSING = "api_key_missing"
    API_AUTHENTICATION = "api_authentication"
    API_RATE_LIMIT = "api_rate_limit"
    API_QUOTA_EXCEEDED = "api_quota_exceeded"
    NETWORK_CONNECTION = "network_connection"
    NETWORK_TIMEOUT = "network_timeout"
    CONFIGURATION_ERROR = "configuration_error"
    PERMISSION_ERROR = "permission_error"
    FILE_NOT_FOUND = "file_not_found"
    UNKNOWN_ERROR = "unknown_error"


@dataclass
class ErrorInfo:
    """Structured error information"""
    error_type: ErrorType
    title: str
    message: str
    suggestions: list[str]
    technical_details: Optional[str] = None
    help_url: Optional[str] = None


class IntelliScriptErrorHandler:
    """Comprehensive error handler with user-friendly messages"""
    
    def __init__(self, debug_mode: bool = False):
        self.debug_mode = debug_mode
        self.error_mappings = self._build_error_mappings()
    
    def _build_error_mappings(self) -> Dict[str, ErrorInfo]:
        """Build mapping of error patterns to user-friendly messages"""
        return {
            # OpenAI Errors
            "openai.AuthenticationError": ErrorInfo(
                error_type=ErrorType.API_AUTHENTICATION,
                title="🔑 OpenAI Authentication Failed",
                message="Your OpenAI API key is invalid or has expired.",
                suggestions=[
                    "Check your API key in the configuration file",
                    "Verify your API key at https://platform.openai.com/api-keys",
                    "Make sure you have sufficient credits in your OpenAI account",
                    "Try regenerating your API key if it's old"
                ],
                help_url="https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety"
            ),
            
            "openai.RateLimitError": ErrorInfo(
                error_type=ErrorType.API_RATE_LIMIT,
                title="🚦 OpenAI Rate Limit Exceeded",
                message="You've exceeded OpenAI's rate limits for API requests.",
                suggestions=[
                    "Wait a few minutes before trying again",
                    "Consider upgrading your OpenAI plan for higher limits",
                    "Implement request batching for multiple queries",
                    "Use a different provider (Claude or Gemini) as backup"
                ],
                help_url="https://help.openai.com/en/articles/5955598-is-api-usage-subject-to-any-rate-limits"
            ),
            
            "openai.APIConnectionError": ErrorInfo(
                error_type=ErrorType.NETWORK_CONNECTION,
                title="🌐 OpenAI Connection Failed",
                message="Could not connect to OpenAI's servers.",
                suggestions=[
                    "Check your internet connection",
                    "Verify you can access https://api.openai.com",
                    "Try again in a few minutes (might be temporary)",
                    "Check if your firewall/proxy is blocking the connection"
                ]
            ),
            
            # Anthropic Claude Errors
            "anthropic.AuthenticationError": ErrorInfo(
                error_type=ErrorType.API_AUTHENTICATION,
                title="🔑 Claude Authentication Failed",
                message="Your Anthropic API key is invalid or has expired.",
                suggestions=[
                    "Check your API key in the configuration file",
                    "Verify your API key at https://console.anthropic.com",
                    "Make sure your API key starts with 'sk-ant-'",
                    "Try regenerating your API key if needed"
                ],
                help_url="https://docs.anthropic.com/claude/reference/getting-started-with-the-api"
            ),
            
            "anthropic.RateLimitError": ErrorInfo(
                error_type=ErrorType.API_RATE_LIMIT,
                title="🚦 Claude Rate Limit Exceeded",
                message="You've exceeded Anthropic's rate limits for API requests.",
                suggestions=[
                    "Wait before making more requests",
                    "Check your usage at https://console.anthropic.com",
                    "Consider using shorter prompts to reduce token usage",
                    "Switch to OpenAI or Gemini temporarily"
                ]
            ),
            
            # Google API Errors  
            "google.api_core.exceptions.Unauthenticated": ErrorInfo(
                error_type=ErrorType.API_AUTHENTICATION,
                title="🔑 Google API Authentication Failed",
                message="Your Google API key is invalid or lacks proper permissions.",
                suggestions=[
                    "Verify your API key at https://console.cloud.google.com",
                    "Ensure Generative AI API is enabled for your project",
                    "Check that your API key has Gemini API permissions",
                    "Try creating a new API key with proper scopes"
                ],
                help_url="https://ai.google.dev/tutorials/setup"
            ),
            
            "google.api_core.exceptions.ResourceExhausted": ErrorInfo(
                error_type=ErrorType.API_QUOTA_EXCEEDED,
                title="📊 Google API Quota Exceeded",
                message="You've exceeded your Google API quota or rate limits.",
                suggestions=[
                    "Check your quota usage in Google Cloud Console",
                    "Wait for quota to reset (usually daily)",
                    "Request quota increase if needed",
                    "Use OpenAI or Claude as alternative"
                ]
            ),
            
            # Network Errors
            "requests.exceptions.ConnectionError": ErrorInfo(
                error_type=ErrorType.NETWORK_CONNECTION,
                title="🌐 Network Connection Failed",
                message="Could not establish network connection to AI services.",
                suggestions=[
                    "Check your internet connection",
                    "Verify DNS resolution is working",
                    "Try connecting through different network",
                    "Check if corporate firewall is blocking requests"
                ]
            ),
            
            "requests.exceptions.Timeout": ErrorInfo(
                error_type=ErrorType.NETWORK_TIMEOUT,
                title="⏱️ Request Timeout",
                message="Request to AI service timed out.",
                suggestions=[
                    "Check your internet connection speed",
                    "Try with a shorter prompt",
                    "Retry the request (might be temporary)",
                    "Switch to a different AI provider"
                ]
            ),
            
            # Configuration Errors
            "KeyError": ErrorInfo(
                error_type=ErrorType.CONFIGURATION_ERROR,
                title="⚙️ Configuration Error",
                message="Required configuration is missing or invalid.",
                suggestions=[
                    "Check your config file for missing values",
                    "Run 'intelliscript config' to set up configuration",
                    "Verify all required API keys are set",
                    "Reset configuration if corrupted"
                ]
            ),
            
            # File System Errors
            "FileNotFoundError": ErrorInfo(
                error_type=ErrorType.FILE_NOT_FOUND,
                title="📁 File Not Found",
                message="Required file or directory could not be found.",
                suggestions=[
                    "Check if the file path is correct",
                    "Verify you have read permissions",
                    "Create missing directories if needed",
                    "Check if the file was moved or deleted"
                ]
            ),
            
            "PermissionError": ErrorInfo(
                error_type=ErrorType.PERMISSION_ERROR,
                title="🔒 Permission Denied",
                message="Insufficient permissions to access file or directory.",
                suggestions=[
                    "Check file/directory permissions",
                    "Run with appropriate user privileges", 
                    "Verify you own the file/directory",
                    "Use sudo if necessary (Linux/Mac)"
                ]
            )
        }
    
    def handle_error(self, exception: Exception, context: str = "") -> ErrorInfo:
        """Handle an exception and return user-friendly error info"""
        error_class = f"{exception.__class__.__module__}.{exception.__class__.__name__}"
        error_message = str(exception).lower()
        
        # Try exact class match first
        if error_class in self.error_mappings:
            error_info = self.error_mappings[error_class]
        # Try partial class name match
        elif any(key in error_class for key in self.error_mappings.keys()):
            matching_key = next(key for key in self.error_mappings.keys() if key in error_class)
            error_info = self.error_mappings[matching_key]
        # Try error message pattern matching
        elif "authentication" in error_message or "unauthorized" in error_message:
            error_info = self._create_auth_error()
        elif "rate limit" in error_message or "too many requests" in error_message:
            error_info = self._create_rate_limit_error()
        elif "network" in error_message or "connection" in error_message:
            error_info = self._create_network_error()
        elif "api key" in error_message or "invalid key" in error_message:
            error_info = self._create_api_key_error()
        else:
            error_info = self._create_unknown_error(exception)
        
        # Add technical details if in debug mode
        if self.debug_mode:
            error_info.technical_details = f"{error_class}: {str(exception)}"
            if context:
                error_info.technical_details += f" (Context: {context})"
        
        return error_info
    
    def _create_api_key_error(self) -> ErrorInfo:
        """Create API key missing error"""
        return ErrorInfo(
            error_type=ErrorType.API_KEY_MISSING,
            title="🔑 API Key Missing",
            message="No valid API key found for any AI provider.",
            suggestions=[
                "Set your API key in the config file: ~/.config/intelliscript/config.toml",
                "Or set environment variable: OPENAI_API_KEY, ANTHROPIC_API_KEY, or GOOGLE_API_KEY",
                "Get API keys from:",
                "  - OpenAI: https://platform.openai.com/api-keys", 
                "  - Anthropic: https://console.anthropic.com",
                "  - Google: https://console.cloud.google.com"
            ]
        )
    
    def _create_auth_error(self) -> ErrorInfo:
        """Create generic authentication error"""
        return ErrorInfo(
            error_type=ErrorType.API_AUTHENTICATION,
            title="🔑 Authentication Failed",
            message="API authentication failed with current credentials.",
            suggestions=[
                "Verify your API key is correct and active",
                "Check if API key has required permissions",
                "Try regenerating your API key",
                "Ensure you have sufficient account credits/quota"
            ]
        )
    
    def _create_rate_limit_error(self) -> ErrorInfo:
        """Create generic rate limit error"""
        return ErrorInfo(
            error_type=ErrorType.API_RATE_LIMIT,
            title="🚦 Rate Limit Exceeded",
            message="You've exceeded the API rate limits.",
            suggestions=[
                "Wait a few minutes before retrying",
                "Consider upgrading your API plan",
                "Try using a different AI provider",
                "Reduce the frequency of requests"
            ]
        )
    
    def _create_network_error(self) -> ErrorInfo:
        """Create generic network error"""
        return ErrorInfo(
            error_type=ErrorType.NETWORK_CONNECTION,
            title="🌐 Network Error",
            message="Network connection to AI services failed.",
            suggestions=[
                "Check your internet connection",
                "Verify you can access external websites",
                "Try connecting from a different network",
                "Check firewall/proxy settings"
            ]
        )
    
    def _create_unknown_error(self, exception: Exception) -> ErrorInfo:
        """Create unknown error info"""
        return ErrorInfo(
            error_type=ErrorType.UNKNOWN_ERROR,
            title="❌ Unexpected Error",
            message=f"An unexpected error occurred: {type(exception).__name__}",
            suggestions=[
                "Try running the command again",
                "Check if the issue persists",
                "Report this issue if it continues",
                f"Error details: {str(exception)[:100]}..."
            ],
            technical_details=str(exception) if self.debug_mode else None
        )
    
    def print_error(self, error_info: ErrorInfo, show_suggestions: bool = True) -> None:
        """Print formatted error message to console"""
        print(f"\n{error_info.title}")
        print(f"📋 {error_info.message}")
        
        if show_suggestions and error_info.suggestions:
            print(f"\n💡 Suggested solutions:")
            for i, suggestion in enumerate(error_info.suggestions, 1):
                print(f"   {i}. {suggestion}")
        
        if error_info.help_url:
            print(f"\n📚 More help: {error_info.help_url}")
        
        if error_info.technical_details and self.debug_mode:
            print(f"\n🔧 Technical details: {error_info.technical_details}")


def validate_api_keys(config: Dict[str, Any]) -> Dict[str, str]:
    """
    Validate API keys and return validation results
    Returns dict with provider names as keys and status messages as values
    """
    results = {}
    
    # OpenAI validation
    openai_key = config.get('openai', {}).get('api_key', '')
    if openai_key:
        if openai_key.startswith('sk-') and len(openai_key) > 20:
            results['openai'] = "✅ API key format looks valid"
        else:
            results['openai'] = "⚠️ API key format seems invalid"
    else:
        results['openai'] = "❌ No API key found"
    
    # Anthropic validation  
    claude_key = config.get('anthropic', {}).get('api_key', '')
    if claude_key:
        if claude_key.startswith('sk-ant-') and len(claude_key) > 20:
            results['anthropic'] = "✅ API key format looks valid"
        else:
            results['anthropic'] = "⚠️ API key format seems invalid"
    else:
        results['anthropic'] = "❌ No API key found"
    
    # Google validation
    google_key = config.get('google', {}).get('api_key', '')
    if google_key:
        if len(google_key) > 20:  # Google keys don't have standard prefix
            results['google'] = "✅ API key found"
        else:
            results['google'] = "⚠️ API key seems too short"
    else:
        results['google'] = "❌ No API key found"
    
    return results


def check_system_requirements() -> Dict[str, str]:
    """Check system requirements and dependencies"""
    results = {}
    
    # Python version
    python_version = sys.version_info
    if python_version >= (3, 8):
        results['python'] = f"✅ Python {python_version.major}.{python_version.minor} (OK)"
    else:
        results['python'] = f"❌ Python {python_version.major}.{python_version.minor} (Need 3.8+)"
    
    # Required packages
    required_packages = [
        ('openai', 'OpenAI API client'),
        ('anthropic', 'Anthropic Claude API client'), 
        ('google-generativeai', 'Google Gemini API client'),
        ('click', 'CLI framework'),
        ('tomllib', 'TOML config support')
    ]
    
    for package, description in required_packages:
        try:
            __import__(package)
            results[package] = f"✅ {description}"
        except ImportError:
            results[package] = f"❌ {description} (pip install {package})"
    
    # Optional packages
    optional_packages = [
        ('pyperclip', 'Clipboard support'),
        ('tomli_w', 'TOML writing support')
    ]
    
    for package, description in optional_packages:
        try:
            __import__(package)
            results[package] = f"✅ {description} (optional)"
        except ImportError:
            results[package] = f"⚠️ {description} (optional - pip install {package})"
    
    return results


if __name__ == '__main__':
    # Test error handler
    handler = IntelliScriptErrorHandler(debug_mode=True)
    
    # Test with sample errors
    test_errors = [
        Exception("Invalid API key"),
        KeyError("missing_config"),
        FileNotFoundError("config.toml not found")
    ]
    
    for error in test_errors:
        error_info = handler.handle_error(error)
        handler.print_error(error_info)
        print("-" * 50)
