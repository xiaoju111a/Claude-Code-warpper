# Claude-Code-Wrapper

Wrap Claude Code CLI as an HTTP API service, supporting calls through URL and API Key.

## Prerequisites

### Install Claude Code CLI
```bash
npm install -g @anthropic-ai/claude-code
```

### Verify Installation
```bash
claude --version
which claude
```

## Setup

### 1. Configure Claude Code Path
Edit `claude_server.py` and update the Claude Code path:
```python
def __init__(self, claude_path: str = "/path/to/your/claude"):
    # Update this path to match your Claude Code installation
    # Common paths:
    # - "/usr/local/bin/claude" (global npm install)
    # - "/home/codespace/nvm/current/bin/claude" (nvm)
    # - "/home/username/.nvm/versions/node/v18.x.x/bin/claude" (nvm with specific version)
```

To find your Claude Code path:
```bash
which claude
# or
whereis claude
```

### 2. Set Environment Variables (Optional)
```bash
export ANTHROPIC_API_KEY="your-anthropic-api-key"
export CLAUDE_CODE_API_KEYS="your-custom-api-key-1,your-custom-api-key-2"
```

### 3. Install Python Dependencies
```bash
pip install fastapi uvicorn requests pydantic
```

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

The server will start on `http://localhost:8000` by default.

Output should show:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
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
```http
POST /v1/messages
Content-Type: application/json
Authorization: Bearer your-api-key

{
  "messages": [
    {
      "role": "user", 
      "content": "Hello, how are you?"
    }
  ],
  "max_tokens": 4000,
  "model": "claude-3-sonnet-20240229"
}
```

### Simplified Chat Interface
```http
POST /v1/chat
Content-Type: application/json
Authorization: Bearer your-api-key

{
  "message": "Write a Python function to calculate factorial",
  "session_id": "optional-session-id",
  "max_tokens": 1000
}
```

### Code Generation Interface
```http
POST /v1/code
Content-Type: application/json
Authorization: Bearer your-api-key

{
  "prompt": "Create a REST API with FastAPI for user management",
  "language": "python",
  "complexity": "intermediate"
}
```

### File Operations
```http
POST /v1/file/analyze
Content-Type: application/json
Authorization: Bearer your-api-key

{
  "file_path": "/path/to/your/file.py",
  "task": "analyze and suggest improvements"
}
```

### Health Check
```http
GET /health
```

### Server Info
```http
GET /info
```

## Client Usage

### Basic Client
```python
from claude_cli_client import ClaudeCodeClient

# Create client
client = ClaudeCodeClient(
    api_key="your-api-key",
    base_url="http://localhost:8000"
)

# Send message
response = client.send_message("Hello")
print(response)

# Programming task
code = client.code_task("Write a Python function to calculate Fibonacci sequence")
print(code)
```

### Advanced Usage
```python
# Chat with session
response = client.chat(
    message="Explain machine learning",
    session_id="my-session",
    max_tokens=2000
)

# Code generation
code = client.generate_code(
    prompt="Create a web scraper using requests and BeautifulSoup",
    language="python"
)

# File analysis
analysis = client.analyze_file(
    file_path="./my_script.py",
    task="find bugs and optimization opportunities"
)
```

### Using with curl
```bash
# Health check
curl http://localhost:8000/health

# Send message
curl -X POST http://localhost:8000/v1/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key" \
  -d '{
    "message": "Hello Claude!",
    "max_tokens": 1000
  }'

# Code generation
curl -X POST http://localhost:8000/v1/code \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key" \
  -d '{
    "prompt": "Create a calculator class in Python",
    "language": "python"
  }'
```

## Configuration

### Server Configuration
Edit `claude_server.py` to customize:
```python
class ClaudeCodeWrapper:
    def __init__(self, 
                 claude_path: str = "/usr/local/bin/claude",
                 timeout: int = 300,
                 max_concurrent_requests: int = 10):
        # Your configuration here
```

### Environment Variables
```bash
# Required for Claude Code CLI
export ANTHROPIC_API_KEY="your-anthropic-api-key"

# Optional: Custom API keys for your wrapper service
export CLAUDE_CODE_API_KEYS="key1,key2,key3"

# Optional: Server configuration
export CLAUDE_WRAPPER_HOST="0.0.0.0"
export CLAUDE_WRAPPER_PORT="8000"
export CLAUDE_WRAPPER_LOG_LEVEL="INFO"
```

## Troubleshooting

### Common Issues

1. **Claude Code not found**
   ```
   Error: Claude Code CLI not found at path: /path/to/claude
   ```
   Solution: Update the `claude_path` in `claude_server.py` with the correct path from `which claude`.

2. **Permission denied**
   ```
   Error: Permission denied when executing Claude Code
   ```
   Solution: Make sure the Claude Code binary is executable:
   ```bash
   chmod +x /path/to/claude
   ```

3. **API Key issues**
   ```
   Error: Invalid API key
   ```
   Solution: Set the `ANTHROPIC_API_KEY` environment variable or check your API key configuration.

4. **Port already in use**
   ```
   Error: [Errno 48] Address already in use
   ```
   Solution: Change the port in `claude_server.py` or kill the process using port 8000:
   ```bash
   lsof -ti:8000 | xargs kill -9
   ```

5. **Module not found**
   ```
   ModuleNotFoundError: No module named 'fastapi'
   ```
   Solution: Install the required dependencies:
   ```bash
   pip install fastapi uvicorn requests pydantic
   ```

### Configuration Examples

For different environments:

**Linux/Ubuntu:**
```python
claude_path: str = "/usr/local/bin/claude"
```

**macOS with Homebrew:**
```python
claude_path: str = "/opt/homebrew/bin/claude"
```

**GitHub Codespaces:**
```python
claude_path: str = "/home/codespace/nvm/current/bin/claude"
```

**WSL/Windows:**
```python
claude_path: str = "/mnt/c/Users/username/AppData/Roaming/npm/claude"
```

**Docker:**
```python
claude_path: str = "/usr/local/bin/claude"
```



## License
MIT License - see LICENSE file for details

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Support
For issues and questions:

- Check the troubleshooting section
- Review Claude Code CLI documentation
- Open an issue on GitHub

