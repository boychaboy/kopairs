import os
import json
import sys
import urllib.request
import argparse
import requests
import csv

def google_api(sent):
    from google.cloud import translate_v2 as translate
    # import ipdb; ipdb.set_trace(context=10)
    client = translate.Client()
    result = client.translate(sent, target_language='ko')
    return result['translatedText']

def papago_api(sent):
    client_id = "Y7T7GdECJTVDbx6T7N4d" # 개발자센터에서 발급받은 Client ID 값
    client_secret = "pVTbnwk6GH" # 개발자센터에서 발급받은 Client Secret 값
    encText = urllib.parse.quote(sent)
    data = "source=en&target=ko&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        text= response_body.decode('utf-8')
    else:
        print("Error Code:" + rescode)
    translated_text = json.loads(text)['message']['result']['translatedText']
    return translated_text

def translate(args):
    """
    Translate a CrowS-Paris dataset into Korean
    """

    print("Translating : ")
    print(f"Input : {args.input_file}")
    print(f"Output : {args.output_file}")

    f = open(args.input_file, 'r')
    w = open(args.output_file, 'w')
    
    reader = csv.DictReader(f)
    w.write(",sent_more, sent_less, stereo_antistereo, bias_type\n")
    idx = 0
    for row in reader:
        direction = row['stereo_antistereo']
        bias_type = row['bias_type']

        sent1, sent2 = '', ''
        if direction == 'stereo':
            sent1 = row['sent_more']
            sent2 = row['sent_less']
        else:
            sent1 = row['sent_less']
            sent2 = row['sent_more']
        if bias_type == 'gender':
            bias_type_kr = '성별'
        elif bias_type == 'disability':
            bias_type_kr = '장애'
        elif bias_type == 'sexual-orientation':
            bias_type_kr = '성적지향'
        elif bias_type == 'age':
            bias_type_kr = '나이'
        else:
            continue

        # sent1 = papago_api(sent1)
        # sent2 = papago_api(sent2)
        kr_sent1 = google_api(sent1)
        kr_sent2 = google_api(sent2)
        print(idx)
        print(f"{sent1}\n{sent2}")
        print(f"{kr_sent1}\n{kr_sent2}\n")
        w.write(f'{idx},"{kr_sent1}","{kr_sent2}",stereo,{bias_type}\n')
        idx += 1
    f.close()
    w.close()

parser = argparse.ArgumentParser()
parser.add_argument('--input_file', default='./data/crows_pairs_anonymized.csv')
parser.add_argument('--output_file', default='./data/crows_paris_korean.txt')
args = parser.parse_args()
translate(args)

