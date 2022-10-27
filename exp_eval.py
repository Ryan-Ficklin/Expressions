from stack_array import Stack
from typing import List

# You should not change this Exception class!
class PostfixFormatException(Exception):
    pass

# fairly simple helper function for RPN eval, uses elifs to determine the operator, performs that operation between
# the two given operators if it is possible
# in the case of dividing by 0 or bitshifting with floats, raise appropriate errors instead
def _postfix_eval(oper:str, op1: float, op2: float) -> float:
    """ Input: two operands and a str depiction of an operator
    checks what operator is given, and returns proper operation done to the two operands
    Raises Value error if divide by 0
    Raises Illegal bit shift operand if either operand is bitshifted as a float (besides .0)"""
    if oper == "<<":
        if op1 % 1 != 0 or op2 % 1 != 0:
            raise PostfixFormatException("Illegal bit shift operand")
        return int(op1) << int(op2)
    elif oper == ">>":
        if op1 % 1 != 0 or op2 % 1 != 0:
            raise PostfixFormatException("Illegal bit shift operand")
        return int(op1) >> int(op2)
    elif oper == "**":
        return op1 ** op2
    elif oper == "*":
        return op1 * op2
    elif oper == "/":
        try:
            return op1 / op2
        except ZeroDivisionError:
            raise ValueError
    elif oper == "+":
        return op1 + op2
    else: # this case is only for subtraction, as to appease the type checker without adding useless else case that
        # could never be reached such return None, which couldn't be reached and thus cause a coverage error
        # I would prefer this to be an elif to specify that this is the subtraction case, but now it is
        # subtraction by process of elimination with every other operator, seeing as no other operator in context
        # could possibly be passed in
        return op1 - op2

def postfix_eval(input_str: str) -> float:
    """Evaluates a postfix expression"""
    """Input argument:  a string containing a postfix expression where tokens 
    are space separated.  Tokens are either operators + - * / ** << >> or numbers (integers or floats)
    Returns the result of the expression evaluation. 
    Raises an PostfixFormatException if the input is not well-formed"""
    # list of all valid operaters, used for comparison
    operators: List[str] = ["<<", ">>", "**", "*", "/", "+", "-"]
    # turns the input_str into a list of individual tokens
    tokens: List[str] = input_str.split(" ")
    # creates the stack that will be used to hold values until an operator in the RPN expression is reached
    # stack of capacity 30 as specified by instructions
    eval_stack = Stack(30)
    # two counts that will be used to determine whether the input_str is a valid post fix expression
    op_count: int = 0
    number_count: int = 0
    # Error catching
    # empty input str -> not enough operands
    if input_str == "":
        raise PostfixFormatException("Insufficient operands")
    # loops through to:
    # a) catch any token that is not either an operator or an int/float
    # b) count number of operators
    # c) count number of operands
    for token in tokens:
        # if the token is not an operator, it must be able to be cast to int or float otherwise it is invalid
        if token not in operators:
            try:
                int(token)
            except:
                try:
                    float(token)
                except:
                    raise PostfixFormatException("Invalid token")
        # incrementing op_count for every operator found
        if token in operators:
            op_count += 1
        # incrementing num_count for every non-operator found (which has now been determined to be a valid operand)
        else:
            number_count += 1
    # (example rpn expression: 5 7 + 8 *)
    # ^ three operands, two operators, operators to operand ratio must always be one less
    if op_count > number_count - 1:
        raise PostfixFormatException("Insufficient operands")
    if number_count > op_count + 1:
        raise PostfixFormatException("Too many operands")
    # after error catching, expression can be evaluated
    for token in tokens:
        # pushing all operands to the stack for use once operator is found
        if token not in operators:
            eval_stack.push(token)
        else:
            # i.e. input_str = 5 + 5
            # if two operands cannot be popped from the stack by the time an operator is found, the rpn expression is
            # in bad format, so throw error
            try:
                operand2: float = float(eval_stack.pop())
                operand1: float = float(eval_stack.pop())
            except IndexError:
                raise PostfixFormatException("Bad post-fix format")
            # pushing to the stack the result of a helper function call (determines what operator is used and returns
            # the result of using that operator on the two popped operands
            eval_stack.push(_postfix_eval(token, operand1, operand2))
    # at this point, eval_stack should only have the final resulting value, and to return that value as a float,
    # pop that value set a variable equal to it
    evaluation: float = float(eval_stack.pop())
    return evaluation

def precedence(oper: str) -> int:
    """Given an operator as a string, returns an integer value to represent operator precedence,
    higher value = higher precedence"""
    if oper == ">>" or oper == "<<":
        return 3
    elif oper == "**":
        return 2
    elif oper == "*" or oper == "/":
        return 1
    else: # oper at this point can be assumed to be either + -, both of which have the same precedence
        return 0

def infix_to_postfix(input_str: str) -> str:
    """Converts an infix expression to an equivalent postfix expression"""
    """Input argument:  a string containing an infix expression where tokens are 
    space separated.  Tokens are either operators + - * / ** << >> or numbers (integers or floats)
    Returns a String containing a postfix expression """
    # list of all valid operators the infix statement could contain
    operators: List[str] = ["<<", ">>", "**", "*", "/", "+", "-"]
    # splits the infix notation expression into individual list items for easier processing
    tokens: List[str] = input_str.split(" ")
    # this is the string that will be returned, appropriate operands and operators will be added as the token list is
    # processed
    rpn: str = ""
    # stack which will hold operators and opening parentheses, "(", until necessary
    # specified to be of capacity 30
    op_stack = Stack(30)
    for token in tokens:
        # adds all operands immediately to the rpn notation string
        if token not in operators and token != "(" and token != ")":
            rpn += token + " "
        # if an opening parentheses is found, pushed onto stack
        if token == "(":
            op_stack.push(token)
        # closing parentheses found, NOT pushed to stack, instead pops all operators until opening ( is found, and
        # adds them to the rpn expression string
        if token == ")":
            while op_stack.peek() != "(":
                rpn += op_stack.pop() + " "
            # gets rid of the ( on top of the stack
            op_stack.pop()
        if token in operators:
            # case if there are no other operators in the stack with which token can be compared to
            if op_stack.is_empty():
                op_stack.push(token)
            else:
                # written as bools for a cleaner while loop
                # top of operator stack is an operator, and not, say "("
                top_stack_is_op: bool = op_stack.peek() in operators
                # compared to third index of operators specifically because
                # that is the only right associative operator, **
                token_r_assc: bool = token == operators[2]
                # all other operators beside ** are left assc
                token_l_assc: bool = token != operators[2]
                # helper function calls to determine if the precedence token is < OR <= the operator(s)
                # at the top of op_stack
                prec_less_or_eq: bool = precedence(token) <= precedence(op_stack.peek())
                prec_less: bool = precedence(token) < precedence(op_stack.peek())
                # uses above bools to run while loop in under specific circumstances
                while top_stack_is_op and ((token_l_assc and prec_less_or_eq) or (token_r_assc and prec_less)):
                    # addition of any greater/greater-equal precedence operators to the end of the post fix expression
                    rpn += op_stack.pop() + " "
                    # ends loop without checking bools if the op_stack is emptied, as to not raise index errors
                    # resulting from doing .peek() on an empty stack
                    if op_stack.is_empty():
                        break
                    # "resetting" bools in order to test if loop should run again
                    top_stack_is_op = op_stack.peek() in operators
                    token_r_assc = token == operators[2]
                    token_l_assc = token != operators[2]
                    prec_less_or_eq = precedence(token) <= precedence(op_stack.peek())
                    prec_less = precedence(token) < precedence(op_stack.peek())
                # adds the token to the operator stack once loop is completed and all higher precedence operators have
                # been popped onto the rpn expression
                op_stack.push(token)
    # pushes all remaining operators from opstack to the end of the new post fix expression
    while not op_stack.is_empty():
        rpn += op_stack.pop() + " "
    # rstrip() removes tailing space resulted from always adding a space along with whatever is
    # being added to the expression
    return rpn.rstrip()

def prefix_to_postfix(input_str: str) -> str:
    """Converts a prefix expression to an equivalent postfix expression"""
    """Input argument: a string containing a prefix expression where tokens are 
    space separated.  Tokens are either operators + - * / ** << >> or numbers (integers or floats)
    Returns a String containing a postfix expression(tokens are space separated)"""
    operators: List[str] = ["<<", ">>", "**", "*", "/", "+", "-"]
    tokens: List[str] = input_str.split(" ")
    expression_stack = Stack(30)
    # looping backwards through tokens
    for i in range(len(tokens)-1, -1, -1):
        token = tokens[i]
        # can assume that prefix is formatted correctly, so only non operator token will be operands
        # pushing token to stack whenever it encounters an operand
        if token not in operators:
            expression_stack.push(token)
        # else will always be an operator, as it's the case opposite of not in operators
        else:
            # calls expression_stack.pop() twice, in order to pop the top two values, and add them back to the stack
            # along with the operator that operates on them, with appropriate spacing in between
            string: str = expression_stack.pop() + " " + expression_stack.pop() + " " + token
            expression_stack.push(string)
    # return the only remaining item in the stack, which should be the full expression now in rpn
    post_expression: str = expression_stack.pop()
    return post_expression
