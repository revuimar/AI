'''
Requrements
Prepare a GUI that enables generation and visualization of data samples from two classes. 
Samples should be two-dimensional, so that they can be plotted in x-y space. 
Each class should consist of one or more gaussian modes1 with their means 
and variances chosen randomly from some given inteval (e.g. μx, μy ∈ [−1..1]).
The interface should allow for setting a desired number of modes per class and a desired number of samples per mode, 
as well as visualization of the generated samples on a two-dimensional plot. 
Class labels, which are either 0 or 1, should be indicated by colors.
'''
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import TextBox,Button
import itertools
import copy
from neuralnetwork import *

fig, ax = [],[]
RED = 0
BLUE = 1
color_type = ('ro','bo')
mean = [[[-5,-5],[5,5]],[[10,10],[-10,-10]]]
cov = [[[[1, 2], [0.5, 2]],[[1, 2], [0.5, 2]]],[[[1, 0.3], [2, 0.5]],[[1, 2], [5, 6]]]]
samples = [100,100]
meshDensity = 200
dataClass = []
classesNo = [2,2]
meanRange = [-20,20]
covRange = (-2,2)
neuralNetwork = None
colorbar = None
grid = None
function = "sig_func"
x = [[],[]]
y = [[],[]]

def train():
    global neuralNetwork,x,y
    print("training iter: ",neuralNetwork.train([x[RED],y[RED]],[x[BLUE],y[BLUE]]))
    
def drawPlot(ID):
    global mean
    global cov
    global samples
    global dataClass
    global classesNo
    global x,y

    for i in range(classesNo[ID]):
        _x,_y = np.random.multivariate_normal(mean[ID][i], cov[ID][i], samples[ID]).T
        x[ID].extend(_x)
        y[ID].extend(_y)
    return ax.plot(x[ID], y[ID], color_type[ID])

def redraw(ID):
    return ax.plot(x[ID], y[ID], color_type[ID])

def initsRegenerate(ID):
    global mean
    global cov
    mean.pop(ID)
    mean.insert(ID,[])
    cov.pop(ID)
    cov.insert(ID,[])
    for i in range(classesNo[ID]):
        mean[ID].insert(i,randomMultivariateMean(meanRange[0],meanRange[1]))
        cov[ID].insert(i,randomCov(covRange[0],covRange[1]))
    

def randomMultivariateMean(_min,_max):
    newmean = np.random.uniform(_min,_max,2)
    return [newmean[0],newmean[1]]

def randomCov(_min,_max):
    _x,_y = [],[]
    _x = np.random.uniform(_min,_max,2)
    _y = np.random.uniform(_min,_max,2)
    covariance = [[_x[0],_x[1]],[_y[0],_y[1]]]
    return covariance

def mapCurrentView():
    xLim = ax.get_xlim()
    yLim = ax.get_ylim()
    _x = np.linspace(xLim[0], xLim[1], meshDensity) 
    _y = np.linspace(yLim[0], yLim[1], meshDensity) 
    x_1,y_1 =  np.meshgrid(_x, _y)
    return [x_1,y_1]

def neuralValorisation(_map):
    values = copy.deepcopy(_map[0])
    for i in range(meshDensity):
        for j in range(meshDensity):
            table = [_map[0][i,j],_map[1][i,j]]
            outputTable = neuralNetwork.getNetworkOutput(table)
            #print(outputTable)
            if(outputTable[0] > 0.8 and outputTable[1] > 0.8):
                values[i,j] = outputTable[0]
            if(outputTable[0] >0.8 and outputTable[1] < 0.2):
                values[i,j] = outputTable[1]
            if(outputTable[0] < 0.2 and outputTable[1] > 0.8):
                values[i,j] = outputTable[0]
            if(outputTable[0] < 0.2 and outputTable[1] < 0.2):
                values[i,j] = outputTable[0]
            '''
            if(outputTable[0] == outputTable[1]):
                values[i,j] = outputTable[0]
            else:
                values[i,j] = 0.5
            '''
    return values

def drawFieldDiv():
    global grid,colorbar
    if(grid != None):
        del grid
    _map = mapCurrentView()
    grid = ax.pcolormesh(_map[0],_map[1],neuralValorisation(_map),cmap='jet',alpha = 0.1)

def plotDataUpdate(ID):
    global classesNo,plotFill,mean,cov,samples,dataClass, neurPlot,neuron,x,y
    try:
        x.pop(ID)
        x.insert(ID,[])
        y.pop(ID)
        y.insert(ID,[])
        for i in range(classesNo[ID]):
            _x,_y = np.random.multivariate_normal(mean[ID][i], cov[ID][i], samples[ID]).T
            x[ID].extend(_x)
            y[ID].extend(_y)
    except:
        print("Incorrect data input!")
    dataClass[ID][0].set_xdata(x[ID])
    dataClass[ID][0].set_ydata(y[ID])
    

def plotUpdate():
    ax.cla()
    redraw(RED)
    redraw(BLUE)
    drawFieldDiv()
    ax.relim()
    ax.autoscale_view()
    plt.draw()
    

def initPlots():
    global fig,ax
    global cov
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.29)
    plt.autoscale(enable=True, axis='both', tight=True)
    fig.colorbar(plt.cm.ScalarMappable( cmap='jet'), ax=ax)
    initsRegenerate(RED)
    initsRegenerate(BLUE)
    return fig,ax

class Index(object):
    ind = 0
    def regenerate(self,event):
        global neuralNetwork
        self.ind +=1
        del neuralNetwork
        neuralNetwork = NeuralNetwork([2,3,2],function,0.5)
        initsRegenerate(RED)
        initsRegenerate(BLUE)
        plotDataUpdate(RED)
        plotDataUpdate(BLUE)
        plotUpdate()
    def training(self,event):
        self.ind -=1
        train()
    def refresh(self,event):
        plotUpdate()
        self.ind -=10
        
def initGUI():
    #TextBox position variables (matplotlib.axes.Axes)
    RED_boxAxis = plt.axes([0.15, 0.05, 0.32, 0.05])
    RED_sampleBoxAxis = plt.axes([0.15, 0.11, 0.32, 0.05])
    BLUE_boxAxis = plt.axes([0.61, 0.05, 0.32, 0.05])
    BLUE_sampleBoxAxis = plt.axes([0.61, 0.11, 0.32, 0.05])
    meanBoxAxis = plt.axes([0.63, 0.17, 0.12, 0.05])
    Train_boxAxis = plt.axes([0.15, 0.17, 0.15, 0.05])
    #Button position variables (matplotlib.axes.Axes)
    Train_axButton = plt.axes([0.31, 0.17, 0.1, 0.05])
    Reg_axButton = plt.axes([0.78, 0.17, 0.15, 0.05])
    Refresh_axButton = plt.axes([0.43, 0.17, 0.1, 0.05])
    #buttons
    Train_button = Button(Train_axButton, 'Train',color = 'green')
    Reg_button = Button(Reg_axButton, 'Regenerate')
    Refresh_button = Button(Refresh_axButton, 'Refresh')
    #TextBox text boxes
    
    RED_textBox = TextBox(RED_boxAxis, 'Modes\nRED', initial=str(classesNo[RED]))
    RED_textBox.label.set_wrap(True)
    meantextBox = TextBox(meanBoxAxis, 'Mean\nRange', initial=str(meanRange))
    meantextBox.label.set_wrap(True)
    RED_sampletextBox = TextBox(RED_sampleBoxAxis, 'Samples\nRED', initial=str(samples[RED]))
    RED_sampletextBox.label.set_wrap(True)
    BLUE_textBox = TextBox(BLUE_boxAxis, 'Modes\nBLUE', initial=str(classesNo[BLUE]))
    BLUE_textBox.label.set_wrap(True)
    BLUE_sampletextBox = TextBox(BLUE_sampleBoxAxis, 'Samples\nBLUE', initial=str(samples[BLUE]))
    BLUE_sampletextBox.label.set_wrap(True)
    Train_TextBox = TextBox(Train_boxAxis, 'Func',initial=str(function))

    #on_submit event handlers
    RED_textBox.on_submit(lambda value: submitNo(RED,RED_textBox.text))
    BLUE_textBox.on_submit(lambda value: submitNo(BLUE,BLUE_textBox.text))
    meantextBox.on_submit(lambda value: submitMean(meantextBox.text))
    RED_sampletextBox.on_submit(lambda value: submitSamples(RED,RED_sampletextBox.text))
    BLUE_sampletextBox.on_submit(lambda value: submitSamples(BLUE,BLUE_sampletextBox.text))
    Train_TextBox.on_submit(setFunction)
    callback = Index()
    Train_button.on_clicked(callback.training)
    Refresh_button.on_clicked(callback.refresh)
    Reg_button.on_clicked(callback.regenerate)

    plt.show()
    return callback

def setFunction(input_string):
    global function
    function = input_string

def submitNo(ID, input_string):
    newNo = 0
    global classesNo
    try:
        newNo = int(input_string)
        classesNo[ID] = newNo
    except:
        print("Parsing Error!")
    initsRegenerate(ID)
    #plotDataUpdate(ID)
    
def submitMean(input_string):
    newMeanRange = [0,0]
    global meanRange 
    try:
        newMeanRange = eval(input_string)
        meanRange = newMeanRange
    except:
        print("Parsing Error!")
    initsRegenerate(BLUE)
    initsRegenerate(RED)
    
    
def submitSamples(ID, input_string):
    newSamples = 1
    global samples
    try:
        newSamples = int(input_string)
        samples[ID] = newSamples
    except:
        print("Parsing Error!")
    

    
if __name__ == '__main__':
    initPlots()
    dataClass = [drawPlot(RED),drawPlot(BLUE)]
    neuralNetwork = NeuralNetwork([2,3,2],function,0.5)#Neuron([1,1,1],function,[1,1,1],0.1)
    drawFieldDiv()
    initGUI()
    plt.show()

