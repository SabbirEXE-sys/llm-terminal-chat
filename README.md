# 🚀 FreeModel Chat CLI

A powerful, interactive terminal-based chat client for streaming and conversing with cutting-edge Large Language Models (LLMs) from Anthropic, OpenAI, Google, Meta, DeepSeek, Mistral, xAI, and Alibaba.

Built with ❤️ by **Sabbir**.

---

## 🌟 Key Features

- 🤖 **14+ Top-Tier AI Models**: Chat with Claude 3.5/Sonnet, GPT-4o, Gemini Pro, DeepSeek V3, Llama 3, Grok-1, Mistral, and more.
- ⚡ **Real-Time Streaming**: Token-by-token streaming output directly in your console using Server-Sent Events (SSE).
- 💬 **Context-Aware Conversations**: Retains multi-turn conversation history for coherent back-and-forth dialogue.
- 🎨 **Sleek Color-Coded Terminal UI**: Vibrant ANSI color formatting highlighting providers, status messages, and responses.
- 🛠️ **In-Chat Slash Commands**: Switch models on the fly, view message history, or reset context without restarting.
- 🪶 **Lightweight & Fast**: Pure Python with minimal dependencies (`requests`).

---

## 📋 Supported Models

| # | Model Name | Provider | Identifier |
|---|---|---|---|
| 1 | **Claude Sonnet 5** | Anthropic | `claude-sonnet-5` |
| 2 | **Claude Opus 4.8** | Anthropic | `claude-opus-4-8` |
| 3 | **Claude Haiku 4.5** | Anthropic | `claude-haiku-4-5` |
| 4 | **GPT-4o** | OpenAI | `gpt-4o` |
| 5 | **GPT-4o-mini** | OpenAI | `gpt-4o-mini` |
| 6 | **GPT-4-Turbo** | OpenAI | `gpt-4-turbo` |
| 7 | **Gemini Pro** | Google | `gemini-pro` |
| 8 | **Grok-1** | xAI | `grok-1` |
| 9 | **Llama 3 70B** | Meta | `llama-3-70b` |
| 10 | **Llama 3 8B** | Meta | `llama-3-8b` |
| 11 | **Mistral Large** | Mistral | `mistral-large` |
| 12 | **Mixtral 8x7B** | Mistral | `mixtral-8x7b` |
| 13 | **DeepSeek V3** | DeepSeek | `deepseek-v3` |
| 14 | **Qwen 72B** | Alibaba | `qwen-72b` |

---

## ⚙️ Installation & Setup

### 1. Prerequisites
- Python 3.8 or higher installed on your system.
- Git installed.

### 2. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

Launch the client from your terminal:

```bash
python client.py
```

### Interactive Commands

During the chat session, you can execute the following slash commands at any prompt:

| Command | Description |
|---|---|
| `/model` | Open the interactive menu to switch between available models |
| `/history` | Print the full history of the current conversation session |
| `/clear` | Wipe conversation history and start a fresh context |
| `/help` | Display the list of available commands and instructions |
| `/quit` or `/exit` | Exit the CLI safely |

---

## 📂 Project Structure

```
├── client.py          # Main CLI application & streaming client
├── requirements.txt   # Python dependencies
├── .gitignore         # Git ignore configuration
└── README.md          # Project documentation
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
Feel free to modify, distribute, and integrate it into your own workflows.
