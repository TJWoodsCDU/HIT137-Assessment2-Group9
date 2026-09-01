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
    pass


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
        pass

    def parse_term():
        pass

    def parse_power():
        pass

    def parse_factor():
        pass

    def parse_primary():
        pass

    # Begin chain
    ast = parse_expr()

    # Confirm all tokens parsed
    if pos < len(tokens):
        raise ValueError(f"Unparsed tokens remain starting at {tokens[pos]}")

    # Return Abstract Syntax Tree (AST)
    return ast


def format_number():
    pass


def format_tokens(tokens):
    pass


def format_tree(ast):
    pass


def evaluate_ast(ast):
    pass


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

