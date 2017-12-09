from datetime import datetime
import time
from enum import Enum
# A , B, KA , TS, L, Na1
S = "S IP"
A = "A IP"
B = "B IP"
KA_ = 123
TS_ = datetime.fromtimestamp(time.time())
L_ = 1231
Na1_ = "23231"

class messagetype(Enum):
    authentication = 1
    chat = 2
    directoryserv = 3

mtype_ = messagetype.authentication 
class AFirstPart(object):
    def __init__(self,
            A_ip = A,
            B_ip = B,
            ASecondPart_enc_asbytes = bytearray(bytes("", encoding = 'utf_8'))):
        self.A_ip = A_ip
        self.B_ip = B_ip
        self.ASecondPart_enc_asbytes = ASecondPart_enc_asbytes
class ASecondPart(object):
    def __init__(self,
            A_ip =A, 
            B_ip = B,
            Na2_enc_asbytes = bytearray(bytes("", encoding = 'utf_8')),
            L = L_,
            Na1 = Na1_):
        self.A_ip = A_ip
        self.B_ip = B_ip 
        self.Na2_enc_asbytes = Na2_enc_asbytes
        self.L = L 
        self.Na1 = Na1 
class SecondPart(object):
    def __init__(self, 
            A_ip= A, 
            B_ip= B, 
            KA = KA_, 
            TS = TS_, 
            L = L_,
            Na1 = Na1_):

        self.A_ip = A_ip    
        self.B_ip = B_ip
        self.KA = KA
        self.TS = TS
        self.L = L
        self.Na1 = Na1


# S , A, {A , B, KA , TS, L, Na1}k−1S
class FirstPart(object):
    def __init__(self, 
            S_ip=S, 
            A_ip= A, 
            SecondPart_enc_asbytes = bytearray(bytes("", encoding = 'utf_8'))):
        self.S_ip = S_ip
        self.A_ip = A_ip
        self.SecondPart_enc_asbytes = SecondPart_enc_asbytes

class FifthPart(object):
    def __init__(self, 
            A_ip = A, 
            B_ip = B, 
            KA = KA_, 
            TS = TS_, 
            L = L_, 
            Na2_enc_asbytes = bytearray(bytes("", encoding = 'utf_8'))
            ):
        self.A_ip = A_ip, 
        self.B_ip = B_ip, 
        self.KA = KA_, 
        self.TS = TS_, 
        self.L = L_, 
        self.Na2_enc_asbytes = Na2_enc_asbytes
class FourthPart(object):
    def __init__(self,
            S_ip = S,
            A_ip = A,
            B_ip = B,
            FifthPart_enc_asbytes = bytearray(bytes("", encoding = 'utf_8'))):
        self.S_ip = S_ip
        self.A_ip = A_ip
        self.B_ip = B_ip
        self.FifthPart_enc_asbytes= FifthPart_enc_asbytes
# All messages int the system are to use this class, the mtype specifies mmessage type whether it is an authentication protocol message or not, for now , there are other types that could be added 
class message(object):
    def __init__(self,
            mtype = mtype_,
            message_bytes = bytearray(bytes("", encoding = 'utf_8'))):
        self.mtype = mtype
        self.message_bytes = message_bytes
        # { S, A, B, {A , B, K A , T S , L, {Na2 } kA−1}kS−1}k B



# {A , B, K A , T S , L, {Na2 } KA-1


