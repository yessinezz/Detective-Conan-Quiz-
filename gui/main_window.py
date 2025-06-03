import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton,
                           QLabel, QStackedWidget, QMessageBox, QApplication,
                           QGraphicsBlurEffect)
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QPixmap, QIcon

from quiz_screen import QuizScreen

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_background = None
        self.default_background = None
        self.background_label = None
        self.blur_effect = None
        self.bg_zoom = 1.0
        self.bg_zoom_direction = 1
        self.bg_timer = None
        self.bg_pan_x = 0
        self.bg_pan_y = 0
        self.pan_direction_x = 1
        self.pan_direction_y = 1
        
        self.project_root = os.path.dirname(os.path.dirname(__file__))
        self.initUI()

    def set_background(self, image_path):
        if not self.background_label:
            self.background_label = QLabel(self)
            self.background_label.setGeometry(0, 0, 800, 600)
            self.background_label.lower()
            self.blur_effect = QGraphicsBlurEffect()
            self.blur_effect.setBlurRadius(8)  # Slightly reduced blur for sharper image
            self.background_label.setGraphicsEffect(self.blur_effect)
        if image_path and os.path.exists(image_path):
            self.current_background = QPixmap(image_path)
            self.update_blurred_background()

    def update_blurred_background(self):
        if self.current_background:
            # Calculate zoom and pan
            scaled_size = QSize(
                int(800 * (self.bg_zoom + 0.2)),  # Add 0.2 for more dramatic zoom
                int(600 * (self.bg_zoom + 0.2))
            )
            pixmap = self.current_background.scaled(
                scaled_size,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            
            # Calculate pan offset
            max_pan_x = max(0, (pixmap.width() - 800) // 2)
            max_pan_y = max(0, (pixmap.height() - 600) // 2)
            
            # Apply pan with bounds checking
            x = max(0, min(max_pan_x, (pixmap.width() - 800) // 2 + self.bg_pan_x))
            y = max(0, min(max_pan_y, (pixmap.height() - 600) // 2 + self.bg_pan_y))
            
            # Crop the image at the calculated position
            cropped = pixmap.copy(int(x), int(y), 800, 600)
            self.background_label.setPixmap(cropped)
            self.background_label.setGeometry(0, 0, 800, 600)

    def animate_background(self):
        if not self.bg_timer:
            self.bg_timer = QTimer(self)
            self.bg_timer.timeout.connect(self._animate_bg_step)
            self.bg_timer.start(30)  # Faster updates for smoother animation

    def _animate_bg_step(self):
        # Zoom animation
        zoom_speed = 0.0008
        if self.bg_zoom_direction == 1:
            self.bg_zoom += zoom_speed
            if self.bg_zoom >= 1.15:  # Increased zoom range
                self.bg_zoom_direction = -1
        else:
            self.bg_zoom -= zoom_speed
            if self.bg_zoom <= 1.0:
                self.bg_zoom_direction = 1

        # Pan animation
        pan_speed = 0.3
        if self.pan_direction_x == 1:
            self.bg_pan_x += pan_speed
            if self.bg_pan_x >= 30:  # Limit pan range
                self.pan_direction_x = -1
        else:
            self.bg_pan_x -= pan_speed
            if self.bg_pan_x <= -30:
                self.pan_direction_x = 1

        if self.pan_direction_y == 1:
            self.bg_pan_y += pan_speed * 0.7  # Slower vertical pan
            if self.bg_pan_y >= 20:
                self.pan_direction_y = -1
        else:
            self.bg_pan_y -= pan_speed * 0.7
            if self.bg_pan_y <= -20:
                self.pan_direction_y = 1

        self.update_blurred_background()

    def center_window(self):
        # Get the screen geometry
        screen = QApplication.primaryScreen().geometry()
        # Get the window geometry
        window = self.geometry()
        # Calculate the center point
        center_point = screen.center()
        # Move window to center
        self.setGeometry(
            center_point.x() - 400,  # Half of width (800/2)
            center_point.y() - 300,  # Half of height (600/2)
            800, 600  # Fixed size
        )

    def initUI(self):
        # Set window properties
        self.setWindowTitle('Detective Conan Quiz')
        self.setFixedSize(800, 600)  # Fixed size only
        
        # Set window icon
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Icon.jpg')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            
        self.center_window()
        
        # Set initial background image
        self.default_background = os.path.join(self.project_root, 'images', 'Main.jpg')
        self.set_background(self.default_background)
        self.animate_background()

        # Create central widget and layout
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        # Create main menu and quiz screen
        self.main_menu = QWidget()
        self.quiz_screen = QuizScreen(self)
        
        # Add widgets to stack
        self.central_widget.addWidget(self.main_menu)
        self.central_widget.addWidget(self.quiz_screen)

        # Store background images for each arc
        self.arc_backgrounds = {
            "All Arcs": os.path.join(self.project_root, 'images', 'All arcs.jpg'),
            "Conan Arc": os.path.join(self.project_root, 'images', 'Conan Arc.jpg'),
            "Sherry Arc": os.path.join(self.project_root, 'images', 'Sherry Arc.jpg'),
            "Vermouth Arc": os.path.join(self.project_root, 'images', 'Vermouth Arc.jpg'),
            "Boss's Phone Number Arc": os.path.join(self.project_root, 'images', "Boss's Phone Number Arc.jpg"),
            "Kir Arc": os.path.join(self.project_root, 'images', 'Kir Arc.jpg'),
            "Bourbon Arc": os.path.join(self.project_root, 'images', 'Bourbon Arc.jpg'),
            "Rum Arc": os.path.join(self.project_root, 'images', 'Rum Arc.jpg'),
            "True Detective": os.path.join(self.project_root, 'images', 'True Detective.jpg')
        }
        
        # Main menu layout setup
        outer_layout = QVBoxLayout(self.main_menu)
        outer_layout.setContentsMargins(40, 40, 40, 40)
        outer_layout.setSpacing(0)
        
        # Center container for buttons
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        center_layout.setSpacing(10)
        center_widget.setFixedWidth(650)

        # Common button style
        button_style = '''
            QPushButton {
                background-color: rgba(0, 0, 0, 0.85);
                color: white;
                border: 2px solid white;
                border-radius: 10px;
                padding: 12px;
                font-size: 18px;
                font-weight: bold;
            }            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.95);
                border-color: #00ffff;
                color: #00ffff;
            }
        '''

        # Add buttons for each arc
        arcs = [
            "All Arcs",
            "Conan Arc",
            "Sherry Arc",
            "Vermouth Arc",
            "Boss's Phone Number Arc",
            "Kir Arc",
            "Bourbon Arc",
            "Rum Arc",
            "True Detective"
        ]

        outer_layout.addStretch(1)
        
        for arc in arcs:
            btn = QPushButton(arc)
            btn.setStyleSheet(button_style)
            btn.setFixedSize(550, 45)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, arc=arc: self.start_quiz(arc))
            center_layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)

        # Add spacing before Credits and Quit
        spacer = QWidget()
        spacer.setFixedHeight(15)
        center_layout.addWidget(spacer)

        # Add Credits and Quit buttons with same style
        credits_btn = QPushButton("Credits")
        credits_btn.setStyleSheet(button_style)
        credits_btn.setFixedSize(550, 45)
        credits_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        credits_btn.clicked.connect(self.show_credits)
        center_layout.addWidget(credits_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        quit_btn = QPushButton("Quit")
        quit_btn.setStyleSheet(button_style)
        quit_btn.setFixedSize(550, 45)
        quit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        quit_btn.clicked.connect(self.close)
        center_layout.addWidget(quit_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        # Add the centered widget to main layout
        outer_layout.addWidget(center_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        outer_layout.addStretch(1)

    def start_quiz(self, arc_name):
        if arc_name in self.arc_backgrounds:
            self.set_background(self.arc_backgrounds[arc_name])
            self.quiz_screen.start_quiz(arc_name)
            self.central_widget.setCurrentWidget(self.quiz_screen)

    def show_credits(self):
        credits_text = """
        Made By Med Yessine Khmiri (Student)
        """
        
        QMessageBox.information(self, "Credits", credits_text)
