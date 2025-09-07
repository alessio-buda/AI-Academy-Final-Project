#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow import Flow, listen, start

from report_generator.crews.sanitize_crew.sanitize_crew import SanitizeCrew
from report_generator.crews.analysis_crew.analysis_crew import AnalysisCrew
from report_generator.crews.writer_crew.writer_crew import WriterCrew


class ReportState(BaseModel):
    input: str = ""
    task: str = ""

class ReportFlow(Flow[ReportState]):

    """A flow that generates a report about CrewAI"""

    @start()
    def get_user_input(self):
        user_input = input("Enter a question: ")
        user_input = {
            "project_description": "CrewAI is a framework to build AI applications with LLMs and generative AI.",
            "outline": "Scelte architetturali, Diagramma della crew, Esempi pratici, Analisi critica.",
            "audience": "technical",
        }
        self.state.task = user_input
        
        return self.state.task




    
    @listen(get_user_input)
    def write(self, state: ReportState) -> None:

        # Use the actual user input from get_user_input step
        inputs = {
            "user_input": self.state.task
        }
        print("Starting SanitizeCrew...")

        # Step 1: Sanitize Crew - Security check and query improvement
        sanitize_result = SanitizeCrew().crew().kickoff(inputs=inputs)
        
        print("SanitizeCrew result:", sanitize_result.raw)
        
        # Parse the JSON output from SanitizeCrew
        try:
            import json
            import re
            
            raw_output = sanitize_result.raw
            print("Raw sanitized output:", raw_output)
            
            # Remove markdown code blocks if present
            if "```json" in raw_output:
                json_match = re.search(r'```json\s*(.*?)\s*```', raw_output, re.DOTALL)
                if json_match:
                    json_content = json_match.group(1)
                else:
                    json_content = raw_output
            else:
                json_content = raw_output
            
            sanitized_data = json.loads(json_content)
            print("✅ Parsed sanitized data:", sanitized_data)
            
            # Check if input was approved
            if sanitized_data.get("status") != "APPROVED":
                print("❌ Input blocked by security validation")
                print("Reason:", sanitized_data.get("explanation", "Security check failed"))
                return
                
            # Step 2: Analysis Crew - Project analysis and outline creation
            analysis_inputs = {
                "improved_query": sanitized_data.get("improved_query", self.state.task)
            }
            
            print("Starting AnalysisCrew...")
            analysis_result = AnalysisCrew().crew().kickoff(inputs=analysis_inputs)
            print("AnalysisCrew result:", analysis_result.raw)
            
            # Parse analysis result
            analysis_output = analysis_result.raw
            if "```json" in analysis_output:
                json_match = re.search(r'```json\s*(.*?)\s*```', analysis_output, re.DOTALL)
                if json_match:
                    analysis_content = json_match.group(1)
                else:
                    analysis_content = analysis_output
            else:
                analysis_content = analysis_output
            
            analysis_data = json.loads(analysis_content)
            print("✅ Parsed analysis data:", analysis_data)
            
            # Step 3: Writer Crew - RAG search and report writing
            writer_inputs = {
                "outline_structure": analysis_data,
                "target_audience": analysis_data.get("target_audience", "tecnico"),
                "communication_style": analysis_data.get("stile_comunicazione", "tecnico")
            }
            
            print("Starting WriterCrew...")
            result = WriterCrew().crew().kickoff(inputs=writer_inputs)
            print("WriterCrew result:", result.raw)
            
            # Create a summary file with all steps
            import os
            from datetime import datetime
            
            summary_content = f"""# Report Generation Summary
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Process Flow
1. **Sanitize Crew**: Security check and query improvement
2. **Analysis Crew**: Project analysis and outline creation  
3. **Writer Crew**: RAG search and final report writing

## Files Generated
- `output/security_check.json`: Security validation results
- `output/sanitized_query.json`: Improved and sanitized query
- `output/project_analysis.json`: Project analysis results
- `output/detailed_outline.json`: Detailed report outline
- `output/rag_search_results.md`: RAG search results with sources
- `output/final_report.md`: Final generated report

## Original Query
```
{self.state.task}
```

## Improved Query
```
{sanitized_data.get("improved_query", "N/A")}
```

## Status
✅ All crews completed successfully
✅ All output files generated
"""
            
            # Ensure output directory exists
            os.makedirs("output", exist_ok=True)
            
            # Write summary file
            with open("output/generation_summary.md", "w", encoding="utf-8") as f:
                f.write(summary_content)
            
            print("✅ All files saved in the 'output' directory:")
            print("  - security_check.json")
            print("  - sanitized_query.json") 
            print("  - project_analysis.json")
            print("  - detailed_outline.json")
            print("  - rag_search_results.md")
            print("  - final_report.md")
            print("  - generation_summary.md")
            
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing output: {e}")
            print("Raw output:", sanitize_result.raw)
            return
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return
def kickoff():
    report_flow = ReportFlow()
    report_flow.kickoff()


def plot():
    report_flow = ReportFlow()
    report_flow.plot()


if __name__ == "__main__":
    # Test the sanitize crew
    kickoff()
