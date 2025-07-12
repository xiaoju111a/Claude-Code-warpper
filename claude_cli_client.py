#!/usr/bin/env python3
import requests
import json
import os
from typing import Optional, List, Dict

class ClaudeCodeClient:
    """基于自定义 base_url 的 Claude 客户端"""
    
    def __init__(self, api_key: str = "dummy", base_url: str = "http://localhost:8000"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
    def send_message(self, message: str, session_id: Optional[str] = None) -> str:
        """
        发送消息给本地 Claude 服务器
        
        Args:
            message: 要发送的消息
            session_id: 可选的会话ID
            
        Returns:
            Claude 的回复
        """
        url = f"{self.base_url}/v1/messages"
        
        data = {
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ],
            "max_tokens": 4000
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            if "content" in result and result["content"]:
                return result["content"][0]["text"]
            else:
                return result.get("error", "未知错误")
                
        except Exception as e:
            return f"请求失败: {str(e)}"
    
    def send_simple_message(self, message: str, session_id: Optional[str] = None) -> str:
        """使用简化接口发送消息"""
        url = f"{self.base_url}/v1/chat"
        
        data = {
            "message": message,
            "session_id": session_id
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            if result.get("success"):
                return result["response"]
            else:
                return result.get("error", "未知错误")
                
        except Exception as e:
            return f"请求失败: {str(e)}"
    
    def code_task(self, task_description: str, file_path: Optional[str] = None) -> str:
        """
        执行编程任务
        
        Args:
            task_description: 任务描述
            file_path: 可选的文件路径
            
        Returns:
            执行结果
        """
        if file_path:
            message = f"请帮我处理文件 {file_path}：{task_description}"
        else:
            message = f"请帮我：{task_description}"
            
        return self.send_message(message)
    
    def review_code(self, file_path: str) -> str:
        """代码审查"""
        return self.send_message(f"请审查这个文件的代码：{file_path}")
    
    def debug_issue(self, error_description: str, file_path: Optional[str] = None) -> str:
        """调试问题"""
        if file_path:
            message = f"文件 {file_path} 有以下问题：{error_description}，请帮我调试"
        else:
            message = f"遇到问题：{error_description}，请帮我调试"
        return self.send_message(message)
    
    def explain_code(self, file_path: str) -> str:
        """解释代码"""
        return self.send_message(f"请解释这个文件的代码：{file_path}")

# 使用示例
if __name__ == "__main__":
    client = ClaudeCodeClient()
    
    # 基本对话
    response = client.send_message("你好，请介绍一下你的功能")
    print("Claude回复:", response)
    
    # 编程任务
    print("\n--- 编程任务示例 ---")
    task_response = client.code_task("创建一个简单的HTTP服务器")
    print("任务结果:", task_response)
    
    # 代码审查（如果有现有文件）
    if os.path.exists("demo.py"):
        print("\n--- 代码审查示例 ---")
        review_response = client.review_code("demo.py")
        print("审查结果:", review_response)