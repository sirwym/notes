# 王老师的课堂笔记 — 开发规范

> **AI 修改动画/游戏前必读。** 任何新增或修改 HTML 文件，必须遵循以下规范。

---

## 一、导航栏（不需要）

动画和游戏页面**不需要导航栏**。用户通过浏览器后退按钮返回首页。

动画/游戏通常是全屏交互体验，导航栏会占用空间且干扰沉浸感。

---

## 二、Body 布局

动画/游戏页面通常全屏显示，body 样式：

| 场景 | 写法 |
|------|------|
| Canvas 全屏 | `body { margin: 0; overflow: hidden; height: 100vh; }` |
| 游戏容器居中 | `body { margin: 0; display: flex; height: 100vh; }` |

**不需要 margin-top 偏移（没有导航栏）。**

---

## 三、品牌色（必须）

| 用途 | 色值 | CSS 变量 |
|------|------|----------|
| 主色 | `#2563eb` | `--primary: #2563eb` |
| 主色深 | `#1d4ed8` | `--primary-dark: #1d4ed8` |

**禁止使用紫色**（`#8b5cf6`、`#7c3aed`）或其他非品牌色作为主色。

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
- **动画和游戏**：使用知识点名称（如 `取余与取模`、`条件嵌套`、`树的中心`、`输入输出流`）
- **C++ 模板**：使用 GESP 级别（`GESP1` ~ `GESP8`）
- ⚠️ 动画和游戏的 topic 和 tags 中**不要出现 GESP 等级标签**（如 `GESP1`、`GESP6`），只用知识点关键词

### 示例
```markdown
---
title: cin 数据传送带
category: animation
subtitle: 模拟 cin 输入流的工作方式，理解数据如何传入变量
tags: cin 输入 传送带 流
topic: 输入输出流
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

- [ ] 主色为 #2563eb（品牌蓝），无紫色
- [ ] 无 CDN 引用，全部使用本地 `../assets/` 资源
- [ ] 页面标题带 ` - 王老师的课堂笔记` 后缀
- [ ] 有对应的 `.meta.md` 元数据文件
- [ ] 无导航栏（用户用浏览器后退）
- [ ] body 无 margin-top 偏移，全屏页面用 `height: 100vh`
- [ ] 运行 `python3 build.py` 重新构建