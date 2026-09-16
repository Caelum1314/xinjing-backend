@echo off
chcp 65001 > nul
title 心镜 - 一键安装
cd /d "%~dp0"
echo 正在安装依赖...
python -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
echo 安装完成！
pause
