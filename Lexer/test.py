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


def Print(lexer,fin):
    data = file(fin,'r').read()
    lexer.input(data)

    toklist_key = {}
    #toklist_value =         
    
    while True:
        tok = lexer.token()
        if not tok:
            break
        if tok.type not in toklist_key.keys():
            toklist_key[tok.type] = [tok.value]
        else:
            toklist_key[tok.type].append(tok.value)

    return toklist_key
            
                


    
