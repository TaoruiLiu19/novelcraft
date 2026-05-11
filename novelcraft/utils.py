def count_chinese_chars(text: str) -> int:
    """统计中文字符数量（不包含英文/数字）"""
    import re
    return len(re.findall(r'[\u4e00-\u9fff]', text))

def split_text_by_length(text: str, max_length: int = 10000) -> list:
    """简单按字符数切分文本"""
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]