from src.agent.training.trainer import JeffTrainer
import glob
import os

trainer = JeffTrainer()

def train_from_directory(directory: str, category: str):
    """Train from all .txt files in a directory"""
    files = glob.glob(os.path.join(directory, "*.txt"))
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            text = f.read()
        trainer.add_training_text(category, text)

# Train from directories
train_from_directory("training_data/philosophy", "philosophy")
train_from_directory("training_data/technology", "technical")
train_from_directory("training_data/creativity", "creative") 