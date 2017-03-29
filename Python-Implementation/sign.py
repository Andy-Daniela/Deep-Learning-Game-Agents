import cv2
import numpy as np
import glob
from frame import *
from numpy import *

class Sign(object):
	def __init__(self, path):
		self.path = path
		
		#Getting gloss
		splitted_path = path.split('/')
		self.gloss = splitted_path[len(splitted_path)-1]
		self.frames = []
		self.read_frames()
		
	def read_frames(self):
		frames_paths = glob.glob(self.path+'/*')
		
		for frame_path in frames_paths:
			frame = Frame(frame_path)
			self.frames.append(frame)
	
	def get_path(self):
		return self.path
	
	def get_frames(self):
		return array(self.frames)

	def get_frames_matrices(self):
		frame_matrices = []
		for frame in self.frames:
			frame_matrices.append(frame.get_frame())
		return array(frame_matrices)
	
	def get_frame_at(self, pos):
		return self.frames[pos]
	
	def get_frame_matrix_at(self, pos):
		return self.frames[pos].get_frame()
	
	def get_gloss(self):
		return self.gloss
	
	def set_path(self, path):
		self.path = path
	
	def set_frames(self, frames):
		self.frames = frames
	
	def set_frame_at(self, frame):
		self.frames[pos] = frame
	
	def set_gloss(self, gloss):
		self.gloss = gloss
	
	def __str__(self):
		return self.gloss + '\n' +self.path + '\n' + str(len(self.frames))+' frames'
	
	def __len__(self):
		return len(self.frames)