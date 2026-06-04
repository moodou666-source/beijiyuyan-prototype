#!/bin/bash

# 合并脚本 - 将行程详情页和筛选弹窗功能合并到母版中

BASE_FILE="/Users/jiyi/.openclaw/workspace/北京雨燕-最新版本.html"
SOURCE_FILE="/Users/jiyi/.openclaw/workspace/beijing-yuyan-latest.html"
OUTPUT_FILE="/Users/jiyi/.openclaw/workspace/北京雨燕-合并版.html"

# 创建输出文件
cp "$BASE_FILE" "$OUTPUT_FILE"

echo "合并完成，输出文件: $OUTPUT_FILE"
