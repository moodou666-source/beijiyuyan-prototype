# 北极雨燕 - 设计规范文档

## 色彩系统

### 主色
| 名称 | 色值 | 用途 |
|------|------|------|
| 主橙 | `#FF6B35` | 主按钮、选中状态、强调 |
| 深橙 | `#E85A2D` | 悬停、按下状态 |
| 浅橙 | `#FFF5F0` | 背景、标签底色 |

### 辅助色
| 名称 | 色值 | 用途 |
|------|------|------|
| 深蓝 | `#1A1A2E` | 深色背景、文字 |
| 金黄 | `#FFD93D` | 点缀、高光、评分 |
| 浅灰蓝 | `#F7F9FC` | 页面背景 |

### 中性色
| 名称 | 色值 | 用途 |
|------|------|------|
| 深灰 | `#2D3142` | 主文字 |
| 中灰 | `#8E92BC` | 次要文字 |
| 浅灰 | `#E8E8E8` | 分割线、边框 |
| 白色 | `#FFFFFF` | 卡片背景 |

## 字体规范

### 字体栈
```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
```

### 字号层级
| 级别 | 大小 | 字重 | 用途 |
|------|------|------|------|
| H1 | 28px | Bold | 页面标题 |
| H2 | 22px | Bold | 区块标题 |
| H3 | 18px | Medium | 卡片标题 |
| Body | 16px | Regular | 正文 |
| Small | 14px | Regular | 辅助文字 |
| Caption | 12px | Regular | 标签、时间 |

## 间距系统

### 基础单位: 8px
| Token | 值 | 用途 |
|-------|-----|------|
| xs | 4px | 图标内边距 |
| sm | 8px | 紧凑间距 |
| md | 16px | 标准间距 |
| lg | 24px | 区块间距 |
| xl | 32px | 大区块间距 |
| xxl | 48px | 页面边距 |

## 圆角规范
| Token | 值 | 用途 |
|-------|-----|------|
| sm | 4px | 标签、小按钮 |
| md | 8px | 输入框 |
| lg | 12px | 卡片 |
| xl | 16px | 大卡片 |
| full | 9999px | 按钮、头像 |

## 阴影规范
```css
/* 卡片阴影 */
shadow-card: 0 4px 12px rgba(0, 0, 0, 0.08);

/* 悬浮阴影 */
shadow-hover: 0 8px 24px rgba(0, 0, 0, 0.12);

/* 按钮阴影 */
shadow-button: 0 2px 8px rgba(255, 107, 53, 0.3);
```

## 组件规范

### 按钮

#### 主按钮
```
背景: 渐变 (#FF6B35 → #FF8F5A)
文字: 白色, 16px, Bold
圆角: 24px (全圆角)
高度: 48px
内边距: 0 24px
阴影: shadow-button

状态:
- 正常: 如上
- 悬停: 亮度 +10%
- 按下: 缩放 0.98
- 禁用: 灰色背景, 50% 透明度
```

#### 次要按钮
```
背景: 透明
边框: 1px solid #FF6B35
文字: #FF6B35, 16px, Medium
圆角: 24px

状态:
- 悬停: 浅橙背景
```

#### 图标按钮
```
尺寸: 40×40px
圆角: full
背景: 透明

状态:
- 悬停: 浅灰背景
```

### 输入框
```
背景: #F5F5F5
圆角: 8px
高度: 48px
内边距: 0 16px
字体: 16px

状态:
- 聚焦: 边框 2px #FF6B35
- 错误: 边框 2px #FF4444
```

### 卡片
```
背景: 白色
圆角: 16px
阴影: shadow-card
内边距: 16px

状态:
- 悬停: 阴影 shadow-hover, 上移 2px
```

### 标签
```
背景: #FFF5F0 (浅色) / #FF6B35 (深色)
文字: #FF6B35 (浅色) / 白色 (深色)
圆角: full
内边距: 4px 12px
字体: 12px, Medium
```

## 图标规范
- **风格**: 线性图标，2px 描边
- **尺寸**: 24×24px (标准) / 20×20px (小) / 32×32px (大)
- **颜色**: 跟随文字颜色或橙色强调

## 动画规范

### 时长
| 类型 | 时长 | 用途 |
|------|------|------|
| 快速 | 150ms | 按钮反馈、开关 |
| 标准 | 300ms | 页面切换、弹窗 |
| 缓慢 | 500ms | 加载、复杂动画 |

### 缓动函数
```css
/* 标准 */
ease-standard: cubic-bezier(0.4, 0, 0.2, 1);

/* 进入 */
ease-enter: cubic-bezier(0, 0, 0.2, 1);

/* 退出 */
ease-exit: cubic-bezier(0.4, 0, 1, 1);

/* 弹性 */
ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);
```

### 常用动画
```css
/* 淡入 */
fadeIn: opacity 0→1, 300ms, ease-enter

/* 滑入 */
slideUp: translateY(20px)→0, 300ms, ease-standard

/* 缩放 */
scaleIn: scale(0.9)→1, 300ms, ease-bounce

/* 脉冲 */
pulse: scale(1)→scale(1.05)→scale(1), 2s, infinite
```

## 布局规范

### 安全区
- **顶部**: 状态栏高度 (iOS: 44px, Android: 24px)
- **底部**: 导航栏高度 (iOS: 34px, Android: 0)
- **侧边**: 16px 最小边距

### 网格系统
- **移动端**: 4 列网格
- **平板**: 8 列网格
- **桌面**: 12 列网格
- **间距**: 16px (移动端) / 24px (桌面)

## 地图样式
```javascript
// 地图主题配置
mapStyle: {
  backgroundColor: '#F7F9FC',
  waterColor: '#D4E5F7',
  landColor: '#FFFFFF',
  roadColor: '#FFFFFF',
  roadBorderColor: '#E8E8E8',
  poiColor: '#FF6B35',
  textColor: '#2D3142'
}
```

## 暗黑模式（可选）
```javascript
darkMode: {
  background: '#1A1A2E',
  surface: '#252540',
  primary: '#FF8F5A',
  text: '#FFFFFF',
  textSecondary: '#8E92BC'
}
```

## 文件命名规范
```
assets/
  icons/          # 图标
    ic_home.svg
    ic_map.svg
    ic_user.svg
  images/         # 图片
    logo.png
    splash_bg.jpg
  fonts/          # 字体
    
components/       # 组件
  Button/
    Button.tsx
    Button.styles.ts
  Card/
    Card.tsx
    Card.styles.ts
  
pages/            # 页面
  Home/
  Plan/
  Profile/
```

---
*Version: 1.0.0*
*Last Updated: 2026-04-25*
