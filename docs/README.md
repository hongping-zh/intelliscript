# IntelliScript CLI 

> 🚀 AI智能脚本执行工具 - 让命令行操作更安全、更智能

[![GitHub Stars](https://img.shields.io/github/stars/hongping-zh/intelliscript?style=social)](https://github.com/hongping-zh/intelliscript)
[![License](https://img.shields.io/github/license/hongping-zh/intelliscript)](https://github.com/hongping-zh/intelliscript/blob/main/LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![GitHub Issues](https://img.shields.io/github/issues/hongping-zh/intelliscript)](https://github.com/hongping-zh/intelliscript/issues)

## 🎯 项目概述

IntelliScript CLI 是一款革命性的AI驱动命令行工具，它能够：

- 🤖 **智能理解**：将自然语言转换为精确的系统命令
- 🛡️ **安全防护**：智能检测并阻止危险命令执行
- ⚡ **高效执行**：一键完成复杂的多步骤操作
- 🌍 **全球支持**：完整的多语言界面和文档

## ✨ 核心特性

### 🤖 多AI模型支持
- **Claude 3.5 Sonnet** - Anthropic最新模型
- **GPT-4 Turbo** - OpenAI旗舰模型  
- **Gemini Pro** - Google先进AI
- **可扩展架构** - 轻松集成更多模型

### 🛡️ 企业级安全
- **危险命令检测** - 自动识别`rm -rf`、`mkfs`等高危操作
- **多级风险评估** - LOW/MEDIUM/HIGH/CRITICAL 四级风险分类
- **交互式确认** - 彩色警告 + 多重确认机制
- **会话缓存** - 智能记忆，避免重复确认

### 🎨 优秀的用户体验
- **彩色输出** - 直观的终端界面
- **实时反馈** - 命令执行状态展示
- **智能补全** - 上下文感知的建议
- **错误恢复** - 智能错误处理和修复建议

## 🚀 快速开始

### 安装
```bash
# 从GitHub安装最新版本
pip install git+https://github.com/hongping-zh/intelliscript.git

# 或使用setup.py安装
git clone https://github.com/hongping-zh/intelliscript.git
cd intelliscript
python setup.py install
```

### 基础使用
```bash
# 启动智能CLI
python intelliscript_cli_enhanced.py

# 安全检查单个命令
intelliscript security check "rm -rf /tmp/test"

# 查看安全报告
intelliscript security report
```

## 📊 应用场景

<!-- tabs:start -->

#### ** 🖥️ 系统管理**

```bash
用户输入: "清理所有.log文件，但保留最近3天的"
IntelliScript: find /var/log -name "*.log" -type f -mtime +3 -delete
```

#### ** 🚀 DevOps**

```bash
用户输入: "部署应用并检查服务状态"
IntelliScript: 
  docker build -t myapp .
  docker run -d --name myapp-prod myapp
  docker ps | grep myapp
```

#### ** 📁 文件管理**

```bash
用户输入: "备份重要配置文件到时间戳文件夹"
IntelliScript:
  mkdir -p backup/$(date +%Y%m%d_%H%M%S)
  cp /etc/nginx/nginx.conf backup/$(date +%Y%m%d_%H%M%S)/
```

<!-- tabs:end -->

## 🛡️ 安全演示

### 危险命令检测示例

```bash
⚠️  CRITICAL RISK DETECTED ⚠️
Command: rm -rf /
Risk Level: CRITICAL
Reason: Attempts to delete entire root filesystem

🔴 This command could cause IRREVERSIBLE DAMAGE to your system!

Type 'CONFIRM DELETE EVERYTHING' to proceed: _
```

## 🎯 核心优势

| 功能 | IntelliScript | 传统CLI |
|------|---------------|---------|
| **自然语言输入** | ✅ 支持 | ❌ 不支持 |
| **危险命令检测** | ✅ 多级防护 | ❌ 无保护 |
| **AI智能建议** | ✅ 上下文感知 | ❌ 无智能 |
| **多语言支持** | ✅ 中英双语 | ❌ 单语 |
| **会话记忆** | ✅ 智能缓存 | ❌ 无记忆 |

## 📈 项目统计

- 🌟 **2,800+ 行代码** - 企业级质量
- 🛡️ **50+ 危险模式** - 全面安全防护
- 🌍 **2 语言支持** - 中文 + English
- 📚 **完整文档** - 详细使用指南
- 🧪 **全面测试** - 稳定可靠

## 🤝 参与贡献

我们欢迎社区贡献！查看 [贡献指南](contributing.md) 了解如何参与：

- 🐛 [报告Bug](https://github.com/hongping-zh/intelliscript/issues)
- 💡 [功能建议](https://github.com/hongping-zh/intelliscript/issues)  
- 🔧 [提交代码](https://github.com/hongping-zh/intelliscript/pulls)
- 📚 [完善文档](https://github.com/hongping-zh/intelliscript/tree/main/docs)

## 📞 联系我们

- 📧 **Email**: support@intelliscript.dev
- 💬 **讨论区**: [GitHub Discussions](https://github.com/hongping-zh/intelliscript/discussions)
- 🐛 **问题反馈**: [Issues](https://github.com/hongping-zh/intelliscript/issues)

---

<div align="center">

**如果觉得IntelliScript对你有帮助，请给我们一个⭐️！**

[⭐ Star](https://github.com/hongping-zh/intelliscript) | [🍴 Fork](https://github.com/hongping-zh/intelliscript/fork) | [📋 Issues](https://github.com/hongping-zh/intelliscript/issues)

</div>
