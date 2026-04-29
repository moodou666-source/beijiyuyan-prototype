from PIL import Image, ImageDraw, ImageFont
import os

# 创建输出目录
output_dir = "/Users/jiyi/.openclaw/workspace/memory/projects/beijiyuyan_ui/mockups"
os.makedirs(output_dir, exist_ok=True)

# 颜色定义
COLORS = {
    'primary': '#FF6B35',
    'primary_dark': '#E85A2D',
    'primary_light': '#FFF5F0',
    'dark': '#1A1A2E',
    'dark_light': '#252540',
    'gold': '#FFD93D',
    'bg': '#F7F9FC',
    'white': '#FFFFFF',
    'text': '#2D3142',
    'text_secondary': '#8E92BC',
    'border': '#E8E8E8',
    'gray': '#F5F5F5'
}

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# 字体设置 - 使用系统默认字体
def get_font(size, bold=False):
    """获取字体"""
    # 尝试中文字体
    font_paths = [
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/ArialHB.ttc",
    ]
    
    for path in font_paths:
        try:
            if bold and "STHeiti" in path:
                return ImageFont.truetype(path, size, index=0)
            return ImageFont.truetype(path, size)
        except:
            continue
    
    return ImageFont.load_default()

def create_gradient(width, height, color1, color2, direction='diagonal'):
    """创建渐变背景"""
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    c1 = hex_to_rgb(color1)
    c2 = hex_to_rgb(color2)
    
    for y in range(height):
        for x in range(width):
            if direction == 'diagonal':
                ratio = (x + y) / (width + height)
            else:
                ratio = y / height
            r = int(c1[0] + (c2[0] - c1[0]) * ratio)
            g = int(c1[1] + (c2[1] - c1[1]) * ratio)
            b = int(c1[2] + (c2[2] - c1[2]) * ratio)
            draw.point((x, y), fill=(r, g, b))
    return img

def draw_rounded_rect(draw, xy, radius, fill, outline=None, width=1):
    """绘制圆角矩形"""
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

def create_splash_screen():
    """创建启动页"""
    width, height = 375, 812  # iPhone X 尺寸
    
    # 创建渐变背景
    img = create_gradient(width, height, COLORS['dark'], COLORS['primary'], 'diagonal')
    draw = ImageDraw.Draw(img)
    
    # 绘制地图轮廓线（装饰）
    map_lines = [
        (50, 600, 150, 580, 250, 620, 320, 590),
        (80, 650, 180, 630, 280, 660, 350, 640),
    ]
    for line in map_lines:
        points = list(zip(line[::2], line[1::2]))
        draw.line(points, fill=(*hex_to_rgb(COLORS['white']), 30), width=1)
    
    # 绘制 Logo（雨燕 + 指南针简化图形）
    center_x, center_y = width // 2, height // 2 - 80
    
    # 外圆
    draw.ellipse([center_x-60, center_y-60, center_x+60, center_y+60], 
                 outline=COLORS['white'], width=3)
    
    # 指南针指针
    draw.polygon([(center_x, center_y-45), (center_x-8, center_y+10), (center_x+8, center_y+10)], 
                 fill=COLORS['gold'])
    draw.polygon([(center_x, center_y+45), (center_x-8, center_y-10), (center_x+8, center_y-10)], 
                 fill=COLORS['white'])
    
    # 中心点
    draw.ellipse([center_x-8, center_y-8, center_x+8, center_y+8], fill=COLORS['primary'])
    
    # 文字
    font_title = get_font(28, bold=True)
    font_slogan = get_font(16)
    font_version = get_font(12)
    
    # App 名称
    draw.text((width//2, center_y + 100), "北极雨燕", fill=hex_to_rgb(COLORS['white']), 
              font=font_title, anchor='mm')
    
    # Slogan
    draw.text((width//2, center_y + 145), "让每一次出发，都有最好的路线", 
              fill=(*hex_to_rgb(COLORS['white']), 200), font=font_slogan, anchor='mm')
    
    # 版本号
    draw.text((width//2, height - 80), "v1.0.0", 
              fill=(*hex_to_rgb(COLORS['white']), 100), font=font_version, anchor='mm')
    draw.text((width//2, height - 60), "© 2026 北极雨燕", 
              fill=(*hex_to_rgb(COLORS['white']), 100), font=font_version, anchor='mm')
    
    img.save(f"{output_dir}/01_splash.png", "PNG")
    print("✅ 启动页已生成")
    return img

def create_home_screen():
    """创建首页"""
    width, height = 375, 812
    
    # 白色背景
    img = Image.new('RGB', (width, height), hex_to_rgb(COLORS['bg']))
    draw = ImageDraw.Draw(img)
    
    # 状态栏背景
    draw.rectangle([0, 0, width, 44], fill=hex_to_rgb(COLORS['white']))
    
    # 顶部栏
    draw.rectangle([0, 44, width, 88], fill=hex_to_rgb(COLORS['white']))
    font_location = get_font(16, bold=True)
    font_search = get_font(14)
    
    # 定位按钮
    draw.text((20, 66), "📍 北京市 ▾", fill=hex_to_rgb(COLORS['text']), font=font_location, anchor='lm')
    
    # 搜索图标
    draw.text((width-40, 66), "🔍", fill=hex_to_rgb(COLORS['text_secondary']), font=font_search, anchor='lm')
    
    # 地图区域（简化）
    map_top = 100
    map_height = 380
    draw_rounded_rect(draw, [16, map_top, width-16, map_top + map_height], 16, COLORS['white'])
    
    # 地图背景色
    draw.rounded_rectangle([16, map_top, width-16, map_top + map_height], radius=16, 
                           fill=hex_to_rgb('#E8F4F8'))
    
    # 简化道路线条
    road_color = hex_to_rgb('#FFFFFF')
    draw.line([(50, 250), (150, 200), (250, 280), (340, 240)], fill=road_color, width=8)
    draw.line([(100, 350), (200, 320), (300, 380)], fill=road_color, width=6)
    
    # 景点标记点
    markers = [(150, 200), (250, 280), (200, 320)]
    for mx, my in markers:
        # 外圈
        draw.ellipse([mx-12, my-12, mx+12, my+12], fill=hex_to_rgb(COLORS['primary']))
        # 内圈
        draw.ellipse([mx-6, my-6, mx+6, my+6], fill=hex_to_rgb(COLORS['white']))
    
    # 标签切换
    tab_y = map_top + map_height + 16
    tabs = ["推荐路线", "附近景点", "摄影点"]
    tab_width = (width - 32) // 3
    for i, tab in enumerate(tabs):
        x = 16 + i * tab_width
        if i == 0:
            draw_rounded_rect(draw, [x, tab_y, x + tab_width - 8, tab_y + 32], 16, COLORS['primary'])
            draw.text((x + tab_width//2 - 4, tab_y + 16), tab, fill=hex_to_rgb(COLORS['white']), 
                     font=get_font(13), anchor='mm')
        else:
            draw_rounded_rect(draw, [x, tab_y, x + tab_width - 8, tab_y + 32], 16, COLORS['gray'])
            draw.text((x + tab_width//2 - 4, tab_y + 16), tab, fill=hex_to_rgb(COLORS['text_secondary']), 
                     font=get_font(13), anchor='mm')
    
    # 路线卡片
    card_y = tab_y + 56
    cards = [
        ("🏔️ 川西小环线 3日游", "⭐ 4.9  📍 成都出发", "💰 ¥1,200/人  🚗 自驾"),
        ("🌊 洱海环湖 2日游", "⭐ 4.8  📍 大理出发", "💰 ¥800/人  🚗 自驾"),
    ]
    
    for i, (title, info, price) in enumerate(cards):
        y = card_y + i * 140
        # 卡片背景
        draw_rounded_rect(draw, [16, y, width-16, y + 128], 16, COLORS['white'])
        
        # 图片区域（左侧）
        draw.rounded_rectangle([16, y, 16 + 140, y + 128], radius=16, fill=hex_to_rgb('#D4E5F7'))
        # 图片占位符
        draw.text((16 + 70, y + 64), "🏔️" if i == 0 else "🌊", fill=hex_to_rgb(COLORS['text_secondary']), 
                 font=get_font(32), anchor='mm')
        
        # 文字区域
        text_x = 16 + 140 + 16
        draw.text((text_x, y + 24), title, fill=hex_to_rgb(COLORS['text']), font=get_font(15, bold=True), anchor='lm')
        draw.text((text_x, y + 56), info, fill=hex_to_rgb(COLORS['text_secondary']), font=get_font(12), anchor='lm')
        draw.text((text_x, y + 88), price, fill=hex_to_rgb(COLORS['primary']), font=get_font(13, bold=True), anchor='lm')
    
    # 底部导航栏
    nav_y = height - 83
    draw.rectangle([0, nav_y, width, height], fill=hex_to_rgb(COLORS['white']))
    draw.line([(0, nav_y), (width, nav_y)], fill=hex_to_rgb(COLORS['border']), width=1)
    
    nav_items = [("🗺️", "探索", True), ("📝", "规划", False), ("📷", "足迹", False), ("👤", "我的", False)]
    nav_width = width // 4
    for i, (icon, label, active) in enumerate(nav_items):
        x = i * nav_width + nav_width // 2
        color = COLORS['primary'] if active else COLORS['text_secondary']
        draw.text((x, nav_y + 20), icon, fill=hex_to_rgb(color), font=get_font(20), anchor='mm')
        draw.text((x, nav_y + 44), label, fill=hex_to_rgb(color), font=get_font(10), anchor='mm')
    
    img.save(f"{output_dir}/02_home.png", "PNG")
    print("✅ 首页已生成")
    return img

def create_plan_screen():
    """创建路线规划页"""
    width, height = 375, 812
    
    img = Image.new('RGB', (width, height), hex_to_rgb(COLORS['bg']))
    draw = ImageDraw.Draw(img)
    
    # 顶部栏
    draw.rectangle([0, 0, width, 88], fill=hex_to_rgb(COLORS['white']))
    draw.text((20, 66), "← 路线规划", fill=hex_to_rgb(COLORS['text']), font=get_font(16, bold=True), anchor='lm')
    draw.text((width-20, 66), "保存", fill=hex_to_rgb(COLORS['primary']), font=get_font(14), anchor='rm')
    
    # 步骤指示器
    steps = [("选择时间", True), ("目的地", False), ("偏好", False), ("生成", False)]
    step_y = 110
    for i, (label, active) in enumerate(steps):
        x = 30 + i * 85
        # 圆圈
        color = COLORS['primary'] if active else COLORS['text_secondary']
        draw.ellipse([x-12, step_y-12, x+12, step_y+12], fill=hex_to_rgb(color))
        draw.text((x, step_y), str(i+1), fill=hex_to_rgb(COLORS['white']), font=get_font(12, bold=True), anchor='mm')
        # 标签
        draw.text((x, step_y + 28), label, fill=hex_to_rgb(color), font=get_font(11), anchor='mm')
        # 连接线
        if i < len(steps) - 1:
            draw.line([(x+12, step_y), (x+73, step_y)], fill=hex_to_rgb(COLORS['border']), width=2)
    
    # 步骤 1: 选择时间
    content_y = 180
    draw.text((20, content_y), "第 1 步: 选择时间", fill=hex_to_rgb(COLORS['text']), font=get_font(18, bold=True), anchor='lm')
    
    # 时间卡片
    card_y = content_y + 40
    draw_rounded_rect(draw, [16, card_y, width-16, card_y + 140], 12, COLORS['white'])
    
    # 出发日期
    draw.text((40, card_y + 30), "📅 出发日期", fill=hex_to_rgb(COLORS['text_secondary']), font=get_font(14), anchor='lm')
    draw.text((40, card_y + 65), "4月28日", fill=hex_to_rgb(COLORS['text']), font=get_font(20, bold=True), anchor='lm')
    draw.text((40, card_y + 95), "周三", fill=hex_to_rgb(COLORS['text_secondary']), font=get_font(13), anchor='lm')
    
    # 分隔线
    draw.line([(width//2, card_y + 20), (width//2, card_y + 120)], fill=hex_to_rgb(COLORS['border']), width=1)
    
    # 返回日期
    draw.text((width//2 + 24, card_y + 30), "📅 返回日期", fill=hex_to_rgb(COLORS['text_secondary']), font=get_font(14), anchor='lm')
    draw.text((width//2 + 24, card_y + 65), "5月1日", fill=hex_to_rgb(COLORS['text']), font=get_font(20, bold=True), anchor='lm')
    draw.text((width//2 + 24, card_y + 95), "周六", fill=hex_to_rgb(COLORS['text_secondary']), font=get_font(13), anchor='lm')
    
    # 共几天
    draw.text((width//2, card_y + 155), "共 4 天", fill=hex_to_rgb(COLORS['primary']), font=get_font(16, bold=True), anchor='mm')
    
    # 步骤 2: 目的地
    dest_y = card_y + 190
    draw.text((20, dest_y), "第 2 步: 选择目的地", fill=hex_to_rgb(COLORS['text']), font=get_font(18, bold=True), anchor='lm')
    
    # 搜索框
    search_y = dest_y + 40
    draw_rounded_rect(draw, [16, search_y, width-16, search_y + 48], 24, COLORS['gray'])
    draw.text((40, search_y + 24), "🔍 搜索目的地...", fill=hex_to_rgb(COLORS['text_secondary']), font=get_font(14), anchor='lm')
    
    # 热门标签
    tags_y = search_y + 70
    tags = ["川西", "云南", "新疆", "西藏", "青海"]
    tag_x = 16
    for tag in tags:
        tag_width = len(tag) * 14 + 24
        draw_rounded_rect(draw, [tag_x, tags_y, tag_x + tag_width, tags_y + 32], 16, COLORS['primary_light'])
        draw.text((tag_x + tag_width//2, tags_y + 16), tag, fill=hex_to_rgb(COLORS['primary']), font=get_font(13), anchor='mm')
        tag_x += tag_width + 8
    
    # 步骤 3: 旅行偏好
    pref_y = tags_y + 70
    draw.text((20, pref_y), "第 3 步: 旅行偏好", fill=hex_to_rgb(COLORS['text']), font=get_font(18, bold=True), anchor='lm')
    
    # 偏好选项
    prefs = [("📸", "摄影优先"), ("🍜", "美食探索"), ("🏛️", "人文历史"), ("🏔️", "自然风光"), ("🏖️", "休闲度假")]
    pref_y += 40
    for i, (icon, label) in enumerate(prefs):
        row = i // 2
        col = i % 2
        x = 16 + col * ((width - 48) // 2 + 16)
        y = pref_y + row * 70
        w = (width - 48) // 2
        
        draw_rounded_rect(draw, [x, y, x + w, y + 60], 12, COLORS['white'])
        draw.text((x + 20, y + 30), icon, fill=hex_to_rgb(COLORS['text']), font=get_font(20), anchor='lm')
        draw.text((x + 50, y + 30), label, fill=hex_to_rgb(COLORS['text']), font=get_font(14), anchor='lm')
    
    # 生成按钮
    btn_y = height - 120
    draw_rounded_rect(draw, [32, btn_y, width-32, btn_y + 52], 26, COLORS['primary'])
    # 渐变效果模拟
    for i in range(52):
        ratio = i / 52
        r = int(255 + (255 - 255) * ratio)
        g = int(107 + (143 - 107) * ratio)
        b = int(53 + (90 - 53) * ratio)
        draw.line([(32, btn_y + i), (width-32, btn_y + i)], fill=(r, g, b))
    
    draw.text((width//2, btn_y + 26), "🚀 生成路线", fill=hex_to_rgb(COLORS['white']), font=get_font(16, bold=True), anchor='mm')
    
    img.save(f"{output_dir}/03_plan.png", "PNG")
    print("✅ 路线规划页已生成")
    return img

def create_footprint_screen():
    """创建足迹页"""
    width, height = 375, 812
    
    img = Image.new('RGB', (width, height), hex_to_rgb(COLORS['bg']))
    draw = ImageDraw.Draw(img)
    
    # 顶部栏
    draw.rectangle([0, 0, width, 88], fill=hex_to_rgb(COLORS['white']))
    draw.text((20, 66), "我的足迹", fill=hex_to_rgb(COLORS['text']), font=get_font(18, bold=True), anchor='lm')
    draw.text((width-20, 66), "⚙️", fill=hex_to_rgb(COLORS['text_secondary']), font=get_font(18), anchor='rm')
    
    # 照片地图区域
    map_y = 100
    map_height = 300
    draw_rounded_rect(draw, [16, map_y, width-16, map_y + map_height], 16, COLORS['dark'])
    
    # 简化地图背景
    draw.rounded_rectangle([16, map_y, width-16, map_y + map_height], radius=16, fill=hex_to_rgb(COLORS['dark_light']))
    
    # 照片标记点
    photo_markers = [
        (100, 200, "🏔️"),
        (200, 250, "🌊"),
        (280, 180, "🌅"),
        (150, 320, "🌲"),
    ]
    for mx, my, emoji in photo_markers:
        # 外圈
        draw.ellipse([mx-18, my-18, mx+18, my+18], fill=hex_to_rgb(COLORS['white']))
        # 内圈照片
        draw.ellipse([mx-15, my-15, mx+15, my+15], fill=hex_to_rgb(COLORS['gray']))
        draw.text((mx, my), emoji, fill=hex_to_rgb(COLORS['text']), font=get_font(14), anchor='mm')
    
    # 筛选标签
    tab_y = map_y + map_height + 16
    tabs = [("全部", True), ("公开", False), ("私密", False)]
    tab_x = 16
    for label, active in tabs:
        w = 60
        if active:
            draw_rounded_rect(draw, [tab_x, tab_y, tab_x + w, tab_y + 32], 16, COLORS['primary'])
            draw.text((tab_x + w//2, tab_y + 16), label, fill=hex_to_rgb(COLORS['white']), font=get_font(13), anchor='mm')
        else:
            draw_rounded_rect(draw, [tab_x, tab_y, tab_x + w, tab_y + 32], 16, COLORS['gray'])
            draw.text((tab_x + w//2, tab_y + 16), label, fill=hex_to_rgb(COLORS['text_secondary']), font=get_font(13), anchor='mm')
        tab_x += w + 8
    
    # 照片卡片
    card_y = tab_y + 56
    photos = [
        ("🏔️", "四姑娘山日出", "2026.04.15", "234", "56"),
        ("🌊", "洱海星空", "2026.03.20", "567", "128"),
    ]
    
    for i, (emoji, title, date, views, likes) in enumerate(photos):
        y = card_y + i * 200
        # 卡片背景
        draw_rounded_rect(draw, [16, y, width-16, y + 188], 16, COLORS['white'])
        
        # 图片区域
        draw.rounded_rectangle([16, y, width-16, y + 120], radius=16, fill=hex_to_rgb('#D4E5F7'))
        draw.text((width//2, y + 60), emoji, fill=hex_to_rgb(COLORS['text_secondary']), font=get_font(40), anchor='mm')
        
        # 信息
        draw.text((32, y + 145), title, fill=hex_to_rgb(COLORS['text']), font=get_font(15, bold=True), anchor='lm')
        draw.text((32, y + 168), f"🗓️ {date}", fill=hex_to_rgb(COLORS['text_secondary']), font=get_font(12), anchor='lm')
        draw.text((width-32, y + 168), f"👁️ {views}  ❤️ {likes}", fill=hex_to_rgb(COLORS['text_secondary']), font=get_font(12), anchor='rm')
    
    # 底部导航
    nav_y = height - 83
    draw.rectangle([0, nav_y, width, height], fill=hex_to_rgb(COLORS['white']))
    draw.line([(0, nav_y), (width, nav_y)], fill=hex_to_rgb(COLORS['border']), width=1)
    
    nav_items = [("🗺️", "探索", False), ("📝", "规划", False), ("📷", "足迹", True), ("👤", "我的", False)]
    nav_width = width // 4
    for i, (icon, label, active) in enumerate(nav_items):
        x = i * nav_width + nav_width // 2
        color = COLORS['primary'] if active else COLORS['text_secondary']
        draw.text((x, nav_y + 20), icon, fill=hex_to_rgb(color), font=get_font(20), anchor='mm')
        draw.text((x, nav_y + 44), label, fill=hex_to_rgb(color), font=get_font(10), anchor='mm')
    
    img.save(f"{output_dir}/04_footprint.png", "PNG")
    print("✅ 足迹页已生成")
    return img

def create_profile_screen():
    """创建个人中心页"""
    width, height = 375, 812
    
    img = Image.new('RGB', (width, height), hex_to_rgb(COLORS['bg']))
    draw = ImageDraw.Draw(img)
    
    # 用户信息卡片（橙色渐变）
    card_height = 220
    for y in range(card_height):
        ratio = y / card_height
        r = int(255 + (26 - 255) * ratio * 0.3)
        g = int(107 + (26 - 107) * ratio * 0.3)
        b = int(53 + (46 - 53) * ratio * 0.3)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # 头像
    avatar_y = 80
    draw.ellipse([width//2-40, avatar_y-40, width//2+40, avatar_y+40], fill=hex_to_rgb(COLORS['white']))
    draw.text((width//2, avatar_y), "👤", fill=hex_to_rgb(COLORS['text_secondary']), font=get_font(32), anchor='mm')
    
    # 用户名
    draw.text((width//2, avatar_y + 60), "北极雨燕用户", fill=hex_to_rgb(COLORS['white']), font=get_font(18, bold=True), anchor='mm')
    draw.text((width//2, avatar_y + 88), "📍 北京", fill=(*hex_to_rgb(COLORS['white']), 200), font=get_font(13), anchor='mm')
    
    # 数据统计
    stats_y = avatar_y + 120
    stats = [("12,580km", "已行驶"), ("186", "照片")]
    stat_width = width // 2
    for i, (value, label) in enumerate(stats):
        x = i * stat_width + stat_width // 2
        draw.text((x, stats_y), value, fill=hex_to_rgb(COLORS['white']), font=get_font(16, bold=True), anchor='mm')
        draw.text((x, stats_y + 24), label, fill=(*hex_to_rgb(COLORS['white']), 200), font=get_font(12), anchor='mm')
    
    # 数据概览卡片
    overview_y = card_height + 20
    draw_rounded_rect(draw, [16, overview_y, width-16, overview_y + 100], 12, COLORS['white'])
    
    stats2 = [("28", "次旅行"), ("15", "个城市"), ("8", "个省份")]
    stat2_width = (width - 32) // 3
    for i, (value, label) in enumerate(stats2):
        x = 16 + i * stat2_width + stat2_width // 2
        draw.text((x, overview_y + 35), value, fill=hex_to_rgb(COLORS['primary']), font=get_font(22, bold=True), anchor='mm')
        draw.text((x, overview_y + 65), label, fill=hex_to_rgb(COLORS['text_secondary']), font=get_font(12), anchor='mm')
        if i < 2:
            draw.line([(16 + (i+1) * stat2_width, overview_y + 20), (16 + (i+1) * stat2_width, overview_y + 80)], 
                     fill=hex_to_rgb(COLORS['border']), width=1)
    
    # 功能列表
    menu_y = overview_y + 120
    menus = [
        ("🗺️", "我的路线"),
        ("📷", "我的照片"),
        ("⭐", "收藏景点"),
        ("🎯", "旅行偏好"),
    ]
    
    draw_rounded_rect(draw, [16, menu_y, width-16, menu_y + len(menus) * 56], 12, COLORS['white'])
    
    for i, (icon, label) in enumerate(menus):
        y = menu_y + i * 56
        if i > 0:
            draw.line([(32, y), (width-32, y)], fill=hex_to_rgb(COLORS['border']), width=1)
        
        draw.text((40, y + 28), icon, fill=hex_to_rgb(COLORS['primary']), font=get_font(18), anchor='lm')
        draw.text((72, y + 28), label, fill=hex_to_rgb(COLORS['text']), font=get_font(15), anchor='lm')
        draw.text((width-32, y + 28), ">", fill=hex_to_rgb(COLORS['text_secondary']), font=get_font(14), anchor='rm')
    
    # 设置列表
    setting_y = menu_y + len(menus) * 56 + 20
    settings = [
        ("⚙️", "设置"),
        ("❓", "帮助与反馈"),
        ("👥", "邀请好友"),
    ]
    
    draw_rounded_rect(draw, [16, setting_y, width-16, setting_y + len(settings) * 56], 12, COLORS['white'])
    
    for i, (icon, label) in enumerate(settings):
        y = setting_y + i * 56
        if i > 0:
            draw.line([(32, y), (width-32, y)], fill=hex_to_rgb(COLORS['border']), width=1)
        
        draw.text((40, y + 28), icon, fill=hex_to_rgb(COLORS['primary']), font=get_font(18), anchor='lm')
        draw.text((72, y + 28), label, fill=hex_to_rgb(COLORS['text']), font=get_font(15), anchor='lm')
        draw.text((width-32, y + 28), ">", fill=hex_to_rgb(COLORS['text_secondary']), font=get_font(14), anchor='rm')
    
    img.save(f"{output_dir}/05_profile.png", "PNG")
    print("✅ 个人中心页已生成")
    return img

def create_logo():
    """创建 Logo"""
    size = 512
    img = Image.new('RGB', (size, size), hex_to_rgb(COLORS['white']))
    draw = ImageDraw.Draw(img)
    
    center = size // 2
    
    # 外圆
    draw.ellipse([center-200, center-200, center+200, center+200], 
                 outline=hex_to_rgb(COLORS['primary']), width=8)
    
    # 内圆
    draw.ellipse([center-160, center-160, center+160, center+160], 
                 outline=hex_to_rgb(COLORS['primary_light']), width=4)
    
    # 指南针指针 - 北（金色）
    draw.polygon([(center, center-140), (center-20, center+20), (center+20, center+20)], 
                 fill=hex_to_rgb(COLORS['gold']))
    
    # 指南针指针 - 南（橙色）
    draw.polygon([(center, center+140), (center-20, center-20), (center+20, center-20)], 
                 fill=hex_to_rgb(COLORS['primary']))
    
    # 中心圆
    draw.ellipse([center-30, center-30, center+30, center+30], fill=hex_to_rgb(COLORS['white']))
    draw.ellipse([center-20, center-20, center+20, center+20], fill=hex_to_rgb(COLORS['dark']))
    
    # 雨燕简化图形（上方）
    # 左翼
    draw.polygon([(center-80, center-80), (center-20, center-100), (center-40, center-60)], 
                 fill=hex_to_rgb(COLORS['primary']))
    # 右翼
    draw.polygon([(center+80, center-80), (center+20, center-100), (center+40, center-60)], 
                 fill=hex_to_rgb(COLORS['primary']))
    # 身体
    draw.polygon([(center, center-120), (center-15, center-60), (center+15, center-60)], 
                 fill=hex_to_rgb(COLORS['dark']))
    
    img.save(f"{output_dir}/logo.png", "PNG")
    print("✅ Logo 已生成")
    return img

# 生成所有设计稿
if __name__ == "__main__":
    print("🎨 开始生成北极雨燕 UI 设计稿...\n")
    
    create_logo()
    create_splash_screen()
    create_home_screen()
    create_plan_screen()
    create_footprint_screen()
    create_profile_screen()
    
    print(f"\n✅ 所有设计稿已生成到: {output_dir}")
    print("\n文件列表:")
    for f in sorted(os.listdir(output_dir)):
        print(f"  - {f}")
