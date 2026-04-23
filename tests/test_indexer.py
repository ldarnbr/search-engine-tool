import unittest
from src.indexer import Indexer

class TestIndexer(unittest.TestCase):

  # Instantiate the indexer before each test
  def setUp(self):
    self.indexer = Indexer()
  
  # Test to make sure input is stripped of capitals and punctuation
  def test_input_sanitation(self):
    self.indexer.add_page("http://test.com", "Foo Bar!! foo.")

    # Expect to see 2 counts of "foo" (punctuation stripped and all to lower)
    foo_check = self.indexer.get_word("foo")
    self.assertEqual(foo_check["http://test.com"]["frequency"], 2)

    # Punctuation should be stripped
    bar_check = self.indexer.get_word("bar")
    self.assertEqual(bar_check["http://test.com"]["frequency"], 1)

  # Test to make sure index is reversed where all URLs are mapped to a common word
  def test_many_urls(self):
    self.indexer.add_page("http://test1.com", "beans are tasty")
    self.indexer.add_page("http://test2.com", "i love beans")

    beans_check = self.indexer.get_word("beans")

    # Both URLs should be present for the word beans
    self.assertIn("http://test1.com", beans_check)
    self.assertIn("http://test2.com", beans_check)

    tasty_check = self.indexer.get_word("tasty")

    # The word tasty should only have test1 URL associated
    self.assertIn("http://test1.com", tasty_check)
    self.assertNotIn("http://test2.com", tasty_check)

  def test_missing_word(self):
    # Test how the application handles a word not yet saved to the index
    self.indexer.add_page("http://example.com", "example text")

    missing_word = self.indexer.get_word("elephants")

    # Expect an empty dictionary which should evaluate to False
    self.assertFalse(missing_word)

if __name__ == '__main__':
  unittest.main(verbosity=2)
