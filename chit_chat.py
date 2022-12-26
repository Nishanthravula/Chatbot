import pandas as pd
import chitchat_dataset as ccc
import statistics

dataset = ccc.Dataset()
dataframe = pd.DataFrame(dataset)
# Dataset is a subclass of dict()
data_dict = dict(dataset)
count = 0
# for convo_id, convo in dataset.items():
#     print(convo_id, convo)
#     count += 1
#     if count ==5:
#         break

# for key, value in data_dict.items():
#     print(key, value)
#     conversation = value
#     break

print(len(data_dict.keys()))

# messages = list(ccc.MessageDataset())
# print(messages)
chat_formatted = pd.DataFrame()
for key, value in data_dict.items():
    conversation_id = key
    conversation = value
    if 'ratings' not in conversation.keys() or 'prompt' not in conversation.keys() or 'messages' not in conversation.keys():
        continue
    ratings = conversation['ratings']
    prompt = conversation['prompt']
    messages = conversation['messages']
    mean_rating = statistics.mean(list(ratings.values()))
    is_witty = "TRUE" if ratings['witty'] >= mean_rating else "FALSE"
    is_upbeat = "TRUE" if ratings['upbeat'] >= mean_rating else "FALSE"
    is_interesting = "TRUE" if ratings['interesting'] >= mean_rating else "FALSE"
    index = 1
    for message_list in messages:
        message_id = conversation_id + '_' + str(index)
        parent_message_id = ''
        if index > 1:
            parent_message_id = conversation_id + '_' + str(index - 1)
        for message in message_list:
            text = message['text']
            data = {'message_id': message_id, 'text': text, 'prompt': prompt,
                    'parent_message_id': parent_message_id, 'is_witty': is_witty,
                    'is_upbeat': is_upbeat, 'is_interesting': is_interesting
                    }
            chat_formatted = chat_formatted.append(data, ignore_index=True)
        index += 1

print(chat_formatted)
csv_data = chat_formatted.to_csv('chit_chat_formatted.csv')
print(csv_data)
