from typing import Dict, List, Any, Optional
import logging
from datetime import datetime
from src.agent.llm.ollama.client import OllamaAgent
from src.memory.chroma.queries.storage import MemoryManager

class ConversationManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.agent = OllamaAgent()
        self.memory = MemoryManager()
        self.active_conversations: Dict[str, List[Dict[str, Any]]] = {}
        
    def add_message(self, user_id: str, content: str, role: str):
        """Add a message to the conversation history"""
        if user_id not in self.active_conversations:
            self.active_conversations[user_id] = []
            
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        
        self.active_conversations[user_id].append(message)
        
        # Get embedding for conversation and store in memory
        if len(self.active_conversations[user_id]) >= 2:  # Store after exchange
            conversation_text = "\n".join([
                f"{msg['role'].upper()}: {msg['content']}"
                for msg in self.active_conversations[user_id][-2:]  # Just the last exchange
            ])
            embedding = self.agent.get_embeddings(conversation_text)
            
            if embedding:
                self.memory.store_conversation(
                    user_id,
                    self.active_conversations[user_id][-2:],
                    embedding
                )
                
    def get_context(self, user_id: str, query: Optional[str] = None) -> Optional[str]:
        """Get relevant conversation context"""
        try:
            # If no query provided, use last message as query
            if not query and user_id in self.active_conversations:
                messages = self.active_conversations[user_id]
                if messages:
                    query = messages[-1]["content"]
                    
            if not query:
                return None
                
            # Get embedding for query
            query_embedding = self.agent.get_embeddings(query)
            if not query_embedding:
                return None
                
            # Search conversations and facts
            conversations = self.memory.search_conversations(query_embedding, limit=2)
            facts = self.memory.search_facts(query_embedding, limit=2)
            
            context_parts = []
            
            # Add relevant conversations
            if conversations:
                context_parts.append("Previous conversations:")
                for conv in conversations:
                    context_parts.append(conv["text"])
                    
            # Add relevant facts
            if facts:
                context_parts.append("\nRelevant facts:")
                for fact in facts:
                    context_parts.append(f"- {fact['text']}")
                    
            return "\n".join(context_parts) if context_parts else None
            
        except Exception as e:
            self.logger.error(f"Error getting context: {str(e)}")
            return None
            
    def generate_response(self, user_id: str, message: str) -> str:
        """Generate a response using context"""
        try:
            # Get relevant context
            context = self.get_context(user_id, message)
            
            # Generate response
            response = self.agent.generate_response(message, context)
            
            # Store the exchange
            self.add_message(user_id, message, "user")
            self.add_message(user_id, response, "assistant")
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error generating response: {str(e)}")
            return "I encountered an error while processing your message."
            
    def clear_conversation(self, user_id: str):
        """Clear conversation history for user"""
        if user_id in self.active_conversations:
            del self.active_conversations[user_id] 