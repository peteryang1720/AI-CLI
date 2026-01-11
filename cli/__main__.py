# cli/__main__.py
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_agent.agent import AIAgent
from ai_agent.executors.tmux_auto_executor import TmuxAutoExecutor
from ai_agent.safety import is_dangerous_command


def main():
    agent = AIAgent()

    # 自动模式：通过命令行参数触发
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
        print(f"🤖 AI-CLI (自动模式): {user_input}")

        try:
            commands = agent.generate_shell_commands(user_input)
            if not commands:
                print("⚠️ 无有效命令生成", file=sys.stderr)
                return

            # 检查危险命令
            dangerous_cmds = [cmd for cmd in commands if is_dangerous_command(cmd)]
            has_danger = len(dangerous_cmds) > 0

            print("\n[💡 AI Agent 计划]: 执行以下操作\n")
            for i, cmd in enumerate(commands, 1):
                warn_mark = " ⚠️ [DANGEROUS]" if is_dangerous_command(cmd) else ""
                print(f" {i}. {cmd}{warn_mark}")

            if has_danger:
                print("\n" + "=" * 60)
                print("🚨 警告：检测到高危操作！")
                print("   这些命令可能导致数据丢失或系统损坏！")
                print("   请仔细核对每一条命令！")
                print("=" * 60)

            confirm = input("\n✅ 确认执行？ [y/N]: ").strip().lower()
            if confirm != 'y':
                print("❌ 已取消执行。\n")
                return

            if has_danger:
                final_confirm = input(
                    "\n🛑 为防止误操作，请输入完整确认语句: "
                    "'I UNDERSTAND THE RISK'（不含引号）\n> "
                ).strip()
                if final_confirm != "I UNDERSTAND THE RISK":
                    print("❌ 高危操作未获充分授权，已中止。")
                    return

            executor = TmuxAutoExecutor(session_name="ai-cli")
            executor.run_commands(commands, description=user_input)

        except Exception as e:
            print(f"❌ 错误: {e}", file=sys.stderr)
            sys.exit(1)
        return

    # 交互模式
    print("🤖 AI-CLI (交互模式)")
    print("提示：你也可以直接运行 `ai-cli \"任务描述\"` 进入自动模式\n")
    while True:
        try:
            user_input = input("🤖 AI-CLI> ").strip()
            if not user_input:
                continue
            if user_input.lower() in ('exit', 'quit', 'q'):
                print("👋 再见！")
                break

            commands = agent.generate_shell_commands(user_input)
            if not commands:
                print("⚠️ 无有效命令生成\n")
                continue

            dangerous_cmds = [cmd for cmd in commands if is_dangerous_command(cmd)]
            has_danger = len(dangerous_cmds) > 0

            print("\n[💡 AI Agent 计划]: 执行以下操作\n")
            for i, cmd in enumerate(commands, 1):
                warn_mark = " ⚠️ [DANGEROUS]" if is_dangerous_command(cmd) else ""
                print(f" {i}. {cmd}{warn_mark}")

            if has_danger:
                print("\n" + "=" * 60)
                print("🚨 警告：检测到高危操作！")
                print("   这些命令可能导致数据丢失或系统损坏！")
                print("   请仔细核对每一条命令！")
                print("=" * 60)

            confirm = input("\n✅ 确认执行？ [y/N]: ").strip().lower()
            if confirm == 'y':
                if has_danger:
                    final_confirm = input(
                        "\n🛑 为防止误操作，请输入完整确认语句: "
                        "'I UNDERSTAND THE RISK'（不含引号）\n> "
                    ).strip()
                    if final_confirm != "I UNDERSTAND THE RISK":
                        print("❌ 高危操作未获充分授权，已中止。\n")
                        continue

                executor = TmuxAutoExecutor(session_name="ai-cli")
                executor.run_commands(commands, description=user_input)
            else:
                print("❌ 已取消执行。\n")

        except KeyboardInterrupt:
            print("\n\n👋 再见！")
            break
        except Exception as e:
            print(f"❌ 错误: {e}\n")


if __name__ == "__main__":
    main()
