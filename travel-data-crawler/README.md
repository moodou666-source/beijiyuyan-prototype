# 旅游数据采集系统

## 项目结构
```
travel-data-crawler/
├── config/                 # 配置文件
│   ├── weibo_config.py    # 微博配置
│   ├── douyin_config.py   # 抖音配置
│   └── xiaohongshu_config.py  # 小红书配置
├── src/
│   ├── crawlers/          # 爬虫模块
│   │   ├── base_crawler.py
│   │   ├── weibo_crawler.py
│   │   ├── douyin_crawler.py
│   │   └── xiaohongshu_crawler.py
│   ├── models/            # 数据模型
│   │   ├── spot.py        # 景点模型
│   │   ├── post.py        # 帖子模型
│   │   └── user.py        # 用户模型
│   ├── algorithm/         # 算法模块
│   │   ├── authenticity_scorer.py  # 真实性评分
│   │   ├── recommendation.py       # 推荐算法
│   │   └── anti_spam.py            # 反作弊
│   └── utils/             # 工具函数
│       ├── db.py          # 数据库连接
│       ├── logger.py      # 日志
│       └── helpers.py     # 辅助函数
├── data/
│   ├── raw/               # 原始数据
│   └── processed/         # 处理后数据
└── tests/                 # 测试

```

## 安装依赖
```bash
pip install -r requirements.txt
```

## 运行爬虫
```bash
python src/crawlers/weibo_crawler.py
python src/crawlers/douyin_crawler.py
python src/crawlers/xiaohongshu_crawler.py
```

## 数据处理
```bash
python src/algorithm/authenticity_scorer.py
python src/algorithm/recommendation.py
```
