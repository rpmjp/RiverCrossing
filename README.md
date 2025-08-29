#  River Crossing Puzzle

A modern implementation of the classic river crossing logic puzzle with beautiful PyQt5 GUI and intelligent BFS solver.

##  Game Description

Help the farmer safely transport a lion, goat, and grass across the river! This classic logic puzzle challenges you to find the optimal sequence of moves while following strict safety rules.

**The Challenge:**
-  The farmer must transport everyone across the river
-  Only the farmer can operate the boat
-  The boat can only carry the farmer plus ONE item at a time
-  **Critical Rule:** Lion cannot be alone with goat (lion will eat goat)
-  **Critical Rule:** Goat cannot be alone with grass (goat will eat grass)

##  Screenshots

![Game Interface](https://github.com/user-attachments/assets/83c6b103-bfdb-4fb9-8e95-7becda0f4895)
*Main game interface with modern PyQt5 styling*

![Solution in Progress](https://github.com/user-attachments/assets/310eced4-94cf-4192-85c6-06974ec251a8)
*Automatic solver showing step-by-step solution*

##  Installation & Setup

### Prerequisites
- Python 3.7 or higher
- PyQt5

### Quick Start
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/river-crossing-puzzle.git
   cd river-crossing-puzzle
   ```

2. **Install dependencies:**
   ```bash
   pip install PyQt5
   ```
   
   *Or using requirements.txt:*
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game:**
   ```bash
   python River_Crossing_PyQt5_GUI.py
   ```

##  Features

###  Intelligent Solver
- **BFS Algorithm**: Uses Breadth-First Search to find the optimal solution
- **Guaranteed Optimal**: Always finds the shortest path (8 steps)
- **State Validation**: Prevents invalid moves that violate safety rules

###  Modern GUI
- **Professional Design**: Beautiful PyQt5 interface with gradients and effects
- **Visual Feedback**: Color-coded sides and character positioning
- **Smooth Animations**: Automated solving with step-by-step visualization
- **Responsive Layout**: Scales beautifully to different window sizes

###  Interactive Controls
- ** Find Solution**: Discover the optimal path using BFS
- ** Auto Solve**: Watch the solution unfold automatically
- ** Next Step**: Manually step through the solution
- ** Reset**: Start over at any time

###  Safety Features
- **Invalid State Detection**: Visual warnings when rules are violated
- **Move Validation**: Only allows legal moves
- **Error Handling**: Graceful handling of edge cases

##  Algorithm Details

The puzzle solver uses **Breadth-First Search (BFS)** to guarantee finding the shortest solution:

1. **State Representation**: Each state is a 4-tuple `(farmer, lion, goat, grass)` where `False` = left side, `True` = right side
2. **Move Generation**: From each state, generate all valid moves (farmer alone or with one item)
3. **Validation**: Ensure no invalid states (predator-prey combinations without farmer)
4. **Optimal Path**: BFS explores all possibilities level by level, ensuring the first solution found is optimal

**Time Complexity**: O(2^4) = O(16) states maximum  
**Space Complexity**: O(16) for visited states tracking  
**Solution Length**: 8 steps (optimal)

##  Project Structure

```
river-crossing-puzzle/
├── River_Crossing_PyQt5_GUI.py    # Main PyQt5 implementation
├── river_crossing_puzzle.py       # Original tkinter version
├── River_Crossing_AI_KivyGui.py   # Kivy implementation
├── requirements.txt               # Python dependencies
├── README.md                      # This file
├── .gitignore                     # Git ignore rules
└── screenshots/                   # Game screenshots
    ├── screenshot1.png
    └── screenshot2.png
```

##  Technical Implementation

### Core Components
- **GameCanvas**: Custom PyQt5 widget with professional graphics rendering
- **BFS Solver**: Intelligent pathfinding algorithm
- **State Manager**: Handles game state transitions and validation
- **Animation System**: Smooth auto-solving with configurable timing

### Key Technologies
- **PyQt5**: Modern cross-platform GUI framework
- **Custom Graphics**: Hand-coded gradients, effects, and animations
- **Queue-based BFS**: Efficient optimal pathfinding
- **Event-driven Architecture**: Responsive user interface

##  Educational Value

This project demonstrates several computer science concepts:
- **Graph Theory**: State space representation and traversal
- **Search Algorithms**: BFS implementation and optimization
- **GUI Programming**: Modern desktop application development
- **State Management**: Complex state validation and transitions
- **Algorithm Visualization**: Making abstract concepts tangible

Perfect for:
- Computer Science students learning search algorithms
- Logic puzzle enthusiasts
- GUI programming examples
- Algorithm visualization projects

##  Contributing

Contributions are welcome! Here are some ideas:
-  **UI Improvements**: Enhanced graphics, animations, or themes
-  **Algorithm Extensions**: A* search, different heuristics, or solver comparisons
-  **Game Features**: Difficulty levels, hints system, or puzzle variations
-  **Platform Support**: Mobile versions or web implementation
-  **Audio**: Sound effects and background music

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

##  Acknowledgments

- Classic river crossing puzzle concept
- PyQt5 community for excellent documentation
- Algorithm design inspired by AI search techniques

##  Contact

Created by [Your Name] - feel free to contact me!

- GitHub: [@rpmjp](https://github.com/rpmjp)
- Website: [robertjeanpierre.com](https://robertjeanpierre.com/)
  
---

⭐ **Star this repo if you found it helpful!** ⭐
