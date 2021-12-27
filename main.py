import numpy as np
from sklearn.cluster._kmeans import KMeans

import file_manager as fm

all_links = fm.get("_all_links")
guide = fm.get("_guide")

train = fm.get("_train_gft")
test = fm.get("_test_gft")

clusters = 3
out = KMeans(n_clusters=clusters, random_state=0).fit(train)

test = np.reshape(np.array(test), (-1, len(guide.keys())))
predictions = out.predict(test)

for cluster in range(clusters):
	print("Trained: ", list(out.labels_).count(cluster), " - ", "Predicted: ", list(predictions).count(cluster))