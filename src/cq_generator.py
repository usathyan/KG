"""
Competency Question (CQ) Generator Module

This module is responsible for generating meaningful questions
that can be answered from a given document, focusing on key
entities and concepts.
"""

import spacy
from typing import List, Dict

class CompetencyQuestionGenerator:
    def __init__(self, model='en_core_web_sm'):
        """
        Initialize the CQ Generator with a spaCy language model.
        
        :param model: spaCy language model to use
        """
        try:
            self.nlp = spacy.load(model)
        except OSError:
            print(f"Downloading language model {model}")
            spacy.cli.download(model)
            self.nlp = spacy.load(model)

    def generate_questions(self, document: str, max_questions: int = 3) -> List[str]:
        """
        Generate competency questions from a given document.
        
        :param document: Input text to generate questions from
        :param max_questions: Maximum number of questions to generate
        :return: List of generated questions
        """
        doc = self.nlp(document)
        
        # Extract key entities and their types
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        
        questions = []
        
        # Generate questions based on named entities
        for entity, entity_type in entities:
            if entity_type in ['PERSON', 'ORG', 'GPE', 'DATE']:
                questions.append(f"What is the {entity_type.lower()} of {entity}?")
        
        # Limit to max_questions
        return questions[:max_questions]

def main():
    """
    Example usage of the Competency Question Generator
    """
    sample_doc = "Douglas Noel Adams (11 March 1952 − 11 May 2001) was an English author, humourist, and screenwriter, best known for The Hitchhiker's Guide to the Galaxy (HHGTTG)."
    
    cq_generator = CompetencyQuestionGenerator()
    questions = cq_generator.generate_questions(sample_doc)
    
    print("Generated Competency Questions:")
    for q in questions:
        print(q)

if __name__ == "__main__":
    main()