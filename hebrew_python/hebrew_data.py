# functions:
hebrew_builtins = {
    # numbers
    "מוחלט": "abs",
    "הכל": "all",
    "אחד": "any",  # not sure about this translate: 'אחד' mean '1' in hebrew.

    # list
    "אורך": "len",
    "מינימום": "min",
    "מקסימום": "max",
    "הפוך": 'reversed',
    "מניה":"enumerate",
    "מפה":"map",

    # std
    "הראה": "print",
    "קלט": "input",

    # errors
    "שגיאת_ייבוא": "ImportError",
    "שגיאת_שם": "NameError",
    "שגיאת_הרשאות": "PermissionError",
    "שגיאה":"Exception",
    "שגיאת_קובץ_לא_נמצא":"FileNotFoundError",
    

    # strings
    'יצג': 'repr',
    "בצע": "exec",
    "פתח":"open"
}

# keywords:
hebrew_keywords = {
    "בנוי":
    "hebrew_python",  # TODO : I want to create another module for this.

    # if and booleans:
    "אם": "if",
    "אמת": "True",
    "שקר": "False",
    "וגם": "and",
    "לא": "not",
    "הוא": "is",
    "אחרת": "else",
    "אחרת_אם": "elif",  # אחרתאם ?
    "או": "or",

    # loops
    "לכל": "for",
    "בתוך": "in",
    "טווח": "range",
    "צא": "break",
    "בעוד": "while",
    "המשך": "continue",

    # types:
    "רשימה": "list",
    "שלם": "int",
    "צף": "float",
    "כלום": "None",
    "בוליאני": "bool",
    "מחרוזת":"str",
    "סט": "set()",
    'object': 'אובייקט',

    # imports
    "מתוך": "from",
    "יבא": "import",
    "בתור": "as",

    # classes and functions
    "החזר": "return",
    "מחלקה": "class",
    "גלובלי": "global",
    "הגדר": "def",
    "עבור": "pass",
    "צור": "yield",

    # errors
    "נסה": "try",
    "ודא": "assert",
    "זרוק": "raise",
    "תפוס": "except",
    "לבסוף": "finally",
    
    # list
    "עגל": "round()",
    "פרוסה": "slice()",
    "מיין": "sorted()",
    "סכום": "sum()",
    "סוג": "type()",

    #
    'עם': "with",
    "מחק": "del",
    "למדה": "lambda",
}
