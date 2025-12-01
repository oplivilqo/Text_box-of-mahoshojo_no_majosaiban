@echo off
chcp 65001 >nul
cd /d "%~dp0\.."

REM 检测是否存在虚拟环境
if not exist ".venv" (
    echo 正在创建虚拟环境...

    REM 检测 uv 是否安装
    where uv >nul 2>nul
    if errorlevel 1 (
        echo uv 未安装，正在安装 uv...
        powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
        if errorlevel 1 (
            echo 错误：uv 安装失败。
            exit /b 2
        )
        echo uv 安装成功。
        echo 请重新运行此脚本，以刷新环境变量。
        exit /b 0
    ) else (
        echo uv 已安装。
    )

    REM 创建虚拟环境
    uv venv .venv
    if errorlevel 1 (
        echo 错误：虚拟环境创建失败。
        exit /b 2
    )
    echo 虚拟环境创建成功。

    REM 激活虚拟环境
    call .venv\Scripts\activate.bat
    echo 虚拟环境已激活。

    REM 安装依赖
    if exist "pyproject.toml" (
        echo 正在从 pyproject.toml 安装依赖...
        uv sync
    ) else if exist "requirements.txt" (
        echo 正在从 requirements.txt 安装依赖...
        uv pip install -r requirements.txt
    ) else (
        echo 错误：未找到任何依赖文件，请检查项目文件完整性。
        exit /b 2
    )
) else (
    echo 虚拟环境已存在，正在激活...
    call .venv\Scripts\activate.bat
    echo 虚拟环境已激活。
)

REM 启动项目
echo 正在启动项目...
echo.
uv run python src/tui.py