"""
将爬虫数据转换为APP可用格式
"""

import json
import re
from collections import defaultdict


def convert_data():
    """转换数据为APP格式"""
    
    # 加载爬虫数据
    with open("travel-data-crawler/data/raw/jiangsu_all_cities_20260428_161623.json", "r", encoding="utf-8") as f:
        posts = json.load(f)
    
    print(f"加载了 {len(posts)} 条原始数据")
    
    # 按城市分类
    city_data = defaultdict(list)
    
    for post in posts:
        content = post.get("content", "")
        
        # 识别城市
        city = detect_city(content)
        if city:
            # 提取景点
            spots = extract_spots(content)
            
            # 计算热度
            hot_score = calculate_hot_score(post.get("stats", {}))
            
            # 构建数据
            item = {
                "id": hash(content) % 1000000,
                "username": post.get("username", ""),
                "content": content[:200] + "..." if len(content) > 200 else content,
                "full_content": content,
                "images": post.get("images", [])[:3],  # 最多3张图
                "time": post.get("time", ""),
                "source": post.get("source", ""),
                "stats": post.get("stats", {}),
                "hot_score": hot_score,
                "spots": spots,
                "city": city,
            }
            
            city_data[city].append(item)
    
    # 排序并取TOP
    result = {}
    for city, items in city_data.items():
        # 按热度排序
        items.sort(key=lambda x: x["hot_score"], reverse=True)
        result[city] = items[:20]  # 每个城市取TOP20
    
    # 保存
    output = {
        "update_time": "2026-04-28",
        "total_cities": len(result),
        "total_posts": sum(len(items) for items in result.values()),
        "cities": result,
    }
    
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
    
    # 将数据嵌入HTML
    data_json = json.dumps(output, ensure_ascii=False)
    
    # 找到插入点
    insert_point = "// 城市景点数据（包含详细信息）"
    if insert_point in html:
        # 替换数据
        new_data = f"""
// 真实采集的江苏旅游数据
const REAL_JIANGSU_DATA = {data_json};

// 城市景点数据（包含详细信息）
"""
        html = html.replace(insert_point, new_data)
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html)
        
        print(f"\n数据已整合到APP中！")
        print(f"覆盖城市: {len(result)} 个")
        print(f"总帖子数: {sum(len(items) for items in result.values())} 条")
        
        for city, items in result.items():
            print(f"  {city}: {len(items)} 条")
    else:
        print("未找到插入点，请检查HTML结构")


def detect_city(content):
    """检测内容中的城市"""
    cities = ["南京", "苏州", "扬州", "无锡", "镇江", "常州", 
              "南通", "泰州", "盐城", "连云港", "徐州", "淮安", "宿迁"]
    
    for city in cities:
        if city in content:
            return city
    
    return None


def extract_spots(content):
    """提取内容中的景点"""
    # 常见景点关键词
    spot_keywords = [
        "中山陵", "夫子庙", "总统府", "玄武湖", "鸡鸣寺",
        "拙政园", "虎丘", "平江路", "山塘街", "金鸡湖",
        "瘦西湖", "个园", "何园", "东关街",
        "鼋头渚", "灵山大佛", "太湖",
        "金山", "焦山", "北固山",
        "恐龙园", "天目湖",
        "狼山", "濠河",
        "溱湖", "凤城河",
        "丹顶鹤", "麋鹿",
        "花果山", "连岛",
        "云龙湖", "汉文化",
        "周恩来", "洪泽湖",
        "项王故里", "骆马湖",
    ]
    
    spots = []
    for spot in spot_keywords:
        if spot in content:
            spots.append(spot)
    
    return spots[:3]  # 最多3个景点


def calculate_hot_score(stats):
    """计算热度得分"""
    attitudes = stats.get("attitudes", 0)
    comments = stats.get("comments", 0)
    reposts = stats.get("reposts", 0)
    
    # 权重: 点赞(0.5) + 评论(0.3) + 转发(0.2)
    return attitudes * 0.5 + comments * 0.3 + reposts * 0.2


if __name__ == "__main__":
    convert_data()
