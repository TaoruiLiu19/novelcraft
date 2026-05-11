from .core import generate

def generate_next_chapter(full_book_text: str, api_key: str, hint: str = "", title: str = "未知作品"):
    """基于全书已写内容生成下一章，要求上下文一致、回收伏笔"""
    max_chars = 900_000
    if len(full_book_text) > max_chars:
        trimmed = full_book_text[-max_chars:]
    else:
        trimmed = full_book_text

    system = (
        f"你是一位小说作家，正在创作《{title}》。"
        "下面提供了这部作品截至目前的全部内容。"
        "请根据前文，续写下一章。要求：\n"
        "1. 保持人物性格、情节、世界观完全一致。\n"
        "2. 自然回收前文埋下的伏笔（关键悬念）。\n"
        "3. 为新章设置新的冲突或转折点。\n"
        "4. 请直接输出章节正文，不要包含章节标题。"
    )
    user_prompt = f"已写全文：\n\n{trimmed}\n\n"
    if hint:
        user_prompt += f"本章提示：{hint}\n"
    user_prompt += "请开始续写下一章："

    return generate(
        prompt=user_prompt,
        api_key=api_key,
        system=system,
        max_tokens=4000,
        temperature=0.85,
        reasoning_effort="high"
    )