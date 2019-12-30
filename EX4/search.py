#search alg
import math
import copy

maxTruckLoad = 4
entitiesSupply = {"A":5,"B":3,"C":7}    #define demand
supplierSupply = {"S":100}#math.inf}         #define supply
isOutOfStock = False
entityMap = \
    {\
    "A":{"A":0,"B":2,"C":1,"S":11},\
    "B":{"A":2,"B":0,"C":4,"S":5},\
    "C":{"A":1,"B":4,"C":0,"S":8},\
    "S":{"A":11,"B":5,"C":8,"S":0}\
    }
truckLoad = 4

class Node:
    def __init__(self,entitiesDict,supplierDict,truck,residence,cost,roadHistory):
        self.entities = entitiesDict
        self.supplier = supplierDict
        self.truck = truck
        self.residence = residence
        self.accumulatedCost = cost
        self.roadHistory = roadHistory
        #print(entitiesDict,"|truck: ",self.truck,"|residing: ",self.residence,"|cost: ",self.accumulatedCost,"|")
    
    def setResidence(self,newResidence):
        self.residence = newResidence
        self.roadHistory.append(newResidence)
    
    def _isSupplied(self):
        for item in self.entities:
            if(self.entities[item] > 0):
                return False
        return True
    
    def _delivery(self,recipent):
        self.entities[recipent] -= self.truck
        self.truck = 0
        if(self.entities[recipent] < 0):
            self.truck += self.entities[recipent] * (-1)
            self.entities[recipent] = 0
    
    def loadUp(self):
        global isOutOfStock,maxTruckLoad
        newTruckLoad = maxTruckLoad
        if(self.supplier["S"] == 0):
            isOutOfStock = True
            return
        if(self.supplier["S"] < newTruckLoad):
            newTruckLoad = self.supplier["S"]
        self.supplier["S"] -= newTruckLoad
        self.truck = newTruckLoad
        
    def addCost(self,cost):
        self.accumulatedCost += cost
    
    def calculateCost(_from, _to):
        global entityMap
        return entityMap[_from][_to]
    
    def isTruckEmpty(self):
        return (self.truck == 0)
    
    
    def expand(node):
        expandedNodes = []
        if(node.isTruckEmpty()): 
            newNode = copy.deepcopy(node)
            newNode.setResidence("S")
            #newNode = Node(copy.deepcopy(node.entities),copy.deepcopy(node.supplier),0,"S",copy.deepcopy(node.accumulatedCost))
            newNode.addCost(Node.calculateCost(node.residence,newNode.residence))
            newNode.loadUp()
            expandedNodes.append(newNode)
            #print(newNode.entities,"|truck: ",newNode.truck,"|residing: ",newNode.residence,"|cost: ",newNode.accumulatedCost,"|")
            return expandedNodes
        for item in node.entities:
            if (node.entities[item] > 0 and node.entities[item] != node.residence):
                newNode = copy.deepcopy(node)
                newNode.setResidence(item)
                #newNode = Node(copy.deepcopy(node.entities),copy.deepcopy(node.supplier),copy.deepcopy(node.truck),item,copy.deepcopy(node.accumulatedCost))
                newNode.addCost(Node.calculateCost(node.residence,newNode.residence))
                newNode._delivery(item)
                expandedNodes.append(newNode)
                #print(newNode.entities,"|truck: ",newNode.truck,"|residing: ",newNode.residence,"|cost: ",newNode.accumulatedCost,"|")
        return expandedNodes
    
    def findLowestCostIndex(nodeList):
        cost = math.inf
        lowestCostNode = None
        for node in nodeList:
            if(node.accumulatedCost < cost):
                lowestCostNode = node
                cost = node.accumulatedCost
        return nodeList.index(lowestCostNode)
    
    def printNodes(nodeList):
        for node in nodeList:
            print(node.entities,"|truck: ",node.truck,"|residing: ",node.residence,"|cost: ",node.accumulatedCost,"|")


def blindSearchDFS():
    global entityMap,entitiesSupply,truckLoad
    supplySteps = []
    roadHistory = []
    truckResidence = "S"
    cost = 0
    supplySteps.append(entitiesSupply)
    while(not isSupplied(supplySteps[-1])):
        if(truckLoad == 0):
            roadHistory.append("S")
            truckResidence = "S"
            truckLoad = 4
            continue
        for item in supplySteps[-1]:
            if supplySteps[-1][item] > 0:
                newSupplyStep = copy.deepcopy(supplySteps[-1])
                delivery(item,newSupplyStep)
                supplySteps.append(newSupplyStep)
                roadHistory.append(item)
                truckResidence = item
                break
        print(supplySteps[-1])
    print(supplySteps,roadHistory,truckLoad)
    print("cost: ",calculateTotalCost(roadHistory))

def blindSearch(mode):
    global entityMap,entitiesSupply,truckLoad,isOutOfStock
    isOutOfStock = False
    position = 0
    if(mode == "BFS"):
        position = 0
    else:
        position = -1
    queue = []
    roadHistory = []
    truckResidence = "S"
    cost = 0
    queue.append(Node(copy.deepcopy(entitiesSupply),copy.deepcopy(supplierSupply),0,truckResidence,0,[truckResidence]))
    queue[0].loadUp()
    while(1):
        current = queue.pop(position)
        if(current._isSupplied()):
            print("found ",mode," path! ",current.entities,"|Total Cost: ", current.accumulatedCost,"| residence: ", current.residence)
            print("Path: ",current.roadHistory)
            break
        tmp = Node.expand(current)
        if (isOutOfStock):
            current = tmp[0]
            print("out of stock while: ",mode," search ", "|stock status: ",current.supplier,current.entities,"|Total Cost: ", current.accumulatedCost,"| residence: ", current.residence)
            print("Path: ",current.roadHistory)
            break
        queue.extend(tmp)

def heuresticSerach():
    global entityMap,entitiesSupply,truckLoad,isOutOfStock
    isOutOfStock = False
    queue = []
    roadHistory = []
    truckResidence = "S"
    cost = 0
    queue.append(Node(copy.deepcopy(entitiesSupply),copy.deepcopy(supplierSupply),0,truckResidence,0,[truckResidence]))
    queue[0].loadUp()
    while(1):
        current = queue.pop(Node.findLowestCostIndex(queue))
        
        if(current._isSupplied()):
            print("found heurestic path! ",current.entities,"|Total Cost: ", current.accumulatedCost,"| residence: ", current.residence)
            print("Path: ",current.roadHistory)
            break
        #Node.printNodes(queue)
        #print("expanding -> ",current.entities,"| cost: ",current.accumulatedCost)
        tmp = Node.expand(current)
        if(isOutOfStock):
            current = tmp[0]
            print("out of stock while: heurestic "," search ", "|stock status: ",current.supplier,current.entities,"|Total Cost: ", current.accumulatedCost,"| residence: ", current.residence)
            print("Path: ",current.roadHistory)
            break
        queue.extend(tmp)

def delivery(recipent,supplyList):
    global truckLoad
    supplyList[recipent] -= truckLoad
    truckLoad = 0
    if(supplyList[recipent] < 0):
        truckLoad += supplyList[recipent] * (-1)
        supplyList[recipent] = 0

def isSupplied(supplyList):
    for item in supplyList:
        if(supplyList[item] > 0):
            return False
    return True

def calculateTotalCost(roadHist):
    current = roadHist[0]
    cost = 0
    for i in range(1,len(roadHist)):
        to = roadHist[i]
        #print(current,"->",to," = ",entityMap[current][to])
        cost += entityMap[current][to]
        current = to
    return cost

if __name__ == '__main__':
    #blindSearchDFS()
    blindSearch("BFS")
    blindSearch("DFS")
    heuresticSerach()
