import math
import pandas as pd
import numpy as np
from tkinter import messagebox

class KDTREE:

    def __init__(self,depth,data,total_cluster):
        self.depth = depth
        self.total_cluster = total_cluster
        self.iteration = 0
        self.cluster = []
        self.count_node = 0;
        self.sort_by = 'y'
        self.leaf_bucket = None
        self.centroid = []

        keys = data.keys()
        dt = pd.DataFrame(data, columns=[keys[1], keys[2]])
        self.build_tree(dt)
        self.searchCenteroid()

    def build_tree(self,data,side="left"):
        keys = data.keys()

        n = len(data)
        sample = np.zeros(2)
        half = math.ceil( ( len(data) / 2) )

        if len(data) <= self.depth:
            return None

        #cek jika nilai selanjut dari banyak data lebih
        #sama dengan setengah maka sorting dibuat secara bergantian
        if half >= self.depth or side is 'left':
            self.iteration+=1
            if self.sort_by is "x":
                self.sort_by = "y"
            elif self.sort_by is "y":
                self.sort_by = "x"

        if self.sort_by is 'x':
            data.sort_values(keys[0], ascending=True, inplace=True, na_position='last')
        else:
            data.sort_values(keys[1], ascending=True, inplace=True, na_position='last')

        data.reset_index(drop=True, inplace=True)
        # gunakan values untuk mendapatkan numpy array atau array dimensi

        #buat node dengan kiri, tengah , kanan
        narray = data.values
        #tengah merupakan hasil data yang di dapatkan dari iterasi sebelumnya
        left_data = pd.DataFrame(narray[0:half-1],columns=[keys[0],keys[1]])
        right_data = pd.DataFrame(narray[half:],columns=[keys[0],keys[1]])
        left_node = self.build_tree(left_data,side="left")
        right_node = self.build_tree(right_data,side="right")

        #tambahkan data hasil iterasi terakhir ke variable tree
        #data inilah akan akan digunakan untuk mencari centroid
        if left_node is None or right_node is None:
            self.cluster.append(narray)


        node = {
            "data":narray,
            "left":left_node,
            "right":right_node
        }

        return node;

    def searchCenteroid(self):
        columns = ["Leaf","N","X","Y","V","Pj"]
        dt = np.zeros((len(self.cluster),6))
        dt_frame = pd.DataFrame(dt,columns=columns)
        dt_frame.iloc[0] = np.arange(6)

        for i in range(len(self.cluster)):
            mean = np.mean(self.cluster[i],axis=0)
            max = np.max(self.cluster[i],axis=0)
            min = np.min(self.cluster[i],axis=0)
            V = max[0]-min[0]+max[1]-min[1]
            N = len(self.cluster[i])
            Pj = round(N/V,2)
            # Pj = math.isinf(Pj) if 0 else Pj
            if math.isinf(Pj) is True:
                Pj = 0
            else:
                Pj = Pj

            insert_data = np.array(["L"+str(i),N,round(mean[0],2),round(mean[1],2),V,Pj])
            dt_frame.iloc[i] = insert_data



        self.leaf_bucket = dt_frame
        bucket = dt_frame.copy()
        index = dt_frame.index[dt_frame['Pj'] == dt_frame.max()['Pj']]
        #masalah jika
        result_centroid = dt_frame.iloc[index[0]]
        self.centroid.append(result_centroid.values)
        centroid = result_centroid.values
        # print("not")
        # print(result_centroid.values)
        #jika jumlah total cluster lebih dari 1
        #maka process untuk mengambil centroid selanjutnya
        #leaf bucket centeroid yang kedua diambil dari dari leaf_bucket
        #dengan membuang 20 % nilai dari min Pj

        #dikurang satu karena iterasi untuk mencari c1 tidak dihitung lagi
        self.nextCentroid()

    def nextCentroid(self):
        #duplicate bucket
        bucket = self.leaf_bucket
        bucket_process = pd.DataFrame(bucket.copy())
        centroid_process = self.centroid
        #buat data dummy dengan n jumlah row bucket
        dt_dummy = np.zeros(len(bucket_process))
        bucket_process.insert(6,"Dj",dt_dummy,True)
        bucket_process.insert(7,"Gj",dt_dummy,True)

        for x in range(self.total_cluster - 1):
            used_c = self.centroid[x]
            mean_X = used_c[2]
            mean_Y = used_c[3]
            split_dt = math.ceil((20 / 100) * len(bucket_process))

            for i in range(split_dt):
                bucket_process.reset_index()
                row_drop = bucket_process.index[bucket_process['Pj'] == bucket_process.min()['Pj']]
                index_drop = row_drop.values[0]
                bucket_process.drop(bucket_process.index[index_drop], inplace=True)
                bucket_process.reset_index(drop=True,inplace=True)

            #series yang diloop
            mean_X = pd.to_numeric(mean_X)
            mean_Y = pd.to_numeric(mean_Y)
            current_X = pd.to_numeric( bucket_process['X'] )
            current_Y = pd.to_numeric( bucket_process['Y'] )

            current_Pj = pd.to_numeric( bucket_process['Pj'] )
            #ubah semua nilai x menjadi numeric jika ingin ditambah
            bucket_process['Dj'] = round(np.sqrt ( np.power((current_X - mean_X),2) + np.power( (current_Y - mean_Y),2) ) ,2)
            bucket_process['Gj'] = round( (current_Pj * bucket_process['Dj'] ) ,2)

            index_next_centroid = bucket_process.index[bucket_process['Gj'] == bucket_process.max()['Gj']]

            if len(index_next_centroid) > 0 :
                next_centroid = self.leaf_bucket.iloc[index_next_centroid[0]]
                self.centroid.append(next_centroid.values)
            else:
                messagebox.showinfo("showinfo","jumlah cluster atau depth melebihi dari jumlah maksimum");

    def getCentroid(self):
        centroid = []

        for i in self.centroid:
            centroid.append([float(i[2]),float(i[3])])

        return centroid


# dt = pd.read_excel('tes.xlsx')
# keys =  dt.keys()
# product_code= dt.iloc[:,0]
# length_row = len(keys)-1
# centroid = []

# for i in range(0,length_row,2):
#     x_y = pd.DataFrame(dt.iloc[:, [(i + 1), (i + 2)]])
#     x_y.insert(loc=0, column="Product_Code", value=product_code)
#     result = KDTREE(depth=3,data=pd.DataFrame(x_y),total_cluster=3)
#     centroid.append(result.getCentroid())
#
# print(centroid)
# result = KDTREE(depth=3,data=dt,total_cluster=3)
# leafbucket = result.leaf_bucket
# print(result.cluster)

# pp = pprint.PrettyPrinter()
# pp.pprint(result.getCentroid())
# print(dt.iloc[ :,[1,2] ])
# print(result.getCentroid())
