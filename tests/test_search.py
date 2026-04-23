import unittest
from src.indexer import Indexer
from src.search import SearchEngine

class TestSearchEngine(unittest.TestCase):

  def setUp(self):
    # Populate a new Indexer
    self.indexer = Indexer()
    self.indexer.add_page("http://frogs.com", "frogs can hop high")
    self.indexer.add_page("http://dragonflys.com", "dragonflys hover for hours")
    self.indexer.add_page("http://tadpoles.com", "tadpoles are slimy")
    self.indexer.add_page("http://lilypads.com", "baby ducks can walk on these")

    # Instantiate the search engine with the indexer
    self.search_engine = SearchEngine(self.indexer)
  
  def test_one_argument(self):
    # Tests that searching for a single word returns the correct pages
    results = self.search_engine.find("can")
    self.assertIn("http://frogs.com", results)
    self.assertIn("http://lilypads.com", results)
    self.assertEqual(len(results), 2)

  def test_multiple_arguments(self):
    # Tests that searching for multiple words returns the correct pages
    results1 = self.search_engine.find("hover for hours")
    self.assertIn("http://dragonflys.com", results1)
    self.assertEqual(len(results1), 1)

    # Also check that phrase word order doesn't matter
    results2 = self.search_engine.find("hours hover for")
    self.assertIn("http://dragonflys.com", results2)
    self.assertEqual(len(results2), 1)

  def test_missing_word(self):
    # Tests a search for a word not found in any URL (Expect an empty list)
    results = self.search_engine.find("hello")
    self.assertEqual(results, [])
  
  def test_no_argument(self):
    # Tests that providing no argument just returns an empty list
    results = self.search_engine.find("")
    self.assertEqual(results, [])
  
  def test_invalid_argument(self):
    # Tests that providing invalid arguments (punctuation or whitespace) just returns an empty list
    results = self.search_engine.find(" ,!? ")
    self.assertEqual(results, [])
  
  def test_punctuation_in_argument(self):
    # Tests that arguments containing punctuation and words are cleaned and searched for
    results = self.search_engine.find("frogs!!,.")
    self.assertIn("http://frogs.com", results)
  
if __name__ == '__main__':
  unittest.main()
