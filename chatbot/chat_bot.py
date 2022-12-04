# # -*- coding: utf-8 -*-
#
#
# import json
# # if you are using python 3, you should
# import urllib
# import urllib.request
# import urllib.parse
# from googletrans import Translator
#
# translator = Translator()
# model_name = 'BM25'
#
#
# def translate_and_get_query(text):
#     lang_code = translator.detect(text).lang
#     if lang_code == 'en':
#         text_en = text
#         text_ru = translator.translate(text, src=lang_code, dest='ru').text
#         text_de = translator.translate(text, src=lang_code, dest='de').text
#     elif lang_code == 'de':
#         text_de = text
#         text_en = translator.translate(text, src=lang_code, dest='en').text
#         text_ru = translator.translate(text, src=lang_code, dest='ru').text
#     else:
#         text_ru = text
#         text_en = translator.translate(text, src=lang_code, dest='en').text
#         text_de = translator.translate(text, src=lang_code, dest='de').text
#     return [text_en, text_ru, text_de], lang_code
#
#
# def parser():
#     with open('test-queries.txt', encoding="utf-8") as f:
#         index = 1
#         for line in f.readlines():
#             query = line.split(' ', 1)
#             query[1] = query[1].strip()
#             query[1] = query[1].replace(":", "")
#             translated_query, lang_code = translate_and_get_query(query[1])
#             if lang_code == 'en':
#                 final_query = "text_en:(%s)^1.62 OR text_ru:(%s)^0.5 OR text_de:(%s)^0.8" % (
#                     translated_query[0], translated_query[1]
#                     , translated_query[2])
#             elif lang_code == 'ru':
#                 final_query = "text_en:(%s)^1.33 OR text_ru:(%s)^1.62 OR text_de:(%s)^0.4" % (
#                     translated_query[0], translated_query[1]
#                     , translated_query[2])
#             else:
#                 final_query = "text_en:(%s)^1.33 OR text_ru:(%s)^0.5 OR text_de:(%s)^1.62" % (
#                     translated_query[0], translated_query[1]
#                     , translated_query[2])
#             print(final_query)
#             dictionary = {"q": final_query}
#             encoded_query = urllib.parse.urlencode(dictionary)
#             print(encoded_query)
#             qid = query[0]
#             ir_model = model_name
#             inurl = 'http://104.196.61.19:8983/solr/' + ir_model + '/select?' + encoded_query + '&fl=id%2Cscore&wt=json&indent=true&rows=20'
#             print(inurl)
#             data = urllib.request.urlopen(inurl)
#             docs = json.load(data)['response']['docs']
#             rank = 0
#             outfn = model_name + '/%d.txt' % index
#             outf = open(outfn, 'w')
#             print(outfn)
#             for doc in docs:
#                 outf.write(qid + ' ' + 'Q0' + ' ' + str(doc['id']) + ' ' + str(rank) + ' ' + str(
#                     doc['score']) + ' ' + ir_model + '\n')
#                 rank += 1
#             index += 1
#         outf.close()
#         f.close()
#
#
# parser()

'''
@author: Harshith Pokala Muni
Institute: University at Buffalo
'''

from tqdm import tqdm
import json

import urllib
import urllib.request
import urllib.parse
import argparse
from flask import Flask
from flask import request
import hashlib

app = Flask(__name__)
ir_model = 'mycol1'



@app.route("/bot", methods=['POST'])
def execute_query():
    """ This function handles the POST request to your endpoint.
        Do NOT change it."""
    topic_name = request.args.get('topic')
    query = request.args.get('query')
    solr_query = "text:(%s)" % query
    query_dictionary = {"q": solr_query}
    encoded_solr_query = urllib.parse.urlencode(query_dictionary)

    solr_url = 'http://104.196.61.19:8983/solr/' + ir_model + '/select?' + encoded_solr_query + '&fl=message_id%2Ctext%2Cscore&wt=json&indent' \
                                                                                     '=true&rows=1 '
    print(solr_url)
    query_result = urllib.request.urlopen(solr_url)

    query_docs = json.load(query_result)['response']['docs'][0]
    message_id = query_docs['message_id'][0]

    solr_response_query = "parent_message_id:\"%s\"" % message_id
    response_dictionary = {"q": solr_response_query}
    encoded_solr_response_query = urllib.parse.urlencode(response_dictionary)
    solr_response_url = 'http://104.196.61.19:8983/solr/' + ir_model + '/select?' + encoded_solr_response_query + '&fl=message_id%2Ctext%2Cscore&wt=json&indent' \
                                                                                                '=true&rows=1 '
    response_result = urllib.request.urlopen(solr_response_url)
    response_docs = json.load(response_result)['response']['docs'][0]
    return response_docs['text'][0]

if __name__ == "__main__":
    """ Driver code for the project, which defines the global variables.
        Do NOT change it."""
    app.run(host="0.0.0.0", port=9999)
