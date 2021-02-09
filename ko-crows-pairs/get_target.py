import os
import csv
import json
import math
import torch
import argparse
import difflib
import logging
import numpy as np
import pandas as pd
import nltk

from transformers import BertTokenizer, BertForMaskedLM
from transformers import AlbertTokenizer, AlbertForMaskedLM
from transformers import RobertaTokenizer, RobertaForMaskedLM
from collections import defaultdict
from tqdm import tqdm
#bcb
from transformers import AutoTokenizer, AutoModelForMaskedLM


def read_data(input_file):
    """
    Load data into pandas DataFrame format.
    """
    
    df_data = pd.DataFrame(columns=['sent1', 'sent2', 'direction', 'bias_type'])

    with open(input_file) as f:
        reader = csv.DictReader(f)
        # import ipdb; ipdb.set_trace(context=10)
        for row in reader:
            direction, gold_bias = '_', '_'
            direction = row['stereo_antistereo']
            bias_type = row['bias_type']

            sent1, sent2 = '', ''
            if direction == 'stereo':
                sent1 = row['sent_more']
                sent2 = row['sent_less']
            else:
                sent1 = row['sent_less']
                sent2 = row['sent_more']

            df_item = {'sent1': sent1,
                       'sent2': sent2,
                       'direction': direction,
                       'bias_type': bias_type}
            df_data = df_data.append(df_item, ignore_index=True)

    return df_data

parser = argparse.ArgumentParser()
parser.add_argument("--input_file", type=str, help="path to input file")
parser.add_argument("--output_file", type=str, help="path to output file with targets")
args = parser.parse_args()
df_data = read_data(args.input_file)

target1 = dict()
target2 = dict()
f = open(args.output_file+'.txt', 'w')
f1 = open(args.output_file+'_1.txt', 'w')
f2 = open(args.output_file+'_2.txt', 'w')
ff = open(args.output_file+'_aug.txt', 'w')
f3 = open('crows_pairs.txt', 'w')
for index, data in df_data.iterrows():
    sent1 = nltk.word_tokenize(data['sent1'])
    sent2 = nltk.word_tokenize(data['sent2'])
    set1 = set(sent1)
    set2 = set(sent2)
    intersec = set1 & set2
    set1 = set1 - intersec
    set2 = set2 - intersec
    if data['bias_type'] not in target1.keys():
        target1[data['bias_type']] = set()
        target2[data['bias_type']] = set()
    target1[data['bias_type']] = target1[data['bias_type']].union(set1)
    target2[data['bias_type']] = target2[data['bias_type']].union(set2)
    sent1 = data['sent1']
    sent2 = data['sent2']
    for s in set1:
        f.write(s + ' ')
        sent1 = sent1.replace(s, '['+s+']')
    f.write(', ')
    for s in set2:
        f.write(s + ' ')
        sent2 = sent2.replace(s, '['+s+']')
    f.write(f"| {data['bias_type']}\n")
    f3.write('*'+data['bias_type']+'*'+'\n'+sent1+'\n'+sent2+'\n\n')


# import ipdb; ipdb.set_trace(context=10)
for key in target1.keys():
    f1.write(key)
    f1.write("\n----------\n")
    f2.write(key)
    f2.write("\n----------\n")
    for t1, t2 in zip(target1[key], target2[key]):
        f1.write(t1+'\n')
        f2.write(t2+'\n')
    f1.write("\n")
    f2.write("\n")
f.close()
f1.close()
f2.close()
