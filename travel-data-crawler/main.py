"""
主程序
整合爬虫和算法，实现数据采集和处理
"""

import json
import os
from datetime import datetime
from loguru import logger

from config.jiangsu_spots import JIANGSU_SPOTS, KEYWORDS
from src.crawlers.weibo_crawler import WeiboCrawler
from src.algorithm.authenticity_scorer import AuthenticityScorer
from src.algorithm.recommendation import RecommendationEngine


class TravelDataCollector:
    """旅游数据采集器"""
    
    def __init__(self):
        self.weibo_crawler = WeiboCrawler()
        self.scorer = AuthenticityScorer()
        self.engine = RecommendationEngine()
        self.data_dir = "data"
        
        # 确保目录存在
        os.makedirs(f"{self.data_dir}/raw", exist_ok=True)
        os.makedirs(f"{self.data_dir}/processed", exist_ok=True)
    
    def collect_weibo_data(self, city: str, pages: int = 3) -> list:
        """
        采集微博数据
        
        Args:
            city: 城市名称
            pages: 采集页数
            
        Returns:
            采集的数据列表
        """
        logger.info(f"开始采集 {city} 的微博数据")
        
        all_posts = []
        keywords = KEYWORDS.get(city, [f"{city}旅游"])
        
        for keyword in keywords:
            logger.info(f"搜索关键词: {keyword}")
            for page in range(1, pages + 1):
                posts = self.weibo_crawler.search(keyword, page=page)
                all_posts.extend(posts)
        
        # 去重
        seen_ids = set()
        unique_posts = []
        for post in all_posts:
            if post["post_id"] not in seen_ids:
                seen_ids.add(post["post_id"])
                unique_posts.append(post)
        
        logger.info(f"{city} 共采集 {len(unique_posts)} 条微博")
        return unique_posts
    
    def process_data(self, posts: list) -> list:
        """
        处理数据
        
        Args:
            posts: 原始数据
            
        Returns:
            处理后的数据
        """
        logger.info("开始处理数据")
        
        # 计算真实性得分
        scored_posts = self.scorer.filter_spam_posts(posts, threshold=0.3)
        
        # 排序
        ranked_posts = self.scorer.rank_posts(scored_posts)
        
        logger.info(f"处理后剩余 {len(ranked_posts)} 条高质量数据")
        return ranked_posts
    
    def save_raw_data(self, posts: list, city: str):
        """
        保存原始数据
        
        Args:
            posts: 数据列表
            city: 城市名称
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.data_dir}/raw/weibo_{city}_{timestamp}.json"
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(posts, f, ensure_ascii=False, indent=2)
        
        logger.info(f"原始数据已保存: {filename}")
    
    def save_processed_data(self, posts: list, city: str):
        """
        保存处理后的数据
        
        Args:
            posts: 数据列表
            city: 城市名称
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.data_dir}/processed/weibo_{city}_{timestamp}.json"
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(posts, f, ensure_ascii=False, indent=2)
        
        logger.info(f"处理后数据已保存: {filename}")
    
    def generate_report(self, posts: list, city: str) -> dict:
        """
        生成数据报告
        
        Args:
            posts: 数据列表
            city: 城市名称
            
        Returns:
            报告数据
        """
        report = {
            "city": city,
            "total_posts": len(posts),
            "avg_authenticity": sum(p.get("authenticity_score", 0) for p in posts) / len(posts) if posts else 0,
            "avg_recommendation": sum(p.get("recommendation_score", 0) for p in posts) / len(posts) if posts else 0,
            "top_posts": posts[:5],
            "generated_at": datetime.now().isoformat(),
        }
        
        return report
    
    def run(self, cities: list = None, pages: int = 3):
        """
        运行采集程序
        
        Args:
            cities: 城市列表，默认采集所有城市
            pages: 每城市采集页数
        """
        if cities is None:
            cities = list(JIANGSU_SPOTS.keys())
        
        logger.info(f"开始采集 {len(cities)} 个城市的数据")
        
        for city in cities:
            try:
                # 采集数据
                raw_posts = self.collect_weibo_data(city, pages)
                
                if not raw_posts:
                    logger.warning(f"{city} 未采集到数据")
                    continue
                
                # 保存原始数据
                self.save_raw_data(raw_posts, city)
                
                # 处理数据
                processed_posts = self.process_data(raw_posts)
                
                # 保存处理后数据
                self.save_processed_data(processed_posts, city)
                
                # 生成报告
                report = self.generate_report(processed_posts, city)
                
                logger.info(f"{city} 处理完成")
                logger.info(f"  - 原始数据: {len(raw_posts)}条")
                logger.info(f"  - 高质量数据: {len(processed_posts)}条")
                logger.info(f"  - 平均真实性: {report['avg_authenticity']:.2f}")
                
            except Exception as e:
                logger.error(f"{city} 处理失败: {e}")
        
        logger.info("采集完成")


def main():
    """主函数"""
    # 配置日志
    logger.add("logs/crawler_{time}.log", rotation="1 day")
    
    # 创建采集器
    collector = TravelDataCollector()
    
    # 设置微博Cookie（已获取）
    cookie = "SCF=ApsAef7mHe1Fx6aDfpLVq9_L83X-wn5zT-YM3pIXCgcEOj-4qN3ykOP1aLZDPjRn_NNRGZL79n55K9kuyQjmAOI.; SUB=_2A25E9BKgDeRhGe5N7VUQ9yjJzD2IHXVniCporDV8PUNbmtAbLRjSkW9NdBsGv5Pn4dypnFU3V6dbYlX3Stkj5bvN; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFIzPM5J8RmcFbaT5zLNFCZ5NHD95QRe0qNeKMcSKMpWs4DqcjMi--NiK.Xi-2Ri--ciKnRi-zN1hecS02NSo-NeBtt; ALF=02_1779953648; _s_tentry=weibo.com; Apache=7727023717737.287.1777361724625; SINAGLOBAL=7727023717737.287.1777361724625; ULV=1777361724687:1:1:1:7727023717737.287.1777361724625:"
    collector.weibo_crawler.set_cookie(cookie)
    
    # 运行采集 - 测试南京
    print("开始采集南京数据...")
    collector.run(cities=["南京"], pages=2)
    
    print("采集完成！")


if __name__ == "__main__":
    main()
