#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简易 Todo List 程序
支持：添加、查看、完成、删除任务，数据持久化到 JSON 文件
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path


class TodoList:
    def __init__(self, data_file="todos.json"):
        self.data_file = Path(data_file)
        self.todos = self._load_todos()

    def _load_todos(self):
        """从文件加载待办事项"""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载数据失败: {e}")
                return []
        return []

    def _save_todos(self):
        """保存待办事项到文件"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.todos, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存数据失败: {e}")

    def add(self, task, priority="normal"):
        """添加任务"""
        todo = {
            "id": len(self.todos) + 1,
            "task": task,
            "done": False,
            "priority": priority,  # high, normal, low
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "completed_at": None
        }
        self.todos.append(todo)
        self._save_todos()
        return todo

    def list_all(self, show_done=True, show_pending=True):
        """列出所有任务"""
        result = []
        for todo in self.todos:
            if todo["done"] and not show_done:
                continue
            if not todo["done"] and not show_pending:
                continue
            result.append(todo)
        return result

    def mark_done(self, task_id):
        """标记任务为完成"""
        for todo in self.todos:
            if todo["id"] == task_id:
                todo["done"] = True
                todo["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self._save_todos()
                return todo
        return None

    def mark_undone(self, task_id):
        """取消完成状态"""
        for todo in self.todos:
            if todo["id"] == task_id:
                todo["done"] = False
                todo["completed_at"] = None
                self._save_todos()
                return todo
        return None

    def delete(self, task_id):
        """删除任务"""
        for i, todo in enumerate(self.todos):
            if todo["id"] == task_id:
                deleted = self.todos.pop(i)
                self._save_todos()
                return deleted
        return None

    def clear_done(self):
        """清除所有已完成的任务"""
        original_count = len(self.todos)
        self.todos = [t for t in self.todos if not t["done"]]
        deleted_count = original_count - len(self.todos)
        self._save_todos()
        return deleted_count


def print_todos(todos, show_details=False):
    """格式化打印任务列表"""
    if not todos:
        print("📝 没有待办事项")
        return

    print("\n📋 待办事项列表")
    print("=" * 50)

    pending = [t for t in todos if not t["done"]]
    done = [t for t in todos if t["done"]]

    if pending:
        print("\n⏳ 进行中:")
        for todo in pending:
            status = "🔴" if todo["priority"] == "high" else "🟡" if todo["priority"] == "normal" else "🟢"
            print(f"  {status} [{todo['id']}] {todo['task']}")
            if show_details:
                print(f"      创建于: {todo['created_at']}")

    if done:
        print("\n✅ 已完成:")
        for todo in done:
            print(f"  ✅ [{todo['id']}] {todo['task']}")
            if show_details:
                print(f"      完成于: {todo['completed_at']}")

    print(f"\n总计: {len(todos)} 项 ({len(pending)} 进行中, {len(done)} 已完成)")
    print("=" * 50)


def print_help():
    """打印帮助信息"""
    help_text = """
╔═══════════════════════════════════════════════════════════════╗
║                    📝 Todo List 程序                          ║
╚═══════════════════════════════════════════════════════════════╝

用法:
  python todo_cli.py [命令] [参数]

命令:
  add <任务内容> [优先级]     添加任务 (优先级: high/normal/low)
  list [all|pending|done]    查看任务列表
  done <ID>                  标记任务为完成
  undo <ID>                  取消完成
  del <ID>                   删除任务
  clear                      清除所有已完成的任务
  help                       显示帮助信息

示例:
  python todo_cli.py add "写代码"
  python todo_cli.py add "完成报告" high
  python todo_cli.py list
  python todo_cli.py done 1
  python todo_cli.py del 1
  python todo_cli.py clear

或直接运行交互模式:
  python todo_cli.py
    """
    print(help_text)


def interactive_mode():
    """交互模式"""
    todo = TodoList()
    print("\n📝 Todo List - 交互模式")
    print("输入 'help' 查看帮助，'quit' 退出\n")

    while True:
        try:
            cmd = input("\n➤ ").strip()
            if not cmd:
                continue

            if cmd.lower() in ['quit', 'exit', 'q']:
                print("👋 再见！")
                break

            parts = cmd.split(maxsplit=2)
            action = parts[0].lower()

            if action == 'help':
                print_help()

            elif action == 'list':
                filter_type = parts[1] if len(parts) > 1 else 'all'
                if filter_type == 'pending':
                    todos = todo.list_all(show_done=False)
                elif filter_type == 'done':
                    todos = todo.list_all(show_pending=False)
                else:
                    todos = todo.list_all()
                print_todos(todos, show_details=True)

            elif action == 'add':
                if len(parts) < 2:
                    print("❌ 请输入任务内容")
                    continue
                task = parts[1]
                priority = parts[2] if len(parts) > 2 else 'normal'
                if priority not in ['high', 'normal', 'low']:
                    priority = 'normal'
                todo.add(task, priority)
                print(f"✅ 已添加: {task}")

            elif action == 'done':
                if len(parts) < 2:
                    print("❌ 请输入任务 ID")
                    continue
                task_id = int(parts[1])
                result = todo.mark_done(task_id)
                if result:
                    print(f"✅ 已完成: {result['task']}")
                else:
                    print("❌ 未找到该任务")

            elif action == 'undo':
                if len(parts) < 2:
                    print("❌ 请输入任务 ID")
                    continue
                task_id = int(parts[1])
                result = todo.mark_undone(task_id)
                if result:
                    print(f"↩️ 已恢复: {result['task']}")
                else:
                    print("❌ 未找到该任务")

            elif action == 'del':
                if len(parts) < 2:
                    print("❌ 请输入任务 ID")
                    continue
                task_id = int(parts[1])
                result = todo.delete(task_id)
                if result:
                    print(f"🗑️ 已删除: {result['task']}")
                else:
                    print("❌ 未找到该任务")

            elif action == 'clear':
                count = todo.clear_done()
                print(f"🗑️ 已清除 {count} 项已完成任务")

            else:
                print(f"❌ 未知命令: {action}")
                print("输入 'help' 查看帮助")

        except KeyboardInterrupt:
            print("\n👋 再见！")
            break
        except Exception as e:
            print(f"❌ 错误: {e}")


def main():
    """主函数"""
    if len(sys.argv) == 1:
        # 没有参数，进入交互模式
        interactive_mode()
        return

    todo = TodoList()
    action = sys.argv[1].lower()

    if action == 'help':
        print_help()

    elif action == 'add':
        if len(sys.argv) < 3:
            print("❌ 用法: python todo_cli.py add <任务内容> [优先级]")
            return
        task = sys.argv[2]
        priority = sys.argv[3] if len(sys.argv) > 3 else 'normal'
        if priority not in ['high', 'normal', 'low']:
            priority = 'normal'
        todo.add(task, priority)
        print(f"✅ 已添加: {task}")

    elif action == 'list':
        filter_type = sys.argv[2] if len(sys.argv) > 2 else 'all'
        if filter_type == 'pending':
            todos = todo.list_all(show_done=False)
        elif filter_type == 'done':
            todos = todo.list.list(show_pending=False)
        else:
            todos = todo.list_all()
        print_todos(todos)

    elif action == 'done':
        if len(sys.argv) < 3:
            print("❌ 用法: python todo_cli.py done <ID>")
            return
        task_id = int(sys.argv[2])
        result = todo.mark_done(task_id)
        if result:
            print(f"✅ 已完成: {result['task']}")
        else:
            print("❌ 未找到该任务")

    elif action == 'undo':
        if len(sys.argv) < 3:
            print("❌ 用法: python todo_cli.py undo <ID>")
            return
        task_id = int(sys.argv[2])
        result = todo.mark_undone(task_id)
        if result:
            print(f"↩️ 已恢复: {result['task']}")
        else:
            print("❌ 未找到该任务")

    elif action == 'del':
        if len(sys.argv) < 3:
            print("❌ 用法: python todo_cli.py del <ID>")
            return
        task_id = int(sys.argv[2])
        result = todo.delete(task_id)
        if result:
            print(f"🗑️ 已删除: {result['task']}")
        else:
            print("❌ 未找到该任务")

    elif action == 'clear':
        count = todo.clear_done()
        print(f"🗑️ 已清除 {count} 项已完成任务")

    else:
        print(f"❌ 未知命令: {action}")
        print("运行 'python todo_cli.py help' 查看帮助")


if __name__ == "__main__":
    main()
