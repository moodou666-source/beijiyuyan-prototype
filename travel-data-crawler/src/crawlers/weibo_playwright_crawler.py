"""
微博爬虫 - 使用 Playwright 模拟浏览器
绕过反爬机制
"""

import json
import re
import time
from typing import List, Dict, Any
from loguru import logger


class WeiboPlaywrightCrawler:
    """使用 Playwright 的微博爬虫"""
    
    def __init__(self):
        self.base_url = "https://m.weibo.cn"
        self.data = []
    
    def search(self, keyword: str, pages: int = 3) -> List[Dict[str, Any]]:
        """
        搜索微博内容
        
        Args:
            keyword: 搜索关键词
            pages: 页数
            
        Returns:
            微博列表
        """
        try:
            from playwright.sync_api import sync_playwright
            
            with sync_playwright() as p:
                # 启动浏览器
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(
                    user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15",
                    viewport={"width": 375, "height": 812},
                )
                
                page = context.new_page()
                
                results = []
                for page_num in range(1, pages + 1):
                    logger.info(f"搜索 '{keyword}' 第{page_num}页")
                    
                    # 访问搜索页面
                    search_url = f"https://m.weibo.cn/search?containerid=100103type%3D1%26q%3D{keyword}&page_type=searchall&page={page_num}"
                    page.goto(search_url, wait_until="networkidle")
                    
                    # 等待内容加载
                    time.sleep(3)
                    
                    # 获取页面内容
                    content = page.content()
                    
                    # 解析数据
                    posts = self._parse_page(content)
                    results.extend(posts)
                    
                    logger.info(f"第{page_num}页获取{len(posts)}条数据")
                
                browser.close()
                return results
                
        except ImportError:
            logger.error("请先安装 Playwright: pip install playwright")
            logger.error("然后运行: playwright install")
            return []
        except Exception as e:
            logger.error(f"搜索失败: {e}")
            return []
    
    def _parse_page(self, html: str) -> List[Dict[str, Any]]:
        """
        解析页面内容
        
        Args:
            html: 页面HTML
            
        Returns:
            解析后的数据
        """
        import re
        
        posts = []
        
        # 尝试从页面中提取JSON数据
        # 微博数据通常在 <script> 标签中
        scripts = re.findall(r'<script>window\.__INITIAL_STATE__=(.*?);</script>', html)
        
        if scripts:
            try:
                data = json.loads(scripts[0])
                cards = data.get("cards", [])
                
                for card in cards:
                    if card.get("card_type") != 9:
                        continue
                    
                    mblog = card.get("mblog", {})
                    if not mblog:
                        continue
                    
                    post = self._parse_mblog(mblog)
                    if post:
                        posts.append(post)
            except Exception as e:
                logger.error(f"解析JSON失败: {e}")
        
        return posts
    
    def _parse_mblog(self, mblog: Dict[str, Any]) -> Dict[str, Any]:
        """解析单条微博"""
        try:
            user = mblog.get("user", {})
            
            post = {
                "platform": "weibo",
                "post_id": str(mblog.get("id", "")),
                "user_id": str(user.get("id", "")),
                "username": user.get("screen_name", ""),
                "content": re.sub(r"<[^>]+>", "", mblog.get("text", "")),
                "images": [pic.get("large", {}).get("url", pic.get("url", "")) for pic in mblog.get("pics", [])],
                "created_at": mblog.get("created_at", ""),
                "stats": {
                    "reposts": mblog.get("reposts_count", 0),
                    "comments": mblog.get("comments_count", 0),
                    "attitudes": mblog.get("attitudes_count", 0),
                },
                "user_info": {
                    "followers": user.get("followers_count", 0),
                    "verified": user.get("verified", False),
                },
            }
            
            return post
        except Exception as e:
            logger.error(f"解析微博失败: {e}")
            return None
    
    def save_data(self, data: List[Dict[str, Any]], filename: str):
        """保存数据"""
        import os
        from datetime import datetime
        
        os.makedirs("data/raw", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = f"data/raw/{filename}_{timestamp}.json"
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"数据已保存: {filepath}")


if __name__ == "__main__":
    # 测试
    crawler = WeiboPlaywrightCrawler()
    results = crawler.search("南京旅游", pages=2)
    print(f"共获取 {len(results)} 条数据")
    
    if results:
        crawler.save_data(results, "weibo_test")
        print("数据已保存")
    else:
        print("未获取到数据")
        print("\n请确保已安装 Playwright:")
        print("1. pip install playwright")
        print("2. playwright install")
