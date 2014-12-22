PyScribe
=====================

#####A Python library to make debugging with print statements simpler and more effective.

###Implementation Details:
1. Make API calls in your program as needed
2. Run `python pyscribe.py test.py`
3. PyScribe creates 3 temporary files:
    - A record of where each line of pyscribe is called
    - A version of the file with every pyscribe call removed
    - An AST made in the compilation of the above file
4. PyScribe analyzes the AST (3rd file) & call to line mapping (1st file) and replaces the clean version (2nd file) with desugared calls.
    - Example: `pyscribe.scribe(x)` becomes `logs.write('From line ' + get_line(call_index) + ': x is the ' + type(x) + ' ' + x`
    - Example: `for i in xrange(5): pyscribe.iterscribe(i)` becomes
                `for pyscribe_enum, i in enumerate(xrange(5)): logs.write('Iteration ' + pyscribe_enum + ': i is the ' + type(i) + ' ' + i`
5. A "test_desugared.py" will be the output (and is the one intended to be run, maybe with a --run flag or something in the future)

###API Calls:
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

###Example:
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
