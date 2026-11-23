<div align="center">
  <img src="assets/logo.png" alt="芸窗 Logo" width="128" />
</div>

# 芸窗·古籍 AI 排版系统 (Guji AI Typesetter)

一款**零后端、纯静态可托管于 GitHub Pages** 的古籍雕版重排与 AI 标校工作台。支持将任意现代文本、本地文档或 GitHub 开源古籍语料一键重排为传统线装雕版书叶，并导出高清 PNG 与整书 PDF。

<div align="center">

**🚀 在线试用（GitHub Pages）：[https://erich1566.github.io/guji-ai-typesetter/](https://erich1566.github.io/guji-ai-typesetter/)**

</div>

---

## ✨ 核心特性

1. **传统雕版字格级排版引擎**
   - 严格遵循竖排左行、自上而下阅读次序，支持**筒子页全叶（右半叶 + 版心 + 左半叶）**、单看半叶及整书平铺总览。
   - 完整还原**版框（文武双边/左右双边/单边）**、**界行（乌丝栏/朱丝栏/无界行）**、**鱼尾（单/双/花鱼尾）**、**象鼻（白口/细黑口/大黑口）**、**书耳**、**天头朱笔眉批**、**藏书钤印**与**双行小字夹注**（支持传统同列先右后左跨格折行）。
2. **打通 GitHub 开源底层语料库**
   - **殆知阁古代文献库（[`garychowcmu/daizhigev20`](https://github.com/garychowcmu/daizhigev20)）**：在线直连浏览儒/史/子/集/诗/易/医/艺/道/佛十大部类目录，一键拉取原文载入排版。
   - **中华古诗词数据库（[`chinese-poetry/chinese-poetry`](https://github.com/chinese-poetry/chinese-poetry)）**：直连《全唐诗》《宋词》《诗经》《楚辞》《论语》《元曲》等分卷 JSON，自动解析作者、诗题、正文与诗注。
3. **内置免费开源古籍字体 + 本地字体支持**
   - 内置 **7 款免费开源古籍字体**（思源宋体繁/简、霞鹜文楷繁体/屏显版、Shippori Mincho 刻本明朝、志莽行书、马善政楷书）。
   - 支持直接加载本地 `.ttf` / `.otf` / `.woff2` 字体文件或扫描调用本机已安装字库。
4. **自定义 AI API 智能标校**
   - 支持配置任意 **OpenAI 兼容接口**（DeepSeek、通义千问、OpenAI、智谱 GLM、本地 Ollama），实现正文与注疏分离、专名/书名标校、智能分卷眉批与体裁版式推荐。
5. **多格式文档上传与工程导入**
   - 支持上传 `.txt`、`.md`、`.json`、`.html`、`.docx`（Word 文档前端直解）及 `.guji.json` 工程文件。
6. **线装封面与牌记定制 + 整书 PDF 一键导出**
   - 自定义书衣绢锦底色、四眼/六眼线装、题签样式与扉页木记牌记；支持整书一次性合成高清 PDF 导出。
7. **配套 Agent Skill（`skills/guji-ai-typesetter/`）**
   - 提供标准 `SKILL.md` 与 Python CLI 脚本（`preprocess_guji.py`、`auto_typeset.py`），供 **Codex、WorkBuddy、Claude Code、Gemini CLI** 等 Agent 直接调用完成文本规范化与自动排版。

---

## 📁 仓库结构

```text
.
├── index.html                          # 静态 Web 应用主程序（可直接部署 GitHub Pages）
├── package.json                        # npm 一键启动/部署脚本（npm start 本地部署）
├── README.md                           # 项目说明文档
├── docs/
│   ├── PRD.md                          # 产品需求文档
│   └── IMPLEMENTATION_ROADMAP.md       # 技术架构与实现路径
├── skills/
│   └── guji-ai-typesetter/             # 配套 Agent Skill（支持 Codex / WorkBuddy 等）
│       ├── SKILL.md
│       └── scripts/
│           ├── preprocess_guji.py      # 文本清洗、正文注疏分离、句读与分卷脚本
│           └── auto_typeset.py         # 自动版式匹配与 .guji.json 工程生成脚本
└── .github/
    └── workflows/
        └── pages.yml                   # GitHub Actions 自动部署 GitHub Pages 配置
```

---

## 🖥️ 本地部署（推荐）

在线试用版已部署于 **[https://erich1566.github.io/guji-ai-typesetter/](https://erich1566.github.io/guji-ai-typesetter/)** ，可先在线体验；如需本地私密使用或二次开发，按以下步骤部署。

**零后端、零构建、无需安装任何依赖** —— 克隆仓库后一条命令即可启动：

```bash
git clone https://github.com/Erich1566/guji-ai-typesetter.git
cd guji-ai-typesetter
npm start
```

启动后浏览器打开 **http://localhost:8080** 即可使用全部功能（重排工坊、语料库直连、AI 标校、整书 PDF 导出）。

### 一键启动方式（任选其一）

| 方式 | 命令 | 环境要求 |
| :--- | :--- | :--- |
| **npm / npx 一键启动** | `npm start`（等价于 `npx -y serve -l 8080 .`） | Node.js ≥ 18，无需 `npm install` |
| **Python 内置服务器** | `python -m http.server 8080`（或 `npm run start:py`） | Python ≥ 3.8 |
| **免安装直接使用** | 双击 `index.html` 用浏览器打开 | 无；本地存储策略可能影响配置持久化，建议优先用前两种 |

> 💡 AI 标校功能需在「✨ AI 标校与 API」面板配置您的自定义大模型 API（OpenAI 兼容格式），API Key 仅保存在本地浏览器，不经任何中转。

### CLI 一键部署到专属 GitHub Pages（可选）

如需拥有专属在线地址，将仓库推送到您的 GitHub 账号即可 —— 仓库已内置 Actions 工作流（`.github/workflows/pages.yml`），**推送即自动发布**，无需手动配置：

```bash
# 首次使用请先完成 GitHub 授权：gh auth login
npm run deploy        # 等价于 git add -A && git commit && git push
```

1–2 分钟后即可通过 `https://<username>.github.io/guji-ai-typesetter/` 在线访问。若推送至您新建/fork 的仓库，请在 **Settings → Pages → Source** 中选择 **GitHub Actions**（`Deploy from a branch` → `main` / `(root)` 亦可）。
