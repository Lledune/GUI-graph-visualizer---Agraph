from tkinter import *
from tkinter import ttk, messagebox
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import *
import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import palettable
from matplotlib.colors import ListedColormap

mpl.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import os
import community
import palettable as pal


#paths names
dirname = os.path.dirname(__file__)
dataOne = os.path.join(dirname, 'data/lesmiserables.gexf')
dataTwo = os.path.join(dirname, 'data/airlines-sample.gexf')
dataThree = os.path.join(dirname, 'data/karate.gml')
dirDic = {
    "Les miserables" : dataOne,
    "Airlines" : dataTwo,
    "Karate" : dataThree
}

#Color settings
bgCol = "#0088AA"
fgCol = "#B7C8C4"

#Global variables
global fArray
fArray = [] #Array for figures

global fI
fI = 0 #counter for keeping track of current graph

global fCount
fCount = 0

#Global arguments
global toolbar
toolbar = None
global globalLayout
globalLayout = "0" #0 = kamada, 1 = circular, 2 = spectral, 3 = shell

global globalData
globalData = "path"

global globalImport
globalImport = dirDic["Les miserables"]

global globalColMet
globalColMet = 0 #metrics to be defined, but same principle as globalLayout

global globalSizeMet
globalSizeMet = 0 #idem

global globalSize
globalSize = 10

global globalFilter
globalFilter = 0 #idem

global globalFilterThreshold
globalFilterThreshold = 0

global f
f = 0 #plot

global checkedImport
checkedImport = False

global globalImported
globalImported = "path"

global checkedLabel
checkedLabel = False

global globalColCom
globalColCom = False

global globalOptionsMet2
globalOptionsMet2 = ""

global cmap1
cmap1 = ""

global maxSize
maxSize = 100

global globalOptionsMet3
globalOptionsMet3 = "Default"

global globalOptionsMet4
globalOptionsMet4 = "Default"

global threshold
threshold = 100

# Testing networkx and importing test file
f = plt.Figure(figsize = (5,4), facecolor = bgCol)
a = f.add_subplot(111)
a.set_facecolor(fgCol)
path = dataOne
G = nx.read_gexf(dataOne, relabel = True)
pos = nx.circular_layout(G)
nx.draw_networkx(G, pos = pos, ax = a, with_labels=False)
xlim = a.get_xlim()
ylim = a.get_ylim()
plt.axis('off')
a.set_title('Circular', fontsize = 30, color = "white")
fCount = fCount + 1
fArray.append(f)

#####################
#Utility functions
#####################
#Import
def openFile():
    global globalImported
    globalImported = askopenfilename(parent = window)
    print(globalImported)

def normalize(val, max, min):
    val = ((val-min)/max)
    return val

def normalizeSize(val, max, min, m):
    val = ((val-min)/max)*m
    return val

#Refresh global variables (take widget values)
def refreshGlobals():

    global maxSize
    maxSize = int(sizeEntry.get())

    global globalLayout
    globalLayout = radioVar.get()

    global threshold
    threshold = float(filterEntry.get())

    global cmap1
    cmap1 = optionsCombo5.get()

    global globalData
    globalData = optionsCombo1.get()

    global globalOptionsMet2
    globalOptionsMet2 = optionsCombo2.get()

    global globalOptionsMet3
    globalOptionsMet3 = optionsCombo3.get()

    global globalOptionsMet4
    globalOptionsMet4 = optionsCombo4.get()

    global checkedLabel
    checkedLabel = useLabelChecked.get()

    global globalImport
    global checkedImport
    checkedImport = useImportChecked.get()
    print("checked : ", checkedImport)
    if(checkedImport == False):
        globalImport = dirDic[optionsCombo1.get()]
    if(checkedImport == True):
        globalImport = globalImported

    global globalColMet
    globalColMet = 0  #todo

    global globalSizeMet
    globalSizeMet = 0  # idem #todo

    global globalSize
    globalSize = 10 #todo

    global globalFilter
    globalFilter = 0  # todo

    global globalFilterThreshold
    globalFilterThreshold = 0 #todo

    #print(globalData) #Can use this line to print on console the variable you want

################
#Plot functions
################
#Main refresh
def refreshPlot():
    #counter
    global fCount
    fCount = fCount + 1
    global fI
    fI = fCount - 1

    #refreshing all parameters
    refreshGlobals()
    global canvasWidget
    canvasWidget.destroy()
    global f
    f = 0
    arg = globalLayout

    #Drawing
    if (arg == "0"):
        f = drawKamada(globalImport, "Kamada-kawai", "white", 30, checkedLabel)
    if (arg == "1"):
        f = drawCircular(globalImport, "Circular", "white", 30, checkedLabel)
    if (arg == "2"):
        f = drawSpiral(globalImport, "Spiral", "white", 30, checkedLabel)
    if (arg == "3"):
        f = drawFruchterman(globalImport, "Fruchterman-reingold", "white", 30, checkedLabel)
    if (arg == "4"):
        f = drawPlanar(globalImport, "Planar", "white", 30, checkedLabel)
    #storing graph

    global fArray
    fArray.append(f)

    canvas = FigureCanvasTkAgg(f, frame)
    canvas.draw()
    canvasWidget = canvas.get_tk_widget()
    canvasWidget.grid(row=2, column=1, columnspan=16, rowspan=12, sticky=N + S + W + E)
    global toolbar
    toolbar.destroy()
    toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)

def prevRefresh():
    global fI
    print(fI)
    if(fI >= 1):
        #Destroying canvas
        global canvasWidget
        canvasWidget.destroy()
        #Getting f prev graph
        global f
        f = fArray[fI - 1]
        #Changing canvas and toolbar
        canvas = FigureCanvasTkAgg(f, frame)
        canvas.draw()
        canvasWidget = canvas.get_tk_widget()
        canvasWidget.grid(row=2, column=1, columnspan=16, rowspan=12, sticky=N + S + W + E)
        global toolbar
        toolbar.destroy()
        toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
        fI = fI - 1
    else:
        messagebox.showerror(title="Agraph", message="There is no previous graph.")

def nextRefresh():
    global fI
    global fCount
    print(fI)
    if(fI < fCount-1):
        #Destroying canvas
        global canvasWidget
        canvasWidget.destroy()
        #Getting f prev graph
        global f
        f = fArray[fI + 1]
        #Changing canvas and toolbar
        canvas = FigureCanvasTkAgg(f, frame)
        canvas.draw()
        canvasWidget = canvas.get_tk_widget()
        canvasWidget.grid(row=2, column=1, columnspan=16, rowspan=12, sticky=N + S + W + E)
        global toolbar
        toolbar.destroy()
        toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
        fI = fI + 1
    else:
        messagebox.showerror(title="Agraph", message="There is no next graph.")

# DRAW THE GRAPH WITH OR WITHOUT COMMUNITIES

def drawGraph(G, pos, a, labels):

    #Changing G for threshold here


    #Check filter metric
    if(globalOptionsMet4 == "Default"):
        G = G

    if (globalOptionsMet4 == "Degree"):
        displayedNodes = []
        nx.set_node_attributes(G, values=nx.degree_centrality(G), name='degree')
        for node, data in G.nodes(data=True):
            if (data['degree'] > threshold):
                displayedNodes.append(node)
        G = G.subgraph(displayedNodes)

    if (globalOptionsMet4 == "Between Centrality"):
        displayedNodes = []
        # Metrics computing
        betweenCentralities = nx.betweenness_centrality(G)
        # Add metrics as params of the nodes
        nx.set_node_attributes(G, values=betweenCentralities, name='betweenCentrality')

        # iterate trough nodes
        for node, data in G.nodes(data=True):
            if (data['betweenCentrality'] > threshold):
                displayedNodes.append(node)

        G = G.subgraph(displayedNodes)

    if (globalOptionsMet4 == "Load Centrality"):
        # Metrics computing
        loadCentralities = nx.load_centrality(G)
        # Add metrics as params of the nodes
        nx.set_node_attributes(G, values=loadCentralities, name='loadCentrality')

        # iterate trough nodes
        for node, data in G.nodes(data=True):
            if (data['loadCentrality'] > threshold):
                displayedNodes.append(node)

        G = G.subgraph(displayedNodes)

    if (globalOptionsMet4 == "Subgraph Centrality"):
        # Metrics computing
        subgraphCentralities = nx.subgraph_centrality(G)
        # Add metrics as params of the nodes
        nx.set_node_attributes(G, values=subgraphCentralities, name='subgraphCentrality')

        # iterate trough nodes
        for node, data in G.nodes(data=True):
            if (data['subgraphCentrality'] > threshold):
                displayedNodes.append(node)

        G = G.subgraph(displayedNodes)

    #Choosing size,  the size list will be defined here for the rest of the function
    sizeM = maxSize
    sizes = []
    if(globalOptionsMet3 == "Default"):
        for node, data in G.nodes(data=True):
            sizes.append(sizeM)
    if(globalOptionsMet3 == "Degree"):
        degrees = nx.degree_centrality(G)
        # Add metrics as params of the nodes
        nx.set_node_attributes(G, values=degrees, name='degree')
        # minmax
        minDeg = min(degrees.values())
        maxDeg = max(degrees.values())
        #loop trough nodes
        for node, data in G.nodes(data=True):
            sizes.append((normalizeSize(data['degree'], maxDeg, minDeg, sizeM) + 5))

    if(globalOptionsMet3 == "Between Centrality"):
        # Metrics computing
        betweenCentralities = nx.betweenness_centrality(G)
        # Add metrics as params of the nodes
        nx.set_node_attributes(G, values=betweenCentralities, name='betweenCentrality')
        # minmax
        minBetween = min(betweenCentralities.values())
        maxBetween = max(betweenCentralities.values())
        #loop trough nodes
        for node, data in G.nodes(data=True):
            sizes.append((normalizeSize(data['betweenCentrality'], maxBetween, minBetween, sizeM) + 5))

    if(globalOptionsMet3 == "Load Centrality"):
        # Metrics computing
        loadCentralities = nx.load_centrality(G)
        # Add metrics as params of the nodes
        nx.set_node_attributes(G, values=loadCentralities, name='loadCentrality')
        # minmax
        minLoad = min(loadCentralities.values())
        maxLoad = max(loadCentralities.values())
        #loop trough nodes
        for node, data in G.nodes(data=True):
            sizes.append((normalizeSize(data['loadCentrality'], maxLoad, minLoad, sizeM) + 5))

    if(globalOptionsMet3 == "Subgraph Centrality"):
        # Metrics computing
        subgraphCentralities = nx.subgraph_centrality(G)
        # Add metrics as params of the nodes
        nx.set_node_attributes(G, values=subgraphCentralities, name='subgraphCentrality')
        # minmax
        minSub = min(subgraphCentralities.values())
        maxSub = max(subgraphCentralities.values())
        #loop trough nodes
        for node, data in G.nodes(data=True):
            sizes.append((normalizeSize(data['subgraphCentrality'], maxSub, minSub, sizeM) + 5))

    #Choosing cmap for colors
    cmapChosen = plt.cm.viridis
    if(cmap1 == "Viridis"):
        cmapChosen = plt.cm.viridis
    if(cmap1 == "Magma"):
        cmapChosen = plt.cm.magma

    if(globalOptionsMet2 == "Default"):
            nx.draw_networkx(G, pos=pos, ax=a, with_labels=labels, node_color = range(len(G)), cmap = cmapChosen, node_size = sizes)
    if(globalOptionsMet2 == "Communities"):
        cmapUsed = ""
        if(cmap1 == "Viridis"):
            cmapUsed = ListedColormap(palettable.colorbrewer.qualitative.Set3_12.mpl_colors, N = len(G))
        if(cmap1 == "Magma"):
            cmapUsed = ListedColormap(palettable.colorbrewer.qualitative.Set1_9.mpl_colors, N = len(G))

        partition = community.best_partition(G)
        labelSet = nx.get_node_attributes(G, 'label')
        size = float(len(set(partition.values())))
        count = 0.
        for com in set(partition.values()) :
            count = count + 1.
            list_nodes = [nodes for nodes in partition.keys() if partition[nodes] == com]
            nx.draw_networkx_nodes(G, pos, list_nodes, label = labelSet, node_color = cmapUsed(com), ax = a, node_size=sizes)
        nx.draw_networkx_edges(G, pos, alpha=0.5, ax = a)
        if(labels):
            nx.draw_networkx_labels(G, pos , ax = a)
    if(globalOptionsMet2 == "Degree"):
        # Metrics computing
        degrees = nx.degree_centrality(G)
        # Add metrics as params of the nodes
        nx.set_node_attributes(G, values=degrees, name='degree')

        # minmax
        minDeg = min(degrees.values())
        maxDeg = max(degrees.values())

        colDeg = []

        # Set the colors that could be used next
        for node, data in G.nodes(data=True):
            colDeg.append(normalize(data['degree'], maxDeg, minDeg))

        nx.draw_networkx(G, pos = pos, vmax=1, vmin=0, cmap = cmapChosen, with_labels=labels, node_size=sizes, node_color=colDeg, ax = a)

    if (globalOptionsMet2 == "Between Centrality"):
        # Metrics computing
        betweenCentralities = nx.betweenness_centrality(G)

        # Add metrics as params of the nodes
        nx.set_node_attributes(G, values=betweenCentralities, name='betweenCentrality')

        # minmax
        minBetween = min(betweenCentralities.values())
        maxBetween = max(betweenCentralities.values())

        colBetween = []

        # Set the colors that could be used next
        for node, data in G.nodes(data=True):
            colBetween.append(normalize(data['betweenCentrality'], maxBetween, minBetween))

        nx.draw_networkx(G, pos = pos, vmax=1, vmin=0, cmap = cmapChosen, with_labels=labels, node_size=sizes, node_color=colBetween, ax = a)
    if (globalOptionsMet2 == "Subgraph Centrality"):
        # Metrics computing
        subgraphCentralities = nx.subgraph_centrality(G)

        # Add metrics as params of the nodes
        nx.set_node_attributes(G, values=subgraphCentralities, name='subgraphCentrality')

        # minmax
        minSub = min(subgraphCentralities.values())
        maxSub = max(subgraphCentralities.values())

        colSub = []

        # Set the colors that could be used next
        for node, data in G.nodes(data=True):
            colSub.append(normalize(data['subgraphCentrality'], maxSub, minSub))

        nx.draw_networkx(G, pos = pos, vmax=1, vmin=0, cmap = cmapChosen, with_labels=labels, node_size=sizes, node_color=colSub, ax = a)
    if (globalOptionsMet2 == "Load Centrality"):
        # Metrics computing
        loadCentralities = nx.load_centrality(G)

        # Add metrics as params of the nodes
        nx.set_node_attributes(G, values=loadCentralities, name='loadCentrality')

        # minmax
        minLoad = min(loadCentralities.values())
        maxLoad = max(loadCentralities.values())

        colLoad = []

        # Set the colors that could be used next
        for node, data in G.nodes(data=True):
            colLoad.append(normalize(data['loadCentrality'], maxLoad, minLoad))

        nx.draw_networkx(G, pos = pos, vmax=1, vmin=0, cmap = cmapChosen, with_labels=labels, node_size=sizes, node_color=colLoad, ax = a)


###########################################################################
#The 4 functions below return f, a Figure that is then drawn on the canvas.
#Circular
def drawCircular(dataPath, titleString = "Title", color = "white", fontSize = 30, labels = False):
    global f
    f = plt.Figure(figsize=(5,4), facecolor=bgCol)
    a = f.add_subplot(111)
    a.set_facecolor(fgCol)

    #Data extension checking, supports gml and gexf
    fileName, fileExtension = os.path.splitext(dataPath)
    gexfBool = (fileExtension == ".gexf")
    gmlBool = (fileExtension == ".gml")
    print(gexfBool, gmlBool)
    #GEXF
    if(gexfBool):
        G = nx.read_gexf(dataPath, relabel=False)
        try:
            G = nx.read_gexf(dataPath, relabel=True, version = "1.1draft")
        except nx.NetworkXError:
            try:
                G = nx.read_gexf(dataPath, relabel=True, version="1.2draft")
            except nx.NetworkXError:
                messagebox.showerror(title="Agraph", message="There was duplicate on labels, using node number instead.")
                G = nx.read_gexf(dataPath, relabel=False)

    if(gmlBool):
        gmlLabelsBool = 'label'
        if(labels == False):
            gmlLabelsBool = None
        try:
            G = nx.read_gml(dataPath, label = gmlLabelsBool)
        except nx.NetworkXError:
            messagebox.showerror(title="Agraph", message="Error in file labels, one node or more may not have 'label' attribute. Labels will be replaced with node ID.")
            G = nx.read_gml(dataPath, label = None)

    pos = nx.circular_layout(G)
    drawGraph(G, pos, a, labels)
    xlim = a.get_xlim()
    ylim = a.get_ylim()
    plt.axis('off')
    a.set_title(titleString, fontsize=fontSize, color=color)
    return f


#Kamada
def drawKamada(dataPath, titleString = "Title", color = "white", fontSize = 30, labels = False):
    global f
    f = plt.Figure(figsize=(5,4), facecolor=bgCol)
    a = f.add_subplot(111)
    a.set_facecolor(fgCol)

    #Data extension checking, supports gml and gexf
    fileName, fileExtension = os.path.splitext(dataPath)
    gexfBool = (fileExtension == ".gexf")
    gmlBool = (fileExtension == ".gml")

    if(gexfBool):
        try:
            G = nx.read_gexf(dataPath, relabel=True, version = "1.1draft")
        except nx.NetworkXError:
            try:
                G = nx.read_gexf(dataPath, relabel=True, version="1.2draft")

            except nx.NetworkXError:
                messagebox.showerror(title="Agraph", message="There was duplicate on labels, using node number instead.")
                G = nx.read_gexf(dataPath, relabel=False)

    if(gmlBool):
        gmlLabelsBool = 'label'
        if(labels == False):
            gmlLabelsBool = None
        try:
            G = nx.read_gml(dataPath, label = gmlLabelsBool)
        except nx.NetworkXError:
            messagebox.showerror(title="Agraph", message="Error in file labels, one node or more may not have 'label' attribute. Labels will be replaced with node ID.")
            G = nx.read_gml(dataPath, label = None)


    pos = nx.kamada_kawai_layout(G)
    drawGraph(G, pos, a, labels)
    plt.axis('off')
    a.set_title(titleString, fontsize=fontSize, color=color)
    return f

def drawFruchterman(dataPath, titleString="Title", color="white", fontSize=30, labels=False):
    global f
    f = plt.Figure(figsize=(5, 4), facecolor=bgCol)
    a = f.add_subplot(111)
    a.set_facecolor(fgCol)

    #Data extension checking, supports gml and gexf
    fileName, fileExtension = os.path.splitext(dataPath)
    gexfBool = (fileExtension == ".gexf")
    gmlBool = (fileExtension == ".gml")

    if(gexfBool):
        G = nx.read_gexf(dataPath, relabel=False)
        try:
            G = nx.read_gexf(dataPath, relabel=True, version = "1.1draft")
        except nx.NetworkXError:
            try:
                G = nx.read_gexf(dataPath, relabel=True, version="1.2draft")
            except nx.NetworkXError:
                messagebox.showerror(title="Agraph", message="There was duplicate on labels, using node number instead.")
                G = nx.read_gexf(dataPath, relabel=False)

    if(gmlBool):
        gmlLabelsBool = 'label'
        if(labels == False):
            gmlLabelsBool = None
        try:
            G = nx.read_gml(dataPath, label = gmlLabelsBool)
        except nx.NetworkXError:
            messagebox.showerror(title="Agraph", message="Error in file labels, one node or more may not have 'label' attribute. Labels will be replaced with node ID.")
            G = nx.read_gml(dataPath, label = None)

    pos = nx.fruchterman_reingold_layout(G)
    drawGraph(G, pos, a, labels)
    xlim = a.get_xlim()
    ylim = a.get_ylim()
    plt.axis('off')
    a.set_title(titleString, fontsize=fontSize, color=color)
    return f


#Spectral
def drawSpiral(dataPath, titleString = "Title", color = "white", fontSize = 30, labels = False):
    global f
    f = plt.Figure(figsize=(5,4), facecolor=bgCol)
    a = f.add_subplot(111)
    a.set_facecolor(fgCol)

    # Data extension checking, supports gml and gexf
    fileName, fileExtension = os.path.splitext(dataPath)
    gexfBool = (fileExtension == ".gexf")
    gmlBool = (fileExtension == ".gml")

    if(gexfBool):
        G = nx.read_gexf(dataPath, relabel=False)
        try:
            G = nx.read_gexf(dataPath, relabel=True, version = "1.1draft")
        except nx.NetworkXError:
            try:
                G = nx.read_gexf(dataPath, relabel=True, version="1.2draft")

            except nx.NetworkXError:
                messagebox.showerror(title="Agraph", message="There was duplicate on labels, using node number instead.")
                G = nx.read_gexf(dataPath, relabel=False)

    if(gmlBool):
        gmlLabelsBool = 'label'
        if(labels == False):
            gmlLabelsBool = None
        try:
            G = nx.read_gml(dataPath, label = gmlLabelsBool)
        except nx.NetworkXError:
            messagebox.showerror(title="Agraph", message="Error in file labels, one node or more may not have 'label' attribute. Labels will be replaced with node ID.")
            G = nx.read_gml(dataPath, label = None)

    pos = nx.drawing.spiral_layout(G)
    drawGraph(G, pos, a, labels)
    xlim = a.get_xlim()
    ylim = a.get_ylim()
    plt.axis('off')
    a.set_title(titleString, fontsize=fontSize, color=color)
    return f

#Shell
def drawPlanar(dataPath, titleString = "Title", color = "white", fontSize = 30, labels = False):
    global f
    f = plt.Figure(figsize=(5,4), facecolor=bgCol)
    a = f.add_subplot(111)
    a.set_facecolor(fgCol)

    # Data extension checking, supports gml and gexf
    fileName, fileExtension = os.path.splitext(dataPath)
    gexfBool = (fileExtension == ".gexf")
    gmlBool = (fileExtension == ".gml")

    if(gexfBool):
        G = nx.read_gexf(dataPath, relabel=False)
        try:
            G = nx.read_gexf(dataPath, relabel=True, version = "1.1draft")
        except nx.NetworkXError:
            try:
                G = nx.read_gexf(dataPath, relabel=True, version="1.2draft")

            except nx.NetworkXError:
                messagebox.showerror(title="Agraph", message="There was duplicate on labels, using node number instead.")
                G = nx.read_gexf(dataPath, relabel=False)

    if(gmlBool):
        gmlLabelsBool = 'label'
        if(labels == False):
            gmlLabelsBool = None
        try:
            G = nx.read_gml(dataPath, label = gmlLabelsBool)
        except nx.NetworkXError:
            messagebox.showerror(title="Agraph", message="Error in file labels, one node or more may not have 'label' attribute. Labels will be replaced with node ID.")
            G = nx.read_gml(dataPath, label = None)

    pos = nx.drawing.planar_layout(G)
    drawGraph(G, pos, a, labels)
    xlim = a.get_xlim()
    ylim = a.get_ylim()
    plt.axis('off')
    a.set_title(titleString, fontsize=fontSize, color=color)
    return f


#Default graph to be displayed
fCirc = drawCircular(dataOne, "Circular", "white", 30, False)


#####################
#Main window config #
#####################

#Show main window
window = Tk()
window.title("A-graph")
window.geometry("1124x780")
window.minsize(1024, 720)
window.resizable(width=False, height=False)

#background color
window.config(background = bgCol)
window.iconbitmap(os.path.join(dirname, 'agraph.ico'))

#################
#Widgets
#################

#frame
frame = Frame(window, bg = bgCol, bd = 1, relief = SUNKEN)
toolbarFrame = Frame(master = window)

#Radiochoice (exclusive choice)
radioVals = ["0","1","2","3","4"]
radioText = ["Kamada", "Circular", "Spiral", "Fruchterman", "Planar"]
radioVar = StringVar(window)
radioVar.set(radioVals[0])
kamada = Radiobutton(frame, variable = radioVar, text = radioText[0], value = radioVals[0], bg = bgCol, fg = fgCol, font = "Courrier")
circular = Radiobutton(frame, variable = radioVar, text = radioText[1], value = radioVals[1], bg = bgCol, font = "Courrier",fg = fgCol)
spectral = Radiobutton(frame, variable = radioVar, text = radioText[2], value = radioVals[2], bg = bgCol, font = "Courrier",fg = fgCol)
fruchterman = Radiobutton(frame, variable = radioVar, text = radioText[3], value = radioVals[3], bg = bgCol, font = "Courrier",fg = fgCol)
planar = Radiobutton(frame, variable = radioVar, text = radioText[4], value = radioVals[4], bg = bgCol, font = "Courrier",fg = fgCol)
buttonHeight= 5
buttonWidth = 11
#kamada.configure(width = buttonWidth, height = buttonHeight)
#circular.configure(width = buttonWidth, height = buttonHeight)
#spectral.configure(width = buttonWidth, height = buttonHeight)
#shell.configure(width = buttonWidth, height = buttonHeight)


#Buttons
refreshButt = Button(frame, text = "Refresh",bg = fgCol, fg =bgCol,font = "Courrier, 20", command=refreshPlot)
loadButt = Button(frame, text = "Import",bg = fgCol, fg =bgCol,font = "Courrier, 20", command = openFile)
exitButton = Button(frame, text = "Exit", bg = fgCol, fg = bgCol, font = "Courrier, 20")
nextButton = Button(frame, text = "Next", bg = fgCol, fg = bgCol, font = "Courrier, 20", command = nextRefresh)
prevButton = Button(frame, text = "Previous", bg = fgCol, fg = bgCol, font = "Courrier, 20", command = prevRefresh)
buttHeight = 1
buttWidth = 7
#refreshButt.configure(width = buttWidth, height = buttHeight)
#loadButt.configure(width = buttWidth, height = buttHeight)
#exitButton.configure(width = buttWidth, height = buttHeight)


#labels
colorLabel = Label(frame, text = "Color",fg = fgCol, bg =bgCol,font = "Courrier, 20")
sizeLabel = Label(frame, text = "Size",fg = fgCol, bg =bgCol,font = "Courrier, 20")
filterLabel = Label(frame, text = "Filter",fg = fgCol, bg =bgCol,font = "Courrier, 20")
layoutLabel = Label(frame, text = "Layout : ",fg = fgCol, bg =bgCol,font = "Courrier, 20")

#Checkbutton
global useImportChecked
useImportChecked = BooleanVar(window)
useImportCheck = Checkbutton(frame, text = "Use import ", variable = useImportChecked, background = bgCol, fg = fgCol, activebackground = bgCol, onvalue = True)
global useLabelChecked
useLabelChecked = BooleanVar(window)
useLabelCheck = Checkbutton(frame, text = "Use labels", variable = useLabelChecked, background = bgCol, fg = fgCol, activebackground = bgCol, onvalue = True)

#text entries
sizeEntry  = Entry(frame)
sizeEntry.insert(END, '100')
filterEntry = Entry(frame)
filterEntry.insert(END, '100')
#déroulantes
optionData = ("Les miserables", "Airlines", "Karate")
optionsCombo1 = ttk.Combobox(frame, values = optionData)
optionsCombo1.current(0)

optionMetrics2 = ("Default","Communities", "Degree", "Between Centrality", "Subgraph Centrality", "Load Centrality")
optionsCombo2 = ttk.Combobox(frame, values = optionMetrics2)
optionsCombo2.current(0)

optionMetrics3 = ("Default", "Degree", "Between Centrality", "Subgraph Centrality", "Load Centrality")
optionsCombo3 = ttk.Combobox(frame, values = optionMetrics3)
optionsCombo3.current(0)

optionMetrics4 = ("Default", "Degree", "Between Centrality", "Subgraph Centrality", "Load Centrality")
optionsCombo4 = ttk.Combobox(frame, values = optionMetrics4)
optionsCombo4.current(0)

optionMetrics5 = ("Viridis", "Magma")
optionsCombo5 = ttk.Combobox(frame, values = optionMetrics5)
optionsCombo5.current(0)

#Canvas
# =============================================================================
# canvas = FigureCanvasTkAgg(f, master = frame)
# canvas.show()
# canvas.get_tk_widget().grid(column = 2, row = 1, columnspan = 12, rowspan = 8)
#
# =============================================================================
canvas = FigureCanvasTkAgg(f, frame)
canvas.draw()
canvasWidget = canvas.get_tk_widget()

##############
#GridSpacing
##############
for i in range(0,21):
    frame.grid_columnconfigure(i, minsize = 49)
frame.grid_columnconfigure(13, minsize = 0)

for i in range(0,15):
    frame.grid_rowconfigure(i, minsize = 51)
#########################
#Gridlayout  Configure
#########################
frame.grid(column = 0, row = 0, columnspan = 21, rowspan = 15, sticky = N + S + W + E)
kamada.grid(column = 1, row = 0, columnspan = 3, sticky = N + S + W + E)
circular.grid(column = 4, row = 0, columnspan = 3, sticky = N + S + W + E)
spectral.grid(column = 7, row = 0, columnspan = 3, sticky = N + S + W + E)
fruchterman.grid(column = 10, row = 0, columnspan = 3, sticky = N + S + W + E)
optionsCombo1.grid(column = 14, row = 0, columnspan = 4, sticky = N + S + W + E)
useImportCheck.grid(column = 16, row = 1, columnspan = 2)
useLabelCheck.grid(column = 14, row = 1, columnspan = 2)
refreshButt.grid(column = 19, row = 0, columnspan = 3, sticky = N + S + W + E)
loadButt.grid(column = 19, row = 1, columnspan = 3, sticky = N + S + W + E)
colorLabel.grid(column = 19, row = 3, columnspan = 3, sticky = N + S + W + E)
optionsCombo2.grid(column = 19, row = 4, columnspan = 3, sticky = N + S + W + E)
optionsCombo5.grid(column = 19, row = 5, columnspan = 3, sticky = N + S + W + E)
sizeLabel.grid(column = 19, row = 6, columnspan = 3, sticky = N + S + W + E)
optionsCombo3.grid(column = 19, row = 7, columnspan = 3, sticky = N + S + W + E)
sizeEntry.grid(column = 19, row = 8, columnspan = 3, sticky = N + S + W + E)
filterLabel.grid(column = 19, row = 9, columnspan = 3, sticky = N + S + W + E)
optionsCombo4.grid(column = 19, row = 10, columnspan = 3, sticky = N + S + W + E)
filterEntry.grid(column = 19, row = 11, columnspan = 3, sticky = N + S + W + E)
prevButton.grid(column = 15, row = 14, columnspan = 2, sticky = N + S + W + E)
nextButton.grid(column = 17, row = 14, columnspan = 2, sticky = N + S + W + E)
layoutLabel.grid(column = 0, row = 0, columnspan = 1, sticky = N + S + W + E)
canvasWidget.grid(row=2, column=1, columnspan = 16, rowspan = 12,sticky = N + S + W + E)
canvas.draw()
#toolbar
toolbarFrame.grid(column = 0, row = 14, columnspan = 10)
toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)



#print(radioVar)
window.mainloop()