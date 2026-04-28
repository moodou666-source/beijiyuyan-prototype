"""
微博爬虫
采集微博上的旅游相关内容
"""

import requests
import json
import re
from typing import List, Dict, Any
from urllib.parse import quote
from loguru import logger

from .base_crawler import BaseCrawler


class WeiboCrawler(BaseCrawler):
    """微博爬虫"""
    
    def __init__(self):
        super().__init__("weibo", delay=(2, 5))
        self.base_url = "https://m.weibo.cn"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15",
            "Referer": "https://m.weibo.cn/",
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def login(self) -> bool:
        """
        登录微博
        注意：需要手动登录获取Cookie
        """
        logger.info("请手动登录微博并获取Cookie")
        logger.info("访问: https://m.weibo.cn")
        return True
    
    def set_cookie(self, cookie: str):
        """设置登录Cookie"""
        self.session.headers["Cookie"] = cookie
        logger.info("Cookie已设置")
    
    def search(self, keyword: str, page: int = 1, **kwargs) -> List[Dict[str, Any]]:
        """
        搜索微博内容
        
        Args:
            keyword: 搜索关键词
            page: 页码
            
        Returns:
            微博列表
        """
        self.random_delay()
        
        url = f"{self.base_url}/api/container/getIndex"
        params = {
            "containerid": f"100103type=1&q={quote(keyword)}",
            "page_type": "searchall",
            "page": page,
        }
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            self.stats["total_requests"] += 1
            
            if response.status_code != 200:
                logger.warning(f"请求失败: {response.status_code}")
                self.stats["failed_requests"] += 1
                return []
            
            data = response.json()
            cards = data.get("data", {}).get("cards", [])
            
            results = []
            for card in cards:
                if card.get("card_type") != 9:
                    continue
                
                mblog = card.get("mblog", {})
                if not mblog:
                    continue
                
                # 解析微博内容
                post = self._parse_mblog(mblog)
                if post:
                    results.append(post)
            
            self.stats["success_requests"] += 1
            self.stats["data_count"] += len(results)
            
            logger.info(f"搜索 '{keyword}' 第{page}页，获取{len(results)}条数据")
            return results
            
        except Exception as e:
            logger.error(f"搜索失败: {e}")
            self.stats["failed_requests"] += 1
            return []
    
    def _parse_mblog(self, mblog: Dict[str, Any]) -> Dict[str, Any]:
        """
        解析微博内容
        
        Args:
            mblog: 微博原始数据
            
        Returns:
            解析后的数据
        """
        try:
            # 获取用户信息
            user = mblog.get("user", {})
            user_info = {
                "id": str(user.get("id", "")),
                "username": user.get("screen_name", ""),
                "followers": user.get("followers_count", 0),
                "following": user.get("follow_count", 0),
                "verified": user.get("verified", False),
                "verified_type": user.get("verified_type", -1),
            }
            
            # 判断是否为营销号
            if self.is_spam_account(user_info):
                return None
            
            # 解析内容
            text = mblog.get("text", "")
            # 去除HTML标签
            text = re.sub(r"<[^>]+>", "", text)
            
            # 判断是否为营销内容
            if self.is_spam_content(text):
                return None
            
            # 获取图片
            pics = mblog.get("pics", [])
            images = [pic.get("large", {}).get("url", pic.get("url", "")) for pic in pics]
            
            # 获取位置信息
            page_info = mblog.get("page_info", {})
            location = page_info.get("page_title", "")
            
            # 构建数据
            post = {
                "platform": "weibo",
                "post_id": str(mblog.get("id", "")),
                "user_id": user_info["id"],
                "username": user_info["username"],
                "content": text,
                "images": images,
                "location": location,
                "created_at": mblog.get("created_at", ""),
                "stats": {
                    "reposts": mblog.get("reposts_count", 0),
                    "comments": mblog.get("comments_count", 0),
                    "attitudes": mblog.get("attitudes_count", 0),
                },
                "user_info": user_info,
                "source": mblog.get("source", ""),
            }
            
            return post
            
        except Exception as e:
            logger.error(f"解析微博失败: {e}")
            return None
    
    def get_user_info(self, user_id: str) -> Dict[str, Any]:
        """获取用户信息"""
        self.random_delay()
        
        url = f"{self.base_url}/api/container/getIndex"
        params = {
            "type": "uid",
            "value": user_id,
        }
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                user = data.get("data", {}).get("userInfo", {})
                return {
                    "id": str(user.get("id", "")),
                    "username": user.get("screen_name", ""),
                    "followers": user.get("followers_count", 0),
                    "following": user.get("follow_count", 0),
                    "verified": user.get("verified", False),
                    "description": user.get("description", ""),
                }
        except Exception as e:
            logger.error(f"获取用户信息失败: {e}")
        
        return {}
    
    def get_post_detail(self, post_id: str) -> Dict[str, Any]:
        """获取微博详情"""
        self.random_delay()
        
        url = f"{self.base_url}/statuses/show"
        params = {"id": post_id}
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return self._parse_mblog(data.get("data", {}))
        except Exception as e:
            logger.error(f"获取微博详情失败: {e}")
        
        return {}
    
    def search_spot(self, spot_name: str, city: str, pages: int = 3) -> List[Dict[str, Any]]:
        """
        搜索特定景点的微博
        
        Args:
            spot_name: 景点名称
            city: 城市名称
            pages: 搜索页数
            
        Returns:
            微博列表
        """
        keywords = [
            f"{city}{spot_name}",
            f"{spot_name}打卡",
            f"{spot_name}攻略",
        ]
        
        results = []
        for keyword in keywords:
            for page in range(1, pages + 1):
                posts = self.search(keyword, page=page)
                results.extend(posts)
        
        # 去重
        seen_ids = set()
        unique_results = []
        for post in results:
            if post["post_id"] not in seen_ids:
                seen_ids.add(post["post_id"])
                unique_results.append(post)
        
        logger.info(f"景点 '{spot_name}' 共获取{len(unique_results)}条微博")
        return unique_results


if __name__ == "__main__":
    # 测试
    crawler = WeiboCrawler()
    
    # 设置Cookie（需要手动获取）
    # crawler.set_cookie("your_cookie_here")
    
    # 搜索南京中山陵
    # results = crawler.search_spot("中山陵", "南京")
    # crawler.save_data(results, "weibo_zhongshanling")
    
    print("微博爬虫初始化完成")
    print("请先登录微博获取Cookie，然后调用set_cookie方法")
