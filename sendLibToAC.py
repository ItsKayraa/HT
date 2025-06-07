funcs = {
    # func:{"dataT":str,"strT":str}
}

curNum = 0
curNumA = 0
usedLines = []


def compLib(file: str):
    global curNum, curNumA
    with open(file) as lib:
        varis = {}
        func = False
        curFunc = ""
        lines = lib.readlines()
        addingData = False
        addingStr = False
        for line in lines:
            argv = line.strip().split()
            if not argv:
                continue
            match argv[0]:
                case "intvar":
                    name = argv[1]
                    value = int(argv[2])
                    varis[name] = value
                case "function":
                    funcName = argv[1]
                    func = True
                    funcs[funcName] = {"dataT": "", "strT": ""}
                    curFunc = funcName
                case "endfunc":
                    func = False
                
                case "recur":
                    curNum -= 1

                case "wved":
                    line = " ".join(argv[1:]).replace("text", f"text{curNum}")
                    funcs[curFunc]["dataT"] += line.strip() + "\n"
                
                case "wvedi":
                    line = " ".join(argv[1:]).replace("len", f"len{curNum}").replace("text", f"text{curNum}")
                    funcs[curFunc]["dataT"] += line.strip() + "\n"
                    curNum += 1
                
                case "os":
                    content = " ".join(line.split()[1:])
                    if content in usedLines:
                        continue
                    print("used: ", usedLines)
                    funcs[curFunc]["strT"] += content + "\n"
                    usedLines.append(content)
                
                case "od":
                    content = line.strip()
                    if content.startswith("od "):
                        content = content[3:].strip()
                    
                    if content in usedLines:
                        continue
                    else:
                        print(usedLines)
                        funcs[curFunc]["dataT"] += content + "\n"
                        usedLines.append(content)

                case "wves":
                    line = " ".join(argv[1:]).replace("text", f"text{curNum}")
                    funcs[curFunc]["strT"] += line.strip() + "\n"
                
                case "wvesi":
                    line = " ".join(argv[1:]).replace("len", f"len{curNum}").replace("text", f"text{curNum}")
                    funcs[curFunc]["strT"] += line.strip() + "\n"
                    curNum += 1
                
                case "wvema":
                    changing = argv[1]
                    typ = argv[2]
                    cn = argv[3]
                    if cn == "A":
                        cn = curNumA
                    else:
                        cn = curNum
                    line = " ".join(argv[4:]).replace(changing, changing + str(cn))
                    funcs[curFunc][typ] += line.strip() + "\n"
                
                case "wvemai":
                    changing = argv[1]
                    typ = argv[2]
                    cn = argv[3]
                    if cn == "A":
                        cn = curNumA
                    else:
                        cn = curNum
                    line = " ".join(argv[4:]).replace(changing, changing + str(cn))
                    funcs[curFunc][typ] += line.strip() + "\n"
                    if argv[3] == "A":
                        curNumA += 1
                    else:
                        curNum += 1
                    
                case "delaylib": # yeah, i wasnt able to cook something in delay.tc so im cooking here
                    typ = argv[1]
                    if typ == "dataT":
                        funcs[curFunc][typ] += f"timespec: dq parameter,0\n"
                    elif typ == "strT":
                        funcs[curFunc][typ] += f"mov rax, 35\nmov rdi, timespec\nxor rsi, rsi\n"

                case "/ad":
                    addingData = not addingData
                case "/astr":
                    addingStr = not addingStr
                case "inc":
                    varis[argv[1]] += 1
                case _:
                    if func:
                        if addingData and argv[0] == "wv":
                            newstr = ""
                            for arg in argv[1:]:
                                if ":" in arg:
                                    prefix, varname = arg.split(":", 1)
                                    value = str(varis.get(varname, f"<UNDEF:{varname}>"))
                                    newarg = f"{prefix}{value}"
                                else:
                                    newarg = arg
                                newstr += newarg + " "
                            funcs[curFunc]["dataT"] += newstr.strip() + "\n"
                        elif addingStr:
                            if addingStr and argv[0] == "wv":
                                newstr = ""
                                for arg in argv[1:]:
                                    if ":" in arg:
                                        prefix, varname = arg.split(":", 1)
                                        value = str(varis.get(varname, f"<UNDEF:{varname}>"))
                                        newarg = f"{prefix}{value}"
                                    else:
                                        newarg = arg
                                    newstr += newarg + " "
                                funcs[curFunc]["strT"] += newstr.strip() + "\n"
                            

import uuid

def proc_nl(code: str):
    if not "%nl" in code:
        return code
    lines = code.split("\n")
    i = 0
    for line in lines:
        if line.startswith("text"):
            parts = " ".join(line.split()[2:]).split("%nl")
            for part in parts:
                lines[i] = line.replace(part, part + '"' + ', 10, "')
        i += 1
    
    outdata = "\n".join(lines)
    print(outdata)
    return outdata.replace("%nl", "")

def funcCall(func: str, parameter: str):
    if func in funcs:
        dataPart = funcs[func]["dataT"]
        textPart = funcs[func]["strT"]

        uniqueID = uuid.uuid4().hex[:32]

        for label in ["text", "len", "timespec"]:
            dataPart = dataPart.replace(f"{label}", f"{label}_{uniqueID}")
            textPart = textPart.replace(f"{label}", f"{label}_{uniqueID}")

        dataPart = proc_nl(dataPart.replace("parameter", parameter))
        textPart = textPart.replace("parameter", parameter)

        return (dataPart, textPart)
    else:
        print(f"Function not found: {func}")
        return ("", "")
