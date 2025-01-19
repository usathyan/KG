#!/bin/bash

# Create samples directory
mkdir -p samples

# Change to samples directory
cd samples

# Sample PDF
wget https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf

# Sample DOCX
wget https://file-examples.com/storage/fe9b3e5b8ddb5f7d4c4a9a/2017/02/file-sample_100kB.docx

# Sample XLSX
wget https://file-examples.com/storage/fe9b3e5b8ddb5f7d4c4a9a/2017/02/file_example_XLS_10.xls

# Sample text file about a notable person
wget https://raw.githubusercontent.com/datasets/country-codes/master/README.md -O sample_text.md

# Return to original directory
cd ..

# Make the script executable
chmod +x download_samples.sh

echo "Sample documents downloaded successfully!"