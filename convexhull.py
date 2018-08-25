"""
   Convex Hull Assignment: COSC262 (2018)
   Student Name: Xiao Meng
   Usercode: xme14
"""
import time

def theta(ptA, ptB):
    '''computes an approximation of the angle between the line AB and a horizontal line through A'''
    dx = ptB[0] - ptA[0]
    dy = ptB[1] - ptA[1]
    if abs(dx) < 1.e-6 and abs(dy) < 1.e-6:
        t = 0
    else:
        t = dy/(abs(dx) + abs(dy))      
    if dx < 0:
        t = 2 - t
    elif dy < 0:
        t = 4 + t
    return t * 90


def lineFn(ptA, ptB, ptC):
    '''return a line segment(Pt0, Pt1)'''
    return (
        (ptB[0] - ptA[0]) * (ptC[1] - ptA[1]) - 
        (ptB[1] - ptA[1]) * (ptC[0] - ptA[0]))


def isCCW(ptA, ptB, ptC):
    '''return if Pt2 is on the left of line segment (Pt0, Pt1)'''
    return lineFn(ptA, ptB, ptC) > 0


def readDataPts(filename, N):
    """Reads the first N lines of data from the input file
          and returns a list of N tuples
          [(x0,y0), (x1, y1), ...]
    """
    f = open(filename)
    listPts = []
    for i in range(N):
        line = map(float, f.readline().split())
        listPts.append(tuple(line))
    return listPts


def giftwrap(listPts):
    """Returns the convex hull vertices computed using the
          giftwrap algorithm as a list of m tuples
          [(u0,v0), (u1,v1), ...]    
    """
    list_point = listPts[:]
    
    #Find Pt0 with the minimum y-coordinate(choose the right-most point)
    Pt0 = min(list_point, key = lambda x: (x[1], -x[0]))

    #initilizations
    n = len(list_point)
    i = 0
    v = 0  #store angle of 
    k = list_point.index(Pt0)
    list_point.append(Pt0)
    chull = [Pt0]
    
    #Repeat until k = n
    start = time.time()
    
    while k != n:
        #Swap pts[i] to pts[k]
        list_point[i], list_point[k] = list_point[k], list_point[i]
        minAngle = 361
        for j in range(i + 1, n + 1):
            angle = theta(list_point[i], list_point[j])
            if angle == 0:
                angle = 360
            if angle < minAngle and angle > v and list_point[i] != list_point[j]:
                minAngle = angle
                k = j  
        if k != n:
            chull.append(list_point[k])
        i += 1
        v = minAngle
        
    print('The amount of vertices : {}'.format(len(chull)))
    return chull


def grahamscan(listPts):
    """Returns the convex hull vertices computed using the
         Graham-scan algorithm as a list of m tuples
         [(u0,v0), (u1,v1), ...]  
    """
    list_point = listPts[:]
    
    #Find Pt0 with the minimum y-coordinate(choose the right-most point)
    Pt0 = min(list_point, key = lambda x: (x[1], -x[0]))
    
    #sort other points by angle throuth Pt0 to the horizontal line and store in a list
    sorted_list = sorted(list_point, key = lambda x: theta(Pt0, x))

    #initilize
    L = sorted_list[3:] #list of points which need to be compare
    chull = sorted_list[0:3] #a stack which compare point is on the top of stack
    n = len(L)
    
    #Compare each point with previous line segment
    for i in range(n):
        while not isCCW(chull[-2], chull[-1], L[i]):
            chull.pop()
        chull.append(L[i])
    
    print('The amount of vertices : {}'.format(len(chull)))
    
    return  chull

    

def amethod(listPts):
    """Returns the convex hull vertices computed using 
    Monotone Chain algorithms a list of m tuples
         [(u0,v0), (u1,v1), ...]  
    """
    list_point = listPts[:]
     
    #sorted the list as x-coordinate then y-coordinate
    sorted_list = sorted(list_point)
    
    #initialize
    chull = []
    lower = []
    upper = []
    
    #set the lower hull
    for point in sorted_list:
        while len(lower) >= 2 and not isCCW(lower[-2], lower[-1], point):
            lower.pop()
        lower.append(point)
    
    #set the upper hull
    for point in reversed(sorted_list):
        while len(upper) >= 2 and not isCCW(upper[-2], upper[-1], point):
            upper.pop()
        upper.append(point)
    chull = lower[:-1] + upper[:-1]

    print('The amount of vertices : {}'.format(len(chull)))
    
    return chull


def main():
    file_type = ['A', 'B']
    for i in file_type: 
        for n in range(3000, 31000, 3000):
            file_name = i + '_' + str(n) + '.dat'
            print('Reading file : {}'.format(file_name))
            listPts = readDataPts(file_name, n)  #File name, numPts given as example only
            print('--------------------------------------------')            
            print(giftwrap(listPts))     #You may r0eplace these three print statements
            print('--------------------------------------------')
            print (grahamscan(listPts))  #with any code for validating your outputs
            print('--------------------------------------------')
            print (amethod(listPts))
            print('\n')

if __name__  ==  "__main__":
    main()
  