# hebrew-python
hebrew-python is a python library (with commandline utitys) for writing python in hebrew.

hebrew_python runs in Python 3.6+ (because ideas runs in Python 3.6+)

(Yes, it is really possible :!)

after download this library you can really write script like:
```python
מתוך בנוי.אקראי יבא מספר_אקראי
הראה(מספר_אקראי)
```
name it like `something.hepy` and run it with `hepy something.hepy`.

you can also import another `.hepy` and `.py` files from the main file

## Installing
To install with pip
type in terminal:
```
(sudo) pip install "https://github.com/matan-h/hebrew_python/archive/main.zip"
```
<!-- TODO:upload this library to pypi :) -->
this will create the commandline script:`hepy`

## Usage
you can run hepy files with `hepy <file>`

you can start hepy repl with just `hepy`


## Built With
* [friendly](https://github.com/aroberge/friendly) - for more friendly traceback (I currectly use my fork with with my own translation to hebrew ).
* [ideas](https://github.com/aroberge/ideas) - most of the library is built on that project. it support easy creation of import hooks and it has [simple example](https://github.com/aroberge/ideas/blob/master/ideas/examples/french.py) for to recplace keywords to french keywords

## Author
matan h

## License
This project is licensed under the MIT License.
