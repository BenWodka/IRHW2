class FixedLengthFile:
    def __init__(self, recordSize):
        self.stream = None
        self.recordSize = recordSize
        self.numRecords = -1
    
    def openForWrite(self, filename):
        self.stream = open(filename, 'w')
        self.numRecords = 0
        return True
    
    def openForRead(self, filename, numRecords):
        self.stream = open(filename, 'r')
        self.numRecords = numRecords
        return True
    
    def closeAfterWriting(self):
        if self.stream:
            self.stream.close()
            self.numRecords = -1
        return self.numRecords
    
    def closeAfterReading(self):
        if self.stream:
            self.stream.close()
            self.numRecords = -1
        return True
    
    def writeRecord(self, *args):
        raise NotImplementedError("This method should be overridden by subclasses")
    
    def readRecord(self, record_num):
        raise NotImplementedError("This method should be overridden by subclasses")

class MapFile(FixedLengthFile):
    def __init__(self):
        super().__init__(record_size=20)

    def writeRecord(self, filename):
        if self.stream:
            token = filename[0:min(len(filename), 14)].rjust(14)
            self.stream.write(token + '\n')
            self.num_records += 1
            return True
        return False

    def readRecord(self, record_num):
        if record_num < 0 or record_num >= self.num_records:
            return None, False
        
        self.stream.seek(0, 0)
        self.stream.seek(self.record_size * record_num)
        record = self.stream.readline()
        return record.strip(), True
    


class InvertedFile:
    def __init__(self):
        self.map_file = MapFile()
        self.dict_file = DictFile()  # You need to define this class
        self.post_file = PostFile()  # You need to define this class
        self.config_file = "config.txt"
    
    def openForWrite(self):
        return self.map_file.openForWrite("map.txt") and \
               self.dict_file.openForWrite("dict.txt") and \
               self.post_file.openForWrite("post.txt")
    
    def openForRead(self):
        with open(self.config_file, 'r') as config:
            num_records = list(map(int, config.readline().split()))
            return self.map_file.openForRead("map.txt", num_records[0]) and \
                   self.dict_file.openForRead("dict.txt", num_records[1]) and \
                   self.post_file.openForRead("post.txt", num_records[2])
    
    def closeAfterWriting(self):
        map_count = self.map_file.closeAfterWriting()
        dict_count = self.dict_file.closeAfterWriting()
        post_count = self.post_file.closeAfterWriting()
        with open(self.config_file, 'w') as config:
            config.write(f"{map_count} {dict_count} {post_count}")
        return True
    
    def closeAfterReading(self):
        return self.map_file.closeAfterReading() and \
               self.dict_file.closeAfterReading() and \
               self.post_file.closeAfterReading()
    
    # Additional methods to read and write records...
