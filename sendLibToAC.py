funcs = {
    # func:{"dataT":str,"strT":str}
}

curNum = 0
usedLines = []


def compLib(file: str):
    global curNum
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
                            

def funcCall(func: str, parameter: str):
    if func in funcs:
        dataPart = funcs[func]["dataT"]
        textPart = funcs[func]["strT"]

        dataPart = dataPart.replace("parameter", parameter)
        textPart = textPart.replace("parameter", parameter)

        return (dataPart, textPart)
    else:
        print(f"Function not found: {func}")
        return ("", "")