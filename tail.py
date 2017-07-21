import os
import sys
import time


class Tail:

    def __init__(self, file_name, line_handler, truncate_handler):
        self._file_name = file_name
        self._line_handler = line_handler
        self._truncate_handler = truncate_handler

    def check_access(self):
        if not os.path.exists(self._file_name):
            raise FileNotFoundError
        elif os.path.isdir(self._file_name):
            raise IsADirectoryError
        elif not os.access(self._file_name, os.R_OK):
            raise PermissionError
        else:
            return 0

    def watch(self, interval):
        try:
            self.check_access()
            fp = open(self._file_name, 'r')

            prev_size = os.path.getsize(self._file_name)
            while True:
                file_size = os.path.getsize(self._file_name)
                if prev_size > file_size:
                    if self._truncate_handler:
                        self._truncate_handler()
                    fp.close()
                    self.check_access()
                    fp = open(self._file_name, 'r')
                    prev_size = 0
                    continue
                fp.seek(prev_size, 0)
                line = fp.readline()
                prev_size = fp.tell()
                if not line:
                    time.sleep(interval)
                elif self._line_handler:
                    self._line_handler(line.rstrip())

        except FileNotFoundError:
            print("File not found: "+self._file_name)
            raise
        except IsADirectoryError:
            print("Is a directory: "+self._file_name)
            raise
        except PermissionError:
            print("Access denied: "+self._file_name)
            raise
        except:
            print("Other error: "+sys.exc_info()[0])
            raise


def main():
    def line_handler(line):
        print(">> "+line)

    def truncate_handler():
        print("File truncated")

    if len(sys.argv) < 2:
        print("Usage: tail.py file")
        exit(1)

    filename = sys.argv[1]

    tail = Tail(filename, line_handler, truncate_handler)
    tail.watch(0.001)


if __name__ == "__main__":
    main()
