@echo off
chcp 65001 > nul
title 心镜 - 后端服务
cd /d "%~dp0代码\project"
echo 后端服务启动中，接口文档： http://localhost:8000/docs
python main.py
pause
