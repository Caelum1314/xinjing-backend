"""冒烟测试：验证 FastAPI 应用能否成功装配、全部路由是否已注册。

设计说明
--------
本项目依赖 tensorflow / deepface / openai-whisper 等重量级包，完整安装需要数 GB
且耗时很长。为了让 CI 能在 1 分钟内跑完，这里用桩模块（stub）替换这些重依赖，
只验证「应用能不能装配起来、接口有没有全部注册」这一件事。

本地运行：
    pip install fastapi uvicorn python-multipart
    python tests/smoke_test.py
"""

import importlib.abc
import importlib.machinery
import os
import sys
import types

from unittest.mock import MagicMock

# 后端项目目录（仓库根目录下的 代码/project）
PROJECT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "代码", "project")
)

# 需要用桩模块替代的重依赖（仅替换这些，其余模块走真实导入）
STUB_TOP_LEVEL = {
    "zhipuai",      # 智谱 GLM SDK
    "cv2",          # OpenCV
    "deepface",     # 情绪识别
    "tensorflow",   # DeepFace 依赖
    "tf_keras",
    "keras",
    "whisper",      # 语音转写
    "reportlab",    # 报告导出
    "docx",
    "PyPDF2",
    "pandas",
    "numpy",
    "PIL",
}

_SHARED_MOCK = MagicMock()


class _StubModule(types.ModuleType):
    """桩模块：带 __path__ 以支持子模块导入，任意属性返回 MagicMock。"""

    __path__ = []

    def __getattr__(self, name):
        if name.startswith("__"):
            raise AttributeError(name)
        return _SHARED_MOCK


class _StubFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split(".")[0] in STUB_TOP_LEVEL:
            return importlib.machinery.ModuleSpec(fullname, _StubLoader(), is_package=True)
        return None


class _StubLoader(importlib.abc.Loader):
    def create_module(self, spec):
        return _StubModule(spec.name)

    def exec_module(self, module):
        pass


def install_stubs():
    """注册桩模块查找器。"""
    sys.meta_path.insert(0, _StubFinder())


def load_app():
    """导入后端应用，返回 FastAPI 实例。"""
    install_stubs()
    if PROJECT_DIR not in sys.path:
        sys.path.insert(0, PROJECT_DIR)
    import main as app_module  # noqa: E402
    return app_module.app


def test_app_routes_registered():
    """全部接口均应成功注册。"""
    app = load_app()
    paths = app.openapi()["paths"]
    operations = sum(len(methods) for methods in paths.values())

    # 当前版本共 17 个接口，允许后续新增，但不允许减少
    assert operations >= 17, f"注册接口数异常：{operations}（期望 >= 17）"
    assert "/chat" in paths, "缺少对话接口 /chat"
    assert "/analyze" in paths, "缺少情绪识别接口 /analyze"
    assert "/speech_to_text" in paths, "缺少语音转写接口 /speech_to_text"
    assert app.title, "FastAPI 应用未设置标题"


def run():
    """命令行入口：打印路由清单并返回退出码。"""
    app = load_app()
    paths = app.openapi()["paths"]
    operations = sum(len(methods) for methods in paths.values())

    print(f"✔ 应用装配成功：{app.title}")
    print(f"✔ 注册路由 {len(paths)} 条 / 接口操作 {operations} 个：")
    for path in sorted(paths):
        methods = ",".join(m.upper() for m in paths[path])
        print(f"    {methods:8s} {path}")

    assert operations >= 17, f"注册接口数异常：{operations}"
    print("\n冒烟测试通过")
    return 0


if __name__ == "__main__":
    sys.exit(run())
