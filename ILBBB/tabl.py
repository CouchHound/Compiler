from my_parser import parsing as ps


def check_same_names(var):
    for key in simbol_table:
        for type in simbol_table[key]:
            if var in simbol_table[key][type]:
                return False
    return True


def table(tree):
    global simbol_table
    for part in tree.parts:
        if type(part) != str and type(part) != int and type(part) != float:
            if part.type == 'Var' or part.type == 'parameter_list':
                for i in part.parts:
                    if i.type == 'Type':
                        type_tmp = i.parts[0]
                    if i.type == 'ID':
                        if part.scope not in simbol_table.keys():
                            simbol_table[part.scope] = {}
                            simbol_table[part.scope][type_tmp] = []
                        elif type_tmp not in simbol_table[part.scope].keys():
                            simbol_table[part.scope][type_tmp] = []
                        for j in i.parts:
                            if check_same_names(j):
                                simbol_table[part.scope][type_tmp].append(j)
                            else:
                                print("Названия переменных должны быть разными!!!")
            table(part)


def get_table(init_prog):
    global simbol_table
    simbol_table = {}
    with open(init_prog, 'r') as f:
        s = f.read()

    result = ps().parse(s)
    # print(result)
    table(result)

    return simbol_table


if __name__ == "__main__":
    simbol_table = {}
    a = '''

var int y, z, p;

func ONE(int b){
    while (b < 10){
        b = b + 10;
    }
    return b
}

y = 2;
p = 3;
z = ONE(p);
while(y < 20){
    y = y + p;
    if(p == 3) then {
        while(p<10){
            p = p+2;
        }
    }
}
print(z);
print(p);
print(y);

    '''
    s = '''
    var int n, f;
    n = 10;
    f = 1;

    while (n > 1){
        f = f * n;
        n = n - 1;
    }

    print(f);


    '''

    result = ps().parse(a)
    print(result)
    table(result)

    for key in simbol_table:
        print(key, ':')
        for i in simbol_table[key]:
            print('\t', i, '= ', simbol_table[key][i])
