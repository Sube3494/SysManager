# 🖥️ SysManager - AstrBot服务器管理插件

通过QQ消息安全地执行服务器命令，支持Windows/Linux/macOS系统。

## ✨ 主要功能

- **🔐 权限控制** - 使用AstrBot核心管理员系统
- **📍 群组限制** - 可配置只在指定群生效
- **🌍 跨平台** - Windows/Linux/macOS全支持
- **📂 会话目录** - 每个用户独立的工作目录
- **📜 命令历史** - 记录并查看历史命令
- **🎨 输出优化** - 智能格式化常用命令输出
- **🚫 安全防护** - 自动拦截交互式命令
- **📏 输出控制** - 支持截断和强制全部输出

## 📥 安装方法

### 方法1：Web面板安装
1. 打开AstrBot Web管理面板
2. 进入 插件管理 → 插件商店
3. 搜索"SysManager"
4. 点击安装并配置

### 方法2：手动安装
1. 下载插件到 `data/plugins/` 目录
2. 重启AstrBot
3. 在Web面板中配置插件

## ⚙️ 插件配置

在Web面板 → 插件管理 → SysManager → 配置 中设置：

| 配置项 | 说明 | 默认值 | 示例 |
|--------|------|--------|------|
| `enabled_groups` | 生效的群组列表 | `[]` (所有群) | `[123456789, 987654321]` |
| `command_timeout` | 命令执行超时时间（秒） | 30 | 10-60 |
| `max_output_length` | 最大输出长度（字符） | 2000 | 1000-5000 |
| `log_operations` | 是否记录操作日志 | true | true/false |

### 📍 群组限制配置说明

**1. 不限制（默认）**
```json
{
  "enabled_groups": []
}
```
效果：所有群和私聊都可以使用

**2. 限制特定群**
```json
{
  "enabled_groups": [123456789, 987654321]
}
```
效果：
- ✅ 只在群 123456789 和 987654321 中生效
- ✅ 私聊仍然可用（管理员）
- ❌ 其他群静默忽略命令

**3. 如何获取群号**
在群里发送 `/sid`，返回格式：
```
aiocqhttp:GroupMessage:123456789
```
最后的数字 `123456789` 就是群号

## 🚀 使用方法

### 基本语法
```
/sys <命令> [参数] [-f]
```

### 📝 内置命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `pwd` | 显示当前工作目录 | `/sys pwd` |
| `history` | 查看最近10条命令历史 | `/sys history` |
| `reset` | 重置到初始目录 | `/sys reset` |

### 💬 系统命令

执行任何Linux/Windows命令：
```bash
/sys ls                  # 列出文件
/sys cd /var/log        # 切换目录（会保持状态）
/sys cat config.txt     # 查看文件
/sys df -h              # 查看磁盘使用
/sys ps aux             # 查看进程
/sys netstat -antp      # 查看网络连接
```

### 📄 输出控制

**自动截断（默认）：**
```
/sys cat large.txt
# 超过2000字符会截断，显示提示
```

**强制全部输出：**
```
/sys cat large.txt -f
# 使用 -f 参数显示全部内容
```

## 🎨 智能输出优化

以下命令会自动优化输出格式：

### Linux命令
- `df -h` - 磁盘使用统计
- `free -h` - 内存使用状态
- `ps aux` - 进程列表（前10条）
- `ls/dir` - 文件列表（分类显示）
- `netstat` - 网络连接统计
- `uptime` - 系统运行时间

### Windows命令
- `systeminfo` - 系统信息摘要

## 🚫 交互式命令处理

自动检测并提供替代方案：

| 命令 | 用途 | 替代方案 |
|------|------|----------|
| vim/vi/nano | 编辑文件 | `cat <文件>` 查看内容 |
| top/htop | 实时进程 | `top -bn1 \| head -20` |
| less/more | 分页查看 | `cat <文件>` 或 `head/tail` |
| mysql/psql | 数据库 | `mysql -e '查询语句'` |
| python/node | 交互式 | `python -c '代码'` |

## 📋 使用示例

### 1. 文件操作
```bash
/sys ls -la              # 详细列表
/sys cat README.md       # 查看文件
/sys head -20 log.txt    # 查看前20行
/sys tail -f app.log     # 查看最后几行
/sys grep "error" *.log  # 搜索错误
```

### 2. 目录管理
```bash
/sys pwd                 # 当前目录
/sys cd /var/log        # 切换目录
/sys cd ..              # 上级目录
/sys reset              # 重置到初始目录
```

### 3. 系统监控
```bash
/sys df -h              # 磁盘空间
/sys free -h            # 内存使用
/sys ps aux             # 进程列表
/sys netstat -antp      # 网络连接
/sys uptime             # 运行时间
```

### 4. 日志查看
```bash
/sys tail -100 /var/log/syslog
/sys grep "ERROR" /var/log/app.log
/sys journalctl -n 50
```

## ⚠️ 安全提示

1. **仅管理员可用** - 使用AstrBot核心权限系统
2. **群组限制** - 通过 `enabled_groups` 限制使用范围
3. **操作记录** - 所有命令都会记录日志便于审计
4. **无命令限制** - 可执行任意命令，请谨慎使用
5. **危险命令** - `rm -rf`、`del`、`format` 等会直接执行
6. **输出限制** - `-f` 参数可能导致大量输出
7. **私聊权限** - 即使配置了群组限制，管理员私聊仍可用

## 📝 操作日志

所有命令都会记录在AstrBot控制台：
```
[2024-01-01 12:00:00] [INFO] [操作日志] 用户:123456 | 命令:ls -la
```

## 🔍 常见问题

**Q: 如何限制插件只在某些群使用？**
- 配置 `enabled_groups`，填入允许的群号
- 留空则所有群都可用

**Q: 执行cd后目录没变化？**
- 插件会为每个用户保持独立的工作目录
- 使用 `/sys pwd` 确认当前目录

**Q: 输出被截断了？**
- 添加 `-f` 参数：`/sys cat file -f`
- 或使用管道限制：`/sys cat file | head -100`

**Q: 命令执行超时？**
- 某些命令可能需要较长时间
- 可在配置中增加 `command_timeout`

**Q: 如何查看命令历史？**
- 使用 `/sys history` 查看最近10条命令

## 📋 系统要求

- Python 3.8+
- AstrBot v4.5.0+
- psutil库（自动安装）

## 🛠️ 故障排除

1. **插件无法加载**
   - 检查Python版本 ≥ 3.8
   - 确认AstrBot版本 ≥ 4.5.0
   - 查看控制台错误信息

2. **命令无响应**
   - 确认用户是管理员
   - 检查群组是否在白名单
   - 查看是否超时

3. **输出异常**
   - 检查命令是否为交互式
   - 确认系统编码设置
   - 查看原始输出：加 `-f`

## 📄 许可证

MIT License

## 👨‍💻 作者

Sube

## 🔗 相关链接

- [AstrBot官方文档](https://github.com/Soulter/AstrBot)
- [插件开发指南](https://github.com/Soulter/AstrBot/wiki)

---

**安全提醒：** 本插件具有完整的系统命令执行权限，请确保只有可信任的管理员能够使用，并定期检查操作日志。