# 服务器命令执行插件

通过QQ消息在服务器上执行命令并获取结果。**支持 Windows / Linux / macOS**

## ✨ 功能

- 📡 **命令传递** - 直接执行任意系统命令
- 🖥️ **跨平台支持** - Windows、Linux、macOS 通用
- 🔧 **自定义前缀** - 可自定义命令前缀（如 /sys、/cmd、/sh等）
- 🎨 **智能优化输出** - 自动美化常用命令的输出（df、free、ps、netstat等）
- 📤 **结果返回** - 实时返回命令执行结果
- 🔐 **权限控制** - 仅AstrBot管理员可用
- 📝 **操作日志** - 记录所有执行的命令
- ⏱️ **超时保护** - 防止命令卡死
- 📏 **输出限制** - 避免输出过长刷屏

## 📦 安装

```bash
pip install psutil
```

## ⚙️ 配置管理员

本插件使用AstrBot核心管理员系统：

**方法一：QQ命令**
```bash
/sid        # 查看你的用户ID
/op 你的ID  # 授权为管理员
```

**方法二：Web面板**
- 配置 → 基本设置 → 管理员 ID

**方法三：编辑配置**
- 编辑 `data/cmd_config.json`
- 在 `admins_id` 中添加你的ID

## 🚀 使用方法

### 基本用法

```bash
/sys <命令>
```

如果修改了命令前缀，使用你配置的前缀：
```bash
/cmd <命令>    # 如果前缀改为 cmd
/sh <命令>     # 如果前缀改为 sh
/exec <命令>   # 如果前缀改为 exec
```

### Linux/macOS 常用示例

```bash
# 查看文件列表
/sys ls -la

# 查看磁盘空间
/sys df -h

# 查看内存使用
/sys free -h

# 查看进程
/sys ps aux | grep python

# 查看系统负载
/sys top -bn1 | head -20

# 查看网络连接
/sys netstat -antp

# 查看系统信息
/sys uname -a

# 查看文件内容
/sys cat /etc/os-release

# 执行多条命令
/sys df -h && free -h && uptime
```

### Windows 常用示例

```bash
# 查看文件列表
/sys dir

# 查看磁盘空间
/sys wmic logicaldisk get size,freespace,caption

# 查看内存使用
/sys systeminfo | findstr /C:"内存"

# 查看进程
/sys tasklist

# 查看网络配置
/sys ipconfig /all

# 查看网络连接
/sys netstat -an

# 查看系统信息
/sys systeminfo

# 查看服务
/sys sc query

# 执行多条命令
/sys dir && ipconfig
```

## ⚙️ 插件配置

在Web面板 → 插件管理 → 服务器管理 → 配置：

### 可配置项

| 配置项 | 说明 | 默认值 | 示例 |
|--------|------|--------|------|
| **命令前缀** | 自定义触发命令 | `sys` | `cmd`, `sh`, `exec` |
| **命令执行超时时间** | 命令最长执行时间（秒） | `30` | `10-60` |
| **最大输出长度** | 输出结果最大字符数 | `2000` | `1000-3000` |
| **记录操作日志** | 是否记录所有命令 | `true` | `true/false` |

### 自定义命令前缀示例

修改 `command_prefix` 配置：

```json
{
  "command_prefix": "cmd"
}
```

重启插件后，使用新前缀：
```bash
/cmd ls -la      # 使用 cmd 前缀
/cmd ipconfig    # 使用 cmd 前缀
```

**推荐的前缀：**
- `sys` - 默认，简短通用
- `cmd` - 常见，易记
- `sh` - 适合Linux用户
- `exec` - 明确表达执行命令
- `$` - 极简风格（需确保不与其他插件冲突）

## 📝 操作日志

所有命令执行都会记录在AstrBot日志中：

**日志位置：**
- 控制台输出
- AstrBot日志系统（可通过Web面板查看）

**日志格式：**
```
[操作日志] 2024-01-20 10:30:00 | 用户:ID | 命令:ls -la
```

## ⚠️ 安全提示

1. **仅管理员可用** - 使用AstrBot核心权限系统
2. **命令会被记录** - 所有操作记录在日志中
3. **谨慎使用危险命令** - rm、del、format 等会直接执行
4. **无命令限制** - 可执行任意命令，请确保管理员可信
5. **注意输出长度** - 超长输出会被截断
6. **不同系统命令不同** - Windows和Linux命令语法不同
7. **前缀不要冲突** - 避免与其他插件的命令前缀重复

## 🔧 故障排查

**Q: 提示权限不足？**
- 确认你是AstrBot管理员（`/sid` 查看ID）
- 在核心配置中添加你的ID

**Q: 命令执行失败？**
- 检查命令语法是否正确（Windows和Linux不同）
- 查看返回码和错误信息
- 某些命令可能需要管理员/root权限

**Q: 输出被截断？**
- 在配置中增加 `max_output_length`
- 或使用管道过滤输出：`| head -50`（Linux）或 `| findstr "xxx"`（Windows）

**Q: 命令在Windows上不工作？**
- 确认使用Windows命令（如 `dir` 而不是 `ls`）
- 某些Linux命令在Windows上需要安装额外工具

**Q: 修改前缀后不生效？**
- 确认已保存配置
- 重启插件或重启AstrBot
- 检查配置文件格式是否正确

**Q: 前缀冲突？**
- 在AstrBot中使用 `/help` 查看所有已注册的命令
- 选择一个不冲突的前缀

## 🎨 智能输出优化

插件会自动识别并优化以下常用命令的输出：

### Linux/macOS 优化命令

| 命令 | 优化效果 |
|------|---------|
| `df -h` | 💾 格式化磁盘使用率，带颜色告警（>90%红色，>80%黄色） |
| `free -h` | 💾 美化内存使用情况，清晰显示总量/可用/已用 |
| `ps aux` | 🔄 只显示前10个进程，提取CPU和内存占用 |
| `ls -la` | 📁 添加文件夹🔗图标，统计文件和目录数量 |
| `netstat` | 🌐 统计连接状态，显示ESTABLISHED/LISTEN数量 |
| `uptime` | ⏱️ 格式化系统运行时间 |

### Windows 优化命令

| 命令 | 优化效果 |
|------|---------|
| `dir` | 📁 统计目录和文件数量 |
| `systeminfo` | 💻 提取关键系统信息（OS、处理器、内存等） |
| `netstat` | 🌐 统计连接状态 |

### 示例对比

**优化前：**
```
/sys df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       100G   85G   15G  85% /
/dev/sdb1       500G  450G   50G  90% /data
```

**优化后：**
```
💾 磁盘使用情况
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🟡 /
   使用率: 85% | 设备: /dev/sda1
🔴 /data
   使用率: 90% | 设备: /dev/sdb1
```

### 所有命令的基础优化

- ✅ 自动去除多余空行
- ✅ 整理输出格式
- ✅ 保持可读性

## 🎯 使用技巧

### 1. 选择合适的前缀

```bash
# 如果主要管理Linux服务器
command_prefix: "sh"

# 如果是Windows服务器
command_prefix: "cmd"

# 如果想要简短
command_prefix: "x"

# 如果想要明确
command_prefix: "exec"
```

### 2. 处理长输出

```bash
# Linux
/sys dmesg | tail -50
/sys journalctl -n 50

# Windows
/sys dir | findstr ".txt"
/sys tasklist | findstr "python"
```

### 3. 检查服务状态

```bash
# Linux
/sys systemctl status nginx
/sys ps aux | grep nginx

# Windows
/sys sc query nginx
/sys tasklist | findstr nginx
```

## 📋 系统要求

- Python 3.8+
- AstrBot v4.5.0+
- psutil 库
- 支持的操作系统：
  - ✅ Windows 10/11
  - ✅ Windows Server 2016+
  - ✅ Linux (所有发行版)
  - ✅ macOS 10.14+

## 📄 许可证

Apache License 2.0

---

**跨平台支持，自定义前缀，随时随地管理你的服务器！** 🌍
