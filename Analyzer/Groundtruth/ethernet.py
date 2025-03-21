
semantic_Types = ['Static', 'Group', 'String', 'Bit Field', 'Bytes']
semantic_Functions = ['Command', 'Length', 'Delim', 'CheckSum', 'Aligned', 'Filename']


ethernet_Syntax_Groundtruth = {}

#format1
ethernet_Syntax_Groundtruth[0] = [-1,1,3,7,11,19,23,25]
ethernet_Syntax_Groundtruth[1] = [-1,1,3,7,11,19,23,27,29,31,33,35,37,39,41]
ethernet_Syntax_Groundtruth[2] = [-1,1,3,7,11,19]
ethernet_Syntax_Groundtruth[3] = [-1,1,3,5,6,7,9]

#Groundtruth: based on protocol specifications + Wireshark

ethernet_Semantic_Groundtruth = {}

ethernet_Semantic_Functions_Groundtruth = {}

ethernet_lengthOffset = '2,3'

ethernet_commandOffset = '0,1'

''' Semantic-Type Groudtruth'''
# 6500
# 6f00
# 6600
# 6300
#format1
# semantic_Types = ['Static', 'Group', 'String', 'Bit Field', 'Bytes']
# Modified dictionary
ethernet_Semantic_Groundtruth[0] = {
    '0,1': semantic_Types[1],  # command. According to the constraints, Command should be of Group type.
    '2,3': semantic_Types[3],  # length. According to the constraints, Length should be of Integer type, represented by Bit Field.
    '4,5,6,7': semantic_Types[3],  # Session. Considered as an Integer type, represented by Bit Field.
    '8,9,10,11': semantic_Types[3],  # Status. Considered as an Integer type, represented by Bit Field.
    '12,13,14,15,16,17,18,19': semantic_Types[2],  # context. Considered as a String type.
    '20,21,22,23': semantic_Types[3],  # Options. Considered as an Integer type, represented by Bit Field.
    '24,25': semantic_Types[0],  # Version. Considered as an Static type.
    '26,27': semantic_Types[3],  # length. According to the constraints, Length should be of Integer type, represented by Bit Field.
}
ethernet_Semantic_Groundtruth[1] = {
    '0,1': semantic_Types[1],  # command. According to the constraints, Command should be of Group type.
    '2,3': semantic_Types[3],  # length. According to the constraints, Length should be of Integer type, represented by Bit Field.
    '4,5,6,7': semantic_Types[3],  # Session. Considered as an Integer type, represented by Bit Field.
    '8,9,10,11': semantic_Types[3],  # Status. Considered as an Integer type, represented by Bit Field.
    '12,13,14,15,16,17,18,19': semantic_Types[2],  # context. Considered as a String type.
    '20,21,22,23': semantic_Types[3],  # Options. Considered as an Integer type, represented by Bit Field.
    '24,25,26,27': semantic_Types[3],  # Interface Handle. Considered as an Integer type, represented by Bit Field.
    '28,29': semantic_Types[3],  # Timeout. Considered as an Integer type, represented by Bit Field.
    '30,31': semantic_Types[3],  # count. According to the constraints, considered as an Integer type, represented by Bit Field.
    '32,33': semantic_Types[3],  # ID. Considered as an Integer type, represented by Bit Field.
    '34,35': semantic_Types[3],  # length. According to the constraints, Length should be of Integer type, represented by Bit Field.
    '36,37': semantic_Types[3],  # ID. Considered as an Integer type, represented by Bit Field.
    '38,39': semantic_Types[3],  # length. According to the constraints, Length should be of Integer type, represented by Bit Field.
    '40,41': semantic_Types[3],  # response. Considered as an Integer type, represented by Bit Field.
    '42,43': semantic_Types[3],  # status. Considered as an Integer type, represented by Bit Field.
}
ethernet_Semantic_Groundtruth[2] = {
    '0,1': semantic_Types[1],  # command. According to the constraints, Command should be of Group type.
    '2,3': semantic_Types[3],  # length. According to the constraints, Length should be of Integer type, represented by Bit Field.
    '4,5,6,7': semantic_Types[3],  # Session. Considered as an Integer type, represented by Bit Field.
    '8,9,10,11': semantic_Types[3],  # Status. Considered as an Integer type, represented by Bit Field.
    '12,13': semantic_Types[3],  # Time ms. According to the constraints, Time should be of Integer type, represented by Bit Field.
    '14,15,16,17,18,19,20,21': semantic_Types[2],  # context. Considered as a String type.
    '22,23,24,25': semantic_Types[3],  # Options. Considered as an Integer type, represented by Bit Field.
}
ethernet_Semantic_Groundtruth[3] = {
    '0,1': semantic_Types[1],  # command. According to the constraints, Command should be of Group type.
    '2,3': semantic_Types[3],  # length. According to the constraints, Length should be of Integer type, represented by Bit Field.
    '12,13,14,15,16,17,18,19': semantic_Types[2],  # context. Considered as a String type.
    '28,29': semantic_Types[3],  # Timeout. Considered as an Integer type, represented by Bit Field.
    '30,31': semantic_Types[3],  # count. According to the constraints, considered as an Integer type, represented by Bit Field.
    '34,35': semantic_Types[3],  # length. According to the constraints, Length should be of Integer type, represented by Bit Field.
    '38,39': semantic_Types[3],  # length. According to the constraints, Length should be of Integer type, represented by Bit Field.
}

''' Semantic-Function Groudtruth'''
ethernet_Semantic_Functions_Groundtruth[0] = {
    '0,1': semantic_Functions[0],  # command. 
    '2,3': semantic_Functions[1],  # length. 
    '26,27': semantic_Functions[1],  # count. 
}

ethernet_Semantic_Functions_Groundtruth[1] = {
    '0,1': semantic_Functions[0],  # command. 
    '2,3': semantic_Functions[1],  # length. 
    '30,31': semantic_Functions[1],  # count. 
    '34,35': semantic_Functions[1],  # length. 
    '38,39': semantic_Functions[1],  # length.
}


ethernet_Semantic_Functions_Groundtruth[2] = {
    '0,1': semantic_Functions[0],  # command. 
    '2,3': semantic_Functions[1],  # length.
}

ethernet_Semantic_Functions_Groundtruth[3] = {
    '0,1': semantic_Functions[0],  # command. 
    '2,3': semantic_Functions[1],  # length.
}