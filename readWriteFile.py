#-----------------------------------------------------
# Example code to read from fixed length records (random access file)
#-----------------------------------------------------
import sys
import random
import os.path

TOKEN_SIZE = 14
FREQ_SIZE = 4
RECORD_SIZE = TOKEN_SIZE + FREQ_SIZE + 2
num_records = 0
filename='input.txt'

def main():

    if not os.path.isfile(filename):
        print(filename, "not found")
        exit()

    else:		
        print("\n------------- Testing write record ------------\n")

        f = open('input.txt', 'w')

        print("Record 0: Token = information - Freq = 30")
        writeRecord(f, "information", 30)

        print("Record 1: Token = retrieval - Freq = 20")
        writeRecord(f, "retrieval", 20)

        print("Record 2: Token = the - Freq = 100")
        writeRecord(f, "the", 100)

        print("Record 3: Token = intellectualizations - Freq = 5")
        writeRecord(f, "intellectualizations", 5)

        f.close()   #close the file when done
	
        print("\n------------- Testing read record ------------\n")
        
        f = open('input.txt', 'r')

        recordNum = 3
        record = getRecord(f, recordNum)        
        if record[1] is True:
            print("Record {}: {}".format(recordNum, record[0]))
        else:
            print("Could not get record {}".format(recordNum))

        recordNum = 0
        record = getRecord(f, recordNum)        
        if record[1] is True:
            print("Record {}: {}".format(recordNum, record[0]))
        else:
            print("Could not get record {}".format(recordNum))

        f.close()   #close the file when done


# Get record number n (Records numbered from 0 to NUM_RECORDS-1) 
def getRecord(f, recordNum):

	record = ""
	global num_records
	global RECORD_SIZE
	Success = False
	if recordNum >= 0 and recordNum < num_records:
		f.seek(0,0)
		f.seek(RECORD_SIZE * recordNum) #offset from the beginning of the file
		record = f.readline()
		Success = True
	#f.close()
	return " ".join(record.split()), Success
	
# Write a record to the file.  The record consists of a token with width 14, freq with width of 4, one for space and one for new line.  This is a total of 20 for record size.    
def writeRecord(f, token, freq):
    global num_records
    #token[0:min(len(token), TOKEN_SIZE)] - if token is > TOKEN_SIZE, it would truncate the token by getting a substring of the first TOKEN_SIZE characters
    f.write(token[0:min(len(token), TOKEN_SIZE)].rjust(TOKEN_SIZE))
    f.write(' ')
    
    tempFreq = min(freq, (int)(pow(10, FREQ_SIZE)-1))
    f.write(str(tempFreq).rjust(FREQ_SIZE))

    f.write("\r")
    num_records += 1
    
main()