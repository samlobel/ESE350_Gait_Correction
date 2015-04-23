import bluetooth
import sys


target_name = "SamPhone"
target_address = None

nearby_devices = bluetooth.discover_devices()

for bdaddr in nearby_devices:
	print bdaddr
	if target_name == bluetooth.lookup_name(bdaddr):
		target_address = bdaddr
		break
if target_address:
	print "target_address is ", target_address
else:
	print "No dice"