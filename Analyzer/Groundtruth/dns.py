# 60ff01000001000000000000076578616d706c6503636f6d0000010001
semantic_Types = ['Static', 'Group', 'String', 'Bit Field', 'Bytes']
semantic_Functions = ['Command', 'Length', 'Delim', 'CheckSum', 'Aligned', 'Filename']


dns_Syntax_Groundtruth = {}

#format1
dns_Syntax_Groundtruth[0] = [-1,1,3,5,7,9,11,24]

#Groundtruth: based on protocol specifications + Wireshark

dns_Semantic_Groundtruth = {}

dns_Semantic_Functions_Groundtruth = {}

dns_lengthOffset = '4,5'

dns_commandOffset = '7'

''' Semantic-Type Groudtruth'''

#format1
dns_Semantic_Groundtruth[0] = {
    '0,1':semantic_Types[1],# Command
    '2,3':semantic_Types[0],# Standard
    '4,5':semantic_Types[3],# Questio
    '6,7':semantic_Types[0],# Answer
    '8,9':semantic_Types[3],# Authority
    '10,11':semantic_Types[3],# Additional
    '12,13,14,15,16,17,18,19,20,21,22,24':semantic_Types[3],# Domain
    '25,26':semantic_Types[3],# Class
    }


''' Semantic-Function Groudtruth'''
dns_Semantic_Functions_Groundtruth[0] = {
    '4,5':semantic_Functions[1],
    '7':semantic_Functions[0],
}