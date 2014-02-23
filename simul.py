import numpy as np
from random import *
from scipy.stats import norm

#parameters
pop = 10
runs = 100

#vars
avg_node_pk = 0
avg_finalnode_pk = 0

#delegation function
def dele(pk):
    x = 1-norm.cdf(pk)
    y = random()
    if x > y:
        return 1    # delegate
    else:
        return 0    # not delegate

#which nodes links to this node, function
def linksto(node):
    return np.where(list[2]==node)[0]

#structure parsing function
def counter(pot,level,dels):
    #print "we're now at level =",level
    for i in pot:
        dels[0].append(i)
        dels[1].append(level)
        #print "i=",i
        a = linksto(i)
        #print 'a=',a
        for b in a:
            b = [b]
            counter(b,level+1,dels)
    #level -= 1
    #print "we're back to level =",level
    return dels

for p in range(runs):

    #set up initial array
    list = np.zeros((5,pop))
    # 1: final voting power (VP)
    # 2: pk
    # 3: delegate to who?
    # 4: will you delegate? yes/no: 1/0
    # 5: VP that has been delegated

    #put in PK values
    list[0,:] = 1
    for i in range(pop):
        list[1,i] = gauss(0,1)

    #sort after PK value
    list = np.sort(list,1)  # sorting after voting power

    #fill in delegations
    for i in range(pop):
        list[3,i] = dele(list[1,i])

    #list=np.array([[0,0,0,0,0,0,0,7,0,3,1],[0,0,0,0,0,0,0,0,0,0,0],[5,5,6,8,5,6,7,0,9,0,0],[1,1,1,1,1,1,1,0,1,0,0],[1,1,1,1,1,4,6,7,2,3,1]])

    #decide if it actually delegates
    x=1
    j=0
    while x>0:
        x=0
        for i in range(pop-1):
            if list[0,i]>0:
                list[4,i] = list[0,i]
                if list[3,i]==1:
                    p = randint(i+1,pop-1)
                    list[0,p] += list[0,i]
                    list[2,i] = p
                    list[0,i] = 0
                    x+=1
        list[4,pop-1] = list[0,pop-1]
        #print x
        #j+=1
        #print j
        #print list[0,:]
        #print list[2,:]
        #print list[3,:]
        #print list[4,:]

    #find top nodes
    top = np.where((list[0]-list[4])==0)[0] # list of highest rank nodes
    #print top

    #replace DT=0 with -1 (to prevent infinite loops with counter function
    for n, i in enumerate(list[2]):
        if i==0:
            list[2,n] = -1

    #print list[2]

    #call the counter function
    dels = [[],[]]
    level = 0
    d = counter(top,0,dels)
    print d

    #average PK of all nodes
    sum = 0
    for i in list[1]:
        sum = sum+i
    avg_node_pk = avg_node_pk+(sum/pop)

    #average FNP of all final nodes
    sum = 0
    for i in top:
        sum += list[1,i]*list[0,i]
    avg_finalnode_pk += sum/pop

#divide by number of runs
avg_node_pk = avg_node_pk/runs
avg_finalnode_pk = avg_finalnode_pk/runs

#print "avg. node PK of ",runs," is ",avg_node_pk
print "avg. finalnode PK of ",runs," is ",avg_finalnode_pk