from panda3d.core import *
loadPrcFileData("", "win-size 800 800")
loadPrcFileData("", "sync-video 0")
loadPrcFileData("", "basic-shaders-only 0")
loadPrcFileData("", "textures-power-2 none")
import direct.directbase.DirectStart
from direct.task.Task import Task
import math

#from texMaker import noise3D
from simplex import ShaderSimplexNoise

base.setFrameRateMeter(True)
base.disableMouse()

c=CardMaker("CardMaker")
c.setFrameFullscreenQuad()

n=render2d.attachNewNode(c.generate())

'''
n=loader.loadModel("models/panda-model")
n.reparentTo(render)



#base.camera.setPos(-.5,.5,-1)

n.flattenStrong()

n.setScale(0.025,0.025,0.025)
n.setPos(0,55,-8)



#Task to move the camera
def SpinCameraTask(task):
  angledegrees = task.time * 6.0
  angleradians = angledegrees * (math.pi / 180.0)
  #base.camera.setPos(20*math.sin(angleradians),-20.0*math.cos(angleradians),3)
  n.setHpr(angledegrees, 0, 0)
  return Task.cont

taskMgr.add(SpinCameraTask, "SpinCameraTask")

'''


n.setShaderInput("cam", base.camera.getX(),base.camera.getY(),base.camera.getZ())
n.setShader(loader.loadShader("Test.sha"))

noiseD=2

s=ShaderSimplexNoise(0,noiseD)
n.setTexture(s.makeVecTex())


'''

# Make some randomish 4D rotation matrix
# http://steve.hollasch.net/thesis/chapter2.html
m=[Mat4(Mat4.identMat()) for i in range(6)]

seed=0
from math import sin,cos,pi
import random
r=random.Random()
r.seed(seed)
# x1,y1,x2,y2
p=((0,0,1,1),(1,1,2,2),(2,2,0,0),(0,0,3,3),(3,3,1,1),(3,3,2,2))

# Random angles
a=[r.random()*2*pi for i in range(6)]
c=[cos(v) for v in a]
s=[sin(v) for v in a]

for i in range(6):
    v=p[i]
    m[i].setCell(v[0],v[1],c[i])
    m[i].setCell(v[2],v[1],s[i])
    m[i].setCell(v[0],v[3],-s[i])
    m[i].setCell(v[2],v[3],c[i])


mFinal=m[0]
for i in range(1,6):
    mFinal.multiply(Mat4(mFinal),m[i])


mFinalUnRot=Mat4()
mFinalUnRot.invertFrom(mFinal)

# Add a random translation, 3D though
#t=Mat4.translateMat(r.random(),r.random(),r.random())
#mFinal.multiply(t,Mat4(mFinal))

# Apply Scale
s=Mat4()
s.setScaleMat(Vec3(2,2,2))
s.setCell(3,3,2)
print s
mFinal.multiply(Mat4(mFinal),s)



print mFinal
print mFinalUnRot


'''
from time import time
from direct.task.Task import Task
t=time()
def setTime(task=None):
    n.setShaderInput('time',50*(time()-t),0,0,0)
    return Task.cont

setTime()
taskMgr.add(setTime, "setTime")

run()