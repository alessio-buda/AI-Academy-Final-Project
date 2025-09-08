#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow import Flow, listen, start

from report_generator.crews.sanitize_crew.sanitize_crew import SanitizeCrew
from report_generator.crews.analysis_crew.analysis_crew import AnalysisCrew
from report_generator.crews.writer_crew.writer_crew import WriterCrew

import json
import re
import os
from datetime import datetime


class ReportState(BaseModel):
    """State model for the report generation flow.
    
    This class represents the state data structure that persists throughout
    the report generation workflow, storing user input and intermediate results.
    
    Attributes:
        input (str): Raw input string (currently unused). Defaults to empty string.
        task (str): User's question or task description. Defaults to empty string.
        sanitized_data (dict): Security-validated and improved query data. Defaults to empty dict.
        analysis_data (dict): Project analysis and outline structure data. Defaults to empty dict.
        
    Example:
        >>> state = ReportState()
        >>> state.task = "Generate a report about AI"
        >>> state.sanitized_data = {"status": "APPROVED", "improved_query": "AI report"}
        >>> print(state.task)
        Generate a report about AI
    """
    input: str = ""
    task: str = ""
    sanitized_data: dict = {}
    analysis_data: dict = {}

class ReportFlow(Flow[ReportState]):
    """A flow that orchestrates multi-step report generation using CrewAI crews.
    
    This class implements a sequential workflow that sanitizes user input,
    analyzes requirements, and generates comprehensive reports through
    specialized AI crews.
    
    The flow consists of three main stages:
    1. Input sanitization and security validation
    2. Project analysis and outline generation  
    3. RAG-enhanced report writing
    
    Attributes:
        state (ReportState): The flow state containing user input and intermediate results.
        
    Example:
        >>> flow = ReportFlow()
        >>> flow.kickoff()  # Starts the interactive report generation process
    """

    @start()
    def get_user_input(self):
        """Prompts user for input and initializes the flow state.
        
        This is the entry point of the flow that captures user requirements
        and stores them in the flow state for subsequent processing steps.
        
        Returns:
            str: The user's input task/question.
            
        Example:
            >>> flow = ReportFlow()
            >>> # User enters: "How does AI work?"
            >>> task = flow.get_user_input()
            >>> print(task)
            How does AI work?
        """
        user_input = input("Enter a question: ")

        self.state.task = user_input
        
        return self.state.task




    
    @listen(get_user_input)
    def sanitize_input(self, state: ReportState) -> None:
        """Validates and sanitizes user input for security and quality.
        
        This step uses the SanitizeCrew to perform security validation
        and query improvement on the user's input. It parses the JSON
        response and updates the flow state with sanitized data.
        
        Args:
            state (ReportState): The current flow state containing user input.
            
        Returns:
            None: Updates self.state.sanitized_data in place.
            
        Raises:
            json.JSONDecodeError: When the crew output cannot be parsed as JSON.
            
        Note:
            If security validation fails (status != "APPROVED"), the function
            prints an error message and returns early without proceeding.
            
        Example:
            >>> # Assuming state.task = "Tell me about AI security"
            >>> flow.sanitize_input(state)
            >>> print(flow.state.sanitized_data["status"])
            APPROVED
        """

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
            
            self.state.sanitized_data = json.loads(json_content)

            print("✅ Parsed sanitized data:", self.state.sanitized_data)

            # Check if input was approved
            if self.state.sanitized_data.get("status") != "APPROVED":
                print("❌ Input blocked by security validation")
                print("Reason:", self.state.sanitized_data.get("explanation", "Security check failed"))
                return
            
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing output: {e}")
            print("Raw output:", sanitize_result.raw)
            return
            
    @listen(sanitize_input)
    def generate_outline(self, state: ReportState) -> None:
        """Generates project analysis and report outline structure.
        
        This step uses the AnalysisCrew to analyze the sanitized query
        and create a detailed outline for the report. It processes the
        improved query and generates structured analysis data.
        
        Args:
            state (ReportState): The current flow state with sanitized data.
            
        Returns:
            None: Updates self.state.analysis_data in place.
            
        Raises:
            json.JSONDecodeError: When the crew output cannot be parsed as JSON.
            
        Note:
            Uses the improved_query from sanitized_data, falling back to
            the original task if not available.
            
        Example:
            >>> # Assuming sanitized_data contains improved_query
            >>> flow.generate_outline(state)
            >>> print(flow.state.analysis_data.keys())
            dict_keys(['target_audience', 'communication_style', 'outline'])
        """
        
        # Step 2: Analysis Crew - Project analysis and outline creation
        analysis_inputs = {
            "improved_query": self.state.sanitized_data.get("improved_query", self.state.task)
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
        
        self.state.analysis_data = json.loads(analysis_content)
        print("✅ Parsed analysis data:", self.state.analysis_data)
            
    @listen(generate_outline)
    def write_report(self, state: ReportState) -> None:
        """Generates the final report using RAG-enhanced content writing.
        
        This step uses the WriterCrew to perform RAG (Retrieval-Augmented Generation)
        searches and write the comprehensive report based on the analysis outline.
        It also creates a summary file documenting the entire generation process.
        
        Args:
            state (ReportState): The current flow state with analysis data.
            
        Returns:
            None: Creates multiple output files in the 'output' directory.
            
        Side Effects:
            - Creates 'output' directory if it doesn't exist
            - Writes multiple files including final report and generation summary
            - Prints status messages to console
            
        Files Created:
            - output/security_check.json: Security validation results
            - output/sanitized_query.json: Improved query data
            - output/project_analysis.json: Analysis results
            - output/detailed_outline.json: Report outline
            - output/rag_search_results.md: RAG search results
            - output/final_report.md: Generated report
            - output/generation_summary.md: Process summary
            
        Example:
            >>> # Assuming analysis_data is populated
            >>> flow.write_report(state)
            ✅ All files saved in the 'output' directory:
              - security_check.json
              - sanitized_query.json
              ...
        """
        
        # Step 3: Writer Crew - RAG search and report writing
        writer_inputs = {
            "outline_structure": self.state.analysis_data,
            "target_audience": self.state.analysis_data.get("target_audience", "technical"),
            "communication_style": self.state.analysis_data.get("communication_style", "technical"),
        }
        
        print("Starting WriterCrew...")
        result = WriterCrew().crew().kickoff(inputs=writer_inputs)
        print("WriterCrew result:", result.raw)
        
        # Create a summary file with all steps
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
{self.state.sanitized_data.get("improved_query", "N/A")}
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
            
def kickoff():
    """Initializes and starts the report generation flow.
    
    Creates a new ReportFlow instance and begins the interactive
    report generation process. This function serves as the main
    entry point for the application.
    
    Returns:
        None: The flow runs interactively until completion.
        
    Example:
        >>> kickoff()
        Enter a question: What is machine learning?
        Starting SanitizeCrew...
        ...
        ✅ All files saved in the 'output' directory
    """
    report_flow = ReportFlow()
    report_flow.kickoff()


def plot():
    """Generates and displays a visual plot of the report generation flow.
    
    Creates a new ReportFlow instance and renders a flowchart diagram
    showing the sequence of steps and dependencies in the workflow.
    
    Returns:
        None: Displays the flow visualization.
        
    Example:
        >>> plot()
        # Displays a flowchart showing: get_user_input -> sanitize_input -> generate_outline -> write_report
    """
    report_flow = ReportFlow()
    report_flow.plot()


if __name__ == "__main__":
    # Test the sanitize crew
    kickoff()
