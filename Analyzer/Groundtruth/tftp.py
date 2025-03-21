semantic_Types = ['Static', 'Group', 'String', 'Bit Field', 'Bytes']
semantic_Functions = ['Command', 'Length', 'Delim', 'CheckSum', 'Aligned', 'Filename']
tftp_Syntax_Groundtruth = {}
tftp_lengthOffset = '-1'
tftp_commandOffset = '0,1'
# Read Request (RRQ) / Write Request (WRQ)
tftp_Syntax_Groundtruth[0] = [-1, 1]  
tftp_Syntax_Groundtruth[1] = [-1, 1, 3]  

tftp_Semantic_Groundtruth = {}

# ACK
tftp_Semantic_Groundtruth[0] = {
    '0,1': semantic_Types[1],   # Command
    '2,3': semantic_Types[3],   # Block ID
}

# DATA 
tftp_Semantic_Groundtruth[1] = {
    '0,1': semantic_Types[1],   # Command
    '2,3': semantic_Types[3],  # Block ID
    '4,5,6,7': semantic_Types[2]     # Data (Bytes)
}


tftp_Semantic_Functions_Groundtruth = {}

# RRQ/WRQ
tftp_Semantic_Functions_Groundtruth[0] = {
    '0,1': semantic_Functions[0],  # Opcode=Command
}

# DATA
tftp_Semantic_Functions_Groundtruth[1] = {
    '0,1': semantic_Functions[0],  # Block#=CheckSum（用于ACK确认）
    '4,5,6,7': semantic_Functions[5]  # file
}