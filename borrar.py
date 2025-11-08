def parsear_valor(valor: str):

    if valor.isdigit(): 
        int(valor)
    
    elif "." or "," in valor: 
        float(valor)
    
    return valor

numero = '3.14' 
parsear_valor(numero)
print(type(numero))