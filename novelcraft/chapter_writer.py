from .core import generate

def write_chapter(
    chapter_outline: str,
    api_key: str,
    target_word_count: int = 8000,
    title: str = ""
):
    """
    根据章节大纲生成完整章节正文。
    target_word_count: 目标字数（汉字），将转化为 max_tokens 和 prompt 要求。
    """
    # 中文 1 汉字 ≈ 0.5 token（粗略），实际可给 1.2 倍空间防止截断
    max_tokens = min(int(target_word_count * 0.6), 12288)  # 上限 12288 tokens

    system = (
        "你是一位职业小说作家，擅长将简略大纲扩展为生动饱满的章节正文。"
        "请根据提供的大纲，创作完整的章节内容。"
        "注重人物心理、环境描写、对话推进情节，保持文笔流畅。"
        f"目标字数约 {target_word_count} 字。"
    )
    user_prompt = f"章节大纲：\n{chapter_outline}\n"
    if title:
        user_prompt = f"作品名称：《{title}》\n" + user_prompt

    user_prompt += (
        "\n请根据以上大纲，写出完整的章节内容，"
        f"目标约 {target_word_count} 字，直接输出正文，无需额外说明。"
    )

    return generate(
        prompt=user_prompt,
        api_key=api_key,
        system=system,
        max_tokens=max_tokens,
        temperature=0.85,
        reasoning_effort="high"
    )