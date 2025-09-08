main module
===========

.. automodule:: game_builder_crew.main
   :members:
   :undoc-members:
   :show-inheritance:

Module Overview
---------------

The main module provides the primary entry points for executing and training the Game Builder Crew. It contains two key functions that handle different aspects of the system:

- **run()**: Production execution with predefined examples
- **train()**: Training and model improvement functionality

Functions
---------

.. autofunction:: game_builder_crew.main.run

   Executes the Game Builder Crew to create a game using the Snake game example.

   **Process Overview:**

   1. **Configuration Loading**: Loads game examples from ``gamedesign.yaml``
   2. **Crew Initialization**: Creates a new GameBuilderCrew instance
   3. **Execution**: Runs the crew with the Snake game specification
   4. **Output Display**: Shows the generated game code to the user

   **Default Game Example:**

   Uses ``example3_snake`` from the configuration, which includes:
   - Grid-based movement system
   - Food consumption mechanics
   - Growth and collision detection
   - Scoring system
   - Game over conditions

   **Console Output:**

   .. code-block:: text

      ## Welcome to the Game Crew
      -------------------------------
      [CrewAI execution logs showing agent interactions]
      
      ########################
      ## Here is the result
      ########################
      
      final code for the game:
      [Complete Python Snake game implementation]

   **Usage Examples:**

   .. code-block:: python

      # Direct function call
      from game_builder_crew.main import run
      run()

   .. code-block:: bash

      # Command line execution
      poetry run game_builder_crew

   **Error Handling:**

   The function handles several types of errors:

   .. list-table::
      :header-rows: 1
      :widths: 30 70

      * - Exception Type
        - Handling
      * - ``FileNotFoundError``
        - Configuration file missing - provides clear error message
      * - ``yaml.YAMLError``
        - Invalid YAML syntax - shows parsing error details
      * - ``Exception``
        - General execution errors - logs full error context

   **Configuration Dependencies:**

   .. code-block:: text

      Required Files:
      ├── src/game_builder_crew/config/
      │   ├── agents.yaml       # Agent configurations
      │   ├── tasks.yaml        # Task definitions
      │   └── gamedesign.yaml   # Game examples (uses example3_snake)

.. autofunction:: game_builder_crew.main.train

   Trains the Game Builder Crew using iterative learning to improve performance.

   **Training Process:**

   1. **Example Loading**: Uses ``example1_pacman`` for training data
   2. **Parameter Validation**: Validates iteration count and filename
   3. **Training Execution**: Runs CrewAI training process
   4. **Model Persistence**: Saves trained model to specified file

   **Parameters:**

   .. list-table::
      :header-rows: 1
      :widths: 20 15 65

      * - Parameter
        - Type  
        - Description
      * - ``n_iterations``
        - ``Optional[int]``
        - Number of training iterations. If None, reads from ``sys.argv[1]``
      * - ``filename``
        - ``Optional[str]``
        - Output filename for trained model. If None, reads from ``sys.argv[2]``

   **Training Configuration:**

   Uses the complex Pac-Man example for training because:
   - **Complexity**: Provides rich learning scenarios
   - **Variety**: Multiple game mechanics and interactions
   - **Challenge**: Tests agent collaboration effectively

   **Command Line Usage:**

   .. code-block:: bash

      # Method 1: Direct command line arguments
      python -c "from game_builder_crew.main import train; train()" 10 trained_model.pkl

      # Method 2: Custom script
      poetry run python training_script.py

   **Programmatic Usage:**

   .. code-block:: python

      from game_builder_crew.main import train

      # Basic training
      train(n_iterations=10, filename="model_v1.pkl")

      # Advanced training loop
      for phase in range(3):
          train(
              n_iterations=5 + phase * 2,
              filename=f"model_phase_{phase}.pkl"
          )

   **Training Output:**

   .. code-block:: text

      Training completed successfully with 10 iterations.
      Trained model saved as: trained_model.pkl

   **Error Handling:**

   .. list-table::
      :header-rows: 1
      :widths: 30 70

      * - Exception Type
        - Description
      * - ``FileNotFoundError``
        - Configuration file not found
      * - ``yaml.YAMLError``
        - YAML parsing error in configuration
      * - ``ValueError``
        - Invalid iteration count or filename
      * - ``IndexError``
        - Missing command line arguments
      * - ``Exception``
        - General training execution error

   **Validation Rules:**

   .. code-block:: python

      # Parameter validation logic
      if n_iterations <= 0:
          raise ValueError("Number of iterations must be positive")
      
      if not filename:
          raise ValueError("Filename cannot be empty")

   **Training Best Practices:**

   .. code-block:: python

      # Incremental training approach
      def incremental_training():
          base_iterations = 5
          
          for level in ["basic", "intermediate", "advanced"]:
              iterations = base_iterations * (2 ** ["basic", "intermediate", "advanced"].index(level))
              filename = f"model_{level}.pkl"
              
              print(f"Training {level} level with {iterations} iterations")
              train(n_iterations=iterations, filename=filename)

Module Configuration
-------------------

**Default Settings:**

.. code-block:: python

   # Game examples used by default
   PRODUCTION_EXAMPLE = 'example3_snake'    # Used by run()
   TRAINING_EXAMPLE = 'example1_pacman'     # Used by train()

   # File paths
   CONFIG_PATH = 'src/game_builder_crew/config/gamedesign.yaml'

**Environment Variables:**

The module respects these environment variables:

.. code-block:: bash

   # OpenAI Configuration
   OPENAI_API_KEY=your_key_here
   OPENAI_MODEL=gpt-4o

   # Logging
   LOG_LEVEL=INFO
   CREW_VERBOSE=true

   # Training Parameters  
   DEFAULT_ITERATIONS=10
   MODEL_OUTPUT_DIR=./models/

Integration Examples
-------------------

**Custom Execution Script:**

.. code-block:: python

   #!/usr/bin/env python3
   """Custom game generation script."""

   import sys
   import argparse
   from game_builder_crew.main import run, train
   from game_builder_crew.crew import GameBuilderCrew

   def main():
       parser = argparse.ArgumentParser(description='Game Builder Crew CLI')
       parser.add_argument('--mode', choices=['run', 'train', 'custom'], 
                          default='run', help='Execution mode')
       parser.add_argument('--iterations', type=int, default=10,
                          help='Training iterations')
       parser.add_argument('--output', default='trained_model.pkl',
                          help='Output filename for training')
       parser.add_argument('--game', help='Custom game description')
       
       args = parser.parse_args()
       
       if args.mode == 'run':
           run()
       elif args.mode == 'train':
           train(n_iterations=args.iterations, filename=args.output)
       elif args.mode == 'custom' and args.game:
           crew = GameBuilderCrew()
           inputs = {'game': args.game}
           result = crew.crew().kickoff(inputs=inputs)
           print(result)
       else:
           parser.print_help()

   if __name__ == '__main__':
       main()

**Batch Processing:**

.. code-block:: python

   import yaml
   from game_builder_crew.crew import GameBuilderCrew

   def batch_generate_games():
       """Generate multiple games from all examples."""
       
       # Load all examples
       with open('src/game_builder_crew/config/gamedesign.yaml', 'r') as f:
           examples = yaml.safe_load(f)
       
       crew = GameBuilderCrew()
       results = {}
       
       for example_name, game_spec in examples.items():
           if example_name.startswith('example'):
               print(f"Generating game from {example_name}...")
               
               inputs = {'game': game_spec}
               result = crew.crew().kickoff(inputs=inputs)
               
               # Save to file
               output_file = f"generated_{example_name}.py"
               with open(output_file, 'w') as f:
                   f.write(result)
               
               results[example_name] = output_file
               print(f"Saved to {output_file}")
       
       return results

**Performance Monitoring:**

.. code-block:: python

   import time
   import json
   from datetime import datetime
   from game_builder_crew.main import run

   def monitored_execution():
       """Run with performance monitoring."""
       
       start_time = time.time()
       start_memory = get_memory_usage()  # Custom function
       
       try:
           run()
           success = True
           error_msg = None
       except Exception as e:
           success = False
           error_msg = str(e)
       
       end_time = time.time()
       end_memory = get_memory_usage()
       
       # Log performance metrics
       metrics = {
           'timestamp': datetime.now().isoformat(),
           'execution_time': end_time - start_time,
           'memory_used': end_memory - start_memory,
           'success': success,
           'error': error_msg
       }
       
       with open('performance_log.json', 'a') as f:
           f.write(json.dumps(metrics) + '\n')
       
       return metrics

Testing Support
---------------

**Unit Test Helpers:**

.. code-block:: python

   import unittest
   from unittest.mock import patch, MagicMock
   from game_builder_crew.main import run, train

   class TestMainModule(unittest.TestCase):
       
       @patch('game_builder_crew.main.GameBuilderCrew')
       @patch('yaml.safe_load')
       def test_run_success(self, mock_yaml, mock_crew):
           """Test successful execution of run()."""
           
           # Setup mocks
           mock_yaml.return_value = {'example3_snake': 'test game spec'}
           mock_crew_instance = MagicMock()
           mock_crew.return_value = mock_crew_instance
           mock_crew_instance.crew().kickoff.return_value = "# Test game code"
           
           # Execute
           run()
           
           # Verify
           mock_crew_instance.crew().kickoff.assert_called_once()
           
       def test_train_parameter_validation(self):
           """Test parameter validation in train()."""
           
           with self.assertRaises(ValueError):
               train(n_iterations=0, filename="test.pkl")
           
           with self.assertRaises(ValueError):
               train(n_iterations=5, filename="")

See Also
--------

- :doc:`crew`: Core crew orchestration
- :doc:`configuration`: Configuration file formats
- :doc:`../usage`: Detailed usage examples
- :doc:`../development/testing`: Testing strategies
