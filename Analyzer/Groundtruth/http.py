semantic_Types = ['Static', 'Group', 'String', 'Bit Field', 'Bytes']
semantic_Functions = ['Command', 'Length', 'Static', 'CheckSum', 'Aligned', 'Filename']

http_Syntax_Groundtruth = {}

# format1
http_Syntax_Groundtruth[0] = [-1, 2, 3, 4, 5, 13, 15, 19, 21, 30, 32, 42, 44, 55, 57, 63, 65, 68, 70]
http_Syntax_Groundtruth[1] = [-1, 2, 3, 13, 14, 22, 24, 28, 30, 38, 40, 51, 53, 64, 66, 72, 74, 77, 79]
http_Syntax_Groundtruth[2] = [-1, 2, 3, 33, 34, 42, 44, 48, 50, 58, 60, 68, 70, 83, 85, 91, 93, 96, 98]
http_Syntax_Groundtruth[3] = [-1, 2, 3, 4, 5, 13, 15, 19, 21, 30, 32, 42, 44, 55, 57, 63, 65, 81, 83]
http_Syntax_Groundtruth[4] = [-1, 3, 4, 5, 6, 14, 16, 20, 22, 31, 33, 43, 45, 56, 58, 64, 66, 69, 71]

http_lengthOffset = '-1'
http_commandOffset = '0,1,2'

''' Semantic-Type Groundtruth'''
http_Semantic_Groundtruth = {
    0: {
        '0,1,2': semantic_Types[1],  # Group (GET method 属于一组预定义的请求方法集合)
        '3': semantic_Types[0],  # Static (Space 空格是固定格式符号)
        '4': semantic_Types[2],  # String (Path 请求路径是字符串)
        '5': semantic_Types[0],  # Static (Space 空格是固定格式符号)
        '6,7,8,9,10,11,12,13': semantic_Types[0],  # Static (HTTP/1.1 协议版本是固定内容)
        '14,15': semantic_Types[0],  # Static (CRLF 换行符是固定格式符号)
        '16,17,18,19': semantic_Types[1],  # Group (Host 属于一组固定的请求头字段名)
        '20,21': semantic_Types[0],  # Static (Colon 冒号是固定格式符号)
        '22,23,24,25,26,27,28,29,30': semantic_Types[2],  # String (localhost 主机名是字符串)
        '31,32': semantic_Types[0],  # Static (CRLF 换行符是固定格式符号)
        '33,34,35,36,37,38,39,40,41,42': semantic_Types[1],  # Group (User-Agent 属于一组固定的请求头字段名)
        '43,44': semantic_Types[0],  # Static (Colon 冒号是固定格式符号)
        '45,46,47,48,49,50,51,52,53,54,55': semantic_Types[2],  # String (curl/7.68.0 用户代理信息是字符串)
        '56,57': semantic_Types[0],  # Static (CRLF 换行符是固定格式符号)
        '58,59,60,61,62,63': semantic_Types[1],  # Group (Accept 属于一组固定的请求头字段名)
        '64,65': semantic_Types[0],  # Static (Colon 冒号是固定格式符号)
        '66,67,68': semantic_Types[2],  # String (*/* 可接受内容类型是字符串)
        '69,70': semantic_Types[0],  # Static (CRLF 换行符是固定格式符号)
        '71,72': semantic_Types[0]  # Static (CRLF) (End of headers 请求头结束的换行符是固定格式符号)
    },
    1: {
        '0,1,2': semantic_Types[1],  # Group (GET method 属于一组预定义的请求方法集合)
        '3': semantic_Types[0],  # Static (Space 空格是固定格式符号)
        '4,5,6,7,8,9,10,11,12,13': semantic_Types[2],  # String (Path 请求路径是字符串)
        '14': semantic_Types[0],  # Static (Space 空格是固定格式符号)
        '15,16,17,18,19,20,21,22': semantic_Types[0],  # Static (HTTP/1.1 协议版本是固定内容)
        '23,24': semantic_Types[0],  # Static (CRLF 换行符是固定格式符号)
        '25,26,27,28': semantic_Types[1],  # Group (Host 属于一组固定的请求头字段名)
        '29,30': semantic_Types[0],  # Static (Colon 冒号是固定格式符号)
        '31,32,33,34,35,36,37,38': semantic_Types[2],  # String (localhost 主机名是字符串)
        '39,40': semantic_Types[0],  # Static (CRLF 换行符是固定格式符号)
        '41,42,43,44,45,46,47,48,49,50,51': semantic_Types[1],  # Group (User-Agent 属于一组固定的请求头字段名)
        '52,53': semantic_Types[0],  # Static (Colon 冒号是固定格式符号)
        '54,55,56,57,58,59,60,61,62,63,64': semantic_Types[2],  # String (curl/7.68.0 用户代理信息是字符串)
        '65,66': semantic_Types[0],  # Static (CRLF 换行符是固定格式符号)
        '67,68,69,70,71,72': semantic_Types[1],  # Group (Accept 属于一组固定的请求头字段名)
        '73,74': semantic_Types[0],  # Static (Colon 冒号是固定格式符号)
        '75,76,77': semantic_Types[2],  # String (*/* 可接受内容类型是字符串)
        '78,79': semantic_Types[0],  # Static (CRLF 换行符是固定格式符号)
        '80,81': semantic_Types[0]  # Static (CRLF) (End of headers 请求头结束的换行符是固定格式符号)
    },
    2: {
        '0,1,2': semantic_Types[1],  # Group (GET method 属于一组预定义的请求方法集合)
        '3': semantic_Types[0],  # Static (Space 空格是固定格式符号)
        '4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33': semantic_Types[2],  # String (Path with query parameters 带查询参数的请求路径是字符串)
        '34': semantic_Types[0],  # Static (Space 空格是固定格式符号)
        '35,36,37,38,39,40,41,42': semantic_Types[0],  # Static (HTTP/1.1 协议版本是固定内容)
        '43,44': semantic_Types[0],  # Static (CRLF 换行符是固定格式符号)
        '45,46,47,48': semantic_Types[1],  # Group (Host 属于一组固定的请求头字段名)
        '49,50': semantic_Types[0],  # Static (Colon 冒号是固定格式符号)
        '51,52,53,54,55,56,57,58': semantic_Types[2],  # String (localhost 主机名是字符串)
        '59,60': semantic_Types[0],  # Static (CRLF 换行符是固定格式符号)
        '61,62,63,64,65,66,67,68': semantic_Types[1],  # Group (User-Agent 属于一组固定的请求头字段名)
        '69,70': semantic_Types[0],  # Static (Colon 冒号是固定格式符号)
        '71,72,73,74,75,76,77,78,79,80,81,82,83': semantic_Types[2],  # String (curl/7.68.0 用户代理信息是字符串)
        '84,85': semantic_Types[0],  # Static (CRLF 换行符是固定格式符号)
        '86,87,88,89,90,91': semantic_Types[1],  # Group (Accept 属于一组固定的请求头字段名)
        '92,93': semantic_Types[0],  # Static (Colon 冒号是固定格式符号)
        '94,95,96': semantic_Types[2],  # String (*/* 可接受内容类型是字符串)
        '97,98': semantic_Types[0],  # Static (CRLF 换行符是固定格式符号)
        '99,100': semantic_Types[0]  # Static (CRLF) (End of headers 请求头结束的换行符是固定格式符号)
    },
    3: {
        '0,1,2': semantic_Types[1],  # Group (GET method 属于一组预定义的请求方法集合)
        '3': semantic_Types[0],  # Static (Space 空格是固定格式符号)
        '4': semantic_Types[2],  # String (Path 请求路径是字符串)
        '5': semantic_Types[0],  # Static (Space 空格是固定格式符号)
        '6,7,8,9,10,11,12,13': semantic_Types[0],  # Static (HTTP/1.1 协议版本是固定内容)
        '14,15': semantic_Types[0],  # Static (CRLF 换行符是固定格式符号)
        '16,17,18,19': semantic_Types[1],  # Group (Host 属于一组固定的请求头字段名)
        '20,21': semantic_Types[0],  # Static (Colon 冒号是固定格式符号)
        '22,23,24,25,26,27,28,29,30': semantic_Types[2],  # String (localhost 主机名是字符串)
        '31,32': semantic_Types[0],  # Static (CRLF 换行符是固定格式符号)
        '33,34,35,36,37,38,39,40,41,42': semantic_Types[1],  # Group (User-Agent 属于一组固定的请求头字段名)
        '43,44': semantic_Types[0],  # Static (Colon 冒号是固定格式符号)
        '45,46,47,48,49,50,51,52,53,54,55': semantic_Types[2],  # String (curl/7.68.0 用户代理信息是字符串)
        '56,57': semantic_Types[0],  # Static (CRLF 换行符是固定格式符号)
        '58,59,60,61,62,63': semantic_Types[1],  # Group (Accept 属于一组固定的请求头字段名)
        '64,65': semantic_Types[0],  # Static (Colon 冒号是固定格式符号)
        '66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81': semantic_Types[2],  # String (application/json 可接受内容类型是字符串)
        '82,83': semantic_Types[0],  # Static (CRLF 换行符是固定格式符号)
        '84,85': semantic_Types[0]  # Static (CRLF) (End of headers 请求头结束的换行符是固定格式符号)
    },
    4: {
        '0,1,2,3': semantic_Types[1],  # Group (HEAD method 属于一组预定义的请求方法集合)
        '4': semantic_Types[0],  # Static (Space 空格是固定格式符号)
        '5': semantic_Types[2],  # String (Path 请求路径是字符串)
        '6': semantic_Types[0],  # Static (Space 空格是固定格式符号)
        '7,8,9,10,11,12,13,14': semantic_Types[0],  # Static (HTTP/1.1 协议版本是固定内容)
        '15,16': semantic_Types[0],  # Static (CRLF 换行符是固定格式符号)
        '17,18,19,20': semantic_Types[1],  # Group (Host 属于一组固定的请求头字段名)
        '21,22': semantic_Types[0],  # Static (Colon 冒号是固定格式符号)
        '23,24,25,26,27,28,29,30,31': semantic_Types[2],  # String (localhost 主机名是字符串)
        '32,33': semantic_Types[0],  # Static (CRLF 换行符是固定格式符号)
        '34,35,36,37,38,39,40,41,42,43': semantic_Types[1],  # Group (User-Agent 属于一组固定的请求头字段名)
        '44,45': semantic_Types[0],  # Static (Colon 冒号是固定格式符号)
        '46,47,48,49,50,51,52,53,54,55,56': semantic_Types[2],  # String (curl/7.68.0 用户代理信息是字符串)
        '57,58': semantic_Types[0],  # Static (CRLF 换行符是固定格式符号)
        '59,60,61,62,63,64': semantic_Types[1],  # Group (Accept 属于一组固定的请求头字段名)
        '65,66': semantic_Types[0],  # Static (Colon 冒号是固定格式符号)
        '67,68,69': semantic_Types[2],  # String (*/* 可接受内容类型是字符串)
        '70,71': semantic_Types[0],  # Static (CRLF 换行符是固定格式符号)
        '72,73': semantic_Types[0]  # Static (CRLF) (End of headers 请求头结束的换行符是固定格式符号)
    }
}

semantic_Functions = ['Command', 'Length', 'Delim', 'CheckSum', 'Aligned', 'Filename']

http_Semantic_Functions_Groundtruth = {
    0: {
        '0,1,2': semantic_Functions[0],  # Command (GET)
        '3': semantic_Functions[2],  # Delim (Space)
        '4': semantic_Functions[5],  # Filename (Path)
        '5': semantic_Functions[2],  # Delim (Space)
        '6,7,8,9,10,11,12,13': semantic_Functions[2],  # Delim (HTTP/1.1 可看作固定格式部分)
        '14,15': semantic_Functions[2],  # Delim (CRLF)
        '16,17,18,19': semantic_Functions[0],  # Command (Host)
        '20,21': semantic_Functions[2],  # Delim (Colon)
        '22,23,24,25,26,27,28,29,30': semantic_Functions[1],  # Length (localhost)
        '31,32': semantic_Functions[2],  # Delim (CRLF)
        '33,34,35,36,37,38,39,40,41,42': semantic_Functions[0],  # Command (User-Agent)
        '43,44': semantic_Functions[2],  # Delim (Colon)
        '45,46,47,48,49,50,51,52,53,54,55': semantic_Functions[0],  # Command (curl/7.68.0)
        '56,57': semantic_Functions[2],  # Delim (CRLF)
        '58,59,60,61,62,63': semantic_Functions[0],  # Command (Accept)
        '64,65': semantic_Functions[2],  # Delim (Colon)
        '66,67,68': semantic_Functions[5],  # Filename (Path)
        '69,70': semantic_Functions[2],  # Delim (CRLF)
        '71,72': semantic_Functions[2]  # Delim (CRLF) (End of headers)
    },
    1: {
        '0,1,2': semantic_Functions[0],  # Command (GET)
        '3': semantic_Functions[2],  # Delim (Space)
        '4,5,6,7,8,9,10,11,12,13': semantic_Functions[5],  # Filename (Path)
        '14': semantic_Functions[2],  # Delim (Space)
        '15,16,17,18,19,20,21,22': semantic_Functions[2],  # Delim (HTTP/1.1 可看作固定格式部分)
        '23,24': semantic_Functions[2],  # Delim (CRLF)
        '25,26,27,28': semantic_Functions[0],  # Command (Host)
        '29,30': semantic_Functions[2],  # Delim (Colon)
        '31,32,33,34,35,36,37,38': semantic_Functions[1],  # Length (localhost)
        '39,40': semantic_Functions[2],  # Delim (CRLF)
        '41,42,43,44,45,46,47,48,49,50,51': semantic_Functions[0],  # Command (User-Agent)
        '52,53': semantic_Functions[2],  # Delim (Colon)
        '54,55,56,57,58,59,60,61,62,63,64': semantic_Functions[0],  # Command (curl/7.68.0)
        '65,66': semantic_Functions[2],  # Delim (CRLF)
        '67,68,69,70,71,72': semantic_Functions[0],  # Command (Accept)
        '73,74': semantic_Functions[2],  # Delim (Colon)
        '75,76,77': semantic_Functions[5],  # Filename (Path)
        '78,79': semantic_Functions[2],  # Delim (CRLF)
        '80,81': semantic_Functions[2]  # Delim (CRLF) (End of headers)
    },
    2: {
        '0,1,2': semantic_Functions[0],  # Command (GET)
        '3': semantic_Functions[2],  # Delim (Space)
        '4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33': semantic_Functions[5],  # Filename (Path)
        '34': semantic_Functions[2],  # Delim (Space)
        '35,36,37,38,39,40,41,42': semantic_Functions[2],  # Delim (HTTP/1.1 可看作固定格式部分)
        '43,44': semantic_Functions[2],  # Delim (CRLF)
        '45,46,47,48': semantic_Functions[0],  # Command (Host)
        '49,50': semantic_Functions[2],  # Delim (Colon)
        '51,52,53,54,55,56,57,58': semantic_Functions[1],  # Length (localhost)
        '59,60': semantic_Functions[2],  # Delim (CRLF)
        '61,62,63,64,65,66,67,68': semantic_Functions[0],  # Command (User-Agent)
        '69,70': semantic_Functions[2],  # Delim (Colon)
        '71,72,73,74,75,76,77,78,79,80,81,82,83': semantic_Functions[0],  # Command (curl/7.68.0)
        '84,85': semantic_Functions[2],  # Delim (CRLF)
        '86,87,88,89,90,91': semantic_Functions[0],  # Command (Accept)
        '92,93': semantic_Functions[2],  # Delim (Colon)
        '94,95,96': semantic_Functions[5],  # Filename (Path)
        '97,98': semantic_Functions[2],  # Delim (CRLF)
        '99,100': semantic_Functions[2]  # Delim (CRLF) (End of headers)
    },
    3: {
        '0,1,2': semantic_Functions[0],  # Command (GET)
        '3': semantic_Functions[2],  # Delim (Space)
        '4': semantic_Functions[5],  # Filename (Path)
        '5': semantic_Functions[2],  # Delim (Space)
        '6,7,8,9,10,11,12,13': semantic_Functions[2],  # Delim (HTTP/1.1 可看作固定格式部分)
        '14,15': semantic_Functions[2],  # Delim (CRLF)
        '16,17,18,19': semantic_Functions[0],  # Command (Host)
        '20,21': semantic_Functions[2],  # Delim (Colon)
        '22,23,24,25,26,27,28,29,30': semantic_Functions[1],  # Length (localhost)
        '31,32': semantic_Functions[2],  # Delim (CRLF)
        '33,34,35,36,37,38,39,40,41,42': semantic_Functions[0],  # Command (User-Agent)
        '43,44': semantic_Functions[2],  # Delim (Colon)
        '45,46,47,48,49,50,51,52,53,54,55': semantic_Functions[0],  # Command (curl/7.68.0)
        '56,57': semantic_Functions[2],  # Delim (CRLF)
        '58,59,60,61,62,63': semantic_Functions[0],  # Command (Accept)
        '64,65': semantic_Functions[2],  # Delim (Colon)
        '66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81': semantic_Functions[5],  # Filename (Path)
        '82,83': semantic_Functions[2],  # Delim (CRLF)
        '84,85': semantic_Functions[2]  # Delim (CRLF) (End of headers)
    },
    4: {
        '0,1,2,3': semantic_Functions[0],  # Command (HEAD)
        '4': semantic_Functions[2],  # Delim (Space)
        '5': semantic_Functions[5],  # Filename (Path)
        '6': semantic_Functions[2],  # Delim (Space)
        '7,8,9,10,11,12,13,14': semantic_Functions[2],  # Delim (HTTP/1.1 可看作固定格式部分)
        '15,16': semantic_Functions[2],  # Delim (CRLF)
        '17,18,19,20': semantic_Functions[0],  # Command (Host)
        '21,22': semantic_Functions[2],  # Delim (Colon)
        '23,24,25,26,27,28,29,30,31': semantic_Functions[1],  # Length (localhost)
        '32,33': semantic_Functions[2],  # Delim (CRLF)
        '34,35,36,37,38,39,40,41,42,43': semantic_Functions[0],  # Command (User-Agent)
        '44,45': semantic_Functions[2],  # Delim (Colon)
        '46,47,48,49,50,51,52,53,54,55,56': semantic_Functions[0],  # Command (curl/7.68.0)
        '57,58': semantic_Functions[2],  # Delim (CRLF)
        '59,60,61,62,63,64': semantic_Functions[0],  # Command (Accept)
        '65,66': semantic_Functions[2],  # Delim (Colon)
        '67,68,69': semantic_Functions[5],  # Filename (Path)
        '70,71': semantic_Functions[2],  # Delim (CRLF)
        '72,73': semantic_Functions[2]  # Delim (CRLF) (End of headers)
    }
}