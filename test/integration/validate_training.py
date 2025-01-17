from src.agent.llm.ollama.client import OllamaAgent
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_jeff_knowledge():
    jeff = OllamaAgent()
    
    # Test prompts for each domain
    test_cases = {
        "Philosophy": [
            "What are the key concepts in Eastern philosophy?",
            "How does consciousness relate to reality?",
            "Explain the relationship between mind and matter."
        ],
        "Technology": [
            "Explain how blockchain consensus works",
            "What are the challenges in distributed systems?",
            "How do neural networks learn patterns?"
        ],
        "Creativity": [
            "How does innovation emerge from constraints?",
            "What is the relationship between art and consciousness?",
            "Describe the creative problem-solving process"
        ]
    }
    
    logger.info("\n=== Validating JEFF's Knowledge ===\n")
    
    for domain, prompts in test_cases.items():
        logger.info(f"\nTesting {domain} Knowledge:")
        for prompt in prompts:
            response = jeff.generate_response(prompt)
            logger.info(f"\nQ: {prompt}")
            logger.info(f"A: {response}")
            logger.info("-" * 80)

if __name__ == "__main__":
    validate_jeff_knowledge() 