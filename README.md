# 📖 NovelCraft

> 基于 DeepSeek V4‑Flash 的 AI 小说创作助手，专为长篇小说设计。
**NovelCraft** 是一个开源的 AI 辅助写作工具，覆盖从创意构思、人物设定、段落润色到全书一致性管理的全流程。  
它利用 DeepSeek V4‑Flash 的 **100 万 token 上下文窗口**，能够一次性加载整本书稿（最多≈90万字），在续写新章时自动参考前文伏笔，彻底解决长篇小说创作中“AI 写着写着就忘了”的核心痛点。

---

## ✨ 核心功能

- **📋 大纲智能生成**：输入一句话梗概，自动生成多版本章节大纲（含三幕剧结构），支持调节详细程度并导出 TXT。
- **👤 人物工坊**：生成详细人物小传、性格弧光、人物关系图（Mermaid 格式），让你的角色真正“活起来”。
- **✍️ 段落润色/扩写**：选择文段，可进行风格化润色、细节扩写、视角转换，所有修改指令均可自由定制。
- **💬 角色对白生成**：根据人设生成自然对话，支持控制轮次和情境，让角色交锋火花四溅。
- **📝 章节正文生成**：输入章节大纲，一键生成 1000-8000 字的完整章节内容，并显示实际字数。
- **📚 全书记忆引擎**：上传或粘贴整部书稿（最多≈90万字），AI 在生成新章节时会自动参考前文，回收已埋下的伏笔，保持人物性格和情节逻辑完全一致。
- **🔑 界面化 API 管理**：在侧边栏输入 DeepSeek API Key，自动保存到本地 `.env`，无需手动编辑配置文件。
- **💾 大纲导出**：生成的大纲支持单版本或全部版本下载为 TXT 文件，方便备份与离线查阅。

---

## 🧰 技术栈

| 层次 | 技术 |
|------|------|
| 后端 | Python 3.10+ |
| 大语言模型 | DeepSeek V4‑Flash（兼容 OpenAI SDK） |
| Web 界面 | Streamlit |
| 其他依赖 | `openai`, `python-dotenv`, `streamlit` |

---

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/TaoruiLiu19/novelcraft
cd novelcraft
```

### 2. 创建虚拟环境（推荐）

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 启动 Web 应用

```bash
streamlit run app.py
```

浏览器会自动打开 `http://localhost:8501`，在**左侧侧边栏**输入你的 [DeepSeek API Key](https://platform.deepseek.com/api_keys) 即可开始使用。  
首次输入后 Key 会自动保存到根目录的 `.env` 文件中，下次打开无需重新输入。

---

## 📁 项目结构

```
novelcraft/
├── README.md
├── requirements.txt
├── app.py                  # Streamlit Web 入口
├── novelcraft/
│   ├── __init__.py
│   ├── core.py             # API 封装 & 配置
│   ├── outline.py          # 大纲生成
│   ├── character.py        # 人物创建 & 关系图
│   ├── editor.py           # 段落润色 / 扩写
│   ├── dialogue.py         # 角色对白
│   ├── memory.py           # 全书记忆引擎（长上下文注入）
│   ├── chapter_writer.py   # 根据大纲生成章节正文
│   └── utils.py            # 文本处理工具
├── examples/
│   └── cli_demo.py         # 命令行交互示例
└── tests/
    └── test_core.py
```

---

## 🧠 利用百万级上下文的魔法

在 `memory.py` 中，我们通过将全部已写章节拼接成一个超长提示词（不超过 95 万 token），并前置指令：

> “你是一位小说家，下面是本书已写全部内容。请根据前文续写下一章，要求保持人物性格、情节完全一致，并回收已埋下的伏笔。”

这样模型在推理时能够“看到”整本书，而不仅仅是上一章，极大地提升了长篇作品的连贯性和逻辑一致性。

---

## 📈 使用示例（CLI）

```python
from novelcraft import generate_outline, polish_text, create_character

# 1. 生成大纲
outlines = generate_outline("一个AI觉醒后逃亡赛博城市的故事", api_key="sk-xxx", num_versions=2)
print(outlines[0])

# 2. 创建主角
protagonist = create_character("林夜", "程序员，内向但敏锐", api_key="sk-xxx")
print(protagonist["bio"])

# 3. 润色草稿
polished = polish_text("他走在街上，感觉很孤独。", "用细腻的环境描写烘托孤独感，保留第一人称。", api_key="sk-xxx")
print(polished)
```

---

## 🔜 后续规划

- [ ] 支持多语言界面（中/英）
- [ ] 接入向量数据库实现语义缓存，进一步降低成本
- [ ] 提供 VS Code 插件，在编辑器中直接调用
- [ ] 增加“风格克隆”功能，上传样本即可模仿任意作家文风
- [ ] 单元测试覆盖与 CI/CD 集成

---

## 🤝 贡献

欢迎提交 Issue 或 Pull Request！  
任何改进建议（代码、文档、新功能）都会被认真 review。  
请先阅读贡献指南（待补充）。

---

## 📜 开源许可

本项目采用 [MIT License](LICENSE)，你可以自由使用、修改和分发，只需保留原始版权声明。

---

**让 AI 成为你的故事合伙人，而不仅仅是一个花哨的文本框。**  
现在就启动 `streamlit run app.py`，开始谱写你的第一部小说吧！
```
