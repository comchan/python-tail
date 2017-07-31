# python-tail
Implementaion of UNIX tail in Python

Tested with Python 3.6. 

This implementation detect file changes by getting the file size from the file system. If the detected file size increases, it outputs the new lines.

If the detected file size reduces, it is determined as a truncation and output all the lines in the tail'ed file. 

Recent update tries to reduce the duration of tail'ed file being locked.

## Note to those who tries to use file timestamp for change detection
**Windows > 7** now will not update accessed and modified timestamp of a file until the file is closed. This is a new feature that reduces disk IO. Therefore, `os.path.getatime()` and `os.path.getmtime()` will not work.
I have not tested this script on UNIX system yet. 

## Usage
    from tail import Tail

    def tail_lines_handler(lines):
        for line in lines:
            print('>> ' + line)
    
    def tail_truncate_handler():
        print('File truncated')
    
    # Create tail object
    tail = Tail('/path/to/logfile.txt', tail_lines_handler, tail_truncate_handler)

    # Start watching file with 0.01 sec interval
    # WARNING: anything faster than 0.01 secs, depends on the speed of your filesystem,
    #          will accidentaly trigger file truncation
    tail.watch(0.01)


## Credits
- https://github.com/kasun/python-tail for inspiration
- GNU tail source http://git.savannah.gnu.org/cgit/coreutils.git/tree/src/tail.c#n1189 for truncation detection
