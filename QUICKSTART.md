# 🚀 快速开始

## 1️⃣ 安装插件

在AstrBot Web面板：
- 插件管理 → 插件商店 → 搜索 "SysManager" → 安装

## 2️⃣ 配置权限

### 选项A：所有群可用（默认）
```json
{
  "enabled_groups": []
}
```

### 选项B：限制特定群
```json
{
  "enabled_groups": [123456789]  // 填入群号
}
```

**获取群号：** 在群里发送 `/sid`

## 3️⃣ 基本使用

```bash
/sys ls                 # 查看文件
/sys pwd                # 当前目录
/sys cd /var/log       # 切换目录
/sys cat file.txt      # 查看文件内容
/sys df -h             # 磁盘使用
/sys ps aux            # 进程列表
```

## 4️⃣ 特殊功能

### 查看历史
```bash
/sys history
```

### 重置目录
```bash
/sys reset
```

### 强制全部输出
```bash
/sys cat large.txt -f
```

## ⚠️ 注意事项

- ✅ 仅管理员可用
- ✅ 每个用户独立的工作目录
- ✅ 所有命令会记录日志
- ❌ 不支持交互式命令（vim、top等）
- ⚠️ 谨慎使用危险命令（rm -rf等）

---

**完成！开始使用 `/sys` 命令吧！** 🎉