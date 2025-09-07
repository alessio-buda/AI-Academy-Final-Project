#!/usr/bin/env python3
"""
Simple test script to verify RAG tool functionality
"""

import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from report_generator.tools.rag_tool import RagTool

def test_rag_tool():
    """Test the RAG tool directly"""
    print("Testing RAG tool...")
    
    try:
        rag_tool = RagTool()
        print(f"Tool name: {rag_tool.name}")
        print(f"Tool description: {rag_tool.description}")
        
        # Test with a simple query
        result = rag_tool._run("CrewAI architecture", 3)
        print(f"RAG tool result: {result}")
        print(f"Result type: {type(result)}")
        
    except Exception as e:
        print(f"Error testing RAG tool: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_rag_tool()
