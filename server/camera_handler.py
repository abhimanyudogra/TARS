__author__ = 'Niharika Dutta and Abhimanyu Dogra'

# import picamera


class ServerCameraHandler:
    """
    ServerCameraHandler interacts with the picamera library to operate the raspberry pi camera
    """

    def __init__(self):
        print "Camera: Initializing.."
        # self.camera = picamera.PiCamera()

    def click_picture(self):
        print "Camera: clicking picture"
        # self.camera.capture('image.jpg')
        # pathname = ''  # path of raspberry pi home
        # img_text = open(pathname, 'rb')
        # image_bytes = img_text.read()
        return ("@Camera: image")
