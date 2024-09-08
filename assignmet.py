#21BCT0366 SYED NAVED
import serial.tools.list_ports
from web3 import Web3

# **Step 1: Read Temperature Data from Arduino**

# Find available serial ports
ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()
portsList = []

for onePort in ports:
    portsList.append(str(onePort))
    print(str(onePort))

# Specify the COM port connected to Arduino
val = 7  # Change this to the correct COM port number if necessary
for x in range(0, len(portsList)):
    if portsList[x].startswith("COM" + str(val)):
        portVar = "COM" + str(val)
        print(f"Selected port: {portVar}")

# Initialize serial communication
serialInst.baudrate = 9600
serialInst.port = portVar
serialInst.open()

# Initialize Web3 for interacting with Ganache
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

account_1 = "0x88F3C5B6651e5f76863AF09a3816A4f5A51dB751"  # Replace with your account address
account_2 = "0x6E96e1384E9a4FD954F10947e069fEbAf0D1eEbF"  # Replace with recipient address
private_key = "0x6ee80840cc9c93423f03ca2bc7068981a9a2fb3fddc29e4dd841fbb6b6a5bb82"  # Replace with your private key

# Infinite loop to continuously read data from Arduino
while True:
    if serialInst.in_waiting:
        # Read temperature data from Arduino
        packet = serialInst.readline()
        temperature_data = packet.decode('utf').rstrip('\n')
        print(f"Temperature Data: {temperature_data}")

        # **Step 2: Send Temperature Data as a Transaction to Ganache**

        # Get the nonce for the transaction
        nonce = web3.eth.get_transaction_count(account_1)

        # Convert temperature data to hexadecimal format
        data = web3.to_hex(text=temperature_data)

        # Define the transaction
        tx = {
            'nonce': nonce,
            'to': account_2,
            'value': web3.to_wei(0.01, 'ether'),  # Small ether value
            'gas': 2000000,
            'gasPrice': web3.to_wei('50', 'gwei'),
            'data': data  # Add temperature data in the transaction
        }

        # Sign the transaction
        signed_tx = web3.eth.account.sign_transaction(tx, private_key)

        # Send the signed transaction
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(f"Transaction sent! Hash: {web3.to_hex(tx_hash)}")

        # **Step 3: Retrieve and Display Sent Data from the Transaction**

        # Fetch the transaction details using Web3.py
        tx_details = web3.eth.get_transaction(tx_hash)

        # Display the transaction data
        print(f"Retrieved Transaction Data: {tx_details['input']}")
