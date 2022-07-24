import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans


img = mpimg.imread('Assets/girl3.jpg')
imgplot = plt.imshow(img)
plt.axis('off')
plt.show()
X = img.reshape((img.shape[0]*img.shape[1], img.shape[2]))

for K in [2, 5, 10, 15, 20]:
    kmeans = KMeans(n_clusters=K).fit(X)
    label = kmeans.predict(X)
    img4 = np.zeros_like(X)
    for k in range(K):
        img4[label == k] = kmeans.cluster_centers_[k]

    img5 = img4.reshape(img.shape[0], img.shape[1], img.shape[2])
    plt.imshow(img5)
    plt.axis('off')
    plt.show()




