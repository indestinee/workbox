#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @import: {{{
import sys, os, time

# }}}


class ColorfulPrint(object):  # {{{

    """Docstring for ColorfulPrint. """

    def __init__(self):
        """nothing needs to be define """
        self.colors = {
            "black": 30,
            "red": 31,
            "green": 32,
            "yellow": 33,
            "blue": 34,
            "magenta": 35,
            "cyan": 36,
            "white": 37,
        }

    def trans(self, *args):
        s = " ".join(map("{}".format, args))
        s = s.replace("(##)", "\033[0m")
        s = s.replace("(#)", "\033[0m")
        for color, value in self.colors.items():
            color_tag = "(#%s)" % color
            s_color_tag = "(#%s)" % color[0]
            s = s.replace(color_tag, "\033[1;%d;m" % value).replace(
                s_color_tag, "\033[1;%d;m" % value
            )
        s = s + "\033[0m"
        return s

    def err(self, *args):
        return self("(#r)[ERR](#)", *args)

    def log(self, *args):
        return self("(#blue)[LOG](#)", *args)

    def wrn(self, *args):
        return self("(#y)[WRN](#)", *args)

    def suc(self, *args):
        return self("(#g)[SUC](#)", *args)

    def __call__(self, *args):
        print(self.trans(*args))


cp = ColorfulPrint()
# }}}


def work_cpp(name, suffix):
    def out_process(ret, _t):  # {{{
        def get_time(t):
            if t < 0.5:
                return "(#g)%.2f ms(#)" % (t * 1000)
            elif t < 1:
                return "(#g)%.2f s(#)" % (t)
            elif t < 5:
                return "(#y)%.2f s(#)" % (t)
            elif t < 60:
                return "(#r)%.2f s(#)" % (t)
            elif t < 3600:
                return "(#r)%dm %ds(#)" % (int(t / 60), int(t % 60))
            else:
                return "(#r)%dh %dm(#)" % (int(t / 3600), int(t / 60 % 60))

        def get_ret(ret):
            if ret == 0:
                return "(#g)0(#)"
            return "(#r)0x%x(#)" % ret

        print("")
        msg = cp.trans(
            "Process returned {}  execution time {}".format(get_ret(ret), get_time(_t))
        )
        cp.log(msg)
        if ret != 0:
            cp.err("(#r)Run Time Error!!! :((#)")
        print("")

    # }}}
    assert os.path.isfile(name), cp.trans("(#r){}(#) not found".format(name))
    _in = name + ".in"
    _out = name + ".out"
    _local = name + ".local_out"
    if os.path.isfile(_in):
        with open(_in, "r") as f:
            data = f.read()

        cp("(#y)-- input", "-" * (32 - 9) + "(#)")
        print(data, end="")
        cp("(#y)--- end", "-" * (32 - 8) + "(#)")
    else:
        _in = None

    if os.path.isfile(_out):
        _t = time.time()
        ret = os.system(
            "./{} > {}.local_out".format(name, name) + " < {}.in".format(name)
            if _in
            else ""
        )
        _t = time.time() - _t
        out_process(ret, _t)
        assert os.path.isfile(_local)
        with open(_local, "r") as f:
            local_ans = f.read().splitlines()
        with open(_out, "r") as f:
            ans = f.read().splitlines()

        _max = max(map(len, local_ans))

        cp("(#y)-- output", "-" * (32 - 10) + "(#)")
        i, j = 0, 0
        n, m = len(local_ans), len(ans)
        mistake = 0
        while i < n or j < m:
            left = local_ans[i] if i < n else ""
            right = ans[j] if j < m else ""
            color = "g" if left == right else "r"
            mistake += 0 if left == right else 1
            left += " " * (_max - len(left))
            cp(
                "(#b)#{0:03} (#{1}){2} (#b)|(#) (#{1}){3}(#)".format(
                    i + 1, color, left, right
                )
            )

            i += 1
            j += 1

        cp("(#y)--- end", "-" * (32 - 8) + "(#)")
        print("")
        if mistake > 0:
            cp.err("{} error(s) found!".format(mistake))
        if n != m:
            cp.err(
                "#lines not match! "
                + "(#b)len(local_ans)(##): (#r){}(##), (#b)len(ans))(##): (#r){}(##)".format(
                    len(local_ans), len(ans)
                )
            )
        if mistake == 0 and n == m:
            cp.suc("ok, ok, all right! :)")
        print("")

    else:
        cp("(#y)-- output", "-" * (32 - 10) + "(#)")
        _t = time.time()
        ret = os.system("./{}".format(name) + " < {}.in".format(name) if _in else "")
        _t = time.time() - _t
        cp("(#y)--- end", "-" * (32 - 8) + "(#)")
        out_process(ret, _t)


if __name__ == "__main__":
    assert len(sys.argv) > 1, cp.err("need at least one argument")

    cp("(#b)-- start", "-" * (64 - 9) + "(#)")
    _t = time.strftime("Date Time: %Y/%m/%d %H:%M:%S", time.localtime())

    cp.log(_t)

    _file = sys.argv[1]
    suffix = _file.split(".")[-1].lower()
    name = ".".join(_file.split(".")[:-1])

    suffixs = {"cpp", "c"}
    assert suffix in suffixs, cp.trans(
        "(#b)suffix(##): (#y){}(##) must in (#b)suffixs(##): (#y){}(##)".format(
            suffix, suffixs
        )
    )
    work_cpp(name, suffix)
    cp("(#b)--- end", "-" * (64 - 8) + "(#)")
