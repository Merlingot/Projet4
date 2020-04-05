#=============================================================================
# Fonctions pour la point grey
#=============================================================================

import PyCapture2
import numpy as np
import matplotlib.pyplot as plt

def test(name, destination=None):

    # Trouver la camera
    cam = get_camera()

    # Take the image
    cam.startCapture(display_frame)
#    frame = take_frame(cam)
    input('cac')
    cam.stopCapture()
    cam.disconnect()

    # Save image
    save_frame(frame, name, destination)




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
    cam=get_camera()
    print('Ready fo callibration :)')
    cam.startCapture()
    while continue_callibration == True:
        user_input = input('Press \n (y) to take image \n (q) to exit \n')
        if user_input == 'y' :
            print('Taking image...')
            frame=take_frame(cam)
            display_frame(frame)
            print('Saving image...')
            name_i=name+'_{}'.format(str(i))
            save_frame(frame, name_i, destination)
            i+=1
        elif user_input == 'q':
            print('Exiting...')
            cam.stopCapture()
            cam.disconnect()
            continue_callibration=False
        else:
            cam.stopCapture()
            print('Please enter a valid key (y/q)')


def get_camera():
    """ Trouve une camera physique et retourne son object camera """
    # Ensure sufficient cameras are found
    bus = PyCapture2.BusManager()
    num_cams = bus.getNumOfCameras()
    print('Number of cameras detected: ', num_cams)
    if not num_cams:
        print('Insufficient number of cameras. Exiting...')
        exit()

    # Select camera on 0th index
    cam = PyCapture2.Camera()
    uid = bus.getCameraFromIndex(0)
    cam.connect(uid)
    return cam

def take_frame(cam, num_images_to_grab=10):

    for i in range(num_images_to_grab):
        try:
            frame = cam.retrieveBuffer()
        except PyCapture2.Fc2error as fc2Err:
            print('Error retrieving buffer : %s' % fc2Err)
            continue
    return frame


def display_frame(frame):
    newimg = frame.getData()
    cols = frame.getCols(); rows = frame.getRows()
    a = np.array(newimg)
    a=a.reshape(rows, cols)
    plt.imshow(a)
    plt.show()


def save_frame(frame, name, destination=None):

    path = "{}{}.png".format( destination if destination is not None else "", name)
    newimg = frame.convert(PyCapture2.PIXEL_FORMAT.BGR)
    isSaved = newimg.save(path.encode('utf-8'), PyCapture2.IMAGE_FILE_FORMAT.PNG)


# test('name')
