import wave, cv2, math
import numpy as np
from bitstring import BitArray



class Stegano:
	def __init__(self):
		self.image = None
		self.audio = None
		self.audioParams = None

	def setImage(self, image):
		self.image = cv2.imread(image)

	def setAudio(self, audio):
		self.audio = wave.open(audio, 'r')
		self.audioParams = self.audio.getparams()

	def encode(self):
		width, height, dim = self.image.shape
		image = self.image.reshape(width*height, dim)
		frames = np.frombuffer(self.audio.readframes(-1), 'int8')
		for i in range (len(frames)):
			frameBinary = self.frameToBinary(frames[i])
			r, g, b = self.pixelToBinary(image[i][0]), self.pixelToBinary(image[i][1]), self.pixelToBinary(image[i][2])
			image[i] = np.array([ int(r[:5] + frameBinary[:3], 2), int(g[:5] + frameBinary[3:6], 2), int(b[:6] + frameBinary[6:], 2)])
		image = image.reshape(width, height, dim)
		cv2.imwrite('steganoImg.png', image)
		print("Successfully encoded !")

	def decode(self):
		extractedFrames = []
		image = cv2.imread('steganoImg.png')
		width, height, dim = image.shape

		image = image.reshape(width*height, dim)
		for i in range (self.audioParams.nframes):
			r, g, b = self.pixelToBinary(image[i][0]), self.pixelToBinary(image[i][1]), self.pixelToBinary(image[i][2])
			data = r[5:] + g[5:] + b[6:]
			frame = self.binaryToframe(data)
			extractedFrames.append(frame)

		params = (self.audioParams.nchannels, self.audioParams.sampwidth, self.audioParams.framerate, self.audioParams.nframes, self.audioParams.comptype, self.audioParams.compname)
		audio = wave.open('steganoAudio.wav', 'w')
		audio.setparams(params)
		for frame in extractedFrames:
			data = np.int8(frame)
			audio.writeframesraw(data)
		print("Successfully decoded !")


	def frameToBinary(self, n):
		binary = BitArray('int:8='+str(n))
		return binary.bin


	def binaryToframe(self, s):
		frame = - int(math.pow(2,7))*int(s[0])
		if ( s[0] == '1'):
			for i in range(6, -1, -1):
				frame = frame + int(math.pow(2,i))*int(s[7-i])
		else:
			frame = int(s, 2)
		return frame


	def pixelToBinary(self, n):
		binaryString = format(n, '08b')
		binaryList = list(binaryString)
		return ''.join(binaryList)
		

