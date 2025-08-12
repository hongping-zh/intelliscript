# IntelliScript 2.0 - Local AI Models & Privacy-First Commands

<div align="center">

![IntelliScript CLI](https://img.shields.io/badge/IntelliScript-AI%20CLI%20Assistant-blue?style=for-the-badge&logo=robot)
![Version](https://img.shields.io/badge/version-2.0.0-green?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.8%2B-blue?style=for-the-badge&logo=python)

**🚀 Multi-Provider AI Command Assistant**

*Cloud AI • Local Models • Privacy-First • Cost-Effective*

[🚀 Quick Start](#-quick-start) • [🏠 Local Models](#-local-models-with-ollama) • [☁️ Cloud AI](#-cloud-ai-providers) • [⚙️ Configuration](#-configuration)

</div>

---

## 🎯 **What is IntelliScript 2.0?**

IntelliScript is an intelligent command-line assistant that translates natural language into executable shell commands using AI. **Version 2.0** introduces **local model support** for privacy-conscious users and **multi-provider architecture** for optimal cost and performance.

### ✨ **Key Features**

- 🏠 **Local AI Models** - Run completely offline with Ollama (llama3, codellama, mistral, etc.)
- ☁️ **Multi-Cloud Support** - OpenAI GPT-4, Anthropic Claude, Google Gemini
- 🔐 **Privacy-First** - Your commands never leave your machine with local models
- 💰 **Cost-Effective** - Use free local models or optimize cloud costs
- 🧠 **Context Memory** - Multi-turn conversations with command history
- 🛡️ **Safety Checks** - Built-in dangerous command detection
- ⚙️ **Flexible Config** - TOML configuration with environment overrides

---

## 🚀 **Quick Start**

### **Method 1: Use Local Models (Recommended for Privacy)**

```bash
# 1. Install Ollama (https://ollama.ai)
curl -fsSL https://ollama.ai/install.sh | sh

# 2. Download a model (choose one)
ollama pull llama3        # General purpose (4.7GB)
ollama pull codellama     # Code-focused (3.8GB)  
ollama pull mistral       # Lightweight (4.1GB)

# 3. Clone IntelliScript
git clone https://github.com/hongping-zh/intelliscript.git
cd intelliscript

# 4. Install dependencies
pip install -r requirements.txt

# 5. Start using immediately!
python intelliscript_cli_refactored.py "show me all python files"
python intelliscript_cli_refactored.py "compress this directory" --provider ollama
```

### **Method 2: Use Cloud AI Providers**

```bash
# 1. Set up API keys (choose one or more)
export OPENAI_API_KEY="sk-your-openai-key"
export ANTHROPIC_API_KEY="sk-ant-your-claude-key" 
export GOOGLE_API_KEY="your-google-key"

# 2. Use cloud providers
python intelliscript_cli_refactored.py "find large files" --provider openai
python intelliscript_cli_refactored.py "backup database" --provider anthropic
```

---

## 🏠 **Local Models with Ollama**

### **Why Local Models?**

- ✅ **Complete Privacy** - Commands never leave your machine
- ✅ **No API Costs** - Use powerful models for free
- ✅ **Offline Operation** - Works without internet connection
- ✅ **No Rate Limits** - Generate unlimited commands
- ✅ **Enterprise Security** - Perfect for sensitive environments

### **Supported Models**

| Model | Size | Best For | Download Command |
|-------|------|----------|------------------|
| **llama3** | 4.7GB | General commands, daily tasks | `ollama pull llama3` |
| **codellama** | 3.8GB | Programming, git, development | `ollama pull codellama` |
| **codellama:13b** | 7.3GB | Complex coding tasks | `ollama pull codellama:13b` |
| **mistral** | 4.1GB | Lightweight, fast responses | `ollama pull mistral` |
| **qwen** | 4.5GB | Multi-language support | `ollama pull qwen` |

### **Local Model Setup**

#### **Step 1: Install Ollama**

**macOS/Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows:**
Download from [ollama.ai](https://ollama.ai/download) and run installer.

#### **Step 2: Download Models**

```bash
# Recommended for most users
ollama pull llama3

# For coding tasks
ollama pull codellama

# For lightweight/fast responses  
ollama pull mistral
```

#### **Step 3: Configure IntelliScript**

```bash
# Interactive configuration
python intelliscript_cli_refactored.py config

# Or manually edit ~/.config/intelliscript/config.toml
```

**Configuration Example:**
```toml
[ollama]
enabled = true
model = "llama3"                    # or codellama, mistral, etc.
url = "http://localhost:11434"      # default Ollama server

default_provider = "ollama"         # Use local models by default
```

### **Usage Examples**

```bash
# Basic queries with local models
python intelliscript_cli_refactored.py "list all docker containers"
python intelliscript_cli_refactored.py "find files modified in last hour"
python intelliscript_cli_refactored.py "show disk usage by directory"

# Specify model explicitly
python intelliscript_cli_refactored.py "git commit with message" --provider ollama
python intelliscript_cli_refactored.py "compress logs older than 7 days" --provider ollama --model codellama

# Multi-turn conversations (with context)
python intelliscript_cli_refactored.py "show running processes" --context
python intelliscript_cli_refactored.py "kill the python ones" --context
```

---

## ☁️ **Cloud AI Providers**

### **OpenAI GPT-4**
- 🎯 **Best for**: Complex reasoning, natural language understanding
- 💰 **Cost**: ~$0.03/1K tokens (input), ~$0.06/1K tokens (output)
- 🚀 **Speed**: Fast responses, excellent quality

```bash
export OPENAI_API_KEY="sk-your-key"
python intelliscript_cli_refactored.py "complex database query" --provider openai
```

### **Anthropic Claude**
- 🎯 **Best for**: Code analysis, safety-conscious tasks
- 💰 **Cost**: ~$0.015/1K tokens (input), ~$0.075/1K tokens (output)  
- 🛡️ **Safety**: Excellent at avoiding dangerous commands

```bash
export ANTHROPIC_API_KEY="sk-ant-your-key"
python intelliscript_cli_refactored.py "system maintenance script" --provider anthropic
```

### **Google Gemini**
- 🎯 **Best for**: Fast responses, cost-effective
- 💰 **Cost**: ~$0.00125/1K tokens (lowest cost)
- ⚡ **Speed**: Very fast responses

```bash
export GOOGLE_API_KEY="your-key"
python intelliscript_cli_refactored.py "quick file operations" --provider google
```

---

## ⚙️ **Configuration**

### **Configuration File Location**
- **Primary**: `~/.config/intelliscript/config.toml`
- **Custom**: Use `--config /path/to/config.toml`

### **Complete Configuration Example**

```toml
# =============================================================================
# IntelliScript 2.0 Configuration
# =============================================================================

# Default provider (ollama, openai, anthropic, google)
default_provider = "ollama"

# Global settings
temperature = 0.2

# =============================================================================
# LOCAL MODELS (Ollama) - Privacy-First Option
# =============================================================================
[ollama]
enabled = true                              # Enable local models
model = "llama3"                            # Default model
url = "http://localhost:11434"              # Ollama server URL

# Available models (run 'ollama list' to see installed models):
# - llama3, llama3:8b, llama3:70b          # General purpose
# - codellama, codellama:7b, codellama:13b  # Code-focused
# - mistral, mistral:7b                     # Lightweight
# - qwen, qwen:7b, qwen:14b                 # Multi-language

# =============================================================================
# CLOUD AI PROVIDERS
# =============================================================================

[openai]
api_key = ""                                # Set via OPENAI_API_KEY env var
model = "gpt-4-turbo"                       # gpt-4-turbo, gpt-4, gpt-3.5-turbo
temperature = 0.2                           # 0.0-2.0

[anthropic]
api_key = ""                                # Set via ANTHROPIC_API_KEY env var  
model = "claude-3-5-sonnet-20241022"       # claude-3-5-sonnet, claude-3-haiku
max_tokens = 1024                           # Max response length
temperature = 0.2                           # 0.0-1.0

[google]
api_key = ""                                # Set via GOOGLE_API_KEY env var
model = "gemini-pro"                        # gemini-pro, gemini-pro-vision
temperature = 0.2                           # 0.0-1.0

# =============================================================================
# SECURITY SETTINGS
# =============================================================================
[security]
enabled = true                              # Enable safety checks
strict_mode = false                         # Extra strict for dangerous commands
dangerous_commands = [                      # Custom dangerous patterns
    "rm -rf", "mkfs", "> /dev/", "dd if=", ":(){ :|:& };:"
]

# =============================================================================
# CONVERSATION & HISTORY
# =============================================================================
[history]
enabled = true                              # Enable conversation memory
max_entries = 10                            # Max history entries to keep
save_to_file = false                        # Persist history to disk

# =============================================================================
# USER INTERFACE
# =============================================================================
[ui]
show_token_usage = true                     # Display token/cost info
colored_output = true                       # Colored terminal output
interactive_confirmation = true             # Ask before running commands
```

### **Environment Variables (Override Config File)**

```bash
# Provider selection
export INTELLISCRIPT_PROVIDER="ollama"     # Override default provider
export INTELLISCRIPT_MODEL="codellama"     # Override default model

# API Keys
export OPENAI_API_KEY="sk-your-openai-key"
export ANTHROPIC_API_KEY="sk-ant-your-claude-key"
export GOOGLE_API_KEY="your-google-key"

# Local model settings  
export OLLAMA_URL="http://localhost:11434"
export OLLAMA_MODEL="llama3"

# Debug
export INTELLISCRIPT_DEBUG="true"
```

---

## 📖 **Usage Examples**

### **File Operations**
```bash
# Find files
python intelliscript_cli_refactored.py "find all .log files larger than 100MB"
python intelliscript_cli_refactored.py "show recently modified Python files"

# Archive operations  
python intelliscript_cli_refactored.py "compress project folder excluding node_modules"
python intelliscript_cli_refactored.py "extract all ZIP files in downloads"
```

### **System Administration**
```bash
# Process management
python intelliscript_cli_refactored.py "show top 10 memory consuming processes"
python intelliscript_cli_refactored.py "kill all Chrome processes"

# Disk management
python intelliscript_cli_refactored.py "show disk usage by directory"
python intelliscript_cli_refactored.py "clean up old log files"
```

### **Development Tasks**
```bash
# Git operations
python intelliscript_cli_refactored.py "commit all changes with descriptive message"
python intelliscript_cli_refactored.py "create new branch for feature work"

# Docker management
python intelliscript_cli_refactored.py "stop all running containers"
python intelliscript_cli_refactored.py "clean up unused Docker images"
```

### **Multi-Turn Conversations**
```bash
# Start with context
python intelliscript_cli_refactored.py "show running docker containers" --context

# Follow up (remembers previous context)
python intelliscript_cli_refactored.py "stop the nginx one" --context
python intelliscript_cli_refactored.py "remove its image too" --context
```

---

## 🔧 **Advanced Features**

### **Command Safety**
```bash
# Safety checks enabled by default
python intelliscript_cli_refactored.py "delete system files"  # Will warn before execution

# Disable for advanced users (use carefully!)
python intelliscript_cli_refactored.py "force delete temp files" --no-safety
```

### **Save Commands as Scripts**
```bash
# Save generated commands to executable script
python intelliscript_cli_refactored.py "backup database" --save backup.sh
python intelliscript_cli_refactored.py "system maintenance" --save maintenance.sh
chmod +x backup.sh && ./backup.sh
```

### **Interactive Configuration**
```bash
# Guided setup
python intelliscript_cli_refactored.py config

# System diagnostics
python intelliscript_cli_refactored.py diag
```

### **Provider Comparison**
```bash
# Same query with different providers
python intelliscript_cli_refactored.py "optimize database" --provider ollama
python intelliscript_cli_refactored.py "optimize database" --provider openai
python intelliscript_cli_refactored.py "optimize database" --provider anthropic
```

---

## 🚀 **Performance & Cost Comparison**

| Provider | Cost/1K Tokens | Speed | Privacy | Offline | Best Use Case |
|----------|----------------|-------|---------|---------|---------------|
| **Ollama (Local)** | **FREE** | Fast | 🔒 Complete | ✅ Yes | Daily tasks, privacy-sensitive |
| **Google Gemini** | $0.00125 | Very Fast | ☁️ Cloud | ❌ No | Quick queries, cost optimization |
| **OpenAI GPT-4** | $0.030 | Fast | ☁️ Cloud | ❌ No | Complex reasoning, quality |
| **Anthropic Claude** | $0.015 | Medium | ☁️ Cloud | ❌ No | Code analysis, safety |

### **Recommendations**

- 🏠 **Privacy-First**: Use **Ollama** with llama3/codellama
- 💰 **Cost-Conscious**: Use **Google Gemini** for cloud queries
- 🎯 **Quality-First**: Use **OpenAI GPT-4** for complex tasks
- 🛡️ **Safety-First**: Use **Anthropic Claude** for system operations

---

## 🛠️ **Installation & Requirements**

### **System Requirements**
- **Python**: 3.8 or higher
- **OS**: Windows, macOS, Linux
- **Memory**: 2GB RAM minimum (8GB recommended for local models)
- **Storage**: 5-10GB for local models

### **Installation Methods**

#### **Method 1: From Source (Recommended)**
```bash
git clone https://github.com/hongping-zh/intelliscript.git
cd intelliscript
pip install -r requirements.txt

# Test installation
python intelliscript_cli_refactored.py --help
```

#### **Method 2: Direct Download**
Download the latest release from [GitHub Releases](https://github.com/hongping-zh/intelliscript/releases)

### **Dependencies**
```txt
# Core dependencies
requests>=2.28.0
toml>=0.10.0  
click>=8.0.0

# Cloud provider dependencies (optional)
openai>=1.0.0           # for OpenAI GPT-4
anthropic>=0.7.0        # for Claude
google-generativeai     # for Gemini

# Optional utilities
pyperclip              # clipboard support
colorama               # colored output
```

---

## 🔍 **Troubleshooting**

### **Ollama Issues**

**Problem**: "Cannot connect to Ollama"
```bash
# Solution: Start Ollama server
ollama serve

# Or check if running
curl http://localhost:11434/api/tags
```

**Problem**: "Model not found"
```bash
# Solution: List and download models
ollama list                    # See installed models
ollama pull llama3            # Download model
```

### **API Key Issues**

**Problem**: "API key not found"
```bash
# Solution: Set environment variables
export OPENAI_API_KEY="sk-your-key"

# Or use config file
python intelliscript_cli_refactored.py config
```

### **Import Errors**

**Problem**: "Module not found"
```bash
# Solution: Install dependencies
pip install -r requirements.txt

# Or install specific packages
pip install requests toml click openai anthropic google-generativeai
```

---

## 🤝 **Contributing**

We welcome contributions! Here's how to get started:

### **Development Setup**
```bash
# Fork and clone
git clone https://github.com/yourusername/intelliscript.git
cd intelliscript

# Create development environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install in development mode
pip install -e .
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/
```

### **Adding New Providers**
```python
# 1. Implement LLMProvider interface
class YourProvider(LLMProvider):
    def get_command(self, query, context):
        # Your implementation
        pass
    
    def is_available(self):
        # Check availability
        pass

# 2. Register in main app
# See src/core/intelliscript_main.py
```

---

## 📄 **License**

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🌟 **Star History**

<a href="https://github.com/hongping-zh/intelliscript/stargazers">
    <img width="500" alt="Star History Chart" src="https://api.star-history.com/svg?repos=hongping-zh/intelliscript&type=Date">
</a>

---

<div align="center">

**Made with ❤️ by the IntelliScript Team**

[⭐ Star us on GitHub](https://github.com/hongping-zh/intelliscript) • [🐛 Report Issues](https://github.com/hongping-zh/intelliscript/issues) • [💬 Discussions](https://github.com/hongping-zh/intelliscript/discussions)

</div>
