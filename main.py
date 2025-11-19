from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.event.filter import PermissionType
import subprocess
import platform
import os
import re
from datetime import datetime

@register("sysmanager", "Sube", "通过QQ消息远程执行服务器命令(支持Windows/Linux/macOS)", "1.0.0")
class ServerManager(Star):
    def __init__(self, context: Context, config: dict | None = None):
        super().__init__(context, config)
        self.config = config or {}
        self.command_timeout: int = 30
        self.max_output_length: int = 2000
        self.log_operations: bool = True
        self.user_cwd: dict = {}  # 记录每个用户的当前工作目录
        
    async def initialize(self):
        """初始化插件，加载配置"""
        try:
            self.command_timeout = self.config.get("command_timeout", 30)
            self.max_output_length = self.config.get("max_output_length", 2000)
            self.log_operations = self.config.get("log_operations", True)
            
            astrbot_admins = self.context.get_config().get("admins_id", [])
            
            logger.info(f"✅ 服务器管理插件已加载")
            logger.info(f"   管理员数量: {len(astrbot_admins)}")
            logger.info(f"   命令前缀: /sys (固定)")
            logger.info(f"   命令超时: {self.command_timeout}秒")
            logger.info(f"   最大输出: {self.max_output_length}字符")
        except Exception as e:
            logger.error(f"❌ 插件初始化失败: {e}")
    
    def _log_operation(self, user_id: str, cmd: str):
        """记录操作日志"""
        if self.log_operations:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"[操作日志] {timestamp} | 用户:{user_id} | 命令:{cmd}")

    @filter.permission_type(PermissionType.ADMIN)
    @filter.command("sys")
    async def execute_command(self, event: AstrMessageEvent):
        """执行系统命令 - 用法: /sys <命令>"""
        user_id = str(event.get_sender_id())
        
        # 获取命令内容（去掉 "sys" 前缀）
        cmd = event.message_str.strip()
        if cmd.lower().startswith("sys"):
            cmd = cmd[3:].strip()
        
        if not cmd:
            # 显示当前工作目录
            current_cwd = self.user_cwd.get(user_id, os.getcwd())
            yield event.plain_result(
                f"当前目录: {current_cwd}\n\n"
                f"用法: /sys <命令> [-f]\n"
                f"  -f: 强制输出全部内容(跳过长度限制)\n\n"
                f"示例:\n"
                f"  /sys ls\n"
                f"  /sys cd /var/log\n"
                f"  /sys cat large.txt -f"
            )
            return
        
        # 检查是否强制全部输出（-f 参数）
        force_full_output = False
        if cmd.endswith(" -f") or cmd.endswith(" --full"):
            force_full_output = True
            cmd = cmd.replace(" -f", "").replace(" --full", "").strip()
        
        # 记录日志
        self._log_operation(user_id, cmd)
        
        # 处理 cd 命令（特殊处理）
        if cmd.strip().lower().startswith("cd ") or cmd.strip().lower() == "cd":
            result_msg = self._handle_cd_command(user_id, cmd)
            yield event.plain_result(result_msg)
            return
        
        # 获取用户的当前工作目录
        cwd = self.user_cwd.get(user_id, None)
        
        # 执行命令
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=self.command_timeout,
                cwd=cwd  # 使用记录的工作目录
            )
            
            # 获取输出
            output = result.stdout if result.stdout else result.stderr
            
            if not output:
                output = "(无输出)"
            else:
                # 智能优化输出
                output = self._optimize_output(cmd, output, result.returncode)
            
            # 限制输出长度（除非使用了 -f 强制全部输出）
            original_length = len(output)
            if not force_full_output and len(output) > self.max_output_length:
                output = output[:self.max_output_length] + f"\n\n(已截断，完整{original_length}字符，使用 -f 强制全部输出)"
            
            # 添加返回码信息
            if result.returncode != 0:
                output = f"[返回码: {result.returncode}]\n{output}"
            
            yield event.plain_result(output)
            
        except subprocess.TimeoutExpired:
            yield event.plain_result(f"超时(>{self.command_timeout}s)")
        except Exception as e:
            logger.error(f"命令执行失败: {e}")
            yield event.plain_result(f"错误: {str(e)}")

    def _handle_cd_command(self, user_id: str, cmd: str) -> str:
        """处理 cd 命令"""
        # 提取目标路径
        parts = cmd.strip().split(maxsplit=1)
        if len(parts) < 2:
            # 只有 cd，切换到用户主目录
            if platform.system() == "Windows":
                target_path = os.path.expanduser("~")
            else:
                target_path = os.path.expanduser("~")
        else:
            target_path = parts[1].strip()
        
        # 获取当前工作目录
        current_cwd = self.user_cwd.get(user_id, os.getcwd())
        
        # 处理相对路径
        if not os.path.isabs(target_path):
            target_path = os.path.join(current_cwd, target_path)
        
        # 规范化路径
        target_path = os.path.normpath(target_path)
        
        # 检查目标路径是否存在
        if os.path.exists(target_path) and os.path.isdir(target_path):
            self.user_cwd[user_id] = target_path
            return f"切换到: {target_path}"
        else:
            return f"目录不存在: {target_path}"
    
    def _optimize_output(self, cmd: str, output: str, returncode: int) -> str:
        """智能优化命令输出"""
        cmd_lower = cmd.lower().strip()
        
        # 提取命令主体（去掉参数）
        cmd_base = cmd_lower.split()[0] if cmd_lower else ""
        
        # df -h: 磁盘使用情况
        if cmd_base in ["df"] and "-h" in cmd_lower:
            return self._format_disk_usage(output)
        
        # free -h: 内存使用情况
        elif cmd_base in ["free"] and "-h" in cmd_lower:
            return self._format_memory_usage(output)
        
        # ps aux: 进程列表
        elif cmd_base == "ps" and "aux" in cmd_lower:
            return self._format_process_list(output)
        
        # ls -la: 文件列表
        elif cmd_base in ["ls", "dir"]:
            return self._format_file_list(output, cmd_base)
        
        # netstat: 网络连接
        elif cmd_base in ["netstat", "ss"]:
            return self._format_network_status(output)
        
        # systeminfo: Windows系统信息
        elif cmd_base == "systeminfo":
            return self._format_systeminfo(output)
        
        # uptime: 运行时间
        elif cmd_base == "uptime":
            return self._format_uptime(output)
        
        # 默认：基础优化（去除多余空行）
        return self._basic_optimize(output)
    
    def _format_disk_usage(self, output: str) -> str:
        """格式化磁盘使用情况"""
        lines = output.strip().split('\n')
        if len(lines) < 2:
            return output
        
        result = "磁盘使用:\n"
        
        for i, line in enumerate(lines):
            if i == 0:  # 标题行
                continue
            
            parts = line.split()
            if len(parts) >= 5:
                use_percent = parts[4] if len(parts) > 4 else "N/A"
                mount = parts[-1]
                size = parts[1]
                used = parts[2]
                avail = parts[3]
                
                result += f"{mount}: {use_percent} ({used}/{size}, 剩余{avail})\n"
        
        return result.strip()
    
    def _format_memory_usage(self, output: str) -> str:
        """格式化内存使用情况"""
        lines = output.strip().split('\n')
        
        result = "内存:\n"
        
        for line in lines:
            if 'Mem:' in line:
                parts = line.split()
                if len(parts) >= 7:
                    total = parts[1]
                    used = parts[2]
                    available = parts[6] if len(parts) > 6 else "N/A"
                    
                    result += f"总量: {total}, 已用: {used}, 可用: {available}\n"
            elif 'Swap:' in line:
                parts = line.split()
                if len(parts) >= 4:
                    total = parts[1]
                    used = parts[2]
                    result += f"交换: {total} (已用: {used})\n"
        
        return result.strip()
    
    def _format_process_list(self, output: str) -> str:
        """格式化进程列表（只显示前10个）"""
        lines = output.strip().split('\n')
        
        result = "进程 (前10条):\n"
        
        count = 0
        for i, line in enumerate(lines):
            if i == 0:  # 跳过标题
                continue
            if count >= 10:
                result += f"... 还有 {len(lines) - 11} 个进程"
                break
            
            parts = line.split(None, 10)
            if len(parts) >= 11:
                cpu = parts[2]
                mem = parts[3]
                command = parts[10][:40]
                
                result += f"{command} (CPU:{cpu}% MEM:{mem}%)\n"
                count += 1
        
        return result.strip()
    
    def _format_file_list(self, output: str, cmd: str) -> str:
        """格式化文件列表"""
        # 直接返回原始输出，简洁
        return output.strip()
    
    def _format_network_status(self, output: str) -> str:
        """格式化网络连接状态"""
        lines = output.strip().split('\n')
        
        # 统计连接状态
        status_count = {}
        for line in lines:
            if 'ESTABLISHED' in line:
                status_count['ESTABLISHED'] = status_count.get('ESTABLISHED', 0) + 1
            elif 'LISTEN' in line:
                status_count['LISTEN'] = status_count.get('LISTEN', 0) + 1
            elif 'TIME_WAIT' in line:
                status_count['TIME_WAIT'] = status_count.get('TIME_WAIT', 0) + 1
        
        result = "连接统计:\n"
        for status, count in sorted(status_count.items(), key=lambda x: x[1], reverse=True):
            result += f"{status}: {count}\n"
        
        result += f"总计: {len(lines) - 1}\n"
        
        # 只显示前10条
        result += "\n前10条:\n"
        for i, line in enumerate(lines[:11]):
            if i > 0:
                result += f"{line}\n"
        
        return result.strip()
    
    def _format_systeminfo(self, output: str) -> str:
        """格式化Windows系统信息"""
        lines = output.strip().split('\n')
        
        result = "系统信息:\n"
        
        # 提取关键信息
        keywords = ['OS 名称', '系统类型', '处理器', '物理内存总量', '可用的物理内存', '系统启动时间']
        
        for line in lines:
            for keyword in keywords:
                if keyword in line:
                    result += f"{line.strip()}\n"
                    break
        
        return result.strip()
    
    def _format_uptime(self, output: str) -> str:
        """格式化系统运行时间"""
        return output.strip()
    
    def _basic_optimize(self, output: str) -> str:
        """基础优化：去除多余空行，整理格式"""
        # 去除多余的连续空行
        lines = output.split('\n')
        optimized_lines = []
        prev_empty = False
        
        for line in lines:
            is_empty = not line.strip()
            if is_empty and prev_empty:
                continue
            optimized_lines.append(line)
            prev_empty = is_empty
        
        return '\n'.join(optimized_lines).strip()

    async def terminate(self):
        """插件销毁"""
        logger.info("服务器管理插件已卸载")
