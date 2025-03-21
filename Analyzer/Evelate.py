#-*- coding:utf-8 -*-

import random
import socket
import time
import sys
import os
import shutil
from scapy.all import *
from scapy.all import IP, TCP, Raw, rdpcap
import Separator
import Corrector
import config
import copy
import fcntl
import binascii
import logging
import sys
log_format = '%(asctime)s - %(filename)s:%(lineno)d - %(message)s'
logging.basicConfig(filename=f'results/{sys.argv[1]}.log', level=logging.INFO, format=log_format, datefmt='%Y-%m-%d %H:%M:%S')
from AAA_Evaluation import *
from ChatPreResult import *

info_file_path = config.info_file_path
format_file_path = config.format_file_path

class Message:
    def __init__(self, ip_src, ip_dst, sport, dport, app_data):
        self.ip_src = ip_src
        self.ip_dst = ip_dst
        self.sport = sport
        self.dport = dport
        self.app_data = app_data

# print baseline results used in boofuzz
def Print_bo_Res(payload_message, Polyglot_Syntax, Polyglot_length_Res, Polyglot_command_Res, AutoFormat_ftrees, Tupni_Syntax):
    
    # with open(config.Boofuzz_bo_Res, "a") as file:
        
    for i in range(0,len(payload_message)):
        logging.info(f"\n\n\n\t########## Msg {i} ########## \n")
        logging.info(f"Application Layer Data:{payload_message[i]}\n")
        logging.info(f"\nPolyglot Syntax----------------------\n")
        logging.info(f"{Polyglot_Syntax[i]}\n")
        logging.info(f"\tPolyglot Command:{Polyglot_command_Res[i]}\n")
        logging.info(f"\tPolyglot Length:{Polyglot_length_Res[i]}\n")


        logging.info(f"\nAutoFormat Syntax----------------------\n")
        logging.info(f"{AutoFormat_ftrees[i]}\n")

        logging.info(f"\nTupni Syntax----------------------\n")
        logging.info(f"{Tupni_Syntax[i]}\n")



def SendInputMsg():
    thread =  sys.argv[8]
    ThreadId = int(thread)
    config.threadId = ThreadId
    # threadId = input("Please enter the value of threadId: ")
    # try:
    #     threadId = int(threadId)
    #     config.threadId = threadId
    # except ValueError:
    #     logging.info("The input values must be integers.")
    #     sys.exit(1)
    with open(r"Dataset/PUT_test_" + sys.argv[1] +r"/hex") as file:
        payload_message = file.readlines()
        payload_message = [bytes.fromhex(l) for l in payload_message]
    index = len(payload_message)
    config.baseline_mode = sys.argv[4]
    return index,payload_message

class Message_Result:
    def __init__(self, payload, fields, boundaries, field_types, field_funcs):
        self.payload = payload
        self.fields = fields
        self.boundaries = boundaries
        self.field_types = field_types
        self.field_funcs = field_funcs

def MonitorAnalysis(index: int, payload_message:list):


    #baseline res
    Polyglot_length_Res = [None] *index
    Polyglot_command_Res = [None] *index
    Polyglot_separator_Res = [None] *index
    Polyglot_Syntax = {}
    AutoFormat_ftrees = {}
    Tupni_Syntax = {}

    #settings
    baseline_mode = config.baseline_mode
    threadId = config.threadId
    ip = config.ip
    port = config.port

    message_Result = [None] * index
    message_Used = [None] * index
    Pre_message_Result = [None] * index


    #Analysis every msg sample
    for i in range(index):
        logging.info("\n\n+++++++++++++++++++++++ Msg {} +++++++++++++++++++++++".format(i))
        # new_directory = f"../PUT_test/{i}_tmp_results/"
        new_directory = f"PUT_test_{sys.argv[1]}/{i}_tmp_results/"
        with open(new_directory + "format.txt", 'r') as f:
            lines = f.readlines()
        matching_lines = [line for line in lines if re.match("^\[Message\].*", line)]
        recordNums = len(matching_lines)

        if baseline_mode == "oa" or baseline_mode == "ba" or baseline_mode == "all":

            fields, field_Types, field_Functions, used_fields = Separator.AllAnalysis_A(recordNums, new_directory,payload_message[i])

            message_Used[i] = used_fields

            boundaries = set()
            msg_len = len(payload_message[i])
            boundaries.add(-1)
            boundaries.add(msg_len-1)
            add_fields = []
            
            boundary_2 = -1
            for field in fields:
                boundary_1 = int(field.split(',')[0])-1
                boundaries.add(boundary_1)

                f_i = ','.join(str(i) for i in range(boundary_2+1, boundary_1+1))
                logging.info(f"add_field:{f_i}")
                if len(f_i)>0 :
                    add_fields.append(f_i)

                boundary_2 = int(field.split(',')[-1])
                boundaries.add(boundary_2)
            if boundary_2 < msg_len-1:
                f_i = ','.join(str(i) for i in range(boundary_2+1, msg_len))
                if len(f_i)>0 :
                    add_fields.append(f_i)
            
            for add_field in add_fields:
                if add_field not in fields:
                    fields.append(add_field)
                
            # logging.info(f"add_fields:{add_fields}")

            boundaries = sorted(list(boundaries))
#
            message_Result[i] = Message_Result(payload_message[i], fields, boundaries, field_Types,field_Functions)

            #print the BinPRE's results on the Message i
            logging.info(f"payload_message: {message_Result[i].payload}")
            logging.info(f"fields: {message_Result[i].fields}")
            logging.info(f"boundaries: {message_Result[i].boundaries}")
            logging.info(f"field_Types: {message_Result[i].field_types}")
            logging.info(f"field_Functions: {message_Result[i].field_funcs}")
            



        if baseline_mode == "bo" or baseline_mode == "all":
            Polyglot_length, Polyglot_keyword,Polyglot_separator,Polyglot_combined_format,AutoFormat_ftree,Tupni_format = Separator.AllAnalysis_B(recordNums, new_directory,payload_message[i])
            Polyglot_length_Res[i] = Polyglot_length
            Polyglot_command_Res[i] = Polyglot_keyword
            Polyglot_separator_Res[i] = Polyglot_separator
            Polyglot_Syntax[i] = Polyglot_combined_format
            AutoFormat_ftrees[i] = AutoFormat_ftree
            Tupni_Syntax[i] = Tupni_format


    
    
    if baseline_mode == "oa" or baseline_mode == "ba" or baseline_mode == "all":

        '''Semantic Refinment: Clustering & Type & Funcs'''

        for i in range(index):
            Pre_message_Result[i] = copy.deepcopy(message_Result[i])
        logging.info(f"Pre_message_Result:{Pre_message_Result[0].field_types}")

        message_Result = Corrector.Validation(message_Result,payload_message)
        logging.info(f"message_Result:{message_Result[0].field_types}")
        logging.info(f"Pre_message_Result:{Pre_message_Result[0].field_types}")

        
        '''Evaluation & Results Printing -- BinPRE'''
        
        Average_Accr, F1_score, Average_Perf = BinPREEvaluator(payload_message, Pre_message_Result, message_Result, config.commandOffset, message_Used)
        no_Semantic_Average_Pre, no_Semantic_Average_Rec, no_Semantic_F1_score, Semantic_Average_Pre, Semantic_Average_Rec, Semantic_F1_score = BinPRE_Semantic_Types_Evaluator(payload_message, Pre_message_Result, message_Result, config.commandOffset)
        no_Function_Average_Pre, no_Function_Average_Rec, no_Function_F1_score, Function_Average_Pre, Function_Average_Rec, Function_F1_score = BinPRE_Semantic_Functions_Evaluator(payload_message, Pre_message_Result, message_Result, config.commandOffset)

        logging.info(f"\n\n\n********* [Summary-{config.protocol_name}]: BinPRE Format Extraction *********")
        logging.info(f"Average_Accr:{Average_Accr}")
        # logging.info(f"Average_Pre:{Average_Pre}")
        # logging.info(f"Average_Rec:{Average_Rec}")
        logging.info(f"F1-score:{F1_score}")
        logging.info(f"Average_Perf:{Average_Perf}")
        logging.info(f"\n-----------------")

        logging.info(f"\n********* [Summary-{config.protocol_name}]: BinPRE(no refine) Semantic-Types Inference *********")
        logging.info(f"Average_Pre:{no_Semantic_Average_Pre}")
        logging.info(f"Average_Rec:{no_Semantic_Average_Rec}")
        logging.info(f"F1_score:{no_Semantic_F1_score}")


        logging.info(f"\n********* [Summary-{config.protocol_name}]: BinPRE#(refinement) Semantic-Types Inference *********")
        logging.info(f"Average_Pre:{Semantic_Average_Pre}")
        logging.info(f"Average_Rec:{Semantic_Average_Rec}")
        logging.info(f"F1_score:{Semantic_F1_score}")

        logging.info(f"\n-----------------")

        logging.info(f"\n********* [Summary-{config.protocol_name}]: BinPRE(no refine) Semantic-Functions Inference *********")
        logging.info(f"Average_Pre:{no_Function_Average_Pre}")
        logging.info(f"Average_Rec:{no_Function_Average_Rec}")
        logging.info(f"F1_score:{no_Function_F1_score}")

        logging.info(f"\n********* [Summary-{config.protocol_name}]: BinPRE#(refinement) Semantic-Functions Inference *********")
        logging.info(f"Average_Pre:{Function_Average_Pre}")
        logging.info(f"Average_Rec:{Function_Average_Rec}")
        logging.info(f"F1_score:{Function_F1_score}")
    
    if baseline_mode == "bo" or baseline_mode == "all":

        '''Evaluation & Results Printing -- Polyglot, AutoFormat, Tupni'''

        PolyglotEvaluator(payload_message,Polyglot_Syntax,config.commandOffset)
        Autoformat_syntaxRes = AutoFormatEvaluator(payload_message,config.commandOffset,AutoFormat_ftrees)
        TupniEvaluator(payload_message,Tupni_Syntax,config.commandOffset)
        for i in range(len(Polyglot_command_Res)):
            if Polyglot_command_Res[i] ==None:
                Polyglot_command_Res[i] = []
        Print_bo_Res(payload_message, Polyglot_Syntax, Polyglot_length_Res, Polyglot_command_Res, Autoformat_syntaxRes, Tupni_Syntax)
        
        Polyglot_SemanticEvaluator(payload_message, Polyglot_length_Res, Polyglot_command_Res, Polyglot_separator_Res, config.commandOffset)

def ChatPreAnalysis(index: int, payload_message:list):
    #settings
    baseline_mode = config.baseline_mode
    threadId = config.threadId
    ip = config.ip
    port = config.port
    chatpre_fields = eval(config.protocol_name + "_field_uesd")
    chatpre_field_type = eval(config.protocol_name + "_field_type")
    chatpre_field_func = eval(config.protocol_name + "_field_func")
    message_Result = [None] * index
    message_Used = [None] * index
    Pre_message_Result = [None] * index

    #Analysis every msg sample
    for i in range(index):
        logging.info("\n\n+++++++++++++++++++++++ Msg {} +++++++++++++++++++++++".format(i))
        # new_directory = f"../PUT_test/{i}_tmp_results/"
        new_directory = f"PUT_test_{sys.argv[1]}/{i}_tmp_results/"
        with open(new_directory + "format.txt", 'r') as f:
            lines = f.readlines()
        matching_lines = [line for line in lines if re.match("^\[Message\].*", line)]
        recordNums = len(matching_lines)

        if baseline_mode == "oa" or baseline_mode == "ba" or baseline_mode == "all":
            # semantic_Types = ['Static', 'Group', 'String', 'Bit Field', 'Bytes']
            # semantic_Functions = ['Command', 'Length', 'Static', 'CheckSum', 'Aligned', 'Filename']
            # fields, field_Types, field_Functions, used_fields = Separator.AllAnalysis_A(recordNums, new_directory,payload_message[i])
            fields = chatpre_fields[i]
            used_fields = chatpre_fields[i]
            field_Functions = chatpre_field_func[i]
            field_Types = chatpre_field_type[i]
            # for item in fields:
            #     if item not in field_Functions:
            #         fields.remove(item)
            for item in used_fields:
                if item not in field_Functions:
                    used_fields.remove(item)
            for item in field_Functions:
                if field_Functions[item][0].lower() == 'length':
                    field_Functions[item][0] = 'Length'
                    field_Types[item][0] = 'Bit Field'
                elif field_Functions[item][0].lower() == 'checksum':
                    field_Functions[item][0] = 'CheckSum'
                    field_Types[item][0] = 'Bit Field'
                elif 'file' in field_Functions[item][0].lower() :
                    field_Functions[item][0] = 'Filename'
                    field_Types[item][0] = 'String'
                elif 'delim' in field_Functions[item][0].lower() :
                    field_Functions[item][0] = 'Delim'
                    field_Types[item][0] = 'Static'
                elif 'command' in field_Functions[item][0].lower() :
                    field_Functions[item][0] = 'Command'
                    field_Types[item][0] = 'Group'
                elif 'static text' in field_Functions[item][0].lower() :
                    field_Functions[item][0] = 'Static'
                    field_Types[item][0] = 'String'
                elif 'version' in field_Functions[item][0].lower() :
                    field_Functions[item][0] = 'Static'
                    field_Types[item][0] = 'String'
            # fields = used_fields = ['2,3', '4', '5', '6', '8', '11,12', '13,14', '15,16', '17', '19,20', '21,22', '23,24']
            # field_Functions = {'2,3': ['Length'], '4': [], '5': [], '6': [], '8': [], '11,12': ['Aligned'], '13,14': ['Aligned'], '15,16': ['Aligned'], '17': ['Command'], '19,20': ['Aligned'], '21,22': ['Aligned'], '23,24': ['Length']}
            # field_Types = {'2,3': ['Group', 'Bit Field'], '4': ['Static'], '5': ['Static'], '6': ['Bit Field'], '8': ['Static'], '11,12': ['Static'], '13,14': ['Static'], '15,16': ['Static'], '17': ['Group'], '19,20': ['Static'], '21,22': ['Static'], '23,24': ['Bit Field']}
            message_Used[i] = used_fields

            boundaries = set()
            msg_len = len(payload_message[i])
            boundaries.add(-1)
            boundaries.add(msg_len-1)
            add_fields = []
            
            boundary_2 = -1
            for field in fields:
                boundary_1 = int(field.split(',')[0])-1
                boundaries.add(boundary_1)

                f_i = ','.join(str(i) for i in range(boundary_2+1, boundary_1+1))
                logging.info(f"add_field:{f_i}")
                if len(f_i)>0 :
                    add_fields.append(f_i)

                boundary_2 = int(field.split(',')[-1])
                boundaries.add(boundary_2)
            if boundary_2 < msg_len-1:
                f_i = ','.join(str(i) for i in range(boundary_2+1, msg_len))
                if len(f_i)>0 :
                    add_fields.append(f_i)
            
            for add_field in add_fields:
                if add_field not in fields:
                    fields.append(add_field)
                
            # logging.info(f"add_fields:{add_fields}")

            boundaries = sorted(list(boundaries))
#
            message_Result[i] = Message_Result(payload_message[i], fields, boundaries, field_Types,field_Functions)

            #print the ChatPRE's results on the Message i
            logging.info(f"payload_message: {message_Result[i].payload}")
            logging.info(f"fields: {message_Result[i].fields}")
            logging.info(f"boundaries: {message_Result[i].boundaries}")
            logging.info(f"field_Types: {message_Result[i].field_types}")
            logging.info(f"field_Functions: {message_Result[i].field_funcs}")

    '''Semantic Refinment: Clustering & Type & Funcs'''

    for i in range(index):
        Pre_message_Result[i] = copy.deepcopy(message_Result[i])
    logging.info(f"Pre_message_Result:{Pre_message_Result[0].field_types}")

    message_Result = Corrector.Validation(message_Result,payload_message)
    logging.info(f"message_Result:{message_Result[0].field_types}")
    logging.info(f"Pre_message_Result:{Pre_message_Result[0].field_types}")

    
    '''Evaluation & Results Printing -- ChatPre'''
    
    Average_Accr, F1_score, Average_Perf = ChatPreEvaluator(payload_message, Pre_message_Result, message_Result, config.commandOffset, message_Used)
    no_Semantic_Average_Pre, no_Semantic_Average_Rec, no_Semantic_F1_score, Semantic_Average_Pre, Semantic_Average_Rec, Semantic_F1_score = ChatPre_Semantic_Types_Evaluator(payload_message, Pre_message_Result, message_Result, config.commandOffset)
    no_Function_Average_Pre, no_Function_Average_Rec, no_Function_F1_score, Function_Average_Pre, Function_Average_Rec, Function_F1_score = ChatPre_Semantic_Functions_Evaluator(payload_message, Pre_message_Result, message_Result, config.commandOffset)

    logging.info(f"\n\n\n********* [Summary-{config.protocol_name}]: ChatPre Format Extraction *********")
    logging.info(f"Average_Accr:{Average_Accr}")
    # logging.info(f"Average_Pre:{Average_Pre}")
    # logging.info(f"Average_Rec:{Average_Rec}")
    logging.info(f"F1-score:{F1_score}")
    logging.info(f"Average_Perf:{Average_Perf}")
    logging.info(f"\n-----------------")

    logging.info(f"\n********* [Summary-{config.protocol_name}]: ChatPre(no refine) Semantic-Types Inference *********")
    logging.info(f"Average_Pre:{no_Semantic_Average_Pre}")
    logging.info(f"Average_Rec:{no_Semantic_Average_Rec}")
    logging.info(f"F1_score:{no_Semantic_F1_score}")


    logging.info(f"\n********* [Summary-{config.protocol_name}]: ChatPre#(refinement) Semantic-Types Inference *********")
    logging.info(f"Average_Pre:{Semantic_Average_Pre}")
    logging.info(f"Average_Rec:{Semantic_Average_Rec}")
    logging.info(f"F1_score:{Semantic_F1_score}")

    logging.info(f"\n-----------------")

    logging.info(f"\n********* [Summary-{config.protocol_name}]: ChatPre(no refine) Semantic-Functions Inference *********")
    logging.info(f"Average_Pre:{no_Function_Average_Pre}")
    logging.info(f"Average_Rec:{no_Function_Average_Rec}")
    logging.info(f"F1_score:{no_Function_F1_score}")

    logging.info(f"\n********* [Summary-{config.protocol_name}]: ChatPre#(refinement) Semantic-Functions Inference *********")
    logging.info(f"Average_Pre:{Function_Average_Pre}")
    logging.info(f"Average_Rec:{Function_Average_Rec}")
    logging.info(f"F1_score:{Function_F1_score}")

def ChatPreAnalysisLLM(index: int, payload_message:list):
    #settings
    baseline_mode = config.baseline_mode
    threadId = config.threadId
    ip = config.ip
    port = config.port
    chatpre_fields = eval(config.protocol_name + "_field_uesd_llm")
    chatpre_field_type = eval(config.protocol_name + "_field_type_llm")
    chatpre_field_func = eval(config.protocol_name + "_field_func_llm")
    message_Result = [None] * index
    message_Used = [None] * index
    Pre_message_Result = [None] * index

    #Analysis every msg sample
    for i in range(index):
        logging.info("\n\n+++++++++++++++++++++++ Msg {} +++++++++++++++++++++++".format(i))
        # new_directory = f"../PUT_test/{i}_tmp_results/"
        new_directory = f"PUT_test_{sys.argv[1]}/{i}_tmp_results/"
        with open(new_directory + "format.txt", 'r') as f:
            lines = f.readlines()
        matching_lines = [line for line in lines if re.match("^\[Message\].*", line)]
        recordNums = len(matching_lines)

        if baseline_mode == "oa" or baseline_mode == "ba" or baseline_mode == "all":

            # fields, field_Types, field_Functions, used_fields = Separator.AllAnalysis_A(recordNums, new_directory,payload_message[i])
            fields = chatpre_fields[i]
            used_fields = chatpre_fields[i]
            field_Functions = chatpre_field_func[i]
            # for item in fields:
            #     if item not in field_Functions:
            #         fields.remove1(item)
            for item in used_fields:
                if item not in field_Functions:
                    used_fields.remove(item)
            field_Types = chatpre_field_type[i]
            for item in field_Functions:
                if field_Functions[item][0].lower() == 'length':
                    field_Functions[item][0] = 'Length'
                    field_Types[item][0] = 'Bit Field'
                if field_Functions[item][0].lower() == 'checksum':
                    field_Functions[item][0] = 'CheckSum'
                    field_Types[item][0] = 'Bit Field'
                if 'file' in field_Functions[item][0].lower() :
                    field_Functions[item][0] = 'Filename'
                    field_Types[item][0] = 'String'
                if 'delim' in field_Functions[item][0].lower() :
                    field_Functions[item][0] = 'Delim'
                    field_Types[item][0] = 'Static'
                if 'command' in field_Functions[item][0].lower() :
                    field_Functions[item][0] = 'Command'
                    field_Types[item][0] = 'Group'
                if 'static text' in field_Functions[item][0].lower() :
                    field_Functions[item][0] = 'Static'
                    field_Types[item][0] = 'String'
                if 'version' in field_Functions[item][0].lower() :
                    field_Functions[item][0] = 'Static'
                    field_Types[item][0] = 'String'
            # fields = used_fields = ['2,3', '4', '5', '6', '8', '11,12', '13,14', '15,16', '17', '19,20', '21,22', '23,24']
            # field_Functions = {'2,3': ['Length'], '4': [], '5': [], '6': [], '8': [], '11,12': ['Aligned'], '13,14': ['Aligned'], '15,16': ['Aligned'], '17': ['Command'], '19,20': ['Aligned'], '21,22': ['Aligned'], '23,24': ['Length']}
            # field_Types = {'2,3': ['Group', 'Bit Field'], '4': ['Static'], '5': ['Static'], '6': ['Bit Field'], '8': ['Static'], '11,12': ['Static'], '13,14': ['Static'], '15,16': ['Static'], '17': ['Group'], '19,20': ['Static'], '21,22': ['Static'], '23,24': ['Bit Field']}
            message_Used[i] = used_fields

            boundaries = set()
            msg_len = len(payload_message[i])
            boundaries.add(-1)
            boundaries.add(msg_len-1)
            add_fields = []
            
            boundary_2 = -1
            for field in fields:
                boundary_1 = int(field.split(',')[0])-1
                boundaries.add(boundary_1)

                f_i = ','.join(str(i) for i in range(boundary_2+1, boundary_1+1))
                logging.info(f"add_field:{f_i}")
                if len(f_i)>0 :
                    add_fields.append(f_i)

                boundary_2 = int(field.split(',')[-1])
                boundaries.add(boundary_2)
            if boundary_2 < msg_len-1:
                f_i = ','.join(str(i) for i in range(boundary_2+1, msg_len))
                if len(f_i)>0 :
                    add_fields.append(f_i)
            
            for add_field in add_fields:
                if add_field not in fields:
                    fields.append(add_field)
                
            # logging.info(f"add_fields:{add_fields}")

            boundaries = sorted(list(boundaries))
#
            message_Result[i] = Message_Result(payload_message[i], fields, boundaries, field_Types,field_Functions)

            #print the ChatPRE's results on the Message i
            logging.info(f"payload_message: {message_Result[i].payload}")
            logging.info(f"fields: {message_Result[i].fields}")
            logging.info(f"boundaries: {message_Result[i].boundaries}")
            logging.info(f"field_Types: {message_Result[i].field_types}")
            logging.info(f"field_Functions: {message_Result[i].field_funcs}")

    '''Semantic Refinment: Clustering & Type & Funcs'''

    for i in range(index):
        Pre_message_Result[i] = copy.deepcopy(message_Result[i])
    logging.info(f"Pre_message_Result:{Pre_message_Result[0].field_types}")

    message_Result = Corrector.Validation(message_Result,payload_message)
    logging.info(f"message_Result:{message_Result[0].field_types}")
    logging.info(f"Pre_message_Result:{Pre_message_Result[0].field_types}")

    
    '''Evaluation & Results Printing -- chatpre - repartition'''
    
    Average_Accr, F1_score, Average_Perf = ChatPreLLMEvaluator(payload_message, Pre_message_Result, message_Result, config.commandOffset, message_Used)
    no_Semantic_Average_Pre, no_Semantic_Average_Rec, no_Semantic_F1_score, Semantic_Average_Pre, Semantic_Average_Rec, Semantic_F1_score = ChatPreLLM_Semantic_Types_Evaluator(payload_message, Pre_message_Result, message_Result, config.commandOffset)
    no_Function_Average_Pre, no_Function_Average_Rec, no_Function_F1_score, Function_Average_Pre, Function_Average_Rec, Function_F1_score = ChatPreLLM_Semantic_Functions_Evaluator(payload_message, Pre_message_Result, message_Result, config.commandOffset)

    logging.info(f"\n\n\n********* [Summary-{config.protocol_name}]: chatpre - repartition Format Extraction *********")
    logging.info(f"Average_Accr:{Average_Accr}")
    # logging.info(f"Average_Pre:{Average_Pre}")
    # logging.info(f"Average_Rec:{Average_Rec}")
    logging.info(f"F1-score:{F1_score}")
    logging.info(f"Average_Perf:{Average_Perf}")
    logging.info(f"\n-----------------")

    logging.info(f"\n********* [Summary-{config.protocol_name}]: chatpre - repartition(no refine) Semantic-Types Inference *********")
    logging.info(f"Average_Pre:{no_Semantic_Average_Pre}")
    logging.info(f"Average_Rec:{no_Semantic_Average_Rec}")
    logging.info(f"F1_score:{no_Semantic_F1_score}")


    logging.info(f"\n********* [Summary-{config.protocol_name}]: chatpre - repartition#(refinement) Semantic-Types Inference *********")
    logging.info(f"Average_Pre:{Semantic_Average_Pre}")
    logging.info(f"Average_Rec:{Semantic_Average_Rec}")
    logging.info(f"F1_score:{Semantic_F1_score}")

    logging.info(f"\n-----------------")

    logging.info(f"\n********* [Summary-{config.protocol_name}]: chatpre - repartition(no refine) Semantic-Functions Inference *********")
    logging.info(f"Average_Pre:{no_Function_Average_Pre}")
    logging.info(f"Average_Rec:{no_Function_Average_Rec}")
    logging.info(f"F1_score:{no_Function_F1_score}")

    logging.info(f"\n********* [Summary-{config.protocol_name}]: chatpre - repartition#(refinement) Semantic-Functions Inference *********")
    logging.info(f"Average_Pre:{Function_Average_Pre}")
    logging.info(f"Average_Rec:{Function_Average_Rec}")
    logging.info(f"F1_score:{Function_F1_score}")

def main():
    start_time = time.time()
    if config.evaluation_mode == "oa":
        with open(config.Evaluation_Res, 'w') as f:
            f.truncate()
    if config.evaluation_mode == "bo":
        with open(config.Evaluation_bo_Res, 'w') as f:
            f.truncate()

    index,payload_message = SendInputMsg()

    MonitorAnalysis(index,payload_message)
    ChatPreAnalysis(index,payload_message)
    ChatPreAnalysisLLM(index,payload_message)

    total_time = time.time()-start_time
    logging.info("\nTotal Analyze Time:{}".format(total_time))



main()