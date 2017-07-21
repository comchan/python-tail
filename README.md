# python-tail
Implementaion of tail in Python

**Warning** Still very buggy, especially on the truncation detection. Debugging in progress.

Add file truncation detection. If the file is truncated (file size become less than last snapshot), it reopens the file and continue tracking.
Currently, python will lock the tail'ed file. It will need further improvment for the behavior of `tail --follow=name` .

Credits:
- https://github.com/kasun/python-tail for inspiration
- GNU tail source http://git.savannah.gnu.org/cgit/coreutils.git/tree/src/tail.c#n1189 for truncation detection
