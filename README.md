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
1. Include `import pyscribe` at the top of the files you are debugging.
2. Initialize a variable of your choice to `pyscriber.Scribe()` (E.g.: `ps = pyscriber.Scribe()`)
3. Make API calls as needed. (E.g.: `ps.p(x)`)
4. Run
```bash
$ pyscribe myfile.py
 ```
 This outputs a myfile_desugared.py, which is intended to be run to debug.

API Calls
----------
- `pyscribe.scribe(object, label=None)` -- Logs the object value with relevant info dependent on type
- `pyscribe.is_debugging(boolean)` -- Enable or disable the library
- `pyscribe.log_lines(boolean)` -- Insert a "from line xx" before each line
- `pyscribe.save_logs(boolean)` -- Save the logs with a timestamp in a file
- `pyscribe.iterscribe(object)` -- Log the object value from inside a for or while loop which prints current iteration
- `pyscribe.watch(object)` -- Log the object whenever its value changes
- `pyscribe.scribevalues(object)` -- Log the internal values of lists and dictionaries in a pretty way
- `pyscribe.scribestate()` -- Log every variable within the current scope
- `pyscribe.distinguish(object, unit="*")` -- Distinguish the log with a clear separator defined by the unit
- `pyscribe.filter_labels(list)` -- Only log the pyscribe.scribe calls that are labeled with a label in the list

Example
--------
#####test.py:
```python
import pyscribe

scriber = pyscribe.Scriber()

scriber.is_debugging(True)
scriber.log_lines(True)
scriber.save_logs(True)

x = 5
scriber.scribe(x) # From line xx: x is the number 5

for i in xrange(5):
    scriber.iterscribe(i) # Starting for loop at line xx.
                           # ============================
                           # Iteration xx: i is the number xx
                           # ....
                           # ============================
                           # End of loop at line xx.

y = "hello"
scriber.scribe(y) # From line xx: y is the string 'hello'
scriber.watch(y)

y = "world" # From line xx: y changed from the string 'hello' to the string 'world'

synonyms = {"clerk": "secretary", "student": "apprentice", "ground": "floor"}
scriber.scribe(synonyms) # From line xx: synonyms is a dictionary of length 3
scriber.scribevalues(synonyms) # From line xx: synonyms contains the following values:
                                # ========================
                                # 'clerk': 'secretary'
                                # 'student': 'apprentice'
                                # 'ground': 'floor'
                                # ========================
```

####logs.txt:
```html
--------------Begin log of run at 12:22 PM---------

From line xx: x is the number 5
Starting for loop at line xx.
   ============================
   Iteration 0: i is the number 1
   Iteration 1: i is the number 1
   Iteration 2: i is the number 1
   Iteration 3: i is the number 1
   Iteration 4: i is the number 1
   ============================
End of loop at line xx.
From line xx: y is the string 'hello'
From line xx: y changed from the string 'hello' to the string 'world'
From line xx: synonyms is a dictionary of length 3
From line xx: synonyms contains the following values:
    ========================
    'clerk': 'secretary'
    'student': 'apprentice'
    'ground': 'floor'
    ========================

----------------End of log---------------
```
