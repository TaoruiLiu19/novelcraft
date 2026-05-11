from .core import generate

def generate_dialogue(char1: str, char2: str, scene: str, rounds: int, api_key: str):
    """生成两个角色之间的对话"""
    system = (
        "你是一位剧本作者，擅长编写自然、符合人设的人物对白。"
        "只输出对话文本，不添加额外说明。"
    )
    prompt = (
        f"角色A设定：{char1}\n"
        f"角色B设定：{char2}\n"
        f"场景：{scene}\n\n"
        f"请生成一段约{rounds}轮的自然对话。使用以下格式：\n"
        f"A: ...\nB: ...\n...\n"
        "要求对话展现角色性格，并推动情节发展。"
    )
    return generate(
        prompt,
        api_key=api_key,
        system=system,
        max_tokens=rounds * 150,
        temperature=1.0
    )