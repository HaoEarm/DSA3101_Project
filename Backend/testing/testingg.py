import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


preds = pd.read_csv("https://raw.githubusercontent.com/HaoEarm/DSA3101_Project/main/Data/predictions.csv")

preds['Date'] = pd.to_datetime(preds['Date'], dayfirst=True)
preds.sort_values(by=['Date'], inplace=True)
preds['cum_pos'] = preds.rolling(window="30D", on='Date')['Positive'].sum()
preds['cum_neg'] = preds.rolling(window="30D", on='Date')['Negative'].sum()
preds_GXS = preds.loc[preds['Bank'].eq('GXS Bank')]

print("plotting")
plt.figure(figsize=(10, 5))
plt.plot(preds_GXS['Date'], preds_GXS['cum_pos'], linestyle='solid', label = 'positive', color = 'green')
plt.plot(preds_GXS['Date'], preds_GXS['cum_neg'], linestyle='solid', label = 'negative', color = 'red')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d')) # format x-axis labels
plt.gcf().autofmt_xdate() # auto fit x-axis labels
plt.xlabel("Date")
plt.ylabel("Cumulative Sentiment Score")
plt.title('Sentiment Scores Over Time: GXS Bank')
plt.legend()
plt.show()
