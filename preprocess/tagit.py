import glob
import json
import math
import re

class Classifier:
    patterns = []
    keywords = []

    def __init__(self):
        for pattern in open("patterns.txt").read().split("\n"):
            pattern = re.sub(r'/ #.*$/', '', pattern)
            splitted = pattern.rsplit(',', 1)
            print(splitted)
            if len(splitted) == 2:
                regexp, category = splitted
                regexp = re.search(r'\/(.*)\/', regexp).group(1)
                category = re.search(r'\'(.*)\'', category).group(1)
                self.patterns.append({'category': category, 'regexp': r'\b{0}\b'.format(regexp)})
        for line in open('keywords.regexp').read().split("\n"):
            if line != '':
                self.keywords.append(r'%s' % line)


    def run(self, text):
        categories = []
        for pattern in self.patterns:
            if re.search(pattern['regexp'], text, re.IGNORECASE):
                categories.append(pattern['category'])
        return categories

    def features_vec(self, text):
        keywords_vec = []
        regexp_vec   = []
        sizes_vec    = [
            min([1, math.log(len(text),10)/10]),
            min([1, math.log(len(re.split(r'\s+', text)),10)/10]),
            min([1, math.log(len(re.split(r'\n\s\n', text)),10)/10])
        ]
        for k in self.keywords:
            keywords_vec.append(1 if re.search(k, text, re.IGNORECASE) else 0)
        for p in self.patterns:
            regexp_vec.append(1 if re.search(p['regexp'], text, re.IGNORECASE) else 0)
        return keywords_vec + regexp_vec + sizes_vec


def get_categories(id, title, text):
    print("=" * 80)
    categories = set(c.run(text))
    print("###{0}:{1}".format(id, ','.join(categories)))
    print("")
    print(categories)
    print("")
    print(text)

def process():
  c = Classifier()

  # print(len(c.patterns))

  titles = json.load(open("../titles.id.txt"))

  for fname in glob.glob("../data/*/*.txt"):
      id = re.search(r'\d+\/(\d+)\.txt', fname).group(1)
      title = titles[id] # fails when not found
      body = open(fname).read()
      content = '\n'.join([title, body])
      #get_categories(id, title, content)
      print(c.features_vec(content)) #.unshift(id).join(',')

# run when directly called
if __name__ == '__main__':
    process()
