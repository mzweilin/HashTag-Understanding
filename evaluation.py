import csv
import numpy
from job import Job

import logging
logging.basicConfig(level=logging.INFO)
logger = logging



def evaluate():
    matrix = numpy.array(list(csv.reader(open("eval.csv","rb"),delimiter=','))).astype('string')
    retrieved = []

    for i in range(1,len(matrix)):
        hashtag = matrix[i][1]
        
        logger.info(hashtag)
        logger.info("expected urls: %s %s %s" % (matrix[i][3], matrix[i][4], matrix[i][5]))

        job  = Job(hashtag)
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

        recall = float(url1Retrieved+url2Retrieved+url3Retrieved)/length
        # if url1Retrieved+url2Retrieved+url3Retrieved > 0:
        #     recall = 1
        # else:
        #     recall = 0
        logger.info("Recall of %s: %f" % (hashtag, recall))
        retrieved.append(recall)

    print retrieved

if __name__ == "__main__":
	evaluate()
        


    
    
    