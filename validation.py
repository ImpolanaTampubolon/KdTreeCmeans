import numpy as np
import pandas as pd
import math

class Validation:

    def __init__(self,n_cluster,centers_KMeans,labels_KMeans,centers_CMeans,labels_CMeans):
        self.data = None
        self.centres_KMeans = centers_KMeans
        self.labels_KMeans = np.array(labels_KMeans)
        self.labels_CMeans = np.array(labels_CMeans)
        self.centres_CMeans = centers_CMeans
        self.Mi_KMeans = []
        self.Mi_CMeans = []
        self.update_clustering_KMeans = []
        self.update_clustering_CMeans = []
        self.n_cluster = n_cluster
        self.ssw_KMeans = None
        self.ssw_CMeans = None
        self.ssb_KMeans = []
        self.ssb_CMeans = []
        self.ratio_KMeans = 0
        self.ratio_CMeans = 0
        self.DBI_KMeans = 0
        self.DBI_CMeans = 0
        self.DBI_result = None

    def fit(self,data):
        self.data = data
        self.ssw()
        self.ssb()
        self.ratio()
        self.DBI()
        return self

    def ssw(self):
        c_K = self.centres_KMeans
        c_C = self.centres_CMeans
        ssw_K = []
        ssw_C = []
        ssw = []

        for i in range(self.n_cluster):
            index_K = np.asarray( np.where(self.labels_KMeans == i)[0] )
            index_C = np.asarray( np.where(self.labels_CMeans == i)[0] )

            #member ke i atau hasil clustering
            Mi_K = self.data[index_K]
            Mi_C = self.data[index_C]

            #init member to global
            # self.Mi_KMeans.append(np.asarray(Mi_K)[0])
            # self.Mi_CMeans.append(np.asarray(Mi_C)[0])


            update_clustering_K = np.transpose(  np.sqrt( np.power( Mi_K[:,0] - c_K[i][0] , 2 ) + np.power( Mi_K[:,1] - c_K[i][1] , 2 ) ) )
            update_clustering_C = np.transpose( np.sqrt( np.power( Mi_C[:,0] - c_C[i][0] , 2 ) + np.power( Mi_C[:,1] - c_C[i][1] , 2 ) )  )

            self.update_clustering_KMeans.append(update_clustering_K)
            self.update_clustering_CMeans.append(update_clustering_C)


            ssw_K.append( np.round(sum(update_clustering_K),2) )
            ssw_C.append( np.round(sum(update_clustering_C),2) )

        self.ssw_KMeans = ssw_K
        self.ssw_CMeans = ssw_C
        return self

    def ssb(self):
        ssb = []
        clustering_K = np.array(self.update_clustering_KMeans)
        clustering_C = np.array(self.update_clustering_CMeans)
        #seperti memasukkan fungsi ke array
        vect = np.vectorize(len)
        max_C = max(vect(clustering_C))
        max_K = max(vect(clustering_K))

        zeros_K = np.zeros([ len(clustering_K), max_K ])

        #ubah nilai 0 menjadi nan sebab, nanti min bisa di ignore
        #kalo tidak diubah menjadi nan maka nilai min nanti selalu 0
        zeros_K[:] = np.nan
        zeros_C = np.zeros([len(clustering_C),max_C])
        zeros_C[:] = np.nan

        #inisiais array nan agar matriks nya tidak ambigous
        for i in range(self.n_cluster):
            zeros_K[i][0:len(clustering_K[i]):1] = clustering_K[i]
            zeros_C[i][0:len(clustering_C[i]):1] = clustering_C[i]

        clustering_K = np.transpose(zeros_K)
        clustering_C = np.transpose(zeros_C)

        min_K = np.nanmin( np.round(clustering_K,2),axis=1)
        min_C = np.nanmin( np.round(clustering_C,2),axis=1)

        # ubah is nan menjadi 0 agar proses perkalian pada ssb menjadi tetap misal 0 kali 10 = 0
        clustering_K[np.isnan(clustering_K)] = 0
        clustering_C[np.isnan(clustering_C)] = 0

        ssb_K = 0
        ssb_C = 0

        for i in range(len(min_K)):
            res_K = round(sum(clustering_K[i] * min_K[i]), 2)
            ssb_K += res_K
            self.ssb_KMeans.append(res_K)

        for x in range(len(min_C)):
            res_C = round(sum(clustering_C[x] * min_C[x]),2)
            ssb_C += res_C
            self.ssb_CMeans.append(res_C)

        return ssb

    def ratio(self):
        ssw_KMeans = sum(self.ssw_KMeans)
        ssw_CMeans = sum(self.ssw_CMeans)
        ssb_KMeans = sum(self.ssb_KMeans)
        ssb_CMeans = sum(self.ssb_CMeans)
        ratio_KMeans = round( ssw_KMeans/ssb_KMeans,2)
        ratio_CMeans = round(ssw_CMeans/ssb_CMeans,2)

        self.ratio_KMeans = ratio_KMeans
        self.ratio_CMeans = ratio_CMeans
        tes = {
            "ssw_KMeans":self.ssw_KMeans,
            "ssw_CMeans":self.ssw_CMeans,
            "ssb_KMeans":ssb_KMeans,
            "ssb_CMeans":ssb_CMeans,
            "ratio_KMeans":ratio_KMeans,
            "ratio_CMeans":ratio_CMeans
        }
        return self

    def DBI(self):
        self.DBI_KMeans = round( 0.5 * self.n_cluster * self.ratio_KMeans,2)
        self.DBI_CMeans = round( 0.5 * self.n_cluster * self.ratio_CMeans,2)

        self.DBI_result = { "KMeans":self.DBI_KMeans , "CMeans": self.DBI_CMeans }
        return self


# dt = np.array([
#     [7,11],
#     [9,14],
#     [17,5],
#     [3,19],
#     [10,2],
#     [6,20],
#     [16,1],
#     [15,13],
#     [1,15],
#     [11,7],
# ]);
#
# centre_KMeans = np.array([ [10.33,12.67],[3.33,18],[13.5,3.75] ])
# centre_CMeans = np.array([ [6.05,13.11],[4.99,19.16],[13.99,3.97] ])
# label_KMeans = [0,0,2,1,2,1,2,0,1,2]
# label_CMeans = [0,0,2,1,2,1,2,0,0,2]
# validation = Validation(n_cluster=3,centers_KMeans=centre_KMeans,labels_KMeans=label_KMeans,labels_CMeans=label_CMeans,centers_CMeans=centre_CMeans)
# validation.fit(data=dt)