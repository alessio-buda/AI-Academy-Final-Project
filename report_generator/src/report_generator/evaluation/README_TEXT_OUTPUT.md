# Analysis Crew MLflow Evaluator - Text Output Feature

## Overview
The `test_analysis_crew_mlflow.py` has been enhanced to include comprehensive text file output functionality alongside the existing MLflow tracking capabilities.

## New Features Added

### 1. Text File Output for Successful Evaluations
- **File naming**: `analysis_crew_scores_YYYYMMDD_HHMMSS.txt`
- **Location**: `evaluation_output/` directory
- **Content includes**:
  - Detailed performance metrics (execution times, success status)
  - Quality metrics (LLM relevance score, keyword coverage percentage)
  - Complete breakdown of found/missing keywords
  - Overall assessment and recommendations
  - All MLflow metric values with full precision

### 2. Text File Output for Failed Evaluations
- **File naming**: `analysis_crew_error_scores_YYYYMMDD_HHMMSS.txt`
- **Content includes**:
  - Error details (type, message, stack trace)
  - Performance metrics up to failure point
  - Zero-valued quality metrics
  - Failure assessment and timing

### 3. MLflow Integration
- Both success and error text files are automatically uploaded as MLflow artifacts
- All existing MLflow functionality preserved
- Error cases properly tagged and logged

## File Structure Example

```
ANALYSIS CREW EVALUATION SCORES
================================================================================
Timestamp: 2025-09-08T18:25:38.930556
Test Input Query: [Original query text]
================================================================================

PERFORMANCE METRICS:
----------------------------------------
Execution Success: ✅ SUCCESS
Execution Time: 25.670 seconds
Judge Evaluation Time: 2.340 seconds
Coverage Analysis Time: 1.120 seconds
Total Evaluation Time: 29.130 seconds

QUALITY METRICS:
----------------------------------------
LLM Relevance Score: 8.50/10.0
Keyword Coverage: 78.3%
Keywords Found: 5/6

KEYWORDS FOUND:
--------------------
✅ sistema di inventario
✅ API REST
✅ PostgreSQL
✅ React
✅ report automatici

KEYWORDS MISSING:
--------------------
❌ gestione ordini

EVALUATION SUMMARY:
----------------------------------------
Overall Assessment: ✅ GOOD
Relevance Level: High
Coverage Level: High
Performance Level: Fast

DETAILED METRICS (for MLflow):
----------------------------------------
execution_success: 1
execution_time_seconds: 25.670000
llm_relevance_score: 8.500000
judge_evaluation_time: 2.340000
keyword_coverage_percentage: 78.300000
keywords_total_count: 6
keywords_found_count: 5
coverage_analysis_time: 1.120000

================================================================================
END OF EVALUATION REPORT
================================================================================
```

## Usage

The text file functionality is automatically activated when running the evaluation:

```python
python test_analysis_crew_mlflow.py
```

## Key Benefits

1. **Human-Readable Reports**: Easy to review evaluation results without accessing MLflow UI
2. **Comprehensive Analysis**: Includes overall assessment and recommendations
3. **Timestamped Archives**: Each run creates a unique file for historical tracking
4. **Error Documentation**: Failed runs generate detailed error reports
5. **MLflow Integration**: Text files are automatically uploaded as artifacts
6. **Portable Results**: Text files can be easily shared or included in documentation

## Testing

A demo script `demo_text_output.py` has been created to test the text output functionality independently of the full AnalysisCrew evaluation.

## Notes

- Files are saved to `evaluation_output/` directory (created automatically)
- Both successful and failed evaluation runs generate text files
- Text files use UTF-8 encoding for international character support
- All errors during text file creation are caught and logged to MLflow
- The functionality gracefully degrades if file writing fails
