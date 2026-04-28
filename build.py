#!/usr/bin/env python3
"""
notes 项目构建脚本
1. 将 cpp/*.md 编译为 cpp/dist/*.html
2. 扫描 .meta.md 元数据 → 生成数据驱动的 index.html
"""

import os
import re
import sys
import glob
import json

# ===== 配置 =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 自动使用 .venv 中的依赖
VENV_SITE = os.path.join(BASE_DIR, ".venv", "lib")
if os.path.isdir(VENV_SITE):
    for d in os.listdir(VENV_SITE):
        site_path = os.path.join(VENV_SITE, d, "site-packages")
        if os.path.isdir(site_path):
            sys.path.insert(0, site_path)
            break

try:
    import markdown
except ImportError:
    print("❌ 缺少 markdown 库，请先运行：")
    print("   python3 -m venv .venv && source .venv/bin/activate && pip install markdown")
    sys.exit(1)

TEMPLATE_PATH = os.path.join(BASE_DIR, "template.html")
INDEX_TEMPLATE_PATH = os.path.join(BASE_DIR, "index_template.html")
CPP_DIR = os.path.join(BASE_DIR, "cpp")
DIST_DIR = os.path.join(CPP_DIR, "dist")

# ===== Frontmatter 解析 =====
def parse_frontmatter(text):
    """解析 Markdown 文件顶部的 YAML frontmatter"""
    if not text.startswith("---"):
        return {}, text
    
    end = text.find("---", 3)
    if end == -1:
        return {}, text
    
    fm_text = text[3:end].strip()
    body = text[end + 3:].strip()
    
    meta = {}
    for line in fm_text.split("\n"):
        if ":" in line:
            key, val = line.split(":", 1)
            meta[key.strip()] = val.strip()
    
    return meta, body

# ===== 标签渲染 =====
def render_tags_html(tags_str):
    """将标签字符串渲染为首页卡片的 HTML 标签"""
    tags = [t.strip() for t in tags_str.split() if t.strip()]
    html_parts = []
    
    difficulty_colors = {
        "入门": "bg-green-100 text-green-600",
        "普及-": "bg-yellow-100 text-yellow-700",
        "普及": "bg-yellow-100 text-yellow-700",
        "提高-": "bg-orange-100 text-orange-600",
        "提高": "bg-orange-100 text-orange-600",
        "提高+": "bg-red-100 text-red-600",
        "NOI": "bg-red-100 text-red-600",
    }
    
    for tag in tags:
        color = difficulty_colors.get(tag, "bg-gray-100 text-gray-500")
        html_parts.append(f'<span class="px-1.5 py-0.5 {color} text-xs rounded">{tag}</span>')
    
    return " ".join(html_parts)


def render_tags_detail(tags_str):
    """将标签字符串渲染为详情页的 HTML 标签"""
    tags = [t.strip() for t in tags_str.split() if t.strip()]
    html_parts = []
    
    difficulty_colors = {
        "入门": "tag-green",
        "普及-": "tag-yellow",
        "普及": "tag-yellow",
        "提高-": "tag-orange",
        "提高": "tag-orange",
        "提高+": "tag-red",
        "NOI": "tag-red",
    }
    
    for tag in tags:
        color_class = difficulty_colors.get(tag, "tag-entry")
        html_parts.append(f'<span class="px-2 py-1 {color_class} text-xs rounded-md">{tag}</span>')
    
    return "\n                ".join(html_parts)

# ===== 数学公式保护 =====
def protect_math(text):
    """在 Markdown 转换前，将 $...$ 和 $$...$$ 替换为占位符，防止被 Markdown 引擎破坏"""
    placeholders = {}
    counter = [0]
    
    def make_placeholder(match):
        key = f"MATHPLACEHOLDER{counter[0]}END"
        counter[0] += 1
        placeholders[key] = match.group(0)
        return key
    
    # 先处理 $$...$$（display math），再处理 $...$（inline math）
    # 顺序很重要，先匹配长的避免短匹配截断
    text = re.sub(r'\$\$(.+?)\$\$', make_placeholder, text, flags=re.DOTALL)
    text = re.sub(r'\$([^\$\n]+?)\$', make_placeholder, text)
    
    return text, placeholders

def restore_math(text, placeholders):
    """将占位符还原为原始数学公式"""
    for key, value in placeholders.items():
        text = text.replace(key, value)
    return text

# ===== iframe 短语法处理 =====
def process_iframe_shortcuts(text):
    """将 !!animation xxx.html!! 替换为完整 iframe 标签"""
    def replace_iframe(match):
        src = match.group(1).strip()
        if not src.startswith("../") and not src.startswith("http"):
            src = "../../animations/" + src
        return f'<iframe src="{src}" width="100%" height="450" frameborder="0" allowfullscreen></iframe>'
    
    text = re.sub(r'!!animation\s+(.+?)!!', replace_iframe, text)
    text = re.sub(r'!!game\s+(.+?)!!', 
                  lambda m: f'<iframe src="../../games/{m.group(1).strip()}" width="100%" height="450" frameborder="0" allowfullscreen></iframe>',
                  text)
    return text

# ===== 构建 C++ 模板 =====
def build_cpp_file(md_path, template_html):
    """将 .md 文件构建为 .html"""
    with open(md_path, "r", encoding="utf-8") as f:
        text = f.read()
    
    meta, body = parse_frontmatter(text)
    
    title = meta.get("title", os.path.splitext(os.path.basename(md_path))[0])
    heading = meta.get("heading", title)
    subtitle = meta.get("subtitle", "")
    tags_str = meta.get("tags", "")
    tags_html = render_tags_detail(tags_str)
    
    body = process_iframe_shortcuts(body)
    
    # 保护数学公式，避免被 Markdown 引擎破坏
    body, math_placeholders = protect_math(body)
    
    md = markdown.Markdown(extensions=["fenced_code", "tables", "attr_list"])
    content_html = md.convert(body)
    
    # 还原数学公式
    content_html = restore_math(content_html, math_placeholders)
    
    output = template_html
    output = output.replace("{{title}}", heading)
    output = output.replace("{{heading}}", heading)
    output = output.replace("{{subtitle}}", subtitle)
    output = output.replace("{{tags_html}}", tags_html)
    output = output.replace("{{content}}", content_html)
    
    basename = os.path.splitext(os.path.basename(md_path))[0]
    out_path = os.path.join(DIST_DIR, basename + ".html")
    
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(output)
    
    print(f"  ✅ {basename}.md → dist/{basename}.html")
    return {
        "title": title,
        "subtitle": subtitle,
        "category": "cpp",
        "tags": tags_str,
        "topic": meta.get("topic", ""),
        "href": f"cpp/dist/{basename}.html",
    }

# ===== 扫描 .meta.md 元数据 =====
def scan_meta_files():
    """扫描 animations/ 和 games/ 下的 .meta.md 文件"""
    items = []
    
    for subdir in ["animations", "games", "ai"]:
        dir_path = os.path.join(BASE_DIR, subdir)
        if not os.path.isdir(dir_path):
            continue
        
        meta_files = sorted(glob.glob(os.path.join(dir_path, "*.meta.md")))
        for meta_path in meta_files:
            with open(meta_path, "r", encoding="utf-8") as f:
                text = f.read()
            
            meta, _ = parse_frontmatter(text)
            
            # 推算对应的 HTML 文件路径
            basename = os.path.basename(meta_path).replace(".meta.md", ".html")
            href = f"{subdir}/{basename}"
            
            # 检查 HTML 文件是否真实存在
            html_path = os.path.join(dir_path, basename)
            if not os.path.isfile(html_path):
                print(f"  ⚠️  {basename} 不存在，跳过 {meta_path}")
                continue
            
            items.append({
                "title": meta.get("title", basename),
                "subtitle": meta.get("subtitle", ""),
                "category": meta.get("category", subdir.rstrip("s")),  # animation or game
                "tags": meta.get("tags", ""),
                "topic": meta.get("topic", ""),
                "href": href,
            })
    
    return items

# ===== 生成首页卡片 HTML =====
def generate_card_html(item):
    """根据数据生成单个卡片 HTML"""
    category = item["category"]
    
    # 分类标签样式
    tag_classes = {
        "animation": ("tag-animation", "算法动画"),
        "game": ("tag-game", "知识点游戏"),
        "cpp": ("tag-cpp", "C++ 模板"),
        "ai": ("tag-ai", "AI 实验室"),
    }
    tag_class, tag_label = tag_classes.get(category, ("tag-entry", category))
    
    tags_html = render_tags_html(item["tags"])
    
    return f'''            <a href="{item['href']}"
               class="note-card p-5 bg-white rounded-xl border border-gray-200 group"
               data-category="{category}" data-topic="{item['topic']}" data-tags="{item['tags']}">
                <div class="flex items-center gap-2 mb-3">
                    <span class="px-2 py-0.5 {tag_class} text-xs font-semibold rounded">{tag_label}</span>
                </div>
                <h3 class="text-base font-semibold text-gray-900 group-hover:text-brand-600 transition-colors leading-snug">{item['title']}</h3>
                <p class="text-sm text-gray-500 mt-1.5">{item['subtitle']}</p>
                <div class="flex items-center gap-2 mt-3 flex-wrap">
                    {tags_html}
                </div>
            </a>'''

# ===== 生成知识点标签筛选栏 =====
def generate_topic_filters(all_items):
    """收集所有知识点并生成筛选按钮 HTML"""
    topics = []
    seen = set()
    for item in all_items:
        t = item.get("topic", "")
        if t and t not in seen:
            topics.append(t)
            seen.add(t)
    
    buttons = '<button class="topic-btn px-3 py-1.5 text-xs font-medium border border-gray-200 rounded-lg text-gray-600 hover:border-brand-300 active" data-topic="all" onclick="switchTopic(\'all\')">全部</button>\n            '
    for t in topics:
        buttons += f'<button class="topic-btn px-3 py-1.5 text-xs font-medium border border-gray-200 rounded-lg text-gray-600 hover:border-brand-300" data-topic="{t}" onclick="switchTopic(\'{t}\')">{t}</button>\n            '
    
    return buttons, topics

# ===== 生成首页 =====
def build_index(all_items):
    """根据数据生成 index.html"""
    # 读取首页模板
    if not os.path.isfile(INDEX_TEMPLATE_PATH):
        print("  ⚠️  index_template.html 不存在，跳过首页生成")
        return
    
    with open(INDEX_TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template = f.read()
    
    # 生成卡片
    cards_html = "\n\n".join(generate_card_html(item) for item in all_items)
    
    # 生成知识点筛选
    topic_buttons, topics = generate_topic_filters(all_items)
    
    # 生成知识点列表（JS 用）
    topics_json = json.dumps(topics, ensure_ascii=False)
    
    # 替换占位符
    output = template
    output = output.replace("{{cards}}", cards_html)
    output = output.replace("{{topic_buttons}}", topic_buttons)
    output = output.replace("{{topics_json}}", topics_json)
    
    # 写入
    out_path = os.path.join(BASE_DIR, "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(output)
    
    print(f"  ✅ 首页 index.html 已生成（{len(all_items)} 个内容卡片）")

# ===== 主流程 =====
def main():
    print("🔨 开始构建 notes 项目...\n")
    
    all_items = []
    
    # ---- 第一步：扫描 .meta.md 元数据 ----
    print("📁 扫描 animations/、games/、ai/ 的元数据...")
    meta_items = scan_meta_files()
    all_items.extend(meta_items)
    print(f"  找到 {len(meta_items)} 个动画/游戏\n")
    
    # ---- 第二步：构建 C++ 模板 ----
    print("📁 构建 C++ 模板...")
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template_html = f.read()
    
    os.makedirs(DIST_DIR, exist_ok=True)
    
    md_files = sorted(glob.glob(os.path.join(CPP_DIR, "*.md")))
    for md_path in md_files:
        item = build_cpp_file(md_path, template_html)
        all_items.append(item)
    
    print(f"  找到 {len(md_files)} 个 Markdown 文件\n")
    
    # ---- 第三步：生成首页 ----
    print("📁 生成首页...")
    build_index(all_items)
    
    print(f"\n🎉 构建完成！共 {len(all_items)} 个内容项")

if __name__ == "__main__":
    main()
