from sklearn.feature_extraction.text import TfidfVectorizer
from alive_progress import alive_bar
from umap import UMAP

import fasttext

import morfeusz2 as morfeusz

import os
import sys
import json


class DocWithMetadata:
    def __init__(self, title, date, tags, source, file_name):
        self.title = title
        self.date = date
        self.tags = tags
        self.source = source
        self.file_name = file_name


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


def fast_text():
    print("Mode: FastText")
    ft = fasttext.load_model('cc.pl.300.bin')
    
    fasttext_results = []

    for doc in docs:
        v=ft.get_sentence_vector(doc)
        fasttext_results.append(v)
    
    umap_vectors = UMAP(n_neighbors=10, min_dist=0.1).fit_transform(fasttext_results)
    return umap_vectors


# Perform tf idf on loaded documents
def tf_idf():
    print("Mode: Tf_idf")
    tf_idf_result = TfidfVectorizer(min_df=0.05, max_df=0.95).fit_transform(docs)

    umap_vectors = UMAP(n_neighbors=10, min_dist=0.1, metric='correlation').fit_transform(tf_idf_result.toarray())
    return umap_vectors


# Set up arguments
docs_path = None
metadata_path = None
should_morf_text = True
use_fasttext = False


def switch_args(arg):
    global should_morf_text
    global use_fasttext
    if arg == "no_morph":
        should_morf_text = False
    elif arg == "fasttext":
        use_fasttext = True
    elif arg == "tf_idf":
        use_fasttext = False
    else:
        print("Unrecognized argument! Ignoring.")

def switch_short_args(arg):
    global should_morf_text
    global use_fasttext
    if arg == "nm":
        should_morf_text = False
    elif arg == "ft":
        use_fasttext = True
    elif arg == "ti":
        use_fasttext = False
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

print("Loadnig data...")
with alive_bar(len(metadata)) as bar:
    for data in metadata:
        try:
            bar()
            doc_file = open(docs_path + '/' + data['id'] + '.txt', 'r', encoding='utf-8')
            
            if should_morf_text:
                doc = morf_text(doc_file.read(), blacklist)
            else:
                doc = doc_file.read()

            docs.append(doc)

            doc_title = data['title'] if 'title' in data else 'Unknown'
            doc_date = data['date'] if 'date' in data else 'Unknown'
            doc_tags = data['key'] if 'key' in data else ['Untagged']
            doc_file_name = data['id'] + '.txt'
            if 'source' in data:
                doc_src = data['source']
            elif 'src' in data:
                doc_src = data['src']
            else:
                doc_src = 'Unknown'

            docs_with_metadata.append(DocWithMetadata(doc_title, doc_date, doc_tags, doc_src, doc_file_name))
            doc_file.close()
        except OSError:
            print("error 1: Error reading from file")
        except:
            print("error 2: Generall error")

umap_vectors = []
if use_fasttext: 
    umap_vectors = fast_text()
else:
    umap_vectors = tf_idf()

print("Loaded!")
# print(umap_vectors)

# Write umap results to file
out_file = open('umap_vectors.txt', 'w', encoding='utf8')

for idx, vector in enumerate(umap_vectors):
    formated_doc_title = docs_with_metadata[idx].title.replace('\t', '   ').replace('\n', ' ')
    formated_doc_source = docs_with_metadata[idx].source.replace('\t', '   ').replace('\n', ' ')
    out_file.write(str(vector[0]) + '\t' + str(vector[1]) + '\t' + formated_doc_title + '\t' + formated_doc_source + '\t' + 
                   str(docs_with_metadata[idx].tags) + '\t' + docs_with_metadata[idx].file_name + '\n')

out_file.close()