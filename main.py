from sklearn.feature_extraction.text import TfidfVectorizer
from alive_progress import alive_bar
from umap import UMAP

import morfeusz2 as morfeusz

import os
import sys

import json


CHUNKS = 1


class DocWithMetadata:
    def __init__(self, title, date, tags, text):
        self.title = title
        self.date = date
        self.tags = tags
        self.text = text

def morf_text(text, blacklist):
    # Remove all invalid utf-8 characters from string
    text = text.replace('�', '')
    out = ""
    analysis = morf.analyse(text)
    
    word = 0
    for i in range(len(analysis)):
        if word == analysis[i][0] and analysis[i][2][1] not in blacklist:
            try:
                out = out + str(analysis[i][2][1]).split(':')[0] + " "
            except:
                print("Error 2: Error analysing data")
            word = word + 1

    return out


def transform_docs(docs, out_file):
    # Perform tf idf on loaded documents
    print("dbg-1")
    tf_idf_result = TfidfVectorizer().fit_transform(docs)

    print("dbg-2")
    # Perform umap on tf idf result
    umap_vectors = UMAP(n_neighbors=2, min_dist=0.3, metric='correlation').fit_transform(tf_idf_result.toarray())

    print("dbg-3")
    # Write umap results to file
    for idx, vector in enumerate(umap_vectors):
        formatetd_doc_title = docs_with_metadata[idx].title.replace('\t', '   ').replace('\n', ' ')
        out_file.write(str(vector[0]) + '\t' + str(vector[1]) + '\t' + formatetd_doc_title + '\n')


# Set up arguments
docs_path = None
metadata_path = None
should_morf_text = True


def switch_args(arg):
    if arg == "no_morph":
        global should_morf_text
        should_morf_text = False
    else:
        print("Unrecognized argument! Ignoring.")

def switch_short_args(arg):
    if arg == "nm":
        global should_morf_text
        should_morf_text = False
    else:
        print("Unrecognized argument! Ignoring.")

# Set up tools
morf = morfeusz.Morfeusz()


args = sys.argv
args.pop(0)
for arg in args:
    if arg.startswith('--'):
        switch_args(arg[2:])
    elif arg.startswith('-'):
        switch_short_args(arg[1:])
    else:
        if docs_path is None:
            docs_path = arg
        else:
            metadata_path = arg

# Read metadata from file
metadate_file = open(metadata_path, 'r', encoding='utf-8')
metadata = json.load(metadate_file)
metadate_file.close()

# Read blacklisted words
blacklist = []
if os.path.exists('blacklist.txt'):
    with open('blacklist.txt', 'r',) as file:
        blacklist = file.read().splitlines()

# Read documents from files by metadata and combine them with metadata
docs = []
docs_with_metadata = []

chunk = 0
chunk_size = int(len(metadata)/CHUNKS)
if os.path.exists('umap_vectors.txt'):
    os.remove('umap_vectors.txt')
out_file = open('umap_vectors.txt', 'a', encoding='utf8')

print("Loadnig data...")
print("Chunk size: " + str(chunk_size))
with alive_bar(len(metadata)) as bar:
    for data in metadata:
        try:
            chunk = chunk + 1
            doc_file = open(docs_path + '/' + data['id'] + '.txt', 'r', encoding='utf-8')
            
            if should_morf_text:
                doc = morf_text(doc_file.read(), blacklist)
            else:
                doc = doc_file.read()

            docs.append(doc)

            doc_title = data['title'] if 'title' in data else 'Unknown'
            doc_date = data['date'] if 'date' in data else 'Unknown'
            doc_tags = data['key'] if 'key' in data else ['Untagged']

            docs_with_metadata.append(DocWithMetadata(doc_title, doc_date, doc_tags, doc))
            doc_file.close()

            if chunk == chunk_size:
                print("Data dump")
                transform_docs(docs, out_file)
                chunk = 0
                docs = []

            bar()

        except OSError:
            print("error 1: Error reading from file")

out_file.close()
