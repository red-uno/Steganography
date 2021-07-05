from tkinter import *
from tkinter import filedialog
import cv2, os
#import stegano as app
os.system('cls')

try:
  	import stegano as app
  	import cv2
except ImportError:
  	print("Trying to Install required modules: \n")
  	os.system('python -m pip install Wave')
  	os.system('python -m pip install bitstring')
  	os.system('python -m pip install opencv-python')
finally:
	import stegano as app
	import cv2


def loadImage():
	file = filedialog.askopenfile(filetypes=(('png files', '*.png'),))
	image = cv2.imread(file.name)
	if ( file != None):
		stegano.setImage(file.name)
		imageNotification.config(text = 'Image loaded succefully')
	print("Image dimens " , image.shape)

def loadAudio():
	file = filedialog.askopenfile(filetypes=(('wav files', '*.wav'),))
	if ( file != None):
		stegano.setAudio(file.name)
		audioNotification.config(text = 'Audio loaded succefully')
	print(file.name)



window = Tk()
window.title('Steganographizer')
window.geometry("500x200+100+100")

stegano = app.Stegano()

assetsFrame = Frame(window)
assetsFrame.pack(padx = 10, pady = 10)

loadImage = Button(assetsFrame, text = 'Load image', width = 15, height = 2, justify = 'center', bg = '#3399ff', fg = 'white', command = loadImage)
loadImage.pack(side = LEFT, padx = 5)
loadAudio = Button(assetsFrame, text = 'Load audio', width = 15, height = 2, justify = 'center', bg = '#3399ff', fg = 'white', command = loadAudio)
loadAudio.pack(side = LEFT, padx = 5)

imageNotification = Label(window, text='Please add image', justify='center')
imageNotification.pack(padx = 10, pady = 10)

audioNotification = Label(window, text='Please add audio', justify='center')
audioNotification.pack(padx = 10, pady = 10)

optionsFrame = Frame(window)
optionsFrame.pack(padx = 10, pady = 10)

encode = Button(optionsFrame, text = 'Encode', width = 15, height = 2, justify='center', bg = '#00cc99', fg = 'white', command = stegano.encode)
encode.pack(side = LEFT, padx = 5)
decode = Button(optionsFrame, text = 'Decode', width = 15, height = 2, justify='center', bg = '#00cc99', fg = 'white', command = stegano.decode)
decode.pack(side = LEFT, padx = 5)


window.mainloop()