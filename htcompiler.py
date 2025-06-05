import sendLibToAC
import os
import sys
import karg

try:
    htInstallPath = open("/usr/share/htip.txt").read()
except:
    htInstallPath = input("Path where HT is installed: ")
dataStr = "section .data\n"
textStr = "section .text\nglobal _start\n"
startLabel = "\n_start:\n"

unc_funcs = {}
compvar = {}
scuts = []

def writeAsm(file: str, output: str, keeptemp: bool, b32: bool):
    global dataStr, textStr, startLabel
    asm_path = f"{file}HTOutputASM.s"
    obj_path = f"{file}HTOutput.o"

    if asm_path in os.listdir(os.pardir(file)):
        asm_path += "INCLUDEDALREADY626262"
    if obj_path in os.listdir(os.pardir(file)):
        obj_path += "INCLUDEDALREADY626262"

    with open(asm_path, "w") as asm:
        asm.write(dataStr)
        asm.write(textStr)
        asm.write(startLabel)

    typ = "elf64"
    if b32:
        typ = "elf32"
    
    os.system(f"nasm -f {typ} {asm_path} -o {obj_path}")

    if keeptemp != True:
        os.system(f"ld {obj_path} -o {output}")
        os.system(f"rm {asm_path}")
        os.system(f"rm {obj_path}")

def onlyLine(line: str, b32: bool):
    global dataStr, startLabel, unc_funcs, compvar, scuts
    argv = line.strip().split()

    match argv[0]:
        case "using":
            lib = htInstallPath + "/" + "lib/" + argv[1]
            scut = lib
            if len(argv) > 2:
                scut = argv[2]
            try:
                sendLibToAC.compLib(lib)
                scuts.append(scut)
            except FileNotFoundError:
                print(f"ERROR: Library not found: {lib}")
                return

        case "libc":
            funcs = argv[1].split(":")
            if len(funcs) < 2:
                print("ERROR: Invalid libc syntax")
                return
            lib = funcs[0]
            libfunc = funcs[1]
            if lib not in scuts:
                print(f"ERROR: Library not imported or found: {lib}")
                return
            parameter = " ".join(argv[2:])
            libreturn = sendLibToAC.funcCall(libfunc, parameter)
            dataStr += libreturn[0]
            startLabel += libreturn[1]

        case "printl":
            if b32:
                sendLibToAC.compLib(f"{htInstallPath}/lib/io32.tc")
            else:
                sendLibToAC.compLib(f"{htInstallPath}/lib/io.tc")
            libreturn = sendLibToAC.funcCall("printl", parameter=" ".join(argv[1:]))
            dataStr += libreturn[0]
            startLabel += libreturn[1]
        
        case "localvar": # DONE
            name, value = argv[1], " ".join(argv[2:])
            try:
                value = float(eval(value))
                compvar[name] = value
            except:
                compvar[name] = value

        case "unc": # DONE
            uncName = argv[1]
            uncVar = argv[2]
            uncFunc = argv[3]
            uncFuncPMS = " ".join(argv[4:])
            unc_funcs[uncName] = {"var": uncVar, "func": uncFunc, "funcpms": uncFuncPMS}

        case "endcode": # DONE
            addEnd()
            writeAsm(file.removesuffix(".ht"), output)
            return

        case "//": # DONE
            pass

        case "/*": # DONE
            comment = True

        case _: # DONE
            if argv[0] in unc_funcs:
                onlyLine(f"{unc_funcs[argv[0]]["func"]} {unc_funcs[argv[0]]["funcpms"]}")
            else:
                print("ERROR: Unknown instruction in line: ", line)
                return

def addEnd(b32: bool): # DONE
    global startLabel
    if b32:
        startLabel += "\nmov eax, 60\nxor edi, edi\nsyscall\n" # / end (full safe)
        return
    startLabel += "\nmov rax, 60\nxor rdi, rdi\nsyscall\n" # / end (full safe)
    return

def startCompile(file: str, output: str, keeptemp: bool, b32: bool):
    global dataStr, startLabel, unc_funcs, compvar, scuts

    with open(file) as fil:
        comment = False
        lines = fil.readlines()
        for line in lines:
            argv = line.strip().split()
            if not argv:
                continue

            if comment:
                if argv[0] == "*\\":
                    comment = False
                continue

            match argv[0]:
                case "using":
                    lib = htInstallPath + "/" + "lib/" + argv[1]
                    scut = lib
                    if len(argv) > 2:
                        scut = argv[2]
                    try:
                        sendLibToAC.compLib(lib)
                        scuts.append(scut)
                    except FileNotFoundError:
                        print(f"ERROR: Library not found: {lib}")
                        return

                case "libc":
                    funcs = argv[1].split(":")
                    if len(funcs) < 2:
                        print("ERROR: Invalid libc syntax")
                        return
                    lib = funcs[0]
                    libfunc = funcs[1]
                    if lib not in scuts:
                        print(f"ERROR: Library not imported or found: {lib}")
                        return
                    parameter = " ".join(argv[2:])
                    libreturn = sendLibToAC.funcCall(libfunc, parameter)
                    dataStr += libreturn[0]
                    startLabel += libreturn[1]
                
                case "localvar":
                    name, value = argv[1], " ".join(argv[2:])
                    try:
                        value = eval(value)
                        compvar[name] = float(value)
                    except:
                        compvar[name] = value

                case "printl": # / shortcut for importing and using library by libc
                    if b32:
                        sendLibToAC.compLib(f"{htInstallPath}/lib/io32.tc")
                    else:
                        sendLibToAC.compLib(f"{htInstallPath}/lib/io.tc")
                    libreturn = sendLibToAC.funcCall("printl", parameter=" ".join(argv[1:]))
                    dataStr += libreturn[0]
                    startLabel += libreturn[1]

                case "unc": # / uncalled
                    uncName = argv[1]
                    uncVar = argv[2]
                    uncFunc = argv[3]
                    uncFuncPMS = " ".join(argv[4:])
                    unc_funcs[uncName] = {"var": uncVar, "func": uncFunc, "funcpms": uncFuncPMS}

                case "endcode":
                    addEnd(b32)
                    writeAsm(file.removesuffix(".ht"), output, keeptemp, b32)
                    print("Compilation finished.")
                    return
                
                case "uselv":
                    cvars = {}
                    i = 1
                    while i < len(argv):
                        if argv[i].lower() == "%endv":
                            break
                        cvars[f"%{i}"] = compvar[argv[i]]
                        i += 1
                    call_line = " ".join(argv[i+1:])
                    for key, value in cvars.items():
                        call_line = call_line.replace(key, str(value))

                    onlyLine(call_line)


                case "//":
                    pass

                case "/*":
                    comment = True

                case _:
                    if argv[0] in unc_funcs:
                        onlyLine(f"{unc_funcs[argv[0]]["func"]} {unc_funcs[argv[0]]["funcpms"].replace("%s", argv[1])}")
                    else:
                        print("ERROR: Unknown instruction in line: ", line)
                        yn = input("ignore? [y/n]").lower()
                        if yn in ["y", "yes"]:
                            continue
                        return

if __name__ == "__main__":

    karg.main(sys.argv)
    sargs = karg.args
    ngargs = karg.nonGivenArgs

    file: str = sargs[""]
    output = file.removesuffix(".ht")
    keeptemp = False
    b32 = False

    if "o" in sargs:
        output = sargs["o"]
    elif "output" in sargs:
        output = sargs["output"]
    
    if "k" in ngargs:
        keeptemp = True
    elif "keeptemp" in ngargs:
        keeptemp = True
    
    if "b32" in ngargs:
        b32 = True


    startCompile(file, output, keeptemp, b32)
