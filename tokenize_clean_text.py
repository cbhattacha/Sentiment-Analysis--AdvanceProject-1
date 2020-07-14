# -*- coding: utf-8 -*-
"""
Spyder Editor

Author - Abhieshree Dhami and Chhandosee Bhattacharya
"""
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk import word_tokenize
import inflect
from contractions import contractions_dict
import re
import pandas as pd
import emoji

#nltk.download('averaged_perceptron_tagger')
#nltk.download('sentiwordnet')

# Instantiate the WordNetLemmatizer 
lemmatizer = WordNetLemmatizer()
 

    
#expand contractions. e.g "don't" to "do not"    
def expand_contractions(text, contraction_mapping=contractions_dict):
    
    contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())), 
                                      flags=re.IGNORECASE|re.DOTALL)
    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contraction_mapping.get(match)\
                                if contraction_mapping.get(match)\
                                else contraction_mapping.get(match.lower())                       
        expanded_contraction = first_char+expanded_contraction[1:]
        return expanded_contraction
        
    expanded_text = contractions_pattern.sub(expand_match, text)
    expanded_text = re.sub("'", "", expanded_text)
    return expanded_text

# Define a dictioary of emoticons
dict_emo = { ':-)'  : b'\xf0\x9f\x98\x8a',
                      ':)'   : b'\xf0\x9f\x98\x8a',
                      '=)'   : b'\xf0\x9f\x98\x8a',  # Smile or happy
                     ':-D'  : b'\xf0\x9f\x98\x83',
                      ':D'   : b'\xf0\x9f\x98\x83',
                      '=D'   : b'\xf0\x9f\x98\x83',  # Big smile
                      '>:-(' : b'\xF0\x9F\x98\xA0',
                      '>:-o' : b'\xF0\x9F\x98\xA0'   # Angry face
                      }
#Function converts emoticons to emoji
def convert_emoticons(emoticons):
    emoticons=emoticons.replace('.',' ')
    emoticons=emoticons.replace(',',' ')
    for i in emoticons.split():
        if i in dict_emo.keys():
            word=dict_emo[i].decode('utf-8')
            emoticons=emoticons.replace(i,word)
    return emoticons

#Function to convert emoji to word
def convert_emoji_to_word(emo_converted_text):
    for i in emo_converted_text:
        if i in emoji.UNICODE_EMOJI:
            emo_word=str(emoji.demojize(i))
            rep_colon=emo_word.replace(':',' ')
            rep_dash=rep_colon.replace('_',' ')
            emo_converted_text=emo_converted_text.replace(i,rep_dash)
    return emo_converted_text

#preprocessing the text
def clean_text(review):
    #remove links,username,other hashtags and accronyms
    review=str(review)
    review=re.sub(r"http\S+", "", review)
    review=re.sub(r"#\S+", "",review)
    review=re.sub(r"@\S+", "",review)
    review = re.sub(r"\b[A-Z]{2,}\b", "", review)
    
    emoticons_treated=convert_emoticons(review)
    review=convert_emoji_to_word(emoticons_treated)
    
    review = review.replace("<br />", " ")
    
    #remove contractions
    review = expand_contractions(review)
    
    # Tokenize the article: tokens
    tokens = word_tokenize(review)
    
    # Convert the tokens into lowercase: lower_tokens
    lower_tokens = [t.lower() for t in tokens]
    
    #Convert digits to words
    p = inflect.engine()
    alpha_num_tokens = [p.number_to_words(t) if t.isdigit() else t for t in lower_tokens]
    
    #Remove all punctuations
    alpha_tokens = [t for t in alpha_num_tokens if t.isalpha()]
    
    #Remove all stop words except no and not
    stop_words = stopwords.words('english')
    stop_words.remove('not')
    stop_words.remove('no')
    no_stops = [t for t in alpha_tokens if t not in stop_words]
    
    return no_stops
    