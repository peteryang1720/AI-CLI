# ai_agent/executors/tmux_auto_executor.py
import subprocess
import time
import sys


def _needs_sudo(commands):
    """检查是否需要 sudo"""
    for cmd in commands:
        stripped = cmd.strip()
        if not stripped:
            continue
        if stripped.startswith("sudo "):
            return True
        if any(pkg_cmd in stripped for pkg_cmd in [" apt ", " apt-get ", " dpkg ", " systemctl "]):
            return True
    return False


class TmuxAutoExecutor:
    def __init__(self, session_name="ai-cli"):
        self.session_name = session_name

    def run_commands(self, commands, description=""):
        if not commands:
            print("⚠️ 无命令可执行", file=sys.stderr)
            return

        session = self.session_name

        # 清理旧会话
        subprocess.run(
            ["tmux", "kill-session", "-t", session],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        try:
            subprocess.run(
                ["tmux", "new-session", "-d", "-s", session, "bash"],
                check=True
            )
        except subprocess.CalledProcessError:
            print("❌ 无法创建 tmux 会话，请安装 tmux：sudo apt install -y tmux", file=sys.stderr)
            sys.exit(1)

        time.sleep(0.2)

        script = []
        script.append(r'printf "\e[?10l\e[?11l\e[?12l"')
        script.append('stty sane')
        script.append('echo "🚀 AI 自动化任务启动"')
        script.append(f'echo "描述: {description}"')
        script.append('echo "-----------------------------"')

        if _needs_sudo(commands):
            script.append('sudo -v')
            script.append('echo "[🔑 提权成功]"')

        for i, cmd in enumerate(commands, 1):
            script.append(f'echo "[{i}/{len(commands)}] 执行: {cmd}"')
            script.append(cmd)

        script.append('echo ""')
        script.append('echo "✅ 所有命令执行完毕！"')
        script.append('while read -r -t 0.01 -N 1000000 _; do :; done 2>/dev/null')
        script.append('echo -n "👉 按任意键退出..."')
        script.append('dd bs=1 count=1 2>/dev/null')
        script.append('echo ""')
        script.append(f'tmux kill-session -t {session} 2>/dev/null || true')

        full_script = "\n".join(script)
        escaped = full_script.replace("'", "'\"'\"'")
        cmd_to_send = f"bash -c $'{escaped}'"

        subprocess.run(["tmux", "send-keys", "-t", session, cmd_to_send, "Enter"])
        time.sleep(0.3)

        try:
            subprocess.run(["tmux", "attach", "-t", session])
        except KeyboardInterrupt:
            print("\n⚠️ 用户中断", file=sys.stderr)
        finally:
            subprocess.run(
                ["tmux", "kill-session", "-t", session],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
