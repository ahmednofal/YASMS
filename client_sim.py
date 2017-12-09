import socket
import sys
from curses import ascii
import pickle 
from messages_formats import SecondPart as SP
from messages_formats import FirstPart as FP
from messages_formats import ASecondPart as ASP
from messages_formats import AFirstPart as AFP
from messages_formats import message as msg
from messages_formats import messagetype as msgty
from utils import CAport, peerport
from utils import myip
import sqlite3
import oauth2
import utils
class client(object):
    # Here implementing the authentication functionality
    # B ip will be request via the directory service from the CA authority
    def __init__(self, CA_ip, sock):
        self.CA_ip = CA_ip
        self.sock = sock
    def receive_message_till_EOT(self):
        acc = bytearray(bytes("", encoding='utf_8'))
        # Here , collecting the data from the socket
        while True:
            self.data = self.sock.recv(1024)
            print (type(self.data))
            print (self.data)
            acc += bytearray(self.data)
            the_byte_flag = self.data[-1] 
            the_chr = chr(the_byte_flag)
            if ord(the_chr) == ascii.EOT:
                    break
        return acc

    def create_db():
        conn = sqlite3.connect('peers.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE peers(
        name text,
        ip text,
        pub_key integer
        )
        """)
    def generate_req(self,B_ip, KB):
        # The L value will be generated in an automated way
        L = 23123
        Na2 = oauth2.generate_nonce() 
        Na1 = oauth2.generate_nonce()
        # should enc Na2 before next line
        Na2_asbytes = bytes(str(Na2), encoding="utf_8")
        # The pre line might be instead of encryption or after encryption, it depends if encryption takes bytes or value, like in int
        Na2_enc_asbytes = bytearray(Na2_asbytes)
        data_to_send_ASP = ASP(myip(), B_ip, Na2_enc_asbytes, L, Na1)
    
        data_to_send_ASP_byted = pickle.dumps(data_to_send_ASP)
        data_to_send_AFP = AFP(utils.myip(), B_ip, data_to_send_ASP_byted)
    
        data_byted = bytearray(pickle.dumps(data_to_send_AFP)) 
        auth_req_as_msg = bytearray(pickle.dumps(msg(msgty.authentication, data_byted)))
        
        auth_req_as_msg.append(ascii.EOT)
        return auth_req_as_msg
    def parse_CA_res(self,msg_bytes):
        info_about_peer = pickle.loads(msg_bytes)
        info_to_peer = (info_about_peer.__dict__["FifthPart_enc_asbytes"])
        return info_to_peer

    def send_info_to_peer(self,info_to_peer, B_ip):
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.sock.connect((B_ip , peerport))

        info_to_peer = bytearray(info_to_peer)
        info_to_peer.append(ascii.EOT)
        self.sock.sendall(info_to_peer)

    def auth_com(self,B_ip, KB): # WARNING
        auth_req_as_msg = self.generate_req(B_ip, KB)        
        self.sock.sendall(auth_req_as_msg)     
        CA_response = self.receive_message_till_EOT()
        info_to_peer = self.parse_CA_res(CA_response)

        self.send_info_to_peer(info_to_peer, B_ip) 

    def connect_to(self, name):
        #B_ip, KB = get_IP_pub_key(name)
        B_ip = '127.0.0.1'
        KB = 12312
        self.auth_com(B_ip, KB)
    def serve_peer_req(self):
        self.sock.listen(1)
        conn, addr = self.sock.accept()
        self.receive_message_till_EOT()

# Create a socket (SOCK_STREAM means a TCP socket)
 
try:
    # Connect to server and send data
    #imagine encrypting Na2
    # should encrypt Na2 after pickling it
    if (sys.argv[2] == '-c'):
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('127.0.0.1', CAport))

        this_machine = client(sys.argv[1], sock)

        this_machine.connect_to("B")
    if (sys.argv[2] == '-s'):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("localhost", peerport))
        this_machine = client(sys.argv[1], sock)
        this_machine.serve_peer_req()
finally:
    print("done")
    # Receive data from the server and shut down


