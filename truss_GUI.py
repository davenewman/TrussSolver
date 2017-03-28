import tkinter as tk
from tkinter import ttk, END
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np
import copy

class Gui():
    def __init__(self, root):
        self.root = root

        # Doesn't look pretty when resizing = DISALLOW
        root.resizable(0,0)
        root.title("Indeterminate Truss Solver")


        frame = tk.Frame(self.root, padx=10,pady=10)
        frame.grid(row=0,column=0, sticky="nw")
        frame.grid_rowconfigure(6, minsize=25)
        frame.grid_rowconfigure(15, minsize=25)
        navFrame = tk.Frame(self.root)
        navFrame.grid(row=1,column=1,sticky="ew")
        

        label1 = tk.Label(frame, text="Node Coordinates").grid(row=0,column=1, sticky="nw")
        label2 = tk.Label(frame, text="Node X Coordinate").grid(row=1,column=0,sticky="nw")
        label3 = tk.Label(frame, text="Node Y Coordinate").grid(row=2,column=0,sticky="nw")
        label4 = tk.Label(frame, text="From Node ").grid(row=8,column=0,sticky="nw")
        label5 = tk.Label(frame, text="To Node ").grid(row=9,column=0,sticky="nw")
        label6 = tk.Label(frame, text="Members").grid(row=7,column=1,sticky="nw")
        label7 = tk.Label(frame, text="Elastic Modulus").grid(row=10,column=0,sticky="nw")
        label8 = tk.Label(frame, text="Area").grid(row=11,column=0,sticky="nw")
        label9 = tk.Label(frame, text="Loads/Supports").grid(row=16,column=1,sticky="nw")
        label10 = tk.Label(frame, text="Node").grid(row=17,column=0,sticky="nw")
        label11 = tk.Label(frame, text="Horizontal Component").grid(row=18,column=0,sticky="nw")
        label12 = tk.Label(frame, text="Vertical Component").grid(row=19,column=0,sticky="nw")
        label13 = tk.Label(frame, text="Support Condition").grid(row=20,column=0,sticky="nw")

        # initializing widgets
        self.xEntry = ttk.Entry(frame)
        self.yEntry = ttk.Entry(frame)
        self.toNode = ttk.Entry(frame)
        self.fromNode = ttk.Entry(frame)
        self.eEntry = ttk.Entry(frame)
        self.aEntry = ttk.Entry(frame)
        self.nodeEntry = ttk.Entry(frame)
        self.horEntry = ttk.Entry(frame)
        self.vertEntry = ttk.Entry(frame)
        drawButton_nodes = ttk.Button(frame,text="Draw",command=self.make_vectors_nodes)
        clearButton_nodes = ttk.Button(frame,text="Clear Nodes", command=self.clear_grid_nodes)
        goBackButton_nodes = ttk.Button(frame,text="Undo",command=self.undo_nodes)
        
        drawButton_forces = ttk.Button(frame,text="Draw",command=self.make_vectors_forces)###
        clearButton_forces = ttk.Button(frame,text="Clear Forces")
        goBackButton_forces = ttk.Button(frame,text="Undo")###

        # Special widget = drop down menu
        self.var = tk.StringVar()
        self.var.set("Free")
        dropMenu = ttk.OptionMenu(frame,self.var,"","Free","Fixed","Horizontal Roller","Vertical Roller")
        
        drawButton_members = ttk.Button(frame,text="Draw", command=self.make_vectors_members)
        clearButton_members = ttk.Button(frame,text="Clear Members", command=self.clear_grid_members)
        goBackButton_members = ttk.Button(frame,text="Undo", command=self.undo_members)

        # placing widgets in the frame
        self.fromNode.grid(row=8,column=1,sticky="we")
        self.toNode.grid(row=9,column=1,sticky="we")
        self.eEntry.grid(row=10,column=1,sticky="we")
        self.aEntry.grid(row=11,column=1,sticky="we")
        
        drawButton_nodes.grid(row = 3,column = 1, sticky = "we")
        clearButton_nodes.grid(row=4,column=1, sticky="we")
        goBackButton_nodes.grid(row=5,column=1,sticky="we")
        
        self.xEntry.grid(row = 1,column = 1,sticky = "we")
        self.yEntry.grid(row = 2,column = 1, sticky = "we")
        
        drawButton_members.grid(row=12,column=1,sticky="we")
        clearButton_members.grid(row=13,column=1,sticky="we")
        goBackButton_members.grid(row=14,column=1,sticky="we")
        
        dropMenu.grid(row=20,column=1,sticky="we")
        self.nodeEntry.grid(row=17,column=1,sticky="we")
        self.horEntry.grid(row=18,column=1,sticky="we")
        self.vertEntry.grid(row=19,column=1,sticky="we")
        
        drawButton_forces.grid(row=21,column=1,sticky="we")
        clearButton_forces.grid(row=22,column=1,sticky="we")
        goBackButton_forces.grid(row=23,column=1,sticky="we")
                                   
        # Vectors containing X and Y coords of each node
        # memberInfo = | From Node | To Node | E | A |
        # boolBC and valBC = | U1 | Q1 |
        
        self.x = []
        self.y = []
        self.memberInfo = []
        self.boolBC = []
        self.valBC = []
        
        self.f = plt.figure(figsize=(5.5,5.5), dpi=100)
        self.a = self.f.add_subplot(111)
        self.a.scatter(self.x,self.y)
        self.a.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        self.a.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))

        self.canvas=FigureCanvasTkAgg(self.f, root)
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, navFrame)
        self.toolbar.update()
        self.canvas.show()
        self.canvas.get_tk_widget().grid(row=0, column=1)

    def undo_nodes(self):
        if len(self.x)>0 and len(self.y)>0:
            del self.x[-1]
            del self.y[-1]
            self.update_plot_nodes()

    def undo_members(self):
        
        if len(self.memberInfo) > 0:
            del self.memberInfo[-1]
        self.update_plot_members(self.memberInfo,[self.x,self.y],'k--')

    def make_vectors_nodes(self):
        try:
            # Input Validation
            self.x.append(float(self.xEntry.get()))
            self.y.append(float(self.yEntry.get()))
        except ValueError:
            print('Need numbers, not whatever you typed in.')  #TODO: call error window
        if len(self.x) == len(self.y):
            self.update_plot_nodes()
        elif len(self.x)>len(self.y):
            del self.x[-1]
        else:
            del self.y[-1]
        # this is definitely a hack, but i need to initialize these arrays somehow...
        # just not every time this function is called
        #self.boolBC = 2*len(self.x)*[[False, True]]
        #self.valBC = 2*len(self.x)*[[0,0]]

        
    def make_vectors_members(self):
        try:
            # | From Node | To Node | E | A |
            self.memberInfo.append([float(self.fromNode.get()), float(self.toNode.get()), float(self.eEntry.get()), float(self.aEntry.get())])
        except ValueError:
            print('Need numbers, not whatever you typed in.') #TODO: call error window
        coords = [self.x, self.y]
        self.update_plot_members(self.memberInfo, coords, 'k--')

    def make_vectors_forces(self):

        #Should only enter this loop the first time
        if len(self.boolBC) == 0:
            self.boolBC = [[False, True] for y in range(2*len(self.x))]
            self.valBC = [[0, 0] for z in range(2*len(self.x))]

        try:
            nodeNum = int(self.nodeEntry.get())
            xComponent = float(self.horEntry.get())
            yComponent = float(self.vertEntry.get())
            supportCond = self.var.get()
        except ValueError:
            print('Input Error')#TODO: call error window
    
        self.valBC[2*nodeNum-2][1] = xComponent
        self.valBC[2*nodeNum-1][1] = yComponent

        #conditionals incoming "Free","Fixed","Horizontal Roller","Vertical Roller"
        if supportCond == 'Free':
            self.boolBC[2*index-2] = [False, True]
            self.boolBC[2*index-1] = [False, True]
        elif supportCond == 'Fixed':
            self.boolBC[2*index-2] = [True, False]
            self.boolBC[2*index-1] = [True, False]
        elif supportCond == 'Horizontal Roller':
            self.boolBC[2*index-2] = [False, True]
            self.boolBC[2*index-1] = [True, False]
        else:
            self.boolBC[2*index-2] = [True, False]
            self.boolBC[2*index-1] = [False, True]
        print(self.valBC)
        print(self.boolBC)
 
        

    def update_plot_members(self, memberInfo, coords, color):

        self.update_plot_nodes()
        
        for ind,row in enumerate(memberInfo):
            self.a.plot( [ coords[0][int(row[0]-1)], coords[0][int(row[1]-1)] ], [coords[1][int(row[0]-1)], coords[1][int(row[1]-1)]], color )
            self.a.text((coords[0][int(row[0]-1)] + coords[0][int(row[1]-1)])/2, (coords[1][int(row[0]-1)]+coords[1][int(row[1]-1)]+0.2)/2,str(ind+1),color='green')
        self.a.axis('equal')
        self.canvas.show()
        self.fromNode.delete(0,END)
        self.toNode.delete(0,END)
        self.eEntry.delete(0,END)
        self.aEntry.delete(0,END)
            

    def clear_grid_nodes(self):
        
        del self.x[:]
        del self.y[:]
        del self.memberInfo[:]
        self.update_plot_nodes()

    def clear_grid_members(self):
        del self.memberInfo[:]
        self.update_plot_members(self.memberInfo,[self.x,self.y],'k--')

    def update_plot_nodes(self):
        
        self.xEntry.delete(0,END)
        self.yEntry.delete(0,END)
        self.f.clf()
        self.a = self.f.add_subplot(111)
        self.a.scatter(self.x,self.y,color='k')
        for ind,val in enumerate(self.x):
            self.a.text(self.x[ind], self.y[ind]+0.1, str(ind+1),color='blue')
        self.a.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        self.a.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        self.a.axis('equal')
        self.canvas.show()



root=tk.Tk()
gui=Gui(root)
root.mainloop()
