"""
Main Orchestration Script for Knowledge Graph Generation

This script coordinates the entire knowledge graph generation process,
integrating components from other modules and supporting multiple file formats.
"""

import sys
import os
import argparse
from typing import List, Dict

import spacy
import textract  # For reading various file formats
from .cq_generator import CompetencyQuestionGenerator
from .relation_extractor import RelationExtractor
from .ontology_matcher import OntologyMatcher
from .kg_builder import KnowledgeGraphBuilder

class KnowledgeGraphOrchestrator:
    def __init__(self):
        """
        Initialize the Knowledge Graph Orchestrator with required components.
        """
        self.cq_generator = CompetencyQuestionGenerator()
        self.relation_extractor = RelationExtractor()
        self.ontology_matcher = OntologyMatcher()
        self.kg_builder = KnowledgeGraphBuilder()

    def generate_knowledge_graph(self, doc_path: str, max_questions: int = 3, output_format: str = 'turtle'):
        """
        Generate a knowledge graph from a given document.

        Args:
            doc_path (str): Path to the input document
            max_questions (int, optional): Maximum number of competency questions to generate. Defaults to 3.
            output_format (str, optional): Output format for the knowledge graph. Defaults to 'turtle'.

        Returns:
            str: Knowledge graph in the specified output format
        """
        # Extract text from the document
        try:
            text = textract.process(doc_path).decode('utf-8')
        except Exception as e:
            raise ValueError(f"Could not extract text from {doc_path}: {e}")

        # Generate competency questions
        competency_questions = self.cq_generator.generate_questions(text, max_questions)

        # Extract relations from the text
        relations = self.relation_extractor.extract_relations(text)

        # Match with ontology
        matched_relations = self.ontology_matcher.match_relations(relations)

        # Build knowledge graph
        kg = self.kg_builder.build_knowledge_graph(text, matched_relations, competency_questions)

        # Convert to specified output format (currently only turtle is supported)
        if output_format.lower() != 'turtle':
            raise ValueError(f"Unsupported output format: {output_format}. Only 'turtle' is currently supported.")

        return kg

def main():
    parser = argparse.ArgumentParser(description='Generate a Knowledge Graph from a document')
    parser.add_argument('input_file', help='Path to the input document')
    parser.add_argument('--max-questions', type=int, default=3, 
                        help='Maximum number of competency questions to generate')
    parser.add_argument('--output-format', default='turtle', 
                        choices=['turtle'], 
                        help='Output format for the knowledge graph')
    
    args = parser.parse_args()

    # Create orchestrator
    orchestrator = KnowledgeGraphOrchestrator()

    try:
        # Generate knowledge graph
        kg = orchestrator.generate_knowledge_graph(
            args.input_file, 
            max_questions=args.max_questions, 
            output_format=args.output_format
        )

        # Determine output filename
        base_filename = os.path.splitext(args.input_file)[0]
        output_filename = f"{base_filename}.ttl"

        # Serialize and save the graph
        with open(output_filename, 'w') as f:
            f.write(kg)

        print(f"Knowledge graph saved to {output_filename}")

    except Exception as e:
        print(f"Error generating knowledge graph: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()