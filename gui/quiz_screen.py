import random
import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QMessageBox, 
                           QLabel, QProgressBar)
from PyQt6.QtCore import Qt, QTimer
from quiz_logic import QuizGame

class QuizScreen(QWidget):
    BUTTON_STYLE = "QPushButton {background-color: rgba(0, 0, 0, 0.85); color: white; border: 2px solid white; border-radius: 15px; padding: 15px 20px; font-size: 16px; text-align: left} QPushButton:hover {background-color: rgba(0, 0, 0, 0.95); border-color: #00ffff; color: #00ffff}"
    
    CORRECT_STYLE = "QPushButton {background-color: rgba(46, 204, 113, 0.95); color: white; border: 2px solid #2ecc71; border-radius: 15px; padding: 15px 20px; font-size: 16px; text-align: left; font-weight: bold}"
    
    INCORRECT_STYLE = "QPushButton {background-color: rgba(231, 76, 60, 0.95); color: white; border: 2px solid #e74c3c; border-radius: 15px; padding: 15px 20px; font-size: 16px; text-align: left; font-weight: bold}"

    def __init__(self, parent=None):
        super().__init__(parent)
        try:
            # Get the absolute path to questions.json
            current_dir = os.path.dirname(os.path.abspath(__file__))
            quiz_file = os.path.join(current_dir, 'questions.json')
            
            if not os.path.exists(quiz_file):
                raise FileNotFoundError(f'Questions file not found: {quiz_file}')
            
            self.quiz_game = QuizGame(quiz_file)
            if not self.quiz_game.arcs:
                raise ValueError('No quiz questions found in the file')
            
            self.current_question = 0
            self.score = 0
            self.questions = []
            self.current_correct = 0  # Add this line to define current_correct
            self.initUI()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to initialize quiz: {str(e)}')
            if parent:
                parent.close()

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(40, 30, 40, 30)
        
        # Progress bar
        self.progress = QProgressBar()
        self.progress.setFixedHeight(30)
        self.progress.setStyleSheet("QProgressBar {border: 2px solid white; border-radius: 12px; text-align: center; background-color: rgba(0, 0, 0, 0.7); color: white; font-size: 14px; font-weight: bold} QProgressBar::chunk {background-color: rgba(52, 152, 219, 0.9); border-radius: 10px}")
        self.layout.addWidget(self.progress)

        # Question label
        self.question_label = QLabel()
        self.question_label.setWordWrap(True)
        self.question_label.setStyleSheet("QLabel {color: white; font-size: 18px; background-color: rgba(0, 0, 0, 0.85); padding: 20px 25px; border-radius: 15px; line-height: 1.4; margin-bottom: 15px; min-height: 120px}")
        self.layout.addWidget(self.question_label)

        # Answer buttons
        self.answer_buttons = []
        for i in range(3):
            btn = QPushButton()
            btn.setFixedHeight(80)
            btn.setStyleSheet("QPushButton {background-color: rgba(0, 0, 0, 0.85); color: white; border: 2px solid white; border-radius: 15px; padding: 15px 20px; font-size: 16px; text-align: left} QPushButton:hover {background-color: rgba(0, 0, 0, 0.95); border-color: #00ffff; color: #00ffff}")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, idx=i: self.check_answer(idx))
            self.answer_buttons.append(btn)
            self.layout.addWidget(btn)

        # Add stretch to keep everything aligned to the top
        self.layout.addStretch(1)

    def start_quiz(self, arc_name):
        if arc_name == 'All Arcs':
            all_questions = []
            for arc in self.quiz_game.arcs:
                all_questions.extend(arc['questions'])
            self.questions = all_questions
        elif arc_name == 'True Detective':
            self.questions = self.quiz_game._create_true_detective_arc()['questions']
        else:
            for arc in self.quiz_game.arcs:
                if arc['name'] == arc_name:
                    self.questions = arc['questions'].copy()
                    break
        
        random.shuffle(self.questions)
        self.current_question = 0
        self.score = 0
        self.progress.setMaximum(len(self.questions))  # Set max value to total questions
        self.progress.setValue(0)  # Start at 0
        self.show_question()

    def show_question(self):
        if self.current_question < len(self.questions):
            question = self.questions[self.current_question]
            
            # Update progress bar - add 1 to current_question since it's 0-based
            progress_value = ((self.current_question + 1) / len(self.questions)) * 100
            self.progress.setValue(self.current_question + 1)
            self.progress.setFormat(f'Progress: {progress_value:.1f}% ({self.current_question + 1}/{len(self.questions)})')
            
            # Update question text with better formatting
            question_text = (
                f'<div style="text-align: center; font-size: 18px; margin-bottom: 10px;">' 
                f'Question {self.current_question + 1}/{len(self.questions)}'
                f'</div>'
                f'<div style="font-size: 16px; margin-top: 5px; line-height: 1.3;">' 
                f'{question["question"]}'
                f'</div>'
            )
            self.question_label.setText(question_text)
            
            # Randomize options and add letter prefixes
            options = question['options'].copy()
            correct_option = options[question['correct_answer']]
            random.shuffle(options)
            
            # Update buttons with letter prefixes
            for i, (btn, option) in enumerate(zip(self.answer_buttons, options)):
                # Simple format: letter + option text
                btn.setText(f'{chr(97 + i)}. {option}')
                
            # Store correct answer
            self.current_correct = options.index(correct_option)
        else:
            self.show_final_score()

    def check_answer(self, selected_idx):
        if selected_idx == self.current_correct:
            self.score += 1
            self.answer_buttons[selected_idx].setStyleSheet(self.CORRECT_STYLE)
        else:
            self.answer_buttons[selected_idx].setStyleSheet(self.INCORRECT_STYLE)
            self.answer_buttons[self.current_correct].setStyleSheet(self.CORRECT_STYLE)

        QTimer.singleShot(1500, self.next_question)

    def next_question(self):
        # Reset button styles
        for btn in self.answer_buttons:
            btn.setStyleSheet(self.BUTTON_STYLE)

        self.current_question += 1
        self.show_question()

    def show_final_score(self):
        percentage = (self.score / len(self.questions)) * 100
        message = (
            f'<div style="text-align: center;">'
            f'<h2 style="color: #00ffff;">Quiz completed!</h2>'
            f'<p style="font-size: 18px; margin: 15px 0;">'
            f'Final score: {self.score}/{len(self.questions)}<br>'
            f'Percentage: {percentage:.2f}%'
            f'</p><p style="font-size: 16px; margin: 15px 0;">'
        )
        
        if percentage == 100:
            message += '🌟 Perfect score! You\'re a true Detective Conan expert! 🌟'
        elif percentage >= 80:
            message += '✨ Great job! You really know your Detective Conan! ✨'
        elif percentage >= 60:
            message += '👍 Good work! Keep watching Detective Conan to learn more!'
        else:
            message += '💪 Keep trying! There\'s still more to learn about Detective Conan!'
        
        message += '</p><p style="font-size: 14px; margin-top: 20px;">Returning to main menu in 5 seconds...</p></div>'

        # Show stylized message in question label
        self.question_label.setText(message)
        self.progress.setValue(len(self.questions))
        
        # Hide answer buttons temporarily
        for btn in self.answer_buttons:
            btn.hide()
            
        # Return to main menu after 5 seconds
        QTimer.singleShot(5000, self.return_to_menu)
        
    def return_to_menu(self):
        # Return to main menu
        # Get the main window (parent of the stacked widget)
        main_window = self.parent().parent()
        
        # Show answer buttons again so they're visible for the next quiz
        for btn in self.answer_buttons:
            btn.show()
            
        if main_window:
            # Reset background to default
            main_window.set_background(main_window.default_background)
            # Switch to main menu widget
            main_window.central_widget.setCurrentWidget(main_window.main_menu)