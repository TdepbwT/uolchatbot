import re
import sys

def main():
  questionwords = []
  answer = input("What is your question?")
  for x in answer.split():
     questionwords.append(x.upper())
  with open("Scraper Text/bannedwords.txt") as bannedwords:
    for s in bannedwords:
      for i in questionwords:
        print(s.strip("\n"))
        while s.strip("\n") in questionwords:
            questionwords.remove(s.strip("\n"))

  print(questionwords)      
  patterns = [r'\b%s\b' % re.escape(s.strip()) for s in questionwords]
  tobesearched = re.compile('|'.join(patterns))

  with open("Scraper Text/bigmergedfile.txt") as f:
    relevantinfofile = open("relevantinfo.txt","w")
    for i, s in enumerate(f):
        if tobesearched.search(s):
            print((s))
            relevantinfofile.write(s)

  print(questionwords)
main()