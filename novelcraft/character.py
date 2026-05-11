from .core import generate

def create_character(name: str, traits: str, api_key: str):
    """生成详细人物小传和关系图描述"""
    system = "你是一位角色设计师，专门为小说创作生动的人物。"
    prompt = (
        f"角色姓名：{name}\n"
        f"基本设定：{traits}\n\n"
        "请生成以下内容：\n"
        "1. 人物小传（包括外貌、性格、背景故事、内心冲突、性格弧光）\n"
        "2. 该角色与其他潜在角色的关系（可虚构几个典型关系）\n"
        "请将回答分成两部分，用 '---RELATION---' 分隔。"
        "关系部分请用简洁的陈述句描述（如：与导师李教授是亦师亦友的关系）。"
    )
    full = generate(prompt, api_key=api_key, system=system, max_tokens=1500, temperature=0.8)
    
    if "---RELATION---" in full:
        parts = full.split("---RELATION---")
        bio = parts[0].strip()
        relation_text = parts[1].strip()
    else:
        bio = full
        relation_text = "（无法解析关系）"

    # 生成 Mermaid 格式关系图
    system_mermaid = "你是一个将人物关系转化为 Mermaid 流程图代码的助手。只输出代码块，不要解释。"
    prompt_mermaid = (
        f"根据以下人物关系描述，生成一个 Mermaid 关系图（graph TD），"
        f"节点是人物姓名，边是关系标签。\n{relation_text}"
    )
    mermaid_code = generate(
        prompt_mermaid,
        api_key=api_key,
        system=system_mermaid,
        max_tokens=500,
        temperature=0.2
    )
    # 清理可能的markdown代码块标记
    mermaid_code = mermaid_code.strip("`").strip()
    if mermaid_code.startswith("mermaid"):
        mermaid_code = mermaid_code[7:].strip()

    return {
        "name": name,
        "traits": traits,
        "bio": bio,
        "relation_diagram": mermaid_code
    }