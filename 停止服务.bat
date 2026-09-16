@echo off
chcp 65001 > nul
title 心镜 - 停止服务
taskkill /f /im python.exe > nul 2>&1
echo 服务已停止
pause
