import pandas
import  numpy
from tkinter import *
# import tkinter
# from tkinter.messagebox import *
# from tkinter.ttk import *
import tkinter.messagebox
import tkinter as tk
import function
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


root = tkinter.Tk()


fun = function.Function(root)
root.title("JONTINUS HANDSOME")
root.state("zoomed")

#tinggi dan lebar screen
width_window = root.winfo_reqwidth()
height_window = root.winfo_reqheight()


#tinggi dan lebar window
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()

w = ws
h = hs


#buat posisi ke tengah
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)


#buat form
labelframe_mid = tk.Frame(root,height = 20,width=20)
labelframe_mid.pack(side=LEFT,expand=False,fill="both",padx=10,pady=10)

# canvas_g_K = Canvas(labelframe_mid,width=150,height=200)
# canvas_g_K.pack(side=LEFT,expand=FALSE,fill=BOTH)


button_excel = tk.Button(labelframe_mid,text="Import File excel",bg="green",fg="white",command = lambda : fun.search_file())
button_excel.pack(padx=20,pady=20)

label1 = tk.Label(labelframe_mid,text="Jumlah Cluster")
label1.pack()
entry_cluster = Entry(labelframe_mid)
entry_cluster.insert(0,3)
entry_cluster.pack()

label_depth = Label(labelframe_mid,text="Depth(KDTREE)")
label_depth.pack()
entry_depth = Entry(labelframe_mid)
entry_depth.insert(0,10)
entry_depth.pack()

label_maxter = Label(labelframe_mid,text="Maksimum Iterasi (CMeans)")
label_maxter.pack()

entry_maxter = Entry(labelframe_mid)
entry_maxter.insert(0,300)
entry_maxter.pack()

# label_weight = Label(labelframe_mid,text="Bobot (CMeans)")
# label_weight.pack()
# entry_weight = Entry(labelframe_mid)
# entry_weight.insert(0,2)
# entry_weight.pack()


labelframe_K = tk.LabelFrame(root,text = "KMeans",width=200,height=300)
labelframe_K.pack(side=LEFT,expand=TRUE,fill=BOTH,padx=10,pady=10)

canvas_g_K = Canvas(labelframe_K)
canvas_g_K.pack(side=TOP,expand=TRUE,fill=X)

canvas_K = Canvas(labelframe_K)
sb_K = Scrollbar(labelframe_K,orient="vertical")
sb_K.pack(side="right",fill=Y)
sb_K.config(command=canvas_K.yview)
canvas_K.config(yscrollcommand=sb_K.set)
canvas_K.pack(side=BOTTOM,expand=TRUE,fill=BOTH)


def createResultKMeans(iteration,clustering_centers,labels,dbi,times,counter):
    label_iteration_K = Label(canvas_K, text="Jumlah Iterasi :")
    label_iteration_K.pack()
    canvas_K.create_window((50, 30), window=label_iteration_K, anchor="nw")
    iteration_K = Label(canvas_K, text=iteration)
    iteration_K.pack()
    canvas_K.create_window((150, 30), window=iteration_K, anchor="nw")
    iteration_K.update()

    label_DBI_KMeans = Label(canvas_K, text="DBI :")
    label_DBI_KMeans.pack()
    canvas_K.create_window((50, 70), window=label_DBI_KMeans, anchor="nw")
    DBI_KMeans = Label(canvas_K, text=dbi)
    DBI_KMeans.pack()
    DBI_KMeans.update()
    canvas_K.create_window((150, 70), window=DBI_KMeans, anchor="nw")
    DBI_KMeans.update()

    label_cluster_center_KMeans = Label(canvas_K, text="Pusat Kluster : ")
    label_cluster_center_KMeans.pack()
    canvas_K.create_window((50, 110), window=label_cluster_center_KMeans, anchor="nw")
    cluster_center_KMeans = Label(canvas_K, text=clustering_centers)
    cluster_center_KMeans.pack()
    cluster_center_KMeans.update()
    canvas_K.create_window((150, 110), window=cluster_center_KMeans, anchor="nw")
    cluster_center_KMeans.update()

    current_y = cluster_center_KMeans.winfo_height() + 130

    label_result_clustering_KMeans = Label(canvas_K, text="Anggota Kluster :")
    label_result_clustering_KMeans.pack()
    canvas_K.create_window((50, current_y), window=label_result_clustering_KMeans, anchor="nw")
    result_clustering_KMeans = Label(canvas_K, text=labels)
    result_clustering_KMeans.pack()
    result_clustering_KMeans.update()
    canvas_K.create_window((150, current_y), window=result_clustering_KMeans, anchor="nw")

    current_y = cluster_center_KMeans.winfo_height() + result_clustering_KMeans.winfo_height() + 160

    label_time_KMeans = Label(canvas_K, text="Waktu : ")
    label_time_KMeans.pack()
    canvas_K.create_window((50, current_y), window=label_time_KMeans, anchor="nw")
    time_KMeans = Label(canvas_K, text=times)
    time_KMeans.pack()
    canvas_K.create_window((150, current_y), window=time_KMeans, anchor="nw")


    current_y = cluster_center_KMeans.winfo_height() + result_clustering_KMeans.winfo_height() + 160 + 80

    label_counter_KMeans = Label(canvas_K, text="Counter : ")
    label_counter_KMeans.pack()
    canvas_K.create_window((50, current_y), window=label_counter_KMeans, anchor="nw")
    counter_KMeans = Label(canvas_K, text=counter)
    counter_KMeans.pack()
    canvas_K.create_window((150, current_y), window=counter_KMeans, anchor="nw")

    canvas_K.configure(scrollregion=canvas_K.bbox("all"))



labelframe_C = tk.LabelFrame(root,text = "CMeans", width=200,height=300)
labelframe_C.pack(side=LEFT,expand=TRUE,fill=BOTH,padx=10,pady=10)
canvas_g_C = Canvas(labelframe_C)
canvas_g_C.pack(side=TOP,expand=TRUE,fill=X)


canvas_C = Canvas(labelframe_C)
sb_C = Scrollbar(labelframe_C,orient="vertical")
sb_C.pack(side="right",fill=Y)
sb_C.config(command=canvas_C.yview)
canvas_C.config(yscrollcommand=sb_C.set)
canvas_C.pack(side=BOTTOM,expand=TRUE,fill=BOTH)

label_iteration_C = Label()
iteration_C = Label()
label_cluster_center_CMeans = Label()
cluster_center_CMeans = Label()
label_result_clustering_CMeans= Label()
result_clustering_CMeans = Label()
label_DBI_CMeans = Label()
DBI_CMeans = Label()
label_time_CMeans = Label()
time_Cmeans = Label()

def createResultCMeans(iteration,clustering_centers,labels,dbi,times,counter):
    label_iteration_C = Label(canvas_C, text="Jumlah Iterasi :")
    label_iteration_C.pack()
    canvas_C.create_window((50, 30), window=label_iteration_C, anchor="nw")
    iteration_C = Label(canvas_C, text=iteration)
    iteration_C.pack()
    canvas_C.create_window((150, 30), window=iteration_C, anchor="nw")
    iteration_C.update()

    label_DBI_CMeans = Label(canvas_C, text="DBI :")
    label_DBI_CMeans.pack()
    canvas_C.create_window((50, 70), window=label_DBI_CMeans, anchor="nw")
    DBI_CMeans = Label(canvas_C, text=dbi)
    DBI_CMeans.pack()
    canvas_C.create_window((150, 70), window=DBI_CMeans, anchor="nw")
    DBI_CMeans.update()

    label_cluster_center_CMeans = Label(canvas_C,text="Pusat Kluster : ")
    label_cluster_center_CMeans.pack()
    canvas_C.create_window((50,110),window=label_cluster_center_CMeans,anchor="nw")

    cluster_center_CMeans = Label(canvas_C,text=clustering_centers)
    cluster_center_CMeans.pack()
    canvas_C.create_window((150,110),window=cluster_center_CMeans,anchor="nw")
    cluster_center_CMeans.update()

    current_y = cluster_center_CMeans.winfo_height() + 130

    label_result_clustering_CMeans = Label(canvas_C,text="Anggota Kluster :")
    label_result_clustering_CMeans.pack()
    canvas_C.create_window((50,current_y),window=label_result_clustering_CMeans,anchor="nw")
    result_clustering_CMeans = Label(canvas_C,text=labels)
    result_clustering_CMeans.pack()
    result_clustering_CMeans.update()
    canvas_C.create_window((150,current_y),window=result_clustering_CMeans,anchor="nw")
    # result_clustering_CMeans.update_idletasks()

    current_y = cluster_center_CMeans.winfo_height() + result_clustering_CMeans.winfo_height() + 160

    label_time_CMeans = Label(canvas_C,text="Waktu : ")
    label_time_CMeans.pack()
    label_time_CMeans.update()
    canvas_C.create_window((50, current_y), window=label_time_CMeans, anchor="nw")
    time_CMeans = Label(canvas_C,text=times)
    time_CMeans.pack()
    canvas_C.create_window((150, current_y), window=time_CMeans, anchor="nw")
    time_Cmeans.update()

    current_y = cluster_center_CMeans.winfo_height() + result_clustering_CMeans.winfo_height() + 160 + 80

    label_counter_CMeans = Label(canvas_C,text="counter : ")
    label_counter_CMeans.pack()
    label_counter_CMeans.update()
    canvas_C.create_window((50, current_y), window=label_counter_CMeans, anchor="nw")
    counter_CMeans = Label(canvas_C,text=counter)
    counter_CMeans.pack()
    canvas_C.create_window((150, current_y), window=counter_CMeans, anchor="nw")
    counter_CMeans.update()
    canvas_C.configure(scrollregion=canvas_C.bbox("all"))



def clearGraph():
    if(len(canvas_g_K.winfo_children()) > 0):
        for child_k in canvas_g_K.winfo_children():
            child_k.destroy()
        canvas_g_K.update()

    if(len(canvas_g_C.winfo_children()) > 0):
        for c in canvas_g_C.winfo_children():
            c.destroy()
        canvas_g_C.update()

def createGraphK(init_canvas,x_k,y_k,c_k_x,c_k_y,l_k):
    # global canvas_g_K,canvas_g_K
    figure_K = plt.Figure(figsize=(5,4),dpi=70)
    #grid parameter means 1 x 1
    ax_k = figure_K.add_subplot(111)
    ax_k.scatter(x_k,y_k,c=l_k.astype(float),s=50,alpha=50)
    ax_k.scatter(c_k_x, c_k_y, c='red', s=70)
    scatter_K = FigureCanvasTkAgg(figure_K, init_canvas)
    scatter_K.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH,expand=FALSE)
    init_canvas.update()

def createGraphC(init_canvas,x_k,y_k,c_k_x,c_k_y,l_k):
    # global canvas_g_K,canvas_g_K

    figure_c = plt.Figure(figsize=(5,4),dpi=70)
    #grid parameter means 1 x 1
    ax_c = figure_c.add_subplot(111)
    ax_c.scatter(x_k,y_k,c=l_k.astype(float),s=50,alpha=50)
    ax_c.scatter(c_k_x, c_k_y, c='red', s=70)
    scatter_c = FigureCanvasTkAgg(figure_c, init_canvas)
    scatter_c.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH,expand=FALSE)
    init_canvas.update

def clearResult():
    canvas_C_child = canvas_C.winfo_children()
    canvas_K_child = canvas_K.winfo_children()

    if len(canvas_C_child) > 0 :
        for child_C in canvas_C_child:
            child_C.destroy()
        canvas_C.update()

    if len(canvas_K_child) > 0 :
        for child_K in canvas_K_child:
            child_K.destroy()
        canvas_K.update()



def updateLabel():
    dict_kdTree = {"depth": int(entry_depth.get())}
    dict_CMeans = {"maxter": int(entry_maxter.get())}

    clearGraph()
    clearResult()
    fun.process(n_cluster=entry_cluster.get(),dict_kdTree=dict_kdTree, dict_CMeans=dict_CMeans)
    result = fun.result
    data = result['data']
    KMeans = result["KMeans"]
    CMeans = result["CMeans"]

    createResultKMeans(iteration=result["KMeans"]["iteration"],clustering_centers=result["KMeans"]["cluster_center"],labels=result["KMeans"]["label_cluster"],dbi=result["KMeans"]["DBI"],times=result["KMeans"]["time"],counter=result["KMeans"]["counter"])
    createResultCMeans(iteration=result["CMeans"]["iteration"],clustering_centers=result["CMeans"]["cluster_center"],labels=result["CMeans"]["label_cluster"],dbi=result["CMeans"]["DBI"],times=result["CMeans"]["time"],counter=result["CMeans"]["counter"])
    createGraphK(init_canvas=canvas_g_K,x_k=data[:,0],y_k=data[:,1],c_k_x=KMeans['cluster_center'][:,0],c_k_y=KMeans['cluster_center'][:,1],l_k=KMeans['label_cluster'])
    createGraphC(init_canvas=canvas_g_C,x_k=data[:,0],y_k=data[:,1],c_k_x=CMeans['cluster_center'][:,0],c_k_y=CMeans['cluster_center'][:,1],l_k=CMeans['label_cluster'])

#process
button_process = tk.Button(labelframe_mid,background="red",fg="white",text="Process",command = lambda : updateLabel())
button_process.pack(pady=10,padx=10)

# root.geometry('%dx%d+%d+%d' % (w, h, x, y))
# root.geometry("%dx%d+0+0" % (w, h))

if __name__ == '__main__':
    root.mainloop()

