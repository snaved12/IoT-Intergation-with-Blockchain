A Blockchain Framework for IoT Data Management and Security
 
Project Overview
This project demonstrates a basic blockchain application for an IoT system using Python and the Web3.py library to interact with an Ethereum-based blockchain (such as Ganache). The application consists of three main components:
1.	IoT Data Simulation: Simulates an IoT device that collects temperature data using an Arduino sensor.
2.	Blockchain Component: Records and verifies IoT data as transactions on the blockchain.
3.	Smart Contracts: A simple smart contract to automate data integrity verification.
Implementation
The implementation consists of three parts:
1.	Reading Data from an IoT Device (Arduino): The Python script reads temperature data from an Arduino device connected via a serial port.
2.	Blockchain Transaction: The data collected is then sent as a transaction to the local Ethereum blockchain (Ganache).
3.	Data Retrieval: Finally, the script retrieves the data from the blockchain and verifies the transaction details.

Arduino Code:
//21BCT0366 SYED NAVED
int baselineTemp = 0;

int celsius = 0;

int fahrenheit = 0;

void setup()
{
  pinMode(A0, INPUT);
  Serial.begin(9600);

}

void loop()
{
  // set threshold temperature to activate LEDs
  baselineTemp = 40;
  // measure temperature in Celsius
  celsius = map(((analogRead(A0) - 20) * 3.04), 0, 1023, -40, 125);
  // convert to Fahrenheit
  fahrenheit = ((celsius * 9) / 5 + 32);
  Serial.print(celsius);
  Serial.print(" C, ");
  Serial.print(fahrenheit);
  Serial.println(" F");
  Serial.println("SYED NAVED 21BCT0366");
  delay(1000); // Wait for 1000 millisecond(s)
}
Explanation of the code's working:
1.	Setup Phase:
o	Configures pin A0 to read input from a temperature sensor.
o	Initializes serial communication at a baud rate of 9600 to send data to the Serial Monitor.
2.	Loop Phase:
o	Reads the analog value from the sensor on pin A0.
o	Converts the analog value to a temperature in Celsius using a mapping formula.
o	Converts the Celsius temperature to Fahrenheit.
o	Prints both temperature values (Celsius and Fahrenheit) and a name identifier to the Serial Monitor.
o	Waits for 1 second before repeating the process.
The code continuously reads and displays temperature readings every second.
Python Code:
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

Explanation of the Code
1.	Reading Temperature Data from Arduino:
o	The code first lists all available serial ports on the computer to find the correct port connected to the Arduino.
o	It sets up a serial communication instance with a baud rate of 9600 to match the Arduino's communication speed.
o	It continuously reads temperature data sent by the Arduino over the serial connection.
2.	Sending Data to Ganache (Local Ethereum Blockchain):
o	The code uses Web3.py to connect to a local Ethereum blockchain running on Ganache (http://127.0.0.1:7545).
o	It fetches the current nonce (transaction count) for the sender's Ethereum account.
o	The temperature data read from the Arduino is converted into hexadecimal format (data field) and included in the transaction.
o	A transaction object is created, specifying the recipient's address, a small amount of Ether to be sent (0.01 Ether), gas limit, gas price, and the encoded temperature data.
o	The transaction is signed using the sender's private key and then sent to the blockchain.
3.	Retrieving and Displaying Transaction Data:
o	After the transaction is sent, the transaction hash is printed for reference.
o	The code retrieves the transaction details from the blockchain using the transaction hash and displays the input field, which contains the encoded temperature data.
Key Steps:
1.	Serial Communication:
o	Reads temperature data from Arduino using serial communication.
2.	Web3 Interaction:
o	Uses Web3.py to send the temperature data as part of a blockchain transaction on Ganache.
3.	Transaction Handling:
o	Signs and sends a transaction containing the temperature data and retrieves it back from the blockchain.
Purpose:
The code continuously monitors temperature data from the Arduino and logs it onto a local Ethereum blockchain (Ganache), providing a decentralized and secure way to store IoT sensor data.
Code Documentation
1.	read_arduino_data():
o	Purpose: Reads temperature data from an Arduino device connected to a specified COM port.
o	Return: The temperature data read from the Arduino.
o	Description: Initializes the serial communication, reads available ports, connects to the specified port, and reads data.
2.	send_data_to_blockchain(data):
o	Purpose: Sends temperature data as a transaction to the blockchain.
o	Args: data - The temperature data to be sent.
o	Return: The transaction hash of the sent transaction.
o	Description: Connects to a local Ethereum blockchain using Web3.py, prepares a transaction containing the temperature data, signs it with the sender's private key, and sends it.
3.	retrieve_transaction_data(tx_hash):
o	Purpose: Retrieves and displays the transaction data from the blockchain.
o	Args: tx_hash - The hash of the transaction to retrieve.
o	Description: Connects to the blockchain and fetches the details of the specified transaction, then prints the input data (temperature data).
Evaluation and Results
•	Performance and Functionality:
o	The application successfully reads data from an Arduino and records it as a transaction on a local Ethereum blockchain.
o	Transaction Speed: Transactions are processed relatively quickly on a local Ganache network. However, speed might vary based on network conditions in a real Ethereum network.
o	Security: Transactions are signed using a private key, ensuring authenticity and integrity of the data sent.
•	Challenges Faced:
o	Port Configuration: Selecting the correct COM port for the Arduino was a challenge. It required iterating over available ports to find the correct one.
o	Data Encoding: Converting the temperature data into a format suitable for blockchain transactions (hexadecimal) required using specific Web3.py utilities.
o	Gas Management: Estimating the gas cost for transactions needed careful consideration to ensure sufficient funds.
•	Potential Improvements:
o	Improved Error Handling: Add error handling to manage cases where the transaction fails or the data cannot be retrieved.
o	Scalability: Use a more scalable blockchain network or layer-2 solutions for handling large amounts of IoT data.
Conclusion
This project demonstrates the feasibility of integrating IoT data with a blockchain, enhancing data security and integrity. The application can be improved by adding more robust error handling, scalability solutions, and smart contract functionalities.
References
•	Web3.py Documentation
•	Ganache Documentation





 


