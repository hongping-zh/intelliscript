# 📦 安装指南

> 详细的 IntelliScript CLI 安装说明，支持多种安装方式

## 🎯 系统要求

### 基础要求
- **Python**: 3.8+ (推荐 3.9+)
- **操作系统**: Linux, macOS, Windows (WSL/PowerShell)
- **内存**: 最少 512MB，推荐 1GB+
- **磁盘空间**: 约 50MB

### 依赖检查
```bash
# 检查Python版本
python --version
# 应输出: Python 3.8.x 或更高

# 检查pip版本
pip --version
```

## 🚀 安装方法

### 方法一：从源码安装 (推荐)

```bash
# 1. 克隆仓库
git clone https://github.com/hongping-zh/intelliscript.git
cd intelliscript

# 2. 创建虚拟环境 (可选但推荐)
python -m venv intelliscript-env
source intelliscript-env/bin/activate  # Linux/macOS
# 或 intelliscript-env\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 验证安装
python intelliscript_cli_enhanced.py --help
```

### 方法二：使用 setup.py 安装

```bash
# 克隆并安装
git clone https://github.com/hongping-zh/intelliscript.git
cd intelliscript
python setup.py install

# 全局使用
intelliscript --help
```

### 方法三：pip 直接安装

```bash
# 从GitHub直接安装
pip install git+https://github.com/hongping-zh/intelliscript.git

# 升级到最新版本
pip install --upgrade git+https://github.com/hongping-zh/intelliscript.git
```

## 🔧 配置设置

### 1. 创建配置文件

在用户目录创建 `.intelliscript/config.json`：

```bash
mkdir -p ~/.intelliscript
cat > ~/.intelliscript/config.json << EOF
{
  "model_provider": "anthropic",
  "api_key": "your_api_key_here",
  "model_name": "claude-3-5-sonnet-20241022",
  "max_tokens": 4096,
  "temperature": 0.1,
  "security": {
    "enabled": true,
    "strict_mode": false
  }
}
EOF
```

### 2. 环境变量设置

<!-- tabs:start -->

#### **Linux/macOS**
```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
export INTELLISCRIPT_API_KEY="your_api_key"
export INTELLISCRIPT_MODEL="claude-3-5-sonnet-20241022"
export INTELLISCRIPT_CONFIG="$HOME/.intelliscript/config.json"

# 重新加载配置
source ~/.bashrc
```

#### **Windows**
```powershell
# PowerShell
$env:INTELLISCRIPT_API_KEY="your_api_key"
$env:INTELLISCRIPT_MODEL="claude-3-5-sonnet-20241022"

# 或使用系统环境变量设置
setx INTELLISCRIPT_API_KEY "your_api_key"
```

<!-- tabs:end -->

## 🗝️ API密钥配置

### Anthropic Claude

1. 访问 [Anthropic Console](https://console.anthropic.com/)
2. 创建新的API密钥
3. 配置示例:
```json
{
  "model_provider": "anthropic",
  "api_key": "sk-ant-api03-...",
  "model_name": "claude-3-5-sonnet-20241022"
}
```

### OpenAI GPT-4

1. 访问 [OpenAI API](https://platform.openai.com/api-keys)
2. 生成API密钥
3. 配置示例:
```json
{
  "model_provider": "openai",
  "api_key": "sk-proj-...",
  "model_name": "gpt-4-turbo"
}
```

### Google Gemini

1. 访问 [Google AI Studio](https://makersuite.google.com/app/apikey)
2. 创建API密钥
3. 配置示例:
```json
{
  "model_provider": "google",
  "api_key": "AIza...",
  "model_name": "gemini-pro"
}
```

## ✅ 安装验证

### 基本验证
```bash
# 检查版本
intelliscript --version

# 检查配置
intelliscript config check

# 测试AI连接
intelliscript test connection
```

### 功能测试
```bash
# 安全功能测试
intelliscript security test

# 简单命令测试
echo "显示当前目录内容" | intelliscript exec

# 交互模式测试
intelliscript
> 帮我查看系统信息
```

## 🐛 常见安装问题

### 问题1：Python版本过低
```bash
错误: ImportError: This package requires Python 3.8+

解决方案:
# 升级Python到3.8+
sudo apt update && sudo apt install python3.9
# 或使用pyenv管理Python版本
```

### 问题2：依赖安装失败
```bash
错误: ERROR: Could not install packages due to an EnvironmentError

解决方案:
# 使用虚拟环境
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 问题3：权限问题
```bash
错误: PermissionError: [Errno 13] Permission denied

解决方案:
# 使用用户安装
pip install --user git+https://github.com/hongping-zh/intelliscript.git

# 或修复权限
sudo chown -R $USER:$USER ~/.local/lib/python3.x/site-packages/
```

### 问题4：API密钥无效
```bash
错误: AuthenticationError: Invalid API key

解决方案:
# 检查API密钥格式
intelliscript config validate

# 重新设置API密钥
intelliscript config set api_key "your_new_key"
```

## 🔄 更新升级

### 检查更新
```bash
# 检查是否有新版本
intelliscript update check

# 查看更新日志
intelliscript changelog
```

### 升级到最新版
```bash
# 从git更新
cd intelliscript
git pull origin main
pip install -r requirements.txt

# 或重新安装
pip install --upgrade git+https://github.com/hongping-zh/intelliscript.git
```

## 🐳 Docker安装

### 使用Docker运行
```bash
# 构建Docker镜像
git clone https://github.com/hongping-zh/intelliscript.git
cd intelliscript
docker build -t intelliscript .

# 运行容器
docker run -it --rm \
  -e INTELLISCRIPT_API_KEY="your_api_key" \
  intelliscript
```

### Docker Compose
```yaml
version: '3.8'
services:
  intelliscript:
    build: .
    environment:
      - INTELLISCRIPT_API_KEY=${API_KEY}
      - INTELLISCRIPT_MODEL=claude-3-5-sonnet-20241022
    volumes:
      - ./configs:/app/configs
    stdin_open: true
    tty: true
```

## 🏢 企业部署

### 批量安装脚本
```bash
#!/bin/bash
# enterprise-install.sh

set -e

echo "IntelliScript 企业批量安装"

# 检查Python版本
if ! python3 --version | grep -q "Python 3.[8-9]"; then
    echo "错误: 需要Python 3.8+"
    exit 1
fi

# 安装到指定目录
INSTALL_DIR="/opt/intelliscript"
sudo mkdir -p $INSTALL_DIR
cd $INSTALL_DIR

# 下载并安装
sudo git clone https://github.com/hongping-zh/intelliscript.git .
sudo python3 -m pip install -r requirements.txt

# 创建符号链接
sudo ln -sf $INSTALL_DIR/intelliscript_cli_enhanced.py /usr/local/bin/intelliscript

echo "✅ IntelliScript 安装完成"
echo "使用 'intelliscript --help' 开始使用"
```

### 系统服务配置
```ini
# /etc/systemd/system/intelliscript.service
[Unit]
Description=IntelliScript CLI Service
After=network.target

[Service]
Type=simple
User=intelliscript
Group=intelliscript
WorkingDirectory=/opt/intelliscript
ExecStart=/usr/local/bin/intelliscript daemon
Restart=always

[Install]
WantedBy=multi-user.target
```

## 📋 卸载指南

### 完整卸载
```bash
# 停止所有进程
pkill -f intelliscript

# 删除安装文件
rm -rf ~/.intelliscript/
pip uninstall intelliscript

# 删除源码目录 (如果从源码安装)
rm -rf ~/intelliscript

# 清理环境变量
unset INTELLISCRIPT_API_KEY
unset INTELLISCRIPT_MODEL
```

## 🔗 下一步

安装完成后，您可以：

- 🚀 [快速开始](quickstart.md) - 5分钟上手指南
- ⚙️ [配置选项](configuration.md) - 详细配置说明
- 🛡️ [安全功能](security.md) - 了解安全特性
- 💡 [使用示例](examples.md) - 实用案例集合

---

?> 💡 **小贴士**: 建议使用虚拟环境安装，避免与其他Python包冲突！
