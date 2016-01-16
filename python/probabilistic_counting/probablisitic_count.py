from __future__ import division
import base64

class ProbabilisticCount:

    def __init__(self, byte_string=None):
        self.NUM_SALTS = 64
        self.HASH_LENGTH = 20
        self.NUM_BYTES = 5
        if byte_string:
            self.HASH_STRING = base64.b64decode(byte_string.strip())
        else:
            self.HASH_STRING = chr(0) * self.NUM_SALTS * self.HASH_LENGTH

    def get_byte_array(self):
        return base64.b64encode(self.HASH_STRING)

    def combine(self, byte_string_list):
        for byte_string in byte_string_list:
            byte_string = base64.b64decode(byte_string.strip())
            hash_length = self.NUM_SALTS * self.HASH_LENGTH
            new_hash_list = []
            for i in xrange(0, hash_length):
                new_hash_list.append(chr(ord(self.HASH_STRING[i]) |  ord(byte_string[i])))
            self.HASH_STRING = ''.join(new_hash_list)

    def get_zero_bit_position(self, start_byte, num_bytes):
        start_bit = start_byte*8
        max_bit = (start_byte + num_bytes) * 8

        for curr_position in xrange(start_bit, max_bit):
            curr_byte = curr_position // 8
            curr_bit = curr_position % 8

            if not (ord(self.HASH_STRING[curr_byte]) & (0x1 << curr_bit)):
                return curr_position - start_bit

        return self.HASH_LENGTH * 8

    def estimate(self):
        bits = 0
        z=0
        for salt in xrange(0, self.NUM_SALTS): #64
            for slice in xrange(0, self.HASH_LENGTH//self.NUM_BYTES): #
                start_byte = (salt * self.HASH_LENGTH) + (slice * self.NUM_BYTES)
                bits += self.get_zero_bit_position(start_byte, self.NUM_BYTES)/((self.HASH_LENGTH / self.NUM_BYTES) * self.NUM_SALTS)

        return long(pow(2, bits) / 0.77351)

    # derived function based on the previous ones to provide a count of elements common between current and other object
    # counter2 is an object of the same type
    def intersection(self, counter2):
        count1 = self.estimate()
        count2 = counter2.estimate()
        self.combine([counter2.get_byte_array()])
        combined_count = self.estimate()
        return count1 + count2 - combined_count


# first byte string. will be read from the database
str1 = '/38IAAD//wEAAP//AQAA/38BAAD//wAAAP9/AAAA//8EAAD//wEAAP//AAAA//8AAAD//wAAAP+/AwAA/38AAAD//wkAAP9/AgAA//8AAAD//wkAAP//AAAA//8DAAD/fwIAAP//BQAA//8AAAD//wEAAP//AQAA//8EAAD/fwIAAP//AQAA//8BAAD//wUAAP//AQAA//8CAAD//wIAAP//BAAA/38BAAD//wEAAP//AQAA/38BAAD//wAAAP8/FQAA/78AAAD/vwEAAP//CAAA//8BAAD//wAAAP9/BQAA//8DAAD//wIAAP//AQAA/38EAAD//wAAAP//AQAA/38BAAD//wAAAP//AQAA//8AAAD//wAAAP//DAAA//8CAAD//wMAAP//AQAA/38BAAD/3wkAAP9/EAAA//8AAAD/fwYAAP8/AQAA/38AAAD//wEAAP//AQAA/38BAAD//wIAAP//AAAA//8AAAD/fwIAAP//AQAA/38BAAD//wEAAP//AQAA/78DAAD/fwAAAP//AAAA//8BAAD//wEAAP9/AAAA//8BAAD//wAAAP//BwAA//8BAAD//yEAAP//CQAA//8AAAD/fwUAAP//BgAA//8AAAD//wEAAP//AAAA//8BAAD/fwMAAP+/AAAA/38AAAD//wAAAP//BAAA//8AAAD/vwAAAP//FAAA/38BAAD//wEAAP9/CwAA/38QAAD//xEAAP//AQAA/39AAAD//wEAAP//BQAA/38AAAD//xcAAP//AwAA/78EAAD//wEAAP//BQAA/38CAAD//wEAAP9/EAAA//8JAAD//wUAAP8/AQAA//8CAAD/PwMAAP//AwAA//8AAAD/fwAAAP//CQAA/38AAAD//wAAAP//QgAA/38QAAD/fwEAAP//AwAA//8AAAD//xEAAP//AgAA/38CAAD//wEAAP//AAAA/38JAAD//wAAAP//BAAA//8BAAD//wAAAP//AQAA//8AAAD//wgAAP//AQAA//8gAAD/fwEAAP9/AAAA/38AAAD/fxEAAP//AQAA//8BAAD//wEAAP//AwAA/38BAAD//wMAAP9/AgAA/38AAAD//wAAAP//AAAA//8BAAD/fwQAAP//EwAA//8mAAD//wEAAP9/DAAA//8CAAD//wMAAP9/AAAA/18BAAD/fwEAAP//AAAA//8FAAD//xMAAP9/AAAA//8BAAD/fwYAAP//AwAA//8AAAD//wUAAP//AgAA//8IAAD//wEAAP//BAAA//8BAAD//wAAAP//EAAA/38BAAD//wAAAP//AwAA/38AAAD//wMAAP9/AQAA//8BAAD//wEAAP//AQAA/38DAQD//wAAAP+/BAAA//8AAAD//woAAP9/AAAA//8AAAD/fwIAAP//AgAA/38AAAD//wAAAP//AAAA//8AAAD//wEAAP9/BwAA//8CAAD/fwAAAP//AAAA//8AAAD/fxEAAP//BQAA//8AAAD//wcAAP//AQAA/78BAAD/PwAAAP/fAQAA//8DAAD/vwUAAP+/AAAA/78AAAD/fyAAAP//AgAA/38BAAD/vwEAAP//AAAA/z8BAAD//wAAAP//AwAA//8DAAD//wAAAP//BAAA//8BAAD//wAAAP8/AQAA//8hAAD//wAAAP9/FAAA//8BAAD//wEAAP//AwAA//8FAAA='
# create object of this type
x = ProbabilisticCount(str1)
# second byte string. will be read from database
str2 = '//8DAAD//wsAAP//AQAA//8AAAD//wEAAP//BwAA//8NAAD//wUAAP//BQAA//8TAAD//wEAAP//AQAA//8AAAD//wkAAP//BwAA//8DAAD//wsAAP//BwAA//8BAAD//wcAAP//CQAA//8VAAD//xkAAP//AAAA//8DAAD//yEAAP//AQAA//8DAAD//x0AAP//BwAA//8BAAD//w8AAP//AwAA//8PAAD//wUAAP//AwAA//8BAAD//y4AAP//AwAA//8AAAD//yoAAP//BQAA//8CAAD//wMAAP//AgAA//9GAAD//wAAAP//BQAA//8lAAD//wEAAP//AQAA//8HAAD//xYAAP//FAAA//8SAAD//wMAAP//BwAA//8RAAD//yAAAP//AwAA//8DAAD//wAAAP//AQAA//8DAAD//wwAAP//CwIA//8DAAD//yYAAP//BQAA//8BAAD//wMAAP//BQAA/38BEAD//wUAAP//LwAA//8HAAD//wEAAP//BwAA//8HAAD//wMAAP//AwAA//8DAAD//wEAAP//AwAA//8CAAD//xMAAP//AwAA//8FAAD//wIAAP//BwAA//8hAAD//yIAAP//BgAA//8DAAD//wkAAP//QQAA//8iAAD//wEAAP//DwAA//8RAAD//wMAAP//BwAA//8FAAD//wcAAP//BwAA//8BAAD//wUAAP//AQAA//8BAAD/fwcAAP//AwAA//8HAAD//yEAAP//AQAA//8DAAD//wcAAP//AwAA//8HAAD//yUAAP9/BQAA//8DAAD//xUAAP//CwAA//8TAAD//xECAP//AgAA//8FAAD//w0AAP//LQAA//8FAAD//wkAAP//gwAA//8DAAD//wkAAP//BQAA//8LAAD//0IAAP//BQAA//8LAAD//wUAAP//EwAA//8CAAD//wMAAP//CwAA//8HAAD//wYAAP9/FgAA//8BAAD//wsAAP//EwAA//8BAAD//wEAAP//EQAA//8CAAD//wAAAP//AQAA//8HAAD//wIAAP//EQAA//+DAAD//wEAAP//CgAA//8VAAD//xEAAP//DwAA//8DAAD//wEAAP//BQAA//8DAAD//wMAAP//DwAA//8iAAD//wsAAP//IQAA//9FAAD//wsAAP//CwAA//+gAAD//wMAAP//BQAA//8GAAD//0kAAP//BwAA//8FAAD//yMAAP//AwAA//8FAAD//xMAAP//GAAA//8BAAD//wcAAP9/CQAA//8BAAD//wEAAP//AgAA//8LAAD//wwAAP//CQAA//8DAAD//wMAAP//BQAA//8XAAD//wMAAP//DQAA//8FAAD//wUAAP//CAAA//8DAAD//wMAAP//BwAA//8HAAD//wEAAP//AgAA//8HAAD//wEAAP//CAAA//8FAAD//wMAAP//CwAA//8RAAD//wMAAP//BQAA/38FAAD//0AAAP//AQAA//8jAAD//wMAAP//AwAA//8BAAD//yMAAP//AwAA//8BAAD//wMAAP//gQAA//8RAAD//wgAAP//AQAA//8BAAD//wgAAP//AQAA//8AAAD//wEAAP//AQAA//8HAAD//wYAAP//AQAA//8JAAD//wMAAP//AwAA//8DAAD//5MAAP//gQAA//8DAAD//wUAAP//AwAA//8FAAA='
# create object of this type
y = ProbabilisticCount(str2)
# find the number of elements common in these two
count = x.intersection(y)
print count
