from getpass import getpass
from novelcraft import generate_outline, create_character, polish_text, generate_dialogue, generate_next_chapter

def main():
    print("=== NovelCraft CLI Demo ===\n")
    api_key = getpass("请输入 DeepSeek API Key: ").strip()
    if not api_key:
        print("需要 API Key 才能运行。")
        return

    print("\n1. 生成大纲")
    outlines = generate_outline("一个时间旅行者试图阻止未来的灾难，却发现灾难正是自己造成的", api_key=api_key, num_versions=1)
    print(outlines[0][:300] + "...\n")

    print("2. 创建人物")
    char = create_character("陈默", "物理学家，性格谨慎但关键时刻勇敢无畏", api_key=api_key)
    print(char["bio"][:300] + "...\n")

    print("3. 段落润色")
    raw = "她站在悬崖边，风很大。"
    polished = polish_text(raw, "用细腻的比喻增强画面感，并暗示内心的挣扎", api_key=api_key)
    print(polished + "\n")

    print("4. 生成对话")
    dialogue = generate_dialogue("高冷上司", "社畜下属", "加班后的电梯间", rounds=4, api_key=api_key)
    print(dialogue + "\n")

    print("5. 续写示例")
    fake_full_book = "第一章：主角在图书馆发现一本神秘日记。日记里记载着他明天的遭遇..."
    next_ch = generate_next_chapter(fake_full_book, api_key=api_key, hint="主角决定验证日记的真实性", title="预知日记")
    print(next_ch[:500] + "...\n")

if __name__ == "__main__":
    main()