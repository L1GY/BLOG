import re
from datetime import datetime

def format_datetime(value, format='%Y-%m-%d %H:%M'):
    """格式化日期时间"""
    if isinstance(value, datetime):
        return value.strftime(format)
    return value

def truncate_text(text, length=100, suffix='...'):
    """截断文本"""
    if len(text) <= length:
        return text
    return text[:length].rsplit(' ', 1)[0] + suffix

def slugify(text):
    """将文本转换为URL友好的slug"""
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    text = re.sub(r'[-\s]+', '-', text)
    return text

def get_reading_time(content):
    """估算阅读时间（基于中文平均每分钟300字）"""
    word_count = len(content)
    return max(1, word_count // 300)

def get_excerpt(content, length=150):
    """获取文章摘要"""
    # 移除HTML标签
    text = re.sub(r'<[^>]+>', '', content)
    return truncate_text(text, length)