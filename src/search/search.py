from pathlib import Path
from utils import db
import pandas as pd
import spacy
from gensim.models.fasttext import FastText
from rank_bm25 import BM25Okapi
import numpy as np
import pickle
import nmslib

def loadFromDb() -> pd.DataFrame:
    with __builtins__["app"].app_context():
        conn = db.connect()
        return pd.read_sql_query("SELECT * FROM Ingredients", conn)

def fix_text(t):
    return t

def fastTextCreateModel(path, vocab):
    if path.exists():
        raise Exception(str(path) + " exists but is not a regular file")
    ft_model = FastText(
        sg=1, # use skip-gram
        window=10, # only consider 10 tokens either side for context
        min_count=1, # consider all tokens
        negative=15, # who knows
        min_n = 1,
        max_n = 7
    )
    print("Building + training FT model, may take a minute")
    ft_model.build_vocab(vocab)
    ft_model.train(vocab, epochs=6, total_examples=ft_model.corpus_count, total_words=ft_model.corpus_total_words)
    print("Done with FT")
    print("path:", str(path))
    ft_model.save(str(path))

    return ft_model

def fastTextInit(vocab):
    model_path = Path("./_cache/fasttext.model")
    if not model_path.is_file():
        model = fastTextCreateModel(model_path, vocab)
    else:
        model = FastText.load(str(model_path))
    return model

def bm25Create(tok_txt, model, path):
    if path.exists():
        raise Exception(str(path) + " exists but is not a regular file")
    bm25 = BM25Okapi(tok_txt)
    weighted_vectors = []
    for i,item in enumerate(tok_txt):
        item_vect = []
        for word in item:
            vector = model.wv[word]
            weight = (bm25.idf[word] * ((bm25.k1 + 1.0)*bm25.doc_freqs[i][word])) / (bm25.k1 * (1.0 - bm25.b + bm25.b *(bm25.doc_len[i]/bm25.avgdl))+bm25.doc_freqs[i][word])
            weighted_vec = vector*weight
            item_vect.append(weighted_vec)
        item_vect_mean = np.mean(item_vect, axis=0)
        weighted_vectors.append(item_vect_mean)
    pickle.dump(weighted_vectors, open(path, "wb"))

    return weighted_vectors


def bm25Init(tok_txt, model):
    vecs_path = Path("./_cache/weighted_vecs.p")
    if not vecs_path.is_file():
        vecs = bm25Create(tok_txt, model, vecs_path)
    else:
        with open(vecs_path, "rb") as file:
            vecs = pickle.load(file)
    return vecs

def indexCreate(data, path):
    # if path.exists():
        # raise Exception(str(path) + " exists but is not a regular file")
    index = nmslib.init(method="hnsw", space="cosinesimil")
    index.addDataPointBatch(data)
    index.createIndex({'post':2}, print_progress=True)
    # pickle.dump(index, open(path, "wb"))
    return index

# TODO: figure out how to pickle-dump index
def indexInit(data):
    idx_path = Path("./_cache/index.p")
    # if not idx_path.is_file():
    index = indexCreate(data, idx_path)
    # else:
        # with open(idx_path, "rb") as file:
            # index = pickle.load(file)
    return index

class SearchIndex():
    def __init__(self, model, index):
        self.model = model
        self.index = index
    def search(self, text: str):
        txt = text.lower().split()
        query = [self.model.wv[vec] for vec in txt]
        query = np.mean(query, axis=0)
        ids, distances = self.index.knnQuery(query, k=10)
        return zip(ids, distances)

def loadMain():
    print("Loading spacy, might take a minute")
    nlp = spacy.load("en_core_web_sm")
    print("Done loading spacy")
    tok_txt = []
    text = [fix_text(i) for i in list(loadFromDb()["IngredientName"])]
    for item in nlp.pipe(text, disable=["tagger", "parser", "ner"]):
        tok = [t.text for t in item if (t.is_ascii and not t.is_punct and not t.is_space)]
        tok_txt.append(tok)
    model = fastTextInit(tok_txt)
    weighted_vecs = bm25Init(tok_txt, model)
    data = np.vstack(weighted_vecs)
    index = indexInit(data)
    s_index = SearchIndex(model, index)
    return s_index

sindex = loadMain()
