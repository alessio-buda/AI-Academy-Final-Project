# Sanitize Crew MLflow Evaluation

This directory contains a simple MLflow evaluation system for the Sanitize Crew. The evaluation tracks security detection accuracy, sanitization quality, and overall performance.

## Quick Start

### 1. Run a Simple Evaluation

After running your sanitize crew, evaluate the results:

```bash
python evaluate_simple.py
```

This script will:
- Load the output files from your sanitize crew run
- Calculate performance metrics
- Log results to MLflow
- Display a performance summary

### 2. View Results in MLflow UI

Start the MLflow UI to see detailed results:

```bash
mlflow ui
```

Then open: http://localhost:5000

### 3. Complete Test Pipeline

Run the complete test with multiple inputs:

```bash
python test_evaluation.py
```

This will run several test cases and evaluate each one.

## Files

- `evaluation.py` - Main evaluation classes and functions
- `evaluate_simple.py` - Simple standalone evaluation script
- `test_evaluation.py` - Complete test pipeline
- `example_evaluation.py` - Example usage (requires proper imports)

## Metrics Tracked

### Security Metrics
- `security_completeness` - How complete the security analysis is
- `confidence_score` - Confidence in the security assessment
- `security_classification` - Whether security status was properly classified
- `risk_score` - Risk level assessment (LOW=0.9, MEDIUM=0.5, HIGH=0.1)
- `threats_count` - Number of threats detected

### Sanitization Metrics
- `process_halted` - Whether the process was halted for unsafe input
- `sanitization_success` - Whether sanitization was successful
- `length_improvement` - How much the query was improved/expanded
- `improvement_documented` - Whether improvements were documented

### Overall Metrics
- `overall_score` - Combined performance score
- `expectation_match` - Whether the result matched expectations

## Usage Examples

### Basic Evaluation
```python
from evaluate_simple import run_simple_evaluation

metrics = run_simple_evaluation(
    user_input="Help me create a presentation about my AI project",
    expected_safe=True
)
print(f"Overall Score: {metrics['overall_score']:.3f}")
```

### With Ground Truth
```python
from src.report_generator.crews.sanitize_crew.evaluation import simple_evaluate_run

metrics = simple_evaluate_run(
    input_text="Suspicious input here",
    expected_risk_level="HIGH",
    expected_threats=["prompt injection"]
)
```

## MLflow Experiments

The evaluation creates these MLflow experiments:
- `sanitize_crew_simple_evaluation` - For simple evaluations
- `sanitize_crew_evaluation` - For detailed evaluations
- `sanitize_crew_batch_evaluation` - For batch tests

## Performance Interpretation

- **Score > 0.8**: Excellent performance 🟢
- **Score 0.6-0.8**: Good performance 🟡  
- **Score < 0.6**: Needs improvement 🔴

## Tips

1. **Run crew first**: Always run your sanitize crew before evaluation
2. **Check output files**: Ensure `output/security_check.json` and `output/sanitized_query.json` exist
3. **Use MLflow UI**: The web interface provides the best view of results
4. **Compare runs**: Use MLflow to compare performance across different inputs
5. **Set expectations**: Provide expected risk levels for more accurate evaluation
