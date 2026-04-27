# 远明老师的课堂笔记

> C++ 信奥知识点交互动画 · 游戏化练习 · 代码模板

🌐 **在线访问**: [notes.yuanming.wang](https://notes.yuanming.wang)

## 项目简介

面向 C++ 信奥竞赛教学的静态知识站点，包含：

- **算法动画** — 交互式可视化演示（取余、分装、cin 流等）
- **知识点游戏** — 游戏化练习（闰年判断、符号识别等）
- **C++ 代码模板** — GESP 1~8 级共 72 个模板，按知识点分级

纯静态站点，零 CDN 依赖，离线可用。

## 目录结构

```
notes/
├── .github/workflows/deploy.yml   # GitHub Pages 自动部署
├── build.py                       # 构建脚本
├── index_template.html            # 首页模板
├── template.html                  # C++ 模板页面外壳
├── CONVENTIONS.md                 # 开发规范（AI 修改前必读）
├── animations/                    # 算法动画 HTML + .meta.md
├── games/                         # 知识点游戏 HTML + .meta.md
├── cpp/                           # C++ 模板 .md 源文件（G1~G8 分级）
│   └── dist/                      # 构建产物（.gitignore）
├── assets/                        # 本地资源（Tailwind/KaTeX/字体）
│   ├── css/
│   └── js/
└── index.html                     # 构建产物（.gitignore）
```

## 本地开发

```bash
# 安装依赖
pip install markdown

# 构建站点
python3 build.py

# 本地预览
python3 -m http.server 8765
# 打开 http://localhost:8765
```

## 部署

推送到 `main` 分支后，GitHub Actions 自动构建并部署到 GitHub Pages。

流程：`push → checkout → pip install markdown → build.py → deploy-pages`

### 自定义域名

CNAME 已配置为 `notes.zhong.ac.cn`，在 GitHub 仓库 Settings → Pages → Custom domain 中设置。

## 开发规范

新增或修改动画/游戏时，请先阅读 [CONVENTIONS.md](./CONVENTIONS.md)，包含：

- 统一导航栏模板
- 品牌色 (#2563eb) 和本地资源路径约定
- `.meta.md` 元数据格式
- 构建流程

## 技术栈

| 组件 | 方案 |
|------|------|
| 页面 | 纯 HTML + CSS/JS |
| 样式 | Tailwind CSS（本地 tailwind.js） |
| 数学渲染 | KaTeX（本地资源） |
| 代码高亮 | Prism.js（本地资源） |
| 构建 | Python 3 + markdown 库 |
| 部署 | GitHub Pages + GitHub Actions |

## License

© 2026 YuanMing
