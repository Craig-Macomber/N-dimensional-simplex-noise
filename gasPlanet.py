"""

This seems to fail on some computers. It uses a pretty complex shader to do the noise.

"""


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
base.setBackgroundColor(0,0,0)

c=CardMaker("CardMaker")
c.setFrameFullscreenQuad()

#n=render2d.attachNewNode(c.generate())


n=loader.loadModel("planet_sphere")
n.reparentTo(render)



#base.camera.setPos(-.5,.5,-1)

n.flattenStrong()

#n.setScale(0.025,0.025,0.025)
n.setPos(0,5,0)

base.camera.reparentTo(n)



n.setShaderInput("edgeColor",.1,.2,.3,1)



#Task to move the camera
def SpinCameraTask(task):
  angledegrees = task.time * 60.0
  angleradians = angledegrees * (math.pi / 180.0)
  base.camera.setPos(5*math.sin(angleradians),-5.0*math.cos(angleradians),0)
  base.camera.lookAt(n)
  #n.setHpr(angledegrees, 0, 0)
  n.setShaderInput("cam", base.camera.getX(),base.camera.getY(),base.camera.getZ())
  return Task.cont

taskMgr.add(SpinCameraTask, "SpinCameraTask")

n.setShader(loader.loadShader("gasPlanet.sha"))

noiseD=3

s=ShaderSimplexNoise(0,noiseD)
n.setTexture(TextureStage("n"),s.makeVecTex())

g=loader.loadTexture("grad.png")
g.setWrapU(Texture.WMClamp)
g.setWrapV(Texture.WMClamp)

n.setTexture(TextureStage("g"),g)


from time import time
from direct.task.Task import Task
t=time()
def setTime(task=None):
    n.setShaderInput('time',50*(time()-t),0,0,0)
    return Task.cont

setTime()
taskMgr.add(setTime, "setTime")
run()