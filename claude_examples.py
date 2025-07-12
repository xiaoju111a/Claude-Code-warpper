#!/usr/bin/env python3
"""
Claude Code CLI 使用示例
演示如何通过脚本调用 Claude Code CLI 完成各种编程任务
"""

from claude_cli_client import ClaudeCodeClient
import os

def main():
    client = ClaudeCodeClient()
    
    print("=== Claude Code CLI 客户端示例 ===\n")
    
    # 1. 基本对话
    print("1. 基本对话:")
    response = client.send_message("解释什么是递归")
    print(f"回复: {response[:200]}...\n")
    
    # 2. 代码生成
    print("2. 代码生成:")
    code_task = client.code_task("用Python写一个计算斐波那契数列的函数")
    print(f"生成的代码: {code_task[:300]}...\n")
    
    # 3. 文件分析
    print("3. 文件分析:")
    if os.path.exists("demo.py"):
        analysis = client.explain_code("demo.py")
        print(f"代码分析: {analysis[:300]}...\n")
    else:
        print("demo.py 文件不存在，跳过文件分析\n")
    
    # 4. 调试帮助
    print("4. 调试帮助:")
    debug_help = client.debug_issue("Python代码出现 'list index out of range' 错误")
    print(f"调试建议: {debug_help[:300]}...\n")
    
    # 5. 代码审查
    print("5. 代码审查:")
    if os.path.exists("requirements.txt"):
        review = client.review_code("requirements.txt")
        print(f"审查结果: {review[:300]}...\n")
    else:
        print("requirements.txt 文件不存在，跳过代码审查\n")

if __name__ == "__main__":
    main()