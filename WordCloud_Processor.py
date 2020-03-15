from os import path
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import matplotlib.pyplot as plt

# Start with one review:
def create_wordcloud(list,n):
    # Create and generate a word cloud image:
    wordcloud = WordCloud(max_font_size=20, max_words=n, background_color="white", contour_width=3, contour_color='firebrick').generate(list)
    plt.figure(figsize=[7, 7])
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig("beatles.png", format="png")
    plt.show()