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


fig, ax = [],[]
RED = 0
BLUE = 1
color_type = ('ro','bo')
mean = [[[-5,-5],[5,5]],[[10,10],[-10,-10]]]
cov = [[[[1, 2], [0.5, 2]],[[1, 2], [0.5, 2]]],[[[1, 0.3], [2, 0.5]],[[1, 2], [5, 6]]]]
samples = [1000,1000]
dataClass = []
classesNo = [2,2]
meanRange = [-100,100]
covRange = (-2,2)

def drawPlot(ID):
    global mean
    global cov
    global samples
    global dataClass
    global classesNo
    x,y = [],[]
    for i in range(classesNo[ID]):
        print(cov)
        print(cov[ID][i])
        _x,_y = np.random.multivariate_normal(mean[ID][i], cov[ID][i], samples[ID]).T
        x.extend(_x)
        y.extend(_y)
    print (len(x),len(y))
    return plt.plot(x, y, color_type[ID])

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
    x,y = [],[]
    x = np.random.uniform(_min,_max,2)
    y = np.random.uniform(_min,_max,2)
    covariance = [[x[0],x[1]],[y[0],y[1]]]
    return covariance

def plotDataUpdate(ID):
    x,y = [],[]
    global classesNo
    global mean
    global cov
    global samples
    global dataClass
    try:
        for i in range(classesNo[ID]):
            _x,_y = np.random.multivariate_normal(mean[ID][i], cov[ID][i], samples[ID]).T
            x.extend(_x)
            y.extend(_y)
    except:
        print("Incorrect data input!")
    dataClass[ID][0].set_xdata(x)
    dataClass[ID][0].set_ydata(y)
    ax.relim()
    ax.autoscale_view()
    plt.draw()



def initPlots():
    global fig,ax
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.29)
    plt.autoscale(enable=True, axis='both', tight=True)
    initsRegenerate(RED)
    initsRegenerate(BLUE)
    return fig,ax
    
class Index(object):
    ind = 0
    def REDregenerate(self,event):
        self.ind +=1
        initsRegenerate(RED)
        plotDataUpdate(RED)
    def BLUEregenerate(self,event):
        self.ind -=1
        initsRegenerate(BLUE)
        plotDataUpdate(BLUE)

def initGUI():
    #TextBox position variables (matplotlib.axes.Axes)
    RED_boxAxis = plt.axes([0.15, 0.05, 0.32, 0.05])
    RED_sampleBoxAxis = plt.axes([0.15, 0.11, 0.32, 0.05])
    BLUE_boxAxis = plt.axes([0.61, 0.05, 0.32, 0.05])
    BLUE_sampleBoxAxis = plt.axes([0.61, 0.11, 0.32, 0.05])
    meanBoxAxis = plt.axes([0.4, 0.17, 0.32, 0.05])
    #Button position variables (matplotlib.axes.Axes)
    RED_axButton = plt.axes([0.15, 0.17, 0.15, 0.05])
    BLUE_axButton = plt.axes([0.78, 0.17, 0.15, 0.05])
    #buttons
    RED_button = Button(RED_axButton, 'Regen Red',color = 'red')
    BLUE_button = Button(BLUE_axButton, 'Regen Blue',color = 'blue')
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

    #on_submit event handlers
    RED_textBox.on_submit(lambda value: submitNo(RED,RED_textBox.text))
    BLUE_textBox.on_submit(lambda value: submitNo(BLUE,BLUE_textBox.text))
    meantextBox.on_submit(lambda value: submitMean(meantextBox.text))
    RED_sampletextBox.on_submit(lambda value: submitSamples(RED,RED_sampletextBox.text))
    BLUE_sampletextBox.on_submit(lambda value: submitSamples(BLUE,BLUE_sampletextBox.text))
    callback = Index()
    RED_button.on_clicked(callback.REDregenerate)
    BLUE_button.on_clicked(callback.BLUEregenerate)
    plt.show()
    return callback,RED_button,BLUE_button

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
    initGUI()
    plt.show()
