# 🛡️ 安全功能

> IntelliScript 的核心安全系统，保护您的系统免受危险命令伤害

## 🎯 安全概述

IntelliScript 内置了企业级安全防护系统，能够：

- 🔍 **智能检测** - 自动识别50+种危险命令模式
- 📊 **风险评估** - 四级风险分类系统 
- 🎨 **可视警告** - 彩色高亮显示危险程度
- 🔐 **多重确认** - 根据风险级别要求不同确认方式
- 💾 **会话缓存** - 智能记忆，避免重复确认

## 🚨 风险等级分类

### 🟢 LOW - 低风险
**特征**: 基础查看、查询操作
```bash
✅ 安全示例:
ls -la
cat file.txt  
ps aux
df -h
```

### 🟡 MEDIUM - 中等风险
**特征**: 文件修改、网络操作
```bash
⚠️ 中等风险示例:
chmod 755 script.sh
wget https://example.com/file
curl -O https://api.com/data
```

### 🟠 HIGH - 高风险
**特征**: 批量删除、系统修改
```bash
🔶 高风险示例:
rm *.log
sudo apt-get remove
iptables -F
systemctl stop service
```

### 🔴 CRITICAL - 极度危险
**特征**: 系统破坏性操作
```bash
🚫 极度危险示例:
rm -rf /
mkfs.ext4 /dev/sda
dd if=/dev/zero of=/dev/sda
:(){ :|:& };:
```

## 🔍 危险命令检测模式

### 文件系统破坏
```python
patterns = {
    r'rm\s+-rf\s+/': 'CRITICAL - 删除根目录',
    r'mkfs\.\w+': 'CRITICAL - 格式化磁盘',
    r'dd\s+if=.*of=/dev/': 'CRITICAL - 写入设备',
    r'shred\s+/dev/': 'CRITICAL - 擦除设备'
}
```

### 系统服务影响
```python
patterns = {
    r'killall\s+-9': 'HIGH - 强制终止所有进程',
    r'systemctl\s+stop\s+\*': 'HIGH - 停止所有服务',
    r'service\s+.+\s+stop': 'MEDIUM - 停止服务'
}
```

### 网络安全风险
```python
patterns = {
    r'iptables\s+-F': 'HIGH - 清空防火墙规则',
    r'ufw\s+disable': 'MEDIUM - 禁用防火墙',
    r'nc\s+.*-e': 'HIGH - 反向Shell'
}
```

## 🎨 交互式确认系统

### CRITICAL级别确认
```bash
🔴⚠️  CRITICAL RISK DETECTED ⚠️🔴
Command: rm -rf /
Risk Level: CRITICAL
Reason: Attempts to delete entire root filesystem

🚫 This command could cause IRREVERSIBLE DAMAGE!

To proceed, type exactly: 'CONFIRM DELETE EVERYTHING'
> _
```

### HIGH级别确认
```bash
🟠 HIGH RISK DETECTED
Command: chmod 777 /etc/passwd
Risk Level: HIGH  
Reason: Dangerous permissions on system file

Type 'CONFIRM HIGH RISK' to proceed: _
```

### MEDIUM级别确认
```bash
🟡 MEDIUM RISK: wget https://unknown-site.com/script.sh
Continue? [y/N]: _
```

## 🔧 CLI安全命令

### 检查命令安全性
```bash
# 检查单个命令
intelliscript security check "rm -rf /tmp/*"

🟠 HIGH RISK DETECTED
Command: rm -rf /tmp/*
Risk Level: HIGH
Reason: Bulk deletion in system directory
Recommendation: Use find with -mtime for safer cleanup
```

### 查看安全报告
```bash
intelliscript security report

📊 IntelliScript 安全报告
=======================
🕒 报告时间: 2024-01-15 10:30:25

📈 统计数据:
- 总检测次数: 1,247
- 阻止危险命令: 12
- CRITICAL级阻止: 2
- HIGH级阻止: 7  
- MEDIUM级阻止: 3

🚫 最近阻止的危险命令:
1. rm -rf / (CRITICAL) - 2024-01-15 09:45
2. chmod 777 /etc (HIGH) - 2024-01-15 08:20
3. killall -9 bash (HIGH) - 2024-01-14 16:30
```

### 运行安全测试
```bash
intelliscript security test

🧪 运行安全系统测试...

✅ 危险模式匹配: PASS (50/50)
✅ 风险级别分类: PASS  
✅ 确认机制: PASS
✅ 缓存系统: PASS
✅ 彩色输出: PASS

🎉 所有安全测试通过！
```

## ⚙️ 安全配置选项

### 自定义危险模式
```json
{
  "security": {
    "custom_patterns": {
      "company_sensitive": {
        "pattern": "rm.*company_data",
        "level": "CRITICAL",
        "message": "禁止删除公司敏感数据"
      }
    }
  }
}
```

### 风险等级调整
```json
{
  "security": {
    "risk_levels": {
      "chmod_777": "CRITICAL",  // 提升到CRITICAL
      "wget_http": "LOW"        // 降低到LOW
    }
  }
}
```

## 🎯 最佳实践

### ✅ DO - 建议做法
- **启用安全模式**: 始终在安全模式下运行
- **仔细阅读警告**: 不要忽视风险提示
- **使用安全替代**: 接受AI建议的安全替代方案
- **定期检查报告**: 查看安全统计报告

### ❌ DON'T - 避免做法  
- **强制跳过确认**: 不要盲目确认危险操作
- **禁用安全功能**: 不要关闭安全检测
- **忽视风险等级**: 重视CRITICAL和HIGH级警告
- **在生产环境测试**: 避免在生产系统测试危险命令

## 🧪 安全测试示例

### 测试危险命令检测
```bash
# 测试文件系统破坏
echo "rm -rf /" | intelliscript security check

# 测试系统服务影响  
echo "systemctl stop *" | intelliscript security check

# 测试网络安全风险
echo "iptables -F" | intelliscript security check
```

### 模拟攻击场景
```bash
# Fork炸弹测试
intelliscript security check ":(){ :|:& };:"

🔴 CRITICAL: Fork bomb detected!
This will consume all system resources and crash the system.
```

## 📊 技术实现

### 检测算法
```python
def assess_risk(command: str) -> RiskLevel:
    """评估命令风险等级"""
    for pattern, risk_info in DANGEROUS_PATTERNS.items():
        if re.search(pattern, command, re.IGNORECASE):
            return RiskLevel(
                level=risk_info.level,
                reason=risk_info.reason,
                recommendation=risk_info.recommendation
            )
    return RiskLevel.LOW
```

### 缓存机制
```python
class CommandCache:
    """命令确认缓存"""
    def __init__(self, ttl: int = 3600):
        self.cache = {}
        self.ttl = ttl
    
    def is_confirmed(self, command_hash: str) -> bool:
        """检查命令是否已确认"""
        return command_hash in self.cache
```

## 🔗 相关资源

- 📖 [CLI命令参考](cli-reference.md)
- 🎯 [最佳实践](best-practices.md)
- ❓ [常见问题](faq.md)
- 🐛 [故障排除](troubleshooting.md)

---

!> ⚠️ **重要提醒**: 安全功能旨在保护您的系统，但不应完全依赖。请始终谨慎执行命令，特别是在生产环境中。
