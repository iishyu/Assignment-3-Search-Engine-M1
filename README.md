# Assignment 3 

### Step 1: Creating the Index

Open the terminal in the project's root directory.

Place the DEV file inside the 'data/DEV directory'.


Run:

'''
bash
python src/indexer.py data/DEV
'''


The program then processes the JSON files, extracts/tokenize the text, applies stemming, then creates an inverted index.


The generated index files are then stored in the 'index/' directory:
- docs.json : Maps the document IDs to URLs
- lexicon.json : Stores token locations in the index.
- index.jsonl : Contains inverted index postings.

### Step 2 Starting the Search Interface

After generating the index, run:

'''
bash
python src/search.py
'''

The terminal should display: 

'''
Search Engine Ready!
Type 'exit' to quit. 

Enter query:
''' 



### Step 3: Querying

Type a search query and press Enter.

The search engine will return up to five matching URLs (ranked by relevance scores) 

