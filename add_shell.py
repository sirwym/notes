#!/usr/bin/env python3
"""
为 animations/ 和 games/ 下的 HTML 文件添加统一的导航栏和页脚
"""

import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 统一导航栏 HTML（固定在顶部，不占内容空间）
NAV_BAR = '''
<!-- 统一导航栏 -->
<nav style="position:fixed;top:0;left:0;right:0;z-index:9999;background:#fff;border-bottom:1px solid #e5e7eb;height:48px;display:flex;align-items:center;justify-content:space-between;padding:0 16px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif;">
    <a href="../index.html" style="display:flex;align-items:center;gap:6px;text-decoration:none;color:#6b7280;font-size:13px;transition:color 0.2s;" onmouseover="this.style.color='#2563eb'" onmouseout="this.style.color='#6b7280'">
        <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
        返回首页
    </a>
    <span style="font-size:12px;color:#9ca3af;">远明老师的课堂笔记</span>
</nav>
<div style="height:48px;"></div>
'''

# 统一页脚 HTML
FOOTER = '''
<!-- 统一页脚 -->
<footer style="text-align:center;padding:16px;font-size:12px;color:#9ca3af;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC',sans-serif;">
    <a href="../index.html" style="color:#9ca3af;text-decoration:none;">返回首页</a>
    <span style="margin:0 8px;">·</span>
    <span>远明老师的课堂笔记</span>
</footer>
'''

# 特殊文件配置（全屏/深色背景的文件不添加页脚，只加导航栏）
SPECIAL_FILES = {
    "08_3D 余数齿轮系统.html": {"no_footer": True, "dark_nav": True},
    "06_代码炼金术：写出判断逻辑.html": {"no_footer": True},
}

def add_shell_to_html(filepath):
    """为单个 HTML 文件添加导航栏和页脚"""
    filename = os.path.basename(filepath)
    config = SPECIAL_FILES.get(filename, {})
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 检查是否已经添加过（避免重复）
    if "统一导航栏" in content:
        print(f"  ⏭️  {filename} 已有导航栏，跳过")
        return
    
    # 生成导航栏（深色背景版本）
    nav = NAV_BAR
    if config.get("dark_nav"):
        nav = nav.replace('background:#fff;', 'background:rgba(10,17,40,0.9);')
        nav = nav.replace('border-bottom:1px solid #e5e7eb;', 'border-bottom:1px solid rgba(255,255,255,0.1);')
        nav = nav.replace('color:#6b7280;', 'color:rgba(255,255,255,0.7);')
        nav = nav.replace("this.style.color='#2563eb'", "this.style.color='#60a5fa'")
        nav = nav.replace("this.style.color='#6b7280'", "this.style.color='rgba(255,255,255,0.7)'")
        nav = nav.replace('color:#9ca3af;', 'color:rgba(255,255,255,0.5);')
    
    # 在 <body> 后插入导航栏
    # 处理各种 body 标签格式
    body_match = re.search(r'(<body[^>]*>)', content)
    if body_match:
        insert_pos = body_match.end()
        content = content[:insert_pos] + nav + content[insert_pos:]
    
    # 在 </body> 前插入页脚
    if not config.get("no_footer"):
        content = content.replace("</body>", FOOTER + "\n</body>")
    
    # 修改 title，加上站点名
    content = re.sub(
        r'<title>(.*?)</title>',
        lambda m: f'<title>{m.group(1)} - 远明老师的课堂笔记</title>',
        content
    )
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"  ✅ {filename}")

def main():
    print("🎨 为动画和游戏页面添加统一外壳...\n")
    
    for subdir in ["animations", "games"]:
        dir_path = os.path.join(BASE_DIR, subdir)
        if not os.path.isdir(dir_path):
            continue
        
        print(f"📁 {subdir}/")
        for f in sorted(os.listdir(dir_path)):
            if f.endswith(".html"):
                add_shell_to_html(os.path.join(dir_path, f))
        print()
    
    print("🎉 全部完成！")

if __name__ == "__main__":
    main()
