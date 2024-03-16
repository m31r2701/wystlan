import operator
import pprint as pretty_print
import sys

import requests

def pprint(obj):
  '''
  Function pretty prints objects with indentation
  '''
  return pretty_print.PrettyPrinter(indent=4).pprint(obj)

def fail(s):
  '''
  Function prints error message and exits
  '''
  print(s)
  sys.exit(-1)

class InterpreterObject(object):
  '''
  Base class for interpreter objects
  ----------------------------------
  This class defines the base class for objects used in the interpreter. The `__init__`
  method is the constructor that takes a `value` parameter and assigns it to the `value`
  attribute of the instance. The `__repr__` method is defined to return the string 
  representation of the object, which is simply the `value` attribute.
  '''
  def __init__(self, value):
      self.value = value

  def __repr__(self):
    '''
    Function returns string representation of object
    '''
    return self.value

# These two classes, `Symbol` and `String`, inherit from the `InterpreterObject` class.
#   They don't define any additional methods or attributes, so they inherit the behavior
#   of the base class.

class Symbol(InterpreterObject):
  '''
  Class representing symbols in the language
  '''
  pass

class String(InterpreterObject):
  '''
  Class representing strings in the language
  '''
  pass

class Lambda(InterpreterObject):
  '''
  Class representing lambda functions in the language
  ---------------------------------------------------
  The `Lambda` class represents a lambda function in the interpreter. It inherits from 
  the `InterpreterObject` class. The `__init__` method takes `arguments` and `code` 
  parameters and assigns them to the corresponding attributes of the instance. The 
  `__repr__` method returns a string representation of the lambda function in the format
  `(lambda (arguments) (code))`.
  '''
  def __init__(self, arguments, code):
      self.arguments = arguments
      self.code = code

  def __repr__(self):
    '''
    Function returns string representation of lambda function
    '''
    return "(lambda (%s) (%s))" % (self.arguments, self.code)

class List(InterpreterObject):
  '''
  Class representing lists in the language
  '''
  def __init__(self, elements):
      self.elements = elements

  def __repr__(self):
    '''
    Function returns string representation of list
    '''
    return str(self.elements)

def tokenize(s):
  '''
  Function to tokenise the input string
  -------------------------------------
  The `tokenize` function takes a string `s` as input and tokenizes it into a list of
  tokens. It iterates over each character in the string and builds tokens based on
  certain rules. It handles strings enclosed in single quotes, parentheses, and 
  whitespace characters. The resulting list of tokens is returned.
  '''
  ret = []
  in_string = False
  current_word = ''
  in_comment = False
  for i, char in enumerate(s):
      if char == "'" and not in_comment:
          if in_string is False:
              in_string = True
              current_word += char
          else:
              in_string = False
              current_word += char
              ret.append(current_word)
              current_word = ''
      elif in_string is True:
          current_word += char
      elif char == ';' and not in_string:
          in_comment = True
      elif char == '\n' and in_comment:
          in_comment = False
      elif not in_comment:
          if char in ['\t', '\n', ' ']:
              if current_word:
                  ret.append(current_word)
                  current_word = ''
          elif char in ['(', ')', '[', ']']:
              if current_word:
                  ret.append(current_word)
                  current_word = ''
              ret.append(char)
          else:
              current_word += char
  if current_word and not in_comment:
      ret.append(current_word)
  return ret

# These three functions, `is_integer`, `is_float`, and `is_string`, are helper functions
#   used to check if a given string represents an integer, float, or string, 
#   respectively. They use exception handling to attempt to convert the string to the 
#   corresponding type and return `True` if successful, `False` otherwise.

def is_integer(s):
  '''
  Function to check if a string represents an integer
  '''
  try:
      int(s)
      return True
  except ValueError:
      return False

def is_float(s):
  '''
  Function to check if a string represents a float
  '''
  try:
      float(s)
      return True
  except ValueError:
      return False

def is_string(s):
  '''
  Function to check if a string represents a string literal
  '''
  if s[0] == "'" and s[-1] == "'":
      return True
  return False

def parse(tokens):
  '''
  Function to parse the tokenised input
  -------------------------------------
  The `parse` function is the entry point for parsing the list of tokens. It expects the
  first token to be an opening parenthesis `(` and calls the `do_parse` function to 
  parse the rest of the tokens.
  '''
  itert = iter(tokens)
  token = next(itert)
  if token == '(':
      return do_parse(itert)
  elif token == '[':
      return parse_list(itert)
  elif is_integer(token):
      return int(token)
  elif is_float(token):
      return float(token)
  elif is_string(token):
      return String(token[1:-1])
  else:
      return Symbol(token)

def parse_list(tokens):
  '''
  Function to parse a list
  '''
  ret = []
  for token in tokens:
      if token == '[':
          ret.append(parse_list(tokens))
      elif token == ']':
          return List(ret)
      else:
          ret.append(parse(iter([token])))
  fail("Unexpected end of list")

def do_parse(tokens):
  '''
  Function to parse expressions within parentheses
  ------------------------------------------------
  The `do_parse` function recursively parses the tokens, handling nested expressions,
  and returns the parsed expression as a list.
  '''
  ret = []
  for token in tokens:
      if token == '(':
          ret.append(do_parse(tokens))
      elif token == ')':
          return ret
      elif token == '[':
          ret.append(parse_list(tokens))
      elif token == ']':
          fail("Unexpected closing square bracket")
      else:
          ret.append(parse(iter([token])))

def eval(expr, environment):
  '''
  Function to evaluate expressions
  --------------------------------
  The `eval` function evaluates an expression `expr` in the given `environment`. 
  It handles different types of expressions, such as integers, floats, strings, symbols,
  and lists. For list expressions, it evaluates special forms like `lambda`, `if`, 
  `define`, and `begin`, and applies functions to their arguments.
  '''
  if isinstance(expr, (int, str, float)):
      return expr
  elif isinstance(expr, String):
      return expr.value
  elif isinstance(expr, Symbol):
      if expr.value not in environment:
          fail("Couldn't find symbol {}".format(expr.value))
      return environment[expr.value]
  elif isinstance(expr, List):
      return List([eval(element, environment) for element in expr.elements])
  elif isinstance(expr, list) and isinstance(expr[0], Symbol):
      if expr[0].value == 'lambda':
          arg_names = expr[1]
          code = expr[2]
          return Lambda(arg_names, code)
      elif expr[0].value == 'if':
          condition = expr[1]
          then = expr[2]
          _else = None
          if len(expr) == 4:
              _else = expr[3]
          if eval(condition, environment) is not False:
              return eval(then, environment)
          elif _else is not None:
              return eval(_else, environment)
      elif expr[0].value == 'define':
          name = expr[1].value
          value = eval(expr[2], environment)
          environment[name] = value
      elif expr[0].value == 'begin':
          for ex in expr[1:]:
              eval(ex, environment)
      elif expr[0].value == 'for':
          var_name = expr[1].value
          iterable = eval(expr[2], environment)
          body = expr[3]
          for item in iterable.elements:
              new_env = dict(environment)
              new_env[var_name] = item
              eval(body, new_env)
      else:
          fn = eval(expr[0], environment)
          args = [eval(arg, environment) for arg in expr[1:]]
          return apply(fn, args, environment)

def apply(fn, args, environment):
  '''
  Function to apply a function to arguments
  -----------------------------------------
  The `apply` function is used to apply a function `fn` to its `args` in the given 
  `environment`. It handles both callable functions and lambda functions.
  '''
  if callable(fn):
      return fn(*args)
  if isinstance(fn, Lambda):
      new_env = dict(environment)
      if len(args) != len(fn.arguments):
          fail("Mismatched number of arguments to lambda")
      for i in range(len(fn.arguments)):
          new_env[fn.arguments[i].value] = args[i]
      return eval(fn.code, new_env)

def req_get(url, *args):
  '''
  Function to make a GET request
  '''
  response = requests.get(url, *args)
  return response.text

def req_post(url, *args):
  '''
  Function to make a POST request
  '''
  response = requests.post(url, *args)
  return response.text

def splitter(presplit, split_arg):
  '''
  Function to split a string into a list
  '''
  return presplit.split(split_arg)

def joiner(prejoin, join_arg):
  '''
  Function to join a list of strings into a string
  '''
  return join_arg.join(prejoin)

# The `base_environment` dictionary defines the initial environment for the 
#   interpreter. It contains built-in functions and operators like arithmetic
#   operations, comparison operations, and the `print` function.
base_environment = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
    '>': operator.gt,
    '>=': operator.ge,
    '<': operator.lt,
    '<=': operator.le,
    '=': operator.eq,
    '!=': operator.ne,
    'and': operator.and_,
    'or': operator.or_,
    'not': operator.not_,
    'is': operator.is_,
    'isnt': operator.is_not,
    'abs': operator.abs,
    '//': operator.floordiv,
    'index': operator.index,
    'mod': operator.mod,
    '**': operator.pow,
    'xor': operator.xor,
    'concat': operator.concat,
    'contains': operator.contains,
    'countOf': operator.countOf,
    'get': req_get,
    'post': req_post,
    'split': splitter,
    'join': joiner,
    'nil': None,
    'print': lambda x: sys.stdout.write(str(x) + '\n'),
    'list': lambda *args: List(args),
    'car': lambda lst: lst.elements[0],
    'cdr': lambda lst: List(lst.elements[1:]),
    'cons': lambda x, lst: List([x] + lst.elements),
    'len': lambda lst: len(lst.elements),
}

def main():
  '''
  The `main` function is the entry point of the program. It expects a single 
  command-line argument specifying the file to be interpreted. It reads the contents of 
  the file, tokenizes it, parses the tokens, and evaluates the parsed expression in the 
  `base_environment`.
  '''
  
  if len(sys.argv) != 2:
      print("usage: python {} <file>.hiss".format(sys.argv[0]))
      sys.exit(-1)

  with open(sys.argv[1]) as fd:
      contents = fd.read()
      parsed = parse(tokenize(contents))
      eval(parsed, base_environment)

# The `if __name__ == '__main__':` block ensures that the `main` function is only 
#   executed if the script is run directly (not imported as a module).
if __name__ == '__main__':
    main()
