from pymba import Vimba

def placeholder():
    pass

def set_continous_aquisition_mode():

    with Vimba() as vimba:
        camera = vimba.camera(0)
        camera.open()
        camera.arm('Continuous', placeholder)
        camera.disarm()
        camera.close()



set_continous_aquisition_mode()
