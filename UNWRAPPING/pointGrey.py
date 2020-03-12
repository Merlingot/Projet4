#=============================================================================
# Fonctions pour la point grey
#=============================================================================

import PyCapture2

def take_one_photo(image_name, dir=None, num_images_to_grab=10):

    """
    Prend une photo la caméra détectée et l'enregistre sous le nom <image_name>.png en format png dans le répertoire <dir>.
    image_name (str):
        nom pour enregistrer l'image sans l'extension
    dir (str):
        path non relatif au répertoire de sauvegarge
        default=None. Si non spécifié, sauvegarde dans le wd.
    num_images_to_grab (int) :
        nombre de capture de buffer à prendre.
        default=10.
    """

    # Trouver la camera
    cam = find_camera()
    # Enable camera embedded timestamp
    enable_embedded_timestamp(cam, True)

    # Take the image
    print('Starting image capture...')
    cam.startCapture()
    grab_images(cam, image_name, dir, num_images_to_grab)
    cam.stopCapture()

    # Disable camera embedded timestamp
    enable_embedded_timestamp(cam, False)
    cam.disconnect()

    input('Done! Press Enter to exit...\n')


def grab_images(cam, image_name, dir=None, num_images_to_grab=10):
    """ Prendre une photo """
    prev_ts = None
    for i in range(num_images_to_grab):
        try:
            image = cam.retrieveBuffer()
        except PyCapture2.Fc2error as fc2Err:
            print('Error retrieving buffer : %s' % fc2Err)
            continue

        ts = image.getTimeStamp()
        if prev_ts:
            diff = (ts.cycleSeconds - prev_ts.cycleSeconds) * 8000 + (ts.cycleCount - prev_ts.cycleCount)
            print('Timestamp [ %d %d ] - %d' % (ts.cycleSeconds, ts.cycleCount, diff))
        prev_ts = ts

    save_name = "{}{}".format(dir if dir is not None else "", image_name)
    newimg = image.convert(PyCapture2.PIXEL_FORMAT.BGR)
    print('Saving the last image to {}.png'.format(save_name))
    newimg.save(save_name.encode('utf-8'), PyCapture2.IMAGE_FILE_FORMAT.PNG)

def find_camera():
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

def enable_embedded_timestamp(cam, enable_timestamp):
    """ Permet d'activer/désactiver le compteur interne (timestep) de la camera <cam>."""
    embedded_info = cam.getEmbeddedImageInfo()
    if embedded_info.available.timestamp:
        cam.setEmbeddedImageInfo(timestamp = enable_timestamp)
        if enable_timestamp :
            print('\nTimeStamp is enabled.\n')
        else:
            print('\nTimeStamp is disabled.\n')
