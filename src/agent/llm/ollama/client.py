import requests
import json
from typing import Dict, Any, Optional, List
import logging
from .config import (
    GENERATE_ENDPOINT,
    EMBEDDINGS_ENDPOINT,
    MODEL_NAME,
    DEFAULT_PARAMS,
    AGENT_PROMPT
)

class OllamaClient:
    """Low-level Ollama API client"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.session = requests.Session()
        
    def generate(self, prompt: str, system_prompt: str = "", **kwargs) -> Optional[str]:
        """Raw generate call to Ollama"""
        try:
            # Merge default params with any overrides
            params = DEFAULT_PARAMS.copy()
            params.update(kwargs)
            
            data = {
                "model": MODEL_NAME,
                "prompt": prompt,
                "system": system_prompt,
                "options": params,
                "stream": False
            }
            
            response = self.session.post(GENERATE_ENDPOINT, json=data)
            response.raise_for_status()
            
            result = response.json()
            return result.get("response", "")
            
        except Exception as e:
            self.logger.error(f"Ollama generate error: {str(e)}")
            return None
            
    def get_embeddings(self, text: str) -> Optional[List[float]]:
        """Get embeddings for text"""
        try:
            data = {
                "model": MODEL_NAME,
                "prompt": text
            }
            
            response = self.session.post(EMBEDDINGS_ENDPOINT, json=data)
            response.raise_for_status()
            
            result = response.json()
            return result.get("embedding")
            
        except Exception as e:
            self.logger.error(f"Ollama embeddings error: {str(e)}")
            return None

class OllamaAgent:
    """High-level Ollama agent with conversation management"""
    
    def __init__(self):
        self.client = OllamaClient()
        self.logger = logging.getLogger(__name__)
        self.conversation_history: List[Dict[str, Any]] = []
        
    def _build_prompt(self, user_input: str, context: Optional[str] = None) -> str:
        """Build full prompt with history and context"""
        prompt_parts = []
        
        # Add recent conversation history (last 5 exchanges)
        if self.conversation_history:
            history = self.conversation_history[-5:]
            for msg in history:
                role = msg["role"]
                content = msg["content"]
                prompt_parts.append(f"{role.upper()}: {content}")
        
        # Add context if provided
        if context:
            prompt_parts.append(f"CONTEXT: {context}")
            
        # Add current input
        prompt_parts.append(f"USER: {user_input}")
        prompt_parts.append("ASSISTANT:")
        
        return "\n".join(prompt_parts)
        
    def generate_response(self, user_input: str, context: Optional[str] = None) -> str:
        """Generate a response to user input"""
        try:
            # Build full prompt
            prompt = self._build_prompt(user_input, context)
            
            # Get response
            response = self.client.generate(prompt, system_prompt=AGENT_PROMPT)
            
            if not response:
                return "I apologize, I'm having trouble generating a response right now."
                
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": user_input})
            self.conversation_history.append({"role": "assistant", "content": response})
            
            return response
            
        except Exception as e:
            self.logger.error(f"Response generation error: {str(e)}")
            return "I encountered an error while trying to respond."
            
    def get_embeddings(self, text: str) -> Optional[List[float]]:
        """Get embeddings for text, used for semantic search"""
        return self.client.get_embeddings(text)
