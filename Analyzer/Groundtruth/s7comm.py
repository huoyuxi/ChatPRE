semantic_Types = ['Static', 'Group', 'String', 'Bit Field', 'Bytes']
semantic_Functions = ['Command', 'Length', 'Delim', 'CheckSum', 'Aligned', 'Filename']
s7comm_Syntax_Groundtruth = {}
s7comm_lengthOffset = '13,14,15,16'
s7comm_commandOffset = '8'
# Read Request (RRQ) / Write Request (WRQ)
s7comm_Syntax_Groundtruth[0] = [-1, 0, 1,3,4,5,6,7,8,10,12,14,16,17,18,20,22]  
s7comm_Syntax_Groundtruth[1] = [-1, 0, 1,3,4,5,6,7,8,10,12,14,16,17,18,19,20,22,24,26,27]  
s7comm_Syntax_Groundtruth[2] = [-1, 0, 1,3,4,5,6,7,8,10,12,14,16,17,18,19,20,21,22,24,26,27,30,31,32,34] 
s7comm_Syntax_Groundtruth[3] = [-1, 0, 1,3,4,5,6,7,8,10,12,14,16,17,18,19,20,21,22,23,24,25,26,28,30] 

s7comm_Semantic_Groundtruth = {}
# Job:Setup communication
# Job:Read Var
# Job:Write Var
# Userdata:Request
s7comm_Semantic_Groundtruth[0] = {
    '0': semantic_Types[0],   # TPKT Version
    '1': semantic_Types[3],   # TPKT Reserved
    '2,3': semantic_Types[3],   # TPKT length
    '4': semantic_Types[3],   # COTP length
    '5': semantic_Types[0],   # COTP PDU Type
    '6': semantic_Types[3],   # COTP TPDU number
    '7': semantic_Types[0],   # S7 Protocol ID
    '8': semantic_Types[1],   # S7 command
    '9,10': semantic_Types[3],   # S7 Redundancy Identification
    '11,12': semantic_Types[3],   # S7 Protocol Data Unit Reference
    '13,14': semantic_Types[3],   # S7 Parameter length
    '15,16': semantic_Types[3],   # S7 Data length
    '17': semantic_Types[1],   # S7 Function
    '18': semantic_Types[3],   # S7 Reserved
    '19,20': semantic_Types[3],   # S7 Max AmQ
    '21,22': semantic_Types[3],   # S7 Max AmQ
    '23,24': semantic_Types[3],   # S7 PDu length
}
s7comm_Semantic_Groundtruth[1] = {
    '0': semantic_Types[0],   # TPKT Version
    '1': semantic_Types[3],   # TPKT Reserved
    '2,3': semantic_Types[3],   # TPKT length
    '4': semantic_Types[3],   # COTP length
    '5': semantic_Types[0],   # COTP PDU Type
    '6': semantic_Types[3],   # COTP TPDU number
    '7': semantic_Types[0],   # S7 Protocol ID
    '8': semantic_Types[1],   # S7 ROSCTR
    '9,10': semantic_Types[3],   # S7 Redundancy Identification
    '11,12': semantic_Types[0],   # S7 Protocol Data Unit Reference
    '13,14': semantic_Types[3],   # S7 Parameter length
    '15,16': semantic_Types[3],   # S7 Data length
    '17': semantic_Types[1],   # S7 Function
    '18': semantic_Types[3],   # S7 Item count
    '19': semantic_Types[1],   # S7 Variable specification
    '20': semantic_Types[3],   # S7 Length of following address specification
    '21': semantic_Types[0],   # S7 Syntax Id
    '22': semantic_Types[3],   # S7 Transport size
    '23,24': semantic_Types[3],   # S7 Length
    '25,26': semantic_Types[3],   # S7 DB number
    '27': semantic_Types[0],   # S7 Area
    '28,29,30': semantic_Types[3],   # S7 Address
}
s7comm_Semantic_Groundtruth[2] = {
    '0': semantic_Types[0],   # TPKT Version
    '1': semantic_Types[3],   # TPKT Reserved
    '2,3': semantic_Types[3],   # TPKT length
    '4': semantic_Types[3],   # COTP length
    '5': semantic_Types[0],   # COTP PDU Type
    '6': semantic_Types[3],   # COTP TPDU number
    '7': semantic_Types[0],   # S7 Protocol ID
    '8': semantic_Types[1],   # S7 ROSCTR
    '9,10': semantic_Types[3],   # S7 Redundancy Identification
    '11,12': semantic_Types[3],   # S7 Protocol Data Unit Reference
    '13,14': semantic_Types[3],   # S7 Parameter length
    '15,16': semantic_Types[3],   # S7 Data length
    '17': semantic_Types[1],   # S7 Function
    '18': semantic_Types[3],   # S7 Item count
    '19': semantic_Types[1],   # S7 Variable specification
    '20': semantic_Types[3],   # S7 Length of following address specification
    '21': semantic_Types[0],   # S7 Syntax Id
    '22': semantic_Types[3],   # S7 Transport size
    '23,24': semantic_Types[3],   # S7 Length
    '25,26': semantic_Types[3],   # S7 DB number
    '27': semantic_Types[0],   # S7 Area
    '28,29,30': semantic_Types[3],   # S7 Address
    '31': semantic_Types[3],   # S7 Return code
    '32': semantic_Types[3],   # S7 Transport size
    '33,34': semantic_Types[3],   # S7 Data length
    '35,36,37,38': semantic_Types[4],   # S7 Data
}
s7comm_Semantic_Groundtruth[3] = {
    '0': semantic_Types[0],   # TPKT Version
    '1': semantic_Types[3],   # TPKT Reserved
    '2,3': semantic_Types[3],   # TPKT length
    '4': semantic_Types[3],   # COTP length
    '5': semantic_Types[0],   # COTP PDU Type
    '6': semantic_Types[3],   # COTP TPDU number
    '7': semantic_Types[0],   # S7 Protocol ID
    '8': semantic_Types[1],   # S7 ROSCTR
    '9,10': semantic_Types[3],   # S7 Redundancy Identification
    '11,12': semantic_Types[3],   # S7 Protocol Data Unit Reference
    '13,14': semantic_Types[3],   # S7 Parameter length
    '15,16': semantic_Types[3],   # S7 Data length
    '17': semantic_Types[1],   # S7 Function
    '18': semantic_Types[3],   # S7 Item count
    '19': semantic_Types[1],   # S7 Variable specification
    '20': semantic_Types[3],   # S7 Length of following address specification
    '21': semantic_Types[0],   # S7 Syntax ID
    '22': semantic_Types[0],   # S7 Type
    '23': semantic_Types[1],   # S7 Function Group
    '24': semantic_Types[1],   # S7 Subfunction
    '25': semantic_Types[3],   # S7 Return code
    '26': semantic_Types[3],   # S7 Transport size
    '27,28': semantic_Types[3],   # S7 Data length
    '29,30': semantic_Types[0],   # S7 SZL-ID
    '31,32': semantic_Types[3],   # S7 SZL-Index
}

s7comm_Semantic_Functions_Groundtruth = {}

s7comm_Semantic_Functions_Groundtruth[0] = {
    '8': semantic_Functions[0],   # S7 command
    '13,14': semantic_Functions[1],   # S7 Parameter length
    '15,16': semantic_Functions[1],   # S7 Data length
    '17': semantic_Functions[0],   # S7 Function
    '23,24': semantic_Functions[1],   # S7 PDu length
}
s7comm_Semantic_Functions_Groundtruth[1] = {
    '2,3': semantic_Functions[1],   # TPKT length
    '4': semantic_Functions[1],   # COTP length
    '8': semantic_Functions[0],   # S7 ROSCTR
    '13,14': semantic_Functions[1],   # S7 Parameter length
    '15,16': semantic_Functions[1],   # S7 Data length
    '17': semantic_Functions[0],   # S7 Function
    '23,24': semantic_Functions[1],   # S7 Length
}
s7comm_Semantic_Functions_Groundtruth[2] = {
    '2,3': semantic_Functions[1],   # TPKT length
    '4': semantic_Functions[1],   # COTP length
    '8': semantic_Functions[0],   # S7 ROSCTR
    '13,14': semantic_Functions[1],   # S7 Parameter length
    '15,16': semantic_Functions[1],   # S7 Data length
    '17': semantic_Functions[0],   # S7 Function
    '23,24': semantic_Functions[1],   # S7 Length
    '33,34': semantic_Functions[1],   # S7 Data length
}
s7comm_Semantic_Functions_Groundtruth[3] = {
    '2,3': semantic_Functions[1],   # TPKT length
    '4': semantic_Functions[1],   # COTP length
    '8': semantic_Functions[0],   # S7 ROSCTR
    '13,14': semantic_Functions[1],   # S7 Parameter length
    '15,16': semantic_Functions[1],   # S7 Data length
    '17': semantic_Functions[0],   # S7 Function
    '20': semantic_Functions[1],   # S7 Length of following address specification
    '27,28': semantic_Functions[1],   # S7 Data length
}