Usage Guide
===========

This comprehensive guide covers all aspects of using the Game Builder Crew system effectively.

Overview
--------

The Game Builder Crew operates through a sequential workflow of specialized AI agents:

.. mermaid::

   flowchart TD
       A[Game Description Input] --> B[Senior Engineer Agent]
       B --> C[Initial Code Creation]
       C --> D[QA Engineer Agent]
       D --> E[Code Review & Bug Fixes]
       E --> F[Chief QA Engineer Agent]
       F --> G[Final Quality Assurance]
       G --> H[Complete Game Output]

Core Components
--------------

Understanding the System Architecture
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Agents:**
   - **Senior Engineer Agent**: Creates initial game code
   - **QA Engineer Agent**: Reviews and fixes code issues
   - **Chief QA Engineer Agent**: Ensures final quality and completeness

**Configuration Files:**
   - ``agents.yaml``: Agent personalities and capabilities
   - ``tasks.yaml``: Task definitions and requirements
   - ``gamedesign.yaml``: Pre-built game examples

**Input/Output:**
   - **Input**: Detailed game specifications
   - **Output**: Complete, executable Python game code

Basic Usage Patterns
--------------------

Pattern 1: Direct Execution
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The simplest way to use the system:

.. code-block:: python

   from game_builder_crew.crew import GameBuilderCrew

   # Initialize crew
   crew = GameBuilderCrew()

   # Define game
   game_spec = """
   Create a simple Snake game where:
   - Player controls snake with arrow keys
   - Snake grows when eating food
   - Game ends on collision with walls or self
   - Display current score
   """

   # Generate game
   inputs = {'game': game_spec}
   result = crew.crew().kickoff(inputs=inputs)
   
   # Save result
   with open('generated_snake_game.py', 'w') as f:
       f.write(result)

Pattern 2: Using Predefined Examples
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Leverage the built-in game examples:

.. code-block:: python

   import yaml
   from game_builder_crew.crew import GameBuilderCrew

   # Load examples
   with open('src/game_builder_crew/config/gamedesign.yaml', 'r') as file:
       examples = yaml.safe_load(file)

   # Available examples:
   # - example1_pacman: Detailed Pac-Man with ghost AI
   # - example2_pacman: Simplified Pac-Man variant  
   # - example3_snake: Comprehensive Snake game

   crew = GameBuilderCrew()
   inputs = {'game': examples['example1_pacman']}
   result = crew.crew().kickoff(inputs=inputs)

Pattern 3: Batch Processing
~~~~~~~~~~~~~~~~~~~~~~~~~~

Generate multiple games efficiently:

.. code-block:: python

   from game_builder_crew.crew import GameBuilderCrew
   import json

   games_to_create = [
       {
           'name': 'pong',
           'description': 'Classic Pong game with two paddles and ball physics'
       },
       {
           'name': 'breakout', 
           'description': 'Breakout game with paddle, ball, and destructible blocks'
       },
       {
           'name': 'space_invaders',
           'description': 'Space Invaders with shooting mechanics and enemy waves'
       }
   ]

   crew = GameBuilderCrew()
   results = {}

   for game in games_to_create:
       print(f"Generating {game['name']}...")
       inputs = {'game': game['description']}
       result = crew.crew().kickoff(inputs=inputs)
       
       # Save each game
       filename = f"generated_{game['name']}.py"
       with open(filename, 'w') as f:
           f.write(result)
       
       results[game['name']] = filename

   print("Generated games:", results)

Advanced Usage
--------------

Custom Agent Configurations
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Modify agent behavior by editing configuration files:

.. code-block:: yaml

   # agents.yaml - Custom agent configuration
   senior_engineer_agent:
     role: >
       Expert Python Game Developer with focus on performance
     goal: >
       Create optimized, well-documented game code using best practices
     backstory: >
       You are a senior developer with 15+ years experience in game development.
       You specialize in creating efficient, maintainable code and always
       include comprehensive documentation and error handling.

Custom Task Definitions
~~~~~~~~~~~~~~~~~~~~~~

Modify the development process by editing tasks:

.. code-block:: yaml

   # tasks.yaml - Enhanced code task
   code_task:
     description: >
       Create a Python game based on these specifications:
       {game}
       
       Additional Requirements:
       - Include comprehensive docstrings for all functions
       - Add type hints for all function parameters and returns  
       - Implement proper error handling with try/catch blocks
       - Use object-oriented design principles
       - Include unit tests for core game functions
       - Optimize for 60 FPS performance
       
     expected_output: >
       Complete Python game code with documentation, type hints, error handling,
       and performance optimizations. Include a separate test file.

Environment Customization
~~~~~~~~~~~~~~~~~~~~~~~~~

Configure the system behavior through environment variables:

.. code-block:: bash

   # .env file
   OPENAI_API_KEY=your_key_here
   OPENAI_MODEL=gpt-4o                    # AI model to use
   CREW_VERBOSE=true                      # Enable detailed logging
   MAX_ITERATIONS=5                       # Maximum retry attempts
   TEMPERATURE=0.1                        # AI creativity level (0.0-1.0)
   MAX_TOKENS=4000                        # Maximum response length

Game Specification Best Practices
---------------------------------

Writing Effective Game Descriptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Structure Your Requirements:**

.. code-block:: text

   Game Title: [Clear, descriptive title]
   
   Game Type: [Genre/Category]
   
   Core Mechanics:
   - [Primary gameplay loop]
   - [Player actions and reactions]
   - [Win/lose conditions]
   
   Technical Requirements:
   - [Graphics library preferences]
   - [Performance targets]
   - [Platform compatibility]
   
   User Interface:
   - [Control scheme]
   - [Menu systems]
   - [Information display]
   
   Special Features:
   - [Unique gameplay elements]
   - [Advanced features]
   - [Easter eggs or bonuses]

**Example: Comprehensive Game Specification**

.. code-block:: text

   Game Title: Advanced Tetris Clone
   
   Game Type: Puzzle/Arcade
   
   Core Mechanics:
   - Seven standard tetromino pieces fall from top of screen
   - Player can move pieces left/right and rotate them
   - Pieces lock in place when they hit bottom or other pieces
   - Complete horizontal lines are cleared and award points
   - Game speed increases every 10 lines cleared
   - Game ends when pieces reach the top of the play area
   
   Technical Requirements:
   - Use Pygame for graphics and sound
   - Maintain 60 FPS performance
   - 10x20 grid play area
   - Smooth piece rotation and movement
   - Compatible with Windows, macOS, and Linux
   
   User Interface:
   - Arrow keys for piece movement (left, right, down for soft drop)
   - Up arrow or Space for rotation
   - Escape key to pause/quit
   - Display current score, level, and lines cleared
   - Show next piece preview
   - Game over screen with restart option
   
   Special Features:
   - Line clearing animation with visual effects
   - Progressive difficulty with speed increase
   - High score persistence between sessions
   - Sound effects for piece placement and line clearing
   - Optional: Hold piece functionality
   - Optional: Ghost piece preview showing drop location

Domain-Specific Guidelines
~~~~~~~~~~~~~~~~~~~~~~~~~

**Arcade Games (Snake, Pac-Man, Pong)**

Focus on:
- Smooth, responsive controls
- Collision detection accuracy
- Score tracking and high scores
- Game over and restart functionality

.. code-block:: text

   Controls: Specify exact key mappings
   Physics: Describe movement speed and collision behavior
   Scoring: Define point values for different actions
   Difficulty: Explain how challenge increases over time

**Puzzle Games (Tetris, Match-3, Sudoku)**

Emphasize:
- Grid-based mechanics
- Rule validation
- Move legality checking
- Win condition detection

.. code-block:: text

   Grid System: Dimensions and cell properties
   Rules: Explicit game rules and constraints
   Validation: How to check valid moves/states
   Solutions: Algorithm for checking win conditions

**Strategy Games (Chess, Checkers, Tic-Tac-Toe)**

Include:
- Turn-based mechanics
- Move validation
- Game state management
- AI opponent behavior

.. code-block:: text

   Turn Management: How turns alternate between players
   Move Validation: Rules for legal moves
   Game States: How to detect check, checkmate, stalemate
   AI Difficulty: Specify AI intelligence level

Working with Generated Code
---------------------------

Code Quality Assessment
~~~~~~~~~~~~~~~~~~~~~~

The generated code typically includes:

**✅ Standard Features:**
- Proper imports and dependencies
- Main game loop structure
- Event handling for user input
- Basic error handling
- Inline comments explaining logic

**✅ Quality Indicators:**
- Object-oriented design patterns
- Separation of concerns
- Consistent naming conventions
- Appropriate data structures
- Performance considerations

**⚠️ Areas to Review:**
- Edge case handling
- Resource cleanup (file handles, network connections)
- Memory management for long-running games
- Platform-specific compatibility issues

Code Enhancement Strategies
~~~~~~~~~~~~~~~~~~~~~~~~~~

**1. Performance Optimization**

.. code-block:: python

   # Add performance monitoring
   import time

   class GameProfiler:
       def __init__(self):
           self.frame_times = []
       
       def start_frame(self):
           self.frame_start = time.time()
       
       def end_frame(self):
           frame_time = time.time() - self.frame_start
           self.frame_times.append(frame_time)
           
           # Keep only last 60 frames
           if len(self.frame_times) > 60:
               self.frame_times.pop(0)
       
       def get_fps(self):
           if not self.frame_times:
               return 0
           avg_frame_time = sum(self.frame_times) / len(self.frame_times)
           return 1.0 / avg_frame_time if avg_frame_time > 0 else 0

**2. Error Handling Enhancement**

.. code-block:: python

   # Robust error handling wrapper
   def safe_game_execution(game_function):
       try:
           game_function()
       except pygame.error as e:
           print(f"Pygame error: {e}")
           print("Make sure Pygame is properly installed and audio/video systems are available")
       except KeyboardInterrupt:
           print("Game interrupted by user")
       except Exception as e:
           print(f"Unexpected error: {e}")
           import traceback
           traceback.print_exc()
       finally:
           pygame.quit()
           sys.exit()

**3. Configuration Management**

.. code-block:: python

   # Game configuration system
   import json

   class GameConfig:
       def __init__(self, config_file='game_config.json'):
           self.config_file = config_file
           self.default_config = {
               'window_width': 800,
               'window_height': 600,
               'fps': 60,
               'sound_enabled': True,
               'difficulty': 'medium',
               'controls': {
                   'up': 'w',
                   'down': 's', 
                   'left': 'a',
                   'right': 'd'
               }
           }
           self.config = self.load_config()
       
       def load_config(self):
           try:
               with open(self.config_file, 'r') as f:
                   return {**self.default_config, **json.load(f)}
           except FileNotFoundError:
               return self.default_config
       
       def save_config(self):
           with open(self.config_file, 'w') as f:
               json.dump(self.config, f, indent=2)

Testing Generated Games
~~~~~~~~~~~~~~~~~~~~~~

**1. Functional Testing**

.. code-block:: python

   def test_game_functionality():
       """Test basic game functions work correctly."""
       # Test game initialization
       game = YourGameClass()
       assert game.score == 0
       assert game.lives > 0
       
       # Test player movement
       initial_pos = game.player.position
       game.handle_input('move_right')
       assert game.player.position.x > initial_pos.x
       
       # Test collision detection
       # ... more tests

**2. Performance Testing**

.. code-block:: python

   import time
   import statistics

   def benchmark_game_performance(duration=10):
       """Measure game performance over specified duration."""
       game = YourGameClass()
       frame_times = []
       
       start_time = time.time()
       while time.time() - start_time < duration:
           frame_start = time.time()
           
           # Simulate one game frame
           game.update()
           game.draw()
           
           frame_time = time.time() - frame_start
           frame_times.append(frame_time)
       
       avg_fps = 1.0 / statistics.mean(frame_times)
       min_fps = 1.0 / max(frame_times)
       max_fps = 1.0 / min(frame_times)
       
       print(f"Average FPS: {avg_fps:.1f}")
       print(f"Min FPS: {min_fps:.1f}")
       print(f"Max FPS: {max_fps:.1f}")

Training and Improvement
-----------------------

Crew Training Process
~~~~~~~~~~~~~~~~~~~

Improve the system's performance through iterative training:

.. code-block:: python

   from game_builder_crew.main import train

   # Basic training with 10 iterations
   train(n_iterations=10, filename='trained_model_v1.pkl')

   # Advanced training with custom parameters
   def advanced_training():
       training_configs = [
           {'iterations': 5, 'example': 'example1_pacman'},
           {'iterations': 3, 'example': 'example2_pacman'}, 
           {'iterations': 7, 'example': 'example3_snake'}
       ]
       
       for i, config in enumerate(training_configs):
           print(f"Training phase {i+1}: {config['example']}")
           train(
               n_iterations=config['iterations'],
               filename=f"model_phase_{i+1}.pkl"
           )

Performance Monitoring
~~~~~~~~~~~~~~~~~~~~

Track system performance and quality:

.. code-block:: python

   import time
   import json
   from datetime import datetime

   class CrewPerformanceMonitor:
       def __init__(self):
           self.metrics = {
               'execution_times': [],
               'code_quality_scores': [],
               'success_rates': [],
               'token_usage': []
           }
       
       def record_execution(self, start_time, end_time, success, tokens_used):
           execution_time = end_time - start_time
           self.metrics['execution_times'].append(execution_time)
           self.metrics['success_rates'].append(1 if success else 0)
           self.metrics['token_usage'].append(tokens_used)
       
       def generate_report(self):
           report = {
               'timestamp': datetime.now().isoformat(),
               'avg_execution_time': sum(self.metrics['execution_times']) / len(self.metrics['execution_times']),
               'success_rate': sum(self.metrics['success_rates']) / len(self.metrics['success_rates']),
               'avg_token_usage': sum(self.metrics['token_usage']) / len(self.metrics['token_usage']),
               'total_executions': len(self.metrics['execution_times'])
           }
           
           with open('performance_report.json', 'w') as f:
               json.dump(report, f, indent=2)
           
           return report

Troubleshooting
--------------

Common Issues and Solutions
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Issue: Generated code has syntax errors**

.. code-block:: python

   # Solution: Add syntax validation
   import ast

   def validate_python_syntax(code):
       try:
           ast.parse(code)
           return True, "Syntax is valid"
       except SyntaxError as e:
           return False, f"Syntax error: {e}"

   # Use in your workflow
   result = crew.crew().kickoff(inputs=inputs)
   is_valid, message = validate_python_syntax(result)
   if not is_valid:
       print(f"Generated code has issues: {message}")

**Issue: Game performance is poor**

Solutions:
1. Add performance requirements to game description
2. Specify target FPS in technical requirements
3. Request optimization techniques in the prompt

**Issue: Missing game features**

Solutions:
1. Be more explicit in feature descriptions
2. Include acceptance criteria
3. Provide examples of expected behavior

**Issue: Inconsistent code quality**

Solutions:
1. Train the crew with more iterations
2. Enhance agent backstories with quality focus
3. Add code review criteria to task descriptions

Best Practices Summary
---------------------

**For Game Specifications:**
- Write detailed, unambiguous requirements
- Include technical constraints and preferences
- Specify user interface and control schemes
- Define win/lose conditions clearly
- Include performance targets

**For System Usage:**
- Start with simple games and increase complexity
- Test generated code thoroughly before deployment
- Monitor performance and quality metrics
- Keep training data diverse and comprehensive
- Document successful patterns for reuse

**For Code Quality:**
- Always validate syntax before execution
- Add error handling and logging
- Include configuration management
- Implement proper resource cleanup
- Test across different platforms

Next Steps
---------

- Explore :doc:`examples` for more game creation scenarios
- Learn about :doc:`development/extending` the system
- Review :doc:`api/modules` for advanced customization
- Join the community discussions for tips and tricks

For additional help and advanced topics, refer to the :doc:`development/architecture` guide.
