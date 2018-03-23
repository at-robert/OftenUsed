import os

byte = []

byte.append(0x47)
byte.append(0x45)
byte.append(0x4F)
byte.append(0x42)

RealSize = ((byte[0]&0x7F)<<21) + ((byte[1]&0x7F)<<14) + ((byte[2]&0x7F)<<7) + (byte[3]&0x7F)
print(" {}".format(hex(RealSize)))