#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import calendar
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# 读取用户提供的图片
user_image_path = "/root/.openclaw/media/inbound/0fb2a972-9c57-4259-a0d3-2eaeb41bc576.jpg"
output_path = "/root/.openclaw/workspace/calendar_february_2026.jpg"

# 打开用户图片
user_img = Image.open(user_image_path)

# 调整图片大小为背景
width, height = 1000, 1200
user_img = user_img.resize((width, height), Image.LANCZOS)

# 创建透明层用于绘制日历
overlay = Image.new('RGBA', (width, height), (255, 255, 255, 230))
draw = ImageDraw.Draw(overlay)

# 在底部创建日历区域
calendar_height = 400
calendar_y = height - calendar_height

# 绘制日历背景
draw.rectangle([0, calendar_y, width, height], fill=(255, 255, 255, 245))

# 设置字体
try:
    title_font = ImageFont.truetype("/usr/share/fonts/truetype/DejaVuSans-Bold.ttf", 36)
    day_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
except:
    title_font = ImageFont.load_default()
    day_font = ImageFont.load_default()

# 标题
year = 2026
month = 2
month_name = "二月"
title = f"{year}年 {month_name}"
title_width = draw.textlength(title, font=title_font)
draw.text(((width - title_width) // 2, calendar_y + 20), title, fill=(50, 50, 100), font=title_font)

# 星期标题
weekdays = ["日", "一", "二", "三", "四", "五", "六"]
cell_width = width // 7
for i, day in enumerate(weekdays):
    draw.text((i * cell_width + cell_width // 2 - 12, calendar_y + 70), day, fill=(80, 80, 80), font=day_font)

# 获取日历数据
cal = calendar.Calendar()
month_days = cal.itermonthdays(year, month)
days_list = list(month_days)

# 今天日期
today = 22

# 绘制日期
row = 0
col = 0
start_x = 10
start_y = calendar_y + 110
cell_w = (width - 20) // 7
cell_h = 60

for day in days_list:
    if day == 0:
        col += 1
        if col == 7:
            col = 0
            row += 1
        continue

    x = start_x + col * cell_w
    y = start_y + row * cell_h

    # 如果是今天，用不同颜色
    if day == today:
        draw.rectangle([x, y, x + cell_w - 4, y + cell_h - 4], fill=(100, 149, 237), outline=(255, 255, 255), width=2)
        text_color = (255, 255, 255)
    else:
        text_color = (60, 60, 60)

    draw.text((x + cell_w // 2 - 8, y + cell_h // 2 - 10), str(day), fill=text_color, font=day_font)

    col += 1
    if col == 7:
        col = 0
        row += 1

# 合并图片
result = Image.alpha_composite(user_img.convert('RGBA'), overlay)

# 保存
result.convert('RGB').save(output_path, 'JPEG', quality=95)

print(f"日历已生成: {output_path}")
