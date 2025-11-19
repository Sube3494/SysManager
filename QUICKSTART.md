# 🚀 快速开始

## 第一步：安装依赖

```bash
pip install psutil
```

## 第二步：配置管理员

发送QQ消息：
```bash
/sid        # 查看你的用户ID
/op 你的ID  # 让现有管理员执行此命令
```

## 第三步：（可选）自定义命令前缀

在Web面板 → 插件管理 → 服务器管理 → 配置中，可以修改命令前缀：

```
command_prefix: cmd     # 改为 /cmd
command_prefix: sh      # 改为 /sh
command_prefix: exec    # 改为 /exec
```

**默认前缀是 `sys`**，如不修改可跳过此步骤。

## 第四步：开始使用

重启AstrBot后，根据你的系统发送命令：

### 如果是 Linux/macOS

```bash
/sys ls -la
/sys df -h
/sys free -h
```

### 如果是 Windows

```bash
/sys dir
/sys ipconfig
/sys systeminfo
```

如果收到结果，说明配置成功！

## 📝 常用命令速查（带智能优化✨）

### Linux/macOS

```bash
/sys df -h               # 💾 磁盘使用（带颜色告警）
/sys free -h             # 💾 内存使用（格式美化）
/sys ps aux              # 🔄 进程列表（前10条）
/sys ls -la              # 📁 文件列表（带图标）
/sys netstat -an         # 🌐 网络连接（统计状态）
/sys uptime              # ⏱️ 运行时间
/sys cat /var/log/syslog | tail -20  # 查看日志
```

### Windows

```bash
/sys dir                 # 📁 查看文件（带统计）
/sys dir /s              # 递归查看
/sys ipconfig            # 网络配置
/sys ipconfig /all       # 详细信息
/sys systeminfo          # 💻 系统信息（提取关键信息）
/sys tasklist            # 进程列表
/sys netstat -an         # 🌐 网络连接（统计状态）
```

### 跨平台通用

```bash
/sys python --version    # Python版本
/sys git status          # Git状态
/sys node --version      # Node版本
/sys npm list            # NPM包
```

## 💡 提示

- 📝 所有命令都会被记录
- ⏱️ 命令超过30秒会超时
- 📏 输出超过2000字符会截断
- 🔐 仅管理员可使用
- 🖥️ Windows和Linux命令不同，注意区分
- 🔧 可在配置中自定义命令前缀
- 🔄 修改配置后需重启插件

## ⚠️ 注意事项

1. **Windows 用户**
   - 使用 `dir` 而不是 `ls`
   - 使用 `ipconfig` 而不是 `ifconfig`
   - 使用 `tasklist` 而不是 `ps`

2. **Linux 用户**
   - 确保命令已安装
   - 某些命令需要 sudo 权限
   - 管道命令正常工作

3. **所有用户**
   - 危险命令会直接执行（rm、del、format等）
   - 建议先在本地测试命令
   - 定期查看操作日志

---

**就是这么简单！跨平台支持！** 🎉🌍
