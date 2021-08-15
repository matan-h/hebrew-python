# hebrew-python
hebrew-python is a python library (with commandline utities) for programming python in Hebrew.
(Yes, it is really possible!)

hebrew-python
runs in Python 3.6+ (because `ideas` runs in Python 3.6+)


After downloading this library you can write a script like:
```python
מתוך בנוי.אקראי יבא מספר_אקראי
משתנה_כלשהו = מספר_אקראי(1,9)
הראה(משתנה_כלשהו)
```
Name the file `something.hepy` and run it with `hepy something.hepy`.

You can also import other `.hepy` and `.py` files from the main file:
```Python
יבא something
```

## Installing
To install with pip
type in terminal:
```
(sudo) pip install hebrew-python
```
This will create the commandline script:`hepy`

## Usage
You can run hepy files with `hepy <file>`

You can start Hebrew Python console with just `hepy`

## `.hepy` file syntax
`.hepy` file supports hebrew python syntax (syntax with keywords like `יבא`(import)  
and functions like `הראה` (print))
in additional to normal python syntax

## Use from normal python file/repl
You can use as library:

to import `.hepy` files into your `.py` file:
```python
from hebrew_python import create_hook
create_hook(run_module=False, console=False) # without running main module or starting repl
import hepy_module # now you can import .hepy files
```

or to start repl from normal repl:
```python
from hebrew_python import create_hook
create_hook(run_module=True, console=True) # *with* starting repl
```
## jupyter/ipython
`hebrew-python` support [jupyter](https://jupyter.org) and [ipython](https://ipython.org/) intercative console by ipython extension. to use:

install jupyter-notebook by : `pip install notebook`  
start jupyter-notebook by : `jupyter notebook`

on the first cell enter the text `%load_ext hebrew_python`
and then you can write hebrew-python in all notebook

## Dependencies
hebrew-python depends on the python libraries:
* [friendly](https://github.com/aroberge/friendly) - for more friendly traceback (friendly doesn't have translation to Hebrew yet, so currently it's using [my fork](https://github.com/matan-h/friendly) with my own translation to Hebrew. Will merge soon).

* [ideas](https://github.com/aroberge/ideas) - most of this library is built on this project. It support easy creation of import hooks and it has a [simple example](https://github.com/aroberge/ideas/blob/master/ideas/examples/french.py) for replacing keywords to French keywords

## Contribute
On all errors, problems or suggestions please open a [github issue](https://github.com/matan-h/ddebug/issues)  

If you found this library useful, it would be great if you could buy me a coffee:  

<a href="https://www.buymeacoffee.com/matanh" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-blue.png" alt="Buy Me A Coffee" height="47" width="200"></a>

## Author
matan h

## License
This project is licensed under the [BSD-4 License](https://spdx.org/licenses/BSD-4-Clause.html).
