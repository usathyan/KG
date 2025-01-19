"""
Knowledge Graph Builder Module

This module is responsible for constructing the final knowledge graph
based on extracted relations and ontology mapping.
"""

from typing import List, Dict, Any
import rdflib
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, XSD
import spacy
import re
import urllib.parse

class KnowledgeGraphBuilder:
    def __init__(self):
        """
        Initialize the Knowledge Graph Builder with namespaces and NLP model.
        """
        # Define common namespaces
        self.WD = Namespace("http://www.wikidata.org/entity/")
        self.WDT = Namespace("http://www.wikidata.org/prop/direct/")
        self.SCHEMA = Namespace("http://schema.org/")
        
        # Load spaCy model for NER
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("SpaCy model not found. Named Entity Recognition will be limited.")
            self.nlp = None

    def sanitize_uri(self, value: str) -> str:
        """
        Sanitize a string to be used as a valid URI component.
        
        :param value: Input string to sanitize
        :return: Sanitized string suitable for URI
        """
        # Replace special characters and spaces
        sanitized = re.sub(r'[^\w\-]', '_', str(value))
        # Remove consecutive underscores
        sanitized = re.sub(r'_+', '_', sanitized)
        # URL encode to handle any remaining special characters
        return urllib.parse.quote(sanitized, safe='')

    def extract_entities(self, text: str) -> List[Dict[str, str]]:
        """
        Extract named entities from the text using spaCy.
        
        :param text: Input text to extract entities from
        :return: List of extracted entities
        """
        if not self.nlp:
            return []

        doc = self.nlp(text)
        entities = []
        for ent in doc.ents:
            entities.append({
                'text': ent.text,
                'label': ent.label_
            })
        return entities

    def build_knowledge_graph(self, 
                               text: str, 
                               relations: List[Dict[str, Any]], 
                               competency_questions: List[str]) -> str:
        """
        Build a knowledge graph from the input text, relations, and questions.
        
        :param text: Input text
        :param relations: List of extracted relations
        :param competency_questions: List of generated competency questions
        :return: Serialized knowledge graph in Turtle format
        """
        # Create a new graph
        g = Graph()
        
        # Add namespace prefixes
        g.namespace_manager.bind("wd", self.WD)
        g.namespace_manager.bind("wdt", self.WDT)
        g.namespace_manager.bind("schema", self.SCHEMA)
        g.namespace_manager.bind("rdfs", RDFS)
        g.namespace_manager.bind("rdf", RDF)
        g.namespace_manager.bind("xsd", XSD)
        
        # Extract named entities
        entities = self.extract_entities(text)
        
        # Create a document-level resource
        doc_uri = URIRef(self.WD['Document'])
        g.add((doc_uri, RDF.type, self.SCHEMA.CreativeWork))
        g.add((doc_uri, RDFS.label, Literal("Source Document", lang='en')))
        
        # Add entities to the graph
        for entity in entities:
            entity_uri = URIRef(self.WD[self.sanitize_uri(entity['text'])])
            g.add((entity_uri, RDF.type, self.SCHEMA[entity['label']]))
            g.add((entity_uri, RDFS.label, Literal(entity['text'], lang='en')))
            g.add((doc_uri, self.SCHEMA.mentions, entity_uri))
        
        # Add relations to the graph
        for relation in relations:
            # Sanitize relation name to create a valid URI
            sanitized_relation = self.sanitize_uri(relation['relation'])
            relation_uri = URIRef(self.WDT[sanitized_relation])
            g.add((relation_uri, RDF.type, self.SCHEMA.Property))
            g.add((relation_uri, RDFS.label, Literal(relation['relation'])))
            g.add((relation_uri, RDFS.comment, Literal(relation['description'])))
        
        # Add competency questions to the graph
        for idx, question in enumerate(competency_questions, 1):
            question_uri = URIRef(f"{self.WD}CompetencyQuestion_{idx}")
            g.add((question_uri, RDF.type, self.SCHEMA.Question))
            g.add((question_uri, RDFS.label, Literal(question, lang='en')))
            g.add((doc_uri, self.SCHEMA.hasPart, question_uri))
        
        # Serialize the graph
        return g.serialize(format='turtle')

def main():
    """
    Example usage of the Knowledge Graph Builder
    """
    # Sample text
    sample_text = "Douglas Adams was a famous British author known for The Hitchhiker's Guide to the Galaxy."
    
    # Sample relations
    relations = [
        {
            'relation': 'occupation',
            'description': 'The primary occupation of a person',
            'domain': 'Person',
            'range': 'Occupation'
        },
        {
            'relation': '20%',  # Test case for special character
            'description': 'Percentage test',
            'domain': 'Measurement',
            'range': 'Percentage'
        }
    ]
    
    # Sample competency questions
    competency_questions = [
        "Who was Douglas Adams?",
        "What is Douglas Adams known for?"
    ]
    
    # Create KG Builder
    kg_builder = KnowledgeGraphBuilder()
    
    # Build and print the knowledge graph
    kg_turtle = kg_builder.build_knowledge_graph(
        sample_text, 
        relations, 
        competency_questions
    )
    print(kg_turtle)

if __name__ == "__main__":
    main()