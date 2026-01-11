# 🤖 AI-CLI 使用与部署指南

`ai-cli` 是一个基于大模型的智能命令行助手，能将自然语言（如“查看本机IP”）自动转换为可执行的 Shell 命令，并在安全沙箱中运行。无需记忆复杂命令，让终端操作更高效、更直观。

---

## ✨ 核心特性

- **自然语言驱动**：输入中文或英文描述，AI 自动生成对应命令  
  例如：`ai-cli "列出最近修改的5个文件"` → 自动执行 `ls -lt | head -6`
- **安全防护**：内置高危命令过滤（如 `rm -rf /`、`mkfs` 等）
- **交互确认**：执行前显示计划，需用户确认
- **可视化反馈**：在 tmux 会话中清晰展示执行过程和结果
- **全局可用**：安装后可在任意目录使用 `ai-cli` 命令

---

## 🚀 快速开始

### 前提条件

- Linux 系统（Ubuntu/Debian/CentOS 等）
- Python ≥ 3.8
- `tmux` 工具（用于会话管理）
- 阿里云 DashScope API Key（免费额度足够日常使用）

> 💡 获取 API Key：[阿里云 DashScope 控制台](https://dashscope.console.aliyun.com/apiKey)

---

## 🔧 部署到系统（全局安装）

> 以下步骤将 `ai-cli` 安装为系统级命令，无需激活虚拟环境。

### 步骤 1：安装系统依赖

```bash
# 安装 tmux 和 pipx（推荐方式）
sudo apt update
sudo apt install -y tmux pipx python3-full
```

### 步骤 2：配置 pipx（一次性）

```bash
# 将 pipx 加入 PATH
pipx ensurepath

# 重新加载 shell 配置
source ~/.bashrc
```

### 步骤 3：下载并安装 ai-cli

```bash
# 克隆项目（若尚未下载）
git clone https://github.com/yourname/ai-cli-local.git ~/ai-cli-local

# 进入项目目录
cd ~/ai-cli-local

# 删除可能存在的虚拟环境（避免干扰）
rm -rf myenv/

# 创建配置文件
cat > .env << EOF
ALIYUN_DASHSCOPE_API_KEY=你的_api_key_here
EOF

# 创建构建配置（pyproject.toml）
cat > pyproject.toml << 'EOF'
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "ai-cli"
version = "0.1.0"
description = "AI-powered CLI assistant"
dependencies = ["python-dotenv", "dashscope"]
requires-python = ">=3.8"

[project.scripts]
ai-cli = "cli.__main__:main"

[tool.setuptools.packages.find]
include = ["cli*", "ai_agent*"]
EOF

# 全局安装（可编辑模式）
pipx install -e .
```

✅ 安装成功后，你将看到：
```
installed package ai-cli 0.1.0, installed using Python 3.13.3
These apps are now globally available
  - ai-cli
```

---

## 🖥️ 使用方法

### 基本语法

```bash
ai-cli "<自然语言任务描述>"
```

### 示例命令

| 描述 | 实际执行命令 |
|------|-------------|
| `ai-cli "查看本机IP地址"` | `ip a` |
| `ai-cli "列出当前目录所有文件"` | `ls -la` |
| `ai-cli "显示磁盘使用情况"` | `df -h` |
| `ai-cli "创建 backup 目录"` | `mkdir -p backup` |
| `ai-cli "今天是几号？"` | `date` |

### 执行流程

1. 输入 `ai-cli "查看本机IP"`
2. AI 分析语义，生成安全命令（如 `ip a`）
3. 进入 tmux 会话，显示执行计划
4. 自动运行命令并输出结果
5. 显示 `👉 按任意键退出...`
6. 按任意键返回主终端

> ⚠️ **安全提示**：所有命令均需要经过用户许可。

---

## 🛠️ 故障排查

### 常见问题

#### Q1: `ai-cli：未找到命令`
**原因**：`pipx` 的 bin 目录未加入 PATH  
**解决**：
```bash
pipx ensurepath
source ~/.bashrc
```

#### Q2: 报错 `ALIYUN_DASHSCOPE_API_KEY not found`
**原因**：缺少 `.env` 配置文件  
**解决**：
```bash
echo "ALIYUN_DASHSCOPE_API_KEY=你的实际key" > ~/ai-cli-local/.env
```

#### Q3: 执行后直接 `[exited]`，看不到结果
**原因**：tmux 未正确 attach 或命令执行过快  
**解决**：
- 确保已安装 `tmux`：`sudo apt install -y tmux`
- 检查 `.env` 中 API Key 是否有效

---

## 📦 目录结构说明

```
ai-cli-local/
├── cli/                  # 主入口模块
│   └── __main__.py       # 命令行接口
├── ai_agent/             # AI 核心逻辑
│   ├── agent.py          # 命令生成器
│   ├── safety.py         # 安全过滤器
│   └── executors/        # 执行器（tmux）
├── .env                  # API 密钥配置（必须）
├── pyproject.toml        # 构建配置（用于 pipx 安装）
└── README.md             # 本指南
```

> 🔒 **安全建议**：`.env` 文件包含敏感信息，请勿提交到 Git！

---

## 🔄 更新与卸载

### 更新项目

```bash
cd ~/ai-cli-local
git pull                    # 拉取最新代码
pipx reinstall ai-cli       # 重新安装
```

### 卸载

```bash
pipx uninstall ai-cli
rm -rf ~/ai-cli-local       # 可选：删除源码
```

---

## 📜 许可证

MIT License - 免费用于个人和商业用途。

---

> 🎉 现在，你可以像这样轻松操作终端：  
> ```bash
> ai-cli "帮我压缩这个文件夹"
> ai-cli "查找占用端口8080的进程"
> ai-cli "生成一个随机密码"
> ```  
> 让 AI 成为你的终端副驾驶！
