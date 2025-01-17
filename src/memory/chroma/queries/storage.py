import chromadb
from chromadb.config import Settings
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import os
from dotenv import load_dotenv

load_dotenv()

class MemoryManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Initialize ChromaDB
        persist_dir = os.getenv("CHROMA_DB_PATH", "./data/chromadb")
        self.client = chromadb.PersistentClient(path=persist_dir)
        
        # Create collections if they don't exist
        self.conversations = self.client.get_or_create_collection(
            name="conversations",
            metadata={"description": "Conversation history"}
        )
        
        self.facts = self.client.get_or_create_collection(
            name="facts",
            metadata={"description": "Learned facts and information"}
        )
        
    def store_conversation(self, user_id: str, messages: List[Dict[str, Any]], embeddings: List[float]):
        """Store a conversation with its embedding"""
        try:
            # Format conversation for storage
            conversation_text = "\n".join([
                f"{msg['role'].upper()}: {msg['content']}"
                for msg in messages
            ])
            
            # Store in ChromaDB
            self.conversations.add(
                documents=[conversation_text],
                embeddings=[embeddings],
                metadatas=[{
                    "user_id": user_id,
                    "timestamp": datetime.now().isoformat(),
                    "message_count": len(messages)
                }],
                ids=[f"conv_{datetime.now().timestamp()}"]
            )
            
        except Exception as e:
            self.logger.error(f"Error storing conversation: {str(e)}")
            
    def store_fact(self, fact: str, source: str, embedding: List[float]):
        """Store a learned fact with its embedding"""
        try:
            self.facts.add(
                documents=[fact],
                embeddings=[embedding],
                metadatas=[{
                    "source": source,
                    "timestamp": datetime.now().isoformat()
                }],
                ids=[f"fact_{datetime.now().timestamp()}"]
            )
        except Exception as e:
            self.logger.error(f"Error storing fact: {str(e)}")
            
    def search_conversations(self, query_embedding: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """Search conversations by similarity"""
        try:
            results = self.conversations.query(
                query_embeddings=[query_embedding],
                n_results=limit
            )
            
            # Format results
            conversations = []
            for i in range(len(results["documents"][0])):
                conversations.append({
                    "text": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "distance": results["distances"][0][i]
                })
                
            return conversations
            
        except Exception as e:
            self.logger.error(f"Error searching conversations: {str(e)}")
            return []
            
    def search_facts(self, query_embedding: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """Search facts by similarity"""
        try:
            results = self.facts.query(
                query_embeddings=[query_embedding],
                n_results=limit
            )
            
            # Format results
            facts = []
            for i in range(len(results["documents"][0])):
                facts.append({
                    "text": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "distance": results["distances"][0][i]
                })
                
            return facts
            
        except Exception as e:
            self.logger.error(f"Error searching facts: {str(e)}")
            return []
