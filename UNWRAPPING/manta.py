import pymba
import cv2
from skimage.io import imsave, imshow
from skimage.viewer import ImageViewer
import numpy as np
from pymba import Vimba, VimbaException
from typing import Optional
from pymba import Frame


def ext_callib(name, destination=None):
    """
    Prend X photo avec la caméra détectée et l'enregistre sous le nom <image_name_i>.png en format png dans le répertoire <destination>.
    name (str):
        nom pour enregistrer l'image sans l'extension
    destination (str):
        path relatif/absolu au répertoire de sauvegarge
        default=None. Si non spécifié, sauvegarde dans le repertoire actuel.
    """
    i=0
    continue_callibration=True
    with Vimba() as vimba:
        cam=vimba.camera(0)
        cam.open()
        input('Ready fo callibration :)')
        while continue_callibration == True:
            # arm the camera and provide a function to be called upon frame
            cam.arm('Continuous', display_frame)
            cam.start_frame_acquisition() # stream images until input
            user_input = input('Press \n (y) to take image \n (q) to exit')
            if user_input == 'y' :
                cam.stop_frame_acquisition()
                cam.arm('SingleFrame')
                print('Taking image...')
                frame=take_frame(cam)
                print('Saving image...')
                name_i=name+'_{}'.format(str(i))
                save_frame(frame, name_i, destination)
                i+=1
            elif user_input == 'q':
                cam.stop_frame_acquisition()
                print('Exiting...')
                cam.disarm()
                cam.close()
                continue_callibration=False
            else:
                cam.stop_frame_acquisition()
                print('Please enter a valid key (y/q)')


def get_camera():
    with Vimba() as vimba:
        # provide camera index or id
        cam = vimba.camera(0)
        return cam

def take_frame(cam):
    """ capture a single frame """
    for i in range(1):
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

def display_frame(frame):
    """
    Displays the acquired frame.
        frame: The frame object to display.
    """
    image = frame_to_image(frame)
    # imshow(image)
    viewer = ImageViewer(image); viewer.show()

def save_frame(frame, name, destination=None):
    """
    Saves the frame as a png image.
        frame : The frame object to save
        name : The name of the image to save (without .png extension)
        destination (optional) : the absolute/relative path to the directory where to save the image
    """
    image = frame_to_image(frame)
    path = "{}{}.png".format( destination if destination is not None else "", name)
    isSaved = imsave(path, image, format='png')

def frame_to_image(frame):
    """
    Takes the data in the camera buffer and converts it to a readable uint8 numpy array
    """
    # get a copy of the frame data
    image = frame.buffer_data_numpy()
    #Convert the datatype to np.uint8
    new_image = image.astype(np.uint8)

    return new_image     


