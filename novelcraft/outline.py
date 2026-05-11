from .core import generate

def generate_outline(idea: str, api_key: str, num_versions: int = 2, words_per_version: int = 2000):
    """
    生成多个版本的小说章节大纲
    words_per_version: 每个大纲版本允许的最大生成 token 数，控制详细程度
    """
    system = (
        "你是一位小说策划编辑。请根据用户提供的故事梗概，设计一份详细的章节大纲。"
        "大纲应该包含章节标题和每章的核心情节。确保有明确的三幕剧结构。"
    )
    outlines = []
    for i in range(num_versions):
        prompt = (
            f"故事梗概：{idea}\n"
            f"请生成第{i+1}种不同方向的大纲，包含约15章的章节概要。"
            f"每章简要描述关键事件，突出情节转折点。"
        )
        res = generate(
            prompt,
            api_key=api_key,
            system=system,
            max_tokens=words_per_version,   # ← 直接使用传入的详细程度值
            temperature=0.9
        )
        outlines.append(res)
    return outlines