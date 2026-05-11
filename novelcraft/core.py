from openai import OpenAI

def generate(
    prompt: str,
    api_key: str,
    system: str = "你是一位经验丰富的小说家。",
    temperature: float = 0.9,
    max_tokens: int = 2048,
    reasoning_effort: str = "medium",
    stream: bool = False
):
    """
    统一调用 DeepSeek V4-Flash，需要提供有效的 api_key
    reasoning_effort: 'low', 'medium', 'high'
    """
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": prompt}
    ]
    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=stream,
        extra_body={"reasoning_effort": reasoning_effort}
    )
    if stream:
        return response  # 返回流式迭代器
    return response.choices[0].message.content