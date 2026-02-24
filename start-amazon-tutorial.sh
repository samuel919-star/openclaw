#!/bin/bash
# 亚马逊初学者教程启动器

echo "🚀 启动亚马逊初学者教程..."
echo ""

# 检查文件是否存在
if [ ! -f "amazon-beginner-tutorial.html" ]; then
    echo "❌ 错误：找不到教程文件 amazon-beginner-tutorial.html"
    echo "请确保你在正确的目录中运行此脚本"
    exit 1
fi

# 获取当前目录的绝对路径
TUTORIAL_PATH="$(pwd)/amazon-beginner-tutorial.html"

# 检测操作系统
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "📱 检测到 macOS，使用默认浏览器打开..."
    open "$TUTORIAL_PATH"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    echo "🐧 检测到 Linux，使用默认浏览器打开..."
    if command -v xdg-open > /dev/null; then
        xdg-open "$TUTORIAL_PATH"
    elif command -v gnome-open > /dev/null; then
        gnome-open "$TUTORIAL_PATH"
    else
        echo "❌ 无法找到合适的浏览器打开工具"
        echo "📖 请手动打开文件：$TUTORIAL_PATH"
    fi
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Windows
    echo "🪟 检测到 Windows，使用默认浏览器打开..."
    start "$TUTORIAL_PATH"
else
    echo "⚠️ 未知操作系统"
    echo "📖 请手动打开文件：$TUTORIAL_PATH"
fi

echo ""
echo "✅ 教程已在浏览器中打开"
echo ""
echo "📚 学习提示："
echo "   - 使用 ← → 按钮切换章节"
echo "   - 完成小测验和练习"
echo "   - 使用费用计算器规划你的业务"
echo ""
echo "祝你学习愉快！🎉"
