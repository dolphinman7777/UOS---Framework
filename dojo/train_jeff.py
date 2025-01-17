from src.agent.training.trainer import JeffTrainer

trainer = JeffTrainer()

# Train on philosophical concepts
philosophical_text = """
Reality is not what it seems. The deeper we look, the more we find that the 
universe operates on principles that defy classical logic. Quantum mechanics 
shows us that particles can exist in multiple states simultaneously until observed.

The nature of consciousness remains one of the greatest mysteries. Are we merely 
complex arrangements of matter, or is there something more fundamental about awareness?

Time itself might be an emergent property, not the fundamental dimension we 
experience it as. The present moment could be an illusion - past and future 
existing simultaneously in a block universe.
"""

trainer.add_training_text("philosophy", philosophical_text)

# Train on technical knowledge
technical_text = """
Distributed systems operate under fundamental constraints:
1. Network delays are unpredictable
2. Process failures can occur at any time
3. Information travels at finite speeds

The CAP theorem states that it's impossible for a distributed system to 
simultaneously provide:
- Consistency
- Availability 
- Partition tolerance

You must choose two at the expense of the third.
"""

trainer.add_training_text("technical", technical_text)

# Train on creative concepts
creative_text = """
Creativity emerges from the intersection of diverse ideas. The most innovative 
solutions often come from connecting seemingly unrelated concepts.

The creative process isn't linear. It involves:
- Divergent thinking (generating many possibilities)
- Convergent thinking (selecting the best options)
- Iteration and refinement
- Testing and validation

Great ideas often come from questioning assumptions and looking at problems 
from multiple perspectives.
"""

trainer.add_training_text("creative", creative_text) 