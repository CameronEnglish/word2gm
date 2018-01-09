import nltk
import string
import sys
from nltk.corpus import stopwords

# run once for each file you wish to change, update input/output names accordingly

# takes first argument as infile path
inFilePath = sys.argv[1]
reader = open(inFilePath, 'r')
# change this to the filepath of your output with desired name; if no file is already there it will make it
outFilePath = sys.argv[2]
target = open(outFilePath, 'w')

stop_words = {'the', 'a', 'and', 'but', 'it', 's', 'd', 'to', 'for', 'of', 'like', 'he', 'she', 'is', 'are', '?', '(', ')', 'i', 'we', '\\', '\'', ',', ',', '`', '\'s', '``', '\'\'', '[', ']', '{', '}', '-', '^', ';', '_', '+', ':'}

for line in reader:
    tokens = nltk.word_tokenize(line)
    tokens = [t.lower() for t in tokens]
    cleaned_tokens = filter(lambda x: x not in stop_words, tokens)
    output = (" ".join(map(str, cleaned_tokens)))
    output = output.strip('"`\'')
    output = ''.join([i for i in output if not i.isdigit()])
    output = output.replace("\\","")
    output = output.replace("^","")
    output = output.replace("_","")
    output = output.replace(",","")
    output = output.replace(".","")
    output = output.replace("=","")
    output = output.replace("\"","")
    target.write(" " +output)
    

target.close()
