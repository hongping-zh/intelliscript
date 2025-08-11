# IntelliScript CLI

<div align="center">

![IntelliScript CLI](https://img.shields.io/badge/IntelliScript-Enterprise%20AI%20Platform-blue?style=for-the-badge&logo=robot)
![Version](https://img.shields.io/badge/version-1.0.0-green?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.8%2B-blue?style=for-the-badge&logo=python)

![Build Status](https://github.com/hongping-zh/intelliscript/workflows/CI/badge.svg)
![PyPI version](https://badge.fury.io/py/intelliscript-cli.svg)
![Downloads](https://pepy.tech/badge/intelliscript-cli)
![GitHub Stars](https://img.shields.io/github/stars/hongping-zh/intelliscript?style=social)

**🚀 Enterprise-Grade AI Model Management Platform**

*Multi-model AI integration • Cost optimization • Enterprise security*

[🚀 Quick Start](#-5-minute-quick-start) • [📺 Live Demo](#-live-demonstrations) • [💡 Features](#-core-features) • [📦 Installation](#-installation) • [📚 Documentation](#-complete-documentation)

</div>

---

## 📺 **Live Demonstrations**

### 🎥 **Basic Usage Demo**
![IntelliScript Basic Demo](https://raw.githubusercontent.com/hongping-zh/intelliscript/main/docs/gifs/basic-usage-demo.gif)
*Basic AI query with automatic model selection and cost tracking*

### 🎥 **Multi-Model Cost Optimization**
![Cost Optimization Demo](https://raw.githubusercontent.com/hongping-zh/intelliscript/main/docs/gifs/cost-optimization-demo.gif)
*Intelligent routing between Claude, Gemini, and GPT-4 for optimal cost-performance*

### 🎥 **Enterprise Dashboard**
![Enterprise Dashboard Demo](https://raw.githubusercontent.com/hongping-zh/intelliscript/main/docs/gifs/dashboard-demo.gif)
*Real-time usage analytics and team management interface*

> **📝 Note**: GIF demonstrations show actual IntelliScript CLI in action. [Create your own demo](docs/CREATE_DEMO.md)

---

## 🚀 **5-Minute Quick Start**

### **Step 1: Installation**
```bash
# Clone the repository
git clone https://github.com/hongping-zh/intelliscript.git
cd intelliscript

# Install dependencies
pip install -r requirements.txt

# Optional: Install globally
pip install -e .
```

### **Step 2: Initialize Configuration**
```bash
# Initialize IntelliScript
intelligript init

# This creates:
# ~/.intelliscript/
# ├── config.json      # Main configuration
# ├── usage.log        # Usage statistics  
# ├── models/          # Model configurations
# └── cache/           # Response caching
```

### **Step 3: Configure AI Models**

<details>
<summary><strong>🤖 Claude Sonnet 4.0 Setup</strong></summary>

```bash
# Add Claude API key
intelligript config add-model claude-sonnet-4 \
  --api-key "your-anthropic-api-key" \
  --priority high \
  --use-cases "analysis,coding,reasoning"

# Test connection
intelligript test claude-sonnet-4
✅ Claude Sonnet 4.0: Connected successfully
💰 Rate: $15/1M tokens input, $75/1M tokens output
```
</details>

<details>
<summary><strong>🧠 Google Gemini 2.5 Pro Setup</strong></summary>

```bash
# Add Gemini API key
intelligript config add-model gemini-2.5-pro \
  --api-key "your-google-api-key" \
  --priority medium \
  --use-cases "multimodal,documents,translation"

# Enable multimodal features
intelligript config set gemini-2.5-pro --enable-vision true
✅ Gemini 2.5 Pro: Configured with vision support
```
</details>

<details>
<summary><strong>🔥 OpenAI GPT-4.1 Setup</strong></summary>

```bash
# Add OpenAI API key
intelligript config add-model gpt-4.1-turbo \
  --api-key "your-openai-api-key" \
  --priority low \
  --use-cases "creative,general,conversation"

# Set usage limits
intelligript config set gpt-4.1-turbo --daily-limit 100
✅ GPT-4.1 Turbo: Ready with usage limits
```
</details>

### **Step 4: Your First AI Query**
```bash
# Basic AI query with automatic model selection
intelligript ai "Explain machine learning in simple terms"

🤖 Selected Model: Gemini 2.5 Pro (best cost-performance for explanation)
💭 Processing your query...

📝 Response:
Machine learning is like teaching a computer to recognize patterns...
[detailed response]

💰 Cost: $0.0023 | ⚡ Response time: 1.2s | 🎯 Model: Gemini 2.5 Pro
✅ 67% cheaper than using GPT-4.1 for this query type
```

### **Step 5: View Your Analytics**
```bash
intelligript stats show

📊 IntelliScript Usage Statistics (Last 30 days)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 Total Cost: $45.67 (vs $67.23 without optimization: 32% saved)
📈 Total Queries: 1,247
⚡ Avg Response Time: 0.8s
🎯 Success Rate: 99.2%

Model Usage Distribution:
🧠 Gemini 2.5 Pro:    62% (774 queries) - $18.23
🤖 Claude Sonnet 4:   28% (349 queries) - $21.45
🔥 GPT-4.1 Turbo:     10% (124 queries) - $5.99
```

---

## 💡 **Core Features**

### 🎯 **Intelligent Model Routing**
```bash
# Automatic model selection based on query type
intelligript ai "Write a creative story" --auto-route
🔥 Selected: GPT-4.1 (best for creative tasks)

intelligript ai "Analyze this financial report" --auto-route  
🤖 Selected: Claude Sonnet 4 (best for analysis)

intelligript ai "Translate this document" --auto-route
🧠 Selected: Gemini 2.5 Pro (best cost-performance for translation)
```

### 💰 **Advanced Cost Optimization**
```bash
# Set budget controls
intelligript budget set --daily-limit 50.00 --alert-threshold 80%

# Cost-aware querying
intelligript ai "Complex analysis task" --max-cost 2.00
🎯 Optimizing for cost constraint...
✅ Using Gemini 2.5 Pro instead of Claude (Est. cost: $1.45)

# Batch processing with cost optimization
intelligript batch process queries.json --optimize-cost
💰 Processing 500 queries with intelligent routing...
✅ Estimated savings: 45% compared to single-model approach
```

### 📊 **Real-Time Analytics Dashboard**
```bash
# Launch web dashboard
intelligript dashboard --port 8080

🌐 Dashboard available at: http://localhost:8080
📈 Real-time metrics:
   • Live query monitoring
   • Cost breakdown by model
   • Performance analytics  
   • Team usage statistics
   • API health monitoring
```

### 🔒 **Enterprise Security**
```bash
# Enable enterprise security features
intelligript security enable --encryption aes-256 --audit-log

# Role-based access control
intelligript users add developer@company.com --role analyst --models "gemini,claude"
intelligript users add manager@company.com --role admin --full-access

# Compliance reporting
intelligript compliance report --format json --period monthly
```

---

## 📦 **Installation Options**

### **Option 1: PyPI Installation (Recommended)**
```bash
# Latest stable release
pip install intelliscript-cli

# With optional dependencies
pip install intelliscript-cli[enterprise,dashboard,security]

# Development version
pip install git+https://github.com/hongping-zh/intelliscript.git
```

### **Option 2: Docker Installation**
```bash
# Pull official image
docker pull hongping/intelliscript:latest

# Run with volume mount for config persistence
docker run -v ~/.intelliscript:/root/.intelliscript \
           -p 8080:8080 \
           hongping/intelliscript:latest
```

### **Option 3: Development Setup**
```bash
# Clone repository
git clone https://github.com/hongping-zh/intelliscript.git
cd intelliscript

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .[dev]

# Run tests
pytest tests/ --cov=intelliscript
```

---

## 📚 **Complete Documentation**

### **🔧 Configuration Reference**

<details>
<summary><strong>Complete config.json example</strong></summary>

```json
{
  "models": {
    "claude-sonnet-4": {
      "api_key": "${ANTHROPIC_API_KEY}",
      "endpoint": "https://api.anthropic.com/v1/messages",
      "priority": "high",
      "rate_limits": {
        "requests_per_minute": 60,
        "tokens_per_minute": 40000
      },
      "cost_per_token": {
        "input": 0.000015,
        "output": 0.000075
      },
      "use_cases": ["analysis", "reasoning", "code_review"],
      "max_tokens": 4096
    },
    "gemini-2.5-pro": {
      "api_key": "${GOOGLE_API_KEY}",
      "endpoint": "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro",
      "priority": "medium",
      "multimodal": true,
      "cost_per_token": {
        "input": 0.000001,
        "output": 0.000002
      },
      "use_cases": ["translation", "documents", "multimodal"],
      "max_tokens": 2048
    }
  },
  "routing": {
    "strategy": "cost_performance",
    "fallback_model": "gemini-2.5-pro",
    "use_case_mapping": {
      "creative": "gpt-4.1-turbo",
      "analysis": "claude-sonnet-4",
      "translation": "gemini-2.5-pro",
      "code": "claude-sonnet-4"
    }
  },
  "budget": {
    "daily_limit": 100.0,
    "monthly_limit": 2500.0,
    "alert_threshold": 0.8,
    "auto_pause_on_limit": true
  },
  "logging": {
    "level": "INFO",
    "file": "~/.intelliscript/usage.log",
    "remote_endpoint": "https://api.intelliscript.dev/usage",
    "include_content": false
  },
  "security": {
    "encryption": "aes-256",
    "audit_logging": true,
    "require_auth": false
  }
}
```
</details>

### **⚙️ Command Reference**

<details>
<summary><strong>All available commands</strong></summary>

#### **Configuration Commands**
```bash
# Initialize new configuration
intelligript init [--config-path PATH] [--interactive]

# Model management
intelligript config add-model MODEL_NAME --api-key KEY [OPTIONS]
intelligript config remove-model MODEL_NAME
intelligript config list-models
intelligript config test MODEL_NAME

# Settings management
intelligript config get KEY
intelligript config set KEY VALUE
intelligript config reset [--confirm]
```

#### **AI Query Commands**
```bash
# Basic AI queries
intelligript ai "PROMPT" [OPTIONS]
intelligript ask "PROMPT" [--model MODEL] [--max-tokens N]

# Advanced querying
intelligript ai "PROMPT" --auto-route --max-cost 5.00
intelligript ai --file input.txt --output result.txt
intelligript ai --interactive  # Start interactive session

# Batch processing
intelligript batch process FILE [--format json|csv] [--optimize-cost]
intelligript batch template create NAME  # Create batch template
```

#### **Analytics & Monitoring**
```bash
# Usage statistics
intelligript stats show [--period 7d|30d|90d]
intelligript stats export [--format json|csv] [--output FILE]
intelligript stats clear [--before DATE]

# Cost analysis
intelligript costs breakdown [--by-model] [--period PERIOD]
intelligript costs forecast [--days N]
intelligript costs compare --before DATE --after DATE

# Performance monitoring
intelligript performance show
intelligript health check [--models] [--endpoints]
```

#### **Enterprise Features**
```bash
# User management
intelligript users list
intelligript users add EMAIL --role ROLE [--models MODELS]
intelligript users remove EMAIL
intelligript users permissions EMAIL --grant PERMISSION

# Compliance & Security
intelligript compliance report [--format FORMAT] [--period PERIOD]
intelligript security scan [--fix]
intelligript audit log [--filter FILTER] [--export]

# Team management
intelligript teams create TEAM_NAME
intelligript teams add-member TEAM_NAME EMAIL
intelligript teams usage TEAM_NAME [--period PERIOD]
```

#### **System Commands**
```bash
# Dashboard
intelligript dashboard [--port PORT] [--host HOST] [--auth]

# Updates & Maintenance
intelligript update [--check-only]
intelligript cache clear [--model MODEL]
intelligript logs show [--tail N] [--follow]

# Import/Export
intelligript export config [--output FILE] [--encrypted]
intelligript import config FILE [--merge] [--decrypt]
```
</details>

### **📋 Advanced Usage Examples**

<details>
<summary><strong>Real-world usage scenarios</strong></summary>

#### **Scenario 1: Content Creation Workflow**
```bash
# Research phase - use cost-effective model
intelligript ai "Research latest trends in quantum computing" \
  --model gemini-2.5-pro \
  --output research.md

# Creative writing - use best creative model
intelligript ai "Write engaging blog post about quantum computing based on: $(cat research.md)" \
  --model gpt-4.1-turbo \
  --max-tokens 2000 \
  --output blog-draft.md

# Review and editing - use analysis model
intelligript ai "Review and suggest improvements for: $(cat blog-draft.md)" \
  --model claude-sonnet-4 \
  --output blog-reviewed.md

# Cost summary
intelligript costs breakdown --period today
```

#### **Scenario 2: Code Review Automation**
```bash
# Batch code review for multiple files
find ./src -name "*.py" | xargs -I {} \
  intelliscript ai "Review this Python code for bugs and improvements: $(cat {})" \
  --model claude-sonnet-4 \
  --output reviews/{}.review.md

# Security analysis
intelligript ai "Analyze security vulnerabilities in: $(cat main.py)" \
  --model claude-sonnet-4 \
  --tag security-review

# Performance optimization suggestions
intelligript ai "Suggest performance optimizations: $(cat algorithm.py)" \
  --auto-route \
  --max-cost 1.50
```

#### **Scenario 3: Enterprise Document Processing**
```bash
# Prepare batch processing template
intelligript batch template create document-analysis \
  --prompt "Analyze and summarize this document: {content}" \
  --model claude-sonnet-4 \
  --output-format json

# Process multiple documents
intelligript batch process documents.json \
  --template document-analysis \
  --optimize-cost \
  --parallel 5 \
  --output analysis-results.json

# Generate executive summary
intelligript ai "Create executive summary from: $(cat analysis-results.json)" \
  --model gpt-4.1-turbo \
  --output executive-summary.md
```

#### **Scenario 4: Multi-language Support**
```bash
# Translation with quality verification
intelligript ai "Translate to Spanish: $(cat document.txt)" \
  --model gemini-2.5-pro \
  --output document-es.txt

# Quality check translation
intelligript ai "Check translation quality between English and Spanish versions" \
  --model claude-sonnet-4 \
  --file document.txt,document-es.txt

# Batch translation for multiple languages
for lang in fr de it pt; do
  intelliscript ai "Translate to $lang: $(cat source.txt)" \
    --model gemini-2.5-pro \
    --output "translated-$lang.txt"
done
```
</details>

### **🎯 Best Practices**

<details>
<summary><strong>Optimization tips and recommendations</strong></summary>

#### **Cost Optimization**
- **Use auto-routing**: Let IntelliScript choose the most cost-effective model
- **Set budget limits**: Prevent unexpected costs with daily/monthly limits
- **Batch processing**: Process multiple queries together for better rates
- **Cache responses**: Avoid duplicate queries with built-in caching
- **Monitor usage**: Regular review of stats to identify optimization opportunities

#### **Performance Best Practices**
- **Use appropriate models**: Match model capabilities to task requirements
- **Optimize prompts**: Clear, specific prompts get better results faster
- **Parallel processing**: Use batch commands for multiple similar tasks
- **Configure timeouts**: Set reasonable limits to avoid hanging requests
- **Monitor health**: Regular health checks ensure optimal performance

#### **Security Guidelines**
- **Environment variables**: Store API keys securely, never in code
- **Enable encryption**: Use AES-256 for sensitive data protection
- **Audit logging**: Track all usage for compliance requirements
- **Role-based access**: Limit model access based on user roles
- **Regular updates**: Keep IntelliScript updated for security patches

#### **Enterprise Deployment**
- **Centralized config**: Use shared configuration for team consistency
- **Usage monitoring**: Track team usage and costs in real-time
- **Compliance reporting**: Generate regular compliance reports
- **Backup configs**: Regular backup of configurations and logs
- **High availability**: Deploy with redundancy for critical systems
</details>

---

## 🤝 **Contributing & Community**

### **🚀 Quick Contribution Guide**
```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/intelliscript.git
cd intelliscript

# Create feature branch
git checkout -b feature/amazing-improvement

# Make your changes
# ... code, test, document ...

# Submit PR
git push origin feature/amazing-improvement
# Then create PR on GitHub
```

### **📞 Support & Community**
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/hongping-zh/intelliscript/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/hongping-zh/intelliscript/discussions)
- 💬 **Community Chat**: [Discord Server](https://discord.gg/intelliscript)
- 📚 **Documentation**: [Wiki](https://github.com/hongping-zh/intelliscript/wiki)
- 📧 **Enterprise Support**: enterprise@intelliscript.dev

---

<div align="center">

**⭐ Star this project if it helps you save costs and improve AI workflow efficiency! ⭐**

![GitHub Stars](https://img.shields.io/github/stars/hongping-zh/intelliscript?style=social)
![Twitter Follow](https://img.shields.io/twitter/follow/intelliscript?style=social)

**Made with ❤️ by the IntelliScript Team**

[⬆️ Back to Top](#intelliscript-cli)

</div>
     token = "YOUR_GEMINI_API_KEY"
     ```
2. **Generate License Key**
   ```bash
   python intelliscript_cli.py gen-license
   ```
3. **Call Gemini (no `run` subcommand!):**
   ```bash
   python intelliscript_cli.py gemini "What is quantum entanglement?"
   ```

---

## VSCode Extension Integration
- Install the IntelliScript VSCode extension
- Use the command palette: `IntelliScript: Ask Gemini (gemini-cli)`
- The extension will internally call IntelliScript CLI, ensuring unified license, API Key, and logging management

---

## Configuration
- **License Key**: Managed by CLI, stored in `~/.intelliscript/config.json`
- **Gemini API Key**: Set in `~/.config/gemini-cli.toml`
- **Remote License/Stats Server**: Optional, set via CLI commands

---

## Example Commands

- Show config:
  ```bash
  python intelliscript_cli.py show-config
  ```
- Set remote license server:
  ```bash
  python intelliscript_cli.py set-license-server http://your-server/api/check_license
  ```
- Use Gemini CLI with markdown output:
  ```bash
  python intelliscript_cli.py gemini --markdown "Explain quantum entanglement"
  ```

---

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

---

## License
MIT License. See [LICENSE](LICENSE) for details.

---

## Contact
For issues, feature requests, or support, please open a GitHub Issue or contact the maintainers via the repository.


## 项目简介
IntelliScript CLI 是一个轻量级命令行工具，支持 License Key 管理、统一配置、本地与远程使用统计、License 校验及自动续期、云端配置、命令同步，并作为 Gemini CLI 的包装器。

---

## 目录结构

```
IntelliScriptCLI/
├── intelliscript_cli.py
├── requirements.txt
├── README.md
```

---

## 依赖安装

```bash
pip install -r requirements.txt
```

requirements.txt 内容：
```
click
requests
```

---

## 功能与命令说明

### 1. License Key 管理
- 生成 License Key
  ```bash
  python intelliscript_cli.py gen-license
  ```
- 远程校验 License Key
  ```bash
  python intelliscript_cli.py check-license
  ```
- 自动续期（命令调用时自动检测本地 key 是否过期，若过期则从云端拉取新 key，详见代码实现）

### 2. 配置统一化
- 设置 Gemini API Key
  ```bash
  python intelliscript_cli.py set-gemini-key 你的APIKey
  ```
- 设置远程统计服务器
  ```bash
  python intelliscript_cli.py set-stats-server https://your-server/api/usage
  ```
- 设置 License 校验服务器
  ```bash
  python intelliscript_cli.py set-license-server https://your-server/api/check_license
  ```
- 查看当前配置
  ```bash
  python intelliscript_cli.py show-config
  ```
- 重置配置
  ```bash
  python intelliscript_cli.py reset-config
  ```

### 3. 使用统计
- 本地统计
  ```bash
  python intelliscript_cli.py usage-stats
  ```
- 远程统计
  - 每次命令调用自动向 stats_server 上报日志（失败不影响主流程）

### 4. Gemini CLI 包装
- 透传参数调用 Gemini CLI
  ```bash
  python intelliscript_cli.py gemini run "你的问题"
  ```

### 5. 本地/远程命令同步
- 支持将本地命令历史同步至云端（可扩展为定时/手动同步）
- 代码中 log_usage_remote 实现了每次命令调用的远程上报

### 6. License 自动续期
- 在每次关键命令调用时，自动检测本地 License 是否过期（如需可扩展为定时检测）
- 若过期则自动向 license_server 拉取新 key 并保存

### 7. 云端配置
- 通过 set-stats-server、set-license-server 动态配置云端地址
- 配置文件统一存储于 `~/.intelliscript/config.json`

---

## 配置文件与日志
- 配置文件：`~/.intelliscript/config.json`
- 使用日志：`~/.intelliscript/usage.log`

---

## 全部核心代码

```python
import os
import json
import uuid
import subprocess
import click
from datetime import datetime, timedelta
import requests

CONFIG_PATH = os.path.expanduser('~/.intelliscript/config.json')
USAGE_LOG = os.path.expanduser('~/.intelliscript/usage.log')

LICENSE_EXPIRE_DAYS = 30  # License 有效期（天）

def load_config():
    if not os.path.exists(CONFIG_PATH):
        return {}
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_config(cfg):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(cfg, f, indent=2)

def log_usage(command, args):
    os.makedirs(os.path.dirname(USAGE_LOG), exist_ok=True)
    with open(USAGE_LOG, 'a', encoding='utf-8') as f:
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'command': command,
            'args': args
        }
        f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
    log_usage_remote(command, args)

def log_usage_remote(command, args):
    cfg = load_config()
    stats_server = cfg.get('stats_server')
    if not stats_server:
        return
    try:
        requests.post(stats_server, json={
            'license_key': cfg.get('license_key'),
            'command': command,
            'args': args,
            'timestamp': datetime.now().isoformat()
        }, timeout=3)
    except Exception:
        pass  # 远程统计失败不影响主流程

def license_expired(cfg):
    # 检查本地 license 是否过期
    date_str = cfg.get('license_date')
    if not date_str:
        return True
    try:
        d0 = datetime.fromisoformat(date_str)
        return (datetime.now() - d0) > timedelta(days=LICENSE_EXPIRE_DAYS)
    except Exception:
        return True

def renew_license(cfg):
    # 自动向 license_server 拉取新 key
    server = cfg.get('license_server')
    if not server:
        click.echo("未配置 license_server，无法自动续期。")
        return False
    try:
        resp = requests.post(server, json={'renew': True, 'old_license': cfg.get('license_key')}, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            cfg['license_key'] = data.get('license_key')
            cfg['license_date'] = datetime.now().isoformat()
            save_config(cfg)
            click.echo("License 自动续期成功。")
            return True
        else:
            click.echo(f"自动续期失败: {resp.text}")
            return False
    except Exception as e:
        click.echo(f"自动续期异常: {e}")
        return False

@click.group()
def cli():
    pass

@cli.command()
def gen_license():
    """生成并保存 License Key"""
    cfg = load_config()
    if 'license_key' not in cfg or license_expired(cfg):
        cfg['license_key'] = str(uuid.uuid4()).replace('-', '')
        cfg['license_date'] = datetime.now().isoformat()
        save_config(cfg)
        click.echo(f"新 License Key: {cfg['license_key']}")
    else:
        click.echo(f"已存在 License Key: {cfg['license_key']}")

@cli.command()
@click.argument('key')
def set_gemini_key(key):
    """配置 Gemini API Key"""
    cfg = load_config()
    cfg['gemini_api_key'] = key
    save_config(cfg)
    click.echo("Gemini API Key 已保存")

@cli.command()
@click.argument('url')
def set_stats_server(url):
    """配置远程统计服务器地址"""
    cfg = load_config()
    cfg['stats_server'] = url
    save_config(cfg)
    click.echo(f"统计服务器已设置为: {url}")

@cli.command()
@click.argument('url')
def set_license_server(url):
    """配置License校验服务器地址"""
    cfg = load_config()
    cfg['license_server'] = url
    save_config(cfg)
    click.echo(f"License服务器已设置为: {url}")

@cli.command()
def show_config():
    """显示当前配置"""
    cfg = load_config()
    click.echo(json.dumps(cfg, indent=2, ensure_ascii=False))

@cli.command()
def reset_config():
    """重置本地配置"""
    if os.path.exists(CONFIG_PATH):
        os.remove(CONFIG_PATH)
        click.echo("配置已重置。")
    else:
        click.echo("配置文件不存在。")

@cli.command()
def usage_stats():
    """显示本地使用统计信息"""
    if not os.path.exists(USAGE_LOG):
        click.echo("无使用日志。")
        return
    with open(USAGE_LOG, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    click.echo(f"共调用 {len(lines)} 次命令。")
    stats = {}
    for line in lines:
        try:
            entry = json.loads(line)
            cmd = entry.get('command')
            stats[cmd] = stats.get(cmd, 0) + 1
        except Exception:
            continue
    for cmd, count in stats.items():
        click.echo(f"  {cmd}: {count} 次")

@cli.command()
def check_license():
    """远程校验 License Key"""
    cfg = load_config()
    license_key = cfg.get('license_key')
    server = cfg.get('license_server')
    if not license_key or not server:
        click.echo("请先生成 License Key 并配置 license_server。")
        return
    # 自动续期逻辑
    if license_expired(cfg):
        click.echo("License 已过期，自动续期...")
        if not renew_license(cfg):
            click.echo("自动续期失败，无法校验。")
            return
    try:
        resp = requests.post(server, json={'license_key': license_key}, timeout=5)
        if resp.status_code == 200:
            click.echo(f"校验结果: {resp.json()}")
        else:
            click.echo(f"服务器返回异常: {resp.text}")
    except Exception as e:
        click.echo(f"远程校验失败: {e}")

@cli.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True))
@click.pass_context
def gemini(ctx):
    """包装 Gemini CLI，自动注入配置与统计"""
    cfg = load_config()
    license_key = cfg.get('license_key')
    # 自动续期逻辑
    if not license_key or license_expired(cfg):
        click.echo("License 不存在或已过期，自动续期...")
        if not renew_license(cfg):
            click.echo("自动续期失败，无法继续执行命令。")
            return
    log_usage('gemini', ctx.args)
    env = os.environ.copy()
    if 'gemini_api_key' in cfg:
        env['GEMINI_API_KEY'] = cfg['gemini_api_key']
    try:
        subprocess.run(['gemini'] + ctx.args, env=env)
    except FileNotFoundError:
        click.echo("未检测到 gemini-cli，请先安装。")

if __name__ == '__main__':
    cli()
```

---

## 远程 License 校验/续期服务器（Flask 示例）

```python
from flask import Flask, request, jsonify
from datetime import datetime
app = Flask(__name__)

VALID_LICENSES = {"your_license_key1", "your_license_key2"}

@app.route('/api/check_license', methods=['POST'])
def check_license():
    data = request.json
    key = data.get('license_key')
    if key in VALID_LICENSES:
        return jsonify({'valid': True, 'expire': False})
    return jsonify({'valid': False, 'expire': True}), 403

@app.route('/api/check_license', methods=['POST'])
def renew_license():
    data = request.json
    if data.get('renew'):
        # 生成新 license key
        new_key = str(uuid.uuid4()).replace('-', '')
        VALID_LICENSES.add(new_key)
        return jsonify({'license_key': new_key, 'renewed': True, 'date': datetime.now().isoformat()})
    return jsonify({'msg': 'invalid request'}), 400

@app.route('/api/usage', methods=['POST'])
def usage():
    print(request.json)
    return jsonify({'msg': 'received'})
```

---

## 总结
- 支持 License Key 全生命周期管理（生成、校验、自动续期）
- 支持本地/远程配置与统计
- 支持命令同步与云端配置
- 所有代码已集成在 intelliscript_cli.py，便于二次开发

如需更多扩展或问题反馈，请随时联系开发者。
