from src.agent.llm.ollama.client import OllamaAgent
import os
from typing import List, Dict, Union
import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class JeffTrainer:
    def __init__(self):
        self.ollama_agent = OllamaAgent()
        self.training_data = {}
        self.data_directory = "src/data/training"
        
    def train_on_domain(self, text: str) -> None:
        """Train on a specific domain of knowledge"""
        try:
            logger.info("Starting training...")
            # Create a training prompt that instructs the model to learn from the text
            training_prompt = f"""System: You are being trained on new knowledge. Please analyze and integrate the following information into your knowledge base.

Content to learn:
{text}

Instructions:
1. Read and analyze the content carefully
2. Extract key concepts and principles
3. Identify important relationships and patterns
4. Note specific examples and applications
5. Understand underlying theories and frameworks

Confirm your understanding by responding: "I have analyzed and integrated this information about [topic]. Key concepts include: [brief summary]"
"""
            # Use generate_response instead of train
            response = self.ollama_agent.generate_response(training_prompt)
            logger.info(f"Training response: {response}")
            logger.info("Training completed successfully")
            
        except Exception as e:
            logger.error(f"Training failed: {e}")
            raise

    def add_training_text(self, category: str, text: Union[str, List[str]]) -> None:
        """Add plain text training data for a specific category"""
        if isinstance(text, str):
            text = [text]
            
        # Create category directory if it doesn't exist
        category_dir = os.path.join(self.data_directory, category)
        os.makedirs(category_dir, exist_ok=True)
        
        # Save to file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{category}_{timestamp}.txt"
        filepath = os.path.join(category_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(text))
        
        # Train on the text
        self.train_on_domain('\n'.join(text))