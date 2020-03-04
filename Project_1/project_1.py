import cv2
import numpy as np
from matplotlib import pylab as plt


def active(th1,x,y):
	
	if x < len(th1) - 1:
		th1[x+1][y] = 255
		if y > 0:
			th1[x+1][y-1] = 255
		if y < len(th1[x]) - 1:
			th1[x+1][y+1] = 255


def active2(th1,x,y):
	
	if y < len(th1[x]) - 1:
		th1[x][y-1] = 255
		if x > 0:
			th1[x-1][y-1] = 255
		if x < len(th1[x]) - 1:
			th1[x+1][y-1] = 255



def upward(img,x,y):
	
	temp = 0
	temp2 = 0
	temp3 = 0

	if x < 0:
		temp = img[x-1][y]
		if y > 0:
			temp2 = img[x-1][y-1]
		if y < len(img[x]) - 1:
			temp3 = img[x-1][y+1]

	return 1 + max(temp,temp2,temp3)

	

def main():


	img = cv2.imread('input.png',0)


	ret,th1 = cv2.threshold(img,0,255,cv2.THRESH_BINARY)
	
	

	for x in range(len(th1)):
		for y in range(len(th1[x])):
			if th1[x][y] == 255:
				temp = upward(img,x,y)
				if temp != img[x][y]:
					img[x][y] = temp
					active(th1,x,y)



	for x in range(th1.shape[0]-1,0,-1):
		for y in range(th1.shape[1]-1,0,-1):
			if th1[x][y] == 255:
				temp = upward(img,x,y)
				if temp != img[x][y]:
					img[x][y] = temp
					active2(th1,x,y)


	cv2.imshow("output",th1)
	cv2.waitKey(10000)



if __name__ == "__main__":
	main()




