from panda3d.core import *

winSize=600

loadPrcFileData("", "win-size "+str(winSize)+" "+str(winSize))
loadPrcFileData("", "sync-video 0")
loadPrcFileData("", "basic-shaders-only 0")
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task

from simplex import ShaderSimplexNoise

base.setFrameRateMeter(True)
base.disableMouse()

c=CardMaker("CardMaker")
c.setFrameFullscreenQuad()
n=render2d.attachNewNode(c.generate())

def setShaderMat(mat,node,name):
    v=mat.getCol(0)
    node.setShaderInput(name+"1", v.getX(),v.getY(),v.getZ(),v.getW())
    v=mat.getCol(1)
    node.setShaderInput(name+"2", v.getX(),v.getY(),v.getZ(),v.getW())
    v=mat.getCol(2)
    node.setShaderInput(name+"3", v.getX(),v.getY(),v.getZ(),v.getW())
    v=mat.getCol(3)
    node.setShaderInput(name+"4", v.getX(),v.getY(),v.getZ(),v.getW())

noiseD=3

s=ShaderSimplexNoise(0,noiseD)
n.setTexture(s.makeVecTex())


n.setShader(loader.loadShader("Ray.sha"))

base.camera.setPos(0.077093, -0.210524, 0.0781958)


base.setBackgroundColor(0,0,0,0)

print(base.win.supportsPixelZoom())
base.win.setPixelZoom(8)


class keyTracker(DirectObject):
    def __init__(self):
        self.keyMap = {}
    def addKey(self,key,name):
        self.accept(key.lower(), self.setKey, [name,True])
        self.accept(key.lower()+"-up", self.setKey, [name,False])
        
        self.accept(key.upper(), self.setKey, [name,True])
        self.accept(key.upper()+"-up", self.setKey, [name,False])
        self.keyMap[name]=False
    def setKey(self, key, value):
        self.keyMap[key] = value

k=keyTracker()
   
k.addKey("w","forward")
k.addKey("a","left")
k.addKey("s","backward")
k.addKey("d","right")
k.addKey("q","rollLeft")
k.addKey("e","rollRight")
k.addKey("arrow_left","turnLeft")
k.addKey("arrow_right","turnRight")
k.addKey("arrow_down","turnDown")
k.addKey("arrow_up","turnUp")



class MouseTracker(DirectObject):
    def __init__(self,sort=0):
        self.dt=1
        self.mouseX=0
        self.mouseY=0
        
        props = WindowProperties()
        props.setCursorHidden(True) 
        base.win.requestProperties(props)
        
        self.trackMouse()
        
        taskMgr.add(self.trackMouse,"trackMouse",sort=sort)

        self.dx=0
        self.dy=0
        
    def trackMouse(self,task=None):
        self.dt=globalClock.getDt()
        
        # figure out how much the mouse has moved (in pixels)
        md = base.win.getPointer(0)
        x=self.mouseX
        y=self.mouseY
        self.mouseX = md.getX()
        self.mouseY = md.getY()
        self.dx=self.mouseX - x
        self.dy=self.mouseY - y
        base.win.movePointer(0,winSize/2,winSize/2)
        self.mouseX=winSize/2
        self.mouseY=winSize/2
        
        if task != None: return Task.cont

mouseTracker=MouseTracker()
   
from time import time
from math import sin


def doFrame(task=None):
    elapsed=globalClock.getDt()
    
    forwardMove=0.0
    rightMove=0.0
    rollRight=0.0
    
    turnRight=0.0
    turnUp=0.0
    
    m=k.keyMap
    if m["forward"]: forwardMove+=1.0
    if m["backward"]: forwardMove-=.5
    if m["left"]: rightMove-=1.0
    if m["right"]: rightMove+=1.0
        
    if m["rollLeft"]: rollRight-=1.0
    if m["rollRight"]: rollRight+=1.0 
    
    if m["turnLeft"]: turnRight-=1.0
    if m["turnRight"]: turnRight+=1.0 
    
    if m["turnDown"]: turnUp-=1.0
    if m["turnUp"]: turnUp+=1.0 

    
    rightMove*=.05
    forwardMove*=.1
    rollRight*=100
    upMove=0.0
    turnUp*=100
    turnRight*=100
    
    turnRight+=mouseTracker.dx/mouseTracker.dt*.2
    turnUp+=mouseTracker.dy/mouseTracker.dt*-.2
    
    
    base.camera.setPos(base.camera,Vec3(rightMove,forwardMove,upMove)*elapsed)
    base.camera.setHpr(base.camera,-turnRight*elapsed,turnUp*elapsed,rollRight*elapsed)
    
    n.setShaderInput("cam", base.camera.getX(),base.camera.getY(),base.camera.getZ())   
    
    
    setShaderMat(base.camera.getMat(),n,"camMat")
    
    n.setShaderInput("threshold", sin(time()/2)/16-.05)
    if task != None: return Task.cont

doFrame()

taskMgr.add(doFrame, "doFrame",sort = 49)










run()