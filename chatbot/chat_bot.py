'''
@author: Harshith Pokala Muni
Institute: University at Buffalo
'''

import json
import random

import urllib
import urllib.request
import urllib.parse

import redditcleaner
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

    solr_url = 'http://35.237.47.57:8983/solr/' + ir_model + '/select?' + encoded_solr_query + '&fl=message_id%2Ctext%2Cscore&wt=json&indent' \
                                                                                               '=true&rows=5'
    print(solr_url)
    query_result = urllib.request.urlopen(solr_url)

    return json.load(query_result)['response']['docs']


def get_top_k_chit_chat_answers(solr_response_query, k):
    # solr_response_query = "parent_message_id:\"%s\"" % message_id
    response_dictionary = {"q": solr_response_query}
    encoded_solr_response_query = urllib.parse.urlencode(response_dictionary)
    solr_response_url = 'http://35.237.47.57:8983/solr/' + ir_model + '/select?' + encoded_solr_response_query + \
                        '&fl=text%2Cscore&wt=json&indent' + '=true&rows=%s' % k
    response_result = urllib.request.urlopen(solr_response_url)
    return json.load(response_result)['response']['docs']


def get_top_5_topic_query_matches(topic, query):
    solr_query = "selftext:(%s)" % query
    topic_query_dictionary = {"q": solr_query}
    encoded_solr_query = urllib.parse.urlencode(topic_query_dictionary)
    facet_query = urllib.parse.urlencode({"facet.query": "topic:\"%s\"" % topic})
    solr_url = 'http://35.237.47.57:8983/solr/' + reddit_ir_model + '/select?' + encoded_solr_query + \
               '&fl=id%2Cscore&wt=json&indent=true&rows=5&facet=true&' + \
               facet_query
    print(solr_url)
    response_result = urllib.request.urlopen(solr_url)
    return json.load(response_result)['response']['docs']


def get_top_k_topic_answers(documents, k):
    string = ""
    for document in documents:
        reddit_id = document['id']
        if not string:
            string += "parent_id:\"%s\"" % ("t3_" + reddit_id)
        else:
            string += " OR " + "parent_id:\"%s\"" % ("t3_" + reddit_id)

    solr_query = {"q": string}
    encoded_solr_query = urllib.parse.urlencode(solr_query)
    solr_response_url = 'http://35.237.47.57:8983/solr/' + reddit_ir_model + '/select?' + encoded_solr_query + \
                        '&fl=body%2Cscore&wt=json&indent' + '=true&rows=%s ' % k
    print(solr_response_url)
    response_result = urllib.request.urlopen(solr_response_url)
    return json.load(response_result)['response']['docs']


def topic_query(topic, query):
    topic_query_documents = get_top_5_topic_query_matches(topic, query)
    documents = get_top_k_topic_answers(topic_query_documents, 10)
    result = [document['body'] for document in documents]
    # result = [redditcleaner.clean(text) for text in result]
    reply = random.choice(result)
    reply = redditcleaner.clean(reply)
    result_list = reply.split()[:50]
    bot_reply = " ".join(result_list)
    return bot_reply  # first 50 words


def chit_chat_query(query):
    query_docs = get_top_5_chit_chat_query_matches(query)
    string = ""
    for doc in query_docs:
        message_id = doc['message_id'][0]
        string = string + "parent_message_id:\"%s\"" % message_id + " or "
    response_docs = get_top_k_chit_chat_answers(string, 10)
    result = [document['text'][0] for document in response_docs]
    bot_reply = similarity_classifier.get_top_similarity_answer(query, result)
    if not bot_reply:
        return "Chat bot is still learning!!"
    else:
        return bot_reply

def get_reddit_results(query):
    reddit_query = "parent_body:(%s)" % query
    query_dict = {"q": reddit_query}
    encoded_solr_query = urllib.parse.urlencode(query_dict)
    solr_url = 'http://35.237.47.57:8983/solr/' + reddit_ir_model + '/select?' + encoded_solr_query + \
               '&fl=body%2Cscore&wt=json&indent=true&rows=3'
    response_result = urllib.request.urlopen(solr_url)
    documents = json.load(response_result)['response']['docs']
    return [document['body'] for document in documents]

def common_query(query):
    reddit_results = get_reddit_results(query)
    query_docs = get_top_5_chit_chat_query_matches(query)
    string = ""
    for doc in query_docs:
        message_id = doc['message_id'][0]
        string = string + "parent_message_id:\"%s\"" % message_id + " or "
    response_docs = get_top_k_chit_chat_answers(string, 5)
    chit_chat_results = [document['text'][0] for document in response_docs]
    final_result = reddit_results + chit_chat_results
    bot_reply = similarity_classifier.get_top_similarity_answer(query, final_result)
    bot_reply = redditcleaner.clean(bot_reply)
    bot_result = bot_reply.split()[:50]
    result = " ".join(bot_result)
    return result


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
    if not topic_name or topic_name == 'chitchat':
        return chit_chat_query(query)
    elif topic_name == 'all':
        return common_query(query)
    else:
        return topic_query(topic_name, query)


if __name__ == "__main__":
    """ Driver code for the project, which defines the global variables.
        Do NOT change it."""
    app.run(host="0.0.0.0", port=9999)
