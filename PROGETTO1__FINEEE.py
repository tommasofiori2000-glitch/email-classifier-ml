    # -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 11:32:12 2024
@author: tommy
Last date: 2024-02-06
"""

import os
import re
import json
import datetime
import pandas as pd
import nltk
from nltk.corpus import stopwords
from collections import Counter
#from nltk.tokenize import word_tokenize

# ================= PARAMETERS ===================================
# define data path
#main_folder_path = r"D:\PYTHON_DATA\pr1_6-main\data"
main_folder_path = r"C:\Users\tommaso\Downloads\dataaa\pr1_6-main\data"

# define debug file
debug_file = r"C:\Users\tommaso\Downloads\tms_debug.txt"

# number of most frequent words
N = 2       
# max number of sentences
M = 1000

# --- define 4 groups with their keywords ---
groups = []
group1_keys = ["farm", "industr", "product","prodott"]
group2_keys = ["storage", "memor", "disk", "usb"]
group3_keys = ["net","connect","conness", "computer", "pc", "cable", "cavo", "job"]
group4_keys = ["sysop", "computer","software", "admin", "problem"]

groups.append(group1_keys)
groups.append(group2_keys)
groups.append(group3_keys)
groups.append(group4_keys)

# ---------------------------------
# Load JSON files into a list
# ---------------------------------
def fn_load_json_files(folder_path):
    json_data_list = []

    # Itera tra i file e le sottocartelle nella cartella specificata
    for root, dirs, files in os.walk(folder_path):
        #root è la percorso del file (cartella)
        #dirs non è usato
        #files sono i file nella cartella
        for filename in files:
            if filename.endswith(".json"):
                file_path = os.path.join(root, filename)

                # Apri il file JSON e carica il suo contenuto nella lista
                try:
                    with open(file_path, 'r') as json_file:
                        json_data = json.load(json_file)
                        json_data_list.append(json_data)
                except Exception as e:
                    print(f"Read file error, {filename}: {str(e)}")

    return json_data_list

# ---------------------------------
#  Extract mail body
# ---------------------------------
def fn_mail_body(text):

    # remove all after '>'
    index = text.find('\n>')
    if index >= 0:
        cleaned_text = text[:index] 
    else:
        cleaned_text = text

    # delete last line
    index = cleaned_text.rfind('\n')
    if index >= 0:
        cleaned_text = cleaned_text[:index] 

    # remove '='
    cleaned_text = cleaned_text.replace("\r", "")    
    cleaned_text = cleaned_text.replace("=\n", "")    
    return cleaned_text
    
# ---------------------------------
# Most frequent words extractor
# ---------------------------------
def fn_words_extracion(text, stopwords, n):

    # clean points and numbers
    cleaned_text = re.sub(pattern='[^a-zA-Z]', repl=' ', string=text)

    # create a list
    words_list = cleaned_text.split()  
    
    # remove stop words
    tmp = ' '.join([parola for parola in words_list if parola.lower() not in stopwords])
    words = tmp.split()

    # compute most frequent words
    most_common_words = [word for word, _ in Counter(words).most_common(n)]
    return most_common_words

# ---------------------------------
# Sentences extractor
# ---------------------------------
def fn_sentences_extracion(text):

    # substitute '!'and '?'with '.'
    my_text = text.replace("?", ".")
    my_text = my_text.replace("!", ".")
    sentences = my_text.split(".")
    
    #trim all sentences
    i = 0
    for s in sentences:
        sentences[i] = s.strip()
        i += 1
    
    return sentences

# ---------------------------------
# create summary
# ---------------------------------
def fn_summary(freq_list, sentence_list, m):
    selected_sentences = []
    i = 0
    for sentence in sentence_list:
        if i < m:
            if any(word in sentence for word in freq_list):
                trim_sentence = sentence.strip()
                selected_sentences.append(trim_sentence)    
                selected_sentences.append(".\n")
                i += 1
    s = ''.join([parola for parola in selected_sentences])            
    return s

# ---------------------------------
# assign group: algorthm 1
# ---------------------------------
def fn_group1(freq_list, groups_list):
    # search keywords into freq_list
    s = ""
    idx=0
    for group in groups_list:
        found = 0
        for key in group:
            key_lower = key.lower()
            for fw in freq_list:
               fw_lower =  fw.lower();
               if fw_lower.find(key_lower) == 0:
                    found = idx + 1
                    
        idx += 1
        if found > 0:
          s += str(found)
    
    return s

# ---------------------------------
# assign group: algorthm 2
# ---------------------------------
def fn_group2(text, groups_list):
    s = ""
    # prepare text split
    new_text = text.replace("'", " ")
    new_text = new_text.replace(".", " ")
    new_text = new_text.replace(",", " ")
    new_text = new_text.replace(";", " ")
    new_text = new_text.replace("!", " ")
    new_text = new_text.replace("?", " ")
    new_text = new_text.lower()
    text_list = new_text.split()

    #  counters elaboration
    group_counters = []
    n = 0
    for group in groups_list:
        cnt = 0
        for key in group:
            key_lower = key.lower()
            for word in text_list:
                if word.find(key_lower) == 0:
                   cnt += 1 
             
        group_counters.append(cnt)
        n += 1
    # use maximum rule   
    max = 0
    for i in range(n):
        if max < group_counters[i]:
            max = group_counters[i]
            
    # check null counters
    if max == 0:
        return s
    
    for i in range(n):
        if max == group_counters[i]:
            s += str(i + 1)
    return s

# ---------------------------------
# Debug print
# ---------------------------------
def fn_debug(msg):
    print(str(datetime.datetime.now()) + " " + msg)
    
# ---------------------------------
# MAIN PROGRAM
# ---------------------------------
        
fn_debug("start...")
# Load JSON data
all_json_data = fn_load_json_files(main_folder_path)
fn_debug("data loaded")

# print list size
n=0
for rec in all_json_data:
    n = n + 1
fn_debug(f"list items no.={n}")

# --- prepare DataFrame with pandas
df = pd.DataFrame(all_json_data, dtype="string")
fn_debug("dataframe ready")

# --- prepare stop words
nltk.download('stopwords')
stop_words = set(stopwords.words(['english', 'italian']))

# ---- summary & group elaboration ----------------

# add new columns to the dataframe
df['summary'] = ""
df['group1'] = ""
df['group2'] = ""

f = open(debug_file, "w")
# ---- main loop -----
i = 0
for mail in df['content']:
    subject = df['subject'][i]
    pure_mail = fn_mail_body(mail)
    current_words = fn_words_extracion(pure_mail, stop_words, N)
    current_sentences = fn_sentences_extracion(pure_mail)
    summary = fn_summary(current_words, current_sentences, M)
    group1 = fn_group1(current_words, groups)
    group2 = fn_group2(subject + mail, groups)

    # insert into dataframe    
    df['summary'][i] = summary
    df['group1'][i] = group1
    df['group2'][i] = group2

    i += 1
    f.write(f"---------- Mail n. {i} group(s): {group1}, {group2} \n")    
    #f.write(f"subject: {subject.encode('utf-8')}\n")    
    #f.write(f"current_words: {current_words}\n")    
    #f.write(f"@@@\ncurrent_sentences: {current_sentences}\n")  
    #f.write(f"@@@\n{summary.encode('utf-8')}\n")    
    
f.close()      
fn_debug("elaboration done")


    
