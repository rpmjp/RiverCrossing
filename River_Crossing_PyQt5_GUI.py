import sys
import queue
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QFrame, QMessageBox)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QRect, pyqtSignal
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QFont, QLinearGradient
from PyQt5.QtCore import QThread


class GameCanvas(QWidget):
    def __init__(self):
        super().__init__()
        self.game_state = (False, False, False, False)  # farmer, lion, goat, grass
        self.setMinimumHeight(400)
        self.character_positions = {}

    def set_game_state(self, state):
        self.game_state = state
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Background gradient
        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, QColor(135, 206, 250))  # Light blue
        gradient.setColorAt(1, QColor(176, 224, 230))  # Powder blue
        painter.fillRect(self.rect(), QBrush(gradient))

        # River
        river_width = self.width() // 4
        river_x = self.width() // 2 - river_width // 2

        # River gradient
        river_gradient = QLinearGradient(river_x, 0, river_x + river_width, 0)
        river_gradient.setColorAt(0, QColor(25, 25, 112))  # Midnight blue
        river_gradient.setColorAt(0.5, QColor(65, 105, 225))  # Royal blue
        river_gradient.setColorAt(1, QColor(25, 25, 112))  # Midnight blue

        painter.fillRect(river_x, 0, river_width, self.height(), QBrush(river_gradient))

        # River waves
        painter.setPen(QPen(QColor(255, 255, 255, 100), 2))
        for i in range(6):
            y = (self.height() // 6) * i + 30
            painter.drawLine(river_x + 20, y, river_x + river_width - 20, y + 5)
            painter.drawLine(river_x + 30, y + 15, river_x + river_width - 30, y + 20)

        # Left side (starting)
        left_gradient = QLinearGradient(0, 0, river_x, 0)
        left_gradient.setColorAt(0, QColor(144, 238, 144))  # Light green
        left_gradient.setColorAt(1, QColor(60, 179, 113))  # Medium sea green
        painter.fillRect(0, 0, river_x, self.height(), QBrush(left_gradient))

        # Right side (target)
        right_gradient = QLinearGradient(river_x + river_width, 0, self.width(), 0)
        right_gradient.setColorAt(0, QColor(60, 179, 113))  # Medium sea green
        right_gradient.setColorAt(1, QColor(34, 139, 34))  # Forest green
        painter.fillRect(river_x + river_width, 0, self.width() - river_x - river_width, self.height(),
                         QBrush(right_gradient))

        # Side labels
        painter.setPen(QPen(QColor(255, 255, 255), 2))
        painter.setFont(QFont("Arial", 16, QFont.Bold))
        painter.drawText(20, 30, "🏠 Starting Side")
        painter.drawText(self.width() - 150, 30, "🎯 Target Side")

        # Boat
        farmer, lion, goat, grass = self.game_state
        boat_x = river_x + 40 if not farmer else river_x + river_width - 80
        boat_y = self.height() // 2 - 15

        # Boat shadow
        painter.setPen(QPen(QColor(0, 0, 0, 50)))
        painter.setBrush(QBrush(QColor(0, 0, 0, 50)))
        painter.drawEllipse(boat_x + 2, boat_y + 2, 60, 30)

        # Boat
        boat_gradient = QLinearGradient(boat_x, boat_y, boat_x, boat_y + 30)
        boat_gradient.setColorAt(0, QColor(139, 69, 19))  # Saddle brown
        boat_gradient.setColorAt(1, QColor(101, 67, 33))  # Dark brown
        painter.setBrush(QBrush(boat_gradient))
        painter.setPen(QPen(QColor(62, 39, 35), 2))
        painter.drawEllipse(boat_x, boat_y, 60, 30)

        self.draw_characters(painter, river_x, river_width)

        # Invalid state warning
        if not self.is_valid(self.game_state):
            painter.setPen(QPen(QColor(255, 0, 0), 3))
            painter.setFont(QFont("Arial", 14, QFont.Bold))
            painter.drawText(self.width() // 2 - 100, self.height() - 20, "⚠️ INVALID STATE! ⚠️")

    def draw_characters(self, painter, river_x, river_width):
        farmer, lion, goat, grass = self.game_state

        characters = [
            ("👨‍🌾", "Farmer", farmer, QColor(70, 130, 180)),
            ("🦁", "Lion", lion, QColor(255, 165, 0)),
            ("🐐", "Goat", goat, QColor(169, 169, 169)),
            ("🌾", "Grass", grass, QColor(154, 205, 50))
        ]

        left_positions = [(80, 80), (80, 160), (80, 240), (80, 320)]
        right_positions = [(self.width() - 120, 80), (self.width() - 120, 160),
                           (self.width() - 120, 240), (self.width() - 120, 320)]

        left_idx = 0
        right_idx = 0

        for emoji, name, side, color in characters:
            if side:  # Right side
                if right_idx < len(right_positions):
                    x, y = right_positions[right_idx]
                    right_idx += 1
                else:
                    continue
            else:  # Left side
                if left_idx < len(left_positions):
                    x, y = left_positions[left_idx]
                    left_idx += 1
                else:
                    continue

            # Character background circle
            gradient = QLinearGradient(x - 30, y - 30, x + 30, y + 30)
            gradient.setColorAt(0, color.lighter(150))
            gradient.setColorAt(1, color.darker(120))

            painter.setBrush(QBrush(gradient))
            painter.setPen(QPen(color.darker(150), 3))
            painter.drawEllipse(x - 35, y - 35, 70, 70)

            # Character emoji/text
            painter.setPen(QPen(QColor(255, 255, 255), 2))
            painter.setFont(QFont("Arial", 24))

            # Draw emoji or fallback text
            if emoji in ["👨‍🌾", "🦁", "🐐", "🌾"]:
                painter.drawText(x - 15, y + 8, emoji)
            else:
                painter.drawText(x - 20, y + 8, name[:1])  # First letter fallback

            # Character name
            painter.setFont(QFont("Arial", 10, QFont.Bold))
            painter.drawText(x - 25, y + 50, name)

    def is_valid(self, state):
        farmer, lion, goat, grass = state
        if lion == goat and farmer != goat:
            return False
        if goat == grass and farmer != goat:
            return False
        return True


class RiverCrossingPuzzle(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_state = (False, False, False, False)
        self.start_state = (False, False, False, False)
        self.goal_state = (True, True, True, True)
        self.solution_path = []
        self.current_step = 0
        self.solving = False

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("🌊 River Crossing Puzzle - Premium Edition")
        self.setGeometry(100, 100, 900, 700)
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #e6f3ff, stop:1 #cce7ff);
            }
            QLabel {
                color: #2c3e50;
                font-weight: bold;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
                margin: 4px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5dade2, stop:1 #3498db);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2980b9, stop:1 #1f618d);
            }
            QPushButton:disabled {
                background: #bdc3c7;
                color: #7f8c8d;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title = QLabel("🌊 River Crossing Puzzle 🌊")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 28px;
            color: #2c3e50;
            font-weight: bold;
            margin: 10px;
        """)
        layout.addWidget(title)

        # Instructions
        instructions = QLabel(
            "Help the farmer transport everyone across the river safely!\n"
            "🚫 Lion cannot be alone with goat  •  🚫 Goat cannot be alone with grass"
        )
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setStyleSheet("""
            font-size: 14px;
            color: #34495e;
            background: rgba(255, 255, 255, 0.8);
            border-radius: 10px;
            padding: 15px;
            margin: 10px;
        """)
        layout.addWidget(instructions)

        # Game canvas
        self.canvas = GameCanvas()
        self.canvas.setStyleSheet("""
            border: 3px solid #34495e;
            border-radius: 15px;
            background: white;
        """)
        layout.addWidget(self.canvas)

        # Control buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        self.find_btn = QPushButton("🔍 Find Solution")
        self.find_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5dade2, stop:1 #3498db);
            }
        """)
        self.find_btn.clicked.connect(self.find_solution)

        self.auto_btn = QPushButton("▶️ Auto Solve")
        self.auto_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #27ae60, stop:1 #229954);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #58d68d, stop:1 #27ae60);
            }
        """)
        self.auto_btn.clicked.connect(self.auto_solve)

        self.step_btn = QPushButton("⏭️ Next Step")
        self.step_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #8e44ad, stop:1 #7d3c98);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #bb8fce, stop:1 #8e44ad);
            }
        """)
        self.step_btn.clicked.connect(self.next_step)

        self.reset_btn = QPushButton("🔄 Reset")
        self.reset_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e74c3c, stop:1 #c0392b);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ec7063, stop:1 #e74c3c);
            }
        """)
        self.reset_btn.clicked.connect(self.reset_game)

        button_layout.addWidget(self.find_btn)
        button_layout.addWidget(self.auto_btn)
        button_layout.addWidget(self.step_btn)
        button_layout.addWidget(self.reset_btn)

        layout.addLayout(button_layout)

        # Status label
        self.status_label = QLabel("🎮 Click 'Find Solution' to discover the optimal path!")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            font-size: 16px;
            color: #27ae60;
            background: rgba(255, 255, 255, 0.9);
            border-radius: 8px;
            padding: 12px;
            font-weight: bold;
        """)
        layout.addWidget(self.status_label)

        # Timer for auto-solving
        self.solve_timer = QTimer()
        self.solve_timer.timeout.connect(self.animate_next_step)

        self.update_display()

    def is_valid(self, state):
        farmer, lion, goat, grass = state
        if lion == goat and farmer != goat:
            return False
        if goat == grass and farmer != goat:
            return False
        return True

    def generate_moves(self, state):
        farmer, lion, goat, grass = state
        moves = []

        # Farmer takes goat
        if farmer == goat:
            new_state = (not farmer, lion, not goat, grass)
            if self.is_valid(new_state):
                moves.append(new_state)

        # Farmer takes lion
        if farmer == lion:
            new_state = (not farmer, not lion, goat, grass)
            if self.is_valid(new_state):
                moves.append(new_state)

        # Farmer takes grass
        if farmer == grass:
            new_state = (not farmer, lion, goat, not grass)
            if self.is_valid(new_state):
                moves.append(new_state)

        # Farmer goes alone
        new_state = (not farmer, lion, goat, grass)
        if self.is_valid(new_state):
            moves.append(new_state)

        return moves

    def bfs_solve(self):
        visited = set()
        q = queue.Queue()
        q.put((self.start_state, [self.start_state]))

        while not q.empty():
            state, path = q.get()
            if state == self.goal_state:
                return path

            visited.add(state)
            for move in self.generate_moves(state):
                if move not in visited:
                    q.put((move, path + [move]))
        return None

    def find_solution(self):
        self.solution_path = self.bfs_solve()
        if self.solution_path:
            self.current_step = 0
            self.status_label.setText(f"✅ Solution found! {len(self.solution_path)} steps total")
            self.current_state = self.solution_path[0]
            self.update_display()
        else:
            QMessageBox.information(self, "No Solution", "No solution found for this puzzle!")

    def auto_solve(self):
        if not self.solution_path:
            self.find_solution()
            return

        if self.solving:
            return

        self.solving = True
        self.auto_btn.setText("⏸️ Solving...")
        self.auto_btn.setEnabled(False)
        self.solve_timer.start(1500)  # 1.5 second intervals

    def animate_next_step(self):
        if self.current_step < len(self.solution_path) - 1:
            self.current_step += 1
            self.current_state = self.solution_path[self.current_step]
            self.update_display()
            self.status_label.setText(f"🎬 Step {self.current_step + 1} of {len(self.solution_path)}")
        else:
            # Finished
            self.solve_timer.stop()
            self.solving = False
            self.auto_btn.setText("▶️ Auto Solve")
            self.auto_btn.setEnabled(True)
            self.status_label.setText("🎉 Puzzle Solved! Everyone safely across! 🎉")
            QMessageBox.information(self, "🎉 Congratulations! 🎉",
                                    "You've successfully solved the river crossing puzzle!")

    def next_step(self):
        if not self.solution_path:
            self.status_label.setText("⚠️ Please find solution first!")
            return

        if self.current_step < len(self.solution_path) - 1:
            self.current_step += 1
            self.current_state = self.solution_path[self.current_step]
            self.update_display()

            if self.current_step == len(self.solution_path) - 1:
                self.status_label.setText("🎉 Puzzle Solved! Everyone safely across! 🎉")
                QMessageBox.information(self, "🎉 Congratulations! 🎉",
                                        "You've successfully solved the puzzle!")
            else:
                self.status_label.setText(f"📍 Step {self.current_step + 1} of {len(self.solution_path)}")
        else:
            self.status_label.setText("✅ Puzzle already completed!")

    def reset_game(self):
        self.solve_timer.stop()
        self.current_state = self.start_state
        self.solution_path = []
        self.current_step = 0
        self.solving = False
        self.auto_btn.setText("▶️ Auto Solve")
        self.auto_btn.setEnabled(True)
        self.status_label.setText("🔄 Game reset! Ready to solve!")
        self.update_display()

    def update_display(self):
        self.canvas.set_game_state(self.current_state)


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern look

    window = RiverCrossingPuzzle()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()