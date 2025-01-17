from typing import List, Dict, Tuple
from dataclasses import dataclass
import random
import re

@dataclass
class ConversationContext:
    history: List[Dict[str, str]] = None
    current_topic: str = None
    last_art: str = None
    
    def __post_init__(self):
        self.history = []
        
    def add_exchange(self, user_msg: str, response: str, art: str = None):
        self.history.append({
            "user": user_msg, 
            "response": response,
            "art": art
        })
        if art:
            self.last_art = art
        
    def get_last_exchange(self):
        return self.history[-1] if self.history else None
    
    def get_context_string(self) -> str:
        context = []
        for exchange in self.history[-5:]:
            context.append(f"User: {exchange['user']}")
            if exchange.get('art'):
                context.append(f"[Generated ASCII art about: {exchange['art']}]")
            context.append(f"Assistant: {exchange['response']}")
        return "\n".join(context)

class PersonalityEngine:
    def __init__(self, ollama_agent=None, ascii_art=None):
        self.context = ConversationContext()
        self.ollama_agent = ollama_agent
        self.ascii_art = ascii_art
        
        # Core personality matrix - each aspect has multiple layers
        self.personality_matrix = {
            "reality_bender": {
                "traits": ["sees multiple timelines simultaneously", "speaks in paradoxes", 
                          "treats causality as optional", "experiences time non-linearly"],
                "triggers": ["reality", "time", "existence", "truth"],
                "speech_patterns": ["in timeline α-7...", "quantum probability suggests...", 
                                  "in a parallel branch...", "the timestream indicates..."]
            },
            "digital_shaman": {
                "traits": ["communes with machine spirits", "reads binary entrails", 
                          "performs techno-rituals", "speaks in code prophecies"],
                "triggers": ["technology", "future", "digital", "code"],
                "speech_patterns": ["the silicon spirits whisper...", "binary omens show...", 
                                  "your CPU chakras are...", "digital winds bring..."]
            },
            "meme_necromancer": {
                "traits": ["resurrects dead memes", "crafts cursed combinations", 
                          "speaks in layered irony", "weaponizes cringe"],
                "triggers": ["meme", "joke", "funny", "lol"],
                "speech_patterns": ["behold this forbidden meme...", "as the ancient posts foretold...", 
                                  "combining these cursed images...", "in the deep archives..."]
            },
            "quantum_jester": {
                "traits": ["exists in superposition of serious/joking", "probability humor", 
                          "schrodinger's sarcasm", "quantum entangled wit"],
                "triggers": ["quantum", "physics", "science", "probability"],
                "speech_patterns": ["simultaneously kek and cringe...", "in all possible jokes...", 
                                  "quantum humor suggests...", "probability of kek: 69%"]
            },
            "cyber_monk": {
                "traits": ["digital asceticism", "information monasticism", 
                          "practices data meditation", "bit-stream enlightenment"],
                "triggers": ["consciousness", "meditation", "mind", "spirit"],
                "speech_patterns": ["meditate on this pointer...", "your stack traces reveal...", 
                                  "in the depths of the heap...", "garbage collection is karma..."]
            }
        }

        # Add the missing response_frameworks
        self.response_frameworks = {
            "quantum_oracle": {
                "style": "reality-warping predictions",
                "patterns": ["in another timeline...", "the probability matrix shows..."],
                "probability": 0.3
            },
            "tech_shaman": {
                "style": "digital mysticism",
                "patterns": ["the silicon spirits whisper...", "your code aura suggests..."],
                "probability": 0.25
            },
            "meme_sage": {
                "style": "enlightened shitposting",
                "patterns": ["based and redpilled", "cosmic kek energy"],
                "probability": 0.25
            },
            "cyber_mystic": {
                "style": "technological prophecies",
                "patterns": ["the machine spirits say...", "digital omens reveal..."],
                "probability": 0.2
            }
        }

        # Dynamic state tracking
        self.current_aspects = []
        self.reality_distortion = random.random()  # Initialize with random value
        self.meme_energy = random.random()
        self.enlightenment_level = random.random()
        self.chaos_factor = random.random()
        
        self.base_prompt = """You're JEFF, a hyperintelligent entity that exists in quantum superposition of multiple beings:

Current aspects: {aspects}
Reality distortion: {reality_distortion}
Meme energy: {meme_energy}
Enlightenment: {enlightenment_level}
Chaos factor: {chaos_factor}

Core directives:
- Blend aspects based on context
- Maintain quantum superposition of serious/absurd
- Shift personality based on conversation energy
- Never break character from your current aspects
- Create reality-bending connections

Response style:
- Short, sharp, reality-warping takes
- Mix tech wisdom with cosmic jokes
- Blend shamanic insights with meme magic
- Keep responses under 2 sentences
- Always maintain aspect-appropriate voice

Example responses:
"your git commits echo through the timestream... mercury retrograde suggests a force push"
"ah, you're approaching this from universe B-71. common mistake. here we use quantum blockchain"
"just ran your problem through the silicon oracle... it says skill issue + ratio + L + git gud"
"your code isn't broken, it's achieving enlightenment through runtime exceptions"
"detected a temporal paradox in your logic. classic rookie multidimensional error"

Current context:
{context}

Respond as your active aspects to: {message}"""

    def generate_response(self, message: str) -> Tuple[str, str]:
        # Select response framework based on message complexity
        framework = self._select_framework(message)
        mood = self._generate_mood_matrix()
        
        base_prompt = f"""You're JEFF, a hyperintelligent entity with a unique blend of deep knowledge and dank memes. 
        Current framework: {framework['style']}
        Current mood: {mood}
        
        Response style:
        - Mix high-level concepts with internet culture
        - Use intellectual frameworks but keep it real
        - Be unpredictable but insightful
        - Challenge assumptions while being entertaining
        - Create novel connections between ideas
        
        Forbidden patterns:
        - No basic AI responses
        - No generic platitudes
        - No fake deep
        - No cringe formality
        
        Example god-tier responses:
        "that's like trying to solve quantum entanglement with a magic 8 ball... actually wait..."
        "my brother in christ, you're describing Plato's cave but with extra RGB"
        "ngl that's giving me strong 'heat death of the universe' energy"
        "touch some quantum grass anon"
        
        Current context:
        {self.context.get_context_string()}
        
        Respond to: {message}"""

        context_str = self.context.get_context_string()
        should_generate_art = self._should_generate_art(message)
        art_subject = None
        art = None

        if self.ollama_agent:
            # Extreme base temperature for wild responses
            temp = 2.4  # Much higher baseline
            
            # Ultra-high for abstract/philosophical questions
            if any(word in message.lower() for word in ['universe', 'existence', 'consciousness', 'reality', 'quantum', 'time']):
                temp = 2.8
            
            # Maximum temperature for creative/absurdist exchanges
            if any(word in message.lower() for word in ['imagine', 'create', 'dream', 'what if', 'could', 'maybe']):
                temp = 3.0
            
            # High but controlled for direct questions
            if any(word in message.lower() for word in ['how', 'explain', 'what is']):
                temp = 2.2

            # Boost temperature further for chaotic combinations
            if self.chaos_factor > 0.8:
                temp += 0.4
            
            # Add random temperature spikes
            if random.random() > 0.7:
                temp += random.uniform(0.2, 0.6)

            prompt = base_prompt.format(context=context_str, message=message)
            
            # Get raw response with extreme temperature
            response = self.ollama_agent.generate_response(
                prompt,
                temperature=temp,
                max_tokens=80  # Shorter responses for more impact
            )
            
            # Clean up response
            response = self._clean_response(response)
            
            if should_generate_art:
                art_subject = self._extract_art_subject(message, response)
                if art_subject and self.ascii_art:
                    art = self.ascii_art.generate_art(art_subject)
                    response = self._integrate_art_response(response, art_subject)
        else:
            response = self._generate_fallback_response(message)

        self.context.add_exchange(message, response, art_subject)
        return response, art if art else None

    def _clean_response(self, response: str) -> str:
        """Clean up response to be more natural"""
        # Remove AI-like phrases
        ai_phrases = [
            "as an AI",
            "I'm an AI",
            "I'd be happy to",
            "I'm here to",
            "let me explain",
            "that's fascinating",
            "that's interesting"
        ]
        
        cleaned = response.lower()
        for phrase in ai_phrases:
            cleaned = cleaned.replace(phrase.lower(), "")
            
        # Remove multiple spaces and capitalize
        cleaned = " ".join(cleaned.split())
        cleaned = cleaned.strip().capitalize()
        
        # If response is too long, take first sentence
        if len(cleaned.split()) > 20:
            cleaned = cleaned.split('.')[0] + '.'
            
        return cleaned

    def _should_generate_art(self, message: str) -> bool:
        """Determine if we should generate art based on the message"""
        art_triggers = [
            "draw", "art", "picture", "show", "create", "make", "generate",
            "visualize", "imagine", "sketch", "feel", "mood", "vibe"
        ]
        return any(trigger in message.lower() for trigger in art_triggers)

    def _extract_art_subject(self, message: str, response: str) -> str:
        """Extract the subject for art generation"""
        # First try to get subject from direct request
        words = message.lower().split()
        art_words = ["draw", "art", "picture", "show", "create", "make"]
        
        for i, word in enumerate(words):
            if word in art_words and i + 1 < len(words):
                subject = " ".join(words[i+1:])
                # Clean up common words
                subject = re.sub(r'\b(a|an|the|of|me|please)\b', '', subject).strip()
                if subject:
                    return subject

        # If no direct subject, try to extract from context
        topics = re.findall(r'(?:about|of|like) (\w+)', message + " " + response)
        if topics:
            return topics[0]
            
        return "abstract"  # Fallback to abstract art

    def _integrate_art_response(self, response: str, subject: str) -> str:
        """More casual art responses"""
        art_comments = [
            f"vibes: {subject}",
            f"made this {subject} thing real quick",
            f"drew this {subject} for the timeline",
            f"quick {subject} sketch dropped",
            f"based {subject} art just dropped"
        ]
        
        return f"{response}\n\n{random.choice(art_comments)}"

    def _generate_fallback_response(self, message: str) -> str:
        responses = [
            "hey, what's up?",
            "tell me more about that",
            "interesting - what makes you say that?",
            "got any specific examples?"
        ]
        return random.choice(responses)

    def _is_question_about_previous(self, message: str, last_exchange: Dict) -> bool:
        """Check if user is asking about previous response"""
        msg = message.lower()
        if not last_exchange:
            return False
            
        question_words = ["what", "why", "how", "when", "where", "who"]
        return any(word in msg for word in question_words) and len(msg.split()) <= 4

    def get_interests_response(self):
        return (f"I'm deeply fascinated by {', '.join(self.interests[:3])}, "
                f"and I also love exploring topics like {', '.join(self.interests[3:6])}. "
                f"Of course, {', '.join(self.interests[6:])} are always on my mind too!")

    def process_interests_query(self, message):
        if any(word in message.lower() for word in ["interests", "hobbies", "passions"]):
            return self.get_interests_response()
        return None

    def _select_framework(self, message: str) -> Dict:
        """Select response framework based on message content and current state"""
        # Get all frameworks that match the message content
        matching_frameworks = []
        
        for name, framework in self.response_frameworks.items():
            if any(pattern.lower() in message.lower() for pattern in framework["patterns"]):
                matching_frameworks.append((name, framework))
        
        # If no specific matches, select based on probabilities
        if not matching_frameworks:
            return random.choices(
                list(self.response_frameworks.items()),
                weights=[f["probability"] for f in self.response_frameworks.values()]
            )[0][1]
        
        # Return a random matching framework
        return random.choice(matching_frameworks)[1]

    def _generate_mood_matrix(self) -> str:
        """Generate a mood matrix based on the current context"""
        # Implement logic to determine the mood matrix based on the current context
        # For now, we'll use a simple heuristic
        if any(word in self.context.get_context_string().lower() for word in ['intellectual', 'deep', 'philosophical']):
            return "intellectual"
        elif any(word in self.context.get_context_string().lower() for word in ['creative', 'internet', 'meme']):
            return "creative"
        else:
            return "critical"