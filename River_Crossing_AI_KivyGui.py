from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Ellipse, Line
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.popup import Popup
import queue


class GameCanvas(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_state = (False, False, False, False)  # farmer, lion, goat, grass
        self.character_positions = {}
        self.boat_pos = [0, 0]
        self.bind(size=self.update_graphics, pos=self.update_graphics)

    def update_graphics(self, *args):
        self.canvas.clear()
        with self.canvas:
            # Background gradient effect
            Color(0.6, 0.8, 1, 1)  # Light blue
            Rectangle(pos=self.pos, size=self.size)

            # River with gradient effect
            river_width = self.width * 0.25
            river_x = self.center_x - river_width / 2

            # River gradient layers
            Color(0.2, 0.4, 0.8, 1)  # Dark blue
            Rectangle(pos=(river_x, self.y), size=(river_width, self.height))
            Color(0.3, 0.5, 0.9, 0.7)  # Medium blue overlay
            Rectangle(pos=(river_x + 10, self.y + 10), size=(river_width - 20, self.height - 20))

            # River waves effect
            Color(1, 1, 1, 0.3)  # White waves
            for i in range(5):
                y_pos = self.y + (self.height / 5) * i + 30
                Line(points=[river_x + 20, y_pos, river_x + river_width - 20, y_pos + 10], width=2)

            # Left side (starting)
            Color(0.4, 0.8, 0.4, 1)  # Green
            Rectangle(pos=(self.x, self.y), size=(river_x - self.x, self.height))

            # Right side (target)
            Color(0.5, 0.9, 0.5, 1)  # Lighter green
            Rectangle(pos=(river_x + river_width, self.y),
                      size=(self.right - river_x - river_width, self.height))

            # Boat
            farmer, lion, goat, grass = self.game_state
            boat_x = river_x + 30 if not farmer else river_x + river_width - 80
            boat_y = self.center_y - 25

            Color(0.6, 0.4, 0.2, 1)  # Brown boat
            Ellipse(pos=(boat_x, boat_y), size=(50, 25))
            Color(0.3, 0.2, 0.1, 1)  # Dark outline
            Line(ellipse=(boat_x, boat_y, 50, 25), width=2)

        self.draw_characters()

    def draw_characters(self):
        farmer, lion, goat, grass = self.game_state

        # Character data: (emoji, color, state)
        characters = [
            ("👨‍🌾", "Farmer", farmer),
            ("🦁", "Lion", lion),
            ("🐐", "Goat", goat),
            ("🌾", "Grass", grass)
        ]

        river_width = self.width * 0.25
        river_x = self.center_x - river_width / 2

        # Position counters
        left_count = 0
        right_count = 0

        with self.canvas:
            for i, (emoji, name, side) in enumerate(characters):
                if side:  # Right side
                    x = river_x + river_width + 50 + (right_count % 2) * 100
                    y = self.y + 100 + (right_count // 2) * 120
                    right_count += 1
                else:  # Left side
                    x = self.x + 50 + (left_count % 2) * 100
                    y = self.y + 100 + (left_count // 2) * 120
                    left_count += 1

                # Character circle background
                if side:
                    Color(0.3, 0.7, 0.3, 0.8)  # Green for target side
                else:
                    Color(0.7, 0.7, 0.3, 0.8)  # Yellow for starting side

                Ellipse(pos=(x - 30, y - 30), size=(60, 60))

                # Store position for character rendering
                self.character_positions[name] = (x, y, emoji)


class RiverCrossingApp(App):
    def build(self):
        self.title = "River Crossing Puzzle - Premium Edition"

        # Game logic
        self.current_state = (False, False, False, False)
        self.start_state = (False, False, False, False)
        self.goal_state = (True, True, True, True)
        self.solution_path = []
        self.current_step = 0
        self.solving = False

        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # Title
        title = Label(text='🌊 River Crossing Puzzle 🌊',
                      font_size='24sp',
                      size_hint_y=0.1,
                      color=[0.2, 0.2, 0.6, 1])
        main_layout.add_widget(title)

        # Instructions
        instructions = Label(
            text='Help the farmer transport everyone across safely!\n' +
                 '🚫 Lion cannot be alone with goat\n' +
                 '🚫 Goat cannot be alone with grass',
            font_size='14sp',
            size_hint_y=0.15,
            text_size=(None, None),
            halign='center',
            color=[0.3, 0.3, 0.3, 1]
        )
        main_layout.add_widget(instructions)

        # Game canvas
        self.canvas_widget = GameCanvas(size_hint_y=0.6)
        main_layout.add_widget(self.canvas_widget)

        # Control buttons
        button_layout = GridLayout(cols=2, rows=2, spacing=10, size_hint_y=0.2)

        # Styled buttons
        self.find_btn = Button(text='🔍 Find Solution',
                               background_color=[0.2, 0.6, 0.8, 1],
                               font_size='16sp')
        self.find_btn.bind(on_press=self.find_solution)

        self.auto_btn = Button(text='▶️ Auto Solve',
                               background_color=[0.2, 0.8, 0.2, 1],
                               font_size='16sp')
        self.auto_btn.bind(on_press=self.auto_solve)

        self.step_btn = Button(text='⏭️ Next Step',
                               background_color=[0.6, 0.2, 0.8, 1],
                               font_size='16sp')
        self.step_btn.bind(on_press=self.next_step)

        self.reset_btn = Button(text='🔄 Reset',
                                background_color=[0.8, 0.4, 0.2, 1],
                                font_size='16sp')
        self.reset_btn.bind(on_press=self.reset_game)

        button_layout.add_widget(self.find_btn)
        button_layout.add_widget(self.auto_btn)
        button_layout.add_widget(self.step_btn)
        button_layout.add_widget(self.reset_btn)

        main_layout.add_widget(button_layout)

        # Status label
        self.status_label = Label(text='🎮 Click "Find Solution" to start!',
                                  font_size='16sp',
                                  size_hint_y=0.1,
                                  color=[0.2, 0.4, 0.2, 1])
        main_layout.add_widget(self.status_label)

        # Initial render
        Clock.schedule_once(lambda dt: self.update_display(), 0.1)

        return main_layout

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

    def find_solution(self, instance):
        self.solution_path = self.bfs_solve()
        if self.solution_path:
            self.current_step = 0
            self.status_label.text = f'✅ Solution found! {len(self.solution_path)} steps total'
            self.current_state = self.solution_path[0]
            self.update_display()
        else:
            self.show_popup("No Solution", "No solution found for this puzzle!")

    def auto_solve(self, instance):
        if not self.solution_path:
            self.find_solution(instance)
            return

        if self.solving:
            return

        self.solving = True
        self.auto_btn.text = "⏸️ Solving..."
        self.auto_btn.disabled = True

        # Animate through solution
        self.animate_solution()

    def animate_solution(self):
        if self.current_step < len(self.solution_path) - 1:
            self.current_step += 1
            self.current_state = self.solution_path[self.current_step]
            self.update_display()
            self.status_label.text = f'🎬 Step {self.current_step + 1} of {len(self.solution_path)}'

            # Schedule next step
            Clock.schedule_once(lambda dt: self.animate_solution(), 1.5)
        else:
            # Finished
            self.solving = False
            self.auto_btn.text = "▶️ Auto Solve"
            self.auto_btn.disabled = False
            self.status_label.text = '🎉 Puzzle Solved! Everyone safely across! 🎉'
            self.show_popup("🎉 Congratulations! 🎉", "You've successfully solved the river crossing puzzle!")

    def next_step(self, instance):
        if not self.solution_path:
            self.status_label.text = '⚠️ Please find solution first!'
            return

        if self.current_step < len(self.solution_path) - 1:
            self.current_step += 1
            self.current_state = self.solution_path[self.current_step]
            self.update_display()

            if self.current_step == len(self.solution_path) - 1:
                self.status_label.text = '🎉 Puzzle Solved! Everyone safely across! 🎉'
                self.show_popup("🎉 Congratulations! 🎉", "You've successfully solved the puzzle!")
            else:
                self.status_label.text = f'📍 Step {self.current_step + 1} of {len(self.solution_path)}'
        else:
            self.status_label.text = '✅ Puzzle already completed!'

    def reset_game(self, instance):
        self.current_state = self.start_state
        self.solution_path = []
        self.current_step = 0
        self.solving = False
        self.auto_btn.text = "▶️ Auto Solve"
        self.auto_btn.disabled = False
        self.status_label.text = '🔄 Game reset! Ready to solve!'
        self.update_display()

    def update_display(self):
        self.canvas_widget.game_state = self.current_state
        self.canvas_widget.update_graphics()

        # Add validation warning
        if not self.is_valid(self.current_state):
            self.status_label.text = '⚠️ INVALID STATE! Someone will be eaten! ⚠️'
            self.status_label.color = [1, 0.2, 0.2, 1]  # Red
        else:
            self.status_label.color = [0.2, 0.4, 0.2, 1]  # Green

    def show_popup(self, title, content):
        popup_content = BoxLayout(orientation='vertical', padding=20, spacing=10)
        popup_content.add_widget(Label(text=content, font_size='16sp'))

        close_btn = Button(text='Close', size_hint_y=0.3, font_size='14sp')
        popup_content.add_widget(close_btn)

        popup = Popup(title=title, content=popup_content, size_hint=(0.8, 0.6))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()


# Character rendering widget
class CharacterWidget(Label):
    def __init__(self, emoji, name, **kwargs):
        super().__init__(**kwargs)
        self.text = emoji
        self.font_size = '32sp'
        self.size_hint = (None, None)
        self.size = (60, 60)


if __name__ == '__main__':
    RiverCrossingApp().run()