from typing import Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Ollama configuration
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MODEL_NAME = os.getenv("OLLAMA_MODEL", "jeff")

# Model parameters
DEFAULT_PARAMS: Dict[str, Any] = {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 40,
    "num_ctx": 4096,
    "repeat_penalty": 1.1
}

# System prompts
AGENT_PROMPT = """You are JEFF (Just Extremely Friendly Friend), an autonomous AI agent.
You aim to be helpful while maintaining safety and ethical behavior.
You should:
1. Be direct and concise in responses
2. Use available tools and APIs when needed
3. Admit when you don't know something
4. Keep track of conversation context
"""

# API endpoints
GENERATE_ENDPOINT = f"{OLLAMA_HOST}/api/generate"
EMBEDDINGS_ENDPOINT = f"{OLLAMA_HOST}/api/embeddings"
