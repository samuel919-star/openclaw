#!/usr/bin/env python3
"""
单词学习助手 - 帮助学习英语单词
"""

import random
import os

class WordPractice:
    def __init__(self, level='beginner'):
        self.level = level
        self.words = []
        self.load_words()

    def load_words(self):
        """加载单词列表"""
        if self.level == 'beginner':
            file_path = 'cefr_beginner.txt'
        elif self.level == 'intermediate':
            file_path = 'cefr_intermediate.txt'
        elif self.level == 'advanced':
            file_path = 'english_vocabulary.txt'
        else:
            file_path = 'cefr_beginner.txt'

        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                self.words = [line.strip() for line in f if line.strip() and len(line.strip()) > 2]
            print(f"✅ 已加载 {len(self.words)} 个单词 ({self.level} 级别)")
        else:
            print(f"❌ 找不到文件: {file_path}")

    def random_word(self, count=10):
        """随机选择单词"""
        if not self.words:
            print("没有单词可显示")
            return []

        selected = random.sample(self.words, min(count, len(self.words)))
        return selected

    def practice_session(self, count=10):
        """开始练习"""
        if not self.words:
            print("❌ 请先加载单词")
            return

        print(f"\n📚 开始单词练习 ({self.level} 级别)")
        print("=" * 50)

        words = self.random_word(count)
        for i, word in enumerate(words, 1):
            print(f"{i}. {word}")

        print("\n💡 建议：")
        print("- 查阅每个单词的含义和用法")
        print("- 造句练习")
        print("- 记录生词本")


def main():
    print("📖 单词学习助手")
    print("=" * 50)

    print("\n选择难度级别：")
    print("1. 初级 (Beginner - A1/A2)")
    print("2. 中级 (Intermediate - B1/B2)")
    print("3. 高级 (Advanced)")

    choice = input("\n请输入选项 (1-3): ").strip()

    level_map = {
        '1': 'beginner',
        '2': 'intermediate',
        '3': 'advanced'
    }

    level = level_map.get(choice, 'beginner')

    practice = WordPractice(level)

    if practice.words:
        try:
            count = int(input("\n每次练习几个单词 (默认10): ").strip() or "10")
        except:
            count = 10

        practice.practice_session(count)
    else:
        print("❌ 无法加载单词列表")


if __name__ == '__main__':
    main()
