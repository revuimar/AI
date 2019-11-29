import math
import numpy as np
from neuron import *

class NeuralNetwork:
    def __init__(self,neuronTable,functionTable, learn_rate):
        self.neuronTable = neuronTable
        self.learn_rate = learn_rate
        self.network = []
        for layer in range(len(neuronTable)):
            self.network.append([])
            for node in range(neuronTable[layer]):
                if(layer == 0):
                    self.network[layer].append(Neuron([1,1,1],"step_func",[1,1,1],0.5))
                    self.network[layer].append(Neuron([1,1,1],"step_func",[1,1,1],0.5))
                else:
                    stuff = [1 for i in range(neuronTable[layer-1])+1]
                    self.network[layer].append(Neuron(stuff,"step_func",stuff,0.5))
    '''
                /-0-\         -> first appended neuron node
    x\  /-0-\  /     \  /--0    numer of inputs and weights determined 
      --     -----1-----        from number of nodes from previous layer
    y/  \-1-/  \     /  \--1  
                \-2-/         -> last appended neuron node
   layers 0-------1--------2
   resulting table: [[N0,N1],[N0,N1,N2],[N0,N1]]
    '''
    def setLayerInputs(self,inputTable,layer):
        if(len(inputTable) != len(network[layer])):
            print("error lengths not coherent!")
            return
        for node in range(network[layer]):
            node.setInput(inputTable)

    def getLayerOutputs(self,layer):
        _output = []
        for node in range(network[layer]):
            _output.append(node.calculateOutput(False))
        return _output

    def getNetworkOutput(self,initialInput):
        outTable = initialInput #for an elegant loop 
        for layer in range(len(self.neuronTable)):
            self.setLayerInputs(outTable,layer)
            outTable = self.getLayerOutputs(layer)
        return outTable
    #todo Training, backpropagation!
            
