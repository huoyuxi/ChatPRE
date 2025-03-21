import sys
sys.path.append('pin-3.28-98749-g6643ecee5-gcc-linux/source/tools/BinPRE/Analyzer/config')
import config
import logging
import sys
log_format = '%(asctime)s - %(filename)s:%(lineno)d - %(message)s'
logging.basicConfig(filename=f'results/{sys.argv[1]}.log', level=logging.INFO, format=log_format, datefmt='%Y-%m-%d %H:%M:%S')
Semantic_Groundtruth = config.Semantic_Groundtruth
Semantic_Functions_Groundtruth = config.Semantic_Functions_Groundtruth

def metrix_Cal(msg_semanticTruth,msg_Res, msg_fields, msg_len):
    '''
    pre = correct_format_inferred_correct_semantic/correct_format_inferred_semantic
    rec = correct_format_inferred_correct_semantic/correct_format
    '''
    correct_format_inferred_semantic = 0
    correct_format_inferred_correct_semantic = 0

    for k,v in msg_Res.items():
        if k in msg_semanticTruth:
            correct_format_inferred_semantic += len(v)
            if msg_semanticTruth[k] in v:
                correct_format_inferred_correct_semantic += 1

    correct_format = 0
    for field in msg_fields:
        if field in msg_semanticTruth:
            correct_format += 1

    logging.info(f"correct_format_inferred_correct_semantic:{correct_format_inferred_correct_semantic}")
    logging.info(f"\ncorrect_format_inferred_semantic:{correct_format_inferred_semantic}")
    logging.info(f"correct_format:{correct_format}")
    if correct_format_inferred_correct_semantic == 0:
        semantic_rec = 0
        semantic_pre = 0
    else:
        semantic_pre = correct_format_inferred_correct_semantic/correct_format_inferred_semantic
        semantic_rec = correct_format_inferred_correct_semantic/correct_format


    return semantic_pre, semantic_rec

def metrix_Cal_Func(msg_semanticTruth, msg_Res, msg_fields, msg_len, msg_fieldTruth):
    '''
    pre = correct_format_inferred_correct_semantic/correct_format_inferred_semantic
    rec = correct_format_inferred_correct_semantic/correct_format
    '''
    correct_format_inferred_semantic = 0
    correct_format_inferred_correct_semantic = 0

    for k,v in msg_Res.items():
        if k in msg_fieldTruth:
            correct_format_inferred_semantic += len(v)

    for k,v in msg_Res.items():
        if k in msg_semanticTruth:
            if msg_semanticTruth[k] in v:
                correct_format_inferred_correct_semantic += 1

    correct_format = 0
    for field in msg_fields:
        if field in msg_semanticTruth:
            correct_format += 1

    logging.info(f"correct_format_inferred_correct_semantic:{correct_format_inferred_correct_semantic}")
    logging.info(f"\ncorrect_format_inferred_semantic:{correct_format_inferred_semantic}")
    logging.info(f"correct_format:{correct_format}")
    if correct_format_inferred_correct_semantic == 0:
        semantic_pre = 0
    else:
        semantic_pre = correct_format_inferred_correct_semantic/correct_format_inferred_semantic
    if correct_format == 0:
        semantic_rec = 0
    else:
        semantic_rec = correct_format_inferred_correct_semantic/correct_format


    return semantic_pre, semantic_rec


def Processing(Static_Res_i):
    msg_syntax = Static_Res_i.syntax
    msg_semantic = Static_Res_i.semantic

    msg_semanticRes = {}

    for i in range(0,len(msg_syntax)):
        msg_semanticRes[msg_syntax[i]] = msg_semantic[i]
    
    return msg_semanticRes

def BinPRE_Semantic_Types_Evaluator(payload_message, Pre_message_Result, message_Result, commandOffset):
    logging.info("\n\n\nSemantic-Types Evaluation Part For BinPRE(no validation)---------------------------------")
    
    '''Semantic-Type'''
    semantic_usedPre,msg_Pre, msg_Rec =0,0,0

    # msg_semanticTruth
    True_static_groudtruth = 0
    static_groudtruth = set()
    True_bytes_groudtruth = 0
    bytes_groudtruth = set()
    True_string_groudtruth = 0
    string_groudtruth = set()
    True_integer_groudtruth = 0
    integer_groudtruth = set()
    True_group_groudtruth = 0
    group_groudtruth = set()

    Inferred_True_static = 0
    Inferred_True_bytes = 0
    Inferred_True_string = 0
    Inferred_True_integer = 0
    Inferred_True_group = 0
    
    Inferred_static = 0
    Inferred_bytes = 0
    Inferred_string = 0
    Inferred_integer = 0
    Inferred_group = 0


    for i in range(0,len(payload_message)):
        msg_i = payload_message[i]
        msg_len = len(msg_i)
        command_start = int(commandOffset.split(',')[0])
        command_end = int(commandOffset.split(',')[-1])+1
        msg_command = payload_message[i][command_start:command_end]

        if config.evaluation_mode == 'index':
            msg_semanticTruth = Semantic_Groundtruth[i]
        else:
             msg_semanticTruth = Semantic_Groundtruth[msg_command]

        msg_semanticRes = Pre_message_Result[i].field_types


        logging.info(f"Msg {i} semantic evaluation:***\n")
        logging.info(f"msg_semanticTruth:{msg_semanticTruth}")
        logging.info(f"msg_semanticRes:{msg_semanticRes}\n")

        msg_pre, msg_rec= metrix_Cal(msg_semanticTruth,msg_semanticRes, Pre_message_Result[i].fields, msg_len)
        logging.info(f"msg_pre:{msg_pre}, msg_rec:{msg_rec}\n")
        
        msg_Pre += msg_pre
        msg_Rec += msg_rec
    
        for f,r in msg_semanticTruth.items():
            if (config.semantic_Types[0] in msg_semanticTruth[f]):
                True_static_groudtruth += 1
                static_groudtruth.add(f)

            if (config.semantic_Types[4] in msg_semanticTruth[f]):
                True_bytes_groudtruth += 1
                bytes_groudtruth.add(f)
            
            if (config.semantic_Types[2] in msg_semanticTruth[f]):
                True_string_groudtruth += 1
                string_groudtruth.add(f)
            
            if (config.semantic_Types[3] in msg_semanticTruth[f]):
                True_integer_groudtruth += 1
                integer_groudtruth.add(f)
            
            if (config.semantic_Types[1] in msg_semanticTruth[f]):
                True_group_groudtruth += 1
                group_groudtruth.add(f)

        for f,r in msg_semanticRes.items():

            if config.semantic_Types[0] in r:
                Inferred_static += 1
                if (f in msg_semanticTruth) and (config.semantic_Types[0] in msg_semanticTruth[f]):
                    Inferred_True_static += 1
            if config.semantic_Types[4] in r:
                Inferred_bytes += 1
                if (f in msg_semanticTruth) and (config.semantic_Types[4] in msg_semanticTruth[f]):
                    Inferred_True_bytes += 1
            
            if config.semantic_Types[2] in r:
                Inferred_string += 1
                if (f in msg_semanticTruth) and (config.semantic_Types[2] in msg_semanticTruth[f]):
                    Inferred_True_string += 1
            if config.semantic_Types[3] in r:
                Inferred_integer += 1
                if (f in msg_semanticTruth) and (config.semantic_Types[3] in msg_semanticTruth[f]):
                    Inferred_True_integer += 1
            if config.semantic_Types[1] in r:
                Inferred_group += 1
                if (f in msg_semanticTruth) and (config.semantic_Types[1] in msg_semanticTruth[f]):
                    Inferred_True_group += 1

    Average_Pre = msg_Pre/len(payload_message)
    Average_Rec = msg_Rec/len(payload_message)
    if (Average_Pre + Average_Rec) > 0:
        F1_score = (2 * Average_Pre * Average_Rec) / (Average_Pre + Average_Rec)
    else:
        F1_score = 0
    

    logging.info(f"Average_Pre:{Average_Pre}")
    logging.info(f"Average_Rec:{Average_Rec}")
    logging.info(f"F1_score:{F1_score}")

    if Inferred_static > 0:
        static_Pre = Inferred_True_static / Inferred_static
    else:
        static_Pre = 0
    if True_static_groudtruth >0:
        static_Rec = Inferred_True_static / True_static_groudtruth
    else:
        static_Rec = 0
    if (static_Pre + static_Rec) > 0:
        static_F1 = (2 * static_Pre * static_Rec) / (static_Pre + static_Rec)
    else:
        static_F1 = 0
    '''bytes'''
    if Inferred_bytes == 0:
        bytes_Pre = 0
    else:
        bytes_Pre = Inferred_True_bytes / Inferred_bytes
    
    if True_bytes_groudtruth == 0:
        bytes_Rec = 0
    else:
        bytes_Rec = Inferred_True_bytes / True_bytes_groudtruth
    
    if (bytes_Pre + bytes_Rec) > 0:
        bytes_F1 = (2 * bytes_Pre * bytes_Rec) / (bytes_Pre + bytes_Rec)
    else:
        bytes_F1 = 0
    '''string'''
    if Inferred_string == 0:
        string_Pre = 0
    else:
        string_Pre = Inferred_True_string / Inferred_string
    
    if True_string_groudtruth == 0:
        string_Rec = 0
    else:
        string_Rec = Inferred_True_string / True_string_groudtruth
    
    if (string_Pre + string_Rec) > 0:
        string_F1 = (2 * string_Pre * string_Rec) / (string_Pre + string_Rec)
    else:
        string_F1 = 0
    '''integer'''
    if Inferred_integer == 0:
        integer_Pre = 0
    else:
        integer_Pre = Inferred_True_integer / Inferred_integer
    
    if True_integer_groudtruth == 0:
        integer_Rec = 0
    else:
        integer_Rec = Inferred_True_integer / True_integer_groudtruth
    
    if (integer_Pre + integer_Rec) > 0:
        integer_F1 = (2 * integer_Pre * integer_Rec) / (integer_Pre + integer_Rec)
    else:
        integer_F1 = 0

    '''group'''
    if Inferred_group == 0:
        group_Pre = 0
    else:
        group_Pre = Inferred_True_group / Inferred_group
    
    if True_group_groudtruth == 0:
        group_Rec = 0
    else:
        group_Rec = Inferred_True_group / True_group_groudtruth
    
    if (group_Pre + group_Rec) > 0:
        group_F1 = (2 * group_Pre * group_Rec) / (group_Pre + group_Rec)
    else:
        group_F1 = 0

    no_Average_Pre = Average_Pre
    no_Average_Rec = Average_Rec
    no_F1_score = F1_score

    # with open(config.Evaluation_Res, "a") as file:
    logging.info("\n\n\Semantic-Type Evaluation Part For BinPRE(no validation)---------------------------------\n")
    logging.info(f"no_Average_Pre:{Average_Pre}\n")
    logging.info(f"no_Average_Rec:{Average_Rec}\n")
    logging.info(f"no_F1_score:{F1_score}\n")

    logging.info(f"\nno_static_Pre:{static_Pre}\n")
    logging.info(f"no_static_Rec:{static_Rec}\n")
    logging.info(f"no_static_F1:{static_F1}\n")
    logging.info(f"no_static_groudtruth:{static_groudtruth}\n")

    logging.info(f"\nno_integer_Pre:{integer_Pre}\n")
    logging.info(f"no_integer_Rec:{integer_Rec}\n")
    logging.info(f"no_integer_F1:{integer_F1}\n")
    logging.info(f"no_integer_groudtruth:{integer_groudtruth}\n") 

    logging.info(f"\nno_group_Pre:{group_Pre}\n")
    logging.info(f"no_group_Rec:{group_Rec}\n")
    logging.info(f"no_group_F1:{group_F1}\n")
    logging.info(f"no_group_groudtruth:{group_groudtruth}\n") 

    logging.info(f"\nno_bytes_Pre:{bytes_Pre}\n")
    logging.info(f"no_bytes_Rec:{bytes_Rec}\n")
    logging.info(f"no_bytes_F1:{bytes_F1}\n")
    logging.info(f"no_bytes_groudtruth:{bytes_groudtruth}\n") 

    logging.info(f"\nno_string_Pre:{string_Pre}\n")
    logging.info(f"no_string_Rec:{string_Rec}\n")
    logging.info(f"no_string_F1:{string_F1}\n")
    logging.info(f"no_string_groudtruth:{string_groudtruth}\n") 


         

    logging.info("\n\n\nSemantic-Types Evaluation Part For BinPRE(Validated)---------------------------------")
    

    '''Semantic-Type'''
    semantic_usedPre,msg_Pre, msg_Rec =0,0,0

    # msg_semanticTruth
    True_static_groudtruth = 0
    static_groudtruth = set()
    True_bytes_groudtruth = 0
    bytes_groudtruth = set()
    True_string_groudtruth = 0
    string_groudtruth = set()
    True_integer_groudtruth = 0
    integer_groudtruth = set()
    True_group_groudtruth = 0
    group_groudtruth = set()

    Inferred_True_static = 0
    Inferred_True_bytes = 0
    Inferred_True_string = 0
    Inferred_True_integer = 0
    Inferred_True_group = 0
    
    Inferred_static = 0
    Inferred_bytes = 0
    Inferred_string = 0
    Inferred_integer = 0
    Inferred_group = 0

    for i in range(0,len(payload_message)):
        msg_i = payload_message[i]
        msg_len = len(msg_i)
        command_start = int(commandOffset.split(',')[0])
        command_end = int(commandOffset.split(',')[-1])+1
        msg_command = payload_message[i][command_start:command_end]

        if config.evaluation_mode == 'index':
            msg_semanticTruth = Semantic_Groundtruth[i]
        else:
            msg_semanticTruth = Semantic_Groundtruth[msg_command]


        msg_semanticRes = message_Result[i].field_types


        logging.info(f"Msg {i} semantic evaluation:***\n")
        logging.info(f"msg_semanticTruth:{msg_semanticTruth}")
        logging.info(f"msg_semanticRes:{msg_semanticRes}\n")

        msg_pre, msg_rec= metrix_Cal(msg_semanticTruth,msg_semanticRes, message_Result[i].fields, msg_len)
        logging.info(f"msg_pre:{msg_pre}, msg_rec:{msg_rec}\n")
        
        msg_Pre += msg_pre
        msg_Rec += msg_rec



        for f,r in msg_semanticTruth.items():
            if (config.semantic_Types[0] in msg_semanticTruth[f]):
                True_static_groudtruth += 1
                static_groudtruth.add(f)

            if (config.semantic_Types[4] in msg_semanticTruth[f]):
                True_bytes_groudtruth += 1
                bytes_groudtruth.add(f)
            
            if (config.semantic_Types[2] in msg_semanticTruth[f]):
                True_string_groudtruth += 1
                string_groudtruth.add(f)
            
            if (config.semantic_Types[3] in msg_semanticTruth[f]):
                True_integer_groudtruth += 1
                integer_groudtruth.add(f)
            
            if (config.semantic_Types[1] in msg_semanticTruth[f]):
                True_group_groudtruth += 1
                group_groudtruth.add(f)

        for f,r in msg_semanticRes.items():

            if config.semantic_Types[0] in r:
                Inferred_static += 1
                if (f in msg_semanticTruth) and (config.semantic_Types[0] in msg_semanticTruth[f]):
                    Inferred_True_static += 1
            if config.semantic_Types[4] in r:
                Inferred_bytes += 1
                if (f in msg_semanticTruth) and (config.semantic_Types[4] in msg_semanticTruth[f]):
                    Inferred_True_bytes += 1
            
            if config.semantic_Types[2] in r:
                Inferred_string += 1
                if (f in msg_semanticTruth) and (config.semantic_Types[2] in msg_semanticTruth[f]):
                    Inferred_True_string += 1
            if config.semantic_Types[3] in r:
                Inferred_integer += 1
                if (f in msg_semanticTruth) and (config.semantic_Types[3] in msg_semanticTruth[f]):
                    Inferred_True_integer += 1
            if config.semantic_Types[1] in r:
                Inferred_group += 1
                if (f in msg_semanticTruth) and (config.semantic_Types[1] in msg_semanticTruth[f]):
                    Inferred_True_group += 1
        

    Average_Pre = msg_Pre/len(payload_message)
    Average_Rec = msg_Rec/len(payload_message)
    if (Average_Pre + Average_Rec) > 0:
        F1_score = (2 * Average_Pre * Average_Rec) / (Average_Pre + Average_Rec)
    else:
        F1_score = 0
    if Inferred_static >0:
        static_Pre = Inferred_True_static / Inferred_static
    else:
        static_Pre = 0
    
    if (static_Pre + static_Rec) > 0:
        static_F1 = (2 * static_Pre * static_Rec) / (static_Pre + static_Rec)
    else:
        static_F1 = 0
    '''bytes'''
    if Inferred_bytes == 0:
        bytes_Pre = 0
    else:
        bytes_Pre = Inferred_True_bytes / Inferred_bytes
    
    if True_bytes_groudtruth == 0:
        bytes_Rec = 0
    else:
        bytes_Rec = Inferred_True_bytes / True_bytes_groudtruth
    
    if (bytes_Pre + bytes_Rec) > 0:
        bytes_F1 = (2 * bytes_Pre * bytes_Rec) / (bytes_Pre + bytes_Rec)
    else:
        bytes_F1 = 0
    '''string'''
    if Inferred_string == 0:
        string_Pre = 0
    else:
        string_Pre = Inferred_True_string / Inferred_string
    
    if True_string_groudtruth == 0:
        string_Rec = 0
    else:
        string_Rec = Inferred_True_string / True_string_groudtruth
    
    if (string_Pre + string_Rec) > 0:
        string_F1 = (2 * string_Pre * string_Rec) / (string_Pre + string_Rec)
    else:
        string_F1 = 0
    '''integer'''
    if Inferred_integer == 0:
        integer_Pre = 0
    else:
        integer_Pre = Inferred_True_integer / Inferred_integer
    
    if True_integer_groudtruth == 0:
        integer_Rec = 0
    else:
        integer_Rec = Inferred_True_integer / True_integer_groudtruth
    
    if (integer_Pre + integer_Rec) > 0:
        integer_F1 = (2 * integer_Pre * integer_Rec) / (integer_Pre + integer_Rec)
    else:
        integer_F1 = 0

    '''group'''
    if Inferred_group == 0:
        group_Pre = 0
    else:
        group_Pre = Inferred_True_group / Inferred_group
    
    if True_group_groudtruth == 0:
        group_Rec = 0
    else:
        group_Rec = Inferred_True_group / True_group_groudtruth
    
    if (group_Pre + group_Rec) > 0:
        group_F1 = (2 * group_Pre * group_Rec) / (group_Pre + group_Rec)
    else:
        group_F1 = 0

    logging.info(f"Average_Pre:{Average_Pre}")
    logging.info(f"Average_Rec:{Average_Rec}")
    logging.info(f"F1_score:{F1_score}")
    

    


    # with open(config.Evaluation_Res, "a") as file:
    logging.info("\n\n\Semantic-Type Evaluation Part For BinPRE(Validated)---------------------------------\n")
    logging.info(f"Average_Pre:{Average_Pre}\n")
    logging.info(f"Average_Rec:{Average_Rec}\n")
    logging.info(f"F1_score:{F1_score}\n")

    logging.info(f"\nstatic_Pre:{static_Pre}\n")
    logging.info(f"static_Rec:{static_Rec}\n")
    logging.info(f"static_F1:{static_F1}\n")
    logging.info(f"static_groudtruth:{static_groudtruth}\n")

    logging.info(f"\ninteger_Pre:{integer_Pre}\n")
    logging.info(f"integer_Rec:{integer_Rec}\n")
    logging.info(f"integer_F1:{integer_F1}\n")
    logging.info(f"integer_groudtruth:{integer_groudtruth}\n") 

    logging.info(f"\ngroup_Pre:{group_Pre}\n")
    logging.info(f"group_Rec:{group_Rec}\n")
    logging.info(f"group_F1:{group_F1}\n")
    logging.info(f"group_groudtruth:{group_groudtruth}\n")    

    logging.info(f"\nbytes_Pre:{bytes_Pre}\n")
    logging.info(f"bytes_Rec:{bytes_Rec}\n")
    logging.info(f"bytes_F1:{bytes_F1}\n")
    logging.info(f"bytes_groudtruth:{bytes_groudtruth}\n") 

    logging.info(f"\nstring_Pre:{string_Pre}\n")
    logging.info(f"string_Rec:{string_Rec}\n")
    logging.info(f"string_F1:{string_F1}\n")
    logging.info(f"string_groudtruth:{string_groudtruth}\n") 
    
    return no_Average_Pre, no_Average_Rec, no_F1_score, Average_Pre, Average_Rec, F1_score

            

def BinPRE_Semantic_Functions_Evaluator(payload_message, Pre_message_Result, message_Result, commandOffset):
    logging.info("\n\n\nSemantic-Functions Evaluation Part For BinPRE(no validation)---------------------------------")
    
    '''Semantic-Function'''
    semantic_usedPre,msg_Pre, msg_Rec =0,0,0

    no_BinPRE_command_count = 0
    no_BinPRE_command_correct = 0

    BinPRE_length_correct = 0
    BinPRE_command_correct = 0
    BinPRE_length_count = 0
    BinPRE_command_count = 0

    True_delim_groudtruth = 0
    Inferred_delim = 0
    Inferred_True_delim = 0
    delim_groudtruth = set()

    True_aligned_groudtruth = 0
    Inferred_aligned = 0
    Inferred_True_aligned = 0
    aligned_groudtruth = set()

    True_filename_groudtruth = 0
    Inferred_filename = 0
    Inferred_True_filename = 0
    filename_groudtruth = set()

    for i in range(0,len(payload_message)):
        msg_i = payload_message[i]
        msg_len = len(msg_i)
        command_start = int(commandOffset.split(',')[0])
        command_end = int(commandOffset.split(',')[-1])+1
        msg_command = payload_message[i][command_start:command_end]

        if config.evaluation_mode == 'index':
            msg_semanticTruth = Semantic_Functions_Groundtruth[i]
            msg_fieldTruth = Semantic_Groundtruth[i]
        else:
            msg_semanticTruth = Semantic_Functions_Groundtruth[msg_command]
            msg_fieldTruth = Semantic_Groundtruth[msg_command]

        msg_semanticRes = Pre_message_Result[i].field_funcs

        for f,r in msg_semanticRes.items():
            if config.semantic_Functions[0] in r:
                no_BinPRE_command_count += 1
                if f == config.commandOffset:
                    no_BinPRE_command_correct += 1


        logging.info(f"Msg {i} semantic evaluation:***\n")
        logging.info(f"msg_semanticTruth:{msg_semanticTruth}")
        logging.info(f"msg_semanticRes:{msg_semanticRes}\n")

        msg_pre, msg_rec= metrix_Cal_Func(msg_semanticTruth,msg_semanticRes, Pre_message_Result[i].fields, msg_len, msg_fieldTruth)
        logging.info(f"msg_pre:{msg_pre}, msg_rec:{msg_rec}\n")
        
        msg_Pre += msg_pre
        msg_Rec += msg_rec
        for f,r in msg_semanticRes.items():
            logging.info(f"f:{f}, r:{r}")
            if config.semantic_Functions[0] in r:
                BinPRE_command_count += 1
                if f == config.commandOffset:
                    BinPRE_command_correct += 1
            if config.semantic_Functions[1] in r:
                BinPRE_length_count += 1
                if f == config.lengthOffset:
                    BinPRE_length_correct += 1
        
        
        
        for f,r in msg_semanticTruth.items():
            if (config.semantic_Functions[2] in msg_semanticTruth[f]):
                True_delim_groudtruth += 1
                delim_groudtruth.add(f)
            if (config.semantic_Functions[4] in msg_semanticTruth[f]):
                True_aligned_groudtruth += 1
                aligned_groudtruth.add(f)
            if (config.semantic_Functions[5] in msg_semanticTruth[f]):
                True_filename_groudtruth += 1
                filename_groudtruth.add(f)


        for f,r in msg_semanticRes.items():

            if config.semantic_Functions[2] in r:
                Inferred_delim += 1
                if (f in msg_semanticTruth) and (config.semantic_Functions[2] in msg_semanticTruth[f]):
                    Inferred_True_delim += 1
            
            if config.semantic_Functions[4] in r:
                Inferred_aligned += 1
                if (f in msg_semanticTruth) and (config.semantic_Functions[4] in msg_semanticTruth[f]):
                    Inferred_True_aligned += 1
            
            if config.semantic_Functions[5] in r:
                Inferred_filename += 1
                if (f in msg_semanticTruth) and (config.semantic_Functions[5] in msg_semanticTruth[f]):
                    Inferred_True_filename += 1

    Average_Pre = msg_Pre/len(payload_message)
    Average_Rec = msg_Rec/len(payload_message)
    if (Average_Pre + Average_Rec) > 0:
        F1_score = (2 * Average_Pre * Average_Rec) / (Average_Pre + Average_Rec)
    else:
        F1_score = 0
    

    logging.info(f"Average_Pre:{Average_Pre}")
    logging.info(f"Average_Rec:{Average_Rec}")
    logging.info(f"F1_score:{F1_score}")

    no_BinPRE_Command_rec = no_BinPRE_command_correct/len(payload_message)
    if no_BinPRE_command_count>0:
        no_BinPRE_Command_pre = no_BinPRE_command_correct / no_BinPRE_command_count
        if (no_BinPRE_Command_pre + no_BinPRE_Command_rec) > 0:
            no_BinPRE_Command_F1 = (2 * no_BinPRE_Command_pre * no_BinPRE_Command_rec) / (no_BinPRE_Command_pre + no_BinPRE_Command_rec)
        else:
            no_BinPRE_Command_F1 = 0
    else:
        no_BinPRE_Command_pre = 0
        no_BinPRE_Command_F1 = 0
    
    BinPRE_Command_rec = BinPRE_command_correct/len(payload_message)
    BinPRE_Length_rec = BinPRE_length_correct/len(payload_message)
    if BinPRE_command_count>0:
        BinPRE_Command_pre = BinPRE_command_correct/BinPRE_command_count
        if (BinPRE_Command_pre + BinPRE_Command_rec) > 0:
            BinPRE_Command_F1 = (2 * BinPRE_Command_pre * BinPRE_Command_rec) / (BinPRE_Command_pre + BinPRE_Command_rec) 
        else:
            BinPRE_Command_F1 = 0
    else:
        BinPRE_Command_pre = 0
        BinPRE_Command_F1 = 0
    if BinPRE_length_count>0:
        BinPRE_Length_pre = BinPRE_length_correct / BinPRE_length_count
        if (BinPRE_Length_pre + BinPRE_Length_rec) > 0:
            BinPRE_Length_F1 = (2 * BinPRE_Length_pre * BinPRE_Length_rec) / (BinPRE_Length_pre + BinPRE_Length_rec)
        else:
            BinPRE_Length_F1 = 0
    else:
        BinPRE_Length_pre = 0
        BinPRE_Length_F1 = 0
    if True_delim_groudtruth > 0:
        BinPRE_Delim_rec = Inferred_True_delim/True_delim_groudtruth
    else:
        BinPRE_Delim_rec = 0
    
    if Inferred_delim > 0:
        BinPRE_Delim_pre = Inferred_True_delim/Inferred_delim
    else:
        BinPRE_Delim_pre = 0
    
    if (BinPRE_Delim_rec + BinPRE_Delim_pre) > 0:
        BinPRE_Delim_F1 = (2 * BinPRE_Delim_rec * BinPRE_Delim_pre) / (BinPRE_Delim_rec + BinPRE_Delim_pre)
    else:
        BinPRE_Delim_F1 = 0
    if True_aligned_groudtruth > 0:
        BinPRE_aligned_rec = Inferred_True_aligned/True_aligned_groudtruth
    else:
        BinPRE_aligned_rec = 0
    
    if Inferred_aligned > 0:
        BinPRE_aligned_pre = Inferred_True_aligned/Inferred_aligned
    else:
        BinPRE_aligned_pre = 0
    
    if (BinPRE_aligned_rec + BinPRE_aligned_pre) > 0:
        BinPRE_aligned_F1 = (2 * BinPRE_aligned_rec * BinPRE_aligned_pre) / (BinPRE_aligned_rec + BinPRE_aligned_pre)
    else:
        BinPRE_aligned_F1 = 0
    if True_filename_groudtruth > 0:
        BinPRE_filename_rec = Inferred_True_filename/True_filename_groudtruth
    else:
        BinPRE_filename_rec = 0
    
    if Inferred_filename > 0:
        BinPRE_filename_pre = Inferred_True_filename/Inferred_filename
    else:
        BinPRE_filename_pre = 0
    
    if (BinPRE_filename_rec + BinPRE_filename_pre) > 0:
        BinPRE_filename_F1 = (2 * BinPRE_filename_rec * BinPRE_filename_pre) / (BinPRE_filename_rec + BinPRE_filename_pre)
    else:
        BinPRE_filename_F1 = 0

    no_Average_Pre = Average_Pre
    no_Average_Rec = Average_Rec
    no_F1_score = F1_score

    # with open(config.Evaluation_Res, "a") as file:
    logging.info("\n\n\Semantic-Function Evaluation Part For BinPRE(no validation)---------------------------------\n")
    logging.info(f"Average_Pre:{Average_Pre}\n")
    logging.info(f"Average_Rec:{Average_Rec}\n")
    logging.info(f"F1_score:{F1_score}\n\n")
    logging.info(f"no_BinPRE_Command_pre:{no_BinPRE_Command_pre}\n")
    logging.info(f"no_BinPRE_Command_rec:{no_BinPRE_Command_rec}\n")
    logging.info(f"no_BinPRE_Command_F1:{no_BinPRE_Command_F1}\n\n")
    logging.info(f"\n")
    logging.info(f"no_BinPRE_Command_pre:{BinPRE_Command_pre}\n")
    logging.info(f"no_BinPRE_Command_rec:{BinPRE_Command_rec}\n")
    logging.info(f"no_BinPRE_Command_F1:{BinPRE_Command_F1}\n")
    logging.info(f"\nno_BinPRE_Length_pre:{BinPRE_Length_pre}\n")
    logging.info(f"no_BinPRE_Length_rec:{BinPRE_Length_rec}\n")
    logging.info(f"no_BinPRE_Length_F1:{BinPRE_Length_F1}\n")
    logging.info(f"\nno_BinPRE_Delim_pre:{BinPRE_Delim_pre}\n")
    logging.info(f"no_BinPRE_Delim_rec:{BinPRE_Delim_rec}\n")
    logging.info(f"no_BinPRE_Delim_F1:{BinPRE_Delim_F1}\n")
    logging.info(f"no_delim_groudtruth:{delim_groudtruth}\n")
    logging.info(f"\nno_BinPRE_aligned_pre:{BinPRE_aligned_pre}\n")
    logging.info(f"no_BinPRE_aligned_rec:{BinPRE_aligned_rec}\n")
    logging.info(f"no_BinPRE_aligned_F1:{BinPRE_aligned_F1}\n")
    logging.info(f"no_aligned_groudtruth:{aligned_groudtruth}\n")
    logging.info(f"\nno_BinPRE_filename_pre:{BinPRE_filename_pre}\n")
    logging.info(f"no_BinPRE_filename_rec:{BinPRE_filename_rec}\n")
    logging.info(f"no_BinPRE_filename_F1:{BinPRE_filename_F1}\n")
    logging.info(f"no_filename_groudtruth:{filename_groudtruth}\n")

    logging.info("\n\n\nSemantic-Functions Evaluation Part For BinPRE(Validated)---------------------------------")
    

    '''Semantic-Function'''
    semantic_usedPre,msg_Pre, msg_Rec =0,0,0

    BinPRE_length_correct = 0
    BinPRE_command_correct = 0
    BinPRE_length_count = 0
    BinPRE_command_count = 0

    True_delim_groudtruth = 0
    Inferred_delim = 0
    Inferred_True_delim = 0
    delim_groudtruth = set()

    True_aligned_groudtruth = 0
    Inferred_aligned = 0
    Inferred_True_aligned = 0
    aligned_groudtruth = set()

    True_filename_groudtruth = 0
    Inferred_filename = 0
    Inferred_True_filename = 0
    filename_groudtruth = set()

    for i in range(0,len(payload_message)):
        msg_i = payload_message[i]
        msg_len = len(msg_i)
        command_start = int(commandOffset.split(',')[0])
        command_end = int(commandOffset.split(',')[-1])+1
        msg_command = payload_message[i][command_start:command_end]

        if config.evaluation_mode == 'index':
            msg_semanticTruth = Semantic_Functions_Groundtruth[i]
            msg_fieldTruth = Semantic_Groundtruth[i]
        else:
            msg_semanticTruth = Semantic_Functions_Groundtruth[msg_command]
            msg_fieldTruth = Semantic_Groundtruth[msg_command]

        msg_semanticRes = message_Result[i].field_funcs

        for f,r in msg_semanticRes.items():
            if config.semantic_Functions[0] in r:
                BinPRE_command_count += 1
                if f == config.commandOffset:
                    BinPRE_command_correct += 1
            if config.semantic_Functions[1] in r:
                BinPRE_length_count += 1
                if f == config.lengthOffset:
                    BinPRE_length_correct += 1
        
        for f,r in msg_semanticTruth.items():
            if (config.semantic_Functions[2] in msg_semanticTruth[f]):
                True_delim_groudtruth += 1
                delim_groudtruth.add(f)
            if (config.semantic_Functions[4] in msg_semanticTruth[f]):
                True_aligned_groudtruth += 1
                aligned_groudtruth.add(f)
            if (config.semantic_Functions[5] in msg_semanticTruth[f]):
                True_filename_groudtruth += 1
                filename_groudtruth.add(f)


        for f,r in msg_semanticRes.items():

            if config.semantic_Functions[2] in r:
                Inferred_delim += 1
                if (f in msg_semanticTruth) and (config.semantic_Functions[2] in msg_semanticTruth[f]):
                    Inferred_True_delim += 1
            
            if config.semantic_Functions[4] in r:
                Inferred_aligned += 1
                if (f in msg_semanticTruth) and (config.semantic_Functions[4] in msg_semanticTruth[f]):
                    Inferred_True_aligned += 1
            
            if config.semantic_Functions[5] in r:
                Inferred_filename += 1
                if (f in msg_semanticTruth) and (config.semantic_Functions[5] in msg_semanticTruth[f]):
                    Inferred_True_filename += 1
            

        logging.info(f"Msg {i} semantic evaluation:***\n")
        logging.info(f"msg_semanticTruth:{msg_semanticTruth}")
        logging.info(f"msg_semanticRes:{msg_semanticRes}\n")

        msg_pre, msg_rec= metrix_Cal_Func(msg_semanticTruth,msg_semanticRes, message_Result[i].fields, msg_len, msg_fieldTruth)
        logging.info(f"msg_pre:{msg_pre}, msg_rec:{msg_rec}\n")
        
        msg_Pre += msg_pre
        msg_Rec += msg_rec
        

    Average_Pre = msg_Pre/len(payload_message)
    Average_Rec = msg_Rec/len(payload_message)
    if (Average_Pre + Average_Rec) > 0:
        F1_score = (2 * Average_Pre * Average_Rec) / (Average_Pre + Average_Rec)
    else:
        F1_score = 0
    

    logging.info(f"Average_Pre:{Average_Pre}")
    logging.info(f"Average_Rec:{Average_Rec}")
    logging.info(f"F1_score:{F1_score}")
    
    BinPRE_Command_rec = BinPRE_command_correct/len(payload_message)
    BinPRE_Length_rec = BinPRE_length_correct/len(payload_message)
    if BinPRE_command_count>0:
        BinPRE_Command_pre = BinPRE_command_correct/BinPRE_command_count
        if (BinPRE_Command_pre + BinPRE_Command_rec) > 0:
            BinPRE_Command_F1 = (2 * BinPRE_Command_pre * BinPRE_Command_rec) / (BinPRE_Command_pre + BinPRE_Command_rec) 
        else:
            BinPRE_Command_F1 = 0
    else:
        BinPRE_Command_pre = 0
        BinPRE_Command_F1 = 0
    if BinPRE_length_count>0:
        BinPRE_Length_pre = BinPRE_length_correct / BinPRE_length_count
        if (BinPRE_Length_pre + BinPRE_Length_rec) > 0:
            BinPRE_Length_F1 = (2 * BinPRE_Length_pre * BinPRE_Length_rec) / (BinPRE_Length_pre + BinPRE_Length_rec)
        else:
            BinPRE_Length_F1 = 0
    else:
        BinPRE_Length_pre = 0
        BinPRE_Length_F1 = 0
    if True_delim_groudtruth > 0:
        BinPRE_Delim_rec = Inferred_True_delim/True_delim_groudtruth
    else:
        BinPRE_Delim_rec = 0
    
    if Inferred_delim > 0:
        BinPRE_Delim_pre = Inferred_True_delim/Inferred_delim
    else:
        BinPRE_Delim_pre = 0
    
    if (BinPRE_Delim_rec + BinPRE_Delim_pre) > 0:
        BinPRE_Delim_F1 = (2 * BinPRE_Delim_rec * BinPRE_Delim_pre) / (BinPRE_Delim_rec + BinPRE_Delim_pre)
    else:
        BinPRE_Delim_F1 = 0
    if True_aligned_groudtruth > 0:
        BinPRE_aligned_rec = Inferred_True_aligned/True_aligned_groudtruth
    else:
        BinPRE_aligned_rec = 0
    
    if Inferred_aligned > 0:
        BinPRE_aligned_pre = Inferred_True_aligned/Inferred_aligned
    else:
        BinPRE_aligned_pre = 0
    
    if (BinPRE_aligned_rec + BinPRE_aligned_pre) > 0:
        BinPRE_aligned_F1 = (2 * BinPRE_aligned_rec * BinPRE_aligned_pre) / (BinPRE_aligned_rec + BinPRE_aligned_pre)
    else:
        BinPRE_aligned_F1 = 0
    if True_filename_groudtruth > 0:
        BinPRE_filename_rec = Inferred_True_filename/True_filename_groudtruth
    else:
        BinPRE_filename_rec = 0
    
    if Inferred_filename > 0:
        BinPRE_filename_pre = Inferred_True_filename/Inferred_filename
    else:
        BinPRE_filename_pre = 0
    
    if (BinPRE_filename_rec + BinPRE_filename_pre) > 0:
        BinPRE_filename_F1 = (2 * BinPRE_filename_rec * BinPRE_filename_pre) / (BinPRE_filename_rec + BinPRE_filename_pre)
    else:
        BinPRE_filename_F1 = 0

    logging.info(f"BinPRE_Command_pre:{BinPRE_Command_pre}")
    logging.info(f"BinPRE_Command_rec:{BinPRE_Command_rec}")
    logging.info(f"BinPRE_Length_pre:{BinPRE_Length_pre}")
    logging.info(f"BinPRE_Length_rec:{BinPRE_Length_rec}")

    # with open(config.Evaluation_Res, "a") as file:
    logging.info("\n\n\Semantic-Function Evaluation Part For BinPRE(Validated)---------------------------------\n")
    logging.info(f"Average_Pre:{Average_Pre}\n")
    logging.info(f"Average_Rec:{Average_Rec}\n")
    logging.info(f"F1_score:{F1_score}\n")
    logging.info(f"\n")
    logging.info(f"BinPRE_Command_pre:{BinPRE_Command_pre}\n")
    logging.info(f"BinPRE_Command_rec:{BinPRE_Command_rec}\n")
    logging.info(f"BinPRE_Command_F1:{BinPRE_Command_F1}\n")
    logging.info(f"\nBinPRE_Length_pre:{BinPRE_Length_pre}\n")
    logging.info(f"BinPRE_Length_rec:{BinPRE_Length_rec}\n")
    logging.info(f"BinPRE_Length_F1:{BinPRE_Length_F1}\n")
    logging.info(f"\nBinPRE_Delim_pre:{BinPRE_Delim_pre}\n")
    logging.info(f"BinPRE_Delim_rec:{BinPRE_Delim_rec}\n")
    logging.info(f"BinPRE_Delim_F1:{BinPRE_Delim_F1}\n")
    logging.info(f"delim_groudtruth:{delim_groudtruth}\n")
    logging.info(f"\nBinPRE_aligned_pre:{BinPRE_aligned_pre}\n")
    logging.info(f"BinPRE_aligned_rec:{BinPRE_aligned_rec}\n")
    logging.info(f"BinPRE_aligned_F1:{BinPRE_aligned_F1}\n")
    logging.info(f"aligned_groudtruth:{aligned_groudtruth}\n")
    logging.info(f"\nBinPRE_filename_pre:{BinPRE_filename_pre}\n")
    logging.info(f"BinPRE_filename_rec:{BinPRE_filename_rec}\n")
    logging.info(f"BinPRE_filename_F1:{BinPRE_filename_F1}\n")
    logging.info(f"filename_groudtruth:{filename_groudtruth}\n")

    return no_Average_Pre, no_Average_Rec, no_F1_score, Average_Pre, Average_Rec, F1_score

def Polyglot_SemanticEvaluator(payload_message, Polyglot_length_Res, Polyglot_command_Res, Polyglot_separator_Res, commandOffset):
    polyglot_length_correct = 0
    polyglot_command_correct = 0
    polyglot_length_count = 0
    polyglot_command_count = 0

    True_delim_groudtruth = 0
    Inferred_delim = 0
    Inferred_True_delim = 0
    delim_groudtruth = set()

    logging.info("\n\n\nSemantic Evaluation Part For Polyglot---------------------------------")
    for i in range(0,len(payload_message)):
        polyglot_length_count += len(Polyglot_length_Res[i])
        if Polyglot_command_Res[i] is not None and len(Polyglot_command_Res[i])>0:
            polyglot_command_count += len(Polyglot_command_Res[i])
        else:
            polyglot_command_count = 0
        if Polyglot_separator_Res[i] is not None and len(Polyglot_separator_Res[i])>0:
            Inferred_delim += len(Polyglot_separator_Res[i])

        command_start = int(commandOffset.split(',')[0])
        command_end = int(commandOffset.split(',')[-1])+1
        msg_command = payload_message[i][command_start:command_end]

        if config.evaluation_mode == 'index':
            msg_semanticTruth = Semantic_Functions_Groundtruth[i]
        else:
            msg_semanticTruth = Semantic_Functions_Groundtruth[msg_command]
        

        if config.lengthOffset in Polyglot_length_Res[i]:
            polyglot_length_correct += 1
        if commandOffset in Polyglot_command_Res[i]:
            polyglot_command_correct += 1

        for k, v in msg_semanticTruth.items():
            v = [v]
            
            if config.semantic_Functions[2] in v:
                True_delim_groudtruth += 1
                delim_groudtruth.add(k)
                if k in Polyglot_separator_Res[i]:
                    Inferred_True_delim += 1
                    

        
    Polyglot_Command_rec = polyglot_command_correct/len(payload_message)
    Polyglot_Length_rec = polyglot_length_correct/len(payload_message)
    if polyglot_command_count > 0 :
        Polyglot_Command_pre = polyglot_command_correct/polyglot_command_count
        if (Polyglot_Command_pre + Polyglot_Command_rec) > 0 : 
            Polyglot_Command_F1 = (2 * Polyglot_Command_pre * Polyglot_Command_rec) / (Polyglot_Command_pre + Polyglot_Command_rec)
        else:
            Polyglot_Command_F1 = 0
    else:
        Polyglot_Command_pre = 0
        Polyglot_Command_F1 = 0

    if polyglot_length_count > 0:
        Polyglot_Length_pre = polyglot_length_correct/polyglot_length_count
        if (Polyglot_Length_pre + Polyglot_Length_rec) > 0:
            Polyglot_Length_F1 = (2 * Polyglot_Length_pre * Polyglot_Length_rec) / (Polyglot_Length_pre + Polyglot_Length_rec)
        else:
            Polyglot_Length_F1 = 0
    else:
        Polyglot_Length_pre = 0
        Polyglot_Length_F1 = 0
    
    if True_delim_groudtruth > 0:
        Polyglot_Delim_rec = Inferred_True_delim/True_delim_groudtruth
    else:
        Polyglot_Delim_rec = 0
    
    if Inferred_delim > 0:
        Polyglot_Delim_pre = Inferred_True_delim/Inferred_delim
    else:
        Polyglot_Delim_pre = 0
    
    if (Polyglot_Delim_rec + Polyglot_Delim_pre) > 0:
        Polyglot_Delim_F1 = (2 * Polyglot_Delim_rec * Polyglot_Delim_pre) / (Polyglot_Delim_rec + Polyglot_Delim_pre)
    else:
        Polyglot_Delim_F1 = 0

    # with open(config.Evaluation_bo_Res, "a") as file:
    logging.info(f"\n\n\nPolyglot_Command_pre:{Polyglot_Command_pre}\n")
    logging.info(f"Polyglot_Command_rec:{Polyglot_Command_rec}\n")
    logging.info(f"Polyglot_Command_F1:{Polyglot_Command_F1}\n")

    logging.info(f"\n\nPolyglot_Tupni_Length_pre:{Polyglot_Length_pre}\n")
    logging.info(f"Polyglot_Tupni_Length_rec:{Polyglot_Length_rec}\n")
    logging.info(f"Polyglot_Tupni_Length_F1:{Polyglot_Length_F1}\n")

    logging.info(f"\n\Polyglot_Delim_pre:{Polyglot_Delim_pre}\n")
    logging.info(f"Polyglot_Delim_rec:{Polyglot_Delim_rec}\n")
    logging.info(f"Polyglot_Delim_F1:{Polyglot_Delim_F1}\n")


def ChatPre_Semantic_Types_Evaluator(payload_message, Pre_message_Result, message_Result, commandOffset):
    logging.info("\n\n\nSemantic-Types Evaluation Part For ChatPre(no validation)---------------------------------")
    
    '''Semantic-Type'''
    semantic_usedPre,msg_Pre, msg_Rec =0,0,0

    # msg_semanticTruth
    True_static_groudtruth = 0
    static_groudtruth = set()
    True_bytes_groudtruth = 0
    bytes_groudtruth = set()
    True_string_groudtruth = 0
    string_groudtruth = set()
    True_integer_groudtruth = 0
    integer_groudtruth = set()
    True_group_groudtruth = 0
    group_groudtruth = set()

    Inferred_True_static = 0
    Inferred_True_bytes = 0
    Inferred_True_string = 0
    Inferred_True_integer = 0
    Inferred_True_group = 0
    
    Inferred_static = 0
    Inferred_bytes = 0
    Inferred_string = 0
    Inferred_integer = 0
    Inferred_group = 0


    for i in range(0,len(payload_message)):
        msg_i = payload_message[i]
        msg_len = len(msg_i)
        command_start = int(commandOffset.split(',')[0])
        command_end = int(commandOffset.split(',')[-1])+1
        msg_command = payload_message[i][command_start:command_end]

        if config.evaluation_mode == 'index':
            msg_semanticTruth = Semantic_Groundtruth[i]
        else:
             msg_semanticTruth = Semantic_Groundtruth[msg_command]

        msg_semanticRes = Pre_message_Result[i].field_types


        logging.info(f"Msg {i} semantic evaluation:***\n")
        logging.info(f"msg_semanticTruth:{msg_semanticTruth}")
        logging.info(f"msg_semanticRes:{msg_semanticRes}\n")

        msg_pre, msg_rec= metrix_Cal(msg_semanticTruth,msg_semanticRes, Pre_message_Result[i].fields, msg_len)
        logging.info(f"msg_pre:{msg_pre}, msg_rec:{msg_rec}\n")
        
        msg_Pre += msg_pre
        msg_Rec += msg_rec
    
        for f,r in msg_semanticTruth.items():
            if (config.semantic_Types[0] in msg_semanticTruth[f]):
                True_static_groudtruth += 1
                static_groudtruth.add(f)

            if (config.semantic_Types[4] in msg_semanticTruth[f]):
                True_bytes_groudtruth += 1
                bytes_groudtruth.add(f)
            
            if (config.semantic_Types[2] in msg_semanticTruth[f]):
                True_string_groudtruth += 1
                string_groudtruth.add(f)
            
            if (config.semantic_Types[3] in msg_semanticTruth[f]):
                True_integer_groudtruth += 1
                integer_groudtruth.add(f)
            
            if (config.semantic_Types[1] in msg_semanticTruth[f]):
                True_group_groudtruth += 1
                group_groudtruth.add(f)

        for f,r in msg_semanticRes.items():

            if config.semantic_Types[0] in r:
                Inferred_static += 1
                if (f in msg_semanticTruth) and (config.semantic_Types[0] in msg_semanticTruth[f]):
                    Inferred_True_static += 1
            if config.semantic_Types[4] in r:
                Inferred_bytes += 1
                if (f in msg_semanticTruth) and (config.semantic_Types[4] in msg_semanticTruth[f]):
                    Inferred_True_bytes += 1
            
            if config.semantic_Types[2] in r:
                Inferred_string += 1
                if (f in msg_semanticTruth) and (config.semantic_Types[2] in msg_semanticTruth[f]):
                    Inferred_True_string += 1
            if config.semantic_Types[3] in r:
                Inferred_integer += 1
                if (f in msg_semanticTruth) and (config.semantic_Types[3] in msg_semanticTruth[f]):
                    Inferred_True_integer += 1
            if config.semantic_Types[1] in r:
                Inferred_group += 1
                if (f in msg_semanticTruth) and (config.semantic_Types[1] in msg_semanticTruth[f]):
                    Inferred_True_group += 1

    Average_Pre = msg_Pre/len(payload_message)
    Average_Rec = msg_Rec/len(payload_message)
    if (Average_Pre + Average_Rec) > 0:
        F1_score = (2 * Average_Pre * Average_Rec) / (Average_Pre + Average_Rec)
    else:
        F1_score = 0
    

    logging.info(f"Average_Pre:{Average_Pre}")
    logging.info(f"Average_Rec:{Average_Rec}")
    logging.info(f"F1_score:{F1_score}")

    if Inferred_static > 0:
        static_Pre = Inferred_True_static / Inferred_static
    else:
        static_Pre = 0
    if True_static_groudtruth >0:
        static_Rec = Inferred_True_static / True_static_groudtruth
    else:
        static_Rec = 0
    if (static_Pre + static_Rec) > 0:
        static_F1 = (2 * static_Pre * static_Rec) / (static_Pre + static_Rec)
    else:
        static_F1 = 0
    '''bytes'''
    if Inferred_bytes == 0:
        bytes_Pre = 0
    else:
        bytes_Pre = Inferred_True_bytes / Inferred_bytes
    
    if True_bytes_groudtruth == 0:
        bytes_Rec = 0
    else:
        bytes_Rec = Inferred_True_bytes / True_bytes_groudtruth
    
    if (bytes_Pre + bytes_Rec) > 0:
        bytes_F1 = (2 * bytes_Pre * bytes_Rec) / (bytes_Pre + bytes_Rec)
    else:
        bytes_F1 = 0
    '''string'''
    if Inferred_string == 0:
        string_Pre = 0
    else:
        string_Pre = Inferred_True_string / Inferred_string
    
    if True_string_groudtruth == 0:
        string_Rec = 0
    else:
        string_Rec = Inferred_True_string / True_string_groudtruth
    
    if (string_Pre + string_Rec) > 0:
        string_F1 = (2 * string_Pre * string_Rec) / (string_Pre + string_Rec)
    else:
        string_F1 = 0
    '''integer'''
    if Inferred_integer == 0:
        integer_Pre = 0
    else:
        integer_Pre = Inferred_True_integer / Inferred_integer
    
    if True_integer_groudtruth == 0:
        integer_Rec = 0
    else:
        integer_Rec = Inferred_True_integer / True_integer_groudtruth
    
    if (integer_Pre + integer_Rec) > 0:
        integer_F1 = (2 * integer_Pre * integer_Rec) / (integer_Pre + integer_Rec)
    else:
        integer_F1 = 0

    '''group'''
    if Inferred_group == 0:
        group_Pre = 0
    else:
        group_Pre = Inferred_True_group / Inferred_group
    
    if True_group_groudtruth == 0:
        group_Rec = 0
    else:
        group_Rec = Inferred_True_group / True_group_groudtruth
    
    if (group_Pre + group_Rec) > 0:
        group_F1 = (2 * group_Pre * group_Rec) / (group_Pre + group_Rec)
    else:
        group_F1 = 0

    no_Average_Pre = Average_Pre
    no_Average_Rec = Average_Rec
    no_F1_score = F1_score

    # with open(config.Evaluation_Res, "a") as file:
    logging.info("\n\n\Semantic-Type Evaluation Part For ChatPre(no validation)---------------------------------\n")
    logging.info(f"no_Average_Pre:{Average_Pre}\n")
    logging.info(f"no_Average_Rec:{Average_Rec}\n")
    logging.info(f"no_F1_score:{F1_score}\n")

    logging.info(f"\nno_static_Pre:{static_Pre}\n")
    logging.info(f"no_static_Rec:{static_Rec}\n")
    logging.info(f"no_static_F1:{static_F1}\n")
    logging.info(f"no_static_groudtruth:{static_groudtruth}\n")

    logging.info(f"\nno_integer_Pre:{integer_Pre}\n")
    logging.info(f"no_integer_Rec:{integer_Rec}\n")
    logging.info(f"no_integer_F1:{integer_F1}\n")
    logging.info(f"no_integer_groudtruth:{integer_groudtruth}\n") 

    logging.info(f"\nno_group_Pre:{group_Pre}\n")
    logging.info(f"no_group_Rec:{group_Rec}\n")
    logging.info(f"no_group_F1:{group_F1}\n")
    logging.info(f"no_group_groudtruth:{group_groudtruth}\n") 

    logging.info(f"\nno_bytes_Pre:{bytes_Pre}\n")
    logging.info(f"no_bytes_Rec:{bytes_Rec}\n")
    logging.info(f"no_bytes_F1:{bytes_F1}\n")
    logging.info(f"no_bytes_groudtruth:{bytes_groudtruth}\n") 

    logging.info(f"\nno_string_Pre:{string_Pre}\n")
    logging.info(f"no_string_Rec:{string_Rec}\n")
    logging.info(f"no_string_F1:{string_F1}\n")
    logging.info(f"no_string_groudtruth:{string_groudtruth}\n") 


         

    logging.info("\n\n\nSemantic-Types Evaluation Part For ChatPre(Validated)---------------------------------")
    

    '''Semantic-Type'''
    semantic_usedPre,msg_Pre, msg_Rec =0,0,0

    # msg_semanticTruth
    True_static_groudtruth = 0
    static_groudtruth = set()
    True_bytes_groudtruth = 0
    bytes_groudtruth = set()
    True_string_groudtruth = 0
    string_groudtruth = set()
    True_integer_groudtruth = 0
    integer_groudtruth = set()
    True_group_groudtruth = 0
    group_groudtruth = set()

    Inferred_True_static = 0
    Inferred_True_bytes = 0
    Inferred_True_string = 0
    Inferred_True_integer = 0
    Inferred_True_group = 0
    
    Inferred_static = 0
    Inferred_bytes = 0
    Inferred_string = 0
    Inferred_integer = 0
    Inferred_group = 0

    for i in range(0,len(payload_message)):
        msg_i = payload_message[i]
        msg_len = len(msg_i)
        command_start = int(commandOffset.split(',')[0])
        command_end = int(commandOffset.split(',')[-1])+1
        msg_command = payload_message[i][command_start:command_end]

        if config.evaluation_mode == 'index':
            msg_semanticTruth = Semantic_Groundtruth[i]
        else:
            msg_semanticTruth = Semantic_Groundtruth[msg_command]


        msg_semanticRes = message_Result[i].field_types


        logging.info(f"Msg {i} semantic evaluation:***\n")
        logging.info(f"msg_semanticTruth:{msg_semanticTruth}")
        logging.info(f"msg_semanticRes:{msg_semanticRes}\n")

        msg_pre, msg_rec= metrix_Cal(msg_semanticTruth,msg_semanticRes, message_Result[i].fields, msg_len)
        logging.info(f"msg_pre:{msg_pre}, msg_rec:{msg_rec}\n")
        
        msg_Pre += msg_pre
        msg_Rec += msg_rec



        for f,r in msg_semanticTruth.items():
            if (config.semantic_Types[0] in msg_semanticTruth[f]):
                True_static_groudtruth += 1
                static_groudtruth.add(f)

            if (config.semantic_Types[4] in msg_semanticTruth[f]):
                True_bytes_groudtruth += 1
                bytes_groudtruth.add(f)
            
            if (config.semantic_Types[2] in msg_semanticTruth[f]):
                True_string_groudtruth += 1
                string_groudtruth.add(f)
            
            if (config.semantic_Types[3] in msg_semanticTruth[f]):
                True_integer_groudtruth += 1
                integer_groudtruth.add(f)
            
            if (config.semantic_Types[1] in msg_semanticTruth[f]):
                True_group_groudtruth += 1
                group_groudtruth.add(f)

        for f,r in msg_semanticRes.items():

            if config.semantic_Types[0] in r:
                Inferred_static += 1
                if (f in msg_semanticTruth) and (config.semantic_Types[0] in msg_semanticTruth[f]):
                    Inferred_True_static += 1
            if config.semantic_Types[4] in r:
                Inferred_bytes += 1
                if (f in msg_semanticTruth) and (config.semantic_Types[4] in msg_semanticTruth[f]):
                    Inferred_True_bytes += 1
            
            if config.semantic_Types[2] in r:
                Inferred_string += 1
                if (f in msg_semanticTruth) and (config.semantic_Types[2] in msg_semanticTruth[f]):
                    Inferred_True_string += 1
            if config.semantic_Types[3] in r:
                Inferred_integer += 1
                if (f in msg_semanticTruth) and (config.semantic_Types[3] in msg_semanticTruth[f]):
                    Inferred_True_integer += 1
            if config.semantic_Types[1] in r:
                Inferred_group += 1
                if (f in msg_semanticTruth) and (config.semantic_Types[1] in msg_semanticTruth[f]):
                    Inferred_True_group += 1
        

    Average_Pre = msg_Pre/len(payload_message)
    Average_Rec = msg_Rec/len(payload_message)
    if (Average_Pre + Average_Rec) > 0:
        F1_score = (2 * Average_Pre * Average_Rec) / (Average_Pre + Average_Rec)
    else:
        F1_score = 0
    if Inferred_static >0:
        static_Pre = Inferred_True_static / Inferred_static
    else:
        static_Pre = 0
    
    if (static_Pre + static_Rec) > 0:
        static_F1 = (2 * static_Pre * static_Rec) / (static_Pre + static_Rec)
    else:
        static_F1 = 0
    '''bytes'''
    if Inferred_bytes == 0:
        bytes_Pre = 0
    else:
        bytes_Pre = Inferred_True_bytes / Inferred_bytes
    
    if True_bytes_groudtruth == 0:
        bytes_Rec = 0
    else:
        bytes_Rec = Inferred_True_bytes / True_bytes_groudtruth
    
    if (bytes_Pre + bytes_Rec) > 0:
        bytes_F1 = (2 * bytes_Pre * bytes_Rec) / (bytes_Pre + bytes_Rec)
    else:
        bytes_F1 = 0
    '''string'''
    if Inferred_string == 0:
        string_Pre = 0
    else:
        string_Pre = Inferred_True_string / Inferred_string
    
    if True_string_groudtruth == 0:
        string_Rec = 0
    else:
        string_Rec = Inferred_True_string / True_string_groudtruth
    
    if (string_Pre + string_Rec) > 0:
        string_F1 = (2 * string_Pre * string_Rec) / (string_Pre + string_Rec)
    else:
        string_F1 = 0
    '''integer'''
    if Inferred_integer == 0:
        integer_Pre = 0
    else:
        integer_Pre = Inferred_True_integer / Inferred_integer
    
    if True_integer_groudtruth == 0:
        integer_Rec = 0
    else:
        integer_Rec = Inferred_True_integer / True_integer_groudtruth
    
    if (integer_Pre + integer_Rec) > 0:
        integer_F1 = (2 * integer_Pre * integer_Rec) / (integer_Pre + integer_Rec)
    else:
        integer_F1 = 0

    '''group'''
    if Inferred_group == 0:
        group_Pre = 0
    else:
        group_Pre = Inferred_True_group / Inferred_group
    
    if True_group_groudtruth == 0:
        group_Rec = 0
    else:
        group_Rec = Inferred_True_group / True_group_groudtruth
    
    if (group_Pre + group_Rec) > 0:
        group_F1 = (2 * group_Pre * group_Rec) / (group_Pre + group_Rec)
    else:
        group_F1 = 0

    logging.info(f"Average_Pre:{Average_Pre}")
    logging.info(f"Average_Rec:{Average_Rec}")
    logging.info(f"F1_score:{F1_score}")
    

    


    # with open(config.Evaluation_Res, "a") as file:
    logging.info("\n\n\Semantic-Type Evaluation Part For ChatPre(Validated)---------------------------------\n")
    logging.info(f"Average_Pre:{Average_Pre}\n")
    logging.info(f"Average_Rec:{Average_Rec}\n")
    logging.info(f"F1_score:{F1_score}\n")

    logging.info(f"\nstatic_Pre:{static_Pre}\n")
    logging.info(f"static_Rec:{static_Rec}\n")
    logging.info(f"static_F1:{static_F1}\n")
    logging.info(f"static_groudtruth:{static_groudtruth}\n")

    logging.info(f"\ninteger_Pre:{integer_Pre}\n")
    logging.info(f"integer_Rec:{integer_Rec}\n")
    logging.info(f"integer_F1:{integer_F1}\n")
    logging.info(f"integer_groudtruth:{integer_groudtruth}\n") 

    logging.info(f"\ngroup_Pre:{group_Pre}\n")
    logging.info(f"group_Rec:{group_Rec}\n")
    logging.info(f"group_F1:{group_F1}\n")
    logging.info(f"group_groudtruth:{group_groudtruth}\n")    

    logging.info(f"\nbytes_Pre:{bytes_Pre}\n")
    logging.info(f"bytes_Rec:{bytes_Rec}\n")
    logging.info(f"bytes_F1:{bytes_F1}\n")
    logging.info(f"bytes_groudtruth:{bytes_groudtruth}\n") 

    logging.info(f"\nstring_Pre:{string_Pre}\n")
    logging.info(f"string_Rec:{string_Rec}\n")
    logging.info(f"string_F1:{string_F1}\n")
    logging.info(f"string_groudtruth:{string_groudtruth}\n") 
    
    return no_Average_Pre, no_Average_Rec, no_F1_score, Average_Pre, Average_Rec, F1_score

            

def ChatPre_Semantic_Functions_Evaluator(payload_message, Pre_message_Result, message_Result, commandOffset):
    logging.info("\n\n\nSemantic-Functions Evaluation Part For ChatPre(no validation)---------------------------------")
    
    '''Semantic-Function'''
    semantic_usedPre,msg_Pre, msg_Rec =0,0,0

    no_ChatPre_command_count = 0
    no_ChatPre_command_correct = 0

    ChatPre_length_correct = 0
    ChatPre_command_correct = 0
    ChatPre_length_count = 0
    ChatPre_command_count = 0

    True_delim_groudtruth = 0
    Inferred_delim = 0
    Inferred_True_delim = 0
    delim_groudtruth = set()

    True_aligned_groudtruth = 0
    Inferred_aligned = 0
    Inferred_True_aligned = 0
    aligned_groudtruth = set()

    True_filename_groudtruth = 0
    Inferred_filename = 0
    Inferred_True_filename = 0
    filename_groudtruth = set()

    for i in range(0,len(payload_message)):
        msg_i = payload_message[i]
        msg_len = len(msg_i)
        command_start = int(commandOffset.split(',')[0])
        command_end = int(commandOffset.split(',')[-1])+1
        msg_command = payload_message[i][command_start:command_end]

        if config.evaluation_mode == 'index':
            msg_semanticTruth = Semantic_Functions_Groundtruth[i]
            msg_fieldTruth = Semantic_Groundtruth[i]
        else:
            msg_semanticTruth = Semantic_Functions_Groundtruth[msg_command]
            msg_fieldTruth = Semantic_Groundtruth[msg_command]

        msg_semanticRes = Pre_message_Result[i].field_funcs

        for f,r in msg_semanticRes.items():
            if config.semantic_Functions[0] in r:
                no_ChatPre_command_count += 1
                if f == config.commandOffset:
                    no_ChatPre_command_correct += 1


        logging.info(f"Msg {i} semantic evaluation:***\n")
        logging.info(f"msg_semanticTruth:{msg_semanticTruth}")
        logging.info(f"msg_semanticRes:{msg_semanticRes}\n")

        msg_pre, msg_rec= metrix_Cal_Func(msg_semanticTruth,msg_semanticRes, Pre_message_Result[i].fields, msg_len, msg_fieldTruth)
        logging.info(f"msg_pre:{msg_pre}, msg_rec:{msg_rec}\n")
        
        msg_Pre += msg_pre
        msg_Rec += msg_rec
        for f,r in msg_semanticRes.items():
            logging.info(f"f:{f}, r:{r}")
            if config.semantic_Functions[0] in r:
                ChatPre_command_count += 1
                if f == config.commandOffset:
                    ChatPre_command_correct += 1
            if config.semantic_Functions[1] in r:
                ChatPre_length_count += 1
                if f == config.lengthOffset:
                    ChatPre_length_correct += 1
        
        
        
        for f,r in msg_semanticTruth.items():
            if (config.semantic_Functions[2] in msg_semanticTruth[f]):
                True_delim_groudtruth += 1
                delim_groudtruth.add(f)
            if (config.semantic_Functions[4] in msg_semanticTruth[f]):
                True_aligned_groudtruth += 1
                aligned_groudtruth.add(f)
            if (config.semantic_Functions[5] in msg_semanticTruth[f]):
                True_filename_groudtruth += 1
                filename_groudtruth.add(f)


        for f,r in msg_semanticRes.items():

            if config.semantic_Functions[2] in r:
                Inferred_delim += 1
                if (f in msg_semanticTruth) and (config.semantic_Functions[2] in msg_semanticTruth[f]):
                    Inferred_True_delim += 1
            
            if config.semantic_Functions[4] in r:
                Inferred_aligned += 1
                if (f in msg_semanticTruth) and (config.semantic_Functions[4] in msg_semanticTruth[f]):
                    Inferred_True_aligned += 1
            
            if config.semantic_Functions[5] in r:
                Inferred_filename += 1
                if (f in msg_semanticTruth) and (config.semantic_Functions[5] in msg_semanticTruth[f]):
                    Inferred_True_filename += 1

    Average_Pre = msg_Pre/len(payload_message)
    Average_Rec = msg_Rec/len(payload_message)
    if (Average_Pre + Average_Rec) > 0:
        F1_score = (2 * Average_Pre * Average_Rec) / (Average_Pre + Average_Rec)
    else:
        F1_score = 0
    

    logging.info(f"Average_Pre:{Average_Pre}")
    logging.info(f"Average_Rec:{Average_Rec}")
    logging.info(f"F1_score:{F1_score}")

    no_ChatPre_Command_rec = no_ChatPre_command_correct/len(payload_message)
    if no_ChatPre_command_count>0:
        no_ChatPre_Command_pre = no_ChatPre_command_correct / no_ChatPre_command_count
        if (no_ChatPre_Command_pre + no_ChatPre_Command_rec) > 0:
            no_ChatPre_Command_F1 = (2 * no_ChatPre_Command_pre * no_ChatPre_Command_rec) / (no_ChatPre_Command_pre + no_ChatPre_Command_rec)
        else:
            no_ChatPre_Command_F1 = 0
    else:
        no_ChatPre_Command_pre = 0
        no_ChatPre_Command_F1 = 0
    
    ChatPre_Command_rec = ChatPre_command_correct/len(payload_message)
    ChatPre_Length_rec = ChatPre_length_correct/len(payload_message)
    if ChatPre_command_count>0:
        ChatPre_Command_pre = ChatPre_command_correct/ChatPre_command_count
        if (ChatPre_Command_pre + ChatPre_Command_rec) > 0:
            ChatPre_Command_F1 = (2 * ChatPre_Command_pre * ChatPre_Command_rec) / (ChatPre_Command_pre + ChatPre_Command_rec) 
        else:
            ChatPre_Command_F1 = 0
    else:
        ChatPre_Command_pre = 0
        ChatPre_Command_F1 = 0
    if ChatPre_length_count>0:
        ChatPre_Length_pre = ChatPre_length_correct / ChatPre_length_count
        if (ChatPre_Length_pre + ChatPre_Length_rec) > 0:
            ChatPre_Length_F1 = (2 * ChatPre_Length_pre * ChatPre_Length_rec) / (ChatPre_Length_pre + ChatPre_Length_rec)
        else:
            ChatPre_Length_F1 = 0
    else:
        ChatPre_Length_pre = 0
        ChatPre_Length_F1 = 0
    if True_delim_groudtruth > 0:
        ChatPre_Delim_rec = Inferred_True_delim/True_delim_groudtruth
    else:
        ChatPre_Delim_rec = 0
    
    if Inferred_delim > 0:
        ChatPre_Delim_pre = Inferred_True_delim/Inferred_delim
    else:
        ChatPre_Delim_pre = 0
    
    if (ChatPre_Delim_rec + ChatPre_Delim_pre) > 0:
        ChatPre_Delim_F1 = (2 * ChatPre_Delim_rec * ChatPre_Delim_pre) / (ChatPre_Delim_rec + ChatPre_Delim_pre)
    else:
        ChatPre_Delim_F1 = 0
    if True_aligned_groudtruth > 0:
        ChatPre_aligned_rec = Inferred_True_aligned/True_aligned_groudtruth
    else:
        ChatPre_aligned_rec = 0
    
    if Inferred_aligned > 0:
        ChatPre_aligned_pre = Inferred_True_aligned/Inferred_aligned
    else:
        ChatPre_aligned_pre = 0
    
    if (ChatPre_aligned_rec + ChatPre_aligned_pre) > 0:
        ChatPre_aligned_F1 = (2 * ChatPre_aligned_rec * ChatPre_aligned_pre) / (ChatPre_aligned_rec + ChatPre_aligned_pre)
    else:
        ChatPre_aligned_F1 = 0
    if True_filename_groudtruth > 0:
        ChatPre_filename_rec = Inferred_True_filename/True_filename_groudtruth
    else:
        ChatPre_filename_rec = 0
    
    if Inferred_filename > 0:
        ChatPre_filename_pre = Inferred_True_filename/Inferred_filename
    else:
        ChatPre_filename_pre = 0
    
    if (ChatPre_filename_rec + ChatPre_filename_pre) > 0:
        ChatPre_filename_F1 = (2 * ChatPre_filename_rec * ChatPre_filename_pre) / (ChatPre_filename_rec + ChatPre_filename_pre)
    else:
        ChatPre_filename_F1 = 0

    no_Average_Pre = Average_Pre
    no_Average_Rec = Average_Rec
    no_F1_score = F1_score

    # with open(config.Evaluation_Res, "a") as file:
    logging.info("\n\n\Semantic-Function Evaluation Part For ChatPre(no validation)---------------------------------\n")
    logging.info(f"Average_Pre:{Average_Pre}\n")
    logging.info(f"Average_Rec:{Average_Rec}\n")
    logging.info(f"F1_score:{F1_score}\n\n")
    logging.info(f"no_ChatPre_Command_pre:{no_ChatPre_Command_pre}\n")
    logging.info(f"no_ChatPre_Command_rec:{no_ChatPre_Command_rec}\n")
    logging.info(f"no_ChatPre_Command_F1:{no_ChatPre_Command_F1}\n\n")
    logging.info(f"\n")
    logging.info(f"no_ChatPre_Command_pre:{ChatPre_Command_pre}\n")
    logging.info(f"no_ChatPre_Command_rec:{ChatPre_Command_rec}\n")
    logging.info(f"no_ChatPre_Command_F1:{ChatPre_Command_F1}\n")
    logging.info(f"\nno_ChatPre_Length_pre:{ChatPre_Length_pre}\n")
    logging.info(f"no_ChatPre_Length_rec:{ChatPre_Length_rec}\n")
    logging.info(f"no_ChatPre_Length_F1:{ChatPre_Length_F1}\n")
    logging.info(f"\nno_ChatPre_Delim_pre:{ChatPre_Delim_pre}\n")
    logging.info(f"no_ChatPre_Delim_rec:{ChatPre_Delim_rec}\n")
    logging.info(f"no_ChatPre_Delim_F1:{ChatPre_Delim_F1}\n")
    logging.info(f"no_delim_groudtruth:{delim_groudtruth}\n")
    logging.info(f"\nno_ChatPre_aligned_pre:{ChatPre_aligned_pre}\n")
    logging.info(f"no_ChatPre_aligned_rec:{ChatPre_aligned_rec}\n")
    logging.info(f"no_ChatPre_aligned_F1:{ChatPre_aligned_F1}\n")
    logging.info(f"no_aligned_groudtruth:{aligned_groudtruth}\n")
    logging.info(f"\nno_ChatPre_filename_pre:{ChatPre_filename_pre}\n")
    logging.info(f"no_ChatPre_filename_rec:{ChatPre_filename_rec}\n")
    logging.info(f"no_ChatPre_filename_F1:{ChatPre_filename_F1}\n")
    logging.info(f"no_filename_groudtruth:{filename_groudtruth}\n")

    logging.info("\n\n\nSemantic-Functions Evaluation Part For ChatPre(Validated)---------------------------------")
    

    '''Semantic-Function'''
    semantic_usedPre,msg_Pre, msg_Rec =0,0,0

    ChatPre_length_correct = 0
    ChatPre_command_correct = 0
    ChatPre_length_count = 0
    ChatPre_command_count = 0

    True_delim_groudtruth = 0
    Inferred_delim = 0
    Inferred_True_delim = 0
    delim_groudtruth = set()

    True_aligned_groudtruth = 0
    Inferred_aligned = 0
    Inferred_True_aligned = 0
    aligned_groudtruth = set()

    True_filename_groudtruth = 0
    Inferred_filename = 0
    Inferred_True_filename = 0
    filename_groudtruth = set()

    for i in range(0,len(payload_message)):
        msg_i = payload_message[i]
        msg_len = len(msg_i)
        command_start = int(commandOffset.split(',')[0])
        command_end = int(commandOffset.split(',')[-1])+1
        msg_command = payload_message[i][command_start:command_end]

        if config.evaluation_mode == 'index':
            msg_semanticTruth = Semantic_Functions_Groundtruth[i]
            msg_fieldTruth = Semantic_Groundtruth[i]
        else:
            msg_semanticTruth = Semantic_Functions_Groundtruth[msg_command]
            msg_fieldTruth = Semantic_Groundtruth[msg_command]

        msg_semanticRes = message_Result[i].field_funcs

        for f,r in msg_semanticRes.items():
            if config.semantic_Functions[0] in r:
                ChatPre_command_count += 1
                if f == config.commandOffset:
                    ChatPre_command_correct += 1
            if config.semantic_Functions[1] in r:
                ChatPre_length_count += 1
                if f == config.lengthOffset:
                    ChatPre_length_correct += 1
        
        for f,r in msg_semanticTruth.items():
            if (config.semantic_Functions[2] in msg_semanticTruth[f]):
                True_delim_groudtruth += 1
                delim_groudtruth.add(f)
            if (config.semantic_Functions[4] in msg_semanticTruth[f]):
                True_aligned_groudtruth += 1
                aligned_groudtruth.add(f)
            if (config.semantic_Functions[5] in msg_semanticTruth[f]):
                True_filename_groudtruth += 1
                filename_groudtruth.add(f)


        for f,r in msg_semanticRes.items():

            if config.semantic_Functions[2] in r:
                Inferred_delim += 1
                if (f in msg_semanticTruth) and (config.semantic_Functions[2] in msg_semanticTruth[f]):
                    Inferred_True_delim += 1
            
            if config.semantic_Functions[4] in r:
                Inferred_aligned += 1
                if (f in msg_semanticTruth) and (config.semantic_Functions[4] in msg_semanticTruth[f]):
                    Inferred_True_aligned += 1
            
            if config.semantic_Functions[5] in r:
                Inferred_filename += 1
                if (f in msg_semanticTruth) and (config.semantic_Functions[5] in msg_semanticTruth[f]):
                    Inferred_True_filename += 1
            

        logging.info(f"Msg {i} semantic evaluation:***\n")
        logging.info(f"msg_semanticTruth:{msg_semanticTruth}")
        logging.info(f"msg_semanticRes:{msg_semanticRes}\n")

        msg_pre, msg_rec= metrix_Cal_Func(msg_semanticTruth,msg_semanticRes, message_Result[i].fields, msg_len, msg_fieldTruth)
        logging.info(f"msg_pre:{msg_pre}, msg_rec:{msg_rec}\n")
        
        msg_Pre += msg_pre
        msg_Rec += msg_rec
        

    Average_Pre = msg_Pre/len(payload_message)
    Average_Rec = msg_Rec/len(payload_message)
    if (Average_Pre + Average_Rec) > 0:
        F1_score = (2 * Average_Pre * Average_Rec) / (Average_Pre + Average_Rec)
    else:
        F1_score = 0
    

    logging.info(f"Average_Pre:{Average_Pre}")
    logging.info(f"Average_Rec:{Average_Rec}")
    logging.info(f"F1_score:{F1_score}")
    
    ChatPre_Command_rec = ChatPre_command_correct/len(payload_message)
    ChatPre_Length_rec = ChatPre_length_correct/len(payload_message)
    if ChatPre_command_count>0:
        ChatPre_Command_pre = ChatPre_command_correct/ChatPre_command_count
        if (ChatPre_Command_pre + ChatPre_Command_rec) > 0:
            ChatPre_Command_F1 = (2 * ChatPre_Command_pre * ChatPre_Command_rec) / (ChatPre_Command_pre + ChatPre_Command_rec) 
        else:
            ChatPre_Command_F1 = 0
    else:
        ChatPre_Command_pre = 0
        ChatPre_Command_F1 = 0
    if ChatPre_length_count>0:
        ChatPre_Length_pre = ChatPre_length_correct / ChatPre_length_count
        if (ChatPre_Length_pre + ChatPre_Length_rec) > 0:
            ChatPre_Length_F1 = (2 * ChatPre_Length_pre * ChatPre_Length_rec) / (ChatPre_Length_pre + ChatPre_Length_rec)
        else:
            ChatPre_Length_F1 = 0
    else:
        ChatPre_Length_pre = 0
        ChatPre_Length_F1 = 0
    if True_delim_groudtruth > 0:
        ChatPre_Delim_rec = Inferred_True_delim/True_delim_groudtruth
    else:
        ChatPre_Delim_rec = 0
    
    if Inferred_delim > 0:
        ChatPre_Delim_pre = Inferred_True_delim/Inferred_delim
    else:
        ChatPre_Delim_pre = 0
    
    if (ChatPre_Delim_rec + ChatPre_Delim_pre) > 0:
        ChatPre_Delim_F1 = (2 * ChatPre_Delim_rec * ChatPre_Delim_pre) / (ChatPre_Delim_rec + ChatPre_Delim_pre)
    else:
        ChatPre_Delim_F1 = 0
    if True_aligned_groudtruth > 0:
        ChatPre_aligned_rec = Inferred_True_aligned/True_aligned_groudtruth
    else:
        ChatPre_aligned_rec = 0
    
    if Inferred_aligned > 0:
        ChatPre_aligned_pre = Inferred_True_aligned/Inferred_aligned
    else:
        ChatPre_aligned_pre = 0
    
    if (ChatPre_aligned_rec + ChatPre_aligned_pre) > 0:
        ChatPre_aligned_F1 = (2 * ChatPre_aligned_rec * ChatPre_aligned_pre) / (ChatPre_aligned_rec + ChatPre_aligned_pre)
    else:
        ChatPre_aligned_F1 = 0
    if True_filename_groudtruth > 0:
        ChatPre_filename_rec = Inferred_True_filename/True_filename_groudtruth
    else:
        ChatPre_filename_rec = 0
    
    if Inferred_filename > 0:
        ChatPre_filename_pre = Inferred_True_filename/Inferred_filename
    else:
        ChatPre_filename_pre = 0
    
    if (ChatPre_filename_rec + ChatPre_filename_pre) > 0:
        ChatPre_filename_F1 = (2 * ChatPre_filename_rec * ChatPre_filename_pre) / (ChatPre_filename_rec + ChatPre_filename_pre)
    else:
        ChatPre_filename_F1 = 0

    logging.info(f"ChatPre_Command_pre:{ChatPre_Command_pre}")
    logging.info(f"ChatPre_Command_rec:{ChatPre_Command_rec}")
    logging.info(f"ChatPre_Length_pre:{ChatPre_Length_pre}")
    logging.info(f"ChatPre_Length_rec:{ChatPre_Length_rec}")

    # with open(config.Evaluation_Res, "a") as file:
    logging.info("\n\n\Semantic-Function Evaluation Part For ChatPre(Validated)---------------------------------\n")
    logging.info(f"Average_Pre:{Average_Pre}\n")
    logging.info(f"Average_Rec:{Average_Rec}\n")
    logging.info(f"F1_score:{F1_score}\n")
    logging.info(f"\n")
    logging.info(f"ChatPre_Command_pre:{ChatPre_Command_pre}\n")
    logging.info(f"ChatPre_Command_rec:{ChatPre_Command_rec}\n")
    logging.info(f"ChatPre_Command_F1:{ChatPre_Command_F1}\n")
    logging.info(f"\nChatPre_Length_pre:{ChatPre_Length_pre}\n")
    logging.info(f"ChatPre_Length_rec:{ChatPre_Length_rec}\n")
    logging.info(f"ChatPre_Length_F1:{ChatPre_Length_F1}\n")
    logging.info(f"\nChatPre_Delim_pre:{ChatPre_Delim_pre}\n")
    logging.info(f"ChatPre_Delim_rec:{ChatPre_Delim_rec}\n")
    logging.info(f"ChatPre_Delim_F1:{ChatPre_Delim_F1}\n")
    logging.info(f"delim_groudtruth:{delim_groudtruth}\n")
    logging.info(f"\nChatPre_aligned_pre:{ChatPre_aligned_pre}\n")
    logging.info(f"ChatPre_aligned_rec:{ChatPre_aligned_rec}\n")
    logging.info(f"ChatPre_aligned_F1:{ChatPre_aligned_F1}\n")
    logging.info(f"aligned_groudtruth:{aligned_groudtruth}\n")
    logging.info(f"\nChatPre_filename_pre:{ChatPre_filename_pre}\n")
    logging.info(f"ChatPre_filename_rec:{ChatPre_filename_rec}\n")
    logging.info(f"ChatPre_filename_F1:{ChatPre_filename_F1}\n")
    logging.info(f"filename_groudtruth:{filename_groudtruth}\n")

    return no_Average_Pre, no_Average_Rec, no_F1_score, Average_Pre, Average_Rec, F1_score



def ChatPreLLM_Semantic_Types_Evaluator(payload_message, Pre_message_Result, message_Result, commandOffset):
    logging.info("\n\n\nSemantic-Types Evaluation Part For ChatPre-repartition(no validation)---------------------------------")
    
    '''Semantic-Type'''
    semantic_usedPre,msg_Pre, msg_Rec =0,0,0

    # msg_semanticTruth
    True_static_groudtruth = 0
    static_groudtruth = set()
    True_bytes_groudtruth = 0
    bytes_groudtruth = set()
    True_string_groudtruth = 0
    string_groudtruth = set()
    True_integer_groudtruth = 0
    integer_groudtruth = set()
    True_group_groudtruth = 0
    group_groudtruth = set()

    Inferred_True_static = 0
    Inferred_True_bytes = 0
    Inferred_True_string = 0
    Inferred_True_integer = 0
    Inferred_True_group = 0
    
    Inferred_static = 0
    Inferred_bytes = 0
    Inferred_string = 0
    Inferred_integer = 0
    Inferred_group = 0


    for i in range(0,len(payload_message)):
        msg_i = payload_message[i]
        msg_len = len(msg_i)
        command_start = int(commandOffset.split(',')[0])
        command_end = int(commandOffset.split(',')[-1])+1
        msg_command = payload_message[i][command_start:command_end]

        if config.evaluation_mode == 'index':
            msg_semanticTruth = Semantic_Groundtruth[i]
        else:
             msg_semanticTruth = Semantic_Groundtruth[msg_command]

        msg_semanticRes = Pre_message_Result[i].field_types


        logging.info(f"Msg {i} semantic evaluation:***\n")
        logging.info(f"msg_semanticTruth:{msg_semanticTruth}")
        logging.info(f"msg_semanticRes:{msg_semanticRes}\n")

        msg_pre, msg_rec= metrix_Cal(msg_semanticTruth,msg_semanticRes, Pre_message_Result[i].fields, msg_len)
        logging.info(f"msg_pre:{msg_pre}, msg_rec:{msg_rec}\n")
        
        msg_Pre += msg_pre
        msg_Rec += msg_rec
    
        for f,r in msg_semanticTruth.items():
            if (config.semantic_Types[0] in msg_semanticTruth[f]):
                True_static_groudtruth += 1
                static_groudtruth.add(f)

            if (config.semantic_Types[4] in msg_semanticTruth[f]):
                True_bytes_groudtruth += 1
                bytes_groudtruth.add(f)
            
            if (config.semantic_Types[2] in msg_semanticTruth[f]):
                True_string_groudtruth += 1
                string_groudtruth.add(f)
            
            if (config.semantic_Types[3] in msg_semanticTruth[f]):
                True_integer_groudtruth += 1
                integer_groudtruth.add(f)
            
            if (config.semantic_Types[1] in msg_semanticTruth[f]):
                True_group_groudtruth += 1
                group_groudtruth.add(f)

        for f,r in msg_semanticRes.items():

            if config.semantic_Types[0] in r:
                Inferred_static += 1
                if (f in msg_semanticTruth) and (config.semantic_Types[0] in msg_semanticTruth[f]):
                    Inferred_True_static += 1
            if config.semantic_Types[4] in r:
                Inferred_bytes += 1
                if (f in msg_semanticTruth) and (config.semantic_Types[4] in msg_semanticTruth[f]):
                    Inferred_True_bytes += 1
            
            if config.semantic_Types[2] in r:
                Inferred_string += 1
                if (f in msg_semanticTruth) and (config.semantic_Types[2] in msg_semanticTruth[f]):
                    Inferred_True_string += 1
            if config.semantic_Types[3] in r:
                Inferred_integer += 1
                if (f in msg_semanticTruth) and (config.semantic_Types[3] in msg_semanticTruth[f]):
                    Inferred_True_integer += 1
            if config.semantic_Types[1] in r:
                Inferred_group += 1
                if (f in msg_semanticTruth) and (config.semantic_Types[1] in msg_semanticTruth[f]):
                    Inferred_True_group += 1

    Average_Pre = msg_Pre/len(payload_message)
    Average_Rec = msg_Rec/len(payload_message)
    if (Average_Pre + Average_Rec) > 0:
        F1_score = (2 * Average_Pre * Average_Rec) / (Average_Pre + Average_Rec)
    else:
        F1_score = 0
    

    logging.info(f"Average_Pre:{Average_Pre}")
    logging.info(f"Average_Rec:{Average_Rec}")
    logging.info(f"F1_score:{F1_score}")

    if Inferred_static > 0:
        static_Pre = Inferred_True_static / Inferred_static
    else:
        static_Pre = 0
    if True_static_groudtruth >0:
        static_Rec = Inferred_True_static / True_static_groudtruth
    else:
        static_Rec = 0
    if (static_Pre + static_Rec) > 0:
        static_F1 = (2 * static_Pre * static_Rec) / (static_Pre + static_Rec)
    else:
        static_F1 = 0
    '''bytes'''
    if Inferred_bytes == 0:
        bytes_Pre = 0
    else:
        bytes_Pre = Inferred_True_bytes / Inferred_bytes
    
    if True_bytes_groudtruth == 0:
        bytes_Rec = 0
    else:
        bytes_Rec = Inferred_True_bytes / True_bytes_groudtruth
    
    if (bytes_Pre + bytes_Rec) > 0:
        bytes_F1 = (2 * bytes_Pre * bytes_Rec) / (bytes_Pre + bytes_Rec)
    else:
        bytes_F1 = 0
    '''string'''
    if Inferred_string == 0:
        string_Pre = 0
    else:
        string_Pre = Inferred_True_string / Inferred_string
    
    if True_string_groudtruth == 0:
        string_Rec = 0
    else:
        string_Rec = Inferred_True_string / True_string_groudtruth
    
    if (string_Pre + string_Rec) > 0:
        string_F1 = (2 * string_Pre * string_Rec) / (string_Pre + string_Rec)
    else:
        string_F1 = 0
    '''integer'''
    if Inferred_integer == 0:
        integer_Pre = 0
    else:
        integer_Pre = Inferred_True_integer / Inferred_integer
    
    if True_integer_groudtruth == 0:
        integer_Rec = 0
    else:
        integer_Rec = Inferred_True_integer / True_integer_groudtruth
    
    if (integer_Pre + integer_Rec) > 0:
        integer_F1 = (2 * integer_Pre * integer_Rec) / (integer_Pre + integer_Rec)
    else:
        integer_F1 = 0

    '''group'''
    if Inferred_group == 0:
        group_Pre = 0
    else:
        group_Pre = Inferred_True_group / Inferred_group
    
    if True_group_groudtruth == 0:
        group_Rec = 0
    else:
        group_Rec = Inferred_True_group / True_group_groudtruth
    
    if (group_Pre + group_Rec) > 0:
        group_F1 = (2 * group_Pre * group_Rec) / (group_Pre + group_Rec)
    else:
        group_F1 = 0

    no_Average_Pre = Average_Pre
    no_Average_Rec = Average_Rec
    no_F1_score = F1_score

    # with open(config.Evaluation_Res, "a") as file:
    logging.info("\n\n\Semantic-Type Evaluation Part For ChatPre-repartition(no validation)---------------------------------\n")
    logging.info(f"no_Average_Pre:{Average_Pre}\n")
    logging.info(f"no_Average_Rec:{Average_Rec}\n")
    logging.info(f"no_F1_score:{F1_score}\n")

    logging.info(f"\nno_static_Pre:{static_Pre}\n")
    logging.info(f"no_static_Rec:{static_Rec}\n")
    logging.info(f"no_static_F1:{static_F1}\n")
    logging.info(f"no_static_groudtruth:{static_groudtruth}\n")

    logging.info(f"\nno_integer_Pre:{integer_Pre}\n")
    logging.info(f"no_integer_Rec:{integer_Rec}\n")
    logging.info(f"no_integer_F1:{integer_F1}\n")
    logging.info(f"no_integer_groudtruth:{integer_groudtruth}\n") 

    logging.info(f"\nno_group_Pre:{group_Pre}\n")
    logging.info(f"no_group_Rec:{group_Rec}\n")
    logging.info(f"no_group_F1:{group_F1}\n")
    logging.info(f"no_group_groudtruth:{group_groudtruth}\n") 

    logging.info(f"\nno_bytes_Pre:{bytes_Pre}\n")
    logging.info(f"no_bytes_Rec:{bytes_Rec}\n")
    logging.info(f"no_bytes_F1:{bytes_F1}\n")
    logging.info(f"no_bytes_groudtruth:{bytes_groudtruth}\n") 

    logging.info(f"\nno_string_Pre:{string_Pre}\n")
    logging.info(f"no_string_Rec:{string_Rec}\n")
    logging.info(f"no_string_F1:{string_F1}\n")
    logging.info(f"no_string_groudtruth:{string_groudtruth}\n") 


         

    logging.info("\n\n\nSemantic-Types Evaluation Part For ChatPre-repartition(Validated)---------------------------------")
    

    '''Semantic-Type'''
    semantic_usedPre,msg_Pre, msg_Rec =0,0,0

    # msg_semanticTruth
    True_static_groudtruth = 0
    static_groudtruth = set()
    True_bytes_groudtruth = 0
    bytes_groudtruth = set()
    True_string_groudtruth = 0
    string_groudtruth = set()
    True_integer_groudtruth = 0
    integer_groudtruth = set()
    True_group_groudtruth = 0
    group_groudtruth = set()

    Inferred_True_static = 0
    Inferred_True_bytes = 0
    Inferred_True_string = 0
    Inferred_True_integer = 0
    Inferred_True_group = 0
    
    Inferred_static = 0
    Inferred_bytes = 0
    Inferred_string = 0
    Inferred_integer = 0
    Inferred_group = 0

    for i in range(0,len(payload_message)):
        msg_i = payload_message[i]
        msg_len = len(msg_i)
        command_start = int(commandOffset.split(',')[0])
        command_end = int(commandOffset.split(',')[-1])+1
        msg_command = payload_message[i][command_start:command_end]

        if config.evaluation_mode == 'index':
            msg_semanticTruth = Semantic_Groundtruth[i]
        else:
            msg_semanticTruth = Semantic_Groundtruth[msg_command]


        msg_semanticRes = message_Result[i].field_types


        logging.info(f"Msg {i} semantic evaluation:***\n")
        logging.info(f"msg_semanticTruth:{msg_semanticTruth}")
        logging.info(f"msg_semanticRes:{msg_semanticRes}\n")

        msg_pre, msg_rec= metrix_Cal(msg_semanticTruth,msg_semanticRes, message_Result[i].fields, msg_len)
        logging.info(f"msg_pre:{msg_pre}, msg_rec:{msg_rec}\n")
        
        msg_Pre += msg_pre
        msg_Rec += msg_rec



        for f,r in msg_semanticTruth.items():
            if (config.semantic_Types[0] in msg_semanticTruth[f]):
                True_static_groudtruth += 1
                static_groudtruth.add(f)

            if (config.semantic_Types[4] in msg_semanticTruth[f]):
                True_bytes_groudtruth += 1
                bytes_groudtruth.add(f)
            
            if (config.semantic_Types[2] in msg_semanticTruth[f]):
                True_string_groudtruth += 1
                string_groudtruth.add(f)
            
            if (config.semantic_Types[3] in msg_semanticTruth[f]):
                True_integer_groudtruth += 1
                integer_groudtruth.add(f)
            
            if (config.semantic_Types[1] in msg_semanticTruth[f]):
                True_group_groudtruth += 1
                group_groudtruth.add(f)

        for f,r in msg_semanticRes.items():

            if config.semantic_Types[0] in r:
                Inferred_static += 1
                if (f in msg_semanticTruth) and (config.semantic_Types[0] in msg_semanticTruth[f]):
                    Inferred_True_static += 1
            if config.semantic_Types[4] in r:
                Inferred_bytes += 1
                if (f in msg_semanticTruth) and (config.semantic_Types[4] in msg_semanticTruth[f]):
                    Inferred_True_bytes += 1
            
            if config.semantic_Types[2] in r:
                Inferred_string += 1
                if (f in msg_semanticTruth) and (config.semantic_Types[2] in msg_semanticTruth[f]):
                    Inferred_True_string += 1
            if config.semantic_Types[3] in r:
                Inferred_integer += 1
                if (f in msg_semanticTruth) and (config.semantic_Types[3] in msg_semanticTruth[f]):
                    Inferred_True_integer += 1
            if config.semantic_Types[1] in r:
                Inferred_group += 1
                if (f in msg_semanticTruth) and (config.semantic_Types[1] in msg_semanticTruth[f]):
                    Inferred_True_group += 1
        

    Average_Pre = msg_Pre/len(payload_message)
    Average_Rec = msg_Rec/len(payload_message)
    if (Average_Pre + Average_Rec) > 0:
        F1_score = (2 * Average_Pre * Average_Rec) / (Average_Pre + Average_Rec)
    else:
        F1_score = 0
    if Inferred_static >0:
        static_Pre = Inferred_True_static / Inferred_static
    else:
        static_Pre = 0
    
    if (static_Pre + static_Rec) > 0:
        static_F1 = (2 * static_Pre * static_Rec) / (static_Pre + static_Rec)
    else:
        static_F1 = 0
    '''bytes'''
    if Inferred_bytes == 0:
        bytes_Pre = 0
    else:
        bytes_Pre = Inferred_True_bytes / Inferred_bytes
    
    if True_bytes_groudtruth == 0:
        bytes_Rec = 0
    else:
        bytes_Rec = Inferred_True_bytes / True_bytes_groudtruth
    
    if (bytes_Pre + bytes_Rec) > 0:
        bytes_F1 = (2 * bytes_Pre * bytes_Rec) / (bytes_Pre + bytes_Rec)
    else:
        bytes_F1 = 0
    '''string'''
    if Inferred_string == 0:
        string_Pre = 0
    else:
        string_Pre = Inferred_True_string / Inferred_string
    
    if True_string_groudtruth == 0:
        string_Rec = 0
    else:
        string_Rec = Inferred_True_string / True_string_groudtruth
    
    if (string_Pre + string_Rec) > 0:
        string_F1 = (2 * string_Pre * string_Rec) / (string_Pre + string_Rec)
    else:
        string_F1 = 0
    '''integer'''
    if Inferred_integer == 0:
        integer_Pre = 0
    else:
        integer_Pre = Inferred_True_integer / Inferred_integer
    
    if True_integer_groudtruth == 0:
        integer_Rec = 0
    else:
        integer_Rec = Inferred_True_integer / True_integer_groudtruth
    
    if (integer_Pre + integer_Rec) > 0:
        integer_F1 = (2 * integer_Pre * integer_Rec) / (integer_Pre + integer_Rec)
    else:
        integer_F1 = 0

    '''group'''
    if Inferred_group == 0:
        group_Pre = 0
    else:
        group_Pre = Inferred_True_group / Inferred_group
    
    if True_group_groudtruth == 0:
        group_Rec = 0
    else:
        group_Rec = Inferred_True_group / True_group_groudtruth
    
    if (group_Pre + group_Rec) > 0:
        group_F1 = (2 * group_Pre * group_Rec) / (group_Pre + group_Rec)
    else:
        group_F1 = 0

    logging.info(f"Average_Pre:{Average_Pre}")
    logging.info(f"Average_Rec:{Average_Rec}")
    logging.info(f"F1_score:{F1_score}")
    

    


    # with open(config.Evaluation_Res, "a") as file:
    logging.info("\n\n\Semantic-Type Evaluation Part For ChatPre-repartition(Validated)---------------------------------\n")
    logging.info(f"Average_Pre:{Average_Pre}\n")
    logging.info(f"Average_Rec:{Average_Rec}\n")
    logging.info(f"F1_score:{F1_score}\n")

    logging.info(f"\nstatic_Pre:{static_Pre}\n")
    logging.info(f"static_Rec:{static_Rec}\n")
    logging.info(f"static_F1:{static_F1}\n")
    logging.info(f"static_groudtruth:{static_groudtruth}\n")

    logging.info(f"\ninteger_Pre:{integer_Pre}\n")
    logging.info(f"integer_Rec:{integer_Rec}\n")
    logging.info(f"integer_F1:{integer_F1}\n")
    logging.info(f"integer_groudtruth:{integer_groudtruth}\n") 

    logging.info(f"\ngroup_Pre:{group_Pre}\n")
    logging.info(f"group_Rec:{group_Rec}\n")
    logging.info(f"group_F1:{group_F1}\n")
    logging.info(f"group_groudtruth:{group_groudtruth}\n")    

    logging.info(f"\nbytes_Pre:{bytes_Pre}\n")
    logging.info(f"bytes_Rec:{bytes_Rec}\n")
    logging.info(f"bytes_F1:{bytes_F1}\n")
    logging.info(f"bytes_groudtruth:{bytes_groudtruth}\n") 

    logging.info(f"\nstring_Pre:{string_Pre}\n")
    logging.info(f"string_Rec:{string_Rec}\n")
    logging.info(f"string_F1:{string_F1}\n")
    logging.info(f"string_groudtruth:{string_groudtruth}\n") 
    
    return no_Average_Pre, no_Average_Rec, no_F1_score, Average_Pre, Average_Rec, F1_score

            

def ChatPreLLM_Semantic_Functions_Evaluator(payload_message, Pre_message_Result, message_Result, commandOffset):
    logging.info("\n\n\nSemantic-Functions Evaluation Part For ChatPre-repartition(no validation)---------------------------------")
    
    '''Semantic-Function'''
    semantic_usedPre,msg_Pre, msg_Rec =0,0,0

    no_ChatPre_command_count = 0
    no_ChatPre_command_correct = 0

    ChatPre_length_correct = 0
    ChatPre_command_correct = 0
    ChatPre_length_count = 0
    ChatPre_command_count = 0

    True_delim_groudtruth = 0
    Inferred_delim = 0
    Inferred_True_delim = 0
    delim_groudtruth = set()

    True_aligned_groudtruth = 0
    Inferred_aligned = 0
    Inferred_True_aligned = 0
    aligned_groudtruth = set()

    True_filename_groudtruth = 0
    Inferred_filename = 0
    Inferred_True_filename = 0
    filename_groudtruth = set()

    for i in range(0,len(payload_message)):
        msg_i = payload_message[i]
        msg_len = len(msg_i)
        command_start = int(commandOffset.split(',')[0])
        command_end = int(commandOffset.split(',')[-1])+1
        msg_command = payload_message[i][command_start:command_end]

        if config.evaluation_mode == 'index':
            msg_semanticTruth = Semantic_Functions_Groundtruth[i]
            msg_fieldTruth = Semantic_Groundtruth[i]
        else:
            msg_semanticTruth = Semantic_Functions_Groundtruth[msg_command]
            msg_fieldTruth = Semantic_Groundtruth[msg_command]

        msg_semanticRes = Pre_message_Result[i].field_funcs

        for f,r in msg_semanticRes.items():
            if config.semantic_Functions[0] in r:
                no_ChatPre_command_count += 1
                if f == config.commandOffset:
                    no_ChatPre_command_correct += 1


        logging.info(f"Msg {i} semantic evaluation:***\n")
        logging.info(f"msg_semanticTruth:{msg_semanticTruth}")
        logging.info(f"msg_semanticRes:{msg_semanticRes}\n")

        msg_pre, msg_rec= metrix_Cal_Func(msg_semanticTruth,msg_semanticRes, Pre_message_Result[i].fields, msg_len, msg_fieldTruth)
        logging.info(f"msg_pre:{msg_pre}, msg_rec:{msg_rec}\n")
        
        msg_Pre += msg_pre
        msg_Rec += msg_rec
        for f,r in msg_semanticRes.items():
            logging.info(f"f:{f}, r:{r}")
            if config.semantic_Functions[0] in r:
                ChatPre_command_count += 1
                if f == config.commandOffset:
                    ChatPre_command_correct += 1
            if config.semantic_Functions[1] in r:
                ChatPre_length_count += 1
                if f == config.lengthOffset:
                    ChatPre_length_correct += 1
        
        
        
        for f,r in msg_semanticTruth.items():
            if (config.semantic_Functions[2] in msg_semanticTruth[f]):
                True_delim_groudtruth += 1
                delim_groudtruth.add(f)
            if (config.semantic_Functions[4] in msg_semanticTruth[f]):
                True_aligned_groudtruth += 1
                aligned_groudtruth.add(f)
            if (config.semantic_Functions[5] in msg_semanticTruth[f]):
                True_filename_groudtruth += 1
                filename_groudtruth.add(f)


        for f,r in msg_semanticRes.items():

            if config.semantic_Functions[2] in r:
                Inferred_delim += 1
                if (f in msg_semanticTruth) and (config.semantic_Functions[2] in msg_semanticTruth[f]):
                    Inferred_True_delim += 1
            
            if config.semantic_Functions[4] in r:
                Inferred_aligned += 1
                if (f in msg_semanticTruth) and (config.semantic_Functions[4] in msg_semanticTruth[f]):
                    Inferred_True_aligned += 1
            
            if config.semantic_Functions[5] in r:
                Inferred_filename += 1
                if (f in msg_semanticTruth) and (config.semantic_Functions[5] in msg_semanticTruth[f]):
                    Inferred_True_filename += 1

    Average_Pre = msg_Pre/len(payload_message)
    Average_Rec = msg_Rec/len(payload_message)
    if (Average_Pre + Average_Rec) > 0:
        F1_score = (2 * Average_Pre * Average_Rec) / (Average_Pre + Average_Rec)
    else:
        F1_score = 0
    

    logging.info(f"Average_Pre:{Average_Pre}")
    logging.info(f"Average_Rec:{Average_Rec}")
    logging.info(f"F1_score:{F1_score}")

    no_ChatPre_Command_rec = no_ChatPre_command_correct/len(payload_message)
    if no_ChatPre_command_count>0:
        no_ChatPre_Command_pre = no_ChatPre_command_correct / no_ChatPre_command_count
        if (no_ChatPre_Command_pre + no_ChatPre_Command_rec) > 0:
            no_ChatPre_Command_F1 = (2 * no_ChatPre_Command_pre * no_ChatPre_Command_rec) / (no_ChatPre_Command_pre + no_ChatPre_Command_rec)
        else:
            no_ChatPre_Command_F1 = 0
    else:
        no_ChatPre_Command_pre = 0
        no_ChatPre_Command_F1 = 0
    
    ChatPre_Command_rec = ChatPre_command_correct/len(payload_message)
    ChatPre_Length_rec = ChatPre_length_correct/len(payload_message)
    if ChatPre_command_count>0:
        ChatPre_Command_pre = ChatPre_command_correct/ChatPre_command_count
        if (ChatPre_Command_pre + ChatPre_Command_rec) > 0:
            ChatPre_Command_F1 = (2 * ChatPre_Command_pre * ChatPre_Command_rec) / (ChatPre_Command_pre + ChatPre_Command_rec) 
        else:
            ChatPre_Command_F1 = 0
    else:
        ChatPre_Command_pre = 0
        ChatPre_Command_F1 = 0
    if ChatPre_length_count>0:
        ChatPre_Length_pre = ChatPre_length_correct / ChatPre_length_count
        if (ChatPre_Length_pre + ChatPre_Length_rec) > 0:
            ChatPre_Length_F1 = (2 * ChatPre_Length_pre * ChatPre_Length_rec) / (ChatPre_Length_pre + ChatPre_Length_rec)
        else:
            ChatPre_Length_F1 = 0
    else:
        ChatPre_Length_pre = 0
        ChatPre_Length_F1 = 0
    if True_delim_groudtruth > 0:
        ChatPre_Delim_rec = Inferred_True_delim/True_delim_groudtruth
    else:
        ChatPre_Delim_rec = 0
    
    if Inferred_delim > 0:
        ChatPre_Delim_pre = Inferred_True_delim/Inferred_delim
    else:
        ChatPre_Delim_pre = 0
    
    if (ChatPre_Delim_rec + ChatPre_Delim_pre) > 0:
        ChatPre_Delim_F1 = (2 * ChatPre_Delim_rec * ChatPre_Delim_pre) / (ChatPre_Delim_rec + ChatPre_Delim_pre)
    else:
        ChatPre_Delim_F1 = 0
    if True_aligned_groudtruth > 0:
        ChatPre_aligned_rec = Inferred_True_aligned/True_aligned_groudtruth
    else:
        ChatPre_aligned_rec = 0
    
    if Inferred_aligned > 0:
        ChatPre_aligned_pre = Inferred_True_aligned/Inferred_aligned
    else:
        ChatPre_aligned_pre = 0
    
    if (ChatPre_aligned_rec + ChatPre_aligned_pre) > 0:
        ChatPre_aligned_F1 = (2 * ChatPre_aligned_rec * ChatPre_aligned_pre) / (ChatPre_aligned_rec + ChatPre_aligned_pre)
    else:
        ChatPre_aligned_F1 = 0
    if True_filename_groudtruth > 0:
        ChatPre_filename_rec = Inferred_True_filename/True_filename_groudtruth
    else:
        ChatPre_filename_rec = 0
    
    if Inferred_filename > 0:
        ChatPre_filename_pre = Inferred_True_filename/Inferred_filename
    else:
        ChatPre_filename_pre = 0
    
    if (ChatPre_filename_rec + ChatPre_filename_pre) > 0:
        ChatPre_filename_F1 = (2 * ChatPre_filename_rec * ChatPre_filename_pre) / (ChatPre_filename_rec + ChatPre_filename_pre)
    else:
        ChatPre_filename_F1 = 0

    no_Average_Pre = Average_Pre
    no_Average_Rec = Average_Rec
    no_F1_score = F1_score

    # with open(config.Evaluation_Res, "a") as file:
    logging.info("\n\n\Semantic-Function Evaluation Part For ChatPre-repartition(no validation)---------------------------------\n")
    logging.info(f"Average_Pre:{Average_Pre}\n")
    logging.info(f"Average_Rec:{Average_Rec}\n")
    logging.info(f"F1_score:{F1_score}\n\n")
    logging.info(f"no_ChatPre_Command_pre:{no_ChatPre_Command_pre}\n")
    logging.info(f"no_ChatPre_Command_rec:{no_ChatPre_Command_rec}\n")
    logging.info(f"no_ChatPre_Command_F1:{no_ChatPre_Command_F1}\n\n")
    logging.info(f"\n")
    logging.info(f"no_ChatPre_Command_pre:{ChatPre_Command_pre}\n")
    logging.info(f"no_ChatPre_Command_rec:{ChatPre_Command_rec}\n")
    logging.info(f"no_ChatPre_Command_F1:{ChatPre_Command_F1}\n")
    logging.info(f"\nno_ChatPre_Length_pre:{ChatPre_Length_pre}\n")
    logging.info(f"no_ChatPre_Length_rec:{ChatPre_Length_rec}\n")
    logging.info(f"no_ChatPre_Length_F1:{ChatPre_Length_F1}\n")
    logging.info(f"\nno_ChatPre_Delim_pre:{ChatPre_Delim_pre}\n")
    logging.info(f"no_ChatPre_Delim_rec:{ChatPre_Delim_rec}\n")
    logging.info(f"no_ChatPre_Delim_F1:{ChatPre_Delim_F1}\n")
    logging.info(f"no_delim_groudtruth:{delim_groudtruth}\n")
    logging.info(f"\nno_ChatPre_aligned_pre:{ChatPre_aligned_pre}\n")
    logging.info(f"no_ChatPre_aligned_rec:{ChatPre_aligned_rec}\n")
    logging.info(f"no_ChatPre_aligned_F1:{ChatPre_aligned_F1}\n")
    logging.info(f"no_aligned_groudtruth:{aligned_groudtruth}\n")
    logging.info(f"\nno_ChatPre_filename_pre:{ChatPre_filename_pre}\n")
    logging.info(f"no_ChatPre_filename_rec:{ChatPre_filename_rec}\n")
    logging.info(f"no_ChatPre_filename_F1:{ChatPre_filename_F1}\n")
    logging.info(f"no_filename_groudtruth:{filename_groudtruth}\n")

    logging.info("\n\n\nSemantic-Functions Evaluation Part For ChatPre-repartition(Validated)---------------------------------")
    

    '''Semantic-Function'''
    semantic_usedPre,msg_Pre, msg_Rec =0,0,0

    ChatPre_length_correct = 0
    ChatPre_command_correct = 0
    ChatPre_length_count = 0
    ChatPre_command_count = 0

    True_delim_groudtruth = 0
    Inferred_delim = 0
    Inferred_True_delim = 0
    delim_groudtruth = set()

    True_aligned_groudtruth = 0
    Inferred_aligned = 0
    Inferred_True_aligned = 0
    aligned_groudtruth = set()

    True_filename_groudtruth = 0
    Inferred_filename = 0
    Inferred_True_filename = 0
    filename_groudtruth = set()

    for i in range(0,len(payload_message)):
        msg_i = payload_message[i]
        msg_len = len(msg_i)
        command_start = int(commandOffset.split(',')[0])
        command_end = int(commandOffset.split(',')[-1])+1
        msg_command = payload_message[i][command_start:command_end]

        if config.evaluation_mode == 'index':
            msg_semanticTruth = Semantic_Functions_Groundtruth[i]
            msg_fieldTruth = Semantic_Groundtruth[i]
        else:
            msg_semanticTruth = Semantic_Functions_Groundtruth[msg_command]
            msg_fieldTruth = Semantic_Groundtruth[msg_command]

        msg_semanticRes = message_Result[i].field_funcs

        for f,r in msg_semanticRes.items():
            if config.semantic_Functions[0] in r:
                ChatPre_command_count += 1
                if f == config.commandOffset:
                    ChatPre_command_correct += 1
            if config.semantic_Functions[1] in r:
                ChatPre_length_count += 1
                if f == config.lengthOffset:
                    ChatPre_length_correct += 1
        
        for f,r in msg_semanticTruth.items():
            if (config.semantic_Functions[2] in msg_semanticTruth[f]):
                True_delim_groudtruth += 1
                delim_groudtruth.add(f)
            if (config.semantic_Functions[4] in msg_semanticTruth[f]):
                True_aligned_groudtruth += 1
                aligned_groudtruth.add(f)
            if (config.semantic_Functions[5] in msg_semanticTruth[f]):
                True_filename_groudtruth += 1
                filename_groudtruth.add(f)


        for f,r in msg_semanticRes.items():

            if config.semantic_Functions[2] in r:
                Inferred_delim += 1
                if (f in msg_semanticTruth) and (config.semantic_Functions[2] in msg_semanticTruth[f]):
                    Inferred_True_delim += 1
            
            if config.semantic_Functions[4] in r:
                Inferred_aligned += 1
                if (f in msg_semanticTruth) and (config.semantic_Functions[4] in msg_semanticTruth[f]):
                    Inferred_True_aligned += 1
            
            if config.semantic_Functions[5] in r:
                Inferred_filename += 1
                if (f in msg_semanticTruth) and (config.semantic_Functions[5] in msg_semanticTruth[f]):
                    Inferred_True_filename += 1
            

        logging.info(f"Msg {i} semantic evaluation:***\n")
        logging.info(f"msg_semanticTruth:{msg_semanticTruth}")
        logging.info(f"msg_semanticRes:{msg_semanticRes}\n")

        msg_pre, msg_rec= metrix_Cal_Func(msg_semanticTruth,msg_semanticRes, message_Result[i].fields, msg_len, msg_fieldTruth)
        logging.info(f"msg_pre:{msg_pre}, msg_rec:{msg_rec}\n")
        
        msg_Pre += msg_pre
        msg_Rec += msg_rec
        

    Average_Pre = msg_Pre/len(payload_message)
    Average_Rec = msg_Rec/len(payload_message)
    if (Average_Pre + Average_Rec) > 0:
        F1_score = (2 * Average_Pre * Average_Rec) / (Average_Pre + Average_Rec)
    else:
        F1_score = 0
    

    logging.info(f"Average_Pre:{Average_Pre}")
    logging.info(f"Average_Rec:{Average_Rec}")
    logging.info(f"F1_score:{F1_score}")
    
    ChatPre_Command_rec = ChatPre_command_correct/len(payload_message)
    ChatPre_Length_rec = ChatPre_length_correct/len(payload_message)
    if ChatPre_command_count>0:
        ChatPre_Command_pre = ChatPre_command_correct/ChatPre_command_count
        if (ChatPre_Command_pre + ChatPre_Command_rec) > 0:
            ChatPre_Command_F1 = (2 * ChatPre_Command_pre * ChatPre_Command_rec) / (ChatPre_Command_pre + ChatPre_Command_rec) 
        else:
            ChatPre_Command_F1 = 0
    else:
        ChatPre_Command_pre = 0
        ChatPre_Command_F1 = 0
    if ChatPre_length_count>0:
        ChatPre_Length_pre = ChatPre_length_correct / ChatPre_length_count
        if (ChatPre_Length_pre + ChatPre_Length_rec) > 0:
            ChatPre_Length_F1 = (2 * ChatPre_Length_pre * ChatPre_Length_rec) / (ChatPre_Length_pre + ChatPre_Length_rec)
        else:
            ChatPre_Length_F1 = 0
    else:
        ChatPre_Length_pre = 0
        ChatPre_Length_F1 = 0
    if True_delim_groudtruth > 0:
        ChatPre_Delim_rec = Inferred_True_delim/True_delim_groudtruth
    else:
        ChatPre_Delim_rec = 0
    
    if Inferred_delim > 0:
        ChatPre_Delim_pre = Inferred_True_delim/Inferred_delim
    else:
        ChatPre_Delim_pre = 0
    
    if (ChatPre_Delim_rec + ChatPre_Delim_pre) > 0:
        ChatPre_Delim_F1 = (2 * ChatPre_Delim_rec * ChatPre_Delim_pre) / (ChatPre_Delim_rec + ChatPre_Delim_pre)
    else:
        ChatPre_Delim_F1 = 0
    if True_aligned_groudtruth > 0:
        ChatPre_aligned_rec = Inferred_True_aligned/True_aligned_groudtruth
    else:
        ChatPre_aligned_rec = 0
    
    if Inferred_aligned > 0:
        ChatPre_aligned_pre = Inferred_True_aligned/Inferred_aligned
    else:
        ChatPre_aligned_pre = 0
    
    if (ChatPre_aligned_rec + ChatPre_aligned_pre) > 0:
        ChatPre_aligned_F1 = (2 * ChatPre_aligned_rec * ChatPre_aligned_pre) / (ChatPre_aligned_rec + ChatPre_aligned_pre)
    else:
        ChatPre_aligned_F1 = 0
    if True_filename_groudtruth > 0:
        ChatPre_filename_rec = Inferred_True_filename/True_filename_groudtruth
    else:
        ChatPre_filename_rec = 0
    
    if Inferred_filename > 0:
        ChatPre_filename_pre = Inferred_True_filename/Inferred_filename
    else:
        ChatPre_filename_pre = 0
    
    if (ChatPre_filename_rec + ChatPre_filename_pre) > 0:
        ChatPre_filename_F1 = (2 * ChatPre_filename_rec * ChatPre_filename_pre) / (ChatPre_filename_rec + ChatPre_filename_pre)
    else:
        ChatPre_filename_F1 = 0

    logging.info(f"ChatPre_Command_pre:{ChatPre_Command_pre}")
    logging.info(f"ChatPre_Command_rec:{ChatPre_Command_rec}")
    logging.info(f"ChatPre_Length_pre:{ChatPre_Length_pre}")
    logging.info(f"ChatPre_Length_rec:{ChatPre_Length_rec}")

    # with open(config.Evaluation_Res, "a") as file:
    logging.info("\n\n\Semantic-Function Evaluation Part For ChatPre-repartition(Validated)---------------------------------\n")
    logging.info(f"Average_Pre:{Average_Pre}\n")
    logging.info(f"Average_Rec:{Average_Rec}\n")
    logging.info(f"F1_score:{F1_score}\n")
    logging.info(f"\n")
    logging.info(f"ChatPre_Command_pre:{ChatPre_Command_pre}\n")
    logging.info(f"ChatPre_Command_rec:{ChatPre_Command_rec}\n")
    logging.info(f"ChatPre_Command_F1:{ChatPre_Command_F1}\n")
    logging.info(f"\nChatPre_Length_pre:{ChatPre_Length_pre}\n")
    logging.info(f"ChatPre_Length_rec:{ChatPre_Length_rec}\n")
    logging.info(f"ChatPre_Length_F1:{ChatPre_Length_F1}\n")
    logging.info(f"\nChatPre_Delim_pre:{ChatPre_Delim_pre}\n")
    logging.info(f"ChatPre_Delim_rec:{ChatPre_Delim_rec}\n")
    logging.info(f"ChatPre_Delim_F1:{ChatPre_Delim_F1}\n")
    logging.info(f"delim_groudtruth:{delim_groudtruth}\n")
    logging.info(f"\nChatPre_aligned_pre:{ChatPre_aligned_pre}\n")
    logging.info(f"ChatPre_aligned_rec:{ChatPre_aligned_rec}\n")
    logging.info(f"ChatPre_aligned_F1:{ChatPre_aligned_F1}\n")
    logging.info(f"aligned_groudtruth:{aligned_groudtruth}\n")
    logging.info(f"\nChatPre_filename_pre:{ChatPre_filename_pre}\n")
    logging.info(f"ChatPre_filename_rec:{ChatPre_filename_rec}\n")
    logging.info(f"ChatPre_filename_F1:{ChatPre_filename_F1}\n")
    logging.info(f"filename_groudtruth:{filename_groudtruth}\n")

    return no_Average_Pre, no_Average_Rec, no_F1_score, Average_Pre, Average_Rec, F1_score
