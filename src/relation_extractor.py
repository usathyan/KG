"""
Relation Extractor Module

This module is responsible for analyzing competency questions
and extracting semantic relationships between entities.
"""

from typing import List, Dict, Tuple
import json
import os

class RelationExtractor:
    def __init__(self, config_path: str = None):
        """
        Initialize the Relation Extractor with predefined and custom relations.
        
        :param config_path: Optional path to a JSON file with custom relations
        """
        # Predefined standard relations
        self.standard_relations = {
            'date of birth': {
                'description': 'The date on which the subject was born',
                'domain': 'Person',
                'range': 'Date'
            },
            'date of death': {
                'description': 'The date on which the subject died',
                'domain': 'Person',
                'range': 'Date'
            },
            'occupation': {
                'description': 'The occupation of a person',
                'domain': 'Person',
                'range': 'Occupation'
            },
            'country of citizenship': {
                'description': 'The country of which the subject is a citizen',
                'domain': 'Person',
                'range': 'Country'
            },
            'notable work': {
                'description': 'The most notable work of a person',
                'domain': 'Person',
                'range': 'Creative Work'
            }
        }
        
        # Load custom relations from JSON if provided
        self.custom_relations = {}
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    self.custom_relations = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading custom relations: {e}")
        
        # Combine standard and custom relations
        self.all_relations = {**self.standard_relations, **self.custom_relations}

    def extract_relations(self, text: str) -> List[Dict[str, str]]:
        """
        Extract relations from a given text.
        
        :param text: Input text to extract relations from
        :return: List of extracted relations
        """
        relations = []
        
        # Normalize text
        text = text.lower()
        
        # Match known relation patterns from all relations
        for relation, details in self.all_relations.items():
            if relation in text:
                relations.append({
                    'relation': relation,
                    'description': details['description'],
                    'domain': details.get('domain', 'Unknown'),
                    'range': details.get('range', 'Unknown')
                })
        
        return relations

    def add_custom_relation(self, relation: Dict[str, str]):
        """
        Add a new custom relation to the extractor.
        
        :param relation: Dictionary containing relation details
        """
        key = relation.get('relation')
        if key:
            self.custom_relations[key] = {
                'description': relation.get('description', ''),
                'domain': relation.get('domain', 'Unknown'),
                'range': relation.get('range', 'Unknown')
            }
            # Update all_relations
            self.all_relations[key] = self.custom_relations[key]

    def save_custom_relations(self, config_path: str):
        """
        Save custom relations to a JSON file.
        
        :param config_path: Path to save the JSON configuration
        """
        try:
            with open(config_path, 'w') as f:
                json.dump(self.custom_relations, f, indent=2)
            print(f"Custom relations saved to {config_path}")
        except IOError as e:
            print(f"Error saving custom relations: {e}")

    def format_relations_for_rdf(self, relations: List[Dict[str, str]]) -> str:
        """
        Convert extracted relations to RDF turtle format.
        
        :param relations: List of extracted relations
        :return: RDF turtle formatted relations
        """
        rdf_prefixes = """
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix wdt: <http://www.wikidata.org/prop/direct/> .
@prefix wd: <http://www.wikidata.org/entity/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
"""
        
        rdf_relations = []
        for relation in relations:
            rdf_entry = f"""
wdt:{relation['relation'].replace(' ', '')} a wikibase:Property ;
    rdfs:label "{relation['relation']}"@en ;
    schema:description "{relation['description']}" ;
    rdfs:domain wd:{relation['domain']} ;
    rdfs:range wd:{relation['range']} .
"""
            rdf_relations.append(rdf_entry)
        
        return rdf_prefixes + '\n'.join(rdf_relations)

def main():
    """
    Example usage of the Relation Extractor
    """
    sample_questions = [
        "What is the date of birth of Douglas Noel Adams?",
        "What is the occupation of Douglas Noel Adams?",
        "What is the country of citizenship of Douglas Noel Adams?"
    ]
    
    extractor = RelationExtractor()
    
    # Extract relations
    relations = extractor.extract_relations(' '.join(sample_questions))
    print("Extracted Relations:")
    for relation in relations:
        print(relation)
    
    # Add a custom relation
    extractor.add_custom_relation({
        'relation': 'research_area',
        'description': 'The primary field of research or study',
        'domain': 'Researcher',
        'range': 'Academic Field'
    })
    
    # Save custom relations
    extractor.save_custom_relations('custom_relations.json')
    
    # Format relations in RDF
    rdf_output = extractor.format_relations_for_rdf(relations)
    print("\nRDF Formatted Relations:")
    print(rdf_output)

if __name__ == "__main__":
    main()