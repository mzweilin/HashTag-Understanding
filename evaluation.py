import csv
import numpy
from job import Job



def evaluate():
	matrix = numpy.array(list(csv.reader(open("eval.csv","rb"),delimiter=','))).astype('string')

	retrieved = []

	for i in range(1,len(matrix)):
		print matrix[i][1]
		job  = Job(matrix[i][1])
		urls = job.execute()

		url1Retrieved  = 0
		url2Retrieved = 0
		url3Retrieved = 0
		for url in urls:
			#print url
			if (url == matrix[i][3] ):
				url1Retrieved  = 1
			if (url == matrix[i][4] ):
				url2Retrieved  = 1
			if (url == matrix[i][5] ):
				url3Retrieved  = 1

		if (matrix[i][5] == ''):
			length = 2
		else:
			length = 3

		retrieved.append(float(url1Retrieved+url2Retrieved+url3Retrieved)/length)


	print retrieved

		


	
    
	