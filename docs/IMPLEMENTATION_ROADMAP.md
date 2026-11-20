# 芸窗·古籍 AI 排版系统 — 技术架构与实现路径

## 1. 系统总体架构

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                        用户交互层 & 外部 Agent 生态                        │
│  ┌─────────────────────────┐        ┌────────────────────────────────┐  │
│  │  静态 Web 应用 (SPA)     │        │  Codex / WorkBuddy / AI Agent  │  │
│  │  index.html (GitHub     │◄──────►│  skills/guji-ai-typesetter/    │  │
│  │  Pages 零后端托管)       │        │  SKILL.md + Python CLI 脚本     │  │
│  └───────────┬─────────────┘        └───────────────┬────────────────┘  │
└──────────────┼──────────────────────────────────────┼───────────────────┘
               │                                      │
               ▼                                      ▼
┌──────────────────────────────┐        ┌─────────────────────────────────┐
│       多源语料与文档接入层     │        │        AI 标校与预处理层          │
│ • 殆知阁 API (GitHub Raw/CDN)│        │ • OpenAI 兼容 API (DeepSeek/    │
│ • Chinese-Poetry JSON 直连   │        │   Qwen/GPT/Ollama 本地模型)     │
│ • 本地上传 (.txt/.md/.docx)  │        │ • 正文/注疏分离、专名标校、分卷  │
└──────────────┬───────────────┘        └────────────────┬────────────────┘
               │                                         │
               └────────────────────┬────────────────────┘
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     字格级雕版引擎与字体/导出层                           │
│ • 竖排左行 Token 解析器（【夹注】/〈专名〉/《书名》/[卷标:]/[眉批:]）      │
│ • 内置 7 款开源免费古籍字体 (Google Fonts / jsDelivr) + 本地 TTF/OTF     │
│ • Canvas 2x 高清书叶渲染 + jsPDF 整书合成（线装封面 + 牌记 + 全部筒子页） │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. 分阶段实现路径（Roadmap）

### Phase 1：基础雕版内核与多卷排版（已完成）
- 实现字格级竖排左行引擎，支持双行小字跨格折行、朱笔句读、专名/书名线、书耳、鱼尾象鼻版心。
- 支持线装封面题签与扉页牌记自定义，支持整书多卷分页与 `jsPDF` 整书 PDF 导出。

### Phase 2：免费古籍字体体系建设（本阶段自动实现）
- 集成 **7 款免费开源古籍字体**：
  1. `Noto Serif TC`（思源宋体繁体·传承旧字形风格）
  2. `Noto Serif SC`（思源宋体简体）
  3. `LXGW WenKai TC`（霞鹜文楷繁体·保留传承字形）
  4. `LXGW WenKai Screen`（霞鹜文楷屏幕阅读版，jsDelivr 分包加速）
  5. `Shippori Mincho`（明朝体·木刻书卷风味）
  6. `Zhi Mang Xing`（行书·手抄古籍风）
  7. `Ma Shan Zheng`（毛笔楷书·适合封面题签与大字匾额）
- 保留本地 `.ttf`/`.otf`/`.woff2` 拖放加载与系统字体枚举能力。

### Phase 3：GitHub 底层语料库直连与多格式文档上传（本阶段自动实现）
- **殆知阁浏览器端直连客户端**：调用 `https://api.github.com/repos/garychowcmu/daizhigev20/contents/<path>` 浏览目录，并通过 `raw.githubusercontent.com` / `cdn.jsdelivr.net` 拉取全文，支持大型典籍自动截取前 N 章或全文载入。
- **中国诗歌（`chinese-poetry`）直连客户端**：内置《全唐诗》《宋词》《诗经》《楚辞》《论语》《元曲》等分卷 JSON 直连入口，自动将 JSON 诗词数组格式化为带卷标、作者、诗题、正文与诗注的规范古籍文本。
- **本地文档解析器**：集成 `mammoth.js`（CDN）实现 `.docx` Word 文档纯前端解析，同时支持 `.txt`、`.md`、`.json`、`html` 导入。

### Phase 4：自定义 AI API 与智能化排版工作流（本阶段自动实现）
- 构建纯前端 `OpenAI Compatible Client`，支持自定义 Endpoint、API Key、Model，预设 DeepSeek、通义千问、OpenAI、Ollama 等模板。
- 实现 Prompt 工程化的四大功能：正文/注疏自动切分、专名/书名/句读精校、智能分卷与眉批、版式风格 JSON 推荐与一键应用。

### Phase 5：配套 Agent Skill（Codex / WorkBuddy / CLI 可调用）（本阶段自动实现）
- 编写 `skills/guji-ai-typesetter/SKILL.md` 及配套脚本：
  - `preprocess_guji.py`：实现正则与规则驱动的古籍文本清洗、繁简转换映射、括号注疏转 `【】`、现代标点转句读、章节自动转 `[卷标:]` 与 `[书耳:]`。
  - `auto_typeset.py`：支持 Agent 一键将任意文本或殆知阁/诗歌语料生成规范化重排工程文件（`.txt` / `.json`）并输出排版统计报告（总卷数、预计叶数、行款建议）。

### Phase 6：GitHub 仓库初始化与 GitHub Pages 自动部署配置
- 生成完整仓库目录结构：
  - `index.html`（核心静态应用入口）
  - `README.md`（中英双语项目说明、快速体验、Skill 安装指引）
  - `docs/PRD.md`、`docs/IMPLEMENTATION_ROADMAP.md`
  - `skills/guji-ai-typesetter/`（完整 Skill 包）
  - `.github/workflows/pages.yml`（GitHub Actions 一键自动部署 GitHub Pages 工作流）
- 推送到用户 GitHub 仓库并开启 GitHub Pages，获得公开可访问的试用 URL。
