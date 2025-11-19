# 🚀 快速开始

## 安装

```bash
pip install psutil
```

## 配置管理员

```bash
/sid        # 查看你的ID
/op 你的ID  # 授权为管理员
```

## 开始使用

```bash
/sys ls           # Linux/macOS
/sys dir          # Windows
```

## 常用命令

```bash
# 目录操作
/sys pwd          # 当前目录
/sys cd /tmp      # 切换目录
/sys ls           # 列出文件

# 系统信息
/sys df -h        # 磁盘
/sys free -h      # 内存
/sys ps aux       # 进程

# 查看文件
/sys cat file.txt
/sys tail -100 log.txt
/sys grep "error" log.txt

# 网络
/sys netstat -an
/sys ping baidu.com -c 4

# 历史和帮助
/sys history      # 查看历史
/sys              # 显示帮助
```

## 特殊参数

```bash
/sys cat large.txt -f    # 强制全部输出
```

## 注意事项

- ✅ 支持 cd 目录切换
- ✅ 每个用户独立会话
- ✅ 自动拦截 vim、top 等交互式命令
- ✅ 智能优化常用命令输出
- 📝 所有命令会被记录

---

**就这么简单！** 🎉
