#!/usr/bin/env python3
"""
测试本地 Claude 服务器
"""

from claude_cli_client import ClaudeCodeClient
import time

def test_local_server():
    print("=== 测试本地 Claude 服务器 ===\n")
    
    # 创建客户端，指向本地服务器
    client = ClaudeCodeClient(
        api_key="test-key",
        base_url="http://localhost:8000"
    )
    
    # 测试基本消息
    print("1. 基本消息测试:")
    response = client.send_message("你好，请简单介绍一下你自己")
    print(f"回复: {response}\n")
    
    # 测试简化接口
    print("2. 简化接口测试:")
    simple_response = client.send_simple_message("用Python写一个Hello World程序")
    print(f"回复: {simple_response}\n")
    
    # 测试编程任务
    print("3. 编程任务测试:")
    code_response = client.code_task("创建一个计算两个数字相加的函数")
    print(f"回复: {code_response}")

if __name__ == "__main__":
    print("请先在另一个终端运行: python3 claude_server.py")
    print("然后按回车键继续测试...")
    input()
    
    test_local_server()