
'''

Implement an articial neuron. The neuron should take samples 
generated by a code from the task 1 as its input 
and predict their class membership at its output.
The neuron should be trainable through the formula presented during the lecture:
    ∆wj =ηεf′(s)xj =η(d−y)f′(wTxj)xj (1)
where:
• xj is the jth sample
• f′(s) is the derivative of the activation function evaluated 
for the jth sample 
• w are the weights associated with inputs
• η is the learning rate
• d is the expected (true) class label
• y is a class label predicted by the neuron

'''
import math
import numpy as np

class Neuron:
    def __init__(self,_input,act_func, weights, learn_rate):
        self._input = _input
        self.act_func = act_func
        self.weights = weights
        self.learn_rate = learn_rate
    
    def setInput(self,_input):
        i_2 = 0
        for i in range(len(self._input)):
            if i == 0: 
                continue
            else: 
                self._input[i] = _input[i_2]
            i_2 += 1
    
    def setWeight(self,weights):
        self.weights = weights
    
    def setLearnRate(self,learn_rate):
        self.learn_rate = learn_rate
    def setActivationFunction(self,new_func):
        self.act_func = new_func

    #neuron functions
    def step_func(s,isDerivative):
        if(isDerivative):
            return 1
        else:
            return 0 if s< 0 else 1

    def sig_func(s,isDerivative):
        base = 1/(1+math.exp(s))
        if(isDerivative):
            return base*(1-base)
        else:
            return base

    def sin_func(s,isDerivative):
        if(isDerivative):
            return math.cos(s)
        else:
            return math.sin(s)

    def tanh_func(s,isDerivative):
        if(isDerivative):
            return 1-(math.tanh(s)**2)
        else:
            return math.tanh(s)

    def sign_func(s,isDerivative):
        result = 1
        if(isDerivative):
            return result
        else:
            result = -1 if s<0  else 1
            return result

    def relu_func(s,isDerivative):
        if(isDerivative):
            return 1 if s> 0 else 0
        else:
            return s if s> 0 else 0

    def leaky_relu_func(s,isDerivative):
        if(isDerivative):
            return 1 if s> 0 else 0.01
        else:
            return s if s> 0 else 0.01*s

    Functions = {
        "step_func": step_func,
        "sig_func":sig_func,
        "sin_func":sin_func,
        "tanh_func":tanh_func,
        "sign_func":sign_func,
        "relu_func":relu_func,
        "leaky_func":leaky_relu_func
    }

    def calculateSum(self):
        return np.dot(self._input,self.weights)

    def calculateValue(self,isDerivative,val):
        out = Neuron.Functions[self.act_func](val,isDerivative)
        return out

    def calculateOutput(self,isDerivative):
        s = self.calculateSum() + self.weights[0]
        out = Neuron.Functions[self.act_func](s,isDerivative)
        return out

    def calculateCorrection(self,real):
        #  ∆wj = η(d−y)f′(wTxj)xj
        delta = real - self.calculateOutput(False) #(d-y)
        fPrime = self.calculateOutput(True) #f'(wTxj)
        correction = []
        for element in self._input:
            correction.append(self.learn_rate * delta * fPrime * element)
        #returns table of ∆wj-corrections per weight
        return correction

    def performCorrection(self,real):
        correction = self.calculateCorrection(real)
        w = self.weights
        for i in range(len(w)):
            w[i] += correction[i]
        self.setWeight(w)
        
    def getRealValue(self,isDataCorrect):
        if self.act_func == ("step_func")\
            or self.act_func == ("sig_func")\
            or self.act_func == ("sin_func")\
            or self.act_func == ("relu_func")\
            or self.act_func == ("leaky_func"):
            return 1 if isDataCorrect else 0
        elif self.act_func == ("tanh_func")\
            or self.act_func == ("sign_func"):
            return 1 if isDataCorrect else -1
        
    def isAccurate(self, side1,side2):
        self.setInput(side1)
        result1 = self.calculateOutput(False)
        self.setInput(side2)
        result2 = self.calculateOutput(False)
        return result1 > result2

    def train(self, redXY,blueXY, treshold):
        loops = 0
        while(True):
            loops += 1
            acc = 0
            for i in range(len(redXY[0])):
                _side1 = [redXY[0][i],redXY[1][i]]
                _side2 = [blueXY[0][i],blueXY[1][i]]
                self.setInput(_side1)
                self.performCorrection(self.getRealValue(True))
                self.setInput(_side2)
                self.performCorrection(self.getRealValue(False))
                if self.isAccurate(_side1,_side2): acc+=1
            if ((loops) > 1000) or (acc == 100): 
                print("accuracy: ",acc,"  on: ",self.act_func)
                print("new w",self.weights)
                break
        return loops
