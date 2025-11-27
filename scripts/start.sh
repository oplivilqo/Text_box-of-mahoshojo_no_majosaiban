cd "$(dirname "$0")/.." || exit 2

# 检测是否存在虚拟环境
if [ ! -d ".venv" ]; then
    echo "正在创建虚拟环境..."
    # 检测 uv 是否安装
    if ! command -v uv &> /dev/null
    then
        echo "uv 未安装，正在安装 uv..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
    else
        echo "uv 已安装。"
        exit 0
    fi

    # 创建虚拟环境
    uv venv create .venv
    echo "虚拟环境创建成功。"

    # 激活虚拟环境
    source .venv/bin/activate
    echo "虚拟环境已激活。"

    # 安装依赖
    if [ -f "pyproject.toml" ]; then
        echo "正在从 pyproject.toml 安装依赖..."
        uv sync
    elif [ -f "requirements.txt" ]; then
        echo "正在从 requirements.txt 安装依赖..."
        uv pip install -r requirements.txt
    else
        echo "错误：未找到任何依赖文件，请检查项目文件完整性。"
        exit 2
    fi

else
    echo "虚拟环境已存在，正在激活..."
    source .venv/bin/activate
    echo "虚拟环境已激活。"
fi

# 启动项目
echo "正在启动项目..."
echo
uv run python src/main.py
