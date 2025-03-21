protocols = ["ethernet","ftp","http","modbus","s7comm","tftp"]
ff = open(r"Analyzer/ChatPreResult.py","w",encoding="utf-8")
for protocol in protocols:
    ff.write(protocol+"_field_uesd = {}\n")
    ff.write(protocol+"_field_type = {}\n")
    ff.write(protocol+"_field_func = {}\n")
    ff.write(protocol+"_field_uesd_llm = {}\n")
    ff.write(protocol+"_field_type_llm = {}\n")
    ff.write(protocol+"_field_func_llm = {}\n")
    with open(r"results-chatpre/ida_analysis_"+protocol+".log", "r") as f:
        for line in f.readlines():
            line = line.strip()
            if " used_fields: " in line:
                ff.write(protocol+"_field_uesd["+(line.split(" - ")[2]).split(":")[0]+"] = "+line.split(" used_fields: ")[1]+"\n")
            if " field_type: " in line:
                ff.write(protocol+"_field_type["+(line.split(" - ")[2]).split(":")[0]+"] = "+line.split(" field_type: ")[1]+"\n")
            if " field_func: " in line:
                ff.write(protocol+"_field_func["+(line.split(" - ")[2]).split(":")[0]+"] = "+line.split(" field_func: ")[1]+"\n")
            if " used_fields_llm: " in line:
                ff.write(protocol+"_field_uesd_llm["+(line.split(" - ")[2]).split(":")[0]+"] = "+line.split(" used_fields_llm: ")[1]+"\n")
            if " field_llm_type_llm: " in line:
                ff.write(protocol+"_field_type_llm["+(line.split(" - ")[2]).split(":")[0]+"] = "+line.split(" field_llm_type_llm: ")[1]+"\n")
            if " field_llm_Sem_llm: " in line:
                ff.write(protocol+"_field_func_llm["+(line.split(" - ")[2]).split(":")[0]+"] = "+line.split(" field_llm_Sem_llm: ")[1]+"\n")