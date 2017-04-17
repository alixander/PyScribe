# [<img title="pyscribe-logo" src="http://i.imgur.com/JZYtIda.png" width="350px" alt="PyScribe logo"/>](https://github.com/alixander/pyscribe)

[![Build Status](https://travis-ci.org/alixander/PyScribe.svg?branch=master)](https://travis-ci.org/alixander/PyScribe) [![Latest Version](https://pypip.in/version/pyscribe/badge.svg?text=version)](https://pypi.python.org/pypi/pyscribe/) [![Supported Python versions](https://pypip.in/py_versions/pyscribe/badge.svg)](https://pypi.python.org/pypi/pyscribe/)

A Python library to make debugging with print statements simpler and more effective.

[PyScribe.com](http://pyscribe.com) for full documentation. (Work in progress)

*Warning*: This project is currently in a pre-release state. Open to contributions and collaborators.

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
4. Run one of the following commands
```bash
$ pyscribe myfile.py
 ```
 This is the equivalent of running `$ python myfile.py` with all calls desugared.

```bash
$ pyscribe myfile.py --extraargs "-u asdf"
```
This is the equivalent of running `$ python myfile.py -u asdf` with all calls desugared.

```bash
$ pyscribe myfile.py --desugared
```
This does not run anything, but rather outputs a myfile_desugared.py, which is intended to be run to debug.


Argument Options
-----------------
- `--extraargs` -- Arguments intended to be passed to Python file when run. Must be called with --run set
- `--clean` -- Produce a clean version of the file with all references to PyScribe removed 
- `--desugared` -- Produce a desugared version of the file with all API calls replaced with valid Python.
- `--log` -- Save logs to a pyscribe_log.txt file along with timestamp.
- `--nolines` -- Don't show line numbers.

API Calls
----------
- `pyscribe.Scriber(labels=[])` -- Initialize PyScribe. If you're scribing values with labels, you can filter by labels by passing in a list of the labels as strings.
- `pyscribe.p(object, label=None)` -- Print the object value with relevant info dependent on type
- `pyscribe.iterscribe(object)` -- Log the object value from inside a for or while loop which prints current iteration
- `pyscribe.watch(object)` -- Log the object whenever its value changes
- `pyscribe.d(object, unit="*")` -- Distinguish the log with a clear separator defined by the unit

Planned
----------
- `pyscribe.values(object)` -- Log the internal values of lists and dictionaries in a pretty way
- `pyscribe.props(object)` -- Log the fields of an object and their values
- Add configurations for the logging messages. e.g. `Line 9: x is 4` instead of `From line 9: x is the int 4`.
- `pyscribe make` -- Command line instruction to search python files in current directory, desugar all files using pyscribe, replace files with desugared version, store old version in temporary directory.
- `pyscribe debug` -- Command line instruction to find any desugared pyscribe files, replace them with counterparts in temporary directory.
- `pyscribe clean` -- Command line instruction to find python files using pyscribe and replace them with a clean version. Erase debug versions unless told otherwise. --save-debug or something.

Tests
----------
Test modules are in the `tests` directory. Specific test cases are in these modules in the form of `testcase.py`, and the test runner compares these with `testcase_correct`. Run the tests with `./run_tests`.

Example
--------
#####test.py:
```python
from pyscribe import pyscribe

def main():
    ps = pyscribe.Scriber()

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
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Log saved at 2014-12-31 22:03:48
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

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
From line 20: y changed to world
From line 23: 
----------------------------------------
foo is the int 1234
----------------------------------------

From line 24: 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
foo is the int 1234
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

From line 27: synonyms is the dict {'clerk': 'secretary', 'student': 'apprentice', 'ground': 'floor'}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
End of log
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
```

This log comes from running the desugared version of test.py:
```python
import re
import pprint
import datetime
# from pyscribe import pyscribe

def main():
    pyscribe_log = open('pyscribe_logs.txt', 'w')
    pyscribe_log.write('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\nLog saved at ' + str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + '\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n\n')

    x = 5
    pyscribe_log.write('From line 9: x is the ' + re.search(r'\'[a-zA-Z]*\'', str(type(x))).group()[1:-1] + ' ' + str(x)+ '\n')

    bar = "foo"
    NAICKSHMWL = -1
    pyscribe_log.write('----------------------------------------\n' + 'bar is the ' + re.search(r'\'[a-zA-Z]*\'', str(type(bar))).group()[1:-1] + ' ' + str(bar) + ' at beginning of for loop at line 12' + '\n')
    for i in xrange(5):
        bar += str(i)
        NAICKSHMWL += 1
        pyscribe_log.write('From line 14: In iteration ' + str(NAICKSHMWL) + ', bar changed to ' + str(bar) + '\n')

    y = "hello"
    pyscribe_log.write('From line 17: y is the ' + re.search(r'\'[a-zA-Z]*\'', str(type(y))).group()[1:-1] + ' ' + str(y)+ '\n')
    pyscribe_log.write('From line 18: Watching variable y, currently ' + re.search(r'\'[a-zA-Z]*\'', str(type(y))).group()[1:-1] + ' ' + str(y)+ '\n')

    y = "world"
    pyscribe_log.write('From line 20: y changed to ' + str(y)+ '\n')

    foo = 1234
    pyscribe_log.write('From line 23: \n----------------------------------------\nfoo is the ' + re.search(r'\'[a-zA-Z]*\'', str(type(foo))).group()[1:-1] + ' ' + str(foo) + '\n----------------------------------------\n'+ '\n')
    pyscribe_log.write('From line 24: \n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nfoo is the ' + re.search(r'\'[a-zA-Z]*\'', str(type(foo))).group()[1:-1] + ' ' + str(foo) + '\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n'+ '\n')

    synonyms = {"clerk": "secretary", "student": "apprentice", "ground": "floor"}
    pyscribe_log.write('From line 27: synonyms is the ' + re.search(r'\'[a-zA-Z]*\'', str(type(synonyms))).group()[1:-1] + ' ' + str(synonyms)+ '\n')

    pyscribe_log.write('\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\nEnd of log\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n')
    pyscribe_log.close()
if __name__ == "__main__":
    main()
```
