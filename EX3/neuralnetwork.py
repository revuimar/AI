import math
import numpy as np
from neuron import *
import random

class NeuralNetwork:
    def __init__(self,neuronTable,functionTable, learn_rate):
        self.neuronTable = neuronTable
        self.learn_rate = learn_rate
        self.functionTable = functionTable
        self.network = []
        print(range(len(neuronTable)))
        for layer in range(len(neuronTable)):
            self.network.append([])
            print(self.network)
            for node in range(neuronTable[layer]):
                if(layer == 0):
                    self.network[layer].append(Neuron([random.uniform(1,2),random.uniform(1,2),random.uniform(1,2)],functionTable[layer],[random.uniform(1,2),random.uniform(1,2),random.uniform(1,2)],learn_rate))
                else:
                    stuff = [random.uniform(1,2) for i in range(neuronTable[layer-1]+1)]
                    self.network[layer].append(Neuron(stuff,functionTable[layer],stuff,learn_rate))
    '''
                /-0-\         -> first appended neuron node
    x\  /-0-\  /     \  /--0    numer of inputs and weights determined 
      --     -----1-----        from number of nodes from previous layer
    y/  \-1-/  \     /  \--1  
                \-2-/         -> last appended neuron node
   layers 0-------1--------2
   resulting table: [[N0,N1],[N0,N1,N2],[N0,N1]]
    interpret output as one hot!!!
    2 cases one gave to be '0' other has to be '1'!!
    '''
    def setNetworkInput(self,inputTable):
        self.setLayerInputs(inputTable,0)

    def setLayerInputs(self,inputTable,layer):
        '''
        if(len(inputTable) != len(self.network[layer])):
            
            print("for layer: ",layer ," error lengths not coherent!")
            print("in: ",len(inputTable),", for: ",len(self.network[layer]))
            print(self.network)
            
            return
        '''
        for node in self.network[layer]:
            node.setInput(inputTable)

    def getLayerOutputs(self,layer):
        _output = []
        for node in self.network[layer]:
            _output.append(node.calculateOutput(False))
        return _output

    def getNetworkOutput(self,initialInput):
        _outTable = initialInput #for an elegant loop 
        for layer in range(len(self.neuronTable)):
            self.setLayerInputs(_outTable,layer)
            _outTable = self.getLayerOutputs(layer)
        return _outTable

    def refreshHiddenAndOutputLayer(self):
        for layer in range(len(self.neuronTable)):
            if layer == 0: 
                _outTable = self.getLayerOutputs(layer)
                continue
            self.setLayerInputs(_outTable,layer)
            _outTable = self.getLayerOutputs(layer)
    
    def getLayerSums(self,layer):
        _sums = []
        for node in self.network[layer]:
            _sums.append(node.calculateSum())
        return _sums

    def getLayerCorrection(self,layer,errors):
        weights = []
        for i in range(len(self.network[layer])):
            weights.append(self.network[layer][i].calculateCorrection(errors[i]))
        return weights

    def performLayerCorrection(self,layer,errors):
        
        for i in range(len(self.network[layer])):
            self.network[layer][i].performCorrection(errors[i])

    def backPropagate(self,reals):
        '''
        Wx Weight of the output node
        f'(Sx) value of derivative from upper node sum!
        deltax error of connected node
        example: we are on node '2' on layer '1'
        we need to iterate through (layer + 1)
        we take the error of this node and sum
        also keep track of your node position on the layer since it's
        identical to position of weight in weight table of connected node(rememer bias +1)
        '''
        #[0,1,2,3,4]
        #[1,2,3,4,5]
        #calculate resulte
        layer = len(self.network) - 1#start from last layer
        _currentErr = []
        _previousErr = []
        self.refreshHiddenAndOutputLayer()#put inputs across network in place
        _errors = []
        while(layer >= 0):
            if(layer == len(self.network)-1):
                #last layer case first
                i = 0
                for node in self.network[layer]:
                    _currentErr.append(node.calculateError(reals[i]))#append node error to list (used by lower layer) 
                    i=+1
                #self.performLayerCorrection(layer,_currentErr) # perform correction - it does not affect calculation(well it does)
                _errors.append(_currentErr)
                _previousErr = _currentErr # previous error for backpropagated calculation of errors of lower nodes
                _currentErr = []
                layer -= 1
                continue
            for i in range(len(self.network[layer])):
                #deltai = Sum_j(W_ij * f'(S_i+1) * delta_j) <- error calculation
                _nodeError_i = 0
                for j in range(len(self.network[layer+1])):
                    W_ij = self.network[layer+1][j].weights[i+1]# W_ij weight on ith node output +1 because of bias
                    derFunc = self.network[layer+1][j].calculateOutput(True)
                    delta_j = _previousErr[j]
                    _nodeError_i += W_ij * derFunc * delta_j # sum throug all j nodes
                _currentErr.append(_nodeError_i)
                #self.network[layer][i].performCorrection(_currentErr[i])
            _errors.append(_currentErr)
            _previousErr = _currentErr
            _currentErr = []
            layer -= 1
        return _errors

    def performNetworkCorrection(self,errors):
        #errors are in reverse layer order - from top to bottom
        layer = len(self.network) - 1#start from last layer
        while(layer >= 0):
            for i in range(len(self.network[layer])):
                self.network[layer][i].performCorrection(errors[layer][i])
            layer -= 1

    def getRealValue(function,correctXY):
        _reals = [Neuron.getRealValue(correctXY[0],function),
                  Neuron.getRealValue(correctXY[1],function)]
        return _reals

    def printWeights(self):
        for layer in range(len(self.network)):
            i =0
            for node in self.network[layer]:
                print("layer: ",layer,"node: ",i," -> ",node.weights)
                i+=1

    def train(self,redXY,bluXY):
        redCount = len(redXY[0])
        bluCount = len(bluXY[0])
        loops = 0
        while(True):
            #one-hot
            for i in range(redCount):
                self.setNetworkInput([redXY[0][i],redXY[1][i]])
                _reals = NeuralNetwork.getRealValue(self.functionTable[-1],[True,False])
                _errors = self.backPropagate(_reals)
                #print(_errors)
                self.performNetworkCorrection(_errors)
                #print("output: ", self.getNetworkOutput([redXY[0][i],redXY[1][i]]),"  REALS: ",_reals)
            for i in range(bluCount):
                self.setNetworkInput([bluXY[0][i],bluXY[1][i]])
                _reals = NeuralNetwork.getRealValue(self.functionTable[-1],[False,True])
                _errors = self.backPropagate(_reals)
                self.performNetworkCorrection(_errors)
                #print("output: ", self.getNetworkOutput([bluXY[0][i],bluXY[1][i]]),"  REALS: ",_reals)
            if(loops > 1000): break
            loops +=1
        self.printWeights()
        print("RED:", self.getNetworkOutput([redXY[0][12],redXY[1][12]]))
        print("BLUE:", self.getNetworkOutput([bluXY[0][12],bluXY[1][12]]))
    #todo Training, backpropagation!
            
