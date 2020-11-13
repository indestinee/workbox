#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import subprocess
import os, time


def run(cmd):
    print(">>", cmd)
    process = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    result_f = process.stdout
    error_f = process.stderr
    errors = error_f.read()
    if errors:
        print(errors)
        return errors.strip()
    return result_f.read().strip()


items = run("pip3 list").decode("utf-8").split("\n")
for item in items:
    item = item.split(" ")[0].split("\t")[0]
    cmd = "pip3 install {} --upgrade".format(item)

    print(">>", cmd)
    os.system(cmd)

    time.sleep(1)
