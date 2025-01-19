"""
Test script for Knowledge Graph Generation with sample documents
"""

import os
import sys
import traceback
from src.main import KnowledgeGraphOrchestrator

def test_kg_generation():
    """
    Test Knowledge Graph Generation with various document types
    """
    # Create KG Orchestrator
    kg_orchestrator = KnowledgeGraphOrchestrator()
    
    # Sample documents to test
    sample_documents = [
        'book.txt',
    ]
    
    # Test each document
    for doc_path in sample_documents:
        print(f"\n--- Processing {doc_path} ---")
        try:
            # Check if file exists
            if not os.path.exists(doc_path):
                print(f"File not found: {doc_path}")
                continue
            
            # Generate Knowledge Graph
            kg = kg_orchestrator.generate_knowledge_graph(
                doc_path, 
                max_questions=3, 
                output_format='turtle'
            )
            
            # Save the generated KG
            output_filename = f"{os.path.splitext(doc_path)[0]}_kg.ttl"
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(kg)
            
            print(f"Knowledge Graph generated and saved to {output_filename}")
        
        except Exception as e:
            print(f"Error processing {doc_path}: {e}")
            traceback.print_exc()

def main():
    """
    Main function to run the tests
    """
    test_kg_generation()

if __name__ == "__main__":
    main()