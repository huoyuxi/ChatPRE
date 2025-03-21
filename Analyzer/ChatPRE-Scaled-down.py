import time
import idaapi
import ida_hexrays
import ida_lines
import requests
import idc
import re
import logging
import idautils
import traceback
import json
protocol2analysis = idc.ARGV[1]
using_thread = idc.ARGV[2]
# 配置日志记录
log_path = r"Result\results\ida_analysis_" + protocol2analysis + ".log"
logging.basicConfig(filename=log_path, level=logging.INFO,format='%(asctime)s - %(filename)s:%(lineno)d  - %(message)s')
url127 = 'http://localhost:7777/'
data2save = {}


def extract_visible_strings(binary_string, min_length=2):
    pattern = re.compile(b'[ -~]{' + str(min_length).encode() + b',}')
    visible_strings = pattern.findall(binary_string)
    result = []
    for string in visible_strings:
        try:
            decoded_string = string.decode('ascii')
            result.append(decoded_string)
        except UnicodeDecodeError:
            pass
    return result


def text_field_LLM(A,B):
    result = [-1]
    start = 0
    r = set()
    string_dict = {}
    while start < len(B):
        found = False
        for pattern in A:
            if pattern == "":
                continue
            if B[start:].startswith(pattern):
                if int(start/2)-1 not in result:
                    result.append(int(start/2)-1)
                result.append(int((start+len(pattern))/2-1))
                string_dict[",".join([str(ii) for ii in range(int(start/2),int((start+len(pattern))/2))])] = pattern
                # result.append((int(start/2),)
                for i in range(int(start/2),int((start+len(pattern))/2)):
                    r.add(i)
                start += len(pattern)
                found = True
                break
        if not found:
            start += 2
    return result,r,string_dict

# 实现并查集类
class UnionFind:
    def __init__(self):
        self.parent = {}

    def find(self, x):
        if x not in self.parent:
            self.parent[x] = x
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            self.parent[root_x] = root_y
    
    def clear(self):
        self.parent = {}
def get_global_vars():
    global_vars = {}
    # 获取全局变量的数量
    nlist_size = idaapi.get_nlist_size()
    logging.info(f"Total global variables: {nlist_size}")

    # 遍历全局变量
    logging.info("Global Variables:")
    for i in range(nlist_size):
        try:
            # 获取全局变量的地址
            ea = idaapi.get_nlist_ea(i)
            if ea == idc.BADADDR:
                continue

            # 获取全局变量的名称
            name = idaapi.get_nlist_name(i)
            if not name:
                name = "Unnamed"

            # 获取全局变量的类型信息
            tinfo = idaapi.tinfo_t()
            if idaapi.get_tinfo(tinfo, ea):
                type_name = tinfo.get_type_name()
            else:
                type_name = "Unknown"
            global_vars[name] = type_name
            # 打印全局变量信息
            logging.info(f"  Address: 0x{ea:X}, Name: {name}, Type: {type_name}")
        except Exception as e:
            logging.error(f"Error processing global variable at index {i}: {e}")
    return global_vars

def get_function_offset(function_name):
    # 遍历所有函数
    for func_ea in idautils.Functions():
        # 获取当前函数的名称
        current_name = idaapi.get_func_name(func_ea)
        if current_name == function_name:
            # 获取程序基地址
            # base_address = idaapi.get_imagebase()
            # # 计算函数偏移
            # offset = func_ea - base_address
            # return offset
            return func_ea
    return None

def find_address_in_pseudocode(target_addr):
    """Match a disassembly address to the corresponding pseudocode line."""
    try:
        # Get the function containing the target address
        func = idaapi.get_func(target_addr)
        if not func:
            logging.info(f"No function found containing address {hex(target_addr)}")
            raise ValueError(f"No function found containing address {hex(target_addr)}")

        # Decompile the function
        decompiled = ida_hexrays.decompile(func.start_ea)
        if not decompiled:
            logging.info(f"Failed to decompile function at {hex(func.start_ea)}")
            raise ValueError(f"Failed to decompile function at {hex(func.start_ea)}")

        # Get the pseudocode
        pseudocode = decompiled.get_pseudocode()
        item = decompiled.body.find_closest_addr(target_addr)
        # logging.info(item)
        coord = decompiled.find_item_coords(item)
        col = coord[0]
        row = coord[1]
        if row < len(pseudocode):
            clean_line = ida_lines.tag_remove(pseudocode[row].line)
            logging.info(f"Pseudocode line: {clean_line}")
            return clean_line
        logging.info(f"Address {hex(target_addr)} not found in pseudocode.")
        raise ValueError(f"Address {hex(target_addr)} not found in pseudocode.")
    except Exception as e:
        logging.info(f"An error occurred: {e}")
        return None

def extract_info_from_file(info_dict,baseaddress):
    result = {}
    for message in info_dict:
        result[message] = {}
        lines = info_dict[message]
        for line in lines:
            if line.startswith("Instruction"):
                try:
                    # 分割行数据
                    parts = line.strip().split()
                    # 提取偏移地址
                    address = parts[1].rstrip(':')
                    # 提取汇编指令
                    parts = line.strip().split("\t")
                    # 提取线程信息
                    thread = parts[1]
                    # 提取污点源（这里跳过）
                    offsets = parts[2]
                    offsets = [int(i) for i in offsets.replace(",", ";").split(";") if i != ""]
                    # 提取汇编操作数
                    operands = ' '.join(parts[3:])

                    # 如果线程信息不在结果字典中，添加该线程
                    if thread not in result[message]:
                        result[message][thread] = {}
                    # 将地址和汇编操作数添加到对应线程的字典中
                    for offset in offsets:
                        if offset not in result[message][thread]:
                            result[message][thread][offset] = {}
                        result[message][thread][offset][hex(int(address,16) - baseaddress)] = operands
                except Exception as e:
                    logging.error(f"Error processing line '{line}': {e}")
    return result

def jaccard_similarity(set1, set2):
    """
    计算两个集合的 Jaccard 相似度
    """
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    if union == 0:
        return 0
    return intersection / union
def get_bss_global_vars():
    bss_vars = []
    # 遍历所有段
    for seg_ea in idautils.Segments():
        seg_name = idc.get_segm_name(seg_ea)
        # 找到 BSS 段
        if seg_name == ".bss":
            seg_end = idc.get_segm_end(seg_ea)
            # 遍历 BSS 段内的地址
            for ea in range(seg_ea, seg_end):
                # 获取变量名
                var_name = idc.get_name(ea)
                if var_name:
                    # 获取变量类型信息
                    tinfo = idaapi.tinfo_t()
                    if idaapi.get_tinfo(tinfo, ea):
                        # 补充 print_tinfo 函数的参数
                        type_str = idaapi.print_tinfo(None, ea, 0, 0, tinfo, None, var_name)
                    else:
                        type_str = "Unknown"
                    # 记录变量信息
                    bss_vars.append((ea, var_name, type_str))
    return bss_vars

def main():
    try:
        # 等待 IDA Pro 的自动分析完成
        logging.info("Waiting for initial analysis to complete...")
        idaapi.auto_wait()  # 等待自动分析结束
        logging.info("Initial analysis completed.")

        # 检查是否传递了参数
        if len(idc.ARGV) > 1:
            arg1 = idc.ARGV[1]  # 获取第一个参数
            arg2 = idc.ARGV[2] 
            logging.info(f"Received argument1: {arg1}")
            logging.info(f"Received argument2: {arg2}")
        else:
            logging.warning("No arguments received.")
        
        # 在这里可以添加更多分析逻辑
        logging.info("Starting analysis...")

        c_code = {}
        c_ea_code = {}
        global_vars = get_global_vars()
        bss_vars = get_bss_global_vars()
        baseaddress = 0
        # response = requests.get(message_url)
        # response.raise_for_status()  # 检查请求是否成功
        # file_content = response.text
        # message_list = file_content.splitlines()

        response = requests.get(url127 + r"PUT_test_" + protocol2analysis + r"/tmp_results/info.txt")
        response.raise_for_status()  # 检查请求是否成功
        file_content = response.text
        file_line_list = file_content.splitlines()
        id = -1
        info_dict = {}
        binary_so = 0
        for i in range(10):
            line = file_line_list[i]
            if "\tenter\tmain" in line:
                main_name = line.split("\t")[-2]
                main_offset = get_function_offset(main_name)
                # main_offset = 0x3ba0
                if main_offset is not None:
                    logging.info(f"The offset address of the function {main_name} is: 0x{main_offset:x}")
                    main_func_str = ((line.split("\t")[-1]).split(",")[0]).replace("(","")
                    main_func_int = int(main_func_str,16)
                    logging.info(f"The base address of the function {main_name} is: 0x{main_func_int:x}")
                    baseaddress = main_func_int - main_offset
                else:
                    logging.info(f"The function named {main_name} was not found.")
                    logging.info(f"Analyze dynamic link libraries instead")
                    binary_so = 1
                    break
        if binary_so:
            for i in range(len(file_line_list)):
                line = file_line_list[i]
                if "\tenter\t" in line:
                    func_name = (line.split("\t")[-2]).split("()")[0]
                    func_offset = get_function_offset(func_name)
                    # main_offset = 0x3ba0
                    if func_offset is not None:
                        logging.info(f"The offset address of the function {func_name} is: 0x{func_offset:x}")
                        func_str = ((line.split("\t")[-1]).split(",")[0]).replace("(","")
                        func_int = int(func_str,16)
                        logging.info(f"The base address of the function {func_name} is: 0x{func_int:x}")
                        baseaddress = func_int - func_offset

        response = requests.get(url127 + r"PUT_test_" + protocol2analysis + r"/hex")
        response.raise_for_status()  # 检查请求是否成功
        file_content = response.text
        message_line_list = file_content.splitlines()
        id = -1 
        for line in message_line_list:
            id += 1
            line = line.replace("\n", "")
            if line != "":
                info_dict[str(id) + ":" + line] = []
                response = requests.get(url127 + r"PUT_test_" + protocol2analysis + r"/" + str(id) + "_tmp_results/info.txt")
                response.raise_for_status()  # 检查请求是否成功
                file_content = response.text
                for info_line in file_content.splitlines():
                    info_dict[str(id) + ":" + line].append(info_line)
        try:
            info_dict = extract_info_from_file(info_dict,baseaddress)
            # 打印结果
            logging.info(f"Extracted information: {info_dict}")
            c_taint_asm_dict = {}
            c_taint_c_dict = {}
            local_vars = {}
            for message in info_dict:
                c_taint_asm_dict[message] = {}
                c_taint_c_dict[message] = {}
                for thread in info_dict[message]:
                    c_taint_asm_dict[message][thread] = {}
                    c_taint_c_dict[message][thread] = {}
                    for offset in info_dict[message][thread]:
                        c_taint_asm_dict[message][thread][offset] = {}
                        c_taint_c_dict[message][thread][offset] = {}
                        for address in info_dict[message][thread][offset]:
                            func = idaapi.get_func(int(address, 16))
                            if not func:
                                logging.warning(f"Function not found at address {address}")
                                continue
                            else:
                                # 获取函数的起始地址
                                func_start_ea = func.start_ea
                                # 根据函数起始地址获取函数名称
                                func_name = idaapi.get_func_name(func_start_ea)
                                if c_code.get(func_name) is None:
                                    try:
                                        # 根据函数名获取函数的C代码
                                        pseudocode = idaapi.decompile(func)
                                        c_code[func_name] = str(pseudocode)
                                    except Exception as e:
                                        logging.error(f"Error decompiling function {func_name}: {e}")
                                # logging.info(f"函数名称: {func_name}")
                                if func_name not in local_vars:
                                    local_vars[func_name] = {}
                                    frame = idaapi.get_frame(func)
                                    frame_size = idaapi.get_frame_size(func)
                                    for i in range(frame_size):
                                        name = idc.get_member_name(frame.id, i)
                                        if name is not None:
                                            if name not in local_vars[func_name]:
                                                local_vars[func_name][name] = {}
                                                local_vars[func_name][name]["start"] = i
                                            local_vars[func_name][name]["end"] = i
                                    logging.info(f"Local variables for {func_name}: {local_vars[func_name]}")
                                if func_name not in c_taint_asm_dict[message][thread][offset]:
                                    c_taint_asm_dict[message][thread][offset][func_name] = set()
                                if func_name not in c_taint_c_dict[message][thread][offset]:
                                    c_taint_c_dict[message][thread][offset][func_name] = set()
                                c_taint_asm_dict[message][thread][offset][func_name].add(idc.generate_disasm_line(int(address, 16), 0))
                                try:
                                    if address not in c_ea_code:
                                        c_ea_code[address] = str(find_address_in_pseudocode(int(address, 16)))
                                    c_taint_c_dict[message][thread][offset][func_name].add(c_ea_code[address])
                                except:
                                    pass
                logging.info(f"{message} c_taint_asm_dict: {c_taint_asm_dict[message]}")
            data2save["msg2asm"] = c_taint_asm_dict
            logging.info(f"local_vars: {local_vars}")
            data2save["cfunc"] = c_code
            logging.info(f"c_code: {str(c_code)}")
        except requests.RequestException as e:
            logging.error(f"An error occurred while requesting a file{e}")
        except ValueError as e:
            logging.error(f"An error occurred while processing file contents:{e}")
        for message in c_taint_asm_dict:
            try:
                for buf_num in c_taint_asm_dict[message].get(using_thread, {}):
                    for func_name in c_taint_asm_dict[message][using_thread][buf_num]:
                        new_fragments = set()
                        for fragment in c_taint_asm_dict[message][using_thread][buf_num][func_name]:
                            fragment = re.sub(r'[^a-zA-Z0-9_]', ' ', fragment)
                            for word in fragment.split():
                                new_fragments.add(word)
                        c_taint_asm_dict[message][using_thread][buf_num][func_name] = new_fragments
                logging.info(f"{message} Updated c_taint_asm_dict: {c_taint_asm_dict[message]}")
            except Exception as e:
                logging.error(f"Error processing c_taint_asm_dict: {e}")


        # 打印结果
        if bss_vars:
            # logging.info("BSS 段的全局变量信息：")
            for ea, var_name, type_str in bss_vars:
                global_vars[var_name] = type_str
                # logging.info(f"bss:{ea:016X} {var_name} ({type_str})")
                logging.info(f"bss:{ea:016X} {var_name} ({type_str})")
        # else:
        #     logging.info("未找到 BSS 段的全局变量。")


        keys = list(global_vars.keys())

        # 遍历键的副本
        for var in keys:
            try:
                # 生成新的键
                new_var = re.sub('\.', '_', var)
                # 将原键对应的值赋给新键
                global_vars[new_var] = global_vars[var]
                # 如果新键和原键不同，删除原键
                if new_var != var:
                    del global_vars[var]
            except Exception as e:
                logging.error(f"Error modifying global variable key {var}: {e}")
        for message in c_taint_asm_dict:
            data2save[message] = {}
            var_flow = {}
            for thread in c_taint_asm_dict[message]:
                var_flow[thread] = {}
                for buf_num in c_taint_asm_dict[message].get(using_thread, {}):
                    var_flow[thread][buf_num] = set()
                    for func_name in c_taint_asm_dict[message][using_thread][buf_num]:
                        for word in c_taint_asm_dict[message][using_thread][buf_num][func_name]:
                            if local_vars[func_name].get(word) is not None:
                                var_flow[thread][buf_num].add(func_name + ":" + word)
                            elif global_vars.get(word) is not None:
                                var_flow[thread][buf_num].add("global:" + word)
            # var_len = 0
            # for thread in var_flow:
            #     for buf_num in var_flow[thread]:
            #         var_len += len(var_flow[thread][buf_num])
            # if var_len < len(var_flow[thread]) or var_len == 0:
                # logging.info(f"var info can't be extracted by asm")
            logging.info(f"{c_taint_c_dict[message]}")

            try:
                for buf_num in c_taint_c_dict[message].get(using_thread, {}):
                    for func_name in c_taint_c_dict[message][using_thread][buf_num]:
                        new_fragments = set()
                        for fragment in c_taint_c_dict[message][using_thread][buf_num][func_name]:
                            fragment = re.sub(r'[^a-zA-Z0-9_]', ' ', fragment)
                            for word in fragment.split():
                                new_fragments.add(word)
                        c_taint_c_dict[message][using_thread][buf_num][func_name] = new_fragments
                logging.info(f"{message} Updated c_taint_c_dict: {c_taint_c_dict[message]}")
            except Exception as e:
                logging.error(f"Error processing c_asm_dict: {e}")
            # var_flow = {}
            for thread in c_taint_c_dict[message]:
                # var_flow[thread] = {}
                for buf_num in c_taint_c_dict[message].get(using_thread, {}):
                    if buf_num not in var_flow[thread]:
                        var_flow[thread][buf_num] = set()
                    for func_name in c_taint_c_dict[message][using_thread][buf_num]:
                        for word in c_taint_c_dict[message][using_thread][buf_num][func_name]:
                            if local_vars[func_name].get(word) is not None:
                                var_flow[thread][buf_num].add(func_name + ":" + word)
                            elif global_vars.get(word) is not None:
                                var_flow[thread][buf_num].add("global:" + word)
                            elif re.match(r'v\d+', word) or re.match(r'a\d+', word):
                                var_flow[thread][buf_num].add(func_name + ":" + word)
            logging.info(f"{message} var_flow: {var_flow}")
            data2save[message]["vars"] = var_flow[thread]
            # 遍历字典，计算相似性
            sub_dict = var_flow.get(using_thread, {})
            keys = list(sub_dict.keys())
            similarity_matrix = {}
            for i in range(len(keys)-1):
                j = i + 1
                key1 = keys[i]
                key2 = keys[j]
                set1 = sub_dict[key1]
                set2 = sub_dict[key2]
                similarity = jaccard_similarity(set1, set2)
                similarity_matrix[(key1, key2)] = similarity

            # 输出相似性矩阵
            for pair, sim in similarity_matrix.items():
                if sim == 1:
                    logging.info(f"Key pair {pair}: Similarity = {sim}")
            iduf = set()
            # 创建并查集实例
            uf = UnionFind()
            logging.info(f"{message} Similarity matrix: {similarity_matrix}")
            # 仅合并相似度一致元素对
            for pair, similarity in similarity_matrix.items():
                if similarity == 1:
                    uf.union(pair[0], pair[1])
                    iduf.add(pair[0])
                    iduf.add(pair[1])

            # 确保 0 - 11 所有元素都在并查集中
            all_elements = [item for item in info_dict[message].get(using_thread, {})]
            for element in all_elements:
                uf.find(element)
                # if element not in iduf:
                #     if element + 1 in var_flow[using_thread]:
                #         if var_flow[using_thread][element] <= var_flow[using_thread][element+1] or var_flow[using_thread][element] >= var_flow[using_thread][element+1]:
                #             uf.union(element, element+1)
                #             continue
                #     if element - 1 in var_flow[using_thread]:
                #         if var_flow[using_thread][element] <= var_flow[using_thread][element-1] or var_flow[using_thread][element] >= var_flow[using_thread][element-1]:
                #             uf.union(element-1, element)
                #             continue

            # 构建新的合并后的队列
            merged_queue = []
            root_groups = {}
            for element in all_elements:
                root = uf.find(element)
                if root not in root_groups:
                    root_groups[root] = set()
                root_groups[root].add(element)
            uf.clear()
            for group in root_groups.values():
                sorted_group = tuple(sorted(group))
                merged_queue.append(sorted_group)

            # 对最终结果按元组第一个元素排序
            merged_queue.sort(key=lambda x: int(x[0]))
            logging.info(f"{message} Merged queue: {merged_queue}")
            used_fields = []
            for offsets in merged_queue:
                start = int(offsets[0])
                end = int(offsets[-1])
                used_fields.append(",".join([str(i) for i in range(start,end+1)]) )
            logging.info(f"{message} used_fields: {used_fields}")
            data2save[message]["fields"] = merged_queue
            data_new = {}
            field_type = {}
            field_func = {}
            for offsets in merged_queue:
                data_temp = set()
                for pair in offsets:
                    if pair not in var_flow.get(using_thread, {}):
                        continue
                    data_temp = data_temp | var_flow[using_thread][pair]
                data_new[offsets] = {}
                for item in data_temp:
                    if item.split(':')[0] not in data_new[offsets]:
                        data_new[offsets][item.split(':')[0]] = []
                    data_new[offsets][item.split(':')[0]].append(item.split(':')[1])
            logging.info(f"{message} data_new: {data_new}") 
            data2save[message]["finall"] = data_new
            deli_field = []
            for i in range(int(len(message.split(":")[1])/2)-1):
                # logging.info(f"{message[i*2:i*2+4]} i: {i}")
                if (message.split(":")[1])[i*2:i*2+4] == "0d0a":
                    deli_field.append(str(i)+"," +str(i+1))
            for offsets in data_new:
                if data_new[offsets] == {}:
                    continue
                # logging.info(f"AAA{message}CCC")
                # packet_hex_offset = str(bytes.fromhex((message.split(":")[-1])[offsets[0]*2:offsets[-1]*2+1]))
                # problem_description = f"I'm currently handling a protocol packet received through the socket.recv function. When analyzing the received protocol packet '{packet_hex}', I found that the field at the offset of {offsets} '{packet_hex_offset}' has some situations that affect the operation of the relevant code" + "\n"
                problem_description = f"I'm currently handling a protocol packet received through the socket.recv function. When analyzing the received protocol packet, I found that the field at the offset of {offsets}  has some situations that affect the operation of the relevant code" + "\n"
                for func in data_new[offsets]:
                    if not func.startswith('global'):
                        problem_description += f"""
                        Function Name: {func}
                        Function Function Overview: [Briefly describe the main function of the function, such as receiving and processing a protocol packet from a socket, etc.]
                        {c_code[func]}
                        """
                local_var = []
                global_var = []
                for func in data_new[offsets]:
                    if func == 'global':
                        global_var = data_new[offsets][func]
                    else:
                        local_var += data_new[offsets][func]
                problem_description += f"""        
                During the execution of the function, I noticed that the fields at the offsets {offsets} appear to "contaminate" the global variables {', '.join(global_var)} and local variables {', '.join(local_var)}. The "contamination" is characterized by [Describe in detail the abnormal situation of the variable value, such as the variable value not meeting expectations, or unexplained changes, etc.].

                I suspect that the fields at the offsets {offsets} have specific types and meanings. Based on the code's processing logic, what are the most likely types and meanings of these fields? For instance, the fields at (offset_n, offset_m) could be 16 - byte unsigned numbers, and since they are related to length combination in the code, I speculate that they might represent lengths.

                The types for classification include static text, command groups, strings, integers, decimals, and binary. The semantic categories include commands, lengths, delimiters, checksums, file names, etc.

                Please provide your answer in the following Python - style format, separating the type and meaning with a comma.Remember that these offsets are a field and you only need to answer one line:
                ```python
                int, length
                ```
                """

                url = "https://api.siliconflow.cn/v1/chat/completions"

                payload = {
                    "model": "Qwen/Qwen2.5-7B-Instruct",
                    "messages": [
                        {
                            "role": "user",
                            "content": f"{problem_description}"
                        }
                    ],
                    "stream": False,
                    "max_tokens": 4096,
                    "stop": ["null"],
                    "temperature": 0.7,
                    "top_p": 0.7,
                    "top_k": 50,
                    "frequency_penalty": 0.5,
                    "n": 1,
                    "response_format": {"type": "text"},
                    "tools": [
                        {
                            "type": "function",
                            "function": {
                                "description": "<string>",
                                "name": "<string>",
                                "parameters": {},
                                "strict": False
                            }
                        }
                    ]
                }
                headers = {
                    "Authorization": "Bearer <Token>",
                    "Content-Type": "application/json"
                }

                logging.info(f"{message} Sending request to {url} with payload: {payload}")
                response = requests.request("POST", url, json=payload, headers=headers)
                result = response.json()['choices'][0]['message']['content'].strip()
                logging.info(f"{message} Response result: {result}")
                time.sleep(2)
                try:
                    field_type_func = re.findall(r"```python(.*?)```", result, re.DOTALL)[0]
                    field_type_func = field_type_func.split('\n')
                    start = int(offsets[0])
                    end = int(offsets[-1])
                    field_func[",".join([str(i) for i in range(start,end+1)])] = []
                    field_type[",".join([str(i) for i in range(start,end+1)])] = []
                    for item in field_type_func:
                        if len(item.split(", "))>1:
                            field_func[",".join([str(i) for i in range(start,end+1)])].append(item.split(", ")[1])
                            field_type[",".join([str(i) for i in range(start,end+1)])].append(item.split(", ")[0])
                            break
                except:
                    continue
            logging.info(f"{message} field_type: {field_type}")
            logging.info(f"{message} field_func: {field_func}")
            stringlist = extract_visible_strings(bytes.fromhex(message.split(":")[1]))
            problem_description = f"""
            You are provided with a list named {stringlist} that contains visible strings. Your task is to analyze these strings. If the strings have specific meanings and can be further divided, please present the division results in a Python code block. Each part of the result should be separated by a comma.
            The types of granularity for division include static text, command groups, strings, integers, decimals, and binary. The semantic granularity includes commands, lengths, delimiters, checksums, file names, etc.
            Here is an example: If the input is ["POST /path HTTP/1.1"], the correct output should be
            ```python
            POST, group, command
             , string, delimiter
            /path, string, file
            HTTP/1.1, static, static
            ```
            If you don't think these strings have a specific meaning, just answer ```python ```
            """
            url = "https://api.siliconflow.cn/v1/chat/completions"

            payload = {
                "model": "Qwen/Qwen2.5-7B-Instruct",
                "messages": [
                    {
                        "role": "user",
                        "content": f"{problem_description}"
                    }
                ],
                "stream": False,
                "max_tokens": 4096,
                "stop": ["null"],
                "temperature": 0.7,
                "top_p": 0.7,
                "top_k": 50,
                "frequency_penalty": 0.5,
                "n": 1,
                "response_format": {"type": "text"},
                "tools": [
                    {
                        "type": "function",
                        "function": {
                            "description": "<string>",
                            "name": "<string>",
                            "parameters": {},
                            "strict": False
                        }
                    }
                ]
            }
            headers = {
                "Authorization": "Bearer <Token>",
                "Content-Type": "application/json"
            }

            logging.info(f"{message} Sending request to {url} with payload: {payload}")
            response = requests.request("POST", url, json=payload, headers=headers)
            result = response.json()['choices'][0]['message']['content'].strip()
            logging.info(f"{message} Response result: {result}")
            time.sleep(2)
            try:
                csv = re.findall(r"```python(.*)```", result, re.DOTALL)[0]
            except:
                logging.info(f"{message} used_fields_llm: {used_fields}")
                logging.info(f"{message} field_llm_type_llm: {field_type}")
                logging.info(f"{message} field_llm_Sem_llm: {field_func}")
                continue
            csv = csv.replace('"',"").split("\n")
            field_llm_type = {}
            field_llm_Sem = {}
            for i in range(len(csv)):
                if csv[i] == "":
                    continue
                if len(csv[i].split(", "))== 3:
                    if field_llm_type.get(csv[i].split(", ")[0]) is  None:
                        field_llm_type[csv[i].split(", ")[0]] = set()
                        field_llm_Sem[csv[i].split(", ")[0]] = set()
                    field_llm_type[csv[i].split(", ")[0]].add(csv[i].split(", ")[1])
                    field_llm_Sem[csv[i].split(", ")[0]].add(csv[i].split(", ")[2])
            logging.info(f"{message} field_llm_type: {field_llm_type}")
            logging.info(f"{message} field_llm_Sem: {field_llm_Sem}")
            if field_llm_type == {}:
                logging.info(f"{message} used_fields_llm: {used_fields}")
                logging.info(f"{message} field_llm_type_llm: {field_type}")
                logging.info(f"{message} field_llm_Sem_llm: {field_func}")
                continue
            split_keys = list(field_llm_type.keys())
            split_keys.sort(key=len, reverse=True)
            split_keys = [''.join(f'{ord(char):02x}' for char in input_str) for input_str in split_keys]
            length_text = 0
            for i in range(len(stringlist)):
                length_text+=len(stringlist[i])
            LLM_field,text_set,string_dict = text_field_LLM(split_keys,message.split(":")[1])
            logging.info(f"{message} LLM_field_string: {LLM_field}")
            logging.info(f"{message} string_dict: {string_dict}")
            if string_dict == {}:
                logging.info(f"{message} used_fields_llm: {used_fields}")
                logging.info(f"{message} field_llm_type_llm: {field_type}")
                logging.info(f"{message} field_llm_Sem_llm: {field_func}")
                continue
            for i in range(int(len(message.split(":")[1])/2)):
                if i not in text_set and i not in LLM_field:
                    if "," + str(i) + "'" in str(used_fields) or "'" + str(i) + "'" in str(used_fields):
                        LLM_field.append(i)
            for deli in deli_field:
                start_deli = int(deli.split(",")[0])
                end_deli = int(deli.split(",")[1])
                if end_deli not in LLM_field:
                    LLM_field.append(end_deli)
                if start_deli - 1 not in LLM_field:
                    LLM_field.append(start_deli-1)
                if start_deli in LLM_field:
                    LLM_field.remove(start_deli)
            logging.info(f"{message} LLM_field_deli: {deli_field}")
            LLM_field.sort( reverse = False )
            used_fields = []
            for i in range(1,len(LLM_field)):
                if ",".join(str(j) for j in range(int(LLM_field[i-1])+1,int(LLM_field[i])+1)) == "":
                    continue
                used_fields.append(",".join(str(j) for j in range(int(LLM_field[i-1])+1,int(LLM_field[i])+1)))
            logging.info(f"{message} LLM_field_LLM: {LLM_field}")
            logging.info(f"{message} used_fields_llm: {used_fields}")
            field_llm_type_llm = {} 
            field_llm_Sem_llm = {}
            for item in used_fields:
                if item in string_dict:
                    for str2type in field_llm_type:
                        if ''.join(f'{ord(char):02x}' for char in str2type) == string_dict[item]:
                            field_llm_type_llm[item] = [" ".join([type for type in field_llm_type[str2type]])]
                            field_llm_Sem_llm[item] = [" ".join([sem for sem in field_llm_Sem[str2type]])]
                            # logging.info(f"{message} ### {str2type} {string_dict[item]} {item}")
                            continue
                if item in field_llm_type_llm:
                    continue
                if item in deli_field:
                    field_llm_type_llm[item] = ["Static"]
                    field_llm_Sem_llm[item] = ["Delim"]
                    continue
                for ty in field_type:
                    if item in ty:
                        field_llm_type_llm[item] = field_type[ty]
                        field_llm_Sem_llm[item] = field_func[ty]
                        continue
                if item in field_llm_type_llm:
                    continue
                else:
                    field_llm_type_llm[item] = ["None"]
                    field_llm_Sem_llm[item] = ["None"]
            logging.info(f"{message} field_llm_type_llm: {field_llm_type_llm}")
            logging.info(f"{message} field_llm_Sem_llm: {field_llm_Sem_llm}")
        logging.info("Analysis completed successfully.")
        # with open(r"C:\Users\Administrator\Desktop\reverse\results\\" + protocol2analysis + ".json", "w") as f:
        #     json.dump(data2save, f, indent=4)
    except Exception as e:
        # 获取异常的堆栈信息
        tb = traceback.format_exc()
        # 记录包含行号等详细信息的错误日志
        logging.error(f"An error occurred: {e}\n{tb}")
    finally:
        # 关闭 IDA Pro
        logging.info("Closing IDA Pro...")
        idc.Exit(0)  # 安全退出 IDA Pro

if __name__ == "__main__":
    main()