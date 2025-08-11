"""
Security module for IntelliScript CLI

Provides command safety checking and dangerous command detection
"""

from .command_safety import (
    CommandSafetyChecker,
    RiskLevel, 
    DangerousCommand,
    check_command_safety,
    analyze_command_risks,
    get_safety_checker
)

__all__ = [
    'CommandSafetyChecker',
    'RiskLevel',
    'DangerousCommand', 
    'check_command_safety',
    'analyze_command_risks',
    'get_safety_checker'
]
