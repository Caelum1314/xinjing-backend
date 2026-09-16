import tempfile
import os
import PyPDF2
from docx import Document
from services.ai_service import call_ai


def extract_text_from_file(file_path, file_ext):
    text = ""
    if file_ext == ".txt":
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
    elif file_ext == ".pdf":
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() + "\n"
    elif file_ext in [".doc", ".docx"]:
        doc = Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    return text


def analyze_document(file_bytes, filename):
    file_ext = os.path.splitext(filename)[1].lower()

    supported_formats = ['.txt', '.pdf', '.doc', '.docx']
    if file_ext not in supported_formats:
        return {"success": False, "error": f"不支持的文件格式: {file_ext}"}

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=file_ext)
    temp_file.write(file_bytes)
    temp_file.close()

    text = extract_text_from_file(temp_file.name, file_ext)

    os.unlink(temp_file.name)

    if not text or len(text.strip()) < 10:
        return {"success": False, "error": "文档内容太少或无法提取文字"}

    if len(text) > 3000:
        text = text[:3000] + "\n...(内容已截断)"

    messages = [
        {"role": "system", "content": "分析文档内容，输出：1.主题 2.情绪倾向 3.关键点 4.建议"},
        {"role": "user", "content": f"请分析：\n\n{text}"}
    ]

    response = call_ai(messages, stream=False, max_tokens=800)
    analysis = response.choices[0].message.content

    return {"success": True, "filename": filename, "analysis": analysis}