"""
Simple demo script to test the text file output functionality
without running the full AnalysisCrew evaluation.
"""

import os
from datetime import datetime

def create_demo_scores_file():
    """Create a demo scores file to test the text output functionality."""
    
    # Create evaluation_output directory if it doesn't exist
    output_dir = "evaluation_output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    scores_file = os.path.join(output_dir, f"analysis_crew_scores_demo_{timestamp}.txt")
    
    # Demo metrics
    execution_time = 25.67
    relevance_score = 8.5
    coverage_percentage = 78.3
    judge_time = 2.34
    coverage_time = 1.12
    
    test_input = {
        "improved_query": "Crea una docs per un sistema di gestione inventario con API REST, database PostgreSQL e interfaccia web React. Il sistema deve permettere di tracciare prodotti, gestire ordini e generare report automatici."
    }
    
    coverage_result = {
        'coverage_percentage': coverage_percentage,
        'total_keywords': 6,
        'found_keywords': 5,
        'found_keywords_list': ['sistema di inventario', 'API REST', 'PostgreSQL', 'React', 'report automatici'],
        'missing_keywords_list': ['gestione ordini']
    }
    
    try:
        with open(scores_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("ANALYSIS CREW EVALUATION SCORES\n")
            f.write("=" * 80 + "\n")
            f.write(f"Timestamp: {datetime.now().isoformat()}\n")
            f.write(f"Test Input Query: {test_input['improved_query']}\n")
            f.write("=" * 80 + "\n\n")
            
            f.write("PERFORMANCE METRICS:\n")
            f.write("-" * 40 + "\n")
            f.write(f"Execution Success: {'✅ SUCCESS'}\n")
            f.write(f"Execution Time: {execution_time:.3f} seconds\n")
            f.write(f"Judge Evaluation Time: {judge_time:.3f} seconds\n")
            f.write(f"Coverage Analysis Time: {coverage_time:.3f} seconds\n")
            f.write(f"Total Evaluation Time: {execution_time + judge_time + coverage_time:.3f} seconds\n\n")
            
            f.write("QUALITY METRICS:\n")
            f.write("-" * 40 + "\n")
            f.write(f"LLM Relevance Score: {relevance_score:.2f}/10.0\n")
            f.write(f"Keyword Coverage: {coverage_percentage:.1f}%\n")
            f.write(f"Keywords Found: {coverage_result.get('found_keywords', 0)}/{coverage_result.get('total_keywords', 0)}\n\n")
            
            if coverage_result.get('found_keywords_list'):
                f.write("KEYWORDS FOUND:\n")
                f.write("-" * 20 + "\n")
                for keyword in coverage_result['found_keywords_list']:
                    f.write(f"✅ {keyword}\n")
                f.write("\n")
            
            if coverage_result.get('missing_keywords_list'):
                f.write("KEYWORDS MISSING:\n")
                f.write("-" * 20 + "\n")
                for keyword in coverage_result['missing_keywords_list']:
                    f.write(f"❌ {keyword}\n")
                f.write("\n")
            
            f.write("EVALUATION SUMMARY:\n")
            f.write("-" * 40 + "\n")
            
            # Overall assessment
            if relevance_score >= 9.0 and coverage_percentage >= 80:
                overall_assessment = "🌟 EXCELLENT"
            elif relevance_score >= 7.0 and coverage_percentage >= 60:
                overall_assessment = "✅ GOOD"
            elif relevance_score >= 5.0 and coverage_percentage >= 40:
                overall_assessment = "⚠️ FAIR"
            else:
                overall_assessment = "❌ POOR"
            
            f.write(f"Overall Assessment: {overall_assessment}\n")
            f.write(f"Relevance Level: {'High' if relevance_score >= 7 else 'Medium' if relevance_score >= 4 else 'Low'}\n")
            f.write(f"Coverage Level: {'High' if coverage_percentage >= 70 else 'Medium' if coverage_percentage >= 40 else 'Low'}\n")
            f.write(f"Performance Level: {'Fast' if execution_time < 30 else 'Medium' if execution_time < 60 else 'Slow'}\n\n")
            
            f.write("DETAILED METRICS (for MLflow):\n")
            f.write("-" * 40 + "\n")
            f.write(f"execution_success: 1\n")
            f.write(f"execution_time_seconds: {execution_time:.6f}\n")
            f.write(f"llm_relevance_score: {relevance_score:.6f}\n")
            f.write(f"judge_evaluation_time: {judge_time:.6f}\n")
            f.write(f"keyword_coverage_percentage: {coverage_percentage:.6f}\n")
            f.write(f"keywords_total_count: {coverage_result.get('total_keywords', 0)}\n")
            f.write(f"keywords_found_count: {coverage_result.get('found_keywords', 0)}\n")
            f.write(f"coverage_analysis_time: {coverage_time:.6f}\n")
            
            f.write("\n" + "=" * 80 + "\n")
            f.write("END OF EVALUATION REPORT\n")
            f.write("=" * 80 + "\n")
        
        print(f"✅ Demo scores file created successfully!")
        print(f"💾 Saved to: {scores_file}")
        
        # Display a preview of the file
        print("\n" + "="*50)
        print("PREVIEW OF GENERATED FILE:")
        print("="*50)
        with open(scores_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Show first 1000 characters
            print(content[:1000] + ("..." if len(content) > 1000 else ""))
        
        return scores_file
        
    except Exception as e:
        print(f"❌ Error creating demo scores file: {e}")
        return None

if __name__ == "__main__":
    print("🧪 Testing text file output functionality")
    print("-" * 50)
    create_demo_scores_file()
    print("\n✅ Text file output test completed!")
