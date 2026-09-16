@echo off
chcp 65001 > nul
title 心镜 - 一键安装
echo 正在安装依赖...
pip install fastapi uvicorn opencv-python deepface tensorflow tf-keras zhipuai numpy pandas reportlab python-docx python-multipart openai-whisper PyPDF2 -i https://pypi.tuna.tsinghua.edu.cn/simple
echo 安装完成！
pause
