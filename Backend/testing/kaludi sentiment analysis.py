import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from scipy.special import softmax


all_data = pd.read_csv("https://raw.githubusercontent.com/HaoEarm/DSA3101_Project/main/Data/combined_data2.csv")

all_s = []
model = AutoModelForSequenceClassification.from_pretrained("Kaludi/Reviews-Sentiment-Analysis")
tokenizer = AutoTokenizer.from_pretrained("Kaludi/Reviews-Sentiment-Analysis")
for i in range(len(all_data['Review'])):
    inputs = tokenizer(all_data['Review'][i],padding=True,return_tensors="pt")
    outputs = model(**inputs)
    scores_ = outputs[0][0].detach().numpy()
    scores_ = softmax(scores_)

# Format output dict of scores
    labels = ["Negative", "Positive"]
    scores = {l:float(s) for (l,s) in zip(labels, scores_) }
    all_s.append(scores)

positive_values = [d['Positive'] for d in all_s]
negative_values = [d['Negative'] for d in all_s]
all_data['Positive'] = positive_values
all_data['Negative'] = negative_values

print("ended")
all_data.to_csv('/app/predictions.csv', encoding='utf-8-sig')

