# Knowledge Graph Generator

## Overview

This project implements a Knowledge Graph Generation system that can extract semantic relationships and create RDF-based knowledge graphs from unstructured text documents.

## Features

- Competency Question Generation
- Relation Extraction
- Ontology Matching
- Knowledge Graph Construction
- RDF Serialization
- Dynamic Entity Configuration

## Prerequisites

- Python 3.8+
- Poetry (Python dependency management)

## Installation

1. Clone the repository
2. Install Poetry (if not already installed):
   ```
   pip install poetry
   ```

3. Install project dependencies:
   ```
   poetry install
   ```

4. Download spaCy language model:
   ```
   poetry run python -m spacy download en_core_web_sm
   ```

## Usage

Generate a knowledge graph from a text file:

```bash
poetry run python -m src.main input_document.txt
```

### Command Line Options

- `input_file`: Path to the input text file (required)
- `--max-questions`: Maximum number of competency questions to generate (default: 3)
- `--output-format`: Output format for the knowledge graph (choices: turtle, xml, json-ld, default: turtle)

Example:
```bash
poetry run python -m src.main document.txt --max-questions 5 --output-format json-ld
```

## Dynamic Entity Configuration

The project now supports dynamic entity configuration through a JSON file:

### Configuring Custom Entities

1. Create or modify `entity_config.json`:
```json
{
    "research_area": {
        "description": "The primary field of research or study",
        "domain": "Researcher",
        "range": "Academic Field"
    },
    "academic_institution": {
        "description": "The primary academic institution associated with an individual",
        "domain": "Researcher", 
        "range": "Institution"
    }
}
```

2. Use in code:
```python
from src.relation_extractor import RelationExtractor

# Load relations from a JSON file
extractor = RelationExtractor('entity_config.json')

# Add a new custom relation dynamically
extractor.add_custom_relation({
    'relation': 'research_project',
    'description': 'A significant research project',
    'domain': 'Researcher',
    'range': 'Research Project'
})

# Save custom relations to a file
extractor.save_custom_relations('updated_entity_config.json')
```

## Project Structure

- `src/`
  - `main.py`: Main orchestration script
  - `cq_generator.py`: Competency Question Generation
  - `relation_extractor.py`: Relation Extraction
  - `ontology_matcher.py`: Ontology Matching
  - `kg_builder.py`: Knowledge Graph Construction
- `entity_config.json`: Custom entity configuration file

## Development

### Running Tests

```bash
poetry run pytest
```

### Code Formatting

```bash
poetry run black .
poetry run isort .
```

### Type Checking

```bash
poetry run mypy .
```

## Dependencies

- spaCy: NLP processing
- RDFLib: RDF graph manipulation
- Poetry: Dependency management

## Roadmap

- [x] Add dynamic entity configuration
- [ ] Improve Named Entity Recognition
- [ ] Add more sophisticated relation extraction
- [ ] Support multiple input document formats
- [ ] Enhance ontology matching capabilities

## License

[Specify your license here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.