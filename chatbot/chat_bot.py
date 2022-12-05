'''
@author: Harshith Pokala Muni
Institute: University at Buffalo
'''

import json

import urllib
import urllib.request
import urllib.parse
from flask import request
from similarity import classifier
from flask import Flask
from flask_cors import cross_origin

app = Flask(__name__)
ir_model = 'mycol1'
reddit_ir_model = 'reddit'
similarity_classifier = classifier()


def get_top_5_chit_chat_query_matches(query):
    solr_query = "text:(%s)" % query
    query_dictionary = {"q": solr_query}
    encoded_solr_query = urllib.parse.urlencode(query_dictionary)

    solr_url = 'http://104.196.61.19:8983/solr/' + ir_model + '/select?' + encoded_solr_query + '&fl=message_id%2Ctext%2Cscore&wt=json&indent' \
                                                                                                '=true&rows=5'
    print(solr_url)
    query_result = urllib.request.urlopen(solr_url)

    return json.load(query_result)['response']['docs']


def get_top_10_chit_chat_answers(solr_response_query):
    # solr_response_query = "parent_message_id:\"%s\"" % message_id
    response_dictionary = {"q": solr_response_query}
    encoded_solr_response_query = urllib.parse.urlencode(response_dictionary)
    solr_response_url = 'http://104.196.61.19:8983/solr/' + ir_model + '/select?' + encoded_solr_response_query + '&fl=text%2Cscore&wt=json&indent' \
                                                                                                                  '=true&rows=10 '
    response_result = urllib.request.urlopen(solr_response_url)
    return json.load(response_result)['response']['docs']


def get_top_5_topic_query_matches(topic, query):
    solr_query = "selftext:(%s)" % query
    topic_query_dictionary = {"q": solr_query}
    encoded_solr_query = urllib.parse.urlencode(topic_query_dictionary)
    facet_query = urllib.parse.urlencode({"facet.query": "topic:\"%s\"" % topic})
    solr_url = 'http://35.222.156.17:8983/solr/' + reddit_ir_model + '/select?' + encoded_solr_query + \
               '&fl=id%2Cscore&wt=json&indent=true&rows=5&facet=true&' + \
               facet_query
    print(solr_url)
    response_result = urllib.request.urlopen(solr_url)
    return json.load(response_result)['response']['docs']


def get_top_10_topic_answers(documents):
    string = ""
    for document in documents:
        reddit_id = document['id']
        if not string:
            string += "parent_id:\"%s\"" % ("t3_" + reddit_id)
        else:
            string += " OR " + "parent_id:\"%s\"" % ("t3_" + reddit_id)

    solr_query = {"q": string}
    encoded_solr_query = urllib.parse.urlencode(solr_query)
    solr_response_url = 'http://35.222.156.17:8983/solr/' + reddit_ir_model + '/select?' + encoded_solr_query + '&fl=body%2Cscore&wt=json&indent' \
                                                                                                                '=true&rows=10 '
    print(solr_response_url)
    response_result = urllib.request.urlopen(solr_response_url)
    return json.load(response_result)['response']['docs']


def topic_query(topic, query):
    topic_query_documents = get_top_5_topic_query_matches(topic, query)
    documents = get_top_10_topic_answers(topic_query_documents)
    result = [document['body'] for document in documents]
    bot_reply = similarity_classifier.get_top_similarity_answer(query, result)
    return bot_reply


def chit_chat_query(query):
    query_docs = get_top_5_chit_chat_query_matches(query)
    string = ""
    for doc in query_docs:
        message_id = doc['message_id'][0]
        string = string + "parent_message_id:\"%s\"" % message_id + " or "
    response_docs = get_top_10_chit_chat_answers(string)
    result = [document['text'][0] for document in response_docs]
    bot_reply = similarity_classifier.get_top_similarity_answer(query, result)
    return bot_reply


@app.route("/bot", methods=['POST'])
@cross_origin(origin='*')
def execute_query():
    """ This function handles the POST request to your endpoint.
        Do NOT change it."""
    request_json = dict(request.json)
    topic_name = ""
    print(request_json.keys)
    if 'topic' in request_json.keys():
        topic_name = request_json['topic']
    query = request_json['query']
    if not topic_name:
        return chit_chat_query(query)
    else:
        return topic_query(topic_name, query)


if __name__ == "__main__":
    """ Driver code for the project, which defines the global variables.
        Do NOT change it."""
    app.run(host="0.0.0.0", port=9999)
