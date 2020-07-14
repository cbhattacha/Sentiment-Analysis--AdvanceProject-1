# -*- coding: utf-8 -*-
"""
Created on Sat May  9 19:15:53 2020

@author: Abhieshree
"""

#Parse the word embedding file
import numpy as np
import os
import pandas as pd
from tokenize_clean_text import clean_text

def generate_embeddings(file_name):
    
    #dict to store word embeddings from glove file
    embeddings_index = {}
    f = open(os.path.join('glove.6B', 'glove.6B.100d.txt'), encoding='utf8')
    for line in f:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        embeddings_index[word] = coefs
    f.close()
    
    print('Found %s word vectors in glove dict' % len(embeddings_index))
    
    
    
    
    #generate a set of unique tokens in entire corpus
    reviews = pd.read_csv(file_name)
    unique_tokens = set()
    for review in reviews['text']:
        unique_tokens.update(clean_text(review))
        
    print("Found %s unique tokens in corpus" % len(unique_tokens))
    
    
    
    # create a dictionary of tokens and their embeddings
    tokens_embeddings_dict = {}
    
    for word in unique_tokens:
        word_vector = embeddings_index.get(word)
        if word_vector is not None:
            tokens_embeddings_dict[word] = word_vector
            
    print("Number of embeddings from corpus generated: %s" % len(tokens_embeddings_dict))
    
    #Generate dataframe from dictionary to export
    # Create dataframe from dic and make keys, index in dataframe
    embeddings_df = pd.DataFrame.from_dict(tokens_embeddings_dict, orient='index')
    embeddings_df.to_csv("project_embeddings.csv")
    
    return None
    
