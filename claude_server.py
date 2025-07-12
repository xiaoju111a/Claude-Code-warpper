#!/usr/bin/env python3
"""
Claude Code CLI HTTP 服务器包装器
将 Claude Code CLI 包装成 HTTP API 服务
"""

from flask import Flask, request, jsonify
import subprocess
import json
import os
from typing import Optional

app = Flask(__name__)

class ClaudeCodeWrapper:
    def __init__(self, claude_path: str = "/home/codespace/nvm/current/bin/claude"):
        self.claude_path = claude_path
    
    def call_claude(self, message: str, session_id: Optional[str] = None) -> dict:
        """调用 Claude Code CLI"""
        cmd = [self.claude_path]
        
        if session_id:
            cmd.extend(["--session", session_id])
            
        try:
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate(input=message)
            
            if process.returncode != 0:
                return {"error": stderr, "success": False}
                
            return {"response": stdout.strip(), "success": True}
            
        except Exception as e:
            return {"error": str(e), "success": False}

# 全局包装器实例
claude_wrapper = ClaudeCodeWrapper()

@app.route('/v1/messages', methods=['POST'])
def send_message():
    """Anthropic API 兼容的消息接口"""
    try:
        data = request.get_json()
        
        # 提取消息内容
        messages = data.get('messages', [])
        if not messages:
            return jsonify({"error": "No messages provided"}), 400
        
        # 获取最后一条用户消息
        user_message = ""
        for msg in messages:
            if msg.get('role') == 'user':
                user_message = msg.get('content', '')
        
        if not user_message:
            return jsonify({"error": "No user message found"}), 400
        
        # 调用 Claude
        result = claude_wrapper.call_claude(user_message)
        
        if not result["success"]:
            return jsonify({"error": result["error"]}), 500
        
        # 返回 Anthropic API 格式
        response = {
            "id": "msg_" + str(hash(user_message))[:8],
            "type": "message",
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": result["response"]
                }
            ],
            "model": "claude-code",
            "stop_reason": "end_turn",
            "stop_sequence": None,
            "usage": {
                "input_tokens": len(user_message.split()),
                "output_tokens": len(result["response"].split())
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/v1/chat', methods=['POST'])
def chat():
    """简化的聊天接口"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        session_id = data.get('session_id')
        
        if not message:
            return jsonify({"error": "No message provided"}), 400
        
        result = claude_wrapper.call_claude(message, session_id)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({"status": "ok", "service": "claude-code-wrapper"})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    print(f"启动 Claude Code CLI 服务器在端口 {port}")
    print(f"API 端点:")
    print(f"  POST /v1/messages - Anthropic API 兼容接口")
    print(f"  POST /v1/chat - 简化聊天接口")
    print(f"  GET /health - 健康检查")
    
    app.run(host='0.0.0.0', port=port, debug=True)