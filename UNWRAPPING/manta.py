import pymba

from pymba import Vimba

def get_camera_object():
  with Vimba() as vimba:
      # provide camera index or id
      camera = vimba.camera(0)
      print(camera)
def 
