from PIL import Image
import math 


class median_filter:
	
	def __init__(self, image, size_of_kernel):

		self.__image = image
		self.__width, self.__height = self.__image.size
		self.__new_image = self.__image.copy()
		self.__pixel_of_image = self.__new_image.load()
		self.__size_of_kernel = size_of_kernel


	def marginal(self, number) :


		for i in range(self.__width) :

			for j in range(self.__height) : 
				
				red_values, green_values, blue_values = self.__helper(i, j)
				red_values.sort()
				green_values.sort()
				blue_values.sort()

				newRed, newGreen, newBlue = red_values[len(green_values) // 2], green_values[len(green_values) // 2], blue_values[len(green_values) // 2]

				self.__pixel_of_image[i,j] = (newRed,newGreen,newBlue)

		self.__new_image.save("Results/Marginal Results/" + number +"--size_of_filter_" + str(self.__size_of_kernel) + ".png")
	

	def vector(self, func, directory_name, number):

		for i in range(self.__width) :

			for j in range(self.__height) : 
				
				red_values, green_values, blue_values = self.__helper(i, j)

				self.__pixel_of_image[i,j] = func(red_values, green_values, blue_values)


		self.__new_image.save(directory_name + "/" + number + "--size_of_filter_" + str(self.__size_of_kernel) + ".png")


	def __helper(self, x_coordinate, y_coordinate):

		red_values = (self.__size_of_kernel * self.__size_of_kernel) * [0]
		green_values = (self.__size_of_kernel * self.__size_of_kernel) * [0]
		blue_values = (self.__size_of_kernel * self.__size_of_kernel) *  [0]

		num = 0
		temp = self.__size_of_kernel // 2

		for i in range(self.__size_of_kernel):
			for j in range(self.__size_of_kernel):
				if (x_coordinate - (temp - i) < 0 or x_coordinate - (temp - i) > self.__width - 1 or y_coordinate - (temp - j) < 0 or y_coordinate - (temp - j) > self.__height - 1) == 0:
					red_values[num], green_values[num], blue_values[num] = self.__image.getpixel((x_coordinate - (temp - i), y_coordinate - (temp - j) )) 	#ust

				num += 1 


		return red_values, green_values, blue_values




	def bitMix_ordering(self, red_values, green_values, blue_values) : # 2 tane parametre alıcak pixel_1 ve pixel_2 

		pixels_values = (self.__size_of_kernel * self.__size_of_kernel) * ["000000000000000000000000"]

		for i in range(self.__size_of_kernel * self.__size_of_kernel):

			pixels_values[i] = format(red_values[i],'08b') + format(green_values[i],'08b') + format(blue_values[i],'08b')

		pixels_values.sort()

		return int(pixels_values[len(pixels_values) // 2][0:8], 2), int(pixels_values[len(pixels_values) // 2][8:16], 2), int(pixels_values[len(pixels_values) // 2][16:24], 2) 


	def lexicographical_ordering(self, red_values, green_values, blue_values) : # 2 tane parametre alıcak pixel_1 ve pixel_2 
		
		pixels_values = []

		for i in range(len(red_values)):
			pixels_values.append([red_values[i], green_values[i], blue_values[i]])


		for i in range(len(pixels_values)):
			
			for j in range(i + 1,len(pixels_values)):
				
				if pixels_values[i][0] > pixels_values[j][0] : 
					pixels_values[i], pixels_values[j] = pixels_values[j], pixels_values[i] 
				
				elif pixels_values[i][0] == pixels_values[j][0]:

					if pixels_values[i][1] > pixels_values[j][1] : 
						pixels_values[i], pixels_values[j] = pixels_values[j], pixels_values[i] 
					
					elif pixels_values[i][1] == pixels_values[j][1]:
						if pixels_values[i][2] > pixels_values[j][2] :
							pixels_values[i], pixels_values[j] = pixels_values[j], pixels_values[i] 



		return tuple(pixels_values[len(pixels_values) // 2])


	def norm_based_ordering(self, red_values, green_values, blue_values) :  #distance fonksiyonunu kullanmadan euclideanı bul 

		
		dic = {}
		euclideans = len(red_values) * [0]

		for i in range(len(red_values)):

			euclidean = math.sqrt(math.pow(red_values[i] - red_values[len(red_values) // 2],2) + math.pow(green_values[i] - green_values[len(red_values) // 2],2) + math.pow(blue_values[i] - blue_values[len(red_values) // 2],2));

			dic[euclidean] = red_values[i], green_values[i], blue_values[i]

			euclideans[i] = euclidean 
	
		euclideans.sort()

		return dic[euclideans[len(euclideans) // 2]]



def main():

	import os
	
	if not os.path.exists("Results"):
		os.mkdir("Results")

	if not os.path.exists("Results/Marginal Results"):
		os.mkdir("Results/Marginal Results")

	if not os.path.exists("Results/BitMix Ordering Results"):
		os.mkdir("Results/BitMix Ordering Results")


	if not os.path.exists("Results/Norm Based Ordering Results"):
		os.mkdir("Results/Norm Based Ordering Results")

	if not os.path.exists("Results/Lexicographical Ordering Results"):
		os.mkdir("Results/Lexicographical Ordering Results")


	images = ["images/1.jpeg",
			  "images/2.jpeg",
			  "images/3.jpeg",
			  "images/4.jpeg",
			  "images/5.png",
			  "images/6.jpg",
			  "images/7.jpeg",
			  "images/8.jpeg",
			  "images/9.jpg",
			  "images/10.jpeg"]



	for i in range(10):

		image = Image.open(images[i])
		rgb_im = image.convert('RGB')


		part1 = median_filter(rgb_im,3)
		part1.vector(part1.bitMix_ordering, "Results/BitMix Ordering Results", str(i + 1))

		part1 = median_filter(rgb_im,3)
		part1.vector(part1.norm_based_ordering, "Results/Norm Based Ordering Results", str(i + 1))

		part1 = median_filter(rgb_im,3)
		part1.vector(part1.lexicographical_ordering, "Results/Lexicographical Ordering Results", str(i + 1))

		part1 = median_filter(rgb_im,3)		
		part1.marginal(str(i + 1))
	

if __name__ == '__main__':
	main()

     