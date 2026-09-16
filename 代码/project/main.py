from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import router

app = FastAPI(
    title="心镜 · 多模态 AI 心理陪伴助手",
    description="基于 FastAPI + Uvicorn 的多模态情感计算后端服务，"
                "提供文本对话、图像情绪识别、语音转写、心理问卷与情感报告能力。",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)