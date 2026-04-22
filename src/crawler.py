import requests
from bs4 import BeautifulSoup
import time
import random
from urllib.parse import urljoin

"""
Using a class means that the crawler can manage its state, keeping track
of the various pages visited/to visit. Normal Python functions would forget
this context without messy passing of lists back and forth every time functions
are called.
"""
class Crawler:
  def __init__(self, indexer):
    self.indexer = indexer
    self.new_pages = []
    # Need to store visited pages to prevent pages that link back
    # to eachother causing an infinite loop.
    self.visited_pages = set()

  def fetch_page(self, url):
    """
    Requests library gets the HTML content and BeautifulSoup returns this as
    a BS object.
    """
    try:
      response = requests.get(url)
      if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
      else:
        print(f"{response.status_code}: Error when fetching {url}")
    except Exception as e:
      print(f"Error occured fetching {url}: {e}")
      return None
  
  def crawl(self, first_url, max_pages=10):
    """
    Traverse the urls and extract the text.
    """
    self.new_pages.append(first_url)

    # Continue until all new pages are explored
    # Note: Perhaps restrict this to a specific number of travels?
    # would prevent struggles with fictitious resources.
    while self.new_pages and len(self.visited_pages) < max_pages:
      # FIFO ordering of exploration - also pops url off the list
      url = self.new_pages.pop(0)

      # skip past visited pages
      if url in self.visited_pages:
        continue

      print(f"Visiting: {url}")
      content = self.fetch_page(url)

      if content:
        # Extract all text from the page and seperate words by spaces.
        # Also strips all the HTML tags
        page_text = content.get_text(separator=' ', strip=True)
        print(f"Extracted {len(page_text.split())} words.")

        self.indexer.add_page(url, page_text)

        # Extract new pages
        # Looks at all the anchor tags and grabs the associated href
        # relative url
        for link in content.find_all('a'):
          href = link.get('href')

          # Conversion to absolute url
          if href:
            absolute_url = urljoin(url, href)

            if absolute_url not in self.visited_pages and absolute_url not in self.new_pages:
              self.new_pages.append(absolute_url)
         
      self.visited_pages.add(url)

      # Randomise the sleep time to avoid crawler being detected.
      sleep_time = random.uniform(6, 9)
      print(f"Waiting {sleep_time:.2f} seconds for politeness")
      time.sleep(sleep_time)
