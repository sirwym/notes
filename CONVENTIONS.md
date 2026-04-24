# 王老师的课堂笔记 — 开发规范

> **AI 修改动画/游戏前必读。** 任何新增或修改 HTML 文件，必须遵循以下规范。

---

## 一、导航栏（必须）

每个动画/游戏页面**必须**包含统一的顶部导航栏，紧贴 `<body>` 标签之后插入：

```html
<!-- 统一导航栏 -->
<nav style="position:fixed;top:0;left:0;right:0;z-index:9999;background:#fff;border-bottom:1px solid #e5e7eb;height:48px;display:flex;align-items:center;justify-content:space-between;padding:0 16px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif;">
    <a href="../index.html" style="display:flex;align-items:center;gap:6px;text-decoration:none;color:#6b7280;font-size:13px;transition:color 0.2s;" onmouseover="this.style.color='#2563eb'" onmouseout="this.style.color='#6b7280'">
        <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
        返回首页
    </a>
    <span style="font-size:12px;color:#9ca3af;">王老师的课堂笔记</span>
</nav>
```

导航栏为 inline style，不依赖任何外部 CSS 框架。

---

## 二、Body 偏移（必须）

导航栏高度 48px、fixed 定位，因此 body 必须偏移：

| 场景 | 写法 |
|------|------|
| 一般页面 | `body { margin-top: 48px; }` |
| 全屏容器页面（100vh） | `body { margin-top: 48px; height: calc(100vh - 48px); }` |
| 使用 Tailwind 的页面 | 直接在 `<body>` 加 `style="margin-top:48px;height:calc(100vh - 48px);"` |

**原则：页面内容不能被导航栏遮挡。**

---

## 三、品牌色（必须）

| 用途 | 色值 | CSS 变量 |
|------|------|----------|
| 主色 | `#2563eb` | `--primary: #2563eb` |
| 主色深 | `#1d4ed8` | `--primary-dark: #1d4ed8` |

**禁止使用紫色**（`#8b5cf6`、`#7c3aed`）或其他非品牌色作为主色。

Tailwind class 映射：
- `bg-brand-600` / `bg-brand-700` 代替 `bg-purple-600` / `bg-blue-600`
- `text-brand-600` 代替 `text-purple-600`
- `focus:ring-brand-500` 代替 `focus:ring-purple-500`
- `hover:border-brand-300` 用于边框高亮

Canvas/JS 中硬编码颜色也必须用 `#2563eb`，不要用紫色。

---

## 四、本地资源（必须，禁止 CDN）

**所有外部资源必须使用本地文件，零 CDN 依赖。**

### Tailwind CSS
```html
<script src="../assets/js/tailwind.js"></script>
```

### KaTeX（如需数学公式）
```html
<link rel="stylesheet" href="../assets/css/katex.min.css">
<script src="../assets/js/katex.min.js"></script>
<script src="../assets/js/auto-render.min.js"></script>
```

### 资源目录结构
```
assets/
├── css/
│   ├── katex.min.css
│   ├── prism-one-light.min.css
│   └── prism-vscode-dark.min.css
└── js/
    ├── auto-render.min.js
    ├── katex.min.js
    ├── prism-bundle.min.js
    └── tailwind.js
```

**删除所有 CDN 引用**（`cdn.tailwindcss.com`、`cdn.jsdelivr.net` 等）。

---

## 五、页面标题格式

```html
<title>页面名称 - 王老师的课堂笔记</title>
```

不要只写功能名，必须带 ` - 王老师的课堂笔记` 后缀。

---

## 六、.meta.md 元数据（必须）

每个新增动画/游戏 **必须** 创建对应的 `.meta.md` 文件，否则 `build.py` 不会收录到首页。

### 位置
- 动画：`animations/xxx.meta.md`
- 游戏：`games/xxx.meta.md`

### 格式
```markdown
---
title: 页面中文名
category: animation 或 game
subtitle: 一句话描述
tags: 关键词1 关键词2 关键词3
topic: GESP级别 或 知识点名称
---
```

### category 取值
| 值 | 含义 |
|----|------|
| `animation` | 算法动画（放 `animations/` 目录） |
| `game` | 知识点游戏（放 `games/` 目录） |

### topic 取值
- GESP 级别：`GESP1` ~ `GESP8`
- 或知识点名称：如 `取余与取模`、`条件嵌套`、`整除与进一`

### 示例
```markdown
---
title: cin 数据传送带
category: animation
subtitle: 模拟 cin 输入流的工作方式，理解数据如何传入变量
tags: cin 输入 传送带 流 GESP1
topic: GESP1
---
```

---

## 七、构建流程

修改动画/游戏或新增 `.meta.md` 后，必须重新构建：

```bash
cd /Users/mymac/工作站/Python项目/notes
python3 build.py
```

构建会扫描所有 `.meta.md` + `cpp/*.md`，重新生成 `index.html` 和 `cpp/dist/*.html`。

---

## 八、文件命名

- HTML 文件和 `.meta.md` 文件**同名**（除扩展名外）
- 例如：`零食大作战：求剩余.html` + `零食大作战：求剩余.meta.md`
- 中文命名可以，但避免特殊符号

---

## 九、适配检查清单

修改或新增动画/游戏时，逐项确认：

- [ ] 有统一导航栏（48px fixed，返回首页链接）
- [ ] body 有 margin-top: 48px 偏移
- [ ] 全屏页面 height 用 calc(100vh - 48px)
- [ ] 主色为 #2563eb（品牌蓝），无紫色
- [ ] 无 CDN 引用，全部使用本地 `../assets/` 资源
- [ ] 页面标题带 ` - 王老师的课堂笔记` 后缀
- [ ] 有对应的 `.meta.md` 元数据文件
- [ ] 运行 `python3 build.py` 重新构建
