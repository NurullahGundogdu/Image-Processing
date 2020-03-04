from PIL import Image
import math 
import os



class histogram_equalization:

	def __init__(self, image):

		self.__image = image
		self.__height, self.__width = self.__image.size
		self.__pixel_of_image = self.__image.load()
		self.__image_size = self.__height * self.__width


	def __pixel_intensity(self):  # to make a histogram (count distribution frequency)  pixel younlugu

		values = [0] * 256

		dic = {}

		for i in range(self.__height):
			for j in range(self.__width):
				values[self.__pixel_of_image[i,j]] += 1
				dic[(i,j)] = self.__pixel_of_image[i,j]

		return values, dic


	def __probability(self, intesity):

		for i in range(256):
			intesity[i] = intesity[i] / self.__image_size
			
		return intesity


	def __cdf(self, hist, dic):

		temp = hist[0]
		temp2 = hist[1]

		hist[0] = math.ceil(hist[0] * 256)

		for i in range(1, len(hist)):

			temp2 = hist[i]

			hist[i] = math.floor((temp + temp2) * 256)

			temp += temp2

		for i in range(self.__height):
			for j in range(self.__width):
				self.__pixel_of_image[i,j] = hist[dic[(i,j)]]



	def equalize_image(self):

		values, dic = self.__pixel_intensity()

		self.__cdf(self.__probability(values), dic)

		return self.__image
	



def load_test_train_classes_files():
											#tek tek file icindeki foto isimlerini oku
	file = open("Outex_TC_00012/problems.txt", "r") 

	files = []

	for i in file:
		files.append(i[:-1])

	file.close()


	train = load_files(files[1], "train.txt")
	test = load_files(files[1], "test.txt")
	classes = load_files(files[1], "classes.txt")


	return train, test, classes, files[1:]



def load_files(dir_name, filename):		#test klasorlerindeki dosyaları okur

	temp = os.getcwd()

	os.chdir("Outex_TC_00012/" + dir_name)

	train = read_file(filename)

	os.chdir(temp)

	return train



def read_file(filename):			#dosyalardaki foto isimlerini okur

	file = open(filename, "r") 

	size = int(file.readline())

	train = {}

	for i in range(size):
		line = file.readline()
		train[line[:-1].split( )[0]] = line[:-1].split( )[1]


	file.close()


	return train



def find_accuracy_rate(train, test, k):			#test klasorundeki fotolarin euclidianını bulur

	train_keys, trains_vector = find_hist_eq_trains(train)
	test_keys, test_vector = find_hist_eq_trains(test)

	euc = [None] * len(test_vector)


	for i in range(len(test_vector)):
		euc[i] = find_test_trains_euc(trains_vector, test_vector[i], k)  #k tane euclidian


	for i in range(len(euc)):
		euc[i] = find_class_num(euc[i], train_keys,train)

	ratio = find_equality_ratio(euc, test_keys, test)

	print ("%"+str(int(ratio)))



def find_hist_eq_trains(train):			#find image feature vector

		
	list_of_file = list(train.keys())

	feat_vects_of_trains = [None] * len(list_of_file)

	for i in range(len(list_of_file)):

		img = Image.open("Outex_TC_00012/images/" + list_of_file[i]).convert('L')

		eq = histogram_equalization(img)
		image = eq.equalize_image()

		local_binary_pattern(img,8,1)


		feat_vects_of_trains[i] = feature_vector(image)

	return list_of_file, feat_vects_of_trains



def local_binary_pattern(imgg, points, radius):

	img = imgg.copy()

	image = img.load()

	height, width = img.size


	for hi in range(height):
		for wi in range(width):
			point_0_1 = [0] * points
			num = 0
			for i in range(radius * 3):
				for j in range(radius * 3):
					if (hi - (radius - i) < 0 or hi - (radius - i) > height - 1 or wi - (radius - j) < 0 or wi - (radius - j) > width - 1) == 0:
						if hi != hi - (radius - i) and wi != wi - (radius - j):
							if image[hi,wi] < image[hi - (radius - i), wi - (radius - j)]:
								point_0_1[num] += 1

					if hi != hi - (radius - i) and wi != wi - (radius - j):			
						num += 1 

			helper_func(point_0_1)

			image[hi,wi] = int(helper_lbp(point_0_1))


def helper_func(points):

	points[3], points[4] = points[4], points[3]
	points[4], points[7] = points[7], points[4]
	points[5], points[6] = points[6], points[5]



def helper_lbp(points):
	num = 0

	for i in range(len(points)):
		if points[i] == 1:
			num += math.pow(2,i)

	return num


def feature_vector(image):		#create Feature vector
	
	height, width = image.size

	pixel_of_image = image.load()

	feat_vec = [0] * (width * height)

	index = 0

	for i in range(height):
		for j in range(width):
			feat_vec[index] = pixel_of_image[i,j]
			index += 1
	

	return feat_vec




def find_class_num(euc, train_keys,train):		#find tests train class

	for i in range(len(euc)):
		euc[i] = train[train_keys[euc[i]]]

	temp = 	0 

	temp2 = 0 

	for i in range(len(euc)):

		num = euc.count(euc[i])

		if num > temp:
			temp = num
			temp2 = euc[i]

	return temp2


def find_equality_ratio(euc, test_keys, test):		#find how many train class is equal to test images class

	ratio = 0


	for i in range(len(euc)):
		if euc[i] == test[test_keys[i]]:
			ratio += 1

	return (ratio / len(euc)) * 100



def find_test_trains_euc(train_vect, test_vect, k):  # herbir train icin euclidian hesaplar


	euc_vector = [0] * len(train_vect)


	for i in range(len(train_vect)):
		euc_vector[i] = euclidian(test_vect, train_vect[i])


	index_of_knn = [0] * k

	for i in range(k):
		
		minn = min(euc_vector)
		t1 = euc_vector.index(minn)
		
		for j in range(i):
			if t1 >= index_of_knn[j]:
				t1 += 1

		index_of_knn[i] = t1


		euc_vector.remove(minn)



	return index_of_knn


def euclidian(feat_vec, train_vec):		#euclidian hesaplar

	euc = 0

	for i in range(len(feat_vec)):
		euc += math.pow(feat_vec[i] - train_vec[i], 2)
	euc = math.sqrt(euc)

	return euc



def main():
	
	train, test, classes, dirname = load_test_train_classes_files()

	k = 3

	for i in range(1, len(dirname) - 1):

		print (str(i) + " th test accuracy rate:")

		find_accuracy_rate(train, test, k)

		test = load_files(dirname[i], "test.txt")



if __name__ == '__main__':
	main()

