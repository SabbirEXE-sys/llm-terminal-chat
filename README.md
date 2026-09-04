# 🚀 FreeModel Chat CLI

An interactive command-line interface (CLI) to stream and chat with multiple AI models (Claude, GPT-4o, Gemini, Grok, Llama 3, DeepSeek, and more).

Built by **Sabbir**.

---

## ✨ Features

- 🤖 **Multi-Model Support**: Access Claude Sonnet/Opus, GPT-4o, Gemini Pro, Grok-1, Llama 3, DeepSeek V3, and Qwen 72B.
- ⚡ **Real-Time Streaming**: Live terminal streaming for AI responses.
- 📜 **Session & History**: Full multi-turn conversation memory, with commands to clear or view history.
- 🎨 **Rich UI**: Colorized terminal output with clear provider branding.
- 🔌 **Zero Complex Setup**: Standard Python dependencies (`requests`).

---

## 🛠️ Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   cd YOUR_REPO_NAME
   ```

2. **Install Dependencies**
   ```bash
   pip install requests
   ```

---

## 🚀 Usage

Run the Python script:

```bash
python client.py
```

### Interactive Commands

During the chat session, you can use the following slash commands:

| Command | Description |
| :--- | :--- |
| `/model` | Change the active AI model |
| `/clear` | Clear the current conversation history |
| `/history` | Display the conversation history |
| `/help` | Show the help menu |
| `/quit` | Exit the CLI application |

---

## 📋 Available Models

- **Anthropic**: Claude Sonnet 5, Claude Opus 4.8, Claude Haiku 4.5
- **OpenAI**: GPT-4o, GPT-4o-mini, GPT-4-Turbo
- **Google**: Gemini Pro
- **xAI**: Grok-1
- **Meta**: Llama 3 70B, Llama 3 8B
- **Mistral**: Mistral Large, Mixtral 8x7B
- **DeepSeek**: DeepSeek V3
- **Alibaba**: Qwen 72B

---

## 📄 License

MIT License - feel free to modify and share!
