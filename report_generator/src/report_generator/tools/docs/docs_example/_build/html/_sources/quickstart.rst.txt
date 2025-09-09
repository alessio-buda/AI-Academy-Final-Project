Quick Start Guide
=================

This guide will get you up and running with the Game Builder Crew in just a few minutes.

Prerequisites
------------

Before starting, make sure you have:

- ✅ Python 3.8+ installed
- ✅ Game Builder Crew installed (see :doc:`installation`)
- ✅ OpenAI API key configured
- ✅ Basic understanding of Python

5-Minute Quick Start
-------------------

1. **Navigate to Project Directory**

   .. code-block:: bash

      cd game-builder-crew

2. **Run Your First Game Creation**

   .. code-block:: bash

      poetry run game_builder_crew

   This will automatically:
   - Load the Snake game example
   - Initialize the three AI agents
   - Create, review, and finalize the game code
   - Display the complete Python game

3. **View the Output**

   The system will output something like:

   .. code-block:: text

      ## Welcome to the Game Crew
      -------------------------------
      [Agent execution logs...]
      
      ########################
      ## Here is the result
      ########################
      
      final code for the game:
      [Complete Python Snake game code]

4. **Save and Run the Game**

   Copy the generated code to a file and run it:

   .. code-block:: bash

      # Save the output to a file
      python generated_game.py

Basic Usage Patterns
--------------------

Method 1: Command Line (Simplest)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Run with default Snake game example
   poetry run game_builder_crew

Method 2: Python Script (Customizable)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from game_builder_crew.crew import GameBuilderCrew

   # Initialize the crew
   crew = GameBuilderCrew()

   # Define your game requirements
   game_description = """
   Create a simple Pong game with:
   - Two paddles controlled by keyboard
   - Ball physics with collision detection
   - Score tracking for both players
   - Game over conditions
   """

   # Generate the game
   inputs = {'game': game_description}
   result = crew.crew().kickoff(inputs=inputs)
   
   print("Generated Game Code:")
   print(result)

Method 3: Using Predefined Examples
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import yaml
   from game_builder_crew.crew import GameBuilderCrew

   # Load predefined examples
   with open('src/game_builder_crew/config/gamedesign.yaml', 'r') as file:
       examples = yaml.safe_load(file)

   # Choose an example
   crew = GameBuilderCrew()
   inputs = {'game': examples['example1_pacman']}  # or example2_pacman, example3_snake
   
   result = crew.crew().kickoff(inputs=inputs)

Understanding the Output
-----------------------

The Game Builder Crew produces complete, executable Python game code that includes:

**Essential Components:**
- All necessary imports
- Game class or function definitions
- Main game loop
- Event handling for user input
- Graphics rendering (using pygame or similar)
- Game logic and physics

**Code Quality Features:**
- Proper error handling
- Inline comments explaining key functions
- Clean, readable code structure
- Cross-platform compatibility

**Example Output Structure:**

.. code-block:: python

   import pygame
   import random
   import sys

   # Game constants
   WINDOW_WIDTH = 800
   WINDOW_HEIGHT = 600
   
   class SnakeGame:
       def __init__(self):
           # Initialization code
           
       def handle_events(self):
           # Input handling
           
       def update(self):
           # Game logic
           
       def draw(self):
           # Rendering
           
       def run(self):
           # Main game loop
           
   if __name__ == "__main__":
       game = SnakeGame()
       game.run()

Customizing Game Generation
---------------------------

Writing Effective Game Descriptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For best results, include these elements in your game descriptions:

**1. Core Mechanics**

.. code-block:: text

   Game Type: [Puzzle/Action/Strategy/etc.]
   Player Controls: [Keyboard/Mouse controls]
   Win Condition: [How to win]
   Lose Condition: [How to lose]

**2. Technical Requirements**

.. code-block:: text

   Graphics: [Simple shapes/Sprites/ASCII]
   Dependencies: [Pygame/Tkinter/Console-only]
   Performance: [Target FPS, optimization needs]

**3. Gameplay Features**

.. code-block:: text

   Scoring System: [How points are earned]
   Difficulty: [Static/Progressive]
   Special Features: [Power-ups, levels, etc.]

**Example: Detailed Game Description**

.. code-block:: text

   Create a Tetris-like puzzle game with the following specifications:
   
   Core Mechanics:
   - Falling tetromino pieces (7 standard shapes)
   - Player can rotate and move pieces left/right
   - Completed horizontal lines disappear
   - Game speeds up as score increases
   
   Controls:
   - Arrow keys for movement (left, right, down)
   - Up arrow or spacebar for rotation
   - Escape key to pause/quit
   
   Technical Requirements:
   - Use Pygame for graphics
   - 10x20 game grid
   - Smooth piece movement and rotation
   - Score display and level indicator
   
   Game Features:
   - Line clearing animation
   - Next piece preview
   - High score tracking
   - Game over screen with restart option

Working with Different Game Types
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Arcade Games (Snake, Pac-Man, Pong)**
   - Focus on collision detection
   - Emphasize smooth movement
   - Include scoring systems

**Puzzle Games (Tetris, Match-3)**
   - Describe grid mechanics
   - Explain matching/clearing rules
   - Detail win/lose conditions

**Strategy Games (Chess, Checkers)**
   - Define piece movement rules
   - Explain turn-based mechanics
   - Include AI opponent if needed

Common Workflows
---------------

Development Workflow
~~~~~~~~~~~~~~~~~~~

1. **Concept Phase**
   - Write detailed game description
   - Define core mechanics and features

2. **Generation Phase**
   - Run Game Builder Crew
   - Review generated code quality

3. **Testing Phase**
   - Test the generated game
   - Note any issues or improvements needed

4. **Iteration Phase**
   - Refine game description based on results
   - Re-run crew with improved specifications

Training Workflow
~~~~~~~~~~~~~~~~

For improving the crew's performance:

.. code-block:: bash

   # Train the crew with multiple iterations
   poetry run python -c "
   from game_builder_crew.main import train
   train(n_iterations=10, filename='improved_model.pkl')
   "

This trains the crew using the Pac-Man example and saves an improved model.

Troubleshooting Quick Issues
---------------------------

**Issue: Code doesn't run**
   - Check for missing dependencies in the generated code
   - Verify Python syntax is correct
   - Ensure all imports are available

**Issue: Game mechanics don't work as expected**
   - Review your game description for clarity
   - Add more specific technical requirements
   - Include edge cases in your specifications

**Issue: Performance problems**
   - Specify performance requirements in description
   - Mention optimization needs
   - Request specific frame rate targets

**Issue: Missing features**
   - Be more explicit about required features
   - Include examples of expected behavior
   - Add acceptance criteria to your description

Next Steps
---------

Now that you've successfully generated your first game:

1. **Explore Examples**: Try the different predefined game examples
2. **Customize Games**: Experiment with your own game descriptions  
3. **Learn the Architecture**: Read about the :doc:`development/architecture`
4. **Extend the System**: Learn how to add new agents in :doc:`development/extending`
5. **Join the Community**: Participate in discussions and share your results

.. tip::
   **Pro Tip**: Start with simple games and gradually increase complexity. The AI agents learn better with clear, specific requirements.

.. note::
   **Remember**: The quality of the generated game depends heavily on the clarity and detail of your game description. Take time to write comprehensive specifications for best results.

For more advanced usage patterns, see the full :doc:`usage` guide.
