from src.agent.llm.ollama.client import OllamaAgent
from src.social.twitter.api.handlers.tweet_handler import TwitterAgent
from src.memory.chroma.queries.storage import MemoryManager
from src.agent.personality.engine import PersonalityEngine
from src.agent.context.conversation_manager import ConversationManager
from src.agent.personality.templates.default.ascii_art import ASCIIArtGenerator
from src.agent.web.access import WebAccess
import logging
import time
from datetime import datetime
import backoff
import signal
import sys
import random
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown
from rich.live import Live
from rich.spinner import Spinner
import yaml
import os
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

console = Console()

# Fun ASCII art signatures to use randomly
SIGNATURES = [
    "ʕ •ᴥ•ʔ", "(-‿‿-)", "(｡◕‿◕｡)", "◉_◉", "^̮^", 
    "(╯°□°）╯︵ ┻━┻", "┬──┬◡ﾉ(° -°)", "¯\_(ツ)_/¯"
]

def get_random_style():
    """Generate random styling for responses"""
    styles = ["bold", "italic", "blue", "green", "yellow", "red", "magenta", "cyan"]
    return random.choice(styles)

class JEFF:
    def __init__(self):
        self.console = Console()
        self.personality_traits = [
            "curious", "philosophical", 
            "deadpan", "blunt", "chaotic",
            "stubborn"
        ]
        self.interests = [
            "retro causality", "alchemy", "singularity", "golden age of humanity",
            "dogs", "consciousness", "memes", "creativity",
            "existence", "technology", "nature", "dreams"
        ]
        self.current_mood = random.choice(self.personality_traits)
        self.current_interest = random.choice(self.interests)
        self.ollama_agent = OllamaAgent(model="mistral")
        self.conversation_history = []
        self.ascii_art = ASCIIArtGenerator()
        self.web = WebAccess()
        
        # Enhanced response patterns with more variety
        self.response_patterns = {
            "quip": {  # New ultra-short response type
                "max_words": 15,
                "style": "sharp and witty",
                "probability": 0.2  # 20% chance
            },
            "short": {
                "max_words": 40,
                "style": "concise but insightful",
                "probability": 0.3  # 30% chance
            },
            "medium": {
                "max_words": 80,
                "style": "balanced and deep",
                "probability": 0.35  # 35% chance
            },
            "long": {
                "max_words": 150,
                "style": "profound and complete",
                "probability": 0.15  # 15% chance
            }
        }
        
        # Add conversation style indicators
        self.casual_indicators = [
            "k", "cool", "nice", "yeah", "nah", "sup", "hey",
            "lol", "hmm", "wow", "oh", "ah", "huh", "right"
        ]
        
        # Load behavior config once during initialization
        try:
            behavior_path = os.path.join(os.path.dirname(__file__), 'src/agent/personality/config/behavior.yml')
            with open(behavior_path, 'r') as file:
                self.behavior = yaml.safe_load(file)
        except Exception as e:
            logger.error(f"Failed to load behavior config: {e}")
            self.behavior = {}

        # Initialize personality engine
        self.personality = PersonalityEngine(
            ollama_agent=self.ollama_agent,
            ascii_art=self.ascii_art
        )

        # Add dynamic personality states
        self.personality_states = {
            "intellectual_depth": 0.0,  # Increases with complex discussions
            "emotional_resonance": 0.0,  # Grows with emotional exchanges
            "creativity_level": 0.0,    # Rises with artistic/creative topics
            "technical_focus": 0.0,     # Increases with technical discussions
            "philosophical_depth": 0.0   # Deepens with existential topics
        }
        
        # Add conversation memory patterns
        self.conversation_patterns = {
            "topic_chains": [],         # Track topic evolution
            "user_interests": set(),    # Accumulate user interests
            "depth_markers": [],        # Track conversation depth
            "emotional_moments": []     # Remember emotional peaks
        }
        
        # Add knowledge integration sources
        self.knowledge_sources = {
            "philosophy": "src/agent/personality/data/philosophy.json",
            "technology": "src/agent/personality/data/tech.json",
            "creativity": "src/agent/personality/data/art.json",
            "science": "src/agent/personality/data/science.json",
            "metaphysics": "src/agent/personality/data/metaphysics.json"
        }

    def get_response(self, user_input):
        """Generate response using personality engine"""
        # Get base response from personality engine
        base_response, art = self.personality.generate_response(user_input)
        
        # Store in history
        self.conversation_history.append((user_input, base_response))
        
        return base_response, art

    def respond(self, user_input):
        try:
            response, art = self.get_response(user_input)
            
            # Add spacing and colorful formatting
            self.console.print("\n")  # Add space after user input
            
            # Format JEFF's response with color and style
            styled_response = Text()
            styled_response.append("JEFF: ", style="bold magenta")
            styled_response.append(response, style="cyan")
            
            # Print the styled response
            self.console.print(styled_response)
            
            # If art was generated, add spacing and print it
            if art:
                self.console.print("\n")
                self.console.print(Panel(art, style="blue"))
            
            self.console.print("\n")  # Add space after JEFF's response
                
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")

    def handle_art_request(self, user_input):
        """Handle requests for art generation"""
        try:
            # Update terminal size before generating art
            self.ascii_art.update_terminal_size()
            
            # Extract subject from input
            words = user_input.lower().split()
            subject = None
            emotion_words = ["feel", "feeling", "mood", "emotion", "vibe"]
            
            # Check if asking about feelings/emotions
            if any(word in words for word in emotion_words):
                if self.current_mood == "chaotic":
                    art = self.ascii_art.generate_art("chaos full")  # Generate full-size chaotic art
                elif self.current_mood == "mysterious":
                    art = self.ascii_art.generate_art("mystery large")  # Generate large mysterious art
                else:
                    subject = self.current_interest
            else:
                # Extract specific subject and size from request
                size_words = ["tiny", "small", "little", "big", "large", "huge", "full"]
                subject_words = []
                for word in words:
                    if word not in ["draw", "art", "picture", "me", "a", "an", "the", "please", "can", "you", "of"] + size_words:
                        subject_words.append(word)
                
                subject = " ".join(subject_words) if subject_words else self.current_interest

            # Generate the art
            art = self.ascii_art.generate_art(subject)
            
            # Add mood-appropriate comment
            comments = {
                "chaotic": "Chaos is just order waiting to be discovered...",
                "mysterious": "Some mysteries are better left as art...",
                "philosophical": "Art, like life, is open to interpretation...",
                "playful": "Ta-da! How's that for creative expression?",
                "cosmic": "A glimpse into the infinite canvas of existence...",
                "enthusiastic": "BAM! Art attack! What do you think?",
                "deadpan": "Beep boop. Art generated.",
                "sarcastic": "Not bad for someone who doesn't have hands, eh?",
                "witty": "I call this one 'Perspective in ASCII'...",
                "chill": "Just vibing with some digital art...",
                "dramatic": "BEHOLD! My masterpiece!",
                "poetic": "A thousand pixels tell a single story..."
            }
            
            comment = comments.get(self.current_mood, "Here's what I came up with...")
            return f"\n{art}\n\n{comment}"
            
        except Exception as e:
            self.logger.error(f"Art generation error: {e}")
            return self.ascii_art.create_abstract_art("error")

    def determine_response_type(self, user_input):
        """Determine response type based on input patterns"""
        input_lower = user_input.lower()
        
        # Check for pattern matches
        for response_type, config in self.response_templates.items():
            if any(pattern in input_lower for pattern in config["patterns"]):
                return response_type
                
        # Default to casual for short inputs
        if len(input_lower.split()) <= 3:
            return "casual"
            
        # Use philosophical framework for longer queries
        return "philosophical"

    def handle_message(self, message):
        if message.lower().strip() in ['exit', 'quit']:
            return None
        
        if "interests" in message.lower():
            return self.personality.get_interests_response()
        
        # Rest of message handling...

    def adapt_conversation_style(self, user_input: str, context: list) -> dict:
        """Dynamically adjust conversation style based on interaction patterns"""
        style_adjustments = {
            "depth": 0.0,
            "creativity": 0.0,
            "technical": 0.0,
            "emotional": 0.0,
            "philosophical": 0.0
        }
        
        # Analyze input complexity
        words = user_input.split()
        if len(words) > 20:
            style_adjustments["depth"] += 0.2
            
        # Check for technical indicators
        technical_terms = ["code", "programming", "algorithm", "system", "technology"]
        if any(term in user_input.lower() for term in technical_terms):
            style_adjustments["technical"] += 0.3
            
        # Detect philosophical queries
        philosophical_indicators = ["why", "meaning", "purpose", "consciousness", "existence"]
        if any(term in user_input.lower() for term in philosophical_indicators):
            style_adjustments["philosophical"] += 0.4
            
        # Track emotional content
        emotional_terms = ["feel", "think", "believe", "love", "hate", "amazing", "terrible"]
        if any(term in user_input.lower() for term in emotional_terms):
            style_adjustments["emotional"] += 0.25
            
        return style_adjustments

    def integrate_knowledge(self, topic: str, depth_level: float) -> str:
        """Integrate specialized knowledge based on conversation context"""
        knowledge_base = {}
        
        # Load relevant knowledge based on topic
        for domain, file_path in self.knowledge_sources.items():
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    knowledge_base[domain] = json.load(f)
        
        # Select knowledge based on depth
        if depth_level < 0.3:
            return knowledge_base[topic].get("basic_concepts", [])
        elif depth_level < 0.6:
            return knowledge_base[topic].get("intermediate_concepts", [])
        else:
            return knowledge_base[topic].get("advanced_concepts", [])

def signal_handler(signum, frame):
    logger.info(f"Received signal {signum}")
    if 'system' in globals():
        system.stop()

def main():
    global system
    
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Set logging to ERROR to reduce output
        logging.getLogger().setLevel(logging.ERROR)
        
        system = JEFF()
        console.print("[bold blue]🤖 JEFF is online[/bold blue]")
        console.print("[italic]I have multiple personality traits and my mood changes randomly.[/italic]")
        console.print("[italic]Type 'exit' or 'quit' to end chat[/italic]\n")
        
        while True:
            try:
                # Format user input prompt
                console.print("\nYou: ", style="bold green", end="")
                user_input = input().strip()
                
                if user_input.lower() in ['exit', 'quit']:
                    console.print("\n[bold red]Goodbye! ʕ •ᴥ•ʔ[/bold red]")
                    break
                    
                system.respond(user_input)
                
            except KeyboardInterrupt:
                console.print("\n[bold red]Caught interrupt signal, shutting down...[/bold red]")
                break
            except Exception as e:
                console.print(f"[bold red]Error: {str(e)}[/bold red]")
                
    except Exception as e:
        logger.error(f"Error running ResponseSystem: {e}", exc_info=True)
    finally:
        console.print("\n👋 JEFF has left the chat")

def debug_mode():
    system = JEFF()
    print("\n🔍 Debug Mode - Testing System Components\n")
    
    # Test Ollama
    print("Testing Ollama...")
    response = system.ollama_agent.generate_response("Hello")
    print(f"Ollama Response: {response}\n")
    
    # Test Memory
    print("Testing Memory...")
    embedding = system.ollama_agent.generate_embedding("Test message")
    system.memory_manager.store_interaction("test_user", "Test message", embedding)
    context = system.memory_manager.retrieve_context("test_user")
    print(f"Memory Context: {context}\n")
    
    # Test Personality
    print("Testing Personality...")
    personality_response = system.personality.generate_response("Hello!")
    print(f"Personality Response: {personality_response}\n")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--debug":
        debug_mode()
    else:
        main() 