import math
import array
import sys
import csv

#---------------------------------------------------------------------------------------
# Professor's Implementations
#---------------------------------------------------------------------------------------

def makeBitArray(bitSize, fill = 0):
    intSize = bitSize >> 5                   # number of 32 bit integers
    if (bitSize & 31):                      # if bitSize != (32 * n) add
        intSize += 1                        #    a record for stragglers
    if fill == 1:
        fill = 4294967295                                 # all bits set
    else:
        fill = 0                                      # all bits cleared

    bitArray = array.array('I')          # 'I' = unsigned 32-bit integer
    bitArray.extend((fill,) * intSize)
    return(bitArray)

  # testBit() returns a nonzero result, 2**offset, if the bit at 'bit_num' is set to 1.
def testBit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = 1 << offset
    return(array_name[record] & mask)

# setBit() returns an integer with the bit at 'bit_num' set to 1.
def setBit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = 1 << offset
    array_name[record] |= mask
    return(array_name[record])

# clearBit() returns an integer with the bit at 'bit_num' cleared.
def clearBit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = ~(1 << offset)
    array_name[record] &= mask
    return(array_name[record])

# toggleBit() returns an integer with the bit at 'bit_num' inverted, 0 -> 1 and 1 -> 0.
def toggleBit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = 1 << offset
    array_name[record] ^= mask
    return(array_name[record])


#---------------------------------------------------------------------------------------
# Cache Penetration / Bloom Filter Implementation
#---------------------------------------------------------------------------------------

# n = ceil(m / (-k / log(1 - exp(log(p) / k))))
# p = pow(1 - exp(-k / (m / n)), k)
# m = ceil((n * log(p)) / log(1 / pow(2, log(2))))
# k = round((m / n) * log(2))

# They're surprisingly simple: take an array of m bits, 
# and for up to n different elements, either test or set 
# k bits using positions chosen using hash functions. 
# If all bits are set, the element probably already exists, 
# with a false positive rate of p; if any of the bits are not set, 
# the element certainly does not exist.

class BloomFilter:
    def __init__(self, n):
        self.n = n                                                                          # size of array
        p = 0.0000001                                                                       # false positive rate
        self.m = math.ceil((self.n * math.log(p)) / math.log(1 / pow(2, math.log(2))))      # bit array size
        self.k = round((self.m / self.n) * math.log(2))                                     # hash functions
        
        self.m = int(self.m)
        self.k = int(self.k)

        self.bit_array = makeBitArray(self.m)

    def add(self, element):
        for i in range(self.k):
            h = hash(element + str(i)) % self.m                                             # calculating the hash value for each element  
            setBit(self.bit_array,h)                                                        # setting bit to 1

    def check(self, element):
        for i in range(self.k):
            h = hash(element + str(i)) % self.m
            if  testBit(self.bit_array,h) == 0: return False                                # if bit is 0 it means it's not available in the database
        return True

def readEmailData():
    if len(sys.argv) > 1:
        output = [None,None]
        with open(sys.argv[1], 'r') as file:
            csvreader = list(csv.reader(file))[1:]
            output[0] = csvreader
        with open(sys.argv[2], 'r') as file:
            csvreader = list(csv.reader(file))[1:]
            output[1] = csvreader
        return output

data = readEmailData()
if data:
    filter = BloomFilter(len(data[0]))
    for x in data[0]:
        email = x[0]
        filter.add(email)
    for x in data[1]:
        email = x[0]
        if filter.check(email):
            print(email+',Probably in the DB')
        else:
            print(email+ ',Not in the DB')
            