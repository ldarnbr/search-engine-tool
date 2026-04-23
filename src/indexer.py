import json
import os
import re
from collections import defaultdict

class Indexer:
  def __init__(self, file_path="data/index.json"):
    """
    defaultdict ensures that when we lookup a word thats not already in the
    dictionary, it won't return a KeyError and instead will build a nested 
    structure for it in the format:

    self.index[word][url] = {"frequency": count, "positions": [pos1, pos2]}

    """
    self.file_path = file_path

    # Creates an empty structure, and applies it to URLs and Words even if they
    # dont exist yet in the index.

    # Level 3: lambda: {"frequency": 0, "positions": []}
    # Level 2: defaultdict(lambda: {"frequency": 0, "positions": []})
    # Level 1: self.index = defaultdict(lambda: defaultdict(...))
    self.index = defaultdict(lambda: defaultdict(lambda: {"frequency": 0, "positions": []}))

  def add_page(self, url, text):
    """
    Builds the reverse index by recording frequency and word position stats.

    """
    text = text.lower()

    # Regular expression to remove non word characters
    nopunc_text = re.sub(r'[^\w\s]', '', text)

    # Gets an array of the whitespace seperated words
    words = nopunc_text.split()

    for position, word in enumerate(words):

      # The defaultdict lambda functions will build the structure if not already
      # present for this word/url combination. Otherwise, store the position
      # and increment frequency count.
      self.index[word][url]["frequency"] += 1
      self.index[word][url]["positions"].append(position)

  def save(self):
    """
    Saves the index to a file in JSON format.
    """
    # Checks that index.json exists already before trying to save
    os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    # Writes the index to the file with some formatting for readability
    with open(self.file_path, 'w', encoding='utf-8') as f:
      json.dump(self.index, f, indent=4)
    
    print(f"Inverted index saved")
  
  def load(self):
    """
    Loads the saved index and rebuilds the dictionary with the defaultdict rules.
    """

    # Handles case where file doesn't exist yet.
    if not os.path.exists(self.file_path):
      print(f"No index file {self.file_path} found.")
      return False
    
    with open(self.file_path, 'r', encoding='utf-8') as f:
      loaded_dict = json.load(f)
    
    # Start with a fresh index defaultdict to reinstate the lambda 'rules'
    self.index = defaultdict(lambda: defaultdict(lambda: {"frequency": 0, "positions": []}))

    # Feed the saved index data into the defaultdict type index
    for word, urls in loaded_dict.items():
      for url, statistics in urls.items():
        self.index[word][url] = statistics
    
    print(f"Loaded index from {self.file_path}")
    return True

  def get_word(self, word):
    """
    Gets all the stats for a specific word in dict format. If a word isn't found
    we prevent the lambda functions from building a new structure by just
    immediately returning an empty dictionary.
    """

    word = word.lower()
    if word in self.index:
      return self.index[word]
    else:
      return {}