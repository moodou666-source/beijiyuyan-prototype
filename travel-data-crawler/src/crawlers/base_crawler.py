"""
基础爬虫类
定义通用接口和基础功能
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
import time
import random
from loguru import logger


class BaseCrawler(ABC):
    """爬虫基类"""
    
    def __init__(self, platform: str, delay: tuple = (1, 3)):
        """
        初始化爬虫
        
        Args:
            platform: 平台名称
            delay: 请求间隔范围(秒)
        """
        self.platform = platform
        self.delay = delay
        self.session = None
        self.stats = {
            "total_requests": 0,
            "success_requests": 0,
            "failed_requests": 0,
            "data_count": 0,
        }
    
    @abstractmethod
    def login(self) -> bool:
        """登录平台"""
        pass
    
    @abstractmethod
    def search(self, keyword: str, **kwargs) -> List[Dict[str, Any]]:
        """
        搜索内容
        
        Args:
            keyword: 搜索关键词
            **kwargs: 其他参数
            
        Returns:
            搜索结果列表
        """
        pass
    
    @abstractmethod
    def get_user_info(self, user_id: str) -> Dict[str, Any]:
        """
        获取用户信息
        
        Args:
            user_id: 用户ID
            
        Returns:
            用户信息
        """
        pass
    
    @abstractmethod
    def get_post_detail(self, post_id: str) -> Dict[str, Any]:
        """
        获取帖子详情
        
        Args:
            post_id: 帖子ID
            
        Returns:
            帖子详情
        """
        pass
    
    def random_delay(self):
        """随机延迟，避免被封"""
        delay = random.uniform(self.delay[0], self.delay[1])
        time.sleep(delay)
    
    def is_spam_account(self, user_info: Dict[str, Any]) -> bool:
        """
        判断是否为营销号
        
        Args:
            user_info: 用户信息
            
        Returns:
            是否为营销号
        """
        # 粉丝数异常高
        if user_info.get("followers", 0) > 100000:
            return True
        
        # 发布频率异常
        if user_info.get("posts_per_day", 0) > 10:
            return True
        
        # 用户名包含营销关键词
        spam_names = ["推广", "营销", "广告", "探店", "合作"]
        username = user_info.get("username", "")
        if any(keyword in username for keyword in spam_names):
            return True
        
        return False
    
    def is_spam_content(self, content: str) -> bool:
        """
        判断内容是否为营销内容
        
        Args:
            content: 内容文本
            
        Returns:
            是否为营销内容
        """
        from config.jiangsu_spots import SPAM_KEYWORDS
        
        content_lower = content.lower()
        spam_count = sum(1 for keyword in SPAM_KEYWORDS if keyword in content_lower)
        
        # 包含3个以上营销关键词
        return spam_count >= 3
    
    def save_data(self, data: List[Dict[str, Any]], filename: str):
        """
        保存数据到文件
        
        Args:
            data: 数据列表
            filename: 文件名
        """
        import json
        import os
        from datetime import datetime
        
        # 确保目录存在
        os.makedirs("data/raw", exist_ok=True)
        
        # 添加时间戳
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = f"data/raw/{filename}_{timestamp}.json"
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"数据已保存: {filepath}")
    
    def get_stats(self) -> Dict[str, int]:
        """获取统计信息"""
        return self.stats
    
    def __enter__(self):
        """上下文管理器入口"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        if exc_type:
            logger.error(f"爬虫异常: {exc_val}")
        logger.info(f"爬虫统计: {self.stats}")
