# Libraries
from wordcloud import WordCloud , STOPWORDS
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import pandas as pd 

def createWordCloud():
	stopwords = set(STOPWORDS)
	data = pd.read_csv("twitter_sentiment_analysis.csv")

	wave_mask = np.array(Image.open( "twitter_mask.png"))
	 
	# Make the figure
	wordcloud = WordCloud(mask=wave_mask, background_color="Black",colormap="Blues").generate(str(data['Tweets']))
	plt.figure()
	plt.imshow(wordcloud, interpolation="bilinear")
	plt.axis("off")
	plt.margins(x=0, y=0)
	plt.show()

#createWordCloud()
