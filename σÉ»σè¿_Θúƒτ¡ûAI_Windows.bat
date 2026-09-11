@echo off
chcp 65001 >nul
cd /d %~dp0
echo [食策AI V0.5.0-R1] 正在检查运行环境...
python -c "import fastapi,uvicorn,multipart" >nul 2>&1
if errorlevel 1 (
  echo 首次运行需要安装依赖，请保持网络可用。
  python -m pip install -r requirements.txt
  if errorlevel 1 (
    echo 依赖安装失败。请确认已安装 Python 3.10+
    pause
    exit /b 1
  )
)
echo 浏览器地址：http://127.0.0.1:8765
start "" cmd /c "timeout /t 2 /nobreak >nul & start http://127.0.0.1:8765"
python run.py
pause
