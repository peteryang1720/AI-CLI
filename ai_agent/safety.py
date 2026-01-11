# ai_agent/safety.py
import re

DANGEROUS_PATTERNS = [
    r'\brm\s+-rf\s+/',          # rm -rf /
    r'\brm\s+-fr\s+/',          # rm -fr /
    r'\bdd\s+if=/',             # dd if=/dev/zero of=...
    r'\bmkfs',                  # 格式化文件系统
    r'\b:\(\)\{\s*:\|\:\&\;\s*\};:',  # fork bomb
    r'chmod\s+777\s+/',
    r'chown\s+.*\s+/',
    r'iptables\s+.*-F',
    r'systemctl\s+(halt|poweroff|reboot)',
    r':\(\)\{\s*:\|\:\&\s*\};\s*:\s*&',  # 另一种 fork bomb
]

def is_dangerous_command(cmd: str) -> bool:
    """判断命令是否属于高危操作（不抛异常，仅返回布尔值）"""
    cmd = cmd.strip()
    if not cmd or cmd.startswith('#') or cmd == 'exit':
        return False
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, cmd, re.IGNORECASE):
            return True
    return False
