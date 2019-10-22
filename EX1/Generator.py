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
from matplotlib.widgets import TextBox

fig, ax = [],[]
RED = 0
BLUE = 1
color = ('ro','bo')
mean = [[-1,0],[0,1]]
cov = [[[1, 2], [0.5, 1/2]],[[1, 0.3], [2, 0.5]]]
samples = [1000,1000]
dataClass = []

def drawPlot(ID):
    x,y = np.random.multivariate_normal(mean[ID], cov[ID], samples[ID]).T
    return plt.plot(x, y, color[ID])



def randomMultivariateMean(_min,_max):
    return np.random.uniform(_min,_max,2)
    
def plotDataUpdate(ID):
    x,y = 0,0
    try:
        x,y = np.random.multivariate_normal(mean[ID], cov[ID], samples[ID]).T
    except:
        print("Incorrect data input!")
    dataClass[ID][0].set_xdata(x)
    dataClass[ID][0].set_ydata(y)
    ax.relim()
    ax.autoscale_view()
    plt.draw()



def initPlots():
    plt.subplots_adjust(bottom=0.29)
    plt.autoscale(enable=True, axis='both', tight=True)
    return 0
    
def initGUI():
    #TextBox position variables (matplotlib.axes.Axes)
    RED_boxAxis = plt.axes([0.15, 0.05, 0.32, 0.05])
    RED_meanBoxAxis = plt.axes([0.15, 0.17, 0.32, 0.05])
    RED_sampleBoxAxis = plt.axes([0.15, 0.11, 0.32, 0.05])
    BLUE_boxAxis = plt.axes([0.61, 0.05, 0.32, 0.05])
    BLUE_meanBoxAxis = plt.axes([0.61, 0.17, 0.32, 0.05])
    BLUE_sampleBoxAxis = plt.axes([0.61, 0.11, 0.32, 0.05])
    #TextBox text boxes
    
    RED_textBox = TextBox(RED_boxAxis, 'Covariance\nRED', initial=str(cov[RED]))
    RED_textBox.label.set_wrap(True)
    RED_meantextBox = TextBox(RED_meanBoxAxis, 'Mean\nRED', initial=str(mean[RED]))
    RED_meantextBox.label.set_wrap(True)
    RED_sampletextBox = TextBox(RED_sampleBoxAxis, 'Samples\nRED', initial=str(samples[RED]))
    RED_sampletextBox.label.set_wrap(True)
    BLUE_textBox = TextBox(BLUE_boxAxis, 'Covariance\nBLUE', initial=str(cov[BLUE]))
    BLUE_textBox.label.set_wrap(True)
    BLUE_meantextBox = TextBox(BLUE_meanBoxAxis, 'Mean\nBLUE', initial=str(mean[BLUE]))
    BLUE_meantextBox.label.set_wrap(True)
    BLUE_sampletextBox = TextBox(BLUE_sampleBoxAxis, 'Samples\nBLUE', initial=str(samples[BLUE]))
    BLUE_sampletextBox.label.set_wrap(True)
    #on_submit event handlers
    RED_textBox.on_submit(lambda value: submitCov(RED,RED_textBox.text))
    BLUE_textBox.on_submit(lambda value: submitCov(BLUE,BLUE_textBox.text))
    RED_meantextBox.on_submit(lambda value: submitMean(RED,RED_meantextBox.text))
    BLUE_meantextBox.on_submit(lambda value: submitMean(BLUE,BLUE_meantextBox.text))
    RED_sampletextBox.on_submit(lambda value: submitSamples(RED,RED_sampletextBox.text))
    BLUE_sampletextBox.on_submit(lambda value: submitSamples(BLUE,BLUE_sampletextBox.text))
    return 0

def submitCov(ID, input_string):
    newCovariance = [[0,0],[0,0]]
    try:
        newCovariance = eval(input_string)
        cov[ID] = newCovariance
    except:
        print("Parsing Error!")
        
    plotDataUpdate(ID)
    
def submitMean(ID, input_string):
    newMean = [0,0]
    try:
        newMean = eval(input_string)
        mean[ID] = newMean
    except:
        print("Parsing Error!")
        
    plotDataUpdate(ID)
    
def submitSamples(ID, input_string):
    newSamples = 1
    try:
        newSamples = eval(input_string)
        samples[ID] = newSamples
    except:
        print("Parsing Error!")
        
    plotDataUpdate(ID)
    
if __name__ == '__main__':
    fig, ax = plt.subplots()
    initPlots()
    dataClass = [drawPlot(RED),drawPlot(BLUE)]
    initGUI()
    plt.show()
