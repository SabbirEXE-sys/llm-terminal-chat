


import requests
import json
import sys
import uuid
from typing import Generator, List, Dict, Optional

# ============================================================
# CONFIGURATION
# ============================================================

BASE_URL = "https://freemodels-chat.freemodels.workers.dev"
TIMEOUT = 120

# Model definitions - Name: Identifier
MODELS = {
    "1": {"name": "Claude Sonnet 5", "id": "claude-sonnet-5", "provider": "Anthropic"},
    "2": {"name": "Claude Opus 4.8", "id": "claude-opus-4-8", "provider": "Anthropic"},
    "3": {"name": "Claude Haiku 4.5", "id": "claude-haiku-4-5", "provider": "Anthropic"},
    "4": {"name": "GPT-4o", "id": "gpt-4o", "provider": "OpenAI"},
    "5": {"name": "GPT-4o-mini", "id": "gpt-4o-mini", "provider": "OpenAI"},
    "6": {"name": "GPT-4-Turbo", "id": "gpt-4-turbo", "provider": "OpenAI"},
    "7": {"name": "Gemini Pro", "id": "gemini-pro", "provider": "Google"},
    "8": {"name": "Grok-1", "id": "grok-1", "provider": "xAI"},
    "9": {"name": "Llama 3 70B", "id": "llama-3-70b", "provider": "Meta"},
    "10": {"name": "Llama 3 8B", "id": "llama-3-8b", "provider": "Meta"},
    "11": {"name": "Mistral Large", "id": "mistral-large", "provider": "Mistral"},
    "12": {"name": "Mixtral 8x7B", "id": "mixtral-8x7b", "provider": "Mistral"},
    "13": {"name": "DeepSeek V3", "id": "deepseek-v3", "provider": "DeepSeek"},
    "14": {"name": "Qwen 72B", "id": "qwen-72b", "provider": "Alibaba"},
}

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    DIM = '\033[2m'

# ============================================================
# CORE CLIENT
# ============================================================

class FreeModelsChat:
    
    
    def __init__(self):
        self.session = requests.Session()
        self.session_id = str(uuid.uuid4())
        self.conversation_history: List[Dict[str, str]] = []
        self.current_model = "claude-sonnet-5"
        self.current_model_name = "Claude Sonnet 5"
        
        # Headers matching the website
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/event-stream",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Origin": "https://freemodels.pro",
            "Referer": "https://freemodels.pro/",
            "Connection": "keep-alive"
        })
    
    def select_model(self):
        """Interactive model selection menu"""
        print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.GREEN}🤖 AVAILABLE MODELS{Colors.END}")
        print(f"{Colors.BOLD}{'='*60}{Colors.END}\n")
        
        # Display models in columns
        for key, model in MODELS.items():
            provider_color = Colors.BLUE if model["provider"] == "Anthropic" else \
                           Colors.GREEN if model["provider"] == "OpenAI" else \
                           Colors.YELLOW
            print(f"  {Colors.BOLD}[{key}]{Colors.END} {model['name']:20} "
                  f"{Colors.DIM}({provider_color}{model['provider']}{Colors.DIM}){Colors.END}")
        
        print(f"\n{Colors.DIM}{'─'*60}{Colors.END}")
        
        while True:
            choice = input(f"{Colors.BOLD}Select model [1-14]{Colors.END} (default: 1): ").strip()
            
            if choice == "":
                choice = "1"
            
            if choice in MODELS:
                self.current_model = MODELS[choice]["id"]
                self.current_model_name = MODELS[choice]["name"]
                print(f"\n✅ Selected: {Colors.GREEN}{self.current_model_name}{Colors.END}\n")
                break
            else:
                print(f"{Colors.RED}❌ Invalid choice. Please enter a number between 1-14.{Colors.END}")
    
    def chat(self, message: str) -> Generator[str, None, None]:
        """Send a message and stream the response"""
        
        # Add user message to history
        self.conversation_history.append({"role": "user", "content": message})
        
        payload = {
            "messages": self.conversation_history,
            "model": self.current_model,
            "temperature": 0.7,
            "max_tokens": 4096,
            "stream": True,
            "session_id": self.session_id
        }
        
        try:
            response = self.session.post(
                BASE_URL,
                json=payload,
                stream=True,
                timeout=TIMEOUT
            )
            response.raise_for_status()
            
            full_response = ""
            
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        data = line[6:]
                        if data == '[DONE]':
                            break
                        try:
                            chunk = json.loads(data)
                            content = self._extract_content(chunk)
                            if content:
                                yield content
                                full_response += content
                        except json.JSONDecodeError:
                            pass
            
            # Add assistant response to history
            if full_response:
                self.conversation_history.append({
                    "role": "assistant", 
                    "content": full_response
                })
                
        except requests.exceptions.Timeout:
            yield f"\n{Colors.RED}⚠️ Request timed out. Please try again.{Colors.END}"
        except requests.exceptions.RequestException as e:
            yield f"\n{Colors.RED}⚠️ Connection error: {str(e)}{Colors.END}"
    
    def _extract_content(self, chunk: dict) -> str:
        """Extract content from various response formats"""
        # OpenAI-style
        if 'choices' in chunk:
            choice = chunk['choices'][0]
            if 'delta' in choice and 'content' in choice['delta']:
                return choice['delta']['content']
            if 'message' in choice and 'content' in choice['message']:
                return choice['message']['content']
        
        # Anthropic-style
        if 'completion' in chunk:
            return chunk['completion']
        
        # Raw text
        if 'text' in chunk:
            return chunk['text']
        
        if 'content' in chunk:
            return chunk['content']
        
        return ""
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        print(f"\n{Colors.YELLOW}🗑️ Conversation history cleared.{Colors.END}")
    
    def show_history(self):
        """Display conversation history"""
        if not self.conversation_history:
            print(f"\n{Colors.DIM}No conversation history yet.{Colors.END}")
            return
        
        print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}📜 CONVERSATION HISTORY{Colors.END}")
        print(f"{Colors.BOLD}{'='*60}{Colors.END}\n")
        
        for i, msg in enumerate(self.conversation_history):
            role = msg["role"]
            content = msg["content"]
            
            if role == "user":
                print(f"{Colors.BOLD}{Colors.GREEN}[USER]{Colors.END} {content[:200]}...")
            else:
                print(f"{Colors.BOLD}{Colors.BLUE}[ASSISTANT]{Colors.END} {content[:200]}...")
            
            if i < len(self.conversation_history) - 1:
                print(f"{Colors.DIM}{'─'*50}{Colors.END}")
        
        print(f"\n{Colors.DIM}Total messages: {len(self.conversation_history)}{Colors.END}")

# ============================================================
# INTERACTIVE CLI
# ============================================================

def print_banner():
    """Print the welcome banner"""
    print(f"""
{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}
{Colors.BOLD}{Colors.GREEN}  🚀 LLM Models for Chats {Colors.END}
{Colors.BOLD}{Colors.BLUE}  Built by Sabbir{Colors.END}
{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}
    """)

def print_help():
    """Print help menu"""
    print(f"""
{Colors.BOLD}Commands:{Colors.END}
  {Colors.GREEN}/model{Colors.END}     - Change the current model
  {Colors.GREEN}/clear{Colors.END}     - Clear conversation history
  {Colors.GREEN}/history{Colors.END}   - Show conversation history
  {Colors.GREEN}/quit{Colors.END}      - Exit the chat
  {Colors.GREEN}/help{Colors.END}      - Show this help menu

{Colors.DIM}Just type your message and press Enter to chat!{Colors.END}
""")

def main():
    """Main entry point"""
    
    print_banner()
    
    # Initialize client
    client = FreeModelsChat()
    
    # Model selection
    client.select_model()
    
    print(f"{Colors.DIM}Type /help for commands, /quit to exit{Colors.END}")
    print(f"{Colors.DIM}{'─'*60}{Colors.END}\n")
    
    # Main chat loop
    while True:
        try:
            # Get user input
            user_input = input(f"{Colors.BOLD}{Colors.GREEN}You{Colors.END} > ").strip()
            
            # Empty input
            if not user_input:
                continue
            
            # Handle commands
            if user_input.startswith('/'):
                cmd = user_input.lower()
                
                if cmd == '/quit' or cmd == '/exit':
                    print(f"\n{Colors.GREEN}👋 Goodbye, Legend!{Colors.END}\n")
                    break
                
                elif cmd == '/help':
                    print_help()
                    continue
                
                elif cmd == '/model':
                    client.select_model()
                    continue
                
                elif cmd == '/clear':
                    client.clear_history()
                    continue
                
                elif cmd == '/history':
                    client.show_history()
                    continue
                
                else:
                    print(f"{Colors.RED}❌ Unknown command: {user_input}{Colors.END}")
                    print(f"{Colors.DIM}Type /help for available commands{Colors.END}")
                    continue
            
            # Process message
            print(f"{Colors.BOLD}{Colors.BLUE}{client.current_model_name}{Colors.END} > ", end='')
            
            full_response = ""
            for chunk in client.chat(user_input):
                print(chunk, end='', flush=True)
                full_response += chunk
            
            print()  # Newline after response
            
        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}⚠️ Interrupted. Type /quit to exit.{Colors.END}")
            continue
        except EOFError:
            break
        except Exception as e:
            print(f"\n{Colors.RED}⚠️ Error: {str(e)}{Colors.END}")
            print(f"{Colors.DIM}The conversation may have been interrupted. Try again.{Colors.END}")

# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.GREEN}👋 Goodbye!{Colors.END}\n")
    except Exception as e:
        print(f"\n{Colors.RED}Fatal error: {str(e)}{Colors.END}")
        sys.exit(1)