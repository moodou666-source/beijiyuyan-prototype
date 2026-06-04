"""
真实性评分算法
计算内容的真实性和可信度
"""

import math
from typing import Dict, Any, List
from collections import Counter
from loguru import logger


class AuthenticityScorer:
    """真实性评分器"""
    
    def __init__(self):
        # 权重配置
        self.weights = {
            "user_credibility": 0.30,      # 用户可信度
            "content_originality": 0.25,   # 内容原创度
            "interaction_quality": 0.25,   # 互动质量
            "content_quality": 0.20,       # 内容质量
        }
    
    def calculate_user_credibility(self, user_info: Dict[str, Any]) -> float:
        """
        计算用户可信度
        
        评分标准:
        - 普通用户(粉丝<1000): 1.0
        - 小V(粉丝1000-10000): 0.8
        - 中V(粉丝10000-50000): 0.6
        - 大V(粉丝50000-100000): 0.4
        - 超大V(粉丝>100000): 0.2
        - 认证用户额外扣分
        """
        followers = user_info.get("followers", 0)
        verified = user_info.get("verified", False)
        
        # 根据粉丝数评分
        if followers < 1000:
            score = 1.0
        elif followers < 10000:
            score = 0.8
        elif followers < 50000:
            score = 0.6
        elif followers < 100000:
            score = 0.4
        else:
            score = 0.2
        
        # 认证用户可能是营销号，适当扣分
        if verified:
            verified_type = user_info.get("verified_type", -1)
            # 企业认证(2,3)扣分更多
            if verified_type in [2, 3]:
                score *= 0.7
            # 个人认证(0)扣分较少
            elif verified_type == 0:
                score *= 0.9
        
        return score
    
    def calculate_content_originality(self, content: str, all_contents: List[str]) -> float:
        """
        计算内容原创度
        
        评分标准:
        - 完全原创: 1.0
        - 部分相似: 0.5-0.8
        - 高度相似: 0.2-0.5
        - 完全复制: 0.0
        """
        if not content or not all_contents:
            return 1.0
        
        # 计算与所有内容的相似度
        similarities = []
        for other_content in all_contents:
            if other_content != content:
                similarity = self._text_similarity(content, other_content)
                similarities.append(similarity)
        
        if not similarities:
            return 1.0
        
        # 取最大相似度
        max_similarity = max(similarities)
        
        # 根据相似度评分
        if max_similarity < 0.3:
            return 1.0
        elif max_similarity < 0.5:
            return 0.8
        elif max_similarity < 0.7:
            return 0.5
        elif max_similarity < 0.9:
            return 0.3
        else:
            return 0.1
    
    def calculate_interaction_quality(self, stats: Dict[str, int]) -> float:
        """
        计算互动质量
        
        评分标准:
        - 评论/点赞比高: 真实互动多
        - 转发/点赞比合理: 内容有价值
        - 异常比例: 可能是刷量
        """
        reposts = stats.get("reposts", 0)
        comments = stats.get("comments", 0)
        attitudes = stats.get("attitudes", 0)
        
        if attitudes == 0:
            return 0.5
        
        # 计算比例
        comment_ratio = comments / attitudes
        repost_ratio = reposts / attitudes
        
        # 正常比例范围
        # 评论率: 0.05-0.3
        # 转发率: 0.1-0.5
        
        comment_score = 1.0
        if comment_ratio < 0.01:
            comment_score = 0.3  # 评论太少，可能是刷赞
        elif comment_ratio > 0.5:
            comment_score = 0.7  # 评论太多，可能是水军
        
        repost_score = 1.0
        if repost_ratio < 0.05:
            repost_score = 0.5
        elif repost_ratio > 0.8:
            repost_score = 0.6
        
        # 综合评分
        return (comment_score + repost_score) / 2
    
    def calculate_content_quality(self, content: str, images: List[str]) -> float:
        """
        计算内容质量
        
        评分标准:
        - 文字长度: 100-500字最佳
        - 图片数量: 1-9张最佳
        - 内容丰富度: 包含地点、时间、感受等
        """
        score = 0.5
        
        # 文字长度评分
        text_length = len(content)
        if 100 <= text_length <= 500:
            score += 0.2
        elif 50 <= text_length < 100:
            score += 0.1
        elif text_length > 500:
            score += 0.15
        
        # 图片数量评分
        image_count = len(images)
        if 3 <= image_count <= 9:
            score += 0.2
        elif 1 <= image_count < 3:
            score += 0.1
        elif image_count > 9:
            score += 0.15
        
        # 内容丰富度
        rich_indicators = ["感觉", "体验", "推荐", "建议", "注意", "门票", "时间", "交通"]
        rich_count = sum(1 for indicator in rich_indicators if indicator in content)
        if rich_count >= 3:
            score += 0.1
        
        return min(score, 1.0)
    
    def calculate_authenticity_score(self, post: Dict[str, Any], all_posts: List[Dict[str, Any]] = None) -> float:
        """
        计算真实性总分
        
        Args:
            post: 帖子数据
            all_posts: 所有帖子（用于计算原创度）
            
        Returns:
            真实性得分 (0-1)
        """
        # 获取各维度得分
        user_credibility = self.calculate_user_credibility(post.get("user_info", {}))
        
        if all_posts:
            all_contents = [p.get("content", "") for p in all_posts]
            content_originality = self.calculate_content_originality(post.get("content", ""), all_contents)
        else:
            content_originality = 1.0
        
        interaction_quality = self.calculate_interaction_quality(post.get("stats", {}))
        content_quality = self.calculate_content_quality(post.get("content", ""), post.get("images", []))
        
        # 加权计算总分
        total_score = (
            user_credibility * self.weights["user_credibility"] +
            content_originality * self.weights["content_originality"] +
            interaction_quality * self.weights["interaction_quality"] +
            content_quality * self.weights["content_quality"]
        )
        
        return round(total_score, 2)
    
    def _text_similarity(self, text1: str, text2: str) -> float:
        """
        计算文本相似度（使用Jaccard相似度）
        
        Args:
            text1: 文本1
            text2: 文本2
            
        Returns:
            相似度 (0-1)
        """
        # 分词（简单按字符分词）
        set1 = set(text1)
        set2 = set(text2)
        
        # 计算Jaccard相似度
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        
        if union == 0:
            return 0.0
        
        return intersection / union
    
    def filter_spam_posts(self, posts: List[Dict[str, Any]], threshold: float = 0.3) -> List[Dict[str, Any]]:
        """
        过滤营销号内容
        
        Args:
            posts: 帖子列表
            threshold: 真实性阈值
            
        Returns:
            过滤后的帖子列表
        """
        filtered_posts = []
        
        for post in posts:
            score = self.calculate_authenticity_score(post, posts)
            post["authenticity_score"] = score
            
            if score >= threshold:
                filtered_posts.append(post)
        
        logger.info(f"过滤前: {len(posts)}条，过滤后: {len(filtered_posts)}条")
        return filtered_posts
    
    def rank_posts(self, posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        按真实性排序
        
        Args:
            posts: 帖子列表
            
        Returns:
            排序后的帖子列表
        """
        # 计算真实性得分
        for post in posts:
            if "authenticity_score" not in post:
                post["authenticity_score"] = self.calculate_authenticity_score(post, posts)
        
        # 按得分排序（降序）
        sorted_posts = sorted(posts, key=lambda x: x["authenticity_score"], reverse=True)
        
        return sorted_posts


if __name__ == "__main__":
    # 测试
    scorer = AuthenticityScorer()
    
    # 测试数据
    test_posts = [
        {
            "user_info": {
                "followers": 500,
                "verified": False,
            },
            "content": "今天去了中山陵，感觉非常棒！建议大家早上8点去，人少景美。门票免费，但需要预约。",
            "images": ["img1.jpg", "img2.jpg", "img3.jpg"],
            "stats": {
                "reposts": 10,
                "comments": 25,
                "attitudes": 100,
            }
        },
        {
            "user_info": {
                "followers": 200000,
                "verified": True,
                "verified_type": 2,
            },
            "content": "推荐大家一定要来中山陵！点击链接购买优惠门票！",
            "images": ["img1.jpg"],
            "stats": {
                "reposts": 5000,
                "comments": 50,
                "attitudes": 10000,
            }
        },
    ]
    
    for post in test_posts:
        score = scorer.calculate_authenticity_score(post, test_posts)
        print(f"帖子真实性得分: {score}")
    
    # 过滤营销号
    filtered = scorer.filter_spam_posts(test_posts)
    print(f"过滤后剩余: {len(filtered)}条")
