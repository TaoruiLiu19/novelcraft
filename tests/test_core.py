import pytest
from novelcraft.core import generate

def test_generate_basic():
    # 需提前设置环境变量 DEEPSEEK_API_KEY，或者在此传入 key
    import os
    key = os.getenv("DEEPSEEK_API_KEY")
    if not key:
        pytest.skip("跳过测试：未设置 DEEPSEEK_API_KEY 环境变量")
    res = generate("用一句话描写秋天", api_key=key, max_tokens=50, temperature=0.5)
    assert isinstance(res, str)
    assert len(res) > 0