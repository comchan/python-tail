# python-tail
Implementaion of tail in Python

**Warning** Still very buggy, especially on the truncation detection. Debugging in progress.

Add file truncation detection. If the file is truncated (file size become less than last snapshot), it reopens the file and continue tracking.
Currently, python will lock the tail'ed file. It will need further improvment for the behavior of `tail --follow=name` .

## Usage
    from tail import Tail

    def tail_line_handler(line):
        print('>> ' + line)
    
    def tail_truncate_handler():
        print('File truncated')
    
    # Create tail object
    tail = Tail('/path/to/logfile.txt', tail_line_handler, tail_truncate_handler)

    # Start watching file with 0.01 sec interval
    # WARNING: anything faster than 0.01 secs, depends on the speed of your filesystem,
    #          will accidentaly trigger file truncation
    tail.watch(0.01)


## Credits
- https://github.com/kasun/python-tail for inspiration
- GNU tail source http://git.savannah.gnu.org/cgit/coreutils.git/tree/src/tail.c#n1189 for truncation detection
