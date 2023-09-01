def tokenize(expression):
    tokens = []
    i = 0
    while i < len(expression):
        if expression[i] in ["⇒", "¬", "=", "+", "∃"]:
            tokens.append(expression[i])
            i += 1
        elif expression[i] == "x":
            end = expression.index("]", i) + 1
            tokens.append(expression[i:end])
            i = end
        elif expression[i] in ["0", "1"]:
            tokens.append(expression[i])
            i += 1
        elif expression[i] == "p":
            end = expression.index("]", i) + 1
            tokens.append(expression[i:end])
            i = end
        else:
            raise ValueError(f"Unexpected character: {expression[i]}")
    return tokens
def parse_statement(tokens):
    # Check for empty tokens
    if not tokens:
        raise ValueError("Unexpected end of input.")

    # Get the next token
    token = tokens.pop(0)

    if token == "⇒":
        left = parse_statement(tokens)
        right = parse_statement(tokens)
        return ["⇒", left, right]

    elif token == "∃":
        int_value = parse_int(tokens)
        statement_value = parse_statement(tokens)
        return ["∃", int_value, statement_value]

    elif token == "¬":
        statement_value = parse_statement(tokens)
        return ["¬", statement_value]

    elif token == "=":
        left = parse_int(tokens)
        right = parse_int(tokens)
        return ["=", left, right]

    # If the token is not one of the operators, it should be a variable
    else:
        return token
def parse_int(tokens):
    if not tokens:
        raise ValueError("Unexpected end of input.")

    token = tokens.pop(0)

    if token in ["0", "1"]:
        return token

    elif token.startswith("x["):
        return token

    elif token == "+":
        left = parse_int(tokens)
        right = parse_int(tokens)
        return ["+", left, right]

    else:
        raise ValueError(f"Unexpected token: {token}")
def parse(expression):
    tokens = tokenize(expression)
    ast = parse_statement(tokens)

    # Ensure all tokens have been consumed
    if tokens:
        raise ValueError(f"Unexpected tokens left: {tokens}")

    return ast
def eval_ast(ast):
    """Evaluate the AST back to a string."""
    if isinstance(ast, str):
        return ast
    elif ast[0] == "⇒":
        return f"⇒{eval_ast(ast[1])}{eval_ast(ast[2])}"
    elif ast[0] == "∃":
        return f"∃{eval_ast(ast[1])}{eval_ast(ast[2])}"
    elif ast[0] == "¬":
        return f"¬{eval_ast(ast[1])}"
    elif ast[0] == "=":
        return f"={eval_ast(ast[1])}{eval_ast(ast[2])}"
    elif ast[0] == "+":
        return f"+{eval_ast(ast[1])}{eval_ast(ast[2])}"
    else:
        raise ValueError(f"Unexpected AST node: {ast}")

def disp(expression):
    expression = substitution_for_in('p','p[0]',expression)
    expression = substitution_for_in('q','p[1]',expression)
    expression = substitution_for_in('r','p[2]',expression)
    expression = substitution_for_in('s','p[3]',expression)
    expression = substitution_for_in('t','p[4]',expression)
    expression = substitution_for_in('x','x[0]',expression)
    expression = substitution_for_in('y','x[1]',expression)
    expression = substitution_for_in('z','x[2]',expression)
    expression = substitution_for_in('a','x[3]',expression)
    expression = substitution_for_in('b','x[4]',expression)
    expression = substitution_for_in('c','x[5]',expression)
    print(expression)

contains = lambda lst,sub : any(lst[i:i+len(sub)] == sub for i in range(len(lst) - len(sub) + 1))

transitivity_of_implies = '⇒⇒p[0]p[1]⇒⇒p[1]p[2]⇒p[0]p[2]'
reductio_ad_absurdum = '⇒⇒¬p[0]p[0]p[0]'
principle_of_explosion = '⇒p[0]⇒¬p[0]p[1]'
reflexivity_of_equals = '=x[0]x[0]'
transitivity_of_equals = '⇒=x[0]x[1]⇒=x[0]x[2]=x[1]x[2]'
additivity_of_equals = '⇒=x[0]x[1]=+x[0]x[2]+x[1]x[2]'
commutativity_of_plus = '=+x[0]x[1]+x[1]x[0]'
associativity_of_plus = '=+x[0]+x[1]x[2]++x[0]x[1]x[2]'
additive_identity_zero = '=+x[0]0x[0]'
existence_of_difference = '∃x[0]=+x[0]x[1]x[2]'

divide_by_natural = lambda a: '⇒='+'+'*(a-1)+'x[0]'*a+'+'*(a-1)+'x[1]'*a+'=x[0]x[1]'
remainder_mod_natural = lambda a:'∃x[0]'+'⇒¬'*(a-1)+''.join(['='+'+'*(a+i-1)+'x[0]'*a+'1'*i+'x[1]' for i in range(a)])
zero_not_one_mod_natural = lambda a: '¬=0'+'+'*a+'x[0]'*a+'1'

existential_instantiation = lambda CExpq : (lambda p :'⇒'+eval_ast(p[1][2])+eval_ast(p[2]) if p[0] == '⇒' and p[1][0] == '∃' else None)(parse(CExpq)) #⇒pq
modus_podens = lambda NCpNCpq : (lambda r : eval_ast(r[1][2][1][2]) if r[0] == '¬' and r[1][0] == '⇒' and r[1][1] == r[1][2][1][1] and r[1][2][0] == '¬' and r[1][2][1][0] == '⇒' else None)(parse(NCpNCpq)) #q
existential_generalization = lambda pq,x: '⇒∃'+x+eval_ast(parse(pq)[1])+eval_ast(parse(pq)[2]) if pq[0] == '⇒' and x in tokenize(eval_ast(parse(pq)[1])) and not(contains(tokenize(eval_ast(parse(pq)[1])),['∃',x])) and not x in tokenize(eval_ast(parse(pq)[2])) else None ##λ⇒p(x)q,x.⇒∃xpq
substitution_for_in = lambda p,q,r: r.replace(q,p)

axioms = [
transitivity_of_implies,
reductio_ad_absurdum,
principle_of_explosion,
reflexivity_of_equals,
transitivity_of_equals,
additivity_of_equals,
commutativity_of_plus,
associativity_of_plus,
additive_identity_zero,
existence_of_difference
]

axioms.extend(p(i) for i in range(2,7) for p in [divide_by_natural, remainder_mod_natural, zero_not_one_mod_natural])

# Testing the parser on the provided examples

for p in axioms:
    disp(p)

disp(modus_podens('¬⇒p[0]¬⇒p[0]p[1]'))
disp(existential_instantiation('⇒∃x[0]p[0]p[1]'))
disp(existential_generalization('⇒'+associativity_of_plus+'p[1]','x[0]'))

for p in axioms:
    print(parse(p))
