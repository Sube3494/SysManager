# 服务器命令执行插件

通过QQ消息在服务器上执行命令并获取结果。**支持 Windows / Linux / macOS**

## ✨ 功能特性

- 📡 **命令传递** - 直接执行任意系统命令
- 🖥️ **跨平台支持** - Windows、Linux、macOS 通用
- 📂 **目录管理** - 支持 cd 切换目录，每个用户独立会话
- 📜 **命令历史** - 记录最近50条命令，可查看历史
- 🚫 **交互式命令拦截** - 自动检测 vim、top 等交互式命令并给出替代建议
- 🎨 **智能输出优化** - 自动美化 df、free、ps、netstat 等常用命令
- 💪 **强制全部输出** - 使用 -f 参数跳过长度限制
- 🔐 **权限控制** - 仅AstrBot管理员可用
- 📝 **操作日志** - 记录所有执行的命令
- ⏱️ **超时保护** - 防止命令卡死

## 📦 安装

```bash
pip install psutil
```

## ⚙️ 配置管理员

本插件使用AstrBot核心管理员系统：

```bash
/sid        # 查看你的用户ID
/op 你的ID  # 授权为管理员
```

## 🚀 使用方法

### 基本命令

```bash
/sys <命令>          # 执行系统命令
/sys <命令> -f       # 强制输出全部内容
```

### 内置命令

```bash
/sys pwd             # 显示当前工作目录
/sys history         # 查看命令历史
/sys h               # 查看命令历史（简写）
/sys reset           # 重置工作目录
```

### 目录管理

```bash
/sys ls              # 列出当前目录
/sys cd /var/log     # 切换到 /var/log
/sys ls              # 列出 /var/log 的文件
/sys cd ..           # 返回上级目录
/sys pwd             # 查看当前在哪里
/sys reset           # 重置回初始目录
```

### 常用示例

**Linux/macOS:**
```bash
/sys ls -la
/sys df -h           # 磁盘使用（带优化）
/sys free -h         # 内存使用（带优化）
/sys ps aux          # 进程列表（前10条）
/sys netstat -antp   # 网络连接（带统计）
/sys cat /etc/os-release
/sys tail -f /var/log/syslog -f    # 查看日志（全部输出）
```

**Windows:**
```bash
/sys dir
/sys ipconfig
/sys tasklist
/sys systeminfo      # 系统信息（提取关键信息）
/sys netstat -an     # 网络连接（带统计）
```

## 🚫 不支持的交互式命令

以下命令会被自动拦截并给出替代建议：

| 命令 | 原因 | 替代方案 |
|------|------|---------|
| `vim`/`vi`/`nano` | 文本编辑器需要交互 | `cat <文件>` 查看内容 |
| `top`/`htop` | 实时监控需要交互 | `top -bn1 \| head -20` 或 `ps aux` |
| `less`/`more` | 分页查看需要交互 | `cat <文件>` 或 `head`/`tail` |
| `bash`/`sh`/`zsh` | 进入shell需要交互 | 直接执行命令 |
| `passwd` | 修改密码需要输入 | 直接登录服务器操作 |
| `mysql`/`psql` | 交互式数据库 | `mysql -e '查询'` |
| `python`/`node` | 交互式解释器 | `python -c '代码'` 或执行脚本 |

**示例：**
```bash
# ❌ 不支持
/sys vim config.txt

# ✅ 替代方案
/sys cat config.txt
/sys head -20 config.txt
/sys tail -50 config.txt
/sys grep "keyword" config.txt
```

## ⚙️ 插件配置

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `enabled_groups` | 生效的群组列表 | `[]` (所有群) |
| `command_timeout` | 命令执行超时时间（秒） | 30 |
| `max_output_length` | 最大输出长度（字符） | 2000 |
| `log_operations` | 是否记录操作日志 | true |

### 群组白名单配置

**留空（默认）：** 所有群和私聊都生效
```json
{
  "enabled_groups": []
}
```

**指定群组：** 只在指定的群中生效
```json
{
  "enabled_groups": [123456789, 987654321]
}
```

**如何获取群号：**
1. 在群里发送 `/sid`
2. 查看返回的 session_id，格式类似：`aiocqhttp:GroupMessage:123456789`
3. 最后的数字就是群号

## 🎨 智能输出优化

自动优化以下命令的输出：

- `df -h` - 磁盘使用（格式化，简洁显示）
- `free -h` - 内存使用（提取关键信息）
- `ps aux` - 进程列表（只显示前10条）
- `ls -la` - 文件列表（保持原样）
- `dir` - Windows文件列表
- `netstat` - 网络连接（统计状态）
- `systeminfo` - Windows系统信息（提取关键信息）
- 其他命令 - 去除多余空行

## 💡 使用技巧

### 1. 处理长输出

```bash
# 自动截断（默认）
/sys cat large.log

# 强制全部输出
/sys cat large.log -f

# 使用管道过滤（推荐）
/sys cat large.log | head -50
/sys cat large.log | tail -100
/sys cat large.log | grep "ERROR"
```

### 2. 目录管理

```bash
/sys cd /var/log     # 切换目录
/sys pwd             # 确认当前目录
/sys ls              # 在当前目录执行
/sys cd ../..        # 相对路径
/sys reset           # 重置目录
```

### 3. 查看历史

```bash
/sys history         # 查看最近10条命令
/sys h               # 简写
```

### 4. 后台进程

```bash
# Linux - 不要使用 &，可能导致问题
/sys nohup python app.py > app.log 2>&1 &
/sys ps aux | grep python    # 查看是否运行

# Windows
/sys start /B python app.py
```

## ⚠️ 安全提示

1. **仅管理员可用** - 使用AstrBot核心权限系统
2. **可限制生效群组** - 配置 `enabled_groups` 限制只在特定群生效
3. **所有命令会被记录** - 便于审计
4. **无命令限制** - 可执行任意命令（除了交互式命令）
5. **谨慎使用危险命令** - rm、del、format 等会直接执行
6. **-f 参数慎用** - 可能导致超长输出刷屏
7. **私聊默认允许** - 即使设置了群组白名单，私聊管理员也可用

## 📝 操作日志

所有命令都会记录在AstrBot控制台：

```
[操作日志] 2024-11-19 00:18:40 | 用户:123456 | 命令:ls -la
```

## 🔧 故障排查

**Q: 提示权限不足？**
- 确认你是AstrBot管理员：`/sid` 查看ID

**Q: cd 后目录没变？**
- 现在已支持！每个用户独立的会话状态

**Q: 想用vim编辑文件？**
- 不支持交互式命令，建议用 `cat` 查看，或直接登录服务器

**Q: 输出被截断？**
- 使用 `-f` 参数：`/sys cat file -f`
- 或使用管道：`/sys cat file | head -100`

**Q: 命令执行很慢？**
- 某些命令（如 find）可能需要较长时间
- 可在配置中增加 `command_timeout`

**Q: 想限制只在某些群使用？**
- 配置 `enabled_groups`，填入群号
- 使用 `/sid` 在群里查看群号
- 留空表示所有群都可用

## 📋 系统要求

- Python 3.8+
- AstrBot v4.5.0+
- psutil 库

## 📄 许可证

Apache License 2.0

---

**功能完整，简洁实用，开箱即用！** 🎯
