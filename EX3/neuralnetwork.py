import math
import numpy as np
from neuron import *
import random

class NeuralNetwork:
    
    def __init__(self,noInputs,neuronTable,functionTable, learn_rate):
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
        self.neuronTable = neuronTable
        self.learn_rate = learn_rate
        self.functionTable = functionTable
        self.network = []
        np.seterr('raise')
        print(range(len(neuronTable)))
        for layer in range(len(neuronTable)):
            self.network.append([])
            for node in range(neuronTable[layer]):
                if(layer == 0):
                    w = [random.uniform(0,1) for i in range(noInputs+1)]
                    inp = [1 for i in range(noInputs)]
                    print("generated layer ",layer," branch: ",w,inp)
                    self.network[layer].append(Neuron(inp,functionTable[layer],w,learn_rate))
                else:
                    w = [random.uniform(0,1) for i in range(neuronTable[layer-1]+1)]
                    inp = [1 for i in range(neuronTable[layer-1])]
                    print("generated ",layer," branch: ",w,inp)
                    self.network[layer].append(Neuron(inp,functionTable[layer],w,learn_rate))
        print(self.network)

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
            #print("for layer: ",layer," outputs: ",_outTable)
    
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
                _errors.insert(0,_currentErr)
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
            _errors.insert(0,_currentErr)
            _previousErr = _currentErr
            _currentErr = []
            layer -= 1
        #print("errors  ",_errors)
        return _errors

    def performNetworkCorrection(self,errors):
        #errors are in reverse layer order - from top to bottom
        layer = len(self.network) - 1#start from last layer
        #kek = errors.reverse()
        #print(errors)
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

    def train(self,redXY,bluXY,epochs):
        redCount = len(redXY[0])
        bluCount = len(bluXY[0])
        loops = 0
        while(True):
            #one-hot
            for i in range(redCount):
                self.setNetworkInput([redXY[0][i],redXY[1][i]])
                _reals = [Neuron.getRealValue(True,self.functionTable[-1]) for i in range(len(self.network[-1]))] #NeuralNetwork.getRealValue(self.functionTable[-1],[True,False])
                _reals[-1] = Neuron.getRealValue(False,self.functionTable[-1])
                #_reals = [Neuron.getRealValue(True,self.functionTable[-1])]
                _errors = self.backPropagate(_reals)
                #print(_errors)
                self.performNetworkCorrection(_errors)
                #print("output: ", self.getNetworkOutput([redXY[0][i],redXY[1][i]]))#,"  REALS: ",_reals)
            
            for i in range(bluCount):
                self.setNetworkInput([bluXY[0][i],bluXY[1][i]])
                __reals = [Neuron.getRealValue(True,self.functionTable[-1]) for i in range(len(self.network[-1]))] #NeuralNetwork.getRealValue(self.functionTable[-1],[True,False])
                _reals[0] = Neuron.getRealValue(False,self.functionTable[-1])
                #_reals = [Neuron.getRealValue(False,self.functionTable[-1])]
                _errors = self.backPropagate(_reals)
                self.performNetworkCorrection(_errors)
                #print("output: ", self.getNetworkOutput([bluXY[0][i],bluXY[1][i]]))#,"  REALS: ",_reals)
            
            if(loops > epochs): break
            loops +=1
        self.printWeights()
        return epochs
        #print("RED:", self.getNetworkOutput([redXY[0][12],redXY[1][12]]))
        #print("BLUE:", self.getNetworkOutput([bluXY[0][12],bluXY[1][12]]))
            
