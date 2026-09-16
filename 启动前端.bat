@echo off
chcp 65001 > nul
title 心镜 - 前端服务
cd /d "%~dp0"
echo 前端地址： http://localhost:8080
start "" cmd /c "timeout /t 2 >nul & start http://localhost:8080"
python -m http.server 8080
pause
