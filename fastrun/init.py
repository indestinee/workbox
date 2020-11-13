#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import os

compiler = "g++-10"

root = os.path.dirname(__file__)
source = os.path.join(root, "source")
bin = os.path.join(root, "bin")


def run(cmd):
    if isinstance(cmd, list):
        cmd = ";\n".join(cmd)
    print(cmd)
    os.system(cmd)


def main():
    if not os.path.isdir(bin):
        os.makedirs(bin)
    fns = os.listdir(source)
    cmds = []
    cmds.append("cd {}".format(bin))
    cmds.append("rm *")
    for fn in fns:
        name, suffix = fn.split(".")
        if suffix == "cpp":
            cmds.append(
                "{compiler} ../source/{name}.cpp -o {name} -O2 -std=c++11 -Wall".format(
                    name=name,
                    compiler=compiler,
                )
            )
        elif suffix in ["sh", "py"]:
            cmds.append("ln -s ../source/{fn} {name}".format(fn=fn, name=name))
    cmds.append("chmod +x *")
    run(cmds)


if __name__ == "__main__":
    main()
