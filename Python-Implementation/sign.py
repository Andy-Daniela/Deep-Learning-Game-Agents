import cv2
import numpy as np
import glob
from frame import *

class Sign(object):
	def __init__(self, path):
		self.path = path
		self.frames = []
		self.read_frames()
		
	def read_frames(self):
		frames_paths = glob.glob('*')
		
		for frame_path in frames_paths:
			frame = Frame(frame_path)
			self.frames.append(frame)
	
	def get_path(self):
		return self.path
	
	def get_frames(self):
		return self.frames
	
	def get_frame_at(self, pos):
		return self.frames[pos]
	
	def set_path(self, path):
		self.path = path
	
	def set_frames(self, frames):
		self.frames = frames
	
	def set_frame_at(self, frame):
		self.frames[pos] = frame
	
	def __str__(self):
		return self.path + '\n' + str(len(self.frames))+' frames'
	
	def __len__(self):
		return len(self.frames)