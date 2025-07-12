#!/usr/bin/env python3
"""
简单的 Claude Code CLI 调用示例
"""

from claude_cli_client import ClaudeCodeClient

def main():
    client = ClaudeCodeClient()
    
    # 简单测试
    print("测试 Claude Code CLI 调用:")
    response = client.send_message("用一句话介绍你自己")
    print(f"Claude: {response}")
    
    # 编程任务测试
    print("\n编程任务测试:")
    code_response = client.code_task("写一个Python函数来判断一个数字是否为质数")
    print(f"代码生成: {code_response}")

if __name__ == "__main__":
    main()