import unittest
from unittest.mock import patch, MagicMock
from src.crawler import Crawler
from src.indexer import Indexer

class TestCrawler(unittest.TestCase):

  def setUp(self):
    self.indexer = Indexer()
    self.crawler = Crawler(self.indexer)

  # Tests crawler successfully gets text
  # Decorator to intercept when crawler.py tries to use requests.get
  @patch('src.crawler.requests.get')
  def test_get_page_successful(self, mock_get):
    # Create a fake successful response
    response = MagicMock()
    response.status_code = 200
    response.text = "<html><head></head><body><h1>hello world</h1></body></html>"
    mock_get.return_value = response

    # Run the crawler (requests.get will be intercepted)
    bsobject = self.crawler.fetch_page("http://test.com")
    
    # The BeautifulSoup object should be created and the HTML text extracted
    self.assertIsNotNone(bsobject)
    self.assertIn("hello world", bsobject.get_text())
  
  # Test to handle get page errors
  @patch('src.crawler.requests.get')
  def test_get_page_404(self, mock_get):
    # Create a fake successful response
    response = MagicMock()
    response.status_code = 404
    mock_get.return_value = response

    # Run the crawler
    bsobject = self.crawler.fetch_page("http://test-fail.com")
    
    # The BeautifulSoup object should not be created and instead return None
    self.assertIsNone(bsobject)

  # Tests that the crawler adds traversed pages
  @patch('src.crawler.requests.get')
  @patch('src.crawler.time.sleep')
  def test_crawl_page(self, mock_sleep, mock_get):
    response = MagicMock()
    response.status_code = 200
    response.text = "<html><head></head><body><h1>hello world</h1></body></html>"
    mock_get.return_value = response

    self.crawler.crawl("http://test.com", max_pages=1)

    # Explored URL's should be added to the seen list
    self.assertIn("http://test.com", self.crawler.visited_pages)

  # Tests that the crawler converts relative links it finds to absolute and adds to the new URL list
  @patch('src.crawler.requests.get')
  @patch('src.crawler.time.sleep')
  def test_converts_relative_url(self, mock_sleep, mock_get):
    response = MagicMock()
    response.status_code = 200
    response.text = '<html><head></head><body><h1><a href="relative">Company Name</a></h1></body></html>'
    mock_get.return_value = response

    self.crawler.crawl("http://test.com", max_pages=1)

    # Explored URL's should be added to the seen list
    self.assertIn("http://test.com/relative", self.crawler.new_pages)

  # Tests that the crawler recursively explores pages
  @patch('src.crawler.requests.get')
  @patch('src.crawler.time.sleep')
  def test_crawler_recursion(self, mock_sleep, mock_get):
    response = MagicMock()
    response.status_code = 200
    response.text = '<html><head></head><body><h1><a href="relative">Company Name</a></h1></body></html>'
    mock_get.return_value = response

    self.crawler.crawl("http://test.com", max_pages=5)

    # Explored URL's should be added to the seen list
    # Mocking serves the same text each time, but the crawler should be robust
    # enough to see that the new href URL is already in the visited pages and quit.
    self.assertIn("http://test.com", self.crawler.visited_pages)
    self.assertIn("http://test.com/relative", self.crawler.visited_pages)

  # Tests the crawler hands the text to the indexer
  @patch('src.crawler.requests.get')
  @patch('src.crawler.time.sleep')
  def test_crawler_sends_to_indexer(self, mock_sleep, mock_get):
    response = MagicMock()
    response.status_code = 200
    response.text = '<html><head></head><body><h1><a href="relative">Company Name</a></h1></body></html>'
    mock_get.return_value = response

    self.crawler.crawl("http://test.com", max_pages=1)

    # Check that the crawler gave the indexer the company word and its associated URL
    company_check = self.indexer.get_word("company")
    self.assertIn("http://test.com", company_check)

if __name__ == '__main__':
  unittest.main()
