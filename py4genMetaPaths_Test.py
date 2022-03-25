import sys
import os
import random
from tqdm import tqdm
from collections import Counter

class MetaPathGenerator:
	def __init__(self):
		self.id_firm = dict()
		self.id_image = dict()
		self.id_object = dict()
		
		# self.object_coobjectlist = dict()
		self.firm_objectlist = dict()
		self.object_firmlist = dict()
		self.image_object = dict()
		self.object_image = dict()
		self.firm_image = dict()
		self.image_firm = dict()

	def read_data(self, dirpath):
		# object dict
		with open(dirpath + "/id_object.txt",encoding = "ISO-8859-1") as odictfile:
			for line in odictfile:
				toks = line.strip().split("\t")
				if len(toks) == 2:
					self.id_object[toks[0]] = toks[1].replace(" ", "")  #e.g.,   {'438659': 'aMichaelJ.Rothman'} {'109954': '1dbarcode'}



		#print "#objects", len(self.id_firm)
		# firm dict
		with open(dirpath + "/id_firm.txt",encoding = "ISO-8859-1") as fdictfile:
			for line in fdictfile:
				toks = line.strip().split("\t")
				if len(toks) == 2:
					newfirm = toks[1].replace(" ", "")
					self.id_firm[toks[0]] = newfirm  # e.g.,   {'4789': 'vVLDBJ.'} {'0': '1800flowers'}
		# image dict
		with open(dirpath + "/id_image_2020.txt",encoding = "ISO-8859-1") as idictfile:
			for line in idictfile:
				toks = line.strip().split("\t")
				if len(toks) == 2:
					image = toks[1].replace(" ", "")
					self.id_image[toks[0]] = image  # e.g.,  {'818': '1800flowers+2020-01-02_14-59-34_UTC'}

		#print "#firm", len(self.id_object)


		# image_object edge file, and object_image_edge_file
		with open(dirpath + "/image_object_2020.txt",encoding = "ISO-8859-1") as iofile:
			for line in iofile:
				toks = line.strip().split("\t")
				if len(toks) == 2:
					i, o = toks[0], toks[1]
					if i not in self.image_object:
						self.image_object[i] = []
					self.image_object[i].append(o)  #  {'21525': ['33467']}



					if o not in self.object_image:
						self.object_image[o] = []
					self.object_image[o].append(i) # {'33467': ['21525']}




		# firm_image and image_firm edge file
		with open(dirpath + "/firm_image_2020.txt",encoding = "ISO-8859-1") as iffile:
			for line in iffile:
				toks = line.strip().split("\t")
				if len(toks) == 2:
					f, i = toks[0], toks[1]
					self.image_firm[i] = f  # {'818': '0'}



					if f not in self.firm_image:
						self.firm_image[f] = []
					self.firm_image[f].append(i) # {'0': ['818']}



		sumimagesfirm, sumobjectsfirm = 0, 0
		firm_objects = dict()
		for firm in self.firm_image:
			images = self.firm_image[firm]  # a list of image of a particular firm
			sumimagesfirm += len(images)
			for image in images:
				if image in self.image_object:
					objects = self.image_object[image] # objects who write the particular image
					sumobjectsfirm += len(objects)

		# print("#firms  ", len(self.firm_image))
		# print("#images ", sumimagesfirm,  "#images per firm ", sumimagesfirm / len(self.firm_image))


	def generate_random_aca(self, outfilename, numwalks, walklength):
		for firm in self.firm_image: # firm id
			self.firm_objectlist[firm] = []
			for image in self.firm_image[firm]:
				if image not in self.image_object: continue
				for object in self.image_object[image]:
					self.firm_objectlist[firm].append(object)
					if object not in self.object_firmlist:
						self.object_firmlist[object] = []
					self.object_firmlist[object].append(firm)


		#print "object-firm list done"

		outfile = open(outfilename, 'w')
		for firm in self.firm_objectlist:
			firm0 = firm
			# for every firm, repeat "numwalks" many walk
			for j in tqdm(range(0, numwalks)): #wnum walks
				outline = self.id_firm[firm0] #outline: initial point, firm

				for i in range(0, walklength):
					images = self.firm_image[firm0]

					numi = len(images)
					imageid = random.randrange(numi)
					image = images[imageid]
					outline = outline +  " " + self.id_image[image]

					if image not in self.image_object: continue

					objects = self.image_object[image]
					numo = len(objects)
					objectid = random.randrange(numo)
					object = objects[objectid]
					outline = outline + " " + self.id_object[object]

					images = self.object_image[object]
					numi = len(images)
					imageid = random.randrange(numi)
					image = images[imageid]
					outline += " " + self.id_image[image]

					if image not in self.image_firm: continue
					firms = self.image_firm[image]
					numf = len(firms)
					firmid = random.randrange(numf)
					firm = firms[firmid]
					outline += " " + self.id_firm[firm]





				outfile.write(outline + "\n")

		outfile.close()


#python py4genMetaPaths_Test.py 1000 100 net_aminer output.aminer.w1000.l100.txt
#python py4genMetaPaths_Test.py 50 10 net_IG   output.IG.w50.l10.txt

dirpath = "net_aminer" 
# OR 
dirpath = "net_dbis"

dirpath = "net_IG"
numwalks = int(sys.argv[1])
walklength = int(sys.argv[2])

dirpath = sys.argv[3]
outfilename = sys.argv[4]

def main():
	mpg = MetaPathGenerator()
	mpg.read_data(dirpath)
	mpg.generate_random_aca(outfilename, numwalks, walklength)


if __name__ == "__main__":
	main()






























