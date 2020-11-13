#!/usr/local/bin/python3
"""Sort srt file by timestamp and add delays."""

import argparse
import re
from eic_utils import colorful_str


def get_args():
    """Setup arguments."""
    parser = argparse.ArgumentParser(description="srt sort")
    parser.add_argument("-f", "--file", required=True, type=str)
    parser.add_argument("-d", "--delay", default=0, type=float)
    parser.add_argument("-o", "--output", type=str, default=None)
    parser.add_argument("--ignore", action="store_true", default=False)
    return parser.parse_args()


class Sentence(object):
    """Setence in each timestap."""

    def __init__(self, time_stamp, text):
        self.time_stamp = time_stamp
        self.text = text


class Srt(object):
    """Srt content."""

    def __init__(self, text, ignore):
        self.ignore = ignore
        self.id_re = re.compile(r"^(\d+)$")
        self.time_stamp = re.compile(
            r"^(\d+):(\d+):(\d+),(\d+) *--> *" r"(\d+):(\d+):(\d+),(\d+)$"
        )
        self.items = self.split(text)

    def match(self, row):
        """Determine row type and extracet content."""
        match = self.id_re.match(row)
        if match is not None:
            return "id", int(match.groups()[0])

        match = self.time_stamp.match(row)

        if match is not None:

            def load_time(ts):
                ts = list(map(int, ts))
                return ts[0] * 3600 + ts[1] * 60 + ts[2] + ts[3] / 1000

            start_time, end_time = map(
                load_time, [match.groups()[:4], match.groups()[-4:]]
            )
            return "time", [start_time, end_time]

        if row.strip() == "":
            return None, None

        return "text", row.strip()

    def split(self, text):
        ignore = True
        """Split text and build srt class."""
        index = 0
        status = 0
        text += "\n\n"
        items = []
        for row_id, row in enumerate(text.split("\n")):
            t, match = self.match(row)
            if t is None:
                if status == 2:
                    items.append(Sentence(time, text))
                    status = 0
                continue

            if status == 0:
                assert ignore or (
                    t == "id" and (index + 1 == match or self.ignore)
                ), colorful_str.err(
                    "row #{}, index not match, expected {} but found {}".format(
                        row_id + 1, index + 1, match
                    )
                )
                index += 1
                status = 1
            elif status == 1:
                assert t == "time", colorful_str.err(
                    "row #{}, timestamp is missing.".format(row_id + 1)
                )
                time = match
                status = 2
                text = []
            elif status == 2:
                assert t == "text", colorful_str.err(
                    "row #{}, text is missing.".format(row_id + 1)
                )
                text.append(match)
        return items

    def sort(self, **kwargs):
        """Inherit 'sort' from class <'list'>."""
        self.items.sort(**kwargs)

    def dump(self, delay=0):
        """Dump srt with time delay."""

        def generate_time_stamp(time):
            return "{:02d}:{:02d}:{:02d},{:03d}".format(
                *list(
                    map(
                        int,
                        [
                            time // 3600,
                            time // 60 % 60,
                            time % 60,
                            round(time * 1000 % 1000),
                        ],
                    )
                )
            )

        results = ""
        for index, sentence in enumerate(self.items):
            results += "{}\n{} --> {}\n{}\n\n".format(
                index + 1,
                generate_time_stamp(sentence.time_stamp[0] + delay),
                generate_time_stamp(sentence.time_stamp[1] + delay),
                "\n".join(sentence.text),
            )
        return results


def test_same(src, dst):
    """Test whether src srt and dst srt are the same."""
    src = src.split("\n")
    dst = dst.split("\n")
    if len(src) != len(dst):
        print(colorful_str.err("row number: {} != {}".format(len(src), len(dst))))
    for i in range(min(map(len, [src, dst]))):
        if src[i] != dst[i]:
            print(
                colorful_str.err(
                    "#{}\n  (#y){}(#)\n  (#b){}(#)".format(i, src[i], dst[i])
                )
            )


def main():
    """Main function."""
    args = get_args()

    assert args.file.lower().endswith("srt"), colorful_str.err(
        "file must end with .srt"
    )

    with open(args.file, "r", encoding="utf-8") as f:
        src = f.read()
        # avoid effect of dark magic of file system
        src = src.replace("\ufeff", "")

    srt = Srt(src, args.ignore)
    test_same(src, srt.dump())

    srt.sort(key=lambda x: x.time_stamp[0])
    dst = srt.dump(delay=args.delay)

    if args.output is None:
        args.output = "{}_{}.srt".format(args.file[:-4], args.delay)

    with open(args.output, "w") as f:
        f.write(dst)


if __name__ == "__main__":
    main()
