#=============================================================================
# Fonctions pour la point grey
#=============================================================================

import PyCapture2

def main(name, destination=None, num_images_to_grab=10):

    """
    Prend une seule photo la caméra détectée et l'enregistre sous le nom <image_name>.png en format png dans le répertoire <destination>.
    name (str):
        nom pour enregistrer l'image sans l'extension
    destination (str):
        path relatif/absolu au répertoire de sauvegarge
        default=None. Si non spécifié, sauvegarde dans le repertoire actuel.
    num_images_to_grab (int) :
        nombre de capture de buffer à prendre.
        default=1.
    """

    # Trouver la camera
    cam = get_camera()

    # Take the image
    print('Starting image capture...')
    cam.startCapture()
    frame = take_frame(cam, num_images_to_grab)
    cam.stopCapture()
    cam.disconnect()

    # Save image
    print('Saving image...')
    save_frame(frame, name, destination)

    input('Done! Press Enter to exit...\n')

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


def save_frame(frame, name, destination=None):

    path = "{}{}.png".format( destination if destination is not None else "", name)
    newimg = frame.convert(PyCapture2.PIXEL_FORMAT.BGR)
    isSaved = newimg.save(path.encode('utf-8'), PyCapture2.IMAGE_FILE_FORMAT.PNG)
    


def enable_embedded_timestamp(cam, enable_timestamp):
    """ Permet d'activer/désactiver le compteur interne (timestep) de la camera <cam>."""
    embedded_info = cam.getEmbeddedImageInfo()
    if embedded_info.available.timestamp:
        cam.setEmbeddedImageInfo(timestamp = enable_timestamp)
        if enable_timestamp :
            print('\nTimeStamp is enabled.\n')
        else:
            print('\nTimeStamp is disabled.\n')
