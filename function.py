from tkinter import filedialog as fd
from tkinter.messagebox import *
import xlrd
import numpy as np
import  pandas as pd
import math
import openpyxl
import kd_tree
import pprint
import c_means
import validation as validity
from collections import Counter
from sklearn.cluster import KMeans
from c_means import CMeans
from sklearn.metrics import davies_bouldin_score
import time

global_data = None

#depth adalah jika jumlah data hasil centroid kurang misal 30 maka iterasi berhenti
class Function:

    def __init__(self,root):
        self.data = None
        self.n_cluster = 3
        self.depth = 2
        self.kd_tree = []
        self.KMeans_centre = []
        self.KMeans_labels = []
        self.CMeans_centre = []
        self.CMeans_labels = []
        self.validity = []
        self.DBI = []
        self.result = {}

    def search_file(self):
        pathfile = fd.askopenfilename(filetypes=[("Excel files", ".xlsx .xls")])
        # self.read_excel(pathfile)
        if pathfile:
            self.read_excel(pathfile)

    def validate_number(self):
        if self.cluster < 0 or self.stop_at < 0:
            return False
        else:
            return True

    def read_excel(self,location):
        excel_data = pd.read_excel(location)
        keys = excel_data.keys();
        df = pd.DataFrame(excel_data)
        dt = np.array(df)
        global global_data
        global_data = df
        keys = global_data.keys()


    def process(self,n_cluster,dict_kdTree=None,dict_KMeans=None,dict_CMeans=None):
        global global_data
        np.set_printoptions(precision=2,suppress=True)
        start_time = time.time()
        self.n_cluster = n_cluster
        self.kd_tree = []
        keys =  global_data.keys()
        depth_KdTree = dict_kdTree['depth']
        maxter_CMeans = dict_CMeans['maxter']
        # weight_CMeans = dict_CMeans['weight']

        product_code=  global_data.iloc[:,1]

        #2 karena ada row No dan Product Code
        length_row = len(keys)-1
        n_cluster = int(n_cluster)
        dummy_data = np.zeros([n_cluster,length_row-1])

        counter = 0

        for i in range(2,length_row,2):
            x_y = global_data.iloc[:, [i, i+1]]
            x_y.insert(loc=0,column="Product_Code",value=product_code)
            result = kd_tree.KDTREE(depth=depth_KdTree, data=pd.DataFrame(x_y), total_cluster=n_cluster)
            centroid =  result.getCentroid()

            for x in range(n_cluster):
                dummy_data[x][counter*2] = centroid[x][0] # karena centroid x dan y maka 0 dan 1
                dummy_data[x][counter*2+1] = centroid[x][1]

            counter += 1

        self.kd_tree = dummy_data
        dt_means = global_data.iloc[:,2:] #2 karena ada Keys No dan Keys Product Code
        dt_means = dt_means.values

#memanggil kmeans serta menghitung waktu iterasi
        start_time_KMeans = time.time()
        kmeans = KMeans(n_clusters=n_cluster, init=self.kd_tree, n_init=1)
        kmeans.fit(dt_means)
        kmeans_label = kmeans.labels_
        kmeans_cluster_centers = np.round(np.array(kmeans.cluster_centers_),2)
        time_KMeans = time.time() - start_time_KMeans

        start_time_CMeans = time.time()
        cmeans = c_means.CMeans(n_cluster=n_cluster,init_centroid=self.kd_tree,maxter=maxter_CMeans)
        cmeans.fit(dt_means)
        cmeans_label = cmeans.labels()
        cmeans_cluster_centers = np.array(cmeans.cluster_center())
        time_CMeans = time.time() - start_time_CMeans

        #validasi
        # valid = validity.Validation(n_cluster=n_cluster, centers_KMeans=kmeans.cluster_centers_,
        #                             centers_CMeans=cmeans.cluster_center(), labels_KMeans=kmeans.labels_,
        #                             labels_CMeans=cmeans.labels())
        # valid.fit(data=dt_means)
        # self.DBI.append(valid.DBI_result)

        time_result = time.time() - start_time
        DBI_KMeans = round(davies_bouldin_score(dt_means,labels=kmeans_label),2)
        DBI_CMeans = round(davies_bouldin_score(dt_means,labels=cmeans_label),2)
        counter_KMeans = Counter(kmeans_label);
        counter_KMeans = sorted(counter_KMeans.items());
        counter_CMeans = Counter(cmeans_label);
        counter_CMeans = sorted(counter_CMeans.items());

        result = {
            "data":dt_means,
            "KMeans": {
                "cluster_center": np.array(kmeans_cluster_centers),
                "label_cluster":kmeans_label,
                "time":time_KMeans,
                "DBI":DBI_KMeans,
                "counter":str(counter_KMeans),
                "iteration":kmeans.n_iter_
            },
            "CMeans":{
                "cluster_center":cmeans_cluster_centers,
                "label_cluster":cmeans_label,
                "time":time_CMeans,
                "DBI":DBI_CMeans,
                "counter":str(counter_CMeans),
                "iteration":cmeans.iteration-1,
            }
        }

        print(result)
        self.result = result

        return self

    # def DaviesBouldin(self,X, labels):
    #     n_cluster = len(np.bincount(labels))
    #     print(labels)
    #     print(self.n_cluster)
    #     cluster_k = [X[labels == k] for k in range(int(self.n_cluster))]
    #     print("impolana")
    #     centroids = [np.mean(k, axis=0) for k in cluster_k]
    #     variances = [np.mean([euclidean(p, centroids[i]) for p in k]) for i, k in enumerate(cluster_k)]
    #     db = []
    #
    #     for i in range(n_cluster):
    #         for j in range(n_cluster):
    #             if j != i:
    #                 db.append((variances[i] + variances[j]) / euclidean(centroids[i], centroids[j]))
    #
    #     return (np.max(db) / n_cluster)



# dt = pd.read_excel('tes100.xlsx')
# dt_process = dt.iloc[:,[1,2]]
# result = kd_tree.KDTREE(depth=10,data=dt,total_cluster=3)
# centroid = result.getCentroid()

# kmeans = KMeans(n_clusters=3,init=centroid,n_init=1)
# cmeans = CMeans(n_cluster=3,init_centroid=centroid)

# kmeans.fit(dt_process.values)
# cmeans.fit(dt_process.values)

# kmeans_centroid = kmeans.cluster_centers_
# cmeans_centroid = cmeans.cluster_center()

# print(kmeans.labels_)
# print("\n")
# print(cmeans.labels())
# print("--- %s seconds ---" % (time.time() - start_time))
