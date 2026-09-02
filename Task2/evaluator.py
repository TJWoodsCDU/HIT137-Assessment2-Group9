"""
Instead of using classes to keep track of the state of the parser,
we use nested functions with nonlocal references to the position in the
state of the token parser we are in.


KEY:
    expr    -> Addition / Subtraction
    term    -> Multiplication / Division
    power   -> Exponentiation (Right-associative)
    factor  -> Unary neg (-)
    primary -> Numbers, Parentheses
"""


def tokenize(expression):
    """
    Tokenizer / Lexer
    Convert the expression string into a list of dictionaries representing
    operators/characters
    """
    tokens = []
    i = 0

    while i < len(expression):
        char = expression[i]

        # Skip whitespace
        if char.isspace():
            i += 1
            continue

        # Handle numbers (including decimals)
        if char.isdigit():
            num = ""
            # Integer part
            while i < len(expression) and expression[i].isdigit():
                num += expression[i]
                i += 1
            # Decimal part
            if i < len(expression) and expression[i] == '.':
                num += '.'
                i += 1
                if i < len(expression) and expression[i].isdigit():
                    while i < len(expression) and expression[i].isdigit():
                        num += expression[i]
                        i += 1
                else:
                    raise ValueError(f"Invalid number format: {num}.")
            tokens.append({"type": "NUM", "value": num})
            continue

        # Handle operators
        if char in '+-*/%^':
            tokens.append({"type": "OP", "value": char})
            i += 1
            continue

        # Handle parenthese
        if char == '(':
            tokens.append({"type": "LPAREN", "value": '('})
            i += 1
            continue
        if char == ')':
            tokens.append({"type": "RPAREN", "value": ')'})
            i += 1
            continue

        # Invalid character
        raise ValueError(f"Invalid character: '{char}'")

    tokens.append({"type": "END", "value": None})
    return tokens


def parse_and_eval(tokens):
    """
    Parser using Recursive Descent without classes.
    Implements implicit multiplication, operators precedence, and associativity.
    """
    pos = 0

    def peek():
        nonlocal pos  # references the pos in parse_and_eval()
        if pos < len(tokens):
            return tokens[pos]
        return None

    def get():
        nonlocal pos
        tok = peek()
        if tok:
            pos += 1
        return tok

    def parse_expr():
        node = parse_term()
        
        while True:
            tok = peek()
            if tok and tok["type"] == "OP" and tok["value"] in '+-':
                op = get()["value"]
                right = parse_term()
                node = (op, node, right)
            else:
                break
       
        return node


    def parse_term():
        node = parse_power()
        
        while True:
            tok = peek()
            if tok and tok["type"] == "OP" and tok["value"] in '*/%':
                op = get()["value"]
                right = parse_power()
                node = (op, node, right)
            else:
                break
                
        return node

    
    def parse_power():
        node = parse_factor()
        
        tok = peek()
        if tok and tok["type"] == "OP" and tok["value"] == '^':
            get() # consume '^'
            right = parse_power() # Right-associative
            node = ('^', node, right)
            
        return node
    

    def parse_factor():
        tok = peek()
        
        # Unary negation
        if tok and tok["type"] == "OP" and tok["value"] == '-':
            get() # consume '-'
            node = parse_factor()
            return ('neg', node)
            
        # Unary plus (not supported - should raise error)
        if tok and tok["type"] == "OP" and tok["value"] == '+':
            raise ValueError("Unary plus is not supported")
            
        # Primary expression
        return parse_primary()

    def parse_primary():
        tok = peek()
        
        # Number literal
        if tok and tok["type"] == "NUM":
            get() # consume number
            return ('num', float(tok["value"]))
            
        # Parenthesized expression
        if tok and tok["type"] == "LPAREN":
            get() # consume '('
            node = parse_expr()
            
            # Expect closing parenthesis
            if not expect("RPAREN", ')'):
                raise ValueError("Missing closing parenthesis")
            
            return node
        
        raise ValueError(f"Unexpected token: {tok}")
            
    
    # Begin chain
    ast = parse_expr()

    # Confirm all tokens parsed
    if pos < len(tokens):
        raise ValueError(f"Unparsed tokens remain starting at {tokens[pos]}")

    # Return Abstract Syntax Tree (AST)
    return ast


def format_number(literal):
    value = float(literal)
    if value.is_integer():
        return str(int(value))
    return str(value)


def format_tokens(tokens):
    parts = []
    for tok in tokens:
        if tok["type"] == "END":
            continue
        parts.append(f"{tok['type']}({tok['value']})")
    return " ".join(parts)


def format_tree(ast):
    node_type = ast[0]
 
    if node_type == "num":
        return format_number(ast[1])
 
    if node_type == "neg":
        return f"(-{format_tree(ast[1])})"
 
    if node_type == "binop":
        _, op, left, right = ast
        return f"({format_tree(left)} {op} {format_tree(right)})"
 
    raise ValueError(f"Unknown AST node: {ast}")


def evaluate_ast(ast):
    node_type = ast[0]
 
    if node_type == "num":
        return float(ast[1])
 
    if node_type == "neg":
        return -evaluate_ast(ast[1])
 
    if node_type == "binop":
        _, op, left_ast, right_ast = ast
        left = evaluate_ast(left_ast)
        right = evaluate_ast(right_ast)
 
        if op == '+':
            return left + right
        if op == '-':
            return left - right
        if op == '*':
            return left * right
        if op == '/':
            if right == 0:
                raise ZeroDivisionError("Division by zero")
            return left / right
        if op == '%':
            if right == 0:
                raise ZeroDivisionError("Modulo by zero")
            return left % right
        if op == '^':
            return left ** right
        raise ValueError(f"Unknown operator: {op}")
 
    raise ValueError(f"Unknown AST node: {ast}")


def process_expression(expression: str) -> dict:
    """
    Entry to the parser.
    Takes an expression and returns the dictionary representing
    the input, tree, tokens, and result.
    """
    raw_expression = expression.rstrip()

    # Initialise result dict (default to error state)
    result_dict = {
        "input": raw_expression,
        "tree": "ERROR",
        "tokens": "ERROR",
        "result": "ERROR",
    }

    try:
        tokens = tokenize(raw_expression)
        result_dict["tokens"] = format_tokens(tokens)

        ast = parse_and_eval(tokens)
        result_dict["tree"] = format_tree(ast)

        calc_result = evaluate_ast(ast)
        result_dict["result"] = (
            int(calc_result) if calc_result.is_integer() else calc_result
        )

    except Exception:
        # Do nothing. Resort to default error state
        pass

    return result_dict


def evaluate_file(input_path: str) -> list[dict]:
    "Takes the input file and returns the final output in a list of dictionaries"
    with open(input_path, "r") as file:
        lines = file.readlines()

    output = []
    for expression in lines:
        output.append(process_expression(expression))

    return output


if __name__ == "__main__":
    # Define files
    input_path = "input.txt"
    output_path = "output.txt"  # TODO: Assert that output path is in the same directory as input path using pathlib

    # Begin parsing
    results = evaluate_file("input.txt")

    # Print to file
    with open(output_path, "w") as out:
        blocks = []
        for result in results:
            result_val = result["resultult"]
            if isinstance(result_val, float):
                result_str = format_number(result_val)
            else:
                result_str = str(result_val)

            block = f"Input: {result['input']}\nTree: {result['tree']}\nTokens: {result['tokens']}\nresultult: {result_str}"
            blocks.append(block)

        out.write("\n\n".join(blocks))

