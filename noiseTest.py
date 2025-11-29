"""

Some basic noise quality tests.

"""



from direct.showbase.RandomNumGen import randHash
from panda3d.core import *
from simplex import SimplexNoise
from math import *
from numpy import array
from time import time

    
import timeit
#t = timeit.Timer("simplexNoise(0,1,1,1)","from simplex import simplexNoise")
#print min(t.repeat(3, 1000))

#t = timeit.Timer("s.simplexNoise(1,1,1)","from simplex import SimplexNoise;s=SimplexNoise(0,3)")
#print min(t.repeat(30, 1000))


import random


#s=SimplexNoise(0,3)
#s.simplexNoise([1,1,1],True)

import cProfile

def verifyDerivatives(dimensions,verbose=True):
    if verbose: print('verifyDerivatives:')
    passedList=[]
    for d in dimensions:
        s=SimplexNoise(0,d)
        stepSize=.01
        stepCount=256
        v=[s.simplexNoise([x*stepSize]*d,True) for x in range(stepCount)]
        estimate=v[0][0]
        changeSum=0
        for i in range(len(v)-1):
            val=v[i]
            der=val[1]
            estimate+=sum(der)
            changeSum+=abs(val[0]-v[1+1][0])
        estimate*=stepSize
        true=v[-1][0]
        error=abs(estimate-true)
        error/=changeSum
        error*=100
        passed=error<0.1
        if verbose:
            print(str(d)+' dimensional:')
            print('    error percent: %5.8f' % error)
            print('    '+('passed' if passed else 'FAILED'))
        passedList.append(passed)
    return all(passedList)


def analyze(dimensions,verbose=True):
    if verbose: print('analyze:')
    for d in dimensions:
        if verbose:
            print(str(d)+' dimensional:')
        count=50000
        s=SimplexNoise(0,d)
        
        data=[s.simplexNoise([random.random()*1000.0 for a in range(d)],True) for x in range(count)]
        distributionCheck([v[0] for v in data],[v[1] for v in data],verbose)

def distributionCheck(values, derivatives, verbose=True):
    dimensions=len(derivatives[0])
    
    def histogram(values,count=25,vmin=None,vmax=None,verbose=True):
        lo=vmin if vmin is not None else min(values)
        hi=vmax if vmax is not None else max(values)
        h=[0]*count
        if lo==hi:
            print('histogram error: lo=hi')
            return
        #print lo,hi,values
        for v in values:
            h[int((v-lo)/(hi-lo)*(count-0.01))]+=1
        if verbose:
            print('    min: %5.8f' % lo)
            s=0
            error=0
            for i in range(count):
                v=h[i]
                s+=v
                val=float(s)/len(values)
                error+=(val-(float(i)/count))**2
                #print '    '+'#'*int(val*100)
                print('    '+'#'*int(v*100/max(h)))
            print('    max: %5.8f' % hi)
            print('    error: %5.8f' % error)
        return h
    def sign(v):
        return 1 if v>0 else -1
    vHistogram=histogram([v for v in values],verbose=verbose)
    vHistogram=histogram([sum([a**2 for a in d])**.5 for d in derivatives],verbose=verbose,vmin=0)
    #dHistograms=[[0]*count for i in xrange(dimensions)]
    #dHistogram=[0]*count    

analyze(list(range(2,6)))
verifyDerivatives(list(range(1,6)))

def loopTest():
    
    loopCount=10000
    print('dimensions','ms','max value','min value')
    #histo=[0 for i in xrange(100)]
        
    print('der')
        
    
    for i in range(2,5):
        s=SimplexNoise(0,i)
        maxV=0.0
        minV=0.0
        t=time()
        for a in range(loopCount):
            v=s.simplexNoise([random.random()*100 for x in range(i)],True)
            d=v[1]
            v=d[0]
            maxV=max(maxV,v)
            minV=min(minV,v)
         
        #print i,(time()-t)/loopCount*1000,maxV,minV
        
        print('derivative check')
        stepSize=.01
        stepCount=200
        v=[s.simplexNoise([x*stepSize]*i,True) for x in range(stepCount)]
        estimate=v[0][0]
        for val in v[:-1]:
            der=val[1]
            estimate+=sum(der)
        estimate*=stepSize
        true=v[-1][0]
        print(estimate-true,estimate,true)
        
        
    print('reg')
    
    if False:
        
        for i in range(2,5):
            s=SimplexNoise(0,i)
            maxV=0.0
            minV=0.0
            t=time()
            for a in range(loopCount):
                v=s.simplexNoise(([random.random()*100 for x in range(i)]))
                maxV=max(maxV,v)
                minV=min(minV,v)
             
            print(i,(time()-t)/loopCount*1000,maxV,minV)
            
#cProfile.run('loopTest()')#'s.simplexNoise([1,1,1],True)'
loopTest()


from panda3d.core import PerlinNoise2,PerlinNoise3
def pandaPerlin():
    loopCount=100000
    print('reg panda2d')

    s=PerlinNoise2()
    maxV=0.0
    minV=0.0
    t=time()
    for a in range(loopCount):
        v=s.noise(*[random.random()*100 for x in range(2)])
        maxV=max(maxV,v)
        minV=min(minV,v)
     
    print(2,(time()-t)/loopCount*1000,maxV,minV)

    print('reg panda3d')

    s=PerlinNoise3()
    maxV=0.0
    minV=0.0
    t=time()
    for a in range(loopCount):
        v=s.noise(*[random.random()*100 for x in range(3)])
        maxV=max(maxV,v)
        minV=min(minV,v)
     
    print(3,(time()-t)/loopCount*1000,maxV,minV)

#pandaPerlin()    