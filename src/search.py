import re

class SearchEngine:
  def __init__(self, indexer):
    self.indexer = indexer

  def find(self, phrase):
    cleaned_phrase = re.sub(r'[^\w\s]', '', phrase.lower())
    words = cleaned_phrase.split()

    # Simple check for any valid phrases/words
    if not words:
      return []
    # Stores the lists of all urls for each word
    words_urls = []

    for word in words:
      data = self.indexer.get_word(word)
      if not data:
        # If any of the words aren't found then no URL contains the phrase
        return []
      words_urls.append(data)

      # Sorts the word url lists from smallest to largest. This optimises the 
      # search time by avoiding unnecessary list comparisons (lowest # lookups first)
      words_urls.sort(key=lambda x: len(x))

      # First populate the set with the smallest count of urls to intersect
      # with the other sets of URLs
      matched_url_set = set(words_urls[0].keys())

    for data in words_urls[1:]:
      # Intersect with the next words urls
      next_urls = set(data.keys())
      matched_url_set = matched_url_set.intersection(next_urls)

      # Stop comparing if any dont have an intersection
      if not matched_url_set:
        break
    
    return list(matched_url_set)
