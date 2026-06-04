# DEV-BRIEF - 北京雨燕 APP 开发简报

> **基线文件：** `北京雨燕1.0版.html`（13080行，单文件SPA）
> **资源目录：** `北京雨燕1.0版_files/`
> **部署：** GitHub Pages（`master` 分支）+ 阿里云 OSS
> **⚠️ GitHub Pages 部署的是 `master` 分支，不是 `main`！**

---

## 技术栈

- **纯原生 HTML + CSS + JavaScript**，无任何框架
- 所有动态内容通过 `innerHTML` 渲染
- 高德地图 JS API（`AMap.Map` / `AMap.Marker` / `AMap.Polyline`）
- 高德 API Key：`718d342bdea025c853f48e00fc342514`
- 阿里云 OSS：Bucket `beijingyuyan`，Endpoint `oss-cn-beijing.aliyuncs.com`
- 字体：`-apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', sans-serif`

---

## 页面结构

### 3个主页面（`.page`）

| 页面 | ID | 内容 |
|------|-----|------|
| 路书 | `tripPage` | 我的行程（横向滚动卡片）+ 路书推荐（垂直列表）|
| 发现 | `explorePage` | 全屏高德地图 + 景点/摄影/广场/避雷 4种模式 |
| 我的 | `profilePage` | 个人主页 + 足迹地图 + 作品/日常/推荐/收藏/喜欢 |

### 6个覆盖页面（`position: fixed`）

| 页面 | ID | z-index |
|------|-----|---------|
| 创建行程 | `createPage` | 1000 |
| 规划进度 | `planningPage` | 10000 |
| 路书筛选 | `roadbookFilterPage` | 3000 |
| 规划结果 | `resultPage` | 1000 |
| 行程详情 | `tripDetailPage` | 2000 |
| 我的行程列表 | `tripListPage` | 3000 |
| 设置 | `settingsPage` | 3000 |
| 广场 | `plazaPage`（动态创建）| 1500 |

### 底部导航

- 4个Tab：**路书 / 规划(+) / 发现 / 我的**
- 高度 83px，背景 `#7C9A3D`，圆角 `24px 24px 0 0`
- "规划"调用 `showCreatePage()`，其他调用 `switchTab(tab)`

---

## 设计规范

### 色彩

| 用途 | 色值 |
|------|------|
| 主色 | `#7C9A3D`（橄榄绿）|
| 主色按下 | `#6a8a33` / `#5a7a2a` |
| 主色浅底 | `#f0f7e6` / `#E8F0D8` |
| 背景 | `#FFFFFF` / `#F5F5F5` / `#F5F5DC` |
| 主文字 | `#1A1A1A` |
| 次要文字 | `#333` / `#666` |
| 辅助文字 | `#999` / `#aaa` / `#ccc` |
| 差评红 | `#ff4444` |
| 中评橙 | `#ff9800` |
| 好评绿 | `#4caf50` |
| 链接蓝 | `#1890FF` / `#3B82F6` |
| 删除红 | `#EF4444` |

### 尺寸

- 最大宽度：`430px`，居中显示
- 卡片圆角：`16px`，面板：`20px`，按钮：`24px`，FAB：`28px`
- 页面内边距：`16px`，卡片间距：`12px`
- 标题字号：`24/22/20/18/17/16px`，正文：`15/14/13px`，辅助：`12/11/10px`
- 状态栏：`44px`，底部导航：`83px`

### z-index 层级

- 底部导航：100
- 弹窗/覆盖页：1000-3001
- Toast：100000

---

## 核心功能模块

### 行程卡片（`.topic-card`）
- 140×200px，背景图 + 渐变遮罩 + 文字
- 横向滚动容器 `.horizontal-scroll`

### 路书卡片（`.roadbook-card`）
- 全宽 150px高，左信息 + 右倾斜图片（rotate: 3deg）
- 左滑操作：收藏 / 不推荐 / 分享（`.roadbook-slide-actions`）

### 景点卡片（`.spot-card`）
- 80×80 图片 + 信息
- 编辑模式：选择圆点 + 拖拽手柄
- 左滑操作（`.spot-swipe-actions`）

### 可拖拽底部面板（`.bottom-panel`）
- 三态：半屏 / 展开 / 收起
- 拖拽手柄 `.drag-handle`
- 用于：景点详情 / 摄影详情 / 避雷详情 / 行程详情

### 地图（5个实例）
- `exploreMap`：发现页全屏地图
- `detailMap`：行程详情全屏地图
- `resultMap`：规划结果（250px高）
- `planningMap`：规划进度（40%高）
- `profileMap`：足迹地图（180px高）
- 已隐藏高德 logo 和版权信息

### 发现页 4 模式
- **景点**（`spots`）：编号圆点标记 + 轮播卡片 + 底部面板列表
- **摄影**（`photo`）：照片缩略图标记（60×60, 圆角12px）+ 2列网格详情
- **广场**（`tracks`）：朋友圈式信息流 + 关注/点赞/分享
- **避雷**（`avoid`）：蓝色闪电图标 + 差评/中评/好评 + 语音评价

### 轮播卡片（`.carousel-overlay`）
- 375px宽 × 170px高，覆盖在地图上
- 80×80 图片 + 标题/描述/标签
- 圆点指示器

### AI 聊天（雨燕聊天弹窗）
- 天数Tab + 消息列表
- 用户/机器人气泡
- 规划日志动画
- 快速标签 + 语音录制（波形动画+计时器）

### 城市选择器
- 弹窗式 `.city-picker-modal`
- 省份→城市 二级选择 + 搜索过滤
- 14个省份数据（`provinceCityData`）

### 日历弹窗
- 月份视图 + 日期范围选择
- 灵活天数开关 → 滚轮选择器

### 分享弹窗
- 大图标：共同编辑 / 长图 / 找搭子 / 求助
- 小图标：复制链接 / 微信 / 朋友圈 / 广场 / 更多

### 行程详情编辑
- 天数Tab（可添加）+ 景点列表
- 编辑模式：选择/拖拽/批量操作（移至/删除）
- 添加景点弹窗：收藏/住宿/自定义/搜索 4种子面板
- 设置页：封面/名称/出行方式/预算/提醒/通知/隐私

### 个人页面
- 头像/名称/简介 + 关注/粉丝/收藏/行程
- 足迹地图（可缩小）+ 打卡城市印章
- Tab：作品/日常/推荐/收藏/喜欢（2列照片网格）

---

## 数据

### 硬编码数据
- `cityDatabase`：8个城市
- `spotDetails`：10个景点
- `tripData`：7天6晚行程
- `spotsData`：6个苏州景点
- `avoidData`：6个避雷景点
- `provinceCityData`：14个省份

### 图片源
- 本地：`./北京雨燕1.0版_files/photo-*`
- Unsplash / Picsum / Pravatar / Randomuser

---

## 交互/手势

- **拖拽**：底部面板三态切换、景点排序
- **左滑**：路书卡片、行程列表卡片、景点卡片
- **横向滚动**：行程卡片（鼠标+触摸）
- **吸顶**：模块标题（top:0）、子标题（top:34px）、天数Tab（top:60px）
- **动画**：slideUp、dropdownFadeIn、pulse-ring、voiceWave

---

## 修改指令格式

每次修改请按此格式：
```
页面：[路书/发现/我的/创建行程/行程详情/规划结果/...]
位置：[具体模块/组件/元素]
改什么：[一句话描述]
```

**示例：**
```
页面：发现
位置：摄影模式底部面板
改什么：照片网格改成3列，间距改为8px
```

## 重要规则

1. **修改前先 read 当前 HTML 文件**确认最新状态
2. **只改目标代码**，不要动无关部分
3. **改完后截图验证**
4. **不确定的地方先问**，不要自己猜
5. **保持原生实现**，不引入新框架/库
6. **遵循现有设计规范和色彩方案**
7. 行程文件：`北京雨燕1.0版.html`
8. 修改完推送到 GitHub 后，同步 master 分支：`git checkout master && git merge main -X theirs --no-edit && git push origin master && git checkout main`
