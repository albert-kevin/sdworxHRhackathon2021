# replace 'key' and 'endpoint':
azure_textanalytics_key = '2180035c81284813a4d457640c87f017'
azure_textanalytics_endpoint = 'https://westeurope.api.cognitive.microsoft.com/'

import pandas as pd
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
client = TextAnalyticsClient(azure_textanalytics_endpoint, AzureKeyCredential(azure_textanalytics_key))

# example data:
documents = ["I had a wonderful trip to Seattle last week."]
df = pd.DataFrame({'col1': documents})

result = pd.DataFrame()
temp   = []
start  = 0      # index id start (ex: 0)
stop   = 1   # index id stop  (ex: 5000)
step   = 1      # max 5 (ex: 5)
column = "col1" # from dataframe
# https://docs.microsoft.com/en-us/azure/cognitive-services/text-analytics/concepts/data-limits

for i in range(start, stop, step): # 0-5000, 5000-10000, etc... (~10min)
    documents = (df[column].iloc[i:i+step]).tolist()

    sentiment_response = client.analyze_sentiment(documents)
    # print(i, end='\r') # second counter
    for idx, doc in enumerate(sentiment_response):
        for idy, sentiment in enumerate(doc.sentences):
            comment.loc[idy, "sentiment"] = str(sentiment.sentiment)
        # temp.append(comment)

    entities_response = client.recognize_entities(documents)
    print(i, end='\r') # counter
    for idx, doc in enumerate(entities_response):
        comment = pd.DataFrame()
        for idy, entity in enumerate(doc.entities):
            comment.loc[idy, "document"] = str(documents[idx])
            comment.loc[idy, "entities"] = str(entity)
            comment.loc[idy, "entity_text"] = str(entity.text)
            comment.loc[idy, "entity_category"] = str(entity.category)
            comment.loc[idy, "entity_subcategory"] = str(entity.subcategory)
            comment.loc[idy, "entity_confidence_score"] = str(entity.confidence_score)
        temp.append(comment)
        
result = pd.concat(temp, axis=0, ignore_index=True)
result.to_csv("entities_"+str(start)+"_"+str(stop)+".csv", index=False)
# result