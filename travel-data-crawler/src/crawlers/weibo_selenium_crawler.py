"""
微博爬虫 - 使用 Selenium + 真实Cookie
"""

import json
import re
import time
from typing import List, Dict, Any
from loguru import logger


class WeiboSeleniumCrawler:
    """使用 Selenium 的微博爬虫"""
    
    def __init__(self, cookie: str = None):
        self.base_url = "https://m.weibo.cn"
        self.cookie = cookie
        self.data = []
    
    def _setup_browser(self):
        """设置浏览器"""
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # 无头模式
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=375,812")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15")
        
        driver = webdriver.Chrome(options=chrome_options)
        
        # 设置Cookie
        if self.cookie:
            driver.get("https://m.weibo.cn")
            time.sleep(2)
            
            # 解析并设置Cookie
            for cookie_item in self.cookie.split(";"):
                cookie_item = cookie_item.strip()
                if "=" in cookie_item:
                    name, value = cookie_item.split("=", 1)
                    try:
                        driver.add_cookie({"name": name, "value": value})
                    except Exception as e:
                        logger.warning(f"设置Cookie失败 {name}: {e}")
        
        return driver
    
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
            driver = self._setup_browser()
            results = []
            
            for page_num in range(1, pages + 1):
                logger.info(f"搜索 '{keyword}' 第{page_num}页")
                
                # 访问搜索页面
                search_url = f"https://m.weibo.cn/search?containerid=100103type%3D1%26q%3D{keyword}&page_type=searchall&page={page_num}"
                driver.get(search_url)
                
                # 等待内容加载
                time.sleep(5)
                
                # 获取页面内容
                html = driver.page_source
                
                # 保存页面样本用于调试
                if page_num == 1:
                    with open("data/page_sample.html", "w", encoding="utf-8") as f:
                        f.write(html)
                    logger.info("已保存页面样本到 data/page_sample.html")
                
                # 解析数据
                posts = self._parse_page(html)
                results.extend(posts)
                
                logger.info(f"第{page_num}页获取{len(posts)}条数据")
            
            # 去重
            seen_contents = set()
            unique_results = []
            for post in results:
                content = post.get("content", "")
                if content and content not in seen_contents:
                    seen_contents.add(content)
                    unique_results.append(post)
            
            driver.quit()
            return unique_results
            
        except ImportError:
            logger.error("请先安装 Selenium: pip install selenium")
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
        posts = []
        
        # 尝试从页面中提取JSON数据
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
        
        # 如果没有解析到数据，尝试从HTML中提取
        if not posts:
            posts = self._parse_html(html)
        
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
    
    def _parse_html(self, html: str) -> List[Dict[str, Any]]:
        """从HTML中解析数据（备用方法）"""
        from bs4 import BeautifulSoup
        
        posts = []
        soup = BeautifulSoup(html, "html.parser")
        
        # 查找所有微博卡片 - 根据实际页面结构
        cards = soup.find_all("div", class_="card9")
        
        for card in cards:
            try:
                # 提取内容 - 根据实际HTML结构
                content_elem = card.find("div", class_="weibo-text")
                content = content_elem.get_text(strip=True) if content_elem else ""
                
                # 清理内容（去除HTML标签）
                content = re.sub(r'<[^>]+>', '', content)
                
                # 提取用户信息
                user_elem = card.find("h3", class_="m-text-cut")
                username = ""
                if user_elem:
                    # 去除VIP图标等
                    username = user_elem.get_text(strip=True)
                    # 清理用户名中的图标文字
                    username = re.sub(r'\s+', ' ', username).strip()
                
                # 提取时间
                time_elem = card.find("span", class_="time")
                post_time = time_elem.get_text(strip=True) if time_elem else ""
                
                # 提取来源
                from_elem = card.find("span", class_="from")
                source = from_elem.get_text(strip=True) if from_elem else ""
                
                # 提取互动数据 - 根据实际结构
                stats = {"reposts": 0, "comments": 0, "attitudes": 0}
                
                footer = card.find("footer", class_="m-ctrl-box")
                if footer:
                    # 转发
                    repost_elem = footer.find("i", class_="m-font-forward")
                    if repost_elem and repost_elem.find_next("h4"):
                        repost_text = repost_elem.find_next("h4").get_text(strip=True)
                        if repost_text.isdigit():
                            stats["reposts"] = int(repost_text)
                    
                    # 评论
                    comment_elem = footer.find("i", class_="m-font-comment")
                    if comment_elem and comment_elem.find_next("h4"):
                        comment_text = comment_elem.find_next("h4").get_text(strip=True)
                        if comment_text.isdigit():
                            stats["comments"] = int(comment_text)
                    
                    # 点赞
                    like_elem = footer.find("i", class_="m-icon-like")
                    if like_elem and like_elem.find_next("h4"):
                        like_text = like_elem.find_next("h4").get_text(strip=True)
                        if like_text.isdigit():
                            stats["attitudes"] = int(like_text)
                
                # 提取图片
                images = []
                img_list = card.find("ul", class_="m-auto-list")
                if img_list:
                    for img in img_list.find_all("img"):
                        src = img.get("src", "")
                        if src:
                            images.append(src)
                
                # 提取视频
                video = None
                video_elem = card.find("div", class_="card-video")
                if video_elem:
                    video_img = video_elem.find("img")
                    if video_img:
                        video = video_img.get("src", "")
                
                post = {
                    "platform": "weibo",
                    "content": content,
                    "username": username,
                    "time": post_time,
                    "source": source,
                    "stats": stats,
                    "images": images,
                    "video": video,
                }
                
                # 只添加有内容的帖子
                if content:
                    posts.append(post)
            except Exception as e:
                logger.warning(f"解析卡片失败: {e}")
        
        return posts
    
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
    cookie = "SCF=ApsAef7mHe1Fx6aDfpLVq9_L83X-wn5zT-YM3pIXCgcEOj-4qN3ykOP1aLZDPjRn_NNRGZL79n55K9kuyQjmAOI.; SUB=_2A25E9BKgDeRhGe5N7VUQ9yjJzD2IHXVniCporDV8PUNbmtAbLRjSkW9NdBsGv5Pn4dypnFU3V6dbYlX3Stkj5bvN; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFIzPM5J8RmcFbaT5zLNFCZ5NHD95QRe0qNeKMcSKMpWs4DqcjMi--NiK.Xi-2Ri--ciKnRi-zN1hecS02NSo-NeBtt; ALF=02_1779953648; _s_tentry=weibo.com; Apache=7727023717737.287.1777361724625; SINAGLOBAL=7727023717737.287.1777361724625; ULV=1777361724687:1:1:1:7727023717737.287.1777361724625:"
    
    crawler = WeiboSeleniumCrawler(cookie=cookie)
    results = crawler.search("南京旅游", pages=2)
    print(f"共获取 {len(results)} 条数据")
    
    if results:
        crawler.save_data(results, "weibo_test")
        print("数据已保存")
        
        # 打印第一条数据
        print("\n第一条数据示例:")
        print(json.dumps(results[0], ensure_ascii=False, indent=2))
    else:
        print("未获取到数据")
        print("\n请确保已安装 Selenium:")
        print("1. pip install selenium")
        print("2. 下载 ChromeDriver")
