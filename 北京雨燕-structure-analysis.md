# 北京雨燕 1.0版 - 完整结构分析

> 源文件: `北京雨燕1.0版.html` (13,080 行, 单文件 HTML 应用)
> 分析日期: 2026-06-02

---

## 1. 页面/标签结构 (Pages/Tabs)

应用是一个移动端单页应用 (SPA), 最大宽度 430px, 居中显示。

### 主页面 (`.page`)

| 页面 | ID | 描述 |
|------|-----|------|
| 行程/路书 | `tripPage` | 默认激活页, 显示我的行程(横向滚动卡片) + 路书推荐(垂直列表) |
| 探索/发现 | `explorePage` | 高德地图为主的全屏地图页, 含景点/摄影/广场/避雷4种模式 |
| 我的 | `profilePage` | 个人主页, 足迹地图 + 作品/日常/推荐/收藏/喜欢 Tab |

### 覆盖/子页面 (Overlay Pages, `position: fixed`)

| 页面 | ID | z-index | 描述 |
|------|-----|---------|------|
| 创建行程 | `createPage` | 1000 | 目的地搜索 + 日期选择 + 偏好标签 |
| 规划进度 | `planningPage` | 10000 | AI规划进度日志 + 地图 |
| 路书筛选 | `roadbookFilterPage` | 3000 | 途经地/天数/季节/特色 筛选面板 |
| 智能规划结果 | `resultPage` | 1000 | 规划结果展示, 含地图 + 每日行程 |
| 行程详情 | `tripDetailPage` | 2000 | 全屏地图 + 可拖拽底部面板, 核心编辑页 |
| 我的行程列表 | `tripListPage` | 3000 | 行程卡片列表, 支持左滑操作 |
| 设置 | `settingsPage` | 3000 | 行程设置(封面/名称/周期/出行方式/预算/提醒/通知/隐私) |
| 广场 | `plazaPage` (动态创建) | 1500 | 朋友圈式社交界面, 广场/关注/本地 Tab |

### 弹窗/底部面板 (Modals & Panels)

| 组件 | ID | 描述 |
|------|-----|------|
| 景点列表弹窗 | `spotDetailPanel` | 可拖拽底部面板, 显示当前区域热门景点 |
| 摄影作品详情 | `photoDetailPanel` | 照片网格 + 拖拽手柄 |
| 避雷详情弹窗 | `avoidDetailPanel` | 差评/中评/好评分类 + 语音评价 |
| 轮播卡片 | `carouselOverlay` | 地图上的景点轮播卡片 |
| 城市选择弹窗 | `cityPickerModal` | 省份→城市 二级选择 |
| 日历弹窗 | `calendarModal` | 日期范围选择 + 灵活天数开关 |
| 分享弹窗 | `shareModal` | 共同编辑/长图/找搭子/求助 + 复制链接/微信等 |
| 添加景点弹窗 | (动态) | 收藏/住宿/自定义/搜索 四种子面板 |
| 雨燕聊天弹窗 | (动态) | AI对话 + 语音录制 + 规划日志 |
| 景点编辑弹窗 | (动态) | 时间/描述/照片编辑 |
| 编辑操作弹窗 | (动态) | 批量操作(移至/删除) |
| 确认删除弹窗 | (动态) | 删除确认对话框 |
| 移动至弹窗 | (动态) | 移动景点到指定天数 |
| 排序面板 | (动态) | 行程排序/置顶 |
| 时长选择器 | (动态) | 滚轮式天数选择 |
| 行程筛选下拉 | `tripFilterDropdown` | 排序(编辑时间/出行时间) + 日期(全部/有日期/无日期) |

---

## 2. 底部导航

```html
<div class="bottom-nav">  <!-- fixed, bottom:0, height:83px, bg:#7C9A3D, border-radius:24px 24px 0 0 -->
  <div class="nav-item" onclick="switchTab('trip')">    <!-- 图标: 路书(book SVG) -->
  <div class="nav-item" onclick="showCreatePage()">     <!-- 图标: 规划(+) -->
  <div class="nav-item" onclick="switchTab('explore')"> <!-- 图标: 发现(compass SVG) -->
  <div class="nav-item" onclick="switchTab('profile')"> <!-- 图标: 我的(person SVG) -->
</div>
```

- **4个Tab**: 路书 / 规划 / 发现 / 我的
- 激活态: `color: #FFFFFF`, 非激活: `rgba(255,255,255,0.6)`
- 图标尺寸: 28px, 标签: 12px
- "规划"Tab 调用 `showCreatePage()` 而非 `switchTab()`

---

## 3. 主要 UI 组件

### 3.1 行程卡片 (`.topic-card`)
- 尺寸: 140×200px, border-radius: 16px
- 背景图 + 渐变遮罩 + 文字叠加
- 显示: 偏好标签 / 时长 / 目的地 / 用户头像 / 协作按钮
- 容器: `.horizontal-scroll` (横向滚动, 分页效果)

### 3.2 路书卡片 (`.roadbook-card`)
- 全宽, 150px高, border-radius: 16px
- 左侧信息 + 右侧倾斜图片 (rotate: 3deg)
- 支持左滑操作: 收藏 / 不推荐 / 分享 (`.roadbook-slide-actions`)

### 3.3 景点卡片 (`.spot-card`)
- 80×80px 图片 + 信息区
- 显示: 类型/名称/时间/描述/距离
- 编辑模式: 左侧选择圆点 + 右侧拖拽手柄
- 支持左滑操作 (`.spot-swipe-actions`)

### 3.4 可拖拽底部面板 (`.bottom-panel`)
- 全屏地图上的底部面板
- 拖拽手柄 (`.drag-handle`) + 面板内容
- 三种状态: 半屏 / 展开 / 收起
- 面板顶部浮动按钮: 推荐地点开关 + 地图适配按钮

### 3.5 地图集成 (高德地图 AMap)
- **exploreMap**: 发现页面全屏地图
- **detailMap**: 行程详情全屏地图
- **resultMap**: 规划结果地图 (250px高)
- **planningMap**: 规划进度地图 (40%高)
- **profileMap**: 个人足迹地图 (180px高)
- 使用 `AMap.Map`, `AMap.Marker`, `AMap.Polyline`
- 自定义标记样式 (编号圆点、照片缩略图)
- 隐藏了高德 logo 和版权信息

### 3.6 轮播卡片 (`.carousel-overlay`)
- 覆盖在地图上的卡片轮播
- 375px宽, 170px高
- 卡片: 80×80 图片 + 标题/描述/标签
- 指示器: 圆点, 激活态变为长条形

### 3.7 城市选择器
- 弹窗式: `.city-picker-modal`
- 两级: 省份列表 → 城市列表
- 搜索过滤城市
- 返回按钮回到省份视图

### 3.8 避雷功能 (Avoid/Thunder)
- 地图标记 + 详情弹窗 (`.avoid-detail-panel`)
- 三类评价: 差评(红)/中评(橙)/好评(绿)
- 支持文字 + 图片 + 语音评价
- 点赞功能
- 发布栏: 文字输入 + 语音录制

### 3.9 广场功能 (Plaza/Social)
- 朋友圈式信息流
- Tab: 广场 / 关注 / 本地
- 帖子: 头像/名称/时间 + 内容 + 图片轮播 + 点赞/评论/分享
- 关注按钮
- 发布 FAB

### 3.10 摄影模式
- 地图上的照片缩略图标记 (60×60, border-radius: 12px)
- 点击展开详情面板: 照片网格 (2列)
- 显示: 照片数/距离/作者/点赞/浏览

### 3.11 日历弹窗
- 月份视图 + 日期范围选择
- 灵活天数开关 (切换为滚轮视图)
- 已选日期高亮, 范围内日期灰色背景

### 3.12 分享弹窗
- 两行:
  - 大图标: 共同编辑 / 长图分享 / 找搭子 / 行程求助
  - 小图标: 复制链接 / 微信好友 / 朋友圈 / 雨燕广场 / 更多

### 3.13 AI 聊天弹窗 (雨燕聊天)
- 天数 Tab + 消息列表
- 用户/机器人消息气泡
- 规划日志动画
- 快速标签 (如"帮我调整第二天行程")
- 输入栏: 文本框 + 语音 + 发送
- 语音录制浮层: 波形动画 + 计时器

### 3.14 个人页面 (Profile)
- 头像/名称/简介
- 统计: 关注/粉丝/收藏/行程
- 足迹地图 (可缩小)
- 打卡城市印章 (圆形, 旋转-8度)
- Tab: 作品/日常/推荐/收藏/喜欢
- 照片网格 (2列)

### 3.15 设置页面
- 封面照片 + 行程名称 + 旅行周期
- 出行方式 (多选分段: 步行/驾车/公交)
- 每日预算 / 提前提醒
- 通知开关: 行程提醒/天气预警/新消息
- 隐私: 可见性/评论/私信
- 其他: 关于/协议/隐私政策

---

## 4. JavaScript 函数清单

### 全局状态
```javascript
selectedDestinations = [];      // 已选目的地
selectedPreferences = [];       // 旅行偏好
currentTab = 'trip';            // 当前Tab
exploreMap / resultMap / planningMap / detailMap = null;  // 地图实例
currentCategory = '景点';       // 当前分类
calendarStartDate / calendarEndDate = null;  // 日历选择
isSelectingStart = true;        // 日历选择状态
currentDayIndex = -1;           // 当前天数索引
panelExpanded = false;          // 面板展开状态
exploreMode = 'spots';          // 发现页模式
isCarouselMode = false;         // 轮播模式
currentSelectedCity = '芜湖市'; // 当前城市
```

### 初始化
- `DOMContentLoaded` → `initExploreMap()`, `initSpotDrag()`, `renderSpotList('景点')`, `initCalendar()`, `initTripScroll()`

### 页面切换
- `switchTab(tab)` - 主页Tab切换 (trip/explore/profile)
- `showCreatePage()` - 显示创建行程页
- `closeCreatePage()` - 关闭创建行程页
- `showTripDetail()` - 显示行程详情
- `closeTripDetail()` - 关闭行程详情
- `showTripListPage()` / `closeTripListPage()` - 行程列表页
- `showRoadbookFilter()` / `closeRoadbookFilter()` - 路书筛选页
- `showResultPage()` / `closeResultPage()` - 规划结果页
- `showSettingsPage()` / `closeSettingsPage()` - 设置页
- `showPlazaPage()` / `closePlazaPage()` - 广场页

### 地图功能
- `initExploreMap()` - 初始化发现页地图 (center: [118.796877, 31.547348], zoom: 8)
- `switchExploreMode(mode)` - 切换模式 (spots/photo/tracks/avoid)
- `clearExploreMarkers()` - 清除标记
- `loadSpotsMode()` - 加载景点标记
- `loadPhotoMode()` - 加载摄影标记
- `loadAvoidMode()` - 加载避雷标记
- `loadTracksMode()` - 加载广场模式
- `initResultMap(center)` - 结果页地图
- `initPlanningMap()` - 规划进度地图
- `initDetailMap()` - 行程详情地图
- `updateDetailMapMarkers()` - 更新详情地图标记
- `toggleMapType()` - 切换列表/地图视图
- `fitMapToRoute()` - 地图适配路线
- `toggleRecommendSpots()` - 推荐地点开关

### 景点/列表
- `renderSpotList(category)` - 渲染景点列表
- `showSpotDetail(spotName)` - 景点详情
- `addToPlan(spotName)` - 添加到行程
- `closeSpotDetail()` - 关闭景点详情

### 轮播
- `renderCarousel()` - 渲染轮播卡片
- `updateCarouselPos()` - 更新轮播位置
- `initCarouselSwipe()` - 轮播滑动手势
- `initCarousel(postId, totalSlides)` - 帖子图片轮播
- `goToSlide(postId, index)` - 跳转到指定幻灯片

### 拖拽/手势
- `initSpotDrag()` - 景点弹窗拖拽
- `initPhotoDrag()` - 摄影弹窗拖拽
- `initAvoidDrag()` - 避雷弹窗拖拽
- `initTripScroll()` - 行程卡片横向滚动 (鼠标+触摸)
- `rbTouchStart/Move/End()` - 路书卡片左滑
- `handleTouchStart/Move/End()` - 路书列表卡片左滑
- `startDragSpot(event, spotId)` - 景点拖拽排序
- `setPanelPosition(translateY, height)` - 面板位置设置

### 创建行程
- `handleDestinationInput(value)` - 目的地输入
- `selectDestination(city)` - 选择目的地
- `renderSelectedTags()` - 渲染已选标签
- `removeDestination(dest)` - 移除目的地
- `showCalendar()` / `closeCalendarModal()` - 日历
- `initCalendar()` - 初始化日历
- `selectCalendarDay(day)` - 选择日期
- `toggleFlexibleDays()` - 灵活天数
- `togglePreference(el)` - 偏好选择
- `startPlanning()` - 开始规划 (显示进度页)
- `cancelPlanning()` - 取消规划
- `createEmptyPlan()` - 创建空计划

### 行程详情
- `switchDay(dayIdx)` - 切换天数Tab
- `addNewDay()` - 添加新天
- `toggleEditMode()` - 编辑模式
- `showAddSpotModal()` / `closeAddSpotModal()` - 添加景点弹窗
- `switchAddDay(dayIdx, el)` - 切换添加天数
- `showAddSubPanel(type)` - 子面板 (fav/hotel/custom/search)
- `addFavToDay(name)` - 添加收藏到天数
- `addHotelToDay(name)` - 添加住宿
- `addCustomToDay()` - 添加自定义景点
- `addSearchSpotToDay(name)` - 搜索添加景点
- `addToSpecificDay(dayIdx, spotData)` - 添加到指定天

### 编辑模式
- `toggleEditMode()` - 编辑模式开关
- `showEditActions()` - 编辑操作弹窗
- `closeEditActions()` - 关闭编辑操作
- `doEditAction(action)` - 执行编辑操作 (move/delete/copy)
- `showDeleteConfirmModal()` / `closeConfirmDelete()` - 删除确认
- `showMoveToModal()` / `closeMoveToModal()` / `doMoveTo(targetDayIdx)` - 移动景点
- `showSpotEditOptions(spotId, event)` - 景点编辑选项
- `saveSpotEdit(spotId)` - 保存景点编辑
- `renderSpotPhotos()` / `removeSpotPhoto()` / `addSpotPhoto()` - 照片管理

### 雨燕聊天 (AI)
- `showYuyanChatModal()` / `closeYuyanChatModal()` - 聊天弹窗
- `switchYuyanDay(dayIdx, el)` - 切换天数
- `sendYuyanQuickMsg(text)` - 快速消息
- `sendYuyanMsg()` - 发送消息
- `appendYuyanMsg(type, text)` - 添加消息
- `appendYuyanPlanMsg(msgId, logs, originalText)` - 规划消息
- `generatePlanningLogs(text, dayIdx)` - 生成规划日志
- `confirmYuyanPlan(originalText)` - 确认规划
- `viewUpdatedPlan(originalText)` - 查看更新规划
- `applyFreePlan/checkinPlan/foodPlan/genericPlan()` - 应用规划模板
- `startVoiceRecord()` / `cancelVoiceRecord()` / `confirmVoiceRecord()` - 语音录制

### 避雷功能
- `showAvoidDetail(spot)` - 避雷详情
- `filterAvoidReviews(type)` - 筛选评价
- `renderAvoidReviews(type)` - 渲染评价
- `closeAvoidDetail()` - 关闭避雷详情
- `toggleAvoidLike(el, key)` - 点赞
- `playAvoidAudio(el, duration)` - 播放语音
- `publishAvoidAudio()` - 发布语音评价

### 广场/社交
- `showPlazaPage()` / `closePlazaPage()` - 广场页
- `switchPlazaTab(element, tab)` - 广场Tab
- `loadPlazaContent(type)` - 加载内容
- `toggleFollow(postId)` - 关注/取关
- `shareToPlaza()` - 分享到广场

### 分享
- `showShareModal()` / `closeShareModal()` - 分享弹窗
- `shareCoEdit()` - 共同编辑
- `shareLongImage()` - 长图分享
- `shareFindPartner()` - 找搭子
- `shareTripHelp()` - 行程求助
- `shareCopyLink()` - 复制链接
- `shareWechatFriend()` / `shareWechatMoments()` - 微信分享
- `shareMore()` - 更多

### 个人页面
- `initProfileScroll()` - 滚动缩小地图
- `scrollProfileTop()` - 回到顶部
- `switchProfileTab(el, tab)` - Tab切换
- `initProfileMap()` - 足迹地图
- `renderProfileContent(tab)` - 渲染内容

### 路书筛选
- `showFilterPanel(type)` / `closeFilterPanel()` - 筛选面板
- `selectProvince(el, province, idx)` / `selectCity(el)` - 途经地选择
- `selectOption(el)` - 选项选择
- `confirmLocationFilter()` / `confirmDaysFilter()` / `confirmSeasonFilter()` / `confirmFeatureFilter()` - 确认筛选

### 设置
- `saveSettings()` - 保存设置
- `selectSegment(el)` / `toggleMultiSegment(el)` - 分段选择
- `toggleSetting(el)` - 开关设置
- `editSetting(name, currentValue)` - 编辑设置
- `changeCoverPhoto()` - 更换封面
- `showDurationPicker()` - 时长选择器
- `initDurationWheels()` - 滚轮初始化
- `confirmDuration()` - 确认时长
- `clearCache()` / `doClearCache()` - 清除缓存
- `checkUpdate()` - 检查更新

### 城市选择
- `openCityPicker()` / `closeCityPicker()` - 城市选择弹窗
- `renderProvinceList()` - 省份列表
- `selectProvince(province)` - 选择省份
- `pickCity(cityName)` - 选择城市
- `locateCurrentCity()` - 定位当前城市
- `filterCities(keyword)` - 搜索城市

### 工具
- `showToast(message)` - Toast提示
- `confirmDeleteTrip(el)` - 删除行程确认
- `showCollabInvite(el)` - 协作邀请

---

## 5. 色彩方案

| 用途 | 颜色值 |
|------|--------|
| **主色 (Primary)** | `#7C9A3D` (橄榄绿) |
| 主色按下态 | `#6a8a33` / `#5a7a2a` |
| 主色浅底 | `#f0f7e6`, `#E8F0D8` |
| **背景色** | `#FFFFFF` (白) |
| 页面背景 | `#F5F5F5`, `#F5F5DC` (米色) |
| 卡片背景 | `#f9f9f9`, `#fafafa` |
| **文字色** | `#1A1A1A` (主文字) |
| 次要文字 | `#333`, `#666` |
| 辅助文字 | `#999`, `#aaa`, `#bbb`, `#ccc` |
| **功能色** | |
| 差评红 | `#ff4444`, `#d32f2f` |
| 中评橙 | `#ff9800`, `#f57c00` |
| 好评绿 | `#4caf50`, `#388e3c` |
| 链接蓝 | `#1890FF`, `#3B82F6` |
| 删除红 | `#EF4444` |
| 标签橙 | `#FF6B35` |
| **分割线** | `#f0f0f0`, `#f5f5f5`, `#e8e8e8`, `#E5E5E5` |

---

## 6. 数据源

### 硬编码数据
- `cityDatabase` - 8个城市 (苏州/杭州/北京/上海/南京/无锡/扬州/常州)
- `spotDetails` - 10个景点详情
- `tripData` - 行程详情 (7天6晚, 含每日景点)
- `spotsData` - 6个苏州景点详细信息
- `yanchengSpots` - 盐城景点列表
- `avoidData` - 6个避雷景点 (各含3-4条评价)
- `provinceCityData` - 14个省份城市数据
- `recommendSpotsData` - 推荐景点

### 图片 URL
- 本地: `./北京雨燕1.0版_files/photo-*` (Unsplash 下载图)
- Unsplash: `https://images.unsplash.com/photo-*`
- Picsum: `https://picsum.photos/400/300?random=*`
- Pravatar: `https://i.pravatar.cc/100?img=*`, `https://i.pravatar.cc/150?img=*`
- Randomuser: `https://randomuser.me/api/portraits/*`

### 外部 API
- 高德地图 JS API (AMap)

---

## 7. 外部依赖

| 依赖 | 路径/URL | 用途 |
|------|----------|------|
| 高德地图 JS API | `./北京雨燕1.0版_files/maps` (本地缓存) | 地图渲染 |
| 系统字体 | `-apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', sans-serif` | 字体 |

**无其他框架/库依赖** - 纯原生 HTML/CSS/JS

---

## 8. 布局规格

### 全局
- 最大宽度: `430px`
- 居中: `margin: 0 auto`, `left: 50%; transform: translateX(-50%)`
- 圆角: `16px` (卡片), `20px` (面板), `24px` (按钮/大面板), `28px` (FAB按钮), `8px`-`12px` (小元素)

### 底部导航
- 高度: `83px` (含 `padding-bottom: 20px`)
- 圆角: `24px 24px 0 0`
- z-index: `100`

### 状态栏
- 高度: `44px`

### 间距
- 页面内边距: `16px`
- 卡片间距: `12px` (gap)
- 模块间距: `16px` (margin-top)

### 字体大小
- 页面标题: `24px` / `22px` / `20px`
- 模块标题: `18px` / `17px` / `16px`
- 正文: `15px` / `14px` / `13px`
- 辅助: `12px` / `11px` / `10px`
- 导航标签: `12px`

### z-index 层级
- 底部导航: `100`
- 弹窗: `1000`-`3001`
- 地图控件: `10`-`2001`
- Toast: `100000`

---

## 9. 特殊行为/交互

### 拖拽手势
- **底部面板拖拽**: `initSpotDrag()` - 三态 (半屏/展开/收起), 使用 touch 事件
- **摄影弹窗拖拽**: `initPhotoDrag()`
- **避雷弹窗拖拽**: `initAvoidDrag()`
- **景点卡片拖拽排序**: `startDragSpot()` - 编辑模式下拖拽排序
- **行程卡片横向滚动**: `initTripScroll()` - 鼠标拖拽 + 触摸滑动

### 左滑操作
- **路书卡片**: `rbTouchStart/Move/End()` - 左滑显示 收藏/不推荐/分享
- **行程列表卡片**: 左滑显示操作按钮
- **景点卡片**: 左滑显示操作按钮
- **路书列表卡片**: `handleTouchStart/Move/End()` - 左滑显示 收藏/删除

### 动画
- `@keyframes slideUp` - 面板上滑进入
- `@keyframes dropdownFadeIn` - 下拉菜单淡入
- `@keyframes pulse-ring` - 语音录制脉冲
- `@keyframes voiceWave` - 语音波形动画
- 过渡: `transition: all 0.3s ease` (通用), `0.2s` (按钮)

### 吸顶 (Sticky)
- `.section-title.sticky` - 模块标题吸顶 (top: 0, z-index: 11)
- `.section-title.sticky-sub` - 子标题吸顶 (top: 34px, z-index: 10)
- `.trip-header` - 行程标题吸顶
- `.day-tabs-container` - 天数Tab吸顶 (top: 60px)
- `.profile-tabs` - 个人Tab吸顶

### 编辑模式
- `body.edit-mode` class 控制
- 显示: 选择圆点 / 拖拽手柄 / 完成按钮
- 隐藏: 编辑按钮
- 底部编辑操作栏

### 地图交互
- 景点标记点击 → 轮播卡片 / 详情面板
- 地图/列表视图切换
- 路线 polyline 绘制
- 推荐地点标记开关

---

## 10. 城市/省份选择

### 数据结构
```javascript
provinceCityData = {
    '江苏省': { count: 13, cities: ['南京市','苏州市',...] },
    '安徽省': { count: 16, cities: ['合肥市','芜湖市',...] },
    '浙江省': { count: 11, cities: ['杭州市','宁波市',...] },
    '山东省': { count: 16, cities: [...] },
    '河南省': { count: 18, cities: [...] },
    '湖北省': { count: 13, cities: [...] },
    '湖南省': { count: 14, cities: [...] },
    '广东省': { count: 21, cities: [...] },
    '四川省': { count: 21, cities: [...] },
    '福建省': { count: 9, cities: [...] },
    '江西省': { count: 11, cities: [...] },
    '北京市': { count: 1, cities: ['北京市'] },
    '上海市': { count: 1, cities: ['上海市'] },
    '天津市': { count: 1, cities: ['天津市'] },
    '重庆市': { count: 1, cities: ['重庆市'] }
};
```

### 交互流程
1. 点击城市选择器 → 显示省份列表
2. 点击省份 → 显示该省城市列表 + 搜索框
3. 点击城市 → 切换当前城市, 关闭弹窗
4. "← 返回省份" 回到省份列表
5. 搜索框实时过滤城市

### 城市数据库 (cityDatabase)
```javascript
{
    '苏州': { name: '苏州市', province: '江苏省', spots: ['拙政园','狮子林',...] },
    '杭州': { name: '杭州市', province: '浙江省', spots: [...] },
    // ... 8个城市
}
```

---

## 11. 定位/位置功能

- `locateCurrentCity()` - 模拟定位当前城市 (Toast提示)
- 地图初始化中心: `[118.796877, 31.547348]` (约芜湖/南京区域)
- 景点距离计算: 硬编码距离值
- 行程详情地图标记: 使用 `location: [lng, lat]` 坐标

---

## 12. 旅行偏好标签

```
📍 经典必玩 | 🍽️ 吃吃喝喝 | 🕵️ 小众探索 | 📸 拍照出片
🛍️ 逛街购物 | 🚶 citywalk | 🏔️ 自然风光 | 🎨 文艺展览 | 🏛️ 历史古建
```

---

## 13. 路书筛选维度

| 维度 | 选项 |
|------|------|
| 途经地 | 省份→城市 二级选择 |
| 天数 | 不限 / 1天 / 2天 / 3天 / 4-7天 / 8天及以上 |
| 季节 | 四季 / 春季 / 夏季 / 秋季 / 冬季 |
| 特色 | 古镇/亲子/登山/海边/越野/漂流/人文/森林/湖泊/美食/滑雪/草原/沙漠/钓鱼/温泉 |

---

## 14. 关键实现细节

1. **纯原生实现** - 无任何框架依赖, 所有交互使用原生 DOM API
2. **页面切换** - 通过 `.page.active` class 控制显示/隐藏
3. **覆盖页面** - 使用 `position: fixed` + z-index 层级
4. **数据驱动** - 大部分动态内容通过 innerHTML 渲染
5. **地图实例** - 全局变量管理, 切换时 resize/destroy
6. **触摸优化** - `-webkit-tap-highlight-color: transparent`, `touch-action`
7. **滚动优化** - `-webkit-overflow-scrolling: touch`, `overscroll-behavior-y: contain`
8. **滚动条隐藏** - `scrollbar-width: none` + `::-webkit-scrollbar { display: none }`

---

## 15. 文件结构概览

```
Lines 1-6:     HTML head + AMap 内联样式 (base64 背景)
Lines 7:       AMap 脚本引用
Lines 8-5260:  <style> 自定义样式 (~5250行)
Lines 5261-6496: <body> HTML 结构 (~1235行)
Lines 6497-13064: <script> JavaScript (~6567行)
Lines 13065-13080: 城市选择弹窗 HTML + 闭合标签
```
