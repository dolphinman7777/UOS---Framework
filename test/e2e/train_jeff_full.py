from src.agent.training.trainer import JeffTrainer
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_training_text(filepath: str) -> str:
    """Load text content from a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error loading {filepath}: {e}")
        return ""

def train_jeff_on_all_data():
    trainer = JeffTrainer()
    
    # Define training categories and their source files
    training_data = {
        "philosophy": [
            "training_data/philosophy/eastern_philosophy.txt",
            "training_data/philosophy/western_philosophy.txt", 
            "training_data/philosophy/metaphysics.txt"
        ],
        "technology": [
            "training_data/technology/ai_concepts.txt",
            "training_data/technology/blockchain.txt",
            "training_data/technology/distributed_systems.txt"
        ],
        "creativity": [
            "training_data/creativity/artistic_expression.txt",
            "training_data/creativity/innovation.txt",
            "training_data/creativity/creative_process.txt"
        ]
    }

    # Train on each category
    for category, files in training_data.items():
        logger.info(f"\n=== Training on {category} ===")
        
        # Combine all texts in category
        category_text = ""
        for filepath in files:
            text = load_training_text(filepath)
            category_text += f"\n{text}"
            logger.info(f"Loaded {filepath}")
        
        # Train on combined category text
        logger.info(f"Training on {category} data...")
        trainer.train_on_domain(category_text)
        logger.info(f"Completed training on {category}")

    logger.info("\nTraining complete!")

if __name__ == "__main__":
    train_jeff_on_all_data() 