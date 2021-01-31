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
from transformers import AutoTokenizer, AutoModelForMaskedLM

tokenizer = AutoTokenizer.from_pretrained("monologg/koelectra-base-v3-generator")  
model = AutoModelForMaskedLM.from_pretrained("monologg/koelectra-base-v3-generator")
uncased = True
model.eval()
if torch.cuda.is_available():
    model.to('cuda')


