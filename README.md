# Claude-Code-warpper
Wrap Claude Code CLI as an HTTP API service, supporting calls through URL and API Key.

## File Description

- `claude_server.py` - HTTP server that wraps Claude Code CLI
- `claude_cli_client.py` - Client for HTTP calls to server
- `test_server.py` - Test script
- `claude_examples.py` - Complete feature demonstration
- `simple_claude_test.py` - Simple test example

## Usage

### 1. Start Server
```bash
cd claude
python3 claude_server.py
```

### 2. Test Client
In another terminal:
```bash
cd claude
python3 test_server.py
```

### 3. Run Examples
```bash
cd claude
python3 claude_examples.py
```

## API Endpoints

### Anthropic API Compatible Interface
```
POST /v1/messages
Content-Type: application/json

{
  "messages": [
    {
      "role": "user", 
      "content": "你好"
    }
  ],
  "max_tokens": 4000
}
```

### Simplified Chat Interface
```
POST /v1/chat
Content-Type: application/json

{
  "message": "Hello",
  "session_id": "optional"
}
```

### Health Check
```
GET /health
```

## Client Usage

```python
from claude_cli_client import ClaudeCodeClient

# Create client
client = ClaudeCodeClient(
    api_key="dummy",
    base_url="http://localhost:8000"
)

# Send message
response = client.send_message("Hello")
print(response)

# Programming task
code = client.code_task("Write a Python function to calculate Fibonacci sequence")
print(code)
```