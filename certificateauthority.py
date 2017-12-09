import socketserver
import marshal
import socket
import pickle 
from curses import ascii
from messages_formats import SecondPart as SP
from messages_formats import FirstPart as FP
from messages_formats import AFirstPart as AFP
from messages_formats import ASecondPart as ASP
from messages_formats import FourthPart as FoP
from messages_formats import FifthPart as FiP
from messages_formats import message as msg
from messages_formats import messagetype as msgty
import messages_formats
from datetime import datetime
import utils
import time
from utils import myip
from utils import to_msg
# Normally the certificate authority will handle two things 
# Authentication and directory handling
# Data Formatting applies here, incoming messages should contain
# a field specifying whether it is an authentication or
# Directory request
# During Directory request, keys of the communicator will be saved

# {S , A, {A , B, KA , TS, L, Na1}kS−1} kA
# steps to construct first message from S -> A
# Collect A, B, KA, TS, L, Na1 into a class
# pickle the collection : Collection1_pickled -> bytes returned
# bytes-> encrypt with KS-1 -> bytes2 returned
# bytes2-> include in collection2 as KS_1_enc_part
# pickle collection2 -> bytes3 returned
# bytes3 -> encrypt bytes3 -> bytes4 returned
# send bytes4 into the network
#               S Side
# ----------------------------------  




#               A Side
# ----------------------------------
# receive bytes4 -> decrypt with KA-priv into bytes3
# unpickle bytes3 -> collection2 restored 
# refer to third datamember in the class bytes2 -> decrypt with KS-pub
# bytes returned -> unpickle bytes
# collection1 restored
# can access elements via their class constructors
     
class CertificateAuthority(socketserver.BaseRequestHandler):
            
       
        
        
   
# Here we support the authentication functionality
    def receive_message_till_EOT(self):
        acc = bytearray(bytes("", encoding='utf_8'))
        # Here , collecting the data from the socket
        print("inside receive_message_server")
        while True:
            self.data = self.request.recv(1024)
            print (type(self.data))
            print (self.data)
            acc += bytearray(self.data)
            the_byte_flag =self.data[-1] 
            the_chr = chr(the_byte_flag)
            if ord(the_chr) == ascii.EOT:
                    break
        acc = acc[:-1]
        return acc
        pass
    def authenticate(self, user_req):
        print ("inside authenticate")
        self.data_dict = self.parse_incoming_req(user_req)

        self.send_comm_info(self.data_dict)

    def dispatch(self, the_com):
        print("inside dispatch")
        user_msg = pickle.loads(the_com)
        # should decide which service should this message be passedto 
        # here it will just be passed to the authentication service
        
        self.authenticate(user_msg.__dict__["message_bytes"])
    def parse_incoming_req(self, incoming_req):
        print("inside parse_incom_req")
        data_received_AFP = pickle.loads(incoming_req)
        data_received_ASP = pickle.loads(data_received_AFP.__dict__["ASecondPart_enc_asbytes"])
        received_A_ip = data_received_ASP.__dict__["A_ip"]
        received_B_ip = data_received_ASP.__dict__["B_ip"]
        received_Na2_enc_asbytes = data_received_ASP.__dict__["Na2_enc_asbytes"]
        received_L = data_received_ASP.__dict__["L"]
        received_Na1 = data_received_ASP.__dict__["Na1"]

# The KA is an example of a communicator's pub key that can be found in the 
# Directory, when there is a directory it will be extracted from it
        #KA = 34234
        #TS = datetime.fromtimestamp(time.time())
        return data_received_ASP.__dict__
    def encrypt_with_pub_key(pub_key):
        pass
    def decrypt_with_pub_key(pub_key):
        pass
    def send_comm_info(self, data_dict):
        print("inside send_comm")
        A_ip = data_dict["A_ip"]
        B_ip = data_dict["B_ip"]
        Na2_enc_asbytes = data_dict["Na2_enc_asbytes"]
        L = data_dict["L"]
        Na1 = data_dict["Na1"]
        TS = self.timestampit()
        data_back_SP = SP(A_ip,B_ip, messages_formats.KA_, TS,L, Na1)
        data_back_SP_bytes = pickle.dumps(data_back_SP)
        # imagine encryption and producing a byte array
        data_back_FP = FP(myip(), A_ip, data_back_SP_bytes)
        data_back_FP_bytes = pickle.dumps(data_back_FP)
        data_back_FiP = FiP(A_ip, B_ip, messages_formats.KA_, TS, L, Na2_enc_asbytes)
        data_back_FiP_bytes = pickle.dumps(data_back_FiP)
        data_back_FoP = FoP(myip(), A_ip, B_ip, data_back_FiP_bytes)
        data_back_FoP_bytes = pickle.dumps(data_back_FoP)
        #message_encapsulation = msg(msgty.authentication, data_back_FoP_bytes)

        #message_as_bytes = pickle.dumps(message_encapsulation)

        message_as_bytes = bytearray(data_back_FoP_bytes)
        message_as_bytes.append(ascii.EOT)
        print(type(message_as_bytes))
        print(message_as_bytes)


        self.request.sendall(message_as_bytes)
        pass
# Supporting api to enter only information that goes into the message


    def handle(self):
        # The following line assumes the req_received will
        # be returned from a call to dispatch
        # the call to receive_message_till_EOT() should return 
        # message class object to be parsed by the dispatch 
        # func
        self.req_received = self.receive_message_till_EOT()
        self.dispatch(self.req_received)
              
    def timestampit(self):
        return datetime.fromtimestamp(time.time())

    
# Here we support the directory functionality
# The simulation
#       i
#       i
#       i
if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    socketserver.TCPServer.allow_reuse_address = True
    	# Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), CertificateAuthority)
    print(server.server_address)
    	# Activate the server; this will keep running until you
    	# interrupt the program with Ctrl-C
    server.serve_forever()
	
