import re
import sys

row = 1
transition = [0, 0]

###########################diccionarios###################################
operators = {
    '~' : 'token_neg',
    '=' : 'token_igual',
    '+' : 'token_mas',
    '-' : 'token_menos',
    '*' : 'token_mul',
    '%' : 'token_mod',
    ';' : 'token_pyc',
    ':' : 'token_dosp',
    '(' : 'token_par_izq',
    ')' : 'token_par_der',
    '[' : 'token_cor_izq',
    ']' : 'token_cor_der',
    '|' : 'token_o',
    '&' : 'token_y',
    ',' : 'token_coma',
    '^' : 'token_pot'
    }

reserved_words = {'proceso':'proceso',
              'caracter':'caracter',
              'numerico':'numerico',
              'numero':'numero',
              'texto':'texto',
              'cadena':'cadena',
              'verdadero':'verdadero',
              'falso':'falso',
              'hasta':'hasta',
              'dimension':'dimension',
              'inproceso':'inproceso',
              'definir':'definir',
              'como':'como',
              'segun':'segun',
              'no':'token_neg',
              'mod':'token_mod',
              'de':'de',
              'otro':'otro',
              'modo':'modo',
              'subalgoritmo':'subalgortimo',
              'logico':'logico',
              'entero':'entero',
              'real':'real', 
              'caracter':'caracter',
              'si':'si',
              'entonces':'entonces',
              'sino':'sino',
              'para':'para',
              'con':'con',
              'paso':'paso',
              'hacer':'hacer',
              'mientras':'mientras',
              'funcion':'funcion',
              'finproceso':'finproceso',
              'finsegun':'finsegun',
              'finsubproceso':'finsubproceso',
              'finsubalgoritmo':'finsubalgoritmo',
              'finfuncion':'finfuncion',
              'hasta':'hasta',
              'que':'que',
              'limpiar':'limpiar',
              'borrar':'borrar',
              'pantalla':'pantalla',
              'esperar':'esperar',
              'tecla':'tecla',
              'segundos':'segundos',
              'milisegundos':'milisegundos',
              'rc':'rc',
              'sen':'sen',
              'cos':'cos',
              'tan':'tan',
              'asen':'asen',
              'acos':'acos',
              'atan':'atan',
              'redon':'redon',
              'aleatorio':'aleatorio',
              'longitud':'longitud',
              'mayusculas':'mayusculas',
              'minusculas':'minusculas',
              'subcadena':'subcadena',   
              'concatenar':'concatenar',
              'convertiranumero':'convertianumero',
              'convertiratexto':'convertiratexto',
              'finsi':'finsi',
              'finpara':'finpara',
              'finmientras':'finmientras',
              'subproceso':'subproceso',
              'repetir':'repetir',
              'escribir':'escribir',
              'leer':'leer',
              'dimension':'dimension',
              'algoritmo':'algoritmo',
              'finalgoritmo':'finalgoritmo',
              'abs' : 'abs',
              'exp' : 'exp',
              'otro':'otro',
              'o':'token_o',
              'y':'token_y',
              'ln':'ln'}


def tokenizer(char, column, state): #método analizador (automáta)
    global lexema
    global line
    if state == 0: #Estado inicial
        
        if re.match(r'["\']',char) : #cadenas no especificas => cadena
            lexema= ""
            return [4, 0]
        
        elif char == '': #Vacio         
            print(">>> Error lexico (linea: " + str(row) + ", posicion: " + str(column) + ")")
            exit(0)
        # operadores especiales
        elif char == '(':
            print("<token_par_izq,"+str(row)+","+str(column)+">")
            return [0, 0]
        elif char == ')':
            print("<token_par_der," + str(row) + "," + str(column) + ">")
            return [0, 0]
        elif char == '[':
            print("<token_cor_izq," + str(row) + "," + str(column) + ">")
            return [0, 0]
        elif char == ']':
            print("<token_cor_der," + str(row) + "," + str(column) + ">")
            return [0, 0]
        elif re.match(r'[@.?$#ÑñÁáÉéÍíÓóÚúäÄëËïÏöÖüÜ$!]', char):#Verificación de eñes,acentos y dieresis  
                print(">>> Error lexico (linea: " + str(row) + ", posicion: " + str(column) + ")")
                exit(0)                
        elif char in operators:  #Verificación de operadores
            print("<"+operators[char]+ "," + str(row) + "," + str(column)  + ">")
            return [0, 0]
        elif char == '/':
            return [1, 0]
        elif char == '>':
            return [2, 0]
        elif char == '<':
            return [3, 0]
        elif re.match(r'[a-z,_]', char) or re.match(r'[A-Z,_]', char): #palabras
            lexema=char.lower()
            return [5, 0]
        elif re.match(r'[0-9]', char): #numeros
            lexema= char
            return [6, 0]
        else:
            return [0, 0]

    if state == 1:
        if char == '/':
            line = ""
            return [0, 0]
        else:
            print("<token_div," + str(row) + "," + str(column-1) + ">")
            state = 0
            return [0, 1]
    if state == 2: # Estado 
        if char == '=':
            print("<token_mayor_igual," + str(row) + "," + str(column-1) + ">")
            return [0, 0]
        else:
            print("<token_mayor," + str(row) + "," + str(column-1) + ">")
            state = 0
            return [0, 1]

    if state == 3:
        if char == '=':
            print("<token_menor_igual," + str(row) + "," + str(column - 1) + ">")
            return [0,0]
        elif char == '-':
            print("<token_asig,"+ str(row) + "," + str(column - 1) + ">")
            return [0,0]
        elif char == '>':
            print("<token_dif,"+ str(row) + "," + str(column - 1) + ">")
            return [0,0]
        else:
            print("<token_menor," + str(row) + "," + str(column - 1) + ">")
            return [0,1]
      
    if state == 4:
        if char=='"':
            print("<token_cadena," + lexema+ "," + str(row) + "," + str(column-len(lexema)-1) + ">")
            return[0, 0]
        elif char == "'":
            print("<token_cadena," + lexema+ "," + str(row) + "," + str(column-len(lexema)-1) + ">")
            return[0, 0]
        else:
            lexema= lexema+ char
            return [4, 0]

    if state == 5:
        if re.match(r'[a-z_]', char) or re.match(r'[A-Z_]', char) or re.match(r'[0-9]', char):
            lexema= lexema+ str.lower(char)
            return[5, 0]
          
        else:
            if lexema in reserved_words:
                print("<"+reserved_words[lexema]+ "," + str(row) + "," + str(column - len(lexema)) + ">")    
            else:
                print("<id," + lexema+ "," + str(row) + "," + str(column - len(lexema)) + ">")
            return [0, 1]

    if state == 6:
        if re.match(r'[0-9]', char):
            lexema= lexema+ char
            return [6, 0]
        elif char == '.':
            lexema= lexema+ char
            return [7, 0]
        elif re.match(r'[a-z_@?$#ÑñÁáÉéÍíÓóÚúäÄëËïÏöÖüÜ$!]', char) or re.match(r'[A-Z_@?$#ÑñÁáÉéÍíÓóÚúäÄëËïÏöÖüÜ$!]', char):
            print(">>> Error lexico (linea: " + str(row) + ", posicion: " + str(column) + ")")
            exit(0)
        else:
            print("<token_entero," + lexema+ "," + str(row) + "," + str(column - len(lexema)) + ">")
            return [0, 1]

    if state == 7:
        if re.match(r'[0-9]', char):
            lexema= lexema+ char
            return[8, 0]
        else:
            print("<token_entero," + lexema[0:len(lexema)-1] + "," + str(row) + "," + str(column - len(lexema)) + ">")
            return[0, 2]

    if state == 8:
        if re.match(r'[0-9]', char):
            lexema= lexema+ char
            return[8, 0]
        else:
            print("<token_real," + lexema+ "," + str(row) + "," + str(column - len(lexema)) + ">")
            return [0, 1]


lines = sys.stdin.readlines() 


for line in lines:
    i = 0
    line = line+" "

    while i < len(line):
        transition = tokenizer(line[i], i+1,  transition[0])
        i = i + 1 - transition[1]
    if transition[0] == 4:
        print(">>> Error lexico (linea: " + str(row) + ", posicion: " + str(i-len(lexema)) + ")")
        exit(0)
        
    row += 1