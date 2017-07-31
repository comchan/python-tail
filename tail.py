import os
import sys
import time


class Tail:

    def __init__(self, file_name, line_handler, truncate_handler, **kwargs):
        self._file_name = file_name
        self._line_handler = line_handler
        self._truncate_handler = truncate_handler
        for kw in kwargs:
            if kw == 'retry':
                self._retry = bool(kwargs[kw])

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

            prev_size = os.path.getsize(self._file_name)

            while True:
                try:
                    self.check_access()
                    file_size = os.path.getsize(self._file_name)
                    lines = list()
                    if prev_size != file_size:
                        fp = open(self._file_name, 'r')
                        if prev_size > file_size:
                            if self._truncate_handler:
                                self._truncate_handler()
                            prev_size = 0
                        do_read_lines = True
                        while do_read_lines:
                            fp.seek(prev_size, 0)
                            line = fp.readline()
                            prev_size = fp.tell()
                            if line:
                                lines.append(line.rstrip('\r\n'))
                            else:
                                do_read_lines = False
                        fp.close()
                    if len(lines) > 0 and self._line_handler:
                        self._line_handler(lines)
                    time.sleep(interval)
                except FileNotFoundError:
                    print("File not found: " + self._file_name)
                    if not self._retry:
                        raise
                except PermissionError:
                    print("Access denied: " + self._file_name)
                    if not self._retry:
                        raise

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
    def line_handler(lines):
        for line in lines:
            print(">> "+line)

    def truncate_handler():
        print("File truncated")

    if len(sys.argv) < 2:
        print("Usage: tail.py file")
        exit(1)

    filename = sys.argv[1]

    tail = Tail(filename, line_handler, truncate_handler)
    tail.watch(0.01)


if __name__ == "__main__":
    main()
