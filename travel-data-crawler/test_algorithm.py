"""
测试算法
处理采集到的微博数据
"""

import json
from src.algorithm.authenticity_scorer import AuthenticityScorer
from src.algorithm.recommendation import RecommendationEngine


def main():
    # 加载数据
    with open("data/raw/weibo_test_20260428_155843.json", "r", encoding="utf-8") as f:
        posts = json.load(f)
    
    print(f"共加载 {len(posts)} 条数据\n")
    
    # 初始化算法
    scorer = AuthenticityScorer()
    engine = RecommendationEngine()
    
    # 计算真实性得分
    print("=" * 50)
    print("真实性评分结果")
    print("=" * 50)
    
    for post in posts[:5]:  # 只显示前5条
        score = scorer.calculate_authenticity_score(post, posts)
        post["authenticity_score"] = score
        
        print(f"\n用户: {post['username']}")
        print(f"内容: {post['content'][:50]}...")
        print(f"互动: 转发{post['stats']['reposts']} 评论{post['stats']['comments']} 点赞{post['stats']['attitudes']}")
        print(f"真实性得分: {score:.2f}")
    
    # 过滤营销号
    print("\n" + "=" * 50)
    print("过滤营销号")
    print("=" * 50)
    
    filtered_posts = scorer.filter_spam_posts(posts, threshold=0.3)
    
    # 推荐排序
    print("\n" + "=" * 50)
    print("推荐排序结果（前10条）")
    print("=" * 50)
    
    recommended = engine.recommend(filtered_posts, top_k=10)
    
    for i, post in enumerate(recommended, 1):
        print(f"\n{i}. {post['username']}")
        print(f"   内容: {post['content'][:60]}...")
        print(f"   真实性: {post.get('authenticity_score', 0):.2f}")
        print(f"   推荐度: {post.get('recommendation_score', 0):.2f}")
        print(f"   互动: 👍{post['stats']['attitudes']} 💬{post['stats']['comments']} 🔄{post['stats']['reposts']}")
    
    # 保存处理后的数据
    with open("data/processed/weibo_nanjing_analyzed.json", "w", encoding="utf-8") as f:
        json.dump(recommended, f, ensure_ascii=False, indent=2)
    
    print(f"\n处理完成！共分析 {len(posts)} 条数据")
    print(f"高质量数据: {len(filtered_posts)} 条")
    print(f"结果已保存到 data/processed/weibo_nanjing_analyzed.json")


if __name__ == "__main__":
    main()
