# coding: utf-8
"""
参考官方文档：https://docs.python.org/2/library/getopt.html
"""
import sys
import getopt

__version__ = "1.0.0.0"


def usage():
    print("""usage: python getopt-example.py [<options>]
    -h, --help       show docs of help;
    -v, --version    display current version;
    ...
    """)


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:v:p:", ["help", "version"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(2)
    print(opts)
    for o, a in opts:
        if o in ("-v", "--version"):
            print(__version__)
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o == "-p":
            print(a)
            print("print {}".format(a))
        else:
            assert "unhandled option"

if __name__ == "__main__":
    main()
