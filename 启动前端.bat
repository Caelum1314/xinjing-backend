@echo off
chcp 65001 > nul
title 心镜 - 前端服务
start http://localhost:8080
python -m http.server 8080
pause
