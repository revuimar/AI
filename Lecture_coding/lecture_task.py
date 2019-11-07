'''
    LEcture live coding
'''

class Node:
    def __init__(self,missionaries,cannibals,boat):
        self.missionaries = missionaries
        self.cannibals = cannibals
        self.boat = boat
    def isSolution(self):
        return (str(self.missionaries) + str(self.cannibals) + self.boat == "00R")

    def expand(node):
        expanded = []
        if(node.boat == "L"):
            expanded.append(Node(node.missionaries-1,node.cannibals,"R"))
            expanded.append(Node(node.missionaries,node.cannibals-1,"R"))
            expanded.append(Node(node.missionaries-2,node.cannibals,"R"))
            expanded.append(Node(node.missionaries-1,node.cannibals-1,"R"))
            expanded.append(Node(node.missionaries,node.cannibals-2,"R"))
        else:
            expanded.append(Node(node.missionaries + 1,node.cannibals,"L"))
            expanded.append(Node(node.missionaries,node.cannibals+1,"L"))
            expanded.append(Node(node.missionaries + 2,node.cannibals,"L"))
            expanded.append(Node(node.missionaries + 1,node.cannibals + 1,"L"))
            expanded.append(Node(node.missionaries,node.cannibals + 2,"L"))
        return expanded


    def toString(self):
        return (str(self.missionaries) + str(self.cannibals) + self.boat)
    def serialise(listOfObj):
        ser = []
        for element in listOfObj: ser.append(element.toString())
        return ser

    def filterLegalStates(list_tmp):
        newlist = []
        for element in list_tmp:
            if(element.missionaries < 0 or element.missionaries > 3):
                continue
            if(element.cannibals < 0 or element.cannibals > 3):
                continue
            if(element.cannibals > element.missionaries):
                continue
            newlist.append(element)
        #print("{",Node.serialise(newlist),"}")
        return newlist
        
    
    def filterNovelStates(list_tmp):
        return None


state = Node(3,3,"L")
#test = Node(0,0,"R")
Q=[]
Q.append(state)
Tracker = [[state.toString()]]
size_tracker = [1]
first = 1
while(1):
    current = Q.pop(0)
    size_tracker[0] -= 1
    
    if(size_tracker[0] == 0):
        size_tracker.pop(0)
        Tracker.append([])
    else:#elif(size_tracker[-1] > 0):
        Tracker[-1].append(current.toString())
    if(first):
        print (size_tracker)
        first=0
    if(current.isSolution()):
        count = 0
        layer = []
        for e in Tracker:
            layer_no = len[e]
            for i in range(layer_no)
                layer.append(e)
            print(e)
        print("im out")
        break
    tmp = Node.expand(current)
    tmp = Node.filterLegalStates(tmp)
    size_tracker.append(len(tmp))
    #tmp = filterNovelStates(tmp)
    Q.extend(tmp)
    
