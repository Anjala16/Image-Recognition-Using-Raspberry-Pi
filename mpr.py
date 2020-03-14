try:
    from PIL import Image
except ImportError:
    import image
from PIL import Image, ImageFilter
import pytesseract
from picamera import PiCamera
from time import sleep
import sys
from subprocess import call
from gpiozero import MotionSensor
import time

pir = MotionSensor(17)
pir.wait_for_no_motion()

camera = PiCamera()

currentstate = False
previousstate = False

try:
	while True:
		currentstate = pir.motion_detected
		if currentstate == True and previousstate == False:
			print("Motion detected by the motion sensor, ready to take the picture")
			camera.start_preview()
			sleep(10)
			camera.capture('image3.jpg')
			camera.stop_preview()
			previousstate = True
                        break
		elif currentstate == False and previousstate == True:
			previousstate = False


except KeyboardInterrupt:
	print("quit")


img = Image.open("image3.jpg")

cropped = img.crop((870, 230, 1300, 300))

ext = ".jpg"

cropped.save("car" + ext)
text = pytesseract.image_to_string("car.jpg", lang='eng', config='-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

print("The number plate captured from image is : " + text.replace(" ", ""))
print("Code will execute '" + sys.argv[1] + "' module.....")

if sys.argv[1] == 'entry':
    exit_code = call("python3.5 car_entry.py " + text.replace(" ", ""), shell=True)

else:
    exit_code = call("python3.5 car_exit.py " + text.replace(" ", ""), shell=True)
