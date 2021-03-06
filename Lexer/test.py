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

    #f_write = file(fout, 'w')

    print "Token  \tOccurences  \tLexemes"
    for key in toklist_key.keys():
        if(toklist_key[key][0] == '\n'):
            print("%s  \t%s  \t%s" %(key, len(toklist_key[key]) , "\\n" ))
        else:
            print("%s  \t%s  \t%s" %(key, len(toklist_key[key]) , toklist_key[key].pop() ))

        for value in toklist_key[key]:
            if(key[0:7]=="NEWLINE"):
                continue
            if(key[0:3]=="KW_"):
                continue
            if key == "WSPACE_LIT":
                continue
            if key == "NEWLINE":
                continue
            if key == "PARALEFT":
                continue        
            if key == "PARARIGHT":
                continue
            if key == "PARALSQUARE":
                continue
            if key == "PARARSQUARE":
                continue
            if key == "PARALCURLY":
                continue
            if key == "PARARCURLY":
                continue
            if key == "SQUOTES":
                continue
            if key == "DQUOTES":
                continue                            
            print("  \t \t \t  %s" %(value ) )    

    return toklist_key
            
                


    
