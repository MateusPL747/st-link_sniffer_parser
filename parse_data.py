import logging
from pyocd.core.helpers import ConnectHelper
import time
import struct

# Set up logging
logging.basicConfig(level=logging.INFO)

# Specify the host and port
host = "localhost"
port = 50002

# debugers = ConnectHelper.get_all_connected_probes(blocking=True)
# print(debugers)

# Connect to the target
with ConnectHelper.session_with_chosen_probe(openocd_server=f"{host}:{port}", target='cortex_m') as session:
    target = session.target

    # Read 33 bytes from the memory address 0x200002e8
    address = 0x200002e8
    length = 33

    while (True):
        # Read memory
        data = target.read_memory_block8(address, length)

        # Print the data in hex format
        # print(" ".join(f"{byte:02x}" for byte in data))

        id_tag = ' '.join(f"{byte:02x}" for byte in data[:2])
        anchor_qty = int(data[2])

        print(f'Hole packet: {" ".join(f"{byte:02x}" for byte in data)}')
        print(f'tag id: {id_tag}')
        print(f'Anchor qty: {anchor_qty}')

        for i in range(1, anchor_qty + 1):
            #        tag_id + anchor_qty = ; each anchor length = 10
            offset = 3 + 10 * (i - 1)
            anchor_id = ' '.join(f"{byte:02x}" for byte in data[(offset):(offset + 2)])
            anchor_distance = struct.unpack('<d', bytes(data[(offset+2):(offset+2+8)]))[0]
            print(f'anchor {i} id: {anchor_id}')
            print(f'anchor {i} distance: {anchor_distance}')

        print()

        time.sleep(0.5)
