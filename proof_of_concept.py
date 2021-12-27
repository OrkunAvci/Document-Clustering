import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster._kmeans import KMeans
import file_manager as fm
import os
from tqdm import tqdm

all_links = fm.get("_all_links")
guide = fm.get("_guide")
raws = [fm.get("raw_" + link) for link in tqdm(all_links) if os.path.isfile('data/raw_'+fm.clean_up_name(link))]

vectorizer = CountVectorizer()
train = vectorizer.fit_transform(raws[:3000])
tests = vectorizer.transform(raws[3000:])

clusters = 4
out = KMeans(n_clusters=clusters, random_state=0).fit(train)


features = len(vectorizer.get_feature_names_out())
tests = np.reshape(tests.toarray(), (-1, features))
predictions = out.predict(tests)

for cluster in tqdm(range(clusters)):
	print("Trained: ", list(out.labels_).count(cluster), " - ", "Predicted: ", list(predictions).count(cluster))
