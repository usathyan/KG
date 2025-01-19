"""
Ontology Matcher Module

This module is responsible for determining semantic similarity
between properties in an ontology.
"""

from typing import List, Tuple, Dict
import difflib

class OntologyMatcher:
    def __init__(self, similarity_threshold: float = 0.8):
        """
        Initialize the Ontology Matcher with similarity thresholds.
        
        :param similarity_threshold: Minimum similarity score to consider properties similar
        """
        self.similarity_threshold = similarity_threshold
        
        # Predefined semantic equivalence groups
        self.semantic_equivalence = {
            'birth': ['born', 'date of birth', 'birthdate'],
            'death': ['died', 'date of death', 'deathdate'],
            'citizenship': ['nationality', 'country of citizenship', 'origin'],
            'occupation': ['profession', 'job', 'career'],
            'work': ['creation', 'notable work', 'achievement']
        }

    def is_semantically_similar(self, property1: str, property2: str) -> bool:
        """
        Determine if two properties are semantically similar.
        
        :param property1: First property to compare
        :param property2: Second property to compare
        :return: Boolean indicating semantic similarity
        """
        # Normalize properties
        prop1 = property1.lower().strip()
        prop2 = property2.lower().strip()
        
        # Exact match
        if prop1 == prop2:
            return True
        
        # Check semantic equivalence groups
        for group in self.semantic_equivalence.values():
            if prop1 in group and prop2 in group:
                return True
        
        # Use difflib for fuzzy matching
        similarity_ratio = difflib.SequenceMatcher(None, prop1, prop2).ratio()
        
        # Check against similarity threshold
        return similarity_ratio >= self.similarity_threshold

    def find_similar_properties(self, 
                                properties: List[str], 
                                reference_properties: List[str]) -> List[Tuple[str, str]]:
        """
        Find similar properties between two lists.
        
        :param properties: List of properties to match
        :param reference_properties: List of reference properties
        :return: List of tuples of similar properties
        """
        similar_properties = []
        
        for prop1 in properties:
            for prop2 in reference_properties:
                if self.is_semantically_similar(prop1, prop2):
                    similar_properties.append((prop1, prop2))
        
        return similar_properties

    def match_relations(self, relations: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Match and potentially refine extracted relations.
        
        :param relations: List of extracted relations
        :return: List of matched and potentially refined relations
        """
        matched_relations = []
        
        for relation in relations:
            # Attempt to find a more precise or standardized version of the relation
            refined_relation = relation.copy()
            
            # Check if the relation can be mapped to a more standard form
            for semantic_group, variants in self.semantic_equivalence.items():
                if relation['relation'] in variants:
                    # Use the first (most standard) variant as the refined relation
                    refined_relation['relation'] = semantic_group
                    break
            
            matched_relations.append(refined_relation)
        
        return matched_relations

    def generate_ontology_mapping(self,
                                  source_properties: List[str],
                                  target_ontology: List[str]) -> dict:
        """
        Generate a mapping between source properties and target ontology.
        
        :param source_properties: Properties to be mapped
        :param target_ontology: Target ontology properties
        :return: Dictionary mapping source to target properties
        """
        ontology_mapping = {}
        
        for source_prop in source_properties:
            best_match = None
            best_similarity = 0
            
            for target_prop in target_ontology:
                similarity = difflib.SequenceMatcher(
                    None,
                    source_prop.lower(),
                    target_prop.lower()
                ).ratio()
                
                if similarity > best_similarity and similarity >= self.similarity_threshold:
                    best_match = target_prop
                    best_similarity = similarity
            
            if best_match:
                ontology_mapping[source_prop] = best_match
        
        return ontology_mapping

def main():
    """
    Example usage of the Ontology Matcher
    """
    matcher = OntologyMatcher()
    
    # Example property similarity checks
    test_cases = [
        ('date of birth', 'birthdate'),
        ('occupation', 'profession'),
        ('country of citizenship', 'nationality')
    ]
    
    print("Semantic Similarity Test Cases:")
    for prop1, prop2 in test_cases:
        similar = matcher.is_semantically_similar(prop1, prop2)
        print(f"{prop1} <-> {prop2}: {similar}")
    
    # Ontology mapping example
    source_props = ['birth date', 'job', 'nationality']
    target_ontology = ['dateOfBirth', 'occupation', 'countryOfCitizenship']
    
    mapping = matcher.generate_ontology_mapping(source_props, target_ontology)
    print("\nOntology Mapping:")
    for source, target in mapping.items():
        print(f"{source} -> {target}")

if __name__ == "__main__":
    main()