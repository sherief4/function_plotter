import re

# the list of supported keywords in mathematical function
supported_words = [
    'x',
    'sin',
    'cos',
    'sqrt',
    'exp',
    '/',
    '+',
    '*',
    '^',
    '-'
]
# for converting unsupported words to mathematical expression
replacements = {
    'sin': 'np.sin',
    'cos': 'np.cos',
    'exp': 'np.exp',
    'sqrt': 'np.sqrt',
    '^': '**',
}


# Read the function as a string from the user and return it as a valid mathematical function
def convert_func(function):
    # loop through the whole equation and check whether it is in the supported words or not
    # if it is in the supported words proceed else raise an error
    for word in re.findall('[a-zA-Z_]+', function):
        if word not in supported_words:
            raise ValueError(
                f"'{word}' is forbidden to use in math expression.\nOnly functions of 'x' are allowed.\n such as  "
                f"5*x^3 + 2*x - 1"
            )
    # deal with the other keywords that are not supported by python or numpy like "^", "sin", etc.
    for old, new in replacements.items():
        function = function.replace(old, new)

    # deal with the constant functions like f(x) = 5 by adding x*0 at the end, so it becomes f(x) = 5 + x * 0
    if "x" not in function:
        function = f"{function}+0*x"

    def f(x):
        return eval(function)

    return f
