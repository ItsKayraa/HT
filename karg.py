import sys

args = {}
nonGivenArgs = []

def main(args: list):
    curArg = ""
    for arg in args:
        if not arg.startswith("--") and arg.startswith("-"):
            argD = arg.strip()[1:]
            curArg = argD
            nonGivenArgs.append(curArg)
        elif arg.startswith("--"):
            argD = arg.strip()[2:]
            curArg = argD
            nonGivenArgs.append(curArg)
        else:
            args[curArg] = arg