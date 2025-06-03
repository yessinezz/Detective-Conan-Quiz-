import json
from typing import Dict, List, Tuple
import random

class QuizGame:
    def __init__(self, quiz_file: str):
        self.score = 0
        self.arcs = self._load_arcs(quiz_file)
    
    def _load_arcs(self, filename: str) -> List[Dict]:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)['arcs']
    
    def _randomize_options(self, question: Dict) -> Tuple[List[str], int]:
        # Get the original options and correct answer
        options = question['options'].copy()
        correct_option = options[question['correct_answer']]
        
        # Shuffle the options
        random.shuffle(options)
        
        # Find the new position of the correct answer
        new_correct_index = options.index(correct_option)
        
        return options, new_correct_index
    
    def display_question(self, question: Dict, num: int, randomized_options: List[str]) -> None:
        print("\n" + "="*50)
        print(f"Question {num}:")
        print(question['question'])
        print("-"*50)
        for i, option in enumerate(randomized_options):
            print(f"{chr(97 + i)}. {option}")
        print("="*50)
    
    def _create_true_detective_arc(self) -> Dict:
        # Create a special arc with 4 random questions from each arc
        true_detective_questions = []
        for arc in self.arcs:
            # Get 4 random questions from this arc
            arc_questions = random.sample(arc['questions'], 4)
            true_detective_questions.extend(arc_questions)
        # Shuffle all selected questions
        random.shuffle(true_detective_questions)
        return {
            "name": "True Detective",
            "description": "A special challenge with random questions from all arcs! Test your complete Detective Conan knowledge!",
            "questions": true_detective_questions
        }

    def select_arc(self) -> Dict:
        print("\nAvailable Arcs:")
        print("0. All Arcs - Test yourself with all questions")
        for i, arc in enumerate(self.arcs, 1):
            print(f"{i}. {arc['name']} - {arc['description']}")
        print(f"{len(self.arcs) + 1}. True Detective - Special challenge with random questions from all arcs!")
        
        while True:
            try:
                choice = int(input(f"\nSelect an arc (0-{len(self.arcs) + 1}): "))
                if 0 <= choice <= len(self.arcs) + 1:
                    break
                print(f"Please enter a number between 0 and {len(self.arcs) + 1}")
            except ValueError:
                print("Please enter a valid number")
        
        if choice == 0:
            # Combine all questions from all arcs
            all_questions = []
            for arc in self.arcs:
                all_questions.extend(arc['questions'])
            return {"name": "All Arcs", "questions": all_questions}
        elif choice == len(self.arcs) + 1:
            # Create the True Detective special arc
            return self._create_true_detective_arc()
        else:
            return self.arcs[choice - 1]
    
    def play(self) -> None:
        print("Welcome to Detective Conan Quiz!")
        
        arc = self.select_arc()
        questions = arc['questions']
        print(f"\nSelected: {arc['name']}")
        print(f"Total questions: {len(questions)}\n")
        
        # Shuffle questions
        random.shuffle(questions)
        self.score = 0
        total_questions = len(questions)
        
        for i, question in enumerate(questions, 1):
            # Randomize options for this question
            randomized_options, correct_index = self._randomize_options(question)
            self.display_question(question, i, randomized_options)
            
            while True:
                answer = input("\nYour answer (a/b/c): ").lower().strip()
                if answer in ['a', 'b', 'c']:
                    answer_index = ord(answer) - 97
                    break
                print("Please enter a, b, or c")
            
            if answer_index == correct_index:
                print("\n✓ Correct! Well done!")
                self.score += 1
            else:
                correct = randomized_options[correct_index]
                print(f"\n✗ Wrong! The correct answer was: {correct}")
            
            print(f"Score: {self.score}/{i}")
            input("\nPress Enter to continue...")
          # Show final score
        print("\n" + "="*50)
        print("Quiz completed!")
        print(f"Final score: {self.score}/{total_questions}")
        percentage = (self.score / total_questions) * 100
        print(f"Percentage: {percentage:.1f}%")
        
        if percentage == 100:
            print("Perfect score! You're a true Detective Conan expert!")
        elif percentage >= 80:
            print("Great job! You really know your Detective Conan!")
        elif percentage >= 60:
            print("Good work! Keep watching Detective Conan to learn more!")
        else:
            print("Keep trying! There's still more to learn about Detective Conan!")
            
        # Ask if they want to continue with another arc
        while True:
            choice = input("\nWant to solve another case, Detective? (y/n): ").lower().strip()
            if choice in ['y', 'n']:
                break
            print("Please enter 'y' for yes or 'n' for no")
        
        if choice == 'y':
            print("\n" + "="*50)
            self.score = 0  # Reset score for new arc
            self.play()  # Start a new arc
        else:
            print("\nThank you for playing, Detective! Until next time!")

if __name__ == "__main__":
    import os
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Create the full path to questions.json
    quiz_file = os.path.join(script_dir, 'questions.json')
    quiz = QuizGame(quiz_file)
    quiz.play()
