import sys
from crawler import Crawler
from indexer import Indexer
from search import SearchEngine

def main():
  indexer = Indexer()
  search_engine = SearchEngine(indexer)
  print("Welcome to the web crawler interface. Please run the 'build' command.")

  while True:
    # Splits off the first command word e.g. "find"
    user_input = input("\n>").strip().split(maxsplit=1)

    if not user_input:
      continue

    # Capture the argument if there is one, otherwise argument is blank
    command = user_input[0].lower()
    if len(user_input) > 1:
      argument = user_input[1]
    else:
      argument = ""

    if command == 'load':
      if argument:
        print("Error: the 'load' command takes no arguments.")
      else:
        indexer.load()
        print("Index loaded")

    elif command == 'build':
      if argument:
        print("Error: the 'build' command takes no arguments.")
      else:
        crawler = Crawler(indexer)
        crawler.crawl('https://quotes.toscrape.com/')
        indexer.save()
        print("Build completed successfully")

    elif command == 'print':
      if argument:
        data = indexer.get_word(argument)
        print(f"Data for '{argument}': {data}")
      else:
        print("Please provide a word to grab statistics for: print <word>")

    elif command == 'find':
      if argument: 
        results = search_engine.find(argument)
        print(f"Found {len(results)} matching pages:")
        for url in results:
          print(f" - {url}")
      else:
        print("Please provide a word or phrase to see a list of urls where they occur.")

    else:
      print("Command not valid. Available commands: build, load, print, find.")

if __name__ == "__main__":
  main()
