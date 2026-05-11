from .core import generate

def polish_text(original: str, instruction: str, api_key: str):
    """根据指令润色或扩写段落"""
    system = (
        "你是一位文字编辑，擅长根据指令优化小说段落。"
        "请严格遵循用户的润色要求，保留原意的同时提升文学质感。"
    )
    prompt = (
        f"原始段落：\n{original}\n\n"
        f"润色指令：{instruction}\n\n"
        "请直接输出润色后的完整段落，无需额外解释。"
    )
    return generate(
        prompt,
        api_key=api_key,
        system=system,
        max_tokens=len(original) * 2 + 200,
        temperature=0.8
    )