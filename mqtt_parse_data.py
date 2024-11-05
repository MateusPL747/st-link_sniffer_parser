import paho.mqtt.client as mqtt
import struct

# MQTT broker details
BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "UWB_test/#"

# Callback when a message is received
def on_message(client, userdata, msg):

    # Read memory
    data = msg.payload

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

def main():
    # Create an MQTT client instance
    client = mqtt.Client()

    # Attach the on_message callback function
    client.on_message = on_message

    # Connect to the MQTT broker
    client.connect(BROKER, PORT, 60)

    # Subscribe to the topic
    client.subscribe(TOPIC)

    # Start the loop to process received messages
    client.loop_forever()

if __name__ == "__main__":
    main()
