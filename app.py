import streamlit as st
from dotenv import load_dotenv, set_key
import os

from novelcraft.outline import generate_outline
from novelcraft.character import create_character
from novelcraft.editor import polish_text
from novelcraft.dialogue import generate_dialogue
from novelcraft.memory import generate_next_chapter
from novelcraft.chapter_writer import write_chapter   # 新增导入

load_dotenv()

st.set_page_config(page_title="NovelCraft", layout="wide")
st.title("📖 NovelCraft 小说创作助手")

# ===== 侧边栏 API Key =====
st.sidebar.header("🔑 API 设置")
saved_key = os.getenv("DEEPSEEK_API_KEY", "")

api_key = st.sidebar.text_input(
    "请输入 DeepSeek API Key",
    type="password",
    value=saved_key,
    placeholder="sk-...",
    help="输入后自动保存到本地 .env 文件"
)

if api_key and api_key != saved_key:
    try:
        set_key(".env", "DEEPSEEK_API_KEY", api_key)
        st.sidebar.success("✅ API Key 已自动保存")
    except Exception as e:
        st.sidebar.warning(f"⚠️ 保存失败: {e}")

if not api_key:
    st.warning("👈 请先在左侧输入 API Key")
    st.stop()

# ===== 六个功能标签 =====
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ["📋 大纲", "👤 人物", "✍️ 润色", "💬 对话", "📚 全书记忆", "📝 章节生成"]
)
# ────── Tab1: 大纲（含导出功能） ──────
with tab1:
    st.header("创意大纲生成")
    idea = st.text_area("输入你的故事梗概", height=100)
    versions = st.slider("生成版本数", 1, 3, 2)
    detail_level = st.slider(
        "大纲详细程度",
        min_value=500, max_value=4000, value=2000, step=100,
        help="数值越大，大纲越详细（对应最大 token 数）"
    )

    if st.button("生成大纲", key="btn_outline"):
        if idea.strip():
            with st.spinner("正在构思..."):
                outlines = generate_outline(
                    idea, api_key=api_key, num_versions=versions,
                    words_per_version=detail_level
                )
            # 保存到 session_state，方便后续下载（避免 re‑run 丢失）
            st.session_state.outlines = outlines
        else:
            st.warning("请输入故事梗概")

    # 如果已有大纲，显示并添加下载按钮
    if "outlines" in st.session_state and st.session_state.outlines:
        for i, o in enumerate(st.session_state.outlines):
            with st.expander(f"📄 版本 {i+1}"):
                st.write(o)
                # 单个版本下载
                st.download_button(
                    label=f"⬇️ 下载 版本 {i+1} (TXT)",
                    data=o,
                    file_name=f"大纲_版本{i+1}.txt",
                    mime="text/plain",
                    key=f"dl_outline_{i}"
                )
        # 全部合并下载
        all_text = "\n\n---\n\n".join(
            [f"# 版本 {i+1}\n{o}" for i, o in enumerate(st.session_state.outlines)]
        )
        st.download_button(
            label="⬇️ 下载全部版本 (合并 TXT)",
            data=all_text,
            file_name="大纲_全部版本.txt",
            mime="text/plain",
            key="dl_outline_all"
        )
# ────── Tab2: 人物 ──────
with tab2:
    st.header("人物工坊")
    name = st.text_input("角色姓名", key="char_name")
    traits = st.text_area("角色标签", height=80, key="char_traits")
    if st.button("生成人物设定", key="btn_char"):
        if name and traits:
            with st.spinner("正在刻画..."):
                char = create_character(name, traits, api_key=api_key)
            st.subheader("人物小传")
            st.write(char["bio"])
            st.subheader("关系图 (Mermaid)")
            st.code(char["relation_diagram"], language="mermaid")
        else:
            st.warning("请填写姓名和标签")

# ────── Tab3: 润色 ──────
with tab3:
    st.header("段落润色/扩写")
    original = st.text_area("原始段落", height=150, key="edit_original")
    instruction = st.text_input("润色指令", key="edit_instruction")
    if st.button("润色段落", key="btn_edit"):
        if original.strip() and instruction.strip():
            with st.spinner("打磨文字..."):
                polished = polish_text(original, instruction, api_key=api_key)
            st.subheader("润色后")
            st.write(polished)
        else:
            st.warning("请输入段落和指令")

# ────── Tab4: 对话 ──────
with tab4:
    st.header("角色对白生成")
    col1, col2 = st.columns(2)
    with col1:
        char1 = st.text_input("角色A设定", "内向的侦探", key="dlg_char1")
    with col2:
        char2 = st.text_input("角色B设定", "神秘的目击者", key="dlg_char2")
    scene = st.text_input("场景", "深夜的旧图书馆", key="dlg_scene")
    rounds = st.slider("对话轮数", 3, 10, 5, key="dlg_rounds")
    if st.button("生成对话", key="btn_dialogue"):
        if char1 and char2 and scene:
            with st.spinner("角色交谈中..."):
                dialogue = generate_dialogue(char1, char2, scene, rounds, api_key=api_key)
            st.subheader("对话脚本")
            st.write(dialogue)
        else:
            st.warning("请填写两个角色和场景")

# ────── Tab5: 全书记忆 ──────
with tab5:
    st.header("全书记忆引擎")
    st.markdown("利用百万Token上下文窗口，续写时自动回收伏笔。")
    if 'book_text' not in st.session_state:
        st.session_state.book_text = ""
    if 'book_title' not in st.session_state:
        st.session_state.book_title = ""

    book_title = st.text_input("书名（可选）", value=st.session_state.book_title or "", key="mem_title")
    uploaded_file = st.file_uploader("上传已写内容（.txt）", type="txt", key="mem_upload")
    if uploaded_file is not None:
        book_content = uploaded_file.read().decode("utf-8")
        st.session_state.book_text = book_content
        st.session_state.book_title = book_title
        st.success(f"已加载 {len(book_content)} 字符")

    manual_text = st.text_area("或直接粘贴全书已写内容", height=200, value=st.session_state.book_text, key="mem_manual")
    if manual_text != st.session_state.book_text:
        st.session_state.book_text = manual_text

    col1, col2 = st.columns(2)
    with col1:
        new_chapter_hint = st.text_area("新章写作方向/提示", height=100, key="mem_hint")
    with col2:
        if st.button("续写下一章", key="btn_memory"):
            if not st.session_state.book_text.strip():
                st.warning("请先输入或上传全书内容")
            else:
                with st.spinner("翻阅前文并创作..."):
                    next_chapter = generate_next_chapter(
                        st.session_state.book_text,
                        api_key=api_key,
                        hint=new_chapter_hint,
                        title=st.session_state.book_title
                    )
                st.subheader("新章草稿")
                st.write(next_chapter)
                if st.button("将新章加入全书记忆", key="btn_append"):
                    st.session_state.book_text += "\n\n" + next_chapter
                    st.success("已追加！全书长度：" + str(len(st.session_state.book_text)) + "字符")

# ────── Tab6: 章节生成（新功能） ──────
with tab6:
    st.header("📝 根据大纲生成章节正文")
    st.markdown("输入某一章的大纲，AI 将为你展开为完整的章节内容（最长 8000 字）。")

    chapter_outline = st.text_area(
        "请输入本章大纲",
        height=150,
        placeholder="例如：主角在废弃工厂发现第一个线索，与追兵发生冲突并惊险逃脱。"
    )
    target_words = st.slider(
        "目标字数",
        min_value=1000,
        max_value=8000,
        value=4000,
        step=500,
        help="AI 会尽量遵照此字数创作，实际可能有浮动。"
    )
    chapter_title = st.text_input("章节标题（可选）", placeholder="第三章：暗夜追踪")

    if st.button("生成章节", key="btn_write_chapter"):
        if chapter_outline.strip():
            with st.spinner("正在撰写章节内容，请稍候..."):
                chapter_content = write_chapter(
                    chapter_outline=chapter_outline,
                    api_key=api_key,
                    target_word_count=target_words,
                    title=chapter_title
                )
            st.subheader("生成结果")
            st.write(chapter_content)
            # 显示实际字数
            char_count = len(chapter_content.replace(" ", "").replace("\n", ""))
            st.caption(f"实际字符数（含标点）：约 {char_count} 字")
        else:
            st.warning("请至少输入章节大纲")