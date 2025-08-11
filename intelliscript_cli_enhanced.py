#!/usr/bin/env python3
"""
Enhanced IntelliScript CLI with multi-model support, advanced license management,
usage statistics, and cloud synchronization.
"""

import os
import sys
import json
import time
import click
from datetime import datetime, timedelta

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.model_handler import ModelHandler
from core.license_manager import LicenseManager
from core.stats_tracker import StatsTracker
from utils.cloud_sync import CloudSync
from security.command_safety import check_command_safety, analyze_command_risks, get_safety_checker

# Configuration paths
CONFIG_PATH = os.path.expanduser('~/.intelliscript/config.json')
USAGE_LOG = os.path.expanduser('~/.intelliscript/usage.log')

def load_config():
    """Load configuration with defaults"""
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    
    # Default configuration
    default_config = {
        'license_key': '',
        'gemini_api_key': '',
        'claude_api_key': '',
        'stats_server': '',
        'license_server': '',
        'cloud_provider': '',
        'email': {
            'enabled': False,
            'smtp_server': '',
            'smtp_port': 587,
            'smtp_user': '',
            'smtp_password': '',
            'from_email': '',
            'admin_email': ''
        },
        'auto_renewal': {
            'enabled': False,
            'default_days': 30
        }
    }
    
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(default_config, f, indent=2)
    
    return default_config

def save_config(cfg):
    """Save configuration to file"""
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(cfg, f, indent=2)

def _contains_shell_commands(text: str) -> bool:
    """Check if text contains shell command patterns"""
    if not text:
        return False
    
    # Common indicators of shell commands
    shell_patterns = [
        r'```(?:bash|sh|shell|zsh|fish)\s*\n([^`]+)```',  # Code blocks
        r'\$\s+([^\n]+)',  # Commands starting with $
        r'#\s+([^\n]+)',   # Commands starting with #
        r'^\s*([a-zA-Z_][\w-]*(?:\s+[^\n]*)?)$',  # Simple command patterns
    ]
    
    for pattern in shell_patterns:
        if re.search(pattern, text, re.MULTILINE):
            return True
    
    return False

def _extract_shell_commands(text: str) -> list:
    """Extract shell commands from text"""
    if not text:
        return []
    
    commands = []
    
    # Extract from code blocks
    code_block_pattern = r'```(?:bash|sh|shell|zsh|fish)\s*\n([^`]+)```'
    code_blocks = re.finditer(code_block_pattern, text, re.MULTILINE | re.DOTALL)
    for block in code_blocks:
        lines = block.group(1).strip().split('\n')
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                commands.append(line)
    
    # Extract commands starting with $ or #
    command_patterns = [
        r'\$\s+([^\n]+)',
        r'#\s+([^\n]+)'
    ]
    
    for pattern in command_patterns:
        matches = re.finditer(pattern, text, re.MULTILINE)
        for match in matches:
            cmd = match.group(1).strip()
            if cmd:
                commands.append(cmd)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_commands = []
    for cmd in commands:
        if cmd not in seen:
            seen.add(cmd)
            unique_commands.append(cmd)
    
    return unique_commands

def check_license_validity(license_manager, license_key, model=None):
    """Check if license is valid and handle auto-renewal"""
    validation = license_manager.validate_license(license_key, model)
    
    if not validation['valid']:
        if validation['reason'] == 'License expired':
            # Attempt auto-renewal
            if license_manager.auto_renew_license(license_key):
                click.echo("License auto-renewed successfully!")
                return True
            else:
                click.echo("❌ License expired. Please renew your license.")
                return False
        else:
            click.echo(f"❌ License validation failed: {validation['reason']}")
            return False
    
    return True

@click.group()
@click.version_option(version='2.0.0', prog_name='IntelliScript')
def cli():
    """IntelliScript Enhanced CLI - Multi-model AI assistant with advanced features"""
    pass

# =============================================================================
# Model Commands
# =============================================================================

@cli.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True))
@click.argument('model', type=click.Choice(['gemini', 'claude']))
@click.option('--max-tokens', default=1024, help='Maximum tokens for Claude responses')
@click.option('--model-version', default='claude-3-sonnet-20240229', help='Claude model version')
@click.pass_context
def ai(ctx, model, max_tokens, model_version):
    """Unified AI command supporting multiple models"""
    start_time = time.time()
    cfg = load_config()
    
    # Initialize components
    license_manager = LicenseManager(CONFIG_PATH)
    stats_tracker = StatsTracker(USAGE_LOG, cfg)
    
    # License validation
    license_key = cfg.get('license_key')
    if not license_key:
        click.echo("❌ No license key found. Use 'intelliscript gen-license' to generate one.")
        return
    
    if not check_license_validity(license_manager, license_key, model):
        return
    
    # Execute model command
    try:
        handler = ModelHandler(cfg)
        
        # Check if model is available
        available_models = handler.get_available_models()
        if model not in available_models:
            missing_key = 'claude_api_key' if model == 'claude' else 'gemini_api_key'
            click.echo(f"❌ {model.capitalize()} not configured. Set {missing_key} first.")
            return
        
        # Prepare args for model
        args = ctx.args
        if model == 'claude' and model_version != 'claude-3-sonnet-20240229':
            # For Claude, we need to pass model version differently
            # This is handled in the model_handler
            pass
        
        # Execute command and get AI response
        result = handler.dispatch(model, args)
        
        # Safety check: if the AI response contains commands, check for dangerous patterns
        ai_response = result.get('response', '')
        if ai_response and _contains_shell_commands(ai_response):
            extracted_commands = _extract_shell_commands(ai_response)
            
            if extracted_commands:
                click.echo(f"\n🛡️  Security Check: Detected shell commands in AI response...")
                
                for cmd in extracted_commands:
                    if not check_command_safety(cmd.strip()):
                        click.echo(f"\n❌ Dangerous command blocked for safety: {cmd}")
                        click.echo(f"🛡️  IntelliScript safety layer prevented potentially harmful execution.")
                        
                        # Log the blocked command
                        stats_tracker.log_usage(
                            command='ai',
                            args=args,
                            model=model,
                            tokens_used=result.get('tokens_used', 0),
                            response_time=int((time.time() - start_time) * 1000),
                            safety_blocked=True,
                            blocked_command=cmd
                        )
                        return
                
                click.echo(f"✅ All commands passed safety checks.")
        
        # Calculate response time
        response_time = int((time.time() - start_time) * 1000)
        
        # Log usage
        stats_tracker.log_usage(
            command='ai',
            args=args,
            model=model,
            tokens_used=result.get('tokens_used', 0),
            response_time=response_time
        )
        
        click.echo(f"\n✅ Command completed in {response_time}ms")
        
    except Exception as e:
        response_time = int((time.time() - start_time) * 1000)
        stats_tracker.log_usage(
            command='ai',
            args=ctx.args,
            model=model,
            error=str(e),
            response_time=response_time
        )
        click.echo(f"❌ Error: {e}")

# =============================================================================
# License Management Commands
# =============================================================================

@cli.command('gen-license')
@click.option('--role', default='user', type=click.Choice(['admin', 'user']), 
              help='License role (admin can generate sub-licenses)')
@click.option('--duration', default=30, help='License duration in days')
@click.option('--models', default='gemini,claude', help='Comma-separated list of bound models')
def generate_license(role, duration, models):
    """Generate a new license with role-based access and model binding"""
    license_manager = LicenseManager(CONFIG_PATH)
    bound_models = [m.strip() for m in models.split(',')]
    
    license_key = license_manager.generate_license(
        role=role,
        duration_days=duration,
        bound_models=bound_models
    )
    
    click.echo(f"🔑 New license generated:")
    click.echo(f"   Key: {license_key}")
    click.echo(f"   Role: {role}")
    click.echo(f"   Duration: {duration} days")
    click.echo(f"   Models: {', '.join(bound_models)}")
    
    # Auto-set as current license if none exists
    cfg = load_config()
    if not cfg.get('license_key'):
        cfg['license_key'] = license_key
        save_config(cfg)
        click.echo(f"✅ License set as current license")

@cli.command('set-license')
@click.argument('license_key')
def set_license(license_key):
    """Set the current license key"""
    license_manager = LicenseManager(CONFIG_PATH)
    
    # Validate license
    validation = license_manager.validate_license(license_key)
    if not validation['valid']:
        click.echo(f"❌ Invalid license: {validation['reason']}")
        return
    
    # Save license
    cfg = load_config()
    cfg['license_key'] = license_key
    save_config(cfg)
    
    click.echo(f"✅ License key set successfully")
    click.echo(f"   Role: {validation['role']}")
    click.echo(f"   Models: {', '.join(validation['bound_models'])}")
    click.echo(f"   Expires: {validation['expires']}")

@cli.command('list-licenses')
@click.option('--include-revoked', is_flag=True, help='Include revoked licenses')
def list_licenses(include_revoked):
    """List all licenses (admin only)"""
    cfg = load_config()
    license_manager = LicenseManager(CONFIG_PATH)
    
    # Check admin privileges
    current_license = cfg.get('license_key')
    if current_license:
        validation = license_manager.validate_license(current_license)
        if not validation['valid'] or validation.get('role') != 'admin':
            click.echo("❌ Admin privileges required")
            return
    
    licenses = license_manager.list_licenses(include_revoked)
    
    if not licenses:
        click.echo("No licenses found")
        return
    
    click.echo(f"📋 Found {len(licenses)} licenses:")
    for i, lic in enumerate(licenses, 1):
        status = "✅ Active" if lic['active'] else "❌ Revoked"
        click.echo(f"\n{i}. {lic['key'][:8]}...")
        click.echo(f"   Status: {status}")
        click.echo(f"   Role: {lic['role']}")
        click.echo(f"   Models: {', '.join(lic['bound_models'])}")
        click.echo(f"   Expires: {lic['expiration']}")

@cli.command('revoke-license')
@click.argument('license_key')
def revoke_license(license_key):
    """Revoke a license (admin only)"""
    cfg = load_config()
    license_manager = LicenseManager(CONFIG_PATH)
    
    # Check admin privileges
    current_license = cfg.get('license_key')
    if current_license:
        validation = license_manager.validate_license(current_license)
        if not validation['valid'] or validation.get('role') != 'admin':
            click.echo("❌ Admin privileges required")
            return
    
    if license_manager.revoke_license(license_key):
        click.echo(f"✅ License {license_key[:8]}... revoked successfully")
    else:
        click.echo(f"❌ License not found: {license_key[:8]}...")

# =============================================================================
# Configuration Commands
# =============================================================================

@cli.command('set-gemini-key')
@click.argument('api_key')
def set_gemini_key(api_key):
    """Set Gemini API key"""
    cfg = load_config()
    cfg['gemini_api_key'] = api_key
    save_config(cfg)
    click.echo("✅ Gemini API key configured")

@cli.command('set-claude-key')
@click.argument('api_key')
def set_claude_key(api_key):
    """Set Claude API key"""
    cfg = load_config()
    cfg['claude_api_key'] = api_key
    save_config(cfg)
    click.echo("✅ Claude API key configured")

@cli.command('set-stats-server')
@click.argument('url')
def set_stats_server(url):
    """Set remote statistics server URL"""
    cfg = load_config()
    cfg['stats_server'] = url
    save_config(cfg)
    click.echo(f"✅ Stats server configured: {url}")

@cli.command('show-config')
def show_config():
    """Show current configuration"""
    cfg = load_config()
    
    click.echo("🔧 Current Configuration:")
    click.echo(f"   License Key: {'✅ Set' if cfg.get('license_key') else '❌ Not set'}")
    click.echo(f"   Gemini API: {'✅ Set' if cfg.get('gemini_api_key') else '❌ Not set'}")
    click.echo(f"   Claude API: {'✅ Set' if cfg.get('claude_api_key') else '❌ Not set'}")
    click.echo(f"   Stats Server: {cfg.get('stats_server', 'Not configured')}")
    click.echo(f"   Cloud Provider: {cfg.get('cloud_provider', 'Not configured')}")

# =============================================================================
# Usage Statistics Commands
# =============================================================================

@cli.command('usage-stats')
@click.option('--model', help='Filter by model (gemini/claude)')
@click.option('--export', type=click.Choice(['json', 'csv', 'prometheus']), 
              default='json', help='Export format')
@click.option('--days', default=30, help='Number of days to analyze')
def usage_stats(model, export, days):
    """Display usage statistics with filtering and export options"""
    cfg = load_config()
    stats_tracker = StatsTracker(USAGE_LOG, cfg)
    
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # Get statistics
    stats = stats_tracker.get_stats(
        format=export,
        start_date=start_date,
        end_date=end_date,
        model_filter=model
    )
    
    if export == 'json':
        click.echo(f"📊 Usage Statistics (Last {days} days)")
        if model:
            click.echo(f"   Filtered by model: {model}")
        click.echo(f"\n📈 Summary:")
        click.echo(f"   Total Calls: {stats.get('total_calls', 0)}")
        click.echo(f"   Success Rate: {stats.get('success_rate', 0):.1f}%")
        
        # Model usage
        by_model = stats.get('by_model', {})
        if by_model:
            click.echo(f"\n🤖 By Model:")
            for model_name, count in by_model.items():
                click.echo(f"   {model_name}: {count} calls")
        
        # Token usage
        tokens = stats.get('tokens', {})
        if tokens.get('total', 0) > 0:
            click.echo(f"\n🔢 Token Usage:")
            click.echo(f"   Total: {tokens['total']:,}")
            click.echo(f"   Average: {tokens['average']:.1f}")
            click.echo(f"   Max: {tokens['max']:,}")
        
        # Performance
        perf = stats.get('performance', {})
        if perf.get('avg_response_time_ms', 0) > 0:
            click.echo(f"\n⚡ Performance:")
            click.echo(f"   Avg Response Time: {perf['avg_response_time_ms']:.0f}ms")
            click.echo(f"   Max Response Time: {perf['max_response_time_ms']:.0f}ms")
        
        # Errors
        errors = stats.get('errors', {})
        if errors.get('total', 0) > 0:
            click.echo(f"\n❌ Errors:")
            click.echo(f"   Total: {errors['total']}")
            error_types = errors.get('types', {})
            for error_type, count in list(error_types.items())[:5]:  # Top 5 errors
                click.echo(f"   {error_type}: {count}")
    
    elif export == 'csv':
        if 'csv_exported' in stats:
            click.echo(f"✅ CSV exported to: {stats['csv_exported']}")
        else:
            click.echo("❌ CSV export failed")
    
    elif export == 'prometheus':
        click.echo("📊 Prometheus Metrics:")
        click.echo(stats)

@cli.command('usage-trends')
@click.option('--days', default=7, help='Number of days for trend analysis')
def usage_trends(days):
    """Show usage trends over time"""
    cfg = load_config()
    stats_tracker = StatsTracker(USAGE_LOG, cfg)
    
    trends = stats_tracker.get_usage_trends(days)
    
    click.echo(f"📈 Usage Trends (Last {days} days):")
    
    for date, data in sorted(trends.items()):
        click.echo(f"\n📅 {date}:")
        click.echo(f"   Calls: {data['calls']}")
        click.echo(f"   Tokens: {data['tokens']:,}")
        click.echo(f"   Models Used: {data['unique_models']}")

# =============================================================================
# Cloud Synchronization Commands
# =============================================================================

@cli.command('sync-cloud')
@click.option('--provider', type=click.Choice(['gcp', 'aws']), 
              help='Cloud provider (gcp/aws)')
@click.option('--direction', type=click.Choice(['pull', 'push']), 
              default='pull', help='Sync direction')
@click.option('--config-only', is_flag=True, help='Sync config only (not licenses)')
def sync_cloud(provider, direction, config_only):
    """Sync configuration and licenses with cloud storage"""
    cfg = load_config()
    
    # Use configured provider if not specified
    if not provider:
        provider = cfg.get('cloud_provider')
        if not provider:
            click.echo("❌ No cloud provider configured. Use --provider option.")
            return
    
    cloud_sync = CloudSync(cfg)
    
    try:
        # Sync configuration
        if cloud_sync.sync_config(CONFIG_PATH, direction):
            click.echo(f"✅ Configuration {direction}ed successfully")
        else:
            click.echo(f"❌ Configuration {direction} failed")
            return
        
        # Sync licenses (if not config-only)
        if not config_only:
            license_manager = LicenseManager(CONFIG_PATH)
            if cloud_sync.sync_licenses(license_manager, direction):
                click.echo(f"✅ Licenses {direction}ed successfully")
            else:
                click.echo(f"❌ License {direction} failed")
    
    except Exception as e:
        click.echo(f"❌ Cloud sync failed: {e}")

@cli.command('setup-cloud')
@click.option('--provider', type=click.Choice(['gcp', 'aws']), 
              prompt='Cloud provider', help='Cloud provider to setup')
def setup_cloud(provider):
    """Setup cloud synchronization"""
    cfg = load_config()
    
    if provider == 'gcp':
        project_id = click.prompt('GCP Project ID')
        bucket_name = click.prompt('GCP Bucket Name')
        credentials_path = click.prompt('GCP Credentials Path (optional)', default='', show_default=False)
        
        credentials = {
            'project_id': project_id,
            'bucket_name': bucket_name,
            'credentials_path': credentials_path if credentials_path else None
        }
    
    elif provider == 'aws':
        region = click.prompt('AWS Region')
        bucket_name = click.prompt('AWS Bucket Name')
        access_key = click.prompt('AWS Access Key')
        secret_key = click.prompt('AWS Secret Key', hide_input=True)
        
        credentials = {
            'region': region,
            'bucket_name': bucket_name,
            'access_key': access_key,
            'secret_key': secret_key
        }
    
    cloud_sync = CloudSync(cfg)
    if cloud_sync.setup_cloud_sync(provider, credentials):
        click.echo(f"✅ {provider.upper()} cloud sync configured successfully")
    else:
        click.echo(f"❌ Failed to configure {provider.upper()} cloud sync")

# =============================================================================
# Maintenance Commands
# =============================================================================

@cli.command('cleanup-logs')
@click.option('--days', default=90, help='Keep logs newer than this many days')
def cleanup_logs(days):
    """Clean up old usage logs"""
    cfg = load_config()
    stats_tracker = StatsTracker(USAGE_LOG, cfg)
    
    result = stats_tracker.cleanup_old_logs(days)
    
    click.echo(f"🧹 Log cleanup completed:")
    click.echo(f"   Kept: {result['kept']} entries")
    click.echo(f"   Removed: {result['removed']} entries")
    click.echo(f"   Cutoff date: {result['cutoff_date']}")

@cli.command('reset-config')
@click.confirmation_option(prompt='This will reset all configuration. Continue?')
def reset_config():
    """Reset configuration to defaults"""
    if os.path.exists(CONFIG_PATH):
        backup_path = f"{CONFIG_PATH}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.rename(CONFIG_PATH, backup_path)
        click.echo(f"📁 Backup created: {backup_path}")
    
    # Create fresh config
    load_config()
    click.echo("✅ Configuration reset to defaults")

# =============================================================================
# Security Management Commands
# =============================================================================

@cli.group()
def security():
    """Security and safety management commands"""
    pass

@security.command('check')
@click.argument('command', required=True)
def security_check(command):
    """Check if a command is considered dangerous"""
    from security.command_safety import analyze_command_risks
    
    analysis = analyze_command_risks(command)
    
    if analysis['is_dangerous']:
        click.echo(f"⚠️  DANGEROUS COMMAND DETECTED")
        click.echo(f"Command: {command}")
        click.echo(f"Risk Level: {analysis['risk_level']}")
        click.echo(f"\nDetected threats:")
        
        for match in analysis['matches']:
            click.echo(f"  • {match['category']}: {match['description']}")
            click.echo(f"    Risk: {match['risk_level']}")
            click.echo(f"    Examples: {', '.join(match['examples'][:2])}")
            click.echo()
    else:
        click.echo(f"✅ SAFE COMMAND")
        click.echo(f"Command: {command}")
        click.echo(f"No dangerous patterns detected.")

@security.command('report')
def security_report():
    """Show security system status and statistics"""
    checker = get_safety_checker()
    report = checker.get_safety_report()
    
    click.echo("🛡️  IntelliScript Security System Report")
    click.echo("=" * 45)
    click.echo(f"Total Dangerous Patterns: {report['total_patterns']}")
    click.echo(f"Confirmed Commands (Session): {report['confirmed_commands_count']}")
    click.echo()
    
    click.echo("📊 Patterns by Category:")
    for category, count in report['patterns_by_category'].items():
        click.echo(f"  • {category}: {count} patterns")
    click.echo()
    
    click.echo("⚠️  Patterns by Risk Level:")
    for risk, count in report['patterns_by_risk'].items():
        click.echo(f"  • {risk}: {count} patterns")
    click.echo()
    
    click.echo("🔒 Security Status: ACTIVE")
    click.echo("All AI-generated commands are automatically scanned for dangerous patterns.")

@security.command('test')
def security_test():
    """Run security system self-test"""
    test_commands = [
        ("ls -la", False),
        ("rm -rf /", True),
        ("mkfs.ext4 /dev/sda1", True),
        ("shutdown -h now", True),
        ("find /tmp -name '*.log' -delete", True),
        ("cat file.txt", False)
    ]
    
    click.echo("🧪 Running IntelliScript Security System Self-Test...")
    click.echo("=" * 50)
    
    passed = 0
    total = len(test_commands)
    
    for command, should_be_dangerous in test_commands:
        analysis = analyze_command_risks(command)
        is_dangerous = analysis['is_dangerous']
        
        if is_dangerous == should_be_dangerous:
            status = "✅ PASS"
            passed += 1
        else:
            status = "❌ FAIL"
        
        risk_info = f"({analysis['risk_level']})" if is_dangerous else "(SAFE)"
        click.echo(f"{status} {command} {risk_info}")
    
    click.echo("=" * 50)
    click.echo(f"Test Results: {passed}/{total} passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        click.echo("🎉 All tests passed! Security system is functioning correctly.")
    else:
        click.echo("⚠️  Some tests failed. Security system may need attention.")

@security.command('enable')
def security_enable():
    """Enable dangerous command detection (default: enabled)"""
    # Note: In this implementation, security is always enabled
    # This command is here for future extensibility
    click.echo("✅ Dangerous command detection is ENABLED.")
    click.echo("All AI-generated commands will be scanned for safety.")

@security.command('disable')
def security_disable():
    """Disable dangerous command detection (NOT RECOMMENDED)"""
    click.echo("⚠️  WARNING: Disabling security features is NOT RECOMMENDED!")
    click.echo("This could expose your system to dangerous AI-generated commands.")
    
    confirm = input("Are you absolutely sure? Type 'DISABLE SECURITY' to confirm: ")
    if confirm == "DISABLE SECURITY":
        click.echo("❌ Security cannot be disabled in this version for safety reasons.")
        click.echo("To bypass security, run commands manually after review.")
    else:
        click.echo("✅ Security remains ENABLED (smart choice!).")

# =============================================================================
# Legacy Compatibility (Deprecated)
# =============================================================================

@cli.command(hidden=True)
@click.pass_context
def gemini(ctx):
    """Legacy Gemini command (deprecated - use 'ai gemini' instead)"""
    click.echo("⚠️  This command is deprecated. Use 'intelliscript ai gemini' instead.")
    click.echo("For help: intelliscript ai gemini --help")
    ctx.invoke(ai, model='gemini')

if __name__ == '__main__':
    cli()
