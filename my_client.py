# import bluetooth

# bd_addr = "90:68:C3:C3:A5:7C"

# port = 20

# sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
# sock.connect((bd_addr, port))

# sock.send("hello")
# sock.close()


import bluetooth

bd_addr = "90:68:C3:C3:A5:7C"

port = 20

sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((bd_addr, port))

print("connected.  type stuff")
while True:
    data = input()
    if len(data) == 0: break
    sock.send(data)

sock.close()
