import pymba
import cv2
import matplotlib.pyplot as plt
import numpy as np
from pymba import Vimba, VimbaException
from typing import Optional
from pymba import Frame


def main(name, destination=None):
    """
    Prend une seule photo la caméra détectée et l'enregistre sous le nom <image_name>.png en format png dans le répertoire <destination>.
    name (str):
        nom pour enregistrer l'image sans l'extension
    destination (str):
        path relatif/absolu au répertoire de sauvegarge
        default=None. Si non spécifié, sauvegarde dans le repertoire actuel.
    """
    with Vimba() as vimba:
        cam = vimba.camera(0)
        cam.open()
        cam.arm('SingleFrame')

        print('Starting image capture...')
        frame=take_frame(cam)
        cam.disarm()
        cam.close()
        
    #display_frame(frame) 
    print('Saving image...')
    save_frame(frame, name, destination)

    input('Done! Press Enter to exit...\n')


def get_camera():
    with Vimba() as vimba:
        # provide camera index or id
        cam = vimba.camera(0)
        return cam

def take_frame(cam):

    # capture a single frame, more than once if desired
    for i in range(10):
        try:
            frame = cam.acquire_frame()
        except VimbaException as e:
            # rearm camera upon frame timeout
            if e.error_code == VimbaException.ERR_TIMEOUT:
                print(e)
                cam.disarm()
                cam.arm('SingleFrame')
            else:
                raise
    return frame

def display_frame(frame, delay=1):
    """
    Displays the acquired frame.
    frame: The frame object to display.
    delay: Display delay in milliseconds, use 0 for indefinite.
    """
    image = frame_to_image(frame)

    # display image
    cv2.imshow('Image', image)
    cv2.waitKey(delay)

def save_frame(frame, name, destination=None):
    """
    Saves the frame as a png image.
    frame : The frame object to save 
    name : The name of the image to save (without .png extension)
    destination (optional) : the absolute/relative path to the directory where to save the image
    """
    
    # get a copy of the frame data
    image = frame_to_image(frame)
    path = "{}{}.png".format( destination if destination is not None else "", name)
    # save image
    isSaved = cv2.imwrite(path, image)

def frame_to_image(frame):

    image = frame.buffer_data_numpy()
    #Converted the datatype to np.uint8
    new_image = image.astype(np.uint8)


    return new_image     


from time import sleep


def stream():

    with Vimba() as vimba:
        camera = vimba.camera(0)
        camera.open()

        # arm the camera and provide a function to be called upon frame ready
        camera.arm('Continuous', display_frame)
        camera.start_frame_acquisition()

        # stream images for a while...
        sleep(5)

        # stop frame acquisition
        # start_frame_acquisition can simply be called again if the camera is still armed
        camera.stop_frame_acquisition()
        camera.disarm()

        camera.close()

