Game Examples
=============

This section showcases various game creation examples using the Game Builder Crew system. Each example demonstrates different aspects of the system's capabilities and provides insights into effective game specification writing.

Overview
--------

The Game Builder Crew comes with three predefined game examples that serve different purposes:

.. list-table::
   :header-rows: 1
   :widths: 20 30 25 25

   * - Example
     - Game Type
     - Complexity
     - Use Case
   * - Snake Game
     - Arcade/Classic
     - Medium
     - Production runs
   * - Pac-Man (Detailed)
     - Arcade/Maze
     - High
     - Training/Learning
   * - Pac-Man (Simple)
     - Arcade/Simplified
     - Low
     - Quick prototyping

Predefined Examples
------------------

Snake Game (example3_snake)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Used by default in production runs**

This example creates a classic Snake game with comprehensive mechanics:

**Game Features:**
- Grid-based movement system
- Arrow key controls (Up, Down, Left, Right)
- Food consumption with snake growth
- Collision detection (walls and self)
- Score tracking
- Game over conditions

**Technical Specifications:**

.. code-block:: text

   Objective:
   Control a snake that moves across a game area, consuming food while 
   avoiding obstacles including its own tail.

   Game Mechanics:
   - Rectangular grid (2D matrix/array)
   - Discrete movement (one cell per frame)
   - Continuous directional movement
   - Growth mechanism (one segment per food)
   - Random food spawning
   - Wall and self-collision detection

   Controls:
   - Arrow keys or WASD for direction
   - Cannot reverse direction immediately
   - Continuous movement until direction change

   Scoring:
   - 10 points per food item consumed
   - Optional: Speed-based bonus scoring
   - High score tracking

**Generated Code Features:**

.. code-block:: python

   import pygame
   import random
   import sys

   class SnakeGame:
       def __init__(self):
           # Game initialization
           self.grid_width = 20
           self.grid_height = 15
           self.cell_size = 30
           
       def handle_input(self):
           # Arrow key handling
           
       def update_snake(self):
           # Movement and growth logic
           
       def check_collisions(self):
           # Wall and self collision detection
           
       def spawn_food(self):
           # Random food placement
           
       def draw_game(self):
           # Rendering system

**Usage Example:**

.. code-block:: python

   import yaml
   from game_builder_crew.crew import GameBuilderCrew

   # Load Snake example
   with open('src/game_builder_crew/config/gamedesign.yaml', 'r') as f:
       examples = yaml.safe_load(f)

   crew = GameBuilderCrew()
   inputs = {'game': examples['example3_snake']}
   snake_game = crew.crew().kickoff(inputs=inputs)

   # Save and run
   with open('snake_game.py', 'w') as f:
       f.write(snake_game)

Pac-Man Detailed (example1_pacman)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Used for training the crew**

This is the most comprehensive example, featuring full Pac-Man game mechanics:

**Game Features:**
- Grid-based maze navigation
- Four distinct ghost AI personalities
- Power pellet mechanics
- Multiple game modes (Chase, Scatter, Frightened)
- Scoring system with bonuses
- Level progression
- Lives system
- Warp tunnels

**Technical Specifications:**

.. code-block:: text

   Core Elements:
   - Maze layout with walls and corridors
   - Pellets (10 points) and Power Pellets (50 points)
   - Four ghosts with unique behaviors:
     * Blinky (Red): Aggressive pursuit
     * Pinky (Pink): Ambush strategy (4 tiles ahead)
     * Inky (Cyan): Complex targeting (between Pac-Man and Blinky)
     * Clyde (Orange): Alternating chase/wander

   Game States:
   - Chase Mode: Normal ghost pursuit
   - Scatter Mode: Ghosts retreat to corners
   - Frightened Mode: Ghosts turn blue and flee

   Advanced Features:
   - Pathfinding algorithms for ghost AI
   - State management system
   - Timer-based mode switching
   - Bonus scoring for consecutive ghost consumption

**Ghost AI Implementation:**

.. code-block:: python

   class Ghost:
       def __init__(self, color, behavior_type):
           self.color = color
           self.behavior = behavior_type
           self.mode = 'chase'
           
       def update_target(self, pacman_pos, blinky_pos=None):
           if self.behavior == 'aggressive':
               return pacman_pos
           elif self.behavior == 'ambush':
               return self.calculate_ambush_point(pacman_pos)
           elif self.behavior == 'complex':
               return self.calculate_complex_target(pacman_pos, blinky_pos)
           elif self.behavior == 'patrol':
               return self.patrol_behavior(pacman_pos)

**Usage for Training:**

.. code-block:: python

   from game_builder_crew.main import train

   # Train using complex Pac-Man example
   train(n_iterations=10, filename='pacman_trained_model.pkl')

Pac-Man Simple (example2_pacman)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Used for quick prototyping**

A simplified version of Pac-Man for rapid development:

**Simplified Features:**
- Basic movement (arrow keys)
- Food dots with point scoring
- Random ghost spawning and movement
- Simple collision detection
- Three lives system
- Level progression with increased difficulty

**Specification:**

.. code-block:: text

   Game Description:
   Build a Pacman game where the pacman moves up, down, left, right 
   with arrow keys. Each food dot eaten gives a point. Ghosts appear 
   at random times and move randomly. If they hit pacman, it loses a 
   life (3 lives total). When all food is eaten, advance to next level 
   with faster pacman and more ghosts.

**Generated Code Structure:**

.. code-block:: python

   class SimplePacman:
       def __init__(self):
           self.score = 0
           self.lives = 3
           self.level = 1
           self.speed = 5
           
       def move_pacman(self, direction):
           # Simple movement logic
           
       def spawn_ghost(self):
           # Random ghost creation
           
       def check_food_collision(self):
           # Food consumption
           
       def next_level(self):
           # Level progression

**Usage Example:**

.. code-block:: python

   # Quick prototype generation
   import yaml
   from game_builder_crew.crew import GameBuilderCrew

   with open('src/game_builder_crew/config/gamedesign.yaml', 'r') as f:
       examples = yaml.safe_load(f)

   crew = GameBuilderCrew()
   inputs = {'game': examples['example2_pacman']}
   simple_game = crew.crew().kickoff(inputs=inputs)

Custom Game Examples
-------------------

Creating Your Own Game Specifications
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here are examples of custom game descriptions that work well with the system:

**Tetris Game:**

.. code-block:: text

   Create a Tetris puzzle game with these specifications:

   Core Mechanics:
   - Seven standard tetromino pieces (I, O, T, S, Z, J, L)
   - Pieces fall from top at regular intervals
   - Player can move pieces left/right and rotate them
   - Pieces lock when they hit bottom or other pieces
   - Complete horizontal lines are cleared and award points
   - Game speed increases every 10 lines cleared

   Controls:
   - Left/Right arrows: Move piece horizontally
   - Up arrow: Rotate piece clockwise
   - Down arrow: Soft drop (faster fall)
   - Space: Hard drop (instant fall)
   - Escape: Pause/quit game

   Technical Requirements:
   - Use Pygame for graphics
   - 10x20 grid playing field
   - Smooth piece movement and rotation
   - Line clearing animation
   - Score and level display

   Scoring System:
   - Single line: 100 points × level
   - Double line: 300 points × level  
   - Triple line: 500 points × level
   - Tetris (4 lines): 800 points × level

**Pong Game:**

.. code-block:: text

   Create a classic Pong game with these features:

   Gameplay:
   - Two paddles (left and right sides of screen)
   - Ball bounces between paddles
   - Players score when ball passes opponent's paddle
   - First to 11 points wins

   Controls:
   - Player 1: W/S keys for up/down
   - Player 2: Up/Down arrow keys
   - Spacebar: Start game/serve ball
   - R key: Restart game

   Physics:
   - Ball bounces off top/bottom walls
   - Ball speed increases slightly after each paddle hit
   - Paddle collision affects ball angle based on hit location
   - Ball resets to center after each score

   Technical:
   - Use Pygame for graphics
   - 800x600 pixel window
   - 60 FPS target
   - Sound effects for paddle hits and scoring

**Breakout Game:**

.. code-block:: text

   Create a Breakout/Arkanoid style game:

   Core Elements:
   - Player-controlled paddle at bottom
   - Ball bounces off paddle and walls
   - Grid of destructible blocks at top
   - Player must destroy all blocks to win

   Game Mechanics:
   - Ball destroys blocks on contact
   - Different block types worth different points
   - Power-ups occasionally drop from destroyed blocks
   - Multiple lives (ball can be lost off bottom)

   Power-ups:
   - Larger paddle
   - Multi-ball
   - Laser paddle (shoot blocks)
   - Catch ball (sticky paddle)

   Controls:
   - Mouse movement: Control paddle
   - Mouse click: Launch ball/activate power-ups
   - Spacebar: Pause game

Advanced Example Patterns
-------------------------

Multi-Level Games
~~~~~~~~~~~~~~~~

For games with level progression:

.. code-block:: text

   Level System Requirements:
   - Define clear progression criteria
   - Specify how difficulty increases
   - Include level transition mechanics
   - Consider save/load functionality

   Example Level Progression:
   Level 1: Basic mechanics introduction
   Level 2: Increased speed/complexity
   Level 3: New obstacles or enemies
   Level 4+: Combined challenges

AI Opponent Games
~~~~~~~~~~~~~~~~

For games requiring AI opponents:

.. code-block:: text

   AI Behavior Specifications:
   - Define difficulty levels (Easy/Medium/Hard)
   - Specify decision-making algorithms
   - Include reaction times and limitations
   - Balance competitiveness with fun

   Example AI Levels:
   Easy: Predictable patterns, slower reactions
   Medium: Semi-random decisions, human-like timing
   Hard: Optimal play with occasional mistakes

Multiplayer Games
~~~~~~~~~~~~~~~~

For local multiplayer games:

.. code-block:: text

   Multiplayer Requirements:
   - Separate control schemes for each player
   - Turn-based or real-time mechanics
   - Score tracking per player
   - Win condition handling

   Control Scheme Example:
   Player 1: WASD keys + Space
   Player 2: Arrow keys + Enter
   Shared: Escape (pause), R (restart)

Best Practices for Game Specifications
-------------------------------------

Specification Writing Guidelines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**1. Be Specific and Detailed**

.. code-block:: text

   ❌ Bad: "Create a simple platformer game"
   ✅ Good: "Create a 2D side-scrolling platformer with jump mechanics, 
            moving platforms, and collectible coins"

**2. Include Technical Constraints**

.. code-block:: text

   Technical Requirements:
   - Graphics library: Pygame
   - Window size: 800x600 pixels
   - Target framerate: 60 FPS
   - Platform compatibility: Windows/macOS/Linux

**3. Define Clear Win/Lose Conditions**

.. code-block:: text

   Win Conditions:
   - Collect all coins in the level
   - Reach the exit door
   - Complete within time limit

   Lose Conditions:
   - Fall off the bottom of the screen
   - Touch enemy sprites
   - Run out of time

**4. Specify Control Schemes**

.. code-block:: text

   Controls:
   - Arrow keys: Movement (left/right)
   - Spacebar: Jump
   - Shift: Run (increased movement speed)
   - Escape: Pause menu

**5. Include Scoring and Progression**

.. code-block:: text

   Scoring System:
   - Coins: 100 points each
   - Time bonus: Remaining seconds × 10
   - Perfect run: 1000 point bonus

Testing Your Examples
~~~~~~~~~~~~~~~~~~~~~

**1. Validation Process**

.. code-block:: python

   def test_game_specification(game_spec):
       """Test a game specification for completeness."""
       
       required_elements = [
           'objective', 'controls', 'mechanics', 
           'win_condition', 'lose_condition'
       ]
       
       missing_elements = []
       for element in required_elements:
           if element.lower() not in game_spec.lower():
               missing_elements.append(element)
       
       if missing_elements:
           print(f"Missing elements: {missing_elements}")
           return False
       
       return True

**2. Iterative Refinement**

.. code-block:: python

   def refine_game_specification(initial_spec):
       """Iteratively improve game specification."""
       
       # Generate initial game
       crew = GameBuilderCrew()
       result1 = crew.crew().kickoff(inputs={'game': initial_spec})
       
       # Analyze result and identify issues
       issues = analyze_generated_code(result1)
       
       # Refine specification based on issues
       refined_spec = add_clarifications(initial_spec, issues)
       
       # Generate improved version
       result2 = crew.crew().kickoff(inputs={'game': refined_spec})
       
       return result2, refined_spec

See Also
--------

- :doc:`usage`: Comprehensive usage guide
- :doc:`quickstart`: Getting started quickly
- :doc:`api/crew`: Core API reference
- :doc:`development/extending`: Adding new examples
