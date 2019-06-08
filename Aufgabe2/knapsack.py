from collections import namedtuple


class Knapsack:
    def __init__(self, triangles, capacity):
        self.triangles = list(triangles)
        self.w = [t[0] for t in triangles]
        self.v =  [t[1] for t in triangles]
        self.capacity = capacity

    def main(self):
        w = self.w
        v = self.v
        maxCost = self.capacity
        answer = self.zeroOneKnapsack(v,w,maxCost)
        result = []
        for i in range(len(answer[1])):
            if (answer[1][i] != 0):
                result.append(self.triangles[i])
        return result

    def zeros(self, rows, cols):
        row = []
        data = []
        for i in range(cols):
            row.append(0)
        for i in range(rows):
            data.append(row[:])
        return data

    def getItemsUsed(self, w,c):
        # item count
        i = len(c)-1
        # weight
        currentW =  len(c[0])-1
        
        # set everything to not marked
        marked = []
        for i in range(i+1):
            marked.append(0)	
            
        while (i >= 0 and currentW >=0):
            # if this weight is different than
            # the same weight for the last item
            # then we used this item to get this profit
            #
            # if the number is the same we could not add
            # this item because it was too heavy		
            if (i==0 and c[i][currentW] >0 )or c[i][currentW] != c[i-1][currentW]:
                marked[i] =1
                currentW = currentW-w[i]
            i = i-1
        return marked
	
    # v = list of item values or profit
    # w = list of item weight or cost
    # W = max weight or max cost for the knapsack
    def zeroOneKnapsack(self, v, w, W):
        # c is the cost matrix
        c = []
        n = len(v)
        #  set inital values to zero
        c = self.zeros(n,W+1)
        #the rows of the matrix are weights
        #and the columns are items
        #cell c[i,j] is the optimal profit
        #for i items of cost j
        
        #for every item
        for i in range(0,n):
            #for ever possible weight
            for j in range(0,W+1):
                #if this weight can be added to this cell
                #then add it if it is better than what we aready have
                
                if (w[i] > j):
                    
                    # this item is to large or heavy to add
                    # so we just keep what we aready have
                    
                    c[i][j] = c[i-1][j] 
                else:
                    # we can add this item if it gives us more value
                    # than skipping it
                    
                    # c[i-1][j-w[i]] is the max profit for the remaining 
                    # weight after we add this item.
                    
                    # if we add the profit of this item to the max profit
                    # of the remaining weight and it is more than 
                    # adding nothing , then it't the new max profit
                    # if not just add nothing.
                    
                    c[i][j] = max(c[i-1][j],v[i] + c[i-1][j-w[i]])
                    
        return [c[n-1][W],  self.getItemsUsed(w,c)]
