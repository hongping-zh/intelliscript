# ⚡ 快速开始

> 5分钟快速上手 IntelliScript CLI，体验AI智能命令执行！

## 📦 安装

### 方法一：从GitHub安装（推荐）

```bash
# 克隆仓库
git clone https://github.com/hongping-zh/intelliscript.git
cd intelliscript

# 安装依赖
pip install -r requirements.txt

# 直接运行
python intelliscript_cli_enhanced.py
```

### 方法二：使用setup.py安装

```bash
# 克隆并安装
git clone https://github.com/hongping-zh/intelliscript.git
cd intelliscript
python setup.py install

# 全局使用
intelliscript --help
```

## 🔧 基础配置

### 1. 配置AI模型

创建配置文件 `config.json`：

```json
{
  "model_provider": "anthropic",
  "api_key": "your_api_key_here",
  "model_name": "claude-3-5-sonnet-20241022",
  "max_tokens": 4096
}
```

### 2. 支持的AI模型

<!-- tabs:start -->

#### **Claude (Anthropic)**
```json
{
  "model_provider": "anthropic",
  "api_key": "sk-ant-xxx",
  "model_name": "claude-3-5-sonnet-20241022"
}
```

#### **GPT-4 (OpenAI)**
```json
{
  "model_provider": "openai", 
  "api_key": "sk-xxx",
  "model_name": "gpt-4-turbo"
}
```

#### **Gemini (Google)**
```json
{
  "model_provider": "google",
  "api_key": "your_gemini_key",
  "model_name": "gemini-pro"
}
```

<!-- tabs:end -->

## 🚀 第一次使用

### 启动交互模式

```bash
# 启动IntelliScript
python intelliscript_cli_enhanced.py

# 或者使用简化命令（如果已安装）
intelliscript
```

### 基础对话示例

```bash
🤖 IntelliScript CLI v1.0+ 
🛡️ 安全模式已启用

用户> 帮我查看当前目录下的所有Python文件
AI> 我来帮你查看当前目录下的所有Python文件：

执行命令: find . -name "*.py" -type f

./main.py
./utils.py
./config.py
./tests/test_main.py

用户> 统计这些文件的行数
AI> 我来统计这些Python文件的行数：

执行命令: wc -l *.py
     45 main.py
     23 utils.py
     12 config.py
     80 总计
```

## 🛡️ 安全功能演示

### 危险命令检测

```bash
用户> 删除所有临时文件
AI> ⚠️  HIGH RISK DETECTED ⚠️
命令: rm -rf /tmp/*
风险级别: HIGH
原因: 批量删除操作可能影响系统稳定性

确认执行此命令吗？[y/N]: n
操作已取消，为您提供更安全的替代方案：

替代命令: find /tmp -name "*" -type f -atime +7 -delete
说明: 只删除7天前的临时文件，更加安全
```

### 安全命令示例

```bash
# 检查单个命令的安全性
intelliscript security check "rm -rf /"

🔴 CRITICAL RISK: 此命令将删除整个文件系统！
风险等级: CRITICAL
建议: 绝对不要执行此命令

# 查看安全功能报告
intelliscript security report

📊 安全统计报告:
- 检测到的高危命令: 0
- 阻止的危险操作: 0  
- 安全确认次数: 0
- 会话缓存命令: 0
```

## 💡 实用示例

### 1. 系统监控

```bash
用户> 检查系统负载和内存使用情况
AI> 执行命令: top -bn1 | head -20 && free -h

load average: 0.50, 0.40, 0.35
内存使用: 4.2G/8.0G (52%)
```

### 2. 文件管理

```bash
用户> 创建今天日期的备份文件夹并复制重要配置
AI> 执行命令: 
mkdir -p backup/$(date +%Y-%m-%d)
cp ~/.bashrc ~/.vimrc backup/$(date +%Y-%m-%d)/

✅ 备份文件夹已创建: backup/2024-01-15/
✅ 配置文件已备份
```

### 3. 开发环境

```bash
用户> 启动Python开发服务器并在8080端口
AI> 执行命令: python -m http.server 8080

Serving HTTP on 0.0.0.0 port 8080 ...
🌐 服务器已启动: http://localhost:8080
```

## 🎯 高级功能

### 命令历史和缓存

```bash
# 查看命令历史
intelliscript history

# 重复执行上一个命令
intelliscript repeat

# 清除会话缓存
intelliscript cache clear
```

### 批量操作模式

```bash
# 批量文件处理
用户> 将所有.txt文件转换为大写并添加时间戳
AI> 我来为您批量处理：

for file in *.txt; do
  timestamp=$(date +%Y%m%d_%H%M%S)
  tr '[:lower:]' '[:upper:]' < "$file" > "${file%.txt}_${timestamp}.TXT"
done
```

## ❓ 常见问题

### Q: 如何停止正在执行的命令？
A: 按 `Ctrl+C` 可以中断当前命令执行。

### Q: 如何查看详细的执行日志？
A: 使用 `--verbose` 参数启动：`intelliscript --verbose`

### Q: 支持哪些操作系统？
A: 支持 Linux、macOS 和 Windows（WSL/PowerShell）

### Q: 如何更新到最新版本？
A: 执行 `git pull origin main` 然后重新安装

## 🔗 下一步

- 📖 阅读[详细使用指南](basic-usage.md)
- 🛡️ 了解[安全功能](security.md)  
- ⚙️ 查看[配置选项](configuration.md)
- 💡 浏览[使用示例](examples.md)

---

?> 💡 **小贴士**: 使用 `intelliscript --help` 查看所有可用命令和选项！
