from sets import Set

def test(lexer):
    
    fname = "Scala.txt"
    data = file(fname, 'r').read()
    
    lexer.input(data)
    
    toklist_key = Set([])
    toklist_value = Set([])
    
    while True:
        tok = lexer.token()
        if not tok:
            break
        toklist_key.add(tok.type)
        toklist_value.add(tok.value)
    return (toklist_key,toklist_value)

    
