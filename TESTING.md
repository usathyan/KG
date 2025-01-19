# Knowledge Graph Generation - Testing Guide

## Prerequisites

1. Ensure Poetry is installed
2. Install project dependencies:
   ```
   poetry install
   ```

3. Download spaCy language model:
   ```
   poetry run python -m spacy download en_core_web_sm
   ```

4. Install additional text extraction dependencies:
   ```
   poetry run pip install textract
   ```

## Downloading Sample Documents

Run the download script to get sample documents:
```
chmod +x download_samples.sh
./download_samples.sh
```

## Running Tests

To test Knowledge Graph Generation on sample documents:
```
poetry run python test_kg_generation.py
```

### Expected Outputs

The script will:
- Process each sample document
- Generate Competency Questions
- Extract Relations
- Create Knowledge Graphs
- Save Knowledge Graphs as .ttl files in the samples directory

## Troubleshooting

- Ensure all dependencies are installed
- Check that sample documents are downloaded
- Verify Python and Poetry versions are compatible

### Common Issues

1. **Missing Dependencies**
   - Reinstall dependencies
   - Check Python version

2. **Text Extraction Failures**
   - Some document formats may have limited extraction capabilities
   - Not all documents will generate meaningful knowledge graphs

## Sample Document Types

- PDF
- DOCX
- XLSX
- Markdown

## Customization

Modify `test_kg_generation.py` to:
- Add more sample documents
- Adjust knowledge graph generation parameters
- Implement more detailed testing