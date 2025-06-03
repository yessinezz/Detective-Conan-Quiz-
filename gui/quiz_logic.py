import json
import random
import os
from typing import Dict, List

class QuizGame:
    def __init__(self, quiz_file: str):
        self.score = 0
        # Get the absolute path to the questions.json file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.quiz_file = os.path.join(current_dir, quiz_file)
        self.arcs = self._load_arcs(self.quiz_file)
    
    def _load_arcs(self, filename: str) -> List[Dict]:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)['arcs']
    
    def _create_true_detective_arc(self) -> Dict:
        # Create a special arc with a percentage of questions from each arc
        true_detective_questions = []
        for arc in self.arcs:
            # Calculate how many questions to take (40% of questions, minimum 1)
            num_questions = max(1, round(len(arc['questions']) * 0.4))
            # Make sure we don't try to take more questions than available
            num_questions = min(num_questions, len(arc['questions']))
            # Get random questions from this arc
            arc_questions = random.sample(arc['questions'], num_questions)
            true_detective_questions.extend(arc_questions)
        # Shuffle all selected questions
        random.shuffle(true_detective_questions)
        return {
            "name": "True Detective",
            "description": "A special challenge with random questions from all arcs! Test your complete Detective Conan knowledge!",
            "questions": true_detective_questions
        }
