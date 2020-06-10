import pandas as pd, os, sys, glob, numpy as np, seaborn as sns, wordcloud, datetime
from collections import Counter
from matplotlib import pyplot as plt

print("\nInitializing...")

count = 0
df_GB = df_ID = df_MY = df_US = df_SG = pd.DataFrame()
dataFrames = [df_GB, df_ID, df_MY, df_SG, df_US]
path = "C:/Users/RnD/PycharmProjects/Youtube-Trending-Analysis/v/output/*.csv"
for file in glob.glob(path):
    dataFrames[count] = pd.read_csv(file)
    count = count + 1
print("Counting...")

print("Cleaning...")
for eachDataset in dataFrames:
    eachDataset = eachDataset.replace(np.nan, '', regex=True)

print("Analysing...")
print("Visualizing...")
for eachDataset in dataFrames:
    h_labels = [x.replace('_', ' ').title() for x in
                list(eachDataset.select_dtypes(include=['number', 'bool']).columns.values)]
    fig, ax = plt.subplots(figsize=(10, 6))
    _ = sns.heatmap(eachDataset.corr(), annot=True, xticklabels=h_labels, yticklabels=h_labels,
                    cmap=sns.cubehelix_palette(as_cmap=True), ax=ax)
    plt.show()



    title_words = list(eachDataset["title"].apply(lambda x: x.split()))
    title_words = [x for y in title_words for x in y]
    Counter(title_words).most_common(25)
    wc = wordcloud.WordCloud(width=1200, height=500,
                             collocations=False, background_color="white",
                             colormap="tab20b").generate(" ".join(title_words))
    plt.figure(figsize=(15, 10))
    plt.imshow(wc, interpolation='bilinear')
    _ = plt.axis("off")



    eachDataset["publishing_day"] = eachDataset["publishedAt"].apply(
        lambda x: datetime.datetime.strptime(x[:10], "%Y-%m-%d").date().strftime('%a'))
    eachDataset["publishing_hour"] = eachDataset["publishedAt"].apply(lambda x: x[11:13])
    eachDataset.drop(labels='publishedAt', axis=1, inplace=True)
    cdf = eachDataset["publishing_day"].value_counts() \
        .to_frame().reset_index().rename(columns={"index": "publishing_day", "publishing_day": "No_of_videos"})
    fig, ax = plt.subplots()
    _ = sns.barplot(x="publishing_day", y="No_of_videos", data=cdf,
                    palette=sns.color_palette(['#003f5c', '#374c80', '#7a5195',
                                               '#bc5090', '#ef5675', '#ff764a', '#ffa600'], n_colors=7), ax=ax)
    _ = ax.set(xlabel="Publishing Day", ylabel="No. of videos")



    cdf = eachDataset["publishing_hour"].value_counts().to_frame().reset_index() \
        .rename(columns={"index": "publishing_hour", "publishing_hour": "No_of_videos"})
    fig, ax = plt.subplots()
    _ = sns.barplot(x="publishing_hour", y="No_of_videos", data=cdf,
                    palette=sns.cubehelix_palette(n_colors=24), ax=ax)
    _ = ax.set(xlabel="Publishing Hour", ylabel="No. of videos")



    cdf = eachDataset["categoryId"].value_counts().to_frame().reset_index()
    cdf.rename(columns={"index": "categoryId", "categoryId": "No_of_videos"}, inplace=True)
    fig, ax = plt.subplots()
    _ = sns.barplot(x="categoryId", y="No_of_videos", data=cdf,
                    palette=sns.cubehelix_palette(n_colors=16, reverse=True), ax=ax)
    _ = ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    _ = ax.set(xlabel="Category", ylabel="No. of videos")


print("\nDONE!")