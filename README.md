# 心镜 · 多模态 AI 心理陪伴助手（后端服务）

基于 **FastAPI + Uvicorn** 的多模态情感计算后端，接入 **OpenCV / DeepFace / Whisper**，
实现图像情绪识别、语音转写与文本对话，并提供心理问卷、成就系统与情感报告导出能力。

省级二等奖项目 · 原创作品

---

## 关于署名与二次使用

本项目为**省级二等奖获奖作品**，代码、文档与交互设计均为原创，开源目的仅为学习与技术交流。

依据 [MIT](LICENSE) 协议，你可以自由使用、复制、修改、合并、发布与分发本项目的代码，但**必须在所有副本或实质性片段中保留版权声明与许可声明**，并明确注明原作者与项目出处。

以下行为**不属于合理使用，明确禁止**：

- 将本项目整体或核心部分作为课程作业、课程设计、竞赛作品、毕业设计提交
- 删除、篡改版权声明后以本人名义发布或署名
- 在简历、面试或评奖中将其表述为本人独立开发成果

本项目自第一行代码起即通过 Git 提交历史留痕，全部 commit 时间戳、作者信息与变更内容均可公开核验，可作为原创归属的完整证据链。如发现上述行为，将保留追溯与公开说明的权利。

引用、转载或二次开发时，请保留如下署名：

```
心镜 · 多模态 AI 心理陪伴助手
作者：Caelum1314
仓库：https://github.com/Caelum1314/xinjing-backend
许可：MIT License
```

---

## 功能特性

- **文本对话**：接入智谱 GLM 大模型，支持流式输出、深度思考模式与联网检索
- **图像情绪识别**：OpenCV 解码图片 + DeepFace 识别 7 类情绪（开心 / 平静 / 惊讶 / 悲伤 / 恐惧 / 愤怒 / 厌恶）
- **情绪趋势分析**：基于最近 7 次情绪记录给出走势判断
- **语音转写**：Whisper 本地模型转写中文语音
- **文档分析**：上传 PDF / Word 提取文本并做内容分析
- **心理问卷**：题目生成、作答保存、统计与开放题文本分析
- **成就系统**：由对话、情绪、问卷行为触发成就解锁
- **情感报告**：导出中文 PDF / Word 报告
- **零数据库依赖**：数据以 JSON 文件落盘，拷贝目录即可运行

## 技术栈

| 层次 | 使用技术 |
| --- | --- |
| Web 框架 | FastAPI + Uvicorn |
| 图像情绪识别 | OpenCV + DeepFace |
| 语音转写 | OpenAI Whisper |
| 大模型 | 智谱 GLM（zhipuai SDK） |
| 数据处理 | NumPy / Pandas |
| 报告导出 | ReportLab / python-docx / PyPDF2 |
| 数据存储 | 本地 JSON 文件（无数据库） |
| 运行环境 | Python 3.11 · Windows 10/11 |

## 项目结构

```
xinjing-backend/
├── 代码/project/              # 后端服务（唯一入口：main.py）
│   ├── main.py                # FastAPI 应用入口，注册全部路由
│   ├── config.py              # 配置与常量（模型 Key、存储路径、情绪映射、成就定义）
│   ├── api/                   # 接口层，按业务模块拆分
│   │   ├── chat.py            # 文本对话
│   │   ├── emotion.py         # 图像情绪识别 / 情绪趋势
│   │   ├── speech.py          # 语音转写
│   │   ├── document.py        # 文档解析
│   │   ├── survey.py          # 心理问卷
│   │   ├── report.py          # 报告生成与导出
│   │   ├── history.py         # 历史记录
│   │   └── achievement.py     # 成就系统
│   ├── services/              # 业务服务层，封装各模型调用
│   ├── utils/                 # 存储读写与对话上下文工具
│   ├── models/                # Pydantic 数据模型
│   └── requirements.txt
├── index.html                 # 前端页面（单文件，无需构建）
├── requirements.txt           # 统一依赖清单
├── 一键安装.bat               # 安装依赖
├── 启动后端.bat               # 启动后端服务
├── 启动前端.bat               # 启动前端页面
├── 停止服务.bat               # 停止全部服务
└── 使用说明.txt
```

## 快速开始

环境要求：Windows 10/11，Python 3.11

**1. 安装依赖**

双击 `一键安装.bat`，或手动执行：

```bash
pip install -r requirements.txt
```

**2. 启动后端**

双击 `启动后端.bat`，或手动执行：

```bash
cd 代码/project
python main.py
```

服务默认监听 `0.0.0.0:8000`，启动后接口文档地址：<http://localhost:8000/docs>

**3. 启动前端**

双击 `启动前端.bat`，浏览器会自动打开 <http://localhost:8080>

**停止服务**：双击 `停止服务.bat`

> **关于前后端地址**：前端会自动识别后端地址（当前页面主机名 + 8000 端口），
> 因此本机访问、局域网其它设备访问都无需改代码。
> 如需指定其它后端地址，在网址后加参数即可：`http://localhost:8080/?api=192.168.1.10`

## 接口列表

共 **17 个**接口，按 8 个业务模块划分：

| 模块 | 方法 | 路径 | 功能 |
| --- | --- | --- | --- |
| chat | POST | `/chat` | 文本对话（流式，支持深度思考 / 联网检索） |
| chat | POST | `/clear_history` | 清空指定用户的对话上下文 |
| emotion | POST | `/analyze` | 上传图片识别 7 类情绪 |
| emotion | POST | `/record_emotion` | 手动记录一次情绪 |
| emotion | GET | `/emotion_trend` | 最近 7 次情绪走势判断 |
| speech | POST | `/speech_to_text` | 语音文件转写为文本 |
| document | POST | `/analyze_document` | 解析 PDF / Word 并做内容分析 |
| survey | POST | `/generate_survey` | 生成心理问卷题目 |
| survey | POST | `/save_survey` | 保存问卷作答 |
| survey | GET | `/get_survey_data` | 获取问卷数据 |
| survey | GET | `/get_statistics` | 问卷统计结果 |
| survey | POST | `/analyze_survey_text` | 开放题作答文本分析 |
| report | POST | `/generate_report` | 生成情感报告 |
| report | GET | `/export_report` | 导出报告文件 |
| history | GET | `/get_chat_history` | 获取聊天历史 |
| history | POST | `/clear_chat_history` | 清空聊天历史 |
| achievement | GET | `/get_achievements` | 获取已解锁成就与统计数据 |

启动服务后可在 <http://localhost:8000/docs> 交互式调试全部接口。

## 技术难点与处理

- **模型加载开销大**：Whisper 权重加载慢且占内存。改为**首次调用语音接口时才加载**，
  之后以模块级单例复用，避免服务启动被拖慢、也避免每次请求重复初始化。

- **流式对话响应**：对话接口使用 `StreamingResponse` 逐块返回，前端边接收边渲染；
  并按普通 / 深度思考两种模式动态调整 `max_tokens` 与 `temperature`。
  联网检索时把命中的搜索结果一并回传，前端可直接展示。

- **分层解耦**：接口层（`api/`）只负责参数校验与响应组装，模型调用收敛到 `services/`，
  存储收敛到 `utils/storage.py`。新增接口只需加一个模块文件，不改动既有代码。

- **稳健性**：图片解析失败、模型异常、大模型调用异常均做了兜底返回，
  单个接口出错不会导致整个服务不可用。

- **零数据库依赖**：使用 JSON 文件持久化，并对历史记录做长度截断（聊天 200 条 / 情绪 500 条），
  换机器只需拷贝整个目录即可运行。

## 说明

- 前端为单文件 `index.html`，依赖 Chart.js CDN，无需 npm 与构建步骤。
- 运行期数据生成在 `代码/project/data/`，该目录已加入 `.gitignore`，不会被提交。

## License

本项目采用 [MIT](LICENSE) 协议开源，Copyright (c) 2026 Caelum。

你可以自由使用本项目，但请遵守协议中的**署名要求**，
并尊重上方「关于署名与二次使用」中的约定。
