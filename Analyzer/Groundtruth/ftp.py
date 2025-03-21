
semantic_Types = ['Static', 'Group', 'String', 'Bit Field', 'Bytes', 'Filename', 'Auth']
semantic_Functions = ['Command', 'Length', 'Delim', 'CheckSum', 'Aligned', 'Authentication','Resource']

ftp_Syntax_Groundtruth = {}
ftp_Semantic_Groundtruth = {}
ftp_Semantic_Functions_Groundtruth = {}
ftp_commandOffset = '-1'
ftp_lengthOffset = '-1'
ftp_Syntax_Groundtruth[0] = [-1, 3, 4, 12]
ftp_Syntax_Groundtruth[1] = [-1, 3, 4, 12]
ftp_Syntax_Groundtruth[2] = [-1, 2]
ftp_Syntax_Groundtruth[3] = [-1, 3]
ftp_Syntax_Groundtruth[4] = [-1, 3, 4, 12]
ftp_Syntax_Groundtruth[5] = [-1, 3, 4, 12]
ftp_Syntax_Groundtruth[6] = [-1, 3, 4, 12]
ftp_Syntax_Groundtruth[7] = [-1, 3, 7]
ftp_Syntax_Groundtruth[8] = [-1, 3, 7]
ftp_Syntax_Groundtruth[9] = [-1, 3]
ftp_Syntax_Groundtruth[10] = [-1, 3]


# USER;PASS;PWD;LIST;RETR;STOR;DELE;MKD;RMD;PASV;QUIT
# USER webadmin\r\n
# semantic_Types = ['Static', 'Group', 'String', 'Bit Field', 'Bytes', 'Filename', 'Auth']
ftp_Semantic_Groundtruth[0] = {
    '0,1,2,3': semantic_Types[1],
    '4': semantic_Types[2],   
    '5,6,7,8,9,10,11,12': semantic_Types[6],   
    '13,14': semantic_Types[0],
}
# PASS webadmin\r\n
ftp_Semantic_Groundtruth[1] = {
    '0,1,2,3': semantic_Types[1],
    '4': semantic_Types[2],   
    '5,6,7,8,9,10,11,12': semantic_Types[6],   
    '13,14': semantic_Types[0], 
}
# PWD\r\n
ftp_Semantic_Groundtruth[2] = {
    '0,1,2': semantic_Types[1],   
    '3,4': semantic_Types[0], 
}
# LIST\r\n
ftp_Semantic_Groundtruth[3] = {
    '0,1,2,3': semantic_Types[1],   
    '4,5': semantic_Types[0],   
}
# RETR test.txt\r\n
ftp_Semantic_Groundtruth[4] = {
    '0,1,2,3': semantic_Types[1],
    '4': semantic_Types[2],   
    '5,6,7,8,9,10,11,12': semantic_Types[5],   
    '13,14': semantic_Types[0],
}
# STOR test.txt\r\n
ftp_Semantic_Groundtruth[5] = {
    '0,1,2,3': semantic_Types[1],
    '4': semantic_Types[2],   
    '5,6,7,8,9,10,11,12': semantic_Types[5],   
    '13,14': semantic_Types[0],
}
# DELE test.txt\r\n
ftp_Semantic_Groundtruth[6] = {
    '0,1,2,3': semantic_Types[1],
    '4': semantic_Types[2],   
    '5,6,7,8,9,10,11,12': semantic_Types[5],   
    '13,14': semantic_Types[0],
}
# MKD test\r\n
ftp_Semantic_Groundtruth[7] = {
    '0,1,2': semantic_Types[1],
    '3': semantic_Types[2],   
    '4,5,6,7': semantic_Types[5],
    '8,9': semantic_Types[0],
}
# RMD test\r\n
ftp_Semantic_Groundtruth[8] = {
    '0,1,2': semantic_Types[1],
    '3': semantic_Types[2],   
    '4,5,6,7': semantic_Types[5],
    '8,9': semantic_Types[0],
}
# PASV\r\n
ftp_Semantic_Groundtruth[9] = {
    '0,1,2,3': semantic_Types[1],   
    '4,5': semantic_Types[0],  
}
# QUIT\r\n
ftp_Semantic_Groundtruth[10] = {
    '0,1,2,3': semantic_Types[1],   
    '4,5': semantic_Types[0],   
}


# The start position of the command is the command semantics, and the space return line is used as the separator
# USER;PASS;PWD;LIST;RETR;STOR;DELE;MKD;RMD;PASV;QUIT
# USER webadmin\r\n
# semantic_Functions = ['Command', 'Length', 'Delim', 'CheckSum', 'Aligned', 'Authentication',"Resource"]
ftp_Semantic_Functions_Groundtruth[0] = {
    '0,1,2,3': semantic_Functions[0],
    '4': semantic_Functions[2],   
    '5,6,7,8,9,10,11,12': semantic_Functions[5],   
    '13,14': semantic_Functions[2],
}
# PASS webadmin\r\n
ftp_Semantic_Functions_Groundtruth[1] = {
    '0,1,2,3': semantic_Functions[0],
    '4': semantic_Functions[2],   
    '5,6,7,8,9,10,11,12': semantic_Functions[5],   
    '13,14': semantic_Functions[2], 
}
# PWD\r\n
ftp_Semantic_Functions_Groundtruth[2] = {
    '0,1,2': semantic_Functions[0],   
    '3,4': semantic_Functions[2], 
}
# LIST\r\n
ftp_Semantic_Functions_Groundtruth[3] = {
    '0,1,2,3': semantic_Functions[0],   
    '4,5': semantic_Functions[2],   
}
# RETR test.txt\r\n
ftp_Semantic_Functions_Groundtruth[4] = {
    '0,1,2,3': semantic_Functions[0],
    '4': semantic_Functions[2],   
    '5,6,7,8,9,10,11,12': semantic_Functions[6],   
    '13,14': semantic_Functions[2],
}
# STOR test.txt\r\n
ftp_Semantic_Functions_Groundtruth[5] = {
    '0,1,2,3': semantic_Functions[0],
    '4': semantic_Functions[2],   
    '5,6,7,8,9,10,11,12': semantic_Functions[6],   
    '13,14': semantic_Functions[2],
}
# DELE test.txt\r\n
ftp_Semantic_Functions_Groundtruth[6] = {
    '0,1,2,3': semantic_Functions[0],
    '4': semantic_Functions[2],   
    '5,6,7,8,9,10,11,12': semantic_Functions[6],   
    '13,14': semantic_Functions[2],
}
# MKD test\r\n
ftp_Semantic_Functions_Groundtruth[7] = {
    '0,1,2': semantic_Functions[0],
    '3': semantic_Functions[2],   
    '4,5,6,7': semantic_Functions[6],
    '8,9': semantic_Functions[2],
}
# RMD test\r\n
ftp_Semantic_Functions_Groundtruth[8] = {
    '0,1,2': semantic_Functions[0],
    '3': semantic_Functions[2],   
    '4,5,6,7': semantic_Functions[6],
    '8,9': semantic_Functions[2],
}
# PASV\r\n
ftp_Semantic_Functions_Groundtruth[9] = {
    '0,1,2,3': semantic_Functions[0],   
    '4,5': semantic_Functions[2],  
}
# QUIT\r\n
ftp_Semantic_Functions_Groundtruth[10] = {
    '0,1,2,3': semantic_Functions[0],   
    '4,5': semantic_Functions[2],   
}