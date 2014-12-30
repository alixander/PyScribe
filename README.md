PyScribe
=====================

A Python library to make debugging with print statements simpler and more effective.

*Warning*: This project is currently in a pre-release state.

Installation
------------
To install pyscribe:
```bash
$ pip install pyscribe
```
It may be necessary to have root privileges, in which case:
```bash
$ sudo pip install pyscribe
```
To uninstall:
```bash
$ pip uninstall pyscribe
```

Usage
------
1. Include `from pyscribe import pyscribe` at the top of the files you are debugging.
2. Initialize a variable of your choice to `pyscribe.Scriber()` (E.g.: `ps = pyscribe.Scriber()`)
3. Make API calls as needed. (E.g.: `ps.p(x)`)
4. Run
```bash
$ pyscribe myfile.py --run
 ```
 This is the equivalent of running `$ python myfile.py` with all calls desugared.
```bash
$ pyscribe myfile.py --run --extraargs "-u asdf"
```
This is the equivalent of running `$ python myfile.py -u asdf` with all calls desugared.
```bash
$ pyscribe myfile.py --desugared
```
This does not run anything, but rather outputs a myfile_desugared.py, which is intended to be run to debug.


Argument Options
-----------------
- `--run` -- Run the desugared version
- `--extraargs` -- Arguments intended to be passed to Python file when run. Must be called with --run set
- `--clean` -- Produce a clean version of the file with all references to PyScribe removed 
- `--desugared` -- Produce a desugared version of the file with all API calls replaced with valid Python.

API Calls
----------
- `pyscribe.p(object, label=None)` -- Print the object value with relevant info dependent on type
- `pyscribe.iterscribe(object)` -- Log the object value from inside a for or while loop which prints current iteration
- `pyscribe.watch(object)` -- Log the object whenever its value changes
- `pyscribe.d(object, unit="*")` -- Distinguish the log with a clear separator defined by the unit

Planned
----------
- `pyscribe.filter_labels(list)` -- Only log the pyscribe.scribe calls that are labeled with a label in the list
- `pyscribe.save_logs(boolean)` -- Save the logs with a timestamp in a file (does this by default right now)
- `pyscribe.log_lines(boolean)` -- Insert a "from line xx" before each line (does this by default right now)
- `pyscribe.scribevalues(object)` -- Log the internal values of lists and dictionaries in a pretty way

Example
--------
#####test.py:
```python
from pyscribe import pyscribe

def main():
    ps = pyscribe.Scriber()

    ps.save_logs(True)

    x = 5
    ps.p(x)

    bar = "foo"
    for i in xrange(5):
        bar += str(i)
        ps.iterscribe(bar)

    y = "hello"
    ps.p(y)
    ps.watch(y)

    y = "world"

    foo = 1234
    ps.d(foo)
    ps.d(foo, unit="^")

    synonyms = {"clerk": "secretary", "student": "apprentice", "ground": "floor"}
    ps.p(synonyms)

if __name__ == "__main__":
    main()
```
####pyscribe_logs.txt:
```html
From line 9: x is the int 5
----------------------------------------
bar is the str foo at beginning of for loop at line 12
From line 14: In iteration 0, bar changed to foo0
From line 14: In iteration 1, bar changed to foo01
From line 14: In iteration 2, bar changed to foo012
From line 14: In iteration 3, bar changed to foo0123
From line 14: In iteration 4, bar changed to foo01234
From line 17: y is the str hello
From line 18: Watching variable y, currently str hello
From line 23: 
----------------------------------------
foo is the int 1234
----------------------------------------

From line 24: 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
foo is the int 1234
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

From line 27: synonyms is the dict {'clerk': 'secretary', 'student': 'apprentice', 'ground': 'floor'}
```
