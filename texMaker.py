"""

Generates 1D, 2D and 3D Panda3D textures using simplexNoise

These do not tile seamlessly.

"""


from direct.showbase.RandomNumGen import randHash
from pandac.PandaModules import *
from simplex import SimplexNoise
from math import *
from time import time

t=time()



def noise3D(sizeX,sizeY,sizeZ,scale):
    s=SimplexNoise(0,3)
    noiseTex=Texture("NoiseTex")
    noiseTex.setup3dTexture(sizeX,sizeY,sizeZ, Texture.TUnsignedByte, Texture.FRgba)
    p=noiseTex.modifyRamImage()
    for z in range(sizeZ): 
        offset = sizeX * sizeY * z
        print 'making slice '+str(z)+' of '+str(sizeZ)
        for y in range(sizeY): 
            for x in range(sizeX):
                index = (offset + sizeX * y + x)*noiseTex.getNumComponents()*noiseTex.getComponentWidth()
                v=s.simplexNoise([x/scale,y/scale,z/scale],True)
                der=v[1]
                v=v[0]
                p.setElement(index, min(255,max(0,der[1]*8*128+128)))#Blue
                p.setElement(index+1, min(255,max(0,der[0]*8*128+128)))#Green
                p.setElement(index+2, min(255,max(0,v*128+128)))#Red
                p.setElement(index+3, 255)#Alpha
    return noiseTex

def make():
    print "This is going to be somewhat slow. Please wait"
    #tex=noise3D(512,512,1,64.0)
    tex=noise2D(512,512,8.0)
    tex.write(Filename('pics/noisepic_#.png'), 0, 0, True, False) 
    print 'done'
    print time()-t
    
    
    
def noise2D(sizeX,sizeY,scale):
    s=SimplexNoise(0,2)
    noiseTex=Texture("NoiseTex")
    noiseTex.setup2dTexture(sizeX,sizeY, Texture.TUnsignedByte, Texture.FRgb)
    p=noiseTex.modifyRamImage()
    print 'making tex '+str(sizeX)+' by '+str(sizeY)
    for y in range(sizeY): 
        for x in range(sizeX):
            index = (sizeX * y + x)*noiseTex.getNumComponents()*noiseTex.getComponentWidth()
            v,der=s.simplexNoise([x/scale,y/scale],True)
            p.setElement(index, min(255,max(0,der[1]*8*128+128)))#Blue
            p.setElement(index+1, min(255,max(0,der[0]*8*128+128)))#Green
            p.setElement(index+2, min(255,max(0,v*128+128)))#Red
    return noiseTex

def noise1D(sizeX,scale):
    s=SimplexNoise(0,1)
    noiseTex=Texture("NoiseTex")
    noiseTex.setup2dTexture(sizeX,sizeX, Texture.TUnsignedByte, Texture.FRgb)
    p=noiseTex.modifyRamImage()
    print 'making tex '+str(sizeX)+' by '+str(sizeX)
    for y in range(sizeX): 
        v,der=s.simplexNoise([y/scale],True)
        for x in range(sizeX):
            index = (sizeX * y + x)*noiseTex.getNumComponents()*noiseTex.getComponentWidth()
            
            p.setElement(index, min(255,max(0,0)))#Blue
            p.setElement(index+1, min(255,max(0,0)))#Green
            p.setElement(index+2, min(255,max(0,v*128+128)))#Red
    return noiseTex

make()    