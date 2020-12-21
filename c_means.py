import random
import numpy as np
import pandas as pd
import math

class CMeans:

    def __init__(self,n_cluster=10,maxter = 100,weight=2,init_centroid=None,epsilon = pow(10,-4)):
        self.n_cluster = n_cluster;
        self.maxter = maxter
        self.w = weight
        self.current_centroid = init_centroid
        self.first_iteration = 1
        self.first_membership = None
        self.data = None
        self.iteration = 0
        self.epsilon = epsilon
        self.current_distance = None
        self.current_objective_function = 0
        self.current_membership = None
        self.inertia = []
        np.seterr(all='ignore')

    #inertia adalah centroid di setiap iterasi

    def fit(self,data):
        self.data = data
        self.current_membership = self.firstMembership()
        return self.objective_function()

    def cluster_center(self):
        return self.current_centroid

    def get_iteration(self):
        return self.iteration

    def labels(self):
        centers = self.current_membership
        labeled = np.zeros([len(self.data), self.n_cluster])
        #return index yang bernilai max pad column
        centers_max = np.argmax(centers,axis=1)
        return centers_max

    def firstMembership(self):
        points = []
        N = len(self.data)
        for i in range(N):
            single_points = []
            a = pow(10,-2)
            c = self.n_cluster * a
            b = 1 - c
            r = 2 #pembulatan

            for k in range(self.n_cluster):
                rand_num = round(random.uniform(a,b),r)

                if k == self.n_cluster - 1 :
                    rand_num = 1 - round(sum(single_points),r)

                if rand_num <= 0:
                    rand_num = 0

                single_points.append(round(rand_num, r))
                b = 1 - round(sum(single_points),r)

            points.append( single_points)

        self.first_membership =  np.array(points)
        return np.array(points)

    def objective_function(self):
        self.iteration += 1
        distance = np.array(self.distance())
        transpose_distance = distance.transpose()
        total = sum( sum( transpose_distance ) )
        total = round( total , 4)- self.current_objective_function
        self.current_objective_function = total

        if total >= self.epsilon and self.iteration <= self.maxter:
            self.updateMembership(distance = distance)
            return self.objective_function()
        else:
            return None

    #rumus mencari centroid
    def centroid(self):

        if self.iteration <= 1 and self.current_centroid is not None:
            return self.current_centroid

        membership = self.current_membership
        current_centroid = []
        #
        # X = self.data[:,0]
        # Y = self.data[:,1]
        len_attribute = self.data.shape[1]

        for i in range(self.n_cluster):
            m = membership[:,i]
            Cj = []

            for x in range(len_attribute):
                dt_pro = self.data[:,x]
                C = sum( dt_pro * pow(m,self.w) )
                j = sum( pow(m,self.w) )
                result = round(C/j,2)
                Cj.append(result)

            current_centroid.append(Cj)

        self.current_centroid = current_centroid
        self.inertia.append(current_centroid)

        return current_centroid

    #rumus mencari jarak
    def distance(self):
        distance = []
        centroid = self.centroid()
        X = self.data[:,0]
        Y = self.data[:,1]
        len_attribute = self.data.shape[1]

        for i in range(self.n_cluster):
            D = 0

            for x in range(len_attribute):
                D += pow( self.data[:,x] - centroid[i][x] ,2)

            Dj = np.sqrt(D)
            distance.append(Dj)

        return distance

    def updateMembership(self,distance):
        D = distance
        new_membership = np.zeros([len(self.data), self.n_cluster])

        for i in range(self.n_cluster):
            Dji = pow( 1/D[i], 1/( self.w-1 ))
            Dki = 0

            for x in range(self.n_cluster):
                if x != i :
                    D[x][ D[x]== 0] = 1
                    Dki += pow( 1/D[x], 1/( self.w-1 ))

            Mj =  Dji / (Dji + Dki)
            new_membership[:,i] = np.array(Mj)

        self.current_membership = new_membership



# print(member)
# print(member[:,0])
#alur
# fit()->objective_function->distance->centroid
# dt = pd.read_excel('tes.xlsx')
# dt = dt.iloc[:,1:]
# dt = dt.values
# c_means = CMeans(n_cluster=3)
# c_means.fit(data=dt)
# print(c_means.cluster_center())
# print("\n")
# print(c_means.labels())

