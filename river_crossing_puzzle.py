import tkinter as tk
from tkinter import messagebox
import queue
import time


class RiverCrossingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("River Crossing Puzzle")
        self.root.geometry("800x600")
        self.root.configure(bg='lightblue')

        # Game state - (farmer, lion, goat, grass) - False=left, True=right
        self.current_state = (False, False, False, False)
        self.start_state = (False, False, False, False)
        self.goal_state = (True, True, True, True)
        self.solution_path = []
        self.current_step = 0
        self.auto_solving = False

        self.setup_ui()
        self.update_display()

    def setup_ui(self):
        # Title
        title = tk.Label(self.root, text="River Crossing Puzzle",
                         font=("Arial", 20, "bold"), bg='lightblue')
        title.pack(pady=10)

        # Instructions
        instructions = tk.Label(self.root,
                                text="Help the farmer transport the lion, goat, and grass across the river!\n" +
                                     "Rules: Lion can't be alone with goat, goat can't be alone with grass",
                                font=("Arial", 10), bg='lightblue', wraplength=600)
        instructions.pack(pady=5)

        # Main game canvas
        self.canvas = tk.Canvas(self.root, width=700, height=400, bg='lightgreen')
        self.canvas.pack(pady=20)

        # Control buttons frame
        controls = tk.Frame(self.root, bg='lightblue')
        controls.pack(pady=10)

        tk.Button(controls, text="Auto Solve", command=self.auto_solve,
                  font=("Arial", 12), bg='green', fg='white').pack(side=tk.LEFT, padx=5)

        tk.Button(controls, text="Next Step", command=self.next_step,
                  font=("Arial", 12), bg='blue', fg='white').pack(side=tk.LEFT, padx=5)

        tk.Button(controls, text="Reset", command=self.reset_game,
                  font=("Arial", 12), bg='red', fg='white').pack(side=tk.LEFT, padx=5)

        tk.Button(controls, text="Manual Move", command=self.show_manual_options,
                  font=("Arial", 12), bg='orange', fg='white').pack(side=tk.LEFT, padx=5)

        # Status label
        self.status_label = tk.Label(self.root, text="Click 'Auto Solve' to see the solution!",
                                     font=("Arial", 12), bg='lightblue')
        self.status_label.pack(pady=5)

    def draw_scene(self):
        self.canvas.delete("all")

        # Draw river
        self.canvas.create_rectangle(250, 50, 450, 350, fill='blue', outline='darkblue', width=3)
        self.canvas.create_text(350, 200, text="RIVER", font=("Arial", 16, "bold"), fill='white')

        # Draw sides
        self.canvas.create_text(125, 30, text="Starting Side", font=("Arial", 14, "bold"))
        self.canvas.create_text(575, 30, text="Target Side", font=("Arial", 14, "bold"))

        # Draw boat
        farmer, lion, goat, grass = self.current_state
        boat_x = 300 if not farmer else 400
        self.canvas.create_oval(boat_x - 20, 180, boat_x + 20, 220, fill='brown', outline='black', width=2)

        # Draw characters based on current state
        self.draw_characters()

        # Highlight invalid states
        if not self.is_valid(self.current_state):
            self.canvas.create_text(350, 380, text="⚠️ INVALID STATE! ⚠️",
                                    font=("Arial", 14, "bold"), fill='red')

    def draw_characters(self):
        farmer, lion, goat, grass = self.current_state

        # Character positions
        left_positions = [(50, 100), (50, 150), (50, 200), (50, 250)]
        right_positions = [(650, 100), (650, 150), (650, 200), (650, 250)]

        characters = [
            ("👨‍🌾", "Farmer", farmer),
            ("🦁", "Lion", lion),
            ("🐐", "Goat", goat),
            ("🌾", "Grass", grass)
        ]

        left_idx = 0
        right_idx = 0

        for emoji, name, side in characters:
            if side:  # Right side
                x, y = right_positions[right_idx]
                right_idx += 1
            else:  # Left side
                x, y = left_positions[left_idx]
                left_idx += 1

            # Draw character
            self.canvas.create_text(x, y, text=emoji, font=("Arial", 30))
            self.canvas.create_text(x, y + 40, text=name, font=("Arial", 10))

    def is_valid(self, state):
        farmer, lion, goat, grass = state
        # Lion and goat alone together (farmer not with them)
        if lion == goat and farmer != goat:
            return False
        # Goat and grass alone together (farmer not with them)
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

    def auto_solve(self):
        self.solution_path = self.bfs_solve()
        if self.solution_path:
            self.current_step = 0
            self.auto_solving = True
            self.status_label.config(
                text=f"Solution found! {len(self.solution_path)} steps total. Click 'Next Step' to proceed.")
            self.current_state = self.solution_path[0]
            self.update_display()
        else:
            messagebox.showinfo("No Solution", "No solution found for this puzzle!")

    def next_step(self):
        if not self.solution_path:
            self.status_label.config(text="Please click 'Auto Solve' first!")
            return

        if self.current_step < len(self.solution_path) - 1:
            self.current_step += 1
            self.current_state = self.solution_path[self.current_step]
            self.update_display()

            if self.current_step == len(self.solution_path) - 1:
                self.status_label.config(text="🎉 Puzzle Solved! Everyone safely across! 🎉")
                messagebox.showinfo("Congratulations!", "You've successfully solved the river crossing puzzle!")
            else:
                self.status_label.config(text=f"Step {self.current_step + 1} of {len(self.solution_path)}")
        else:
            self.status_label.config(text="Puzzle already completed!")

    def show_manual_options(self):
        moves = self.generate_moves(self.current_state)
        if not moves:
            messagebox.showinfo("No Moves", "No valid moves available from current state!")
            return

        # Create a simple dialog for move selection
        move_window = tk.Toplevel(self.root)
        move_window.title("Select Move")
        move_window.geometry("300x200")

        tk.Label(move_window, text="Available Moves:", font=("Arial", 12, "bold")).pack(pady=10)

        for i, move in enumerate(moves):
            move_text = self.describe_move(self.current_state, move)
            tk.Button(move_window, text=move_text,
                      command=lambda m=move, w=move_window: self.make_manual_move(m, w),
                      font=("Arial", 10)).pack(pady=2, padx=20, fill=tk.X)

    def describe_move(self, current, new):
        farmer_current, lion_current, goat_current, grass_current = current
        farmer_new, lion_new, goat_new, grass_new = new

        if farmer_current != farmer_new:
            # Farmer is moving
            if goat_current != goat_new:
                return "Farmer takes Goat across"
            elif lion_current != lion_new:
                return "Farmer takes Lion across"
            elif grass_current != grass_new:
                return "Farmer takes Grass across"
            else:
                return "Farmer goes alone"
        return "Unknown move"

    def make_manual_move(self, new_state, window):
        self.current_state = new_state
        self.update_display()
        self.solution_path = []  # Clear auto-solve path
        self.current_step = 0

        if self.current_state == self.goal_state:
            self.status_label.config(text="🎉 Puzzle Solved Manually! Great job! 🎉")
            messagebox.showinfo("Congratulations!", "You've manually solved the puzzle!")
        else:
            self.status_label.config(text="Manual move made. Continue solving!")

        window.destroy()

    def reset_game(self):
        self.current_state = self.start_state
        self.solution_path = []
        self.current_step = 0
        self.auto_solving = False
        self.status_label.config(text="Game reset! Click 'Auto Solve' or try manual moves.")
        self.update_display()

    def update_display(self):
        self.draw_scene()


def main():
    root = tk.Tk()
    game = RiverCrossingGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()