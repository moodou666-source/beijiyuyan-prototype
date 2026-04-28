"""
推荐算法
基于真实性得分的推荐排序
"""

import math
from typing import List, Dict, Any
from datetime import datetime, timedelta
from loguru import logger


class RecommendationEngine:
    """推荐引擎"""
    
    def __init__(self):
        # 权重配置
        self.weights = {
            "authenticity": 0.35,    # 真实性
            "popularity": 0.25,      # 热度
            "recency": 0.20,         # 时效性
            "location": 0.20,        # 地理位置匹配
        }
    
    def calculate_popularity_score(self, stats: Dict[str, int]) -> float:
        """
        计算热度得分
        
        考虑因素:
        - 点赞数
        - 评论数
        - 转发数
        - 互动增长率
        """
        attitudes = stats.get("attitudes", 0)
        comments = stats.get("comments", 0)
        reposts = stats.get("reposts", 0)
        
        # 使用对数函数，避免极端值影响
        # 权重: 点赞(0.5) + 评论(0.3) + 转发(0.2)
        score = (
            math.log1p(attitudes) * 0.5 +
            math.log1p(comments) * 0.3 +
            math.log1p(reposts) * 0.2
        )
        
        # 归一化到0-1
        max_score = math.log1p(100000) * 0.5 + math.log1p(10000) * 0.3 + math.log1p(50000) * 0.2
        normalized_score = score / max_score
        
        return min(normalized_score, 1.0)
    
    def calculate_recency_score(self, created_at: str) -> float:
        """
        计算时效性得分
        
        评分标准:
        - 一周内: 1.0
        - 一月内: 0.8
        - 三月内: 0.6
        - 半年内: 0.4
        - 一年内: 0.2
        - 超过一年: 0.1
        """
        try:
            # 解析时间
            if "前" in created_at:
                # 相对时间，如"2小时前"
                return 1.0
            
            # 尝试解析绝对时间
            post_time = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
            now = datetime.now()
            days_diff = (now - post_time).days
            
            if days_diff <= 7:
                return 1.0
            elif days_diff <= 30:
                return 0.8
            elif days_diff <= 90:
                return 0.6
            elif days_diff <= 180:
                return 0.4
            elif days_diff <= 365:
                return 0.2
            else:
                return 0.1
                
        except Exception:
            # 无法解析时间，默认中等时效性
            return 0.5
    
    def calculate_location_score(self, post_location: str, user_location: str = None) -> float:
        """
        计算地理位置匹配度
        
        Args:
            post_location: 帖子位置
            user_location: 用户当前位置
            
        Returns:
            匹配度得分
        """
        if not user_location:
            # 没有用户位置，返回中性得分
            return 0.5
        
        # 简单匹配，实际应用中应使用地理坐标计算距离
        if user_location in post_location:
            return 1.0
        
        # 同一城市
        # 这里简化处理，实际应该解析城市信息
        return 0.7
    
    def calculate_recommendation_score(self, post: Dict[str, Any], user_location: str = None) -> float:
        """
        计算推荐得分
        
        Args:
            post: 帖子数据
            user_location: 用户位置
            
        Returns:
            推荐得分
        """
        # 获取各维度得分
        authenticity = post.get("authenticity_score", 0.5)
        popularity = self.calculate_popularity_score(post.get("stats", {}))
        recency = self.calculate_recency_score(post.get("created_at", ""))
        location = self.calculate_location_score(post.get("location", ""), user_location)
        
        # 加权计算总分
        total_score = (
            authenticity * self.weights["authenticity"] +
            popularity * self.weights["popularity"] +
            recency * self.weights["recency"] +
            location * self.weights["location"]
        )
        
        return round(total_score, 2)
    
    def recommend(self, posts: List[Dict[str, Any]], user_location: str = None, top_k: int = 10) -> List[Dict[str, Any]]:
        """
        推荐排序
        
        Args:
            posts: 帖子列表
            user_location: 用户位置
            top_k: 返回前K个结果
            
        Returns:
            推荐列表
        """
        # 计算推荐得分
        for post in posts:
            post["recommendation_score"] = self.calculate_recommendation_score(post, user_location)
        
        # 按推荐得分排序
        sorted_posts = sorted(posts, key=lambda x: x["recommendation_score"], reverse=True)
        
        # 返回前K个
        return sorted_posts[:top_k]
    
    def recommend_by_spot(self, posts: List[Dict[str, Any]], spot_name: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        按景点推荐
        
        Args:
            posts: 帖子列表
            spot_name: 景点名称
            top_k: 返回前K个结果
            
        Returns:
            推荐列表
        """
        # 筛选相关帖子
        related_posts = [
            post for post in posts
            if spot_name in post.get("content", "") or spot_name in post.get("location", "")
        ]
        
        # 推荐排序
        return self.recommend(related_posts, top_k=top_k)
    
    def recommend_by_city(self, posts: List[Dict[str, Any]], city: str, top_k: int = 20) -> List[Dict[str, Any]]:
        """
        按城市推荐
        
        Args:
            posts: 帖子列表
            city: 城市名称
            top_k: 返回前K个结果
            
        Returns:
            推荐列表
        """
        # 筛选相关帖子
        related_posts = [
            post for post in posts
            if city in post.get("content", "") or city in post.get("location", "")
        ]
        
        # 推荐排序
        return self.recommend(related_posts, top_k=top_k)
    
    def get_hot_spots(self, posts: List[Dict[str, Any]], top_k: int = 10) -> List[Dict[str, str]]:
        """
        获取热门景点
        
        Args:
            posts: 帖子列表
            top_k: 返回前K个结果
            
        Returns:
            热门景点列表
        """
        from collections import Counter
        
        # 统计景点提及次数
        spot_counts = Counter()
        
        for post in posts:
            content = post.get("content", "")
            # 这里简化处理，实际应该使用NER识别景点名称
            # 暂时使用简单关键词匹配
            # TODO: 使用更精确的景点识别方法
            
        # 返回热门景点
        return [{"name": spot, "count": count} for spot, count in spot_counts.most_common(top_k)]


if __name__ == "__main__":
    # 测试
    engine = RecommendationEngine()
    
    # 测试数据
    test_posts = [
        {
            "content": "中山陵真的很美！",
            "location": "南京",
            "authenticity_score": 0.9,
            "stats": {"attitudes": 1000, "comments": 100, "reposts": 50},
            "created_at": "2024-01-15 10:00:00",
        },
        {
            "content": "推荐大家一定要来中山陵！",
            "location": "南京",
            "authenticity_score": 0.3,
            "stats": {"attitudes": 10000, "comments": 50, "reposts": 5000},
            "created_at": "2024-01-10 10:00:00",
        },
    ]
    
    # 推荐排序
    recommended = engine.recommend(test_posts, user_location="南京")
    
    for post in recommended:
        print(f"推荐得分: {post['recommendation_score']}, 真实性: {post['authenticity_score']}")
        print(f"内容: {post['content'][:50]}...")
        print()
