from sklearn.feature_extraction.text import TfidfVectorizer
from umap import UMAP
import os, sys
import json

class DocWithMetadata:
    def __init__(self, title, date, tags, text):
        self.title = title
        self.date = date
        self.tags = tags
        self.text = text

# Read script args
docs_path = sys.argv[1]
metadata_path = sys.argv[2]

# Read metadata from file
metadate_file = open(metadata_path, 'r', encoding='utf-8')
metadata = json.load(metadate_file)
metadate_file.close()

# Read documents from files by metadata and combine them with metadata
docs = []
docs_with_metadata = []

for data in metadata:
    try:
        doc_file = open(docs_path + '/' + data['id'] + '.txt', 'r', encoding='utf8')
        doc = doc_file.read()
        docs.append(doc)

        doc_title = data['title'] if 'title' in data else 'Unknown'
        doc_date = data['date'] if 'date' in data else 'Unknown'
        doc_tags = data['key'] if 'key' in data else ['Untagged']

        docs_with_metadata.append(DocWithMetadata(doc_title, doc_date, doc_tags, doc))
        doc_file.close()
    except:
        pass

# Perform tf idf on loaded documents
tf_idf_result = TfidfVectorizer().fit_transform(docs)

# Perform umap on tf idf result
umap_vectors = UMAP(n_neighbors=2, min_dist=0.3, metric='correlation').fit_transform(tf_idf_result.toarray())

# Write umap results to file
out_file = open('umap_vectors.txt', 'w', encoding='utf8')

for idx, vector in enumerate(umap_vectors):
    formatetd_doc_title = docs_with_metadata[idx].title.replace('\t', '   ').replace('\n', ' ')
    out_file.write(str(vector[0]) + '\t' + str(vector[1]) + '\t' + formatetd_doc_title + '\n')

out_file.close()