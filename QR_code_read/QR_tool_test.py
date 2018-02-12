from qrtools import QR


c = QR(filename='./qr-codes-business-cards.jpg')

if c.decode():
    print("QR Data = {}".format(c.data_to_string()))