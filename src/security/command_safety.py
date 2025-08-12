#!/usr/bin/env python3
"""
Dangerous Command Detection and Safety Layer for IntelliScript CLI

This module provides comprehensive protection against potentially dangerous commands
that AI might generate, including file system operations, disk operations, and
system-level commands that could cause data loss or system damage.
"""

import re
import os
import sys
import hashlib
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

try:
    import colorama
    from colorama import Fore, Back, Style
    colorama.init(autoreset=True)
    COLOR_SUPPORT = True
except ImportError:
    COLOR_SUPPORT = False
    # Fallback color constants
    class Fore:
        RED = ""
        YELLOW = ""
        GREEN = ""
        CYAN = ""
        RESET = ""
    
    class Back:
        RED = ""
        YELLOW = ""
        
    class Style:
        BRIGHT = ""
        RESET_ALL = ""


class RiskLevel(Enum):
    """Risk levels for dangerous commands"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class DangerousCommand:
    """Represents a dangerous command pattern"""
    pattern: str
    risk_level: RiskLevel
    description: str
    examples: List[str]
    category: str


class CommandSafetyChecker:
    """
    Advanced safety checker for dangerous commands with multi-layered protection
    """
    
    def __init__(self):
        self.dangerous_patterns = self._initialize_dangerous_patterns()
        self.whitelist_patterns = self._initialize_whitelist_patterns()
        self.confirmation_cache = {}  # Cache for confirmed dangerous commands
        
    def _initialize_dangerous_patterns(self) -> List[DangerousCommand]:
        """Initialize comprehensive list of dangerous command patterns"""
        return [
            # File System Destruction
            DangerousCommand(
                pattern=r'\brm\s+(-[rfRF]*\s+)*(/|~|\$HOME|\.\.)',
                risk_level=RiskLevel.CRITICAL,
                description="Recursive file deletion targeting system or user directories",
                examples=["rm -rf /", "rm -rf ~", "rm -rf /home", "rm -rf ../"],
                category="File System Destruction"
            ),
            DangerousCommand(
                pattern=r'\brm\s+(-[rfRF]*\s+)*/\w*',
                risk_level=RiskLevel.HIGH,
                description="File deletion in root directory",
                examples=["rm -rf /bin", "rm -rf /usr", "rm -rf /etc"],
                category="File System Destruction"
            ),
            DangerousCommand(
                pattern=r'\brmdir\s+(-[rfRF]*\s+)*(/|~)',
                risk_level=RiskLevel.HIGH,
                description="Directory removal targeting system directories",
                examples=["rmdir -rf /", "rmdir ~/"],
                category="File System Destruction"
            ),
            
            # Disk Operations
            DangerousCommand(
                pattern=r'\bmkfs\.',
                risk_level=RiskLevel.CRITICAL,
                description="File system formatting (destroys all data on disk)",
                examples=["mkfs.ext4 /dev/sda1", "mkfs.xfs /dev/sdb"],
                category="Disk Operations"
            ),
            DangerousCommand(
                pattern=r'>\s*/dev/sd[a-z]\d*',
                risk_level=RiskLevel.CRITICAL,
                description="Direct write to disk device (data destruction)",
                examples=["> /dev/sda", "echo 'data' > /dev/sdb1"],
                category="Disk Operations"
            ),
            DangerousCommand(
                pattern=r'\bdd\s+.*of=/dev/sd[a-z]',
                risk_level=RiskLevel.CRITICAL,
                description="Direct disk writing with dd command",
                examples=["dd if=/dev/zero of=/dev/sda", "dd if=image.iso of=/dev/sdb"],
                category="Disk Operations"
            ),
            DangerousCommand(
                pattern=r'\bfdisk\s+/dev/sd[a-z]',
                risk_level=RiskLevel.HIGH,
                description="Disk partitioning operations",
                examples=["fdisk /dev/sda", "fdisk -l /dev/sdb"],
                category="Disk Operations"
            ),
            
            # System Control
            DangerousCommand(
                pattern=r'\b(shutdown|poweroff|reboot|halt)\b',
                risk_level=RiskLevel.MEDIUM,
                description="System shutdown/restart commands",
                examples=["shutdown -h now", "reboot", "poweroff"],
                category="System Control"
            ),
            DangerousCommand(
                pattern=r'\bkillall\s+(-9\s+)*\w',
                risk_level=RiskLevel.MEDIUM,
                description="Mass process termination",
                examples=["killall -9 python", "killall chrome"],
                category="System Control"
            ),
            DangerousCommand(
                pattern=r'\bkill\s+(-9\s+)*1\b',
                risk_level=RiskLevel.CRITICAL,
                description="Killing init process (system crash)",
                examples=["kill -9 1", "kill 1"],
                category="System Control"
            ),
            
            # Network and Security
            DangerousCommand(
                pattern=r'\biptables\s+(-F|-X|--flush)',
                risk_level=RiskLevel.HIGH,
                description="Firewall rules deletion",
                examples=["iptables -F", "iptables --flush"],
                category="Network Security"
            ),
            DangerousCommand(
                pattern=r'\bchmod\s+(777|666)\s+(/|~|\$HOME)',
                risk_level=RiskLevel.HIGH,
                description="Dangerous permission changes on system directories",
                examples=["chmod 777 /", "chmod 666 ~/"],
                category="File Permissions"
            ),
            DangerousCommand(
                pattern=r'\bchown\s+.*:\s*(/|~|\$HOME)',
                risk_level=RiskLevel.HIGH,
                description="Ownership changes on system directories",
                examples=["chown user: /", "chown nobody ~/"],
                category="File Permissions"
            ),
            
            # Data Destruction
            DangerousCommand(
                pattern=r':\s*>\s*\w',
                risk_level=RiskLevel.MEDIUM,
                description="File content destruction (shell redirect)",
                examples=[": > important.txt", ": > ~/.bashrc"],
                category="Data Destruction"
            ),
            DangerousCommand(
                pattern=r'\bfind\s+.*-delete',
                risk_level=RiskLevel.HIGH,
                description="Mass file deletion with find",
                examples=["find / -name '*.txt' -delete", "find ~ -type f -delete"],
                category="Data Destruction"
            ),
            
            # Fork Bomb and Resource Exhaustion  
            DangerousCommand(
                pattern=r':\(\)\s*\{\s*:\s*\|\s*:\s*&\s*\}\s*;\s*:',
                risk_level=RiskLevel.CRITICAL,
                description="Fork bomb (system crash)",
                examples=[":(){ :|:& };:"],
                category="Resource Exhaustion"
            ),
            DangerousCommand(
                pattern=r'\byes\s+.*\s*>\s*/dev/sd[a-z]',
                risk_level=RiskLevel.CRITICAL,
                description="Disk space exhaustion attack",
                examples=["yes 'data' > /dev/sda1"],
                category="Resource Exhaustion"
            )
        ]
    
    def _initialize_whitelist_patterns(self) -> List[str]:
        """Initialize patterns that should be considered safe despite matching dangerous patterns"""
        return [
            r'\brm\s+-[rfRF]*\s+/tmp/\w+',  # Temporary file deletion
            r'\brm\s+-[rfRF]*\s+\./[^/]',   # Current directory file deletion (non-recursive to parent)
            r'\bmkfs\.\w+\s+/dev/loop\d+',  # Loop device formatting (usually safe)
        ]
    
    def _is_whitelisted(self, command: str) -> bool:
        """Check if command matches whitelist patterns"""
        for pattern in self.whitelist_patterns:
            if re.search(pattern, command, re.IGNORECASE):
                return True
        return False
    
    def analyze_command(self, command: str) -> Tuple[bool, List[DangerousCommand], RiskLevel]:
        """
        Analyze command for dangerous patterns
        
        Returns:
            Tuple of (is_dangerous, matched_patterns, max_risk_level)
        """
        if self._is_whitelisted(command):
            return False, [], RiskLevel.LOW
        
        matched_patterns = []
        max_risk = RiskLevel.LOW
        
        for dangerous_cmd in self.dangerous_patterns:
            if re.search(dangerous_cmd.pattern, command, re.IGNORECASE):
                matched_patterns.append(dangerous_cmd)
                if dangerous_cmd.risk_level.value > max_risk.value:
                    max_risk = dangerous_cmd.risk_level
        
        is_dangerous = len(matched_patterns) > 0
        return is_dangerous, matched_patterns, max_risk
    
    def _get_command_hash(self, command: str) -> str:
        """Generate hash for command confirmation caching"""
        return hashlib.md5(command.encode()).hexdigest()[:16]
    
    def _format_dangerous_command(self, command: str, matches: List[DangerousCommand]) -> str:
        """Format dangerous command with color highlighting"""
        if not COLOR_SUPPORT:
            return f"[DANGEROUS] {command}"
        
        # Highlight the entire command in red background
        formatted = f"{Back.RED}{Fore.WHITE}{Style.BRIGHT} DANGEROUS COMMAND DETECTED {Style.RESET_ALL}\n"
        formatted += f"{Fore.RED}{Style.BRIGHT}Command: {command}{Style.RESET_ALL}\n"
        
        # Show matched patterns
        formatted += f"{Fore.YELLOW}⚠️  Detected Threats:{Style.RESET_ALL}\n"
        for match in matches:
            formatted += f"  • {Fore.RED}{match.category}{Fore.RESET}: {match.description}\n"
            formatted += f"    Risk Level: {self._format_risk_level(match.risk_level)}\n"
        
        return formatted
    
    def _format_risk_level(self, risk_level: RiskLevel) -> str:
        """Format risk level with colors"""
        if not COLOR_SUPPORT:
            return risk_level.name
        
        colors = {
            RiskLevel.LOW: Fore.GREEN,
            RiskLevel.MEDIUM: Fore.YELLOW,
            RiskLevel.HIGH: Fore.RED,
            RiskLevel.CRITICAL: Fore.RED + Style.BRIGHT
        }
        
        return f"{colors[risk_level]}{risk_level.name}{Style.RESET_ALL}"
    
    def _prompt_confirmation(self, command: str, risk_level: RiskLevel) -> bool:
        """
        Prompt user for dangerous command confirmation with appropriate security level
        """
        if risk_level == RiskLevel.CRITICAL:
            return self._prompt_critical_confirmation(command)
        elif risk_level == RiskLevel.HIGH:
            return self._prompt_high_confirmation(command)
        else:
            return self._prompt_standard_confirmation(command)
    
    def _prompt_critical_confirmation(self, command: str) -> bool:
        """Critical level confirmation - requires typing the full command"""
        print(f"{Fore.RED}{Style.BRIGHT}🚨 CRITICAL RISK COMMAND DETECTED! 🚨{Style.RESET_ALL}")
        print(f"{Fore.RED}This command could cause IRREVERSIBLE DATA LOSS or SYSTEM DAMAGE!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}To proceed, you must type the EXACT command:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Expected: {command}{Style.RESET_ALL}")
        
        for attempt in range(3):  # Give 3 attempts
            user_input = input(f"{Fore.RED}Type command exactly (attempt {attempt + 1}/3): {Style.RESET_ALL}").strip()
            
            if user_input == command:
                final_confirm = input(f"{Fore.RED}Are you ABSOLUTELY SURE? Type 'I UNDERSTAND THE RISKS': {Style.RESET_ALL}")
                if final_confirm.strip() == "I UNDERSTAND THE RISKS":
                    print(f"{Fore.GREEN}⚠️  Command confirmed. Proceeding with EXTREME CAUTION...{Style.RESET_ALL}")
                    return True
                else:
                    print(f"{Fore.YELLOW}❌ Final confirmation failed. Command blocked for safety.{Style.RESET_ALL}")
                    return False
            else:
                print(f"{Fore.RED}❌ Command doesn't match. {2-attempt} attempts remaining.{Style.RESET_ALL}")
        
        print(f"{Fore.RED}❌ Max attempts reached. Command blocked for safety.{Style.RESET_ALL}")
        return False
    
    def _prompt_high_confirmation(self, command: str) -> bool:
        """High risk confirmation - requires understanding acknowledgment"""
        print(f"{Fore.RED}{Style.BRIGHT}⚠️  HIGH RISK COMMAND DETECTED!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}This command could cause significant damage or data loss.{Style.RESET_ALL}")
        
        confirm = input(f"{Fore.YELLOW}Do you understand the risks and want to proceed? Type 'YES I UNDERSTAND': {Style.RESET_ALL}")
        
        if confirm.strip() == "YES I UNDERSTAND":
            print(f"{Fore.GREEN}⚠️  Command confirmed. Proceeding with caution...{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.YELLOW}❌ Command blocked for safety.{Style.RESET_ALL}")
            return False
    
    def _prompt_standard_confirmation(self, command: str) -> bool:
        """Standard confirmation for medium risk commands"""
        print(f"{Fore.YELLOW}⚠️  Potentially dangerous command detected.{Style.RESET_ALL}")
        
        confirm = input(f"{Fore.YELLOW}Are you sure you want to execute this command? (y/N): {Style.RESET_ALL}")
        
        if confirm.lower() in ['y', 'yes']:
            print(f"{Fore.GREEN}✅ Command confirmed.{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.YELLOW}❌ Command cancelled for safety.{Style.RESET_ALL}")
            return False
    
    def check_and_confirm_command(self, command: str, force_confirm: bool = False) -> bool:
        """
        Main method to check command safety and get user confirmation if needed
        
        Args:
            command: Command to check
            force_confirm: Force confirmation even for cached commands
            
        Returns:
            True if command is safe to execute, False otherwise
        """
        # Quick safety check for empty commands
        if not command.strip():
            return True
        
        # Check if command is dangerous
        is_dangerous, matches, max_risk = self.analyze_command(command)
        
        if not is_dangerous:
            return True  # Safe command, proceed
        
        # Check confirmation cache (unless forced)
        cmd_hash = self._get_command_hash(command)
        if not force_confirm and cmd_hash in self.confirmation_cache:
            print(f"{Fore.GREEN}✅ Previously confirmed dangerous command. Proceeding...{Style.RESET_ALL}")
            return True
        
        # Display warning and get confirmation
        print(self._format_dangerous_command(command, matches))
        
        confirmed = self._prompt_confirmation(command, max_risk)
        
        if confirmed:
            # Cache the confirmation for this session
            self.confirmation_cache[cmd_hash] = True
            return True
        
        return False
    
    def get_safety_report(self) -> Dict:
        """Generate a safety report with statistics"""
        return {
            "total_patterns": len(self.dangerous_patterns),
            "patterns_by_category": self._group_patterns_by_category(),
            "patterns_by_risk": self._group_patterns_by_risk(),
            "confirmed_commands_count": len(self.confirmation_cache)
        }
    
    def _group_patterns_by_category(self) -> Dict[str, int]:
        """Group dangerous patterns by category"""
        categories = {}
        for pattern in self.dangerous_patterns:
            categories[pattern.category] = categories.get(pattern.category, 0) + 1
        return categories
    
    def _group_patterns_by_risk(self) -> Dict[str, int]:
        """Group dangerous patterns by risk level"""
        risks = {}
        for pattern in self.dangerous_patterns:
            risk_name = pattern.risk_level.name
            risks[risk_name] = risks.get(risk_name, 0) + 1
        return risks


# Global safety checker instance
_safety_checker = None

def get_safety_checker() -> CommandSafetyChecker:
    """Get global safety checker instance (singleton pattern)"""
    global _safety_checker
    if _safety_checker is None:
        _safety_checker = CommandSafetyChecker()
    return _safety_checker


def check_command_safety(command: str, force_confirm: bool = False) -> bool:
    """
    Convenience function to check command safety
    
    Args:
        command: Command to check
        force_confirm: Force confirmation even for cached commands
        
    Returns:
        True if safe to execute, False otherwise
    """
    checker = get_safety_checker()
    return checker.check_and_confirm_command(command, force_confirm)


def analyze_command_risks(command: str) -> Dict:
    """
    Analyze command and return detailed risk information
    
    Returns:
        Dict with analysis results
    """
    checker = get_safety_checker()
    is_dangerous, matches, max_risk = checker.analyze_command(command)
    
    return {
        "is_dangerous": is_dangerous,
        "risk_level": max_risk.name if matches else "LOW",
        "matches": [
            {
                "pattern": match.pattern,
                "category": match.category,
                "description": match.description,
                "risk_level": match.risk_level.name,
                "examples": match.examples
            }
            for match in matches
        ]
    }


if __name__ == "__main__":
    # Test the safety checker
    checker = CommandSafetyChecker()
    
    test_commands = [
        "ls -la",  # Safe
        "rm -rf /",  # Critical
        "rm file.txt",  # Safe
        "mkfs.ext4 /dev/sda1",  # Critical
        "shutdown -h now",  # Medium
        "find /tmp -name '*.log' -delete",  # High
        ": > important.txt"  # Medium
    ]
    
    print("🛡️  IntelliScript Command Safety Checker Test\n")
    
    for cmd in test_commands:
        print(f"Testing: {cmd}")
        is_dangerous, matches, risk = checker.analyze_command(cmd)
        
        if is_dangerous:
            print(f"  ⚠️  DANGEROUS - Risk: {risk.name}")
            for match in matches:
                print(f"     • {match.category}: {match.description}")
        else:
            print(f"  ✅ SAFE")
        print()
