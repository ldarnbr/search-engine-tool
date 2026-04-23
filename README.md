# Python Web Crawler Tool

## Project Overview and Purpose

This project is an interactive command line tool which allows a user to crawl web pages
to locate specific search terms/phrases. It recursively explores all URL's from a given
start point to build an inverted index list of URL's associated to each unique word. The exact
position of the search word(s) in each URL is also recorded, allowing a user to precisely locate their word on the page. The crawler adheres to a minimum 6 second politeness window to reduce
network load with variable sleep timers to decrease the likelihood of detection.

## Installation and Setup

1. Clone the repository to your local machine.
```bash
git clone https://github.com/ldarnbr/search-engine-tool.git
```
2. Create a virtual environment to store project dependencies.
```bash
python -m venv venv
```
3. Activate the environment.
```bash
# Windows
venv/Scripts/Activate

# Mac/Linux
source venv/bin/activate
```
4. Install all dependencies.
```bash
pip install -r requirements.txt
```
4. Run the interface.
```bash
python main.py
```

## Usage Commands
* **'build'**: 

  This command should always be given first. This starts the web crawler which visits the default targeted website, extracts all the text at the URL and builds an inverted index. The crawler will observe the politeness sleep timer, so this step is controlled by the max_pages parameter in crawler.py. This restricts the crawler to a maximum recursion of URL's which is defensive against fictituous resources, but also your own precious time! The results are stored in ./data/index.json.

* **'load'**: 

  This command should always given after the build. It loads the saved index into memory from the JSON file, allowing for searches in the saved library rather than recrawling the website.

* **'print <word>'**: 

  This looks up a word in the index and prints the stats (frequency and positions across each URL). Usage example: print hello

* **'find <phrase>'**:

  This searches the index for word(s). If multiple words are provided then only URL's containing all of the words in the query, regardless of their position. This means the search isn't restricted to just the exact ordering of the phrase. e.g. "find hello world" should return the same result as "find world hello".

## Testing
Unit tests are provided in the tests directory for the Crawler, Indexer and Search Engine. The tests mock all network requests so is not dependant on any external website.

To run each test individually, use the following commands:
```bash
python -m unittest -b tests/test_indexer.py
python -m unittest -b tests/test_search.py
python -m unittest -b tests/test_crawler.py
```
*For verbose messages in the console for each of the tests, include the -v flag.*