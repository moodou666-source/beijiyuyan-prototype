# 飞书机器人配置指南

## 创建步骤

### 1. 登录飞书开放平台
访问：https://open.feishu.cn/

### 2. 创建企业自建应用
- 点击「创建企业自建应用」
- 应用名称：`墨墨 - 展厅设计` / `墨墨 - PPT` / `墨墨 - 开发` / `墨墨 - 视频`
- 应用图标：可上传对应图标区分

### 3. 获取凭证信息
每个应用需要记录以下信息：
- **App ID** (cli_xxxxxxxx)
- **App Secret** (xxxxxxxx)
- **Verification Token** (用于事件订阅)
- **Encrypt Key** (如果启用加密)

### 4. 配置权限
每个机器人需要的基础权限：
- 消息读写权限
- 群组读写权限
- 机器人信息权限

### 5. 配置事件订阅
- 启用事件订阅
- 填写请求地址（OpenClaw 的回调 URL）
- 订阅事件：`im.message.receive_v1`

### 6. 发布应用
- 点击「发布」
- 在飞书中搜索并添加机器人到聊天

---

## 凭证存储

将每个机器人的凭证存入 1Password 或环境变量：

```bash
# 展厅设计机器人
FEISHU_EXHIBITION_APP_ID=cli_xxx
FEISHU_EXHIBITION_APP_SECRET=xxx
FEISHU_EXHIBITION_TOKEN=xxx

# PPT 机器人
FEISHU_PPT_APP_ID=cli_xxx
FEISHU_PPT_APP_SECRET=xxx
FEISHU_PPT_TOKEN=xxx

# 开发机器人
FEISHU_DEV_APP_ID=cli_xxx
FEISHU_DEV_APP_SECRET=xxx
FEISHU_DEV_TOKEN=xxx

# 视频机器人
FEISHU_VIDEO_APP_ID=cli_xxx
FEISHU_VIDEO_APP_SECRET=xxx
FEISHU_VIDEO_TOKEN=xxx
```

---

## OpenClaw 配置

在 `~/.openclaw/config.json` 或对应配置文件中添加多账号配置。
