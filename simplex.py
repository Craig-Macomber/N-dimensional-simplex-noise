"""

An n-diminsional smooth noise sampler using SimplexNoise, including deratives.


http://staffwww.itn.liu.se/~stegu/simplexnoise/simplexnoise.pdf
was a main source of information for this project.

"""
from math import floor
import random

class SimplexNoise():
    def __init__(self,seed,dimensions):
        """
        Initalize SimplexNoise by precomputing all that can be
        precomputed to save time when sampling
        """
        
        # This makes sure the seed is good and randomized
        # as sampling may not do so robustly
        self.seed = randHash(seed)
        self.d = dimensions

       
        
        
        
        # Compute skew constant. This is questionably correct
        self.f = ((self.d + 1) ** .5 - 1) / self.d
        
        # Unskew constant
        #self.g=((self.d+1)-(self.d+1)**.5)/((self.d+1)*self.d)
        
        
        #self.f*=1.1
        
        # This is the proper relation between f and g in terms of d
        # that makes sure skewing and unskewing reverse eachother
        #self.f=self.g/(1-self.d*self.g)
        self.g=self.f/(1+self.d*self.f)
        
        
        
        
         # simplex edge length
        sideLength=self.d ** .5 / (self.d * self.f + 1)
        a=(sideLength**2-(sideLength/2)**2)**.5
        # distace from corner to center of most distant face
        # this is the max influance distance for a vertex
        if self.d==2: cornerToFace=a
        elif self.d==1: cornerToFace=sideLength
        else: cornerToFace=(a**2+(a/2)**2)**.5
        self.cornerToFaceSquared=cornerToFace**2
        
        
        
        # Precompute gradient vectors.
        # Make all possible vectors consisting of:
        # +1 and -1 components with a single 0 component:
        # Vecs from center to midddle of edges of hyper-cube
        
        # Little helper generator function for making gradient vecs
        # Makes vecs of all -1 or 1, of d dimensions 
        def vf(d):
            for i in xrange(2 ** d):
                yield [(i >> n) % 2 * 2 - 1 for n in xrange(d)]
        
        if self.d>1:
            # inject 0s into vecs from vf to make needed vecs
            self.vecs=[v[:z] + [0] + v[z:] for z in xrange(self.d) for v in vf(self.d - 1)]
            
            
            # All 1 or -1 version (hypercube corners)
            # Makes number of vecs higher, and a power of 2.
            #self.vecs=[v for z in xrange(self.d) for v in vf(self.d)]
            
            
            # Compensate for gradient vector lengths
            self.valueScaler=(self.d-1)**-.5
            # use d instead of d-1 if using corners instead of edges
            
            
            # Rough estimated/expirmentally determined function
            # for scaling output to be -1 to 1
            self.valueScaler*=((self.d-1)**-3.5*100+13)
        
        else:
            self.f=0
            self.vecs=[[1],[-1]]
            self.valueScaler=1.0
            self.cornerToFaceSquared=1.0
            self.g=1.0
        
        # shuffle the vectors using self.seed
        r=random.Random()
        r.seed(self.seed)
        r.shuffle(self.vecs)
        random.shuffle(self.vecs)
        
        self.vecCount=len(self.vecs)
        
        


        
        #print self.d,self.f,self.g,self.cornerToFaceSquared,self.valueScaler,self.vecCount
        
                
    def simplexNoise(self,loc,getDerivative=False):
        """ loc is a list of coordinates for the sample position """
        # Perform the skew operation on input space will convert the
        # regular simplexs to right simplexes making up huper-cubes
        
        ranged=range(self.d)
        
        
        s=sum(loc)*self.f
        # Skew and round loc to get origin of containing hypercube in skewed space
        intSkewLoc=[int(floor(v+s)) for v in loc]
        
        # Unskewing factor for intSkewLoc to get to input space
        t=sum(intSkewLoc)*self.g
        # skewed simplex origin unskewed to input space would be:
        # cellOrigin=[v-t for v in intSkewLoc]
        
        # Distance from unskewed simplex origin (intSkewLoc[i]-t) to loc,
        # all in input space
        cellDist=[loc[i]-intSkewLoc[i]+t for i in ranged]
        
        # Indexs of items in cellDist, largest to smallest
        # To find correct vertexes of containing simplex, the containing hypercube
        # is traversed one step of +1 on each axis, in the order given
        # by greatest displacement from origin of hyper cube first.
        # This order is stored in distOrder: The order to traverse the axies
        distOrder=sortWith(cellDist,ranged)
        distOrder.reverse()
        
        # Copy intSkewLoc to work through verts of simplex
        # intLoc will hold the current vertex,
        # and intSkewLoc will stay the containing origin's vertex
        # these are still the skewed right simplexes/ hypercube space vertex indexes
        intLoc=list(intSkewLoc)
        
        # our accumulator of noise
        n=0.0
        # skewOffset holds addational skew that needs to get added.
        # It will be self.g * the how many +1s have been added to all the axies total
        # Thus, adding it to the current vertex skewes it to be in input space
        # relative to the simplex's origin vertex:
        # intSkewLoc in skewed space.
        skewOffset=0.0
        
        if getDerivative: der=[0]*self.d
        
        for v in [-1]+distOrder:
            # Move to the next corner of simplex of not on first corner
            if v!=-1: intLoc[v]+=1
            
            # get u: loc's position relative to the current vertex, in input space
            u=[cellDist[i]-(intLoc[i]-intSkewLoc[i])+skewOffset for i in ranged]

            # t is the factor for attenuating the effect from the current vertexes gradient
            # its based on distance squared
            # if distance squared exceeds self.cornerToFaceSquared, there is no contribution
            t=self.cornerToFaceSquared
            for a in u:
                # Accumulate negative distance squared into t
                t-=a*a
                
            if t>0:
                # fech a pseudorandom vec from self.vecs using intLoc
                index=self.seed
                for i in ranged:
                    index+=intLoc[i]<<((5*i)%16)
                vec=self.vecs[(randHash(index))%self.vecCount]
                
                # dot product of vertex to loc vector and vector for gradient
                gr=0
                for i in ranged:
                    gr+=vec[i]*u[i]

                # add current vertexes contribution
                t4=t**4
                n+=gr*t4
                
                if getDerivative:
                    # Apply product rule
                    # n+=gr*t**4
                    # n+=a*b
                    # der+=der(a)*b+a*der(b)
                    # a=gr
                    # b=t**4
                    # der(a)=vec
                    # der(b)=4*t**3*der(t)
                    # t=c-u**2
                    # der(t)=(-2)*u
                    # der(b)=4*t**3*(-2)*u
                    gr8t3=gr*8*t**3
                    der=[der[i]+vec[i]*t4-gr8t3*u[i] for i in ranged]
                
            skewOffset+=self.g
        n*=self.valueScaler
        if getDerivative:
            return n,[d*self.valueScaler for d in der]
        else:
            return n

from pandac.PandaModules import *    
class ShaderSimplexNoise(SimplexNoise):
    def __init__(self,seed,dimensions):
        if dimensions>4 or dimensions<2: print "Invalid Shader Noise Dimensions of "+str(dimensions)
        SimplexNoise.__init__(self,seed,dimensions)
    def makeVecTex(self):
        vecs=[[min(255,(v+1)*128) for v in vec] for vec in self.vecs]
        return tex1D(vecs,len(vecs[0])==4)

def tex1D(vals,alpha):
    tex=Texture("Tex1D")
    size=len(vals)
    if alpha:
        tex.setup1dTexture(size, Texture.TUnsignedByte, Texture.FRgba)
    else:
        tex.setup1dTexture(size, Texture.TUnsignedByte, Texture.FRgb)
    tex.setMagfilter(Texture.FTNearest)
    tex.setMinfilter(Texture.FTNearest)
    p=tex.modifyRamImage()
    for x in range(size):
        index = x*tex.getNumComponents()*tex.getComponentWidth()
        v=vals[x]
        if len(v)>2: p.setElement(index,   v[2])#Blue
        p.setElement(index+1, v[1])#Green
        p.setElement(index+2, v[0])#Red
        if alpha: p.setElement(index+3, v[3])#Alpha
    return tex


      
# jenkins_one_at_a_time_hash algorithm (roughly)
def randHash(v):
    hash = 255 & v
    hash += (hash << 10)
    hash ^= (hash >> 6)
    
    hash += 255 & (v>>(8))
    hash += (hash << 10)
    hash ^= (hash >> 6)
    
    hash += 255 & (v>>(16))
    hash += (hash << 10)
    hash ^= (hash >> 6)
    
    hash += (hash << 3)
    hash ^= (hash >> 11)
    return hash+(hash << 15)
    
def sortWith(l1,l2):
    # Sorts l2 using l1
    pairs = zip(l1,l2)
    pairs.sort()
    return [v[1] for v in pairs]