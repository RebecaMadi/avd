"""
Nome: Rebeca Madi Oliveira
Matricula: 22400981

Trabalho 1 - Projeto 2^kr fatorial
"""

f_names = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E"}
r_names = {1: "yi1", 2: "yi2", 3: "yi3"}
er_names = {1: "ei1", 2: "ei2", 3: "ei3"}

def gen_combinacoes(fatores: int, labels: list):
    qnt_comb = 2**fatores

    combinacoes = {}
    
    conts = []
    conts2 = []
    values = []

    for i in range(0, len(labels), 1):
        combinacoes[labels[i]] = []
        conts.append(2**(i))
        conts2.append(0)
        values.append(-1)

    for i in range(1, qnt_comb+1, 1):
        combinacoes["I"].append(1)
        for j in range(1, fatores+1, 1):
            combinacoes[labels[j]].append(values[j-1])
            conts2[j-1] += 1
            if conts2[j-1] == conts[j-1]:
                values[j-1] *= -1
                conts2[j-1] = 0

        for j in range(fatores+1, len(labels), 1):
            mult = 1
            for l in labels[j]:
                mult *= combinacoes[l][i-1]
            combinacoes[labels[j]].append(mult)

    return combinacoes


def get_labels(fatores):
    labels_list = []
    labels_dict = {}

    for i in range(1, fatores+1, 1):
        labels_dict[f_names[i]] = 1
        labels_list.append(f_names[i])

    size = 1
    while(size<fatores):
        aux = []
        for label in labels_list:
            for l in labels_list:
                col = "".join(sorted(label+l))
                if len(label) == 1 and label not in l and col not in labels_dict.keys():
                    aux.append(col)
                    labels_dict[col] = 1
        labels_list = labels_list+aux
        size += 1        
    
    return ["I"] + labels_list


def get_header(labels, replicas, space, ym):
    header = "|"
    for label in labels:
        header += " "*space + f"{label} |"
    
    for i in range(1, replicas+1, 1):
        header +=  " "*space +  f"{r_names[i]} |"

    if ym is True:
        header += " "*space + "y_estim |"

    return len(header)*"-" + "\n" + header + "\n" + len(header)*"-"


def get_table_body(fatores, replicas, combinacoes, y, ym):
    comb = combinacoes.keys()
    comb_s = ""

    for i in range(1, 2**fatores + 1, 1):
        comb_s += "|"
        for c in comb:
            tam = len(c) + 3
            tam -= max(0, 1 + len(f"{combinacoes[c][i-1]}"))

            comb_s += " "*tam + f"{combinacoes[c][i-1]} |"
        
        for j in range(0, replicas, 1):
            if y is None:
                comb_s += "    ? |"
            else:
                tam = len(r_names[j+1]) + 3
                tam -= max(0, 1 + len(f"{y[i-1][j]}"))

                comb_s += " "*tam + f"{y[i-1][j]} |"

        if ym is not None:
            tam = 10
            tam -= max(1 + len(f"{ym[i-1]}"), 0)

            comb_s += " "*tam + f"{ym[i-1]} |"
        comb_s += "\n"
    return comb_s


def get_combinacoes(fatores: int, replicas: int):
    labels = get_labels(fatores)
    header = get_header(labels, replicas, 2, False)

    print("\nTABELA DE SINAIS E VALORES MEDUDIS: ")
    print(header)

    combinacoes = gen_combinacoes(fatores, labels)
    
    comb_s = get_table_body(fatores, replicas, combinacoes, None, None)
    print(comb_s)

    return labels, combinacoes


def ler_medidas(fatores: int):
    yis = []

    print("Informe os valores medidos: \nEx: yi1 .. yi3 \n")
    for i in range(0, 2**fatores, 1):
        medidas = (input(f"Informe os valores medidos em cada repetição no exmperimento {i+1}: ")).split(" ")
        medidas = [int(m) for m in medidas]
        yis.append(medidas)
    
    return yis


def get_mean_y(y: list, r: int):
    ans = []
    for yi in y:
        ans.append(round(sum(yi)/r, 2))
    return ans


def get_efeitos(labels, combinacoes, y, fatores):
    efeitos = []
    exp = 2**fatores

    for label in labels:
        aux = 0
        for i in range(0, exp, 1):
            aux += combinacoes[label][i]*y[i]
        efeitos.append(round(aux/4, 2))
    
    return efeitos


def get_efeitos_string(labels, efeitos):
    ef_s = "-"*20 + "\n" + "| EFEITOS:         |\n" + "-"*20 + "\n"

    for i in range(0, len(efeitos), 1):
        tam = max(6 - len(labels[i]), 0)
        ef_s += "|" + " "*tam + f"{labels[i]} |"
        tam = max(9 - len(str(efeitos[i])), 0)

        ef_s += " "*tam + f"{efeitos[i]} |\n"
    return ef_s


def  get_erros(ym, y, fatores):
    exp = 2**fatores
    erros = []

    for i in range(0, exp, 1):
        aux = []
        for yij in y[i]:
            aux.append(round(yij - ym[i], 2))
        erros.append(aux)

    return erros


def get_erros_string(erros, r, k):
    exp = 2**k
    err_s = "|      I |"

    for i in range(1, r+1, 1):
        err_s += " "*4 + er_names[i] + " |"
    
    err_s = "-"*len(err_s) +"\n"+ err_s + "\n" + "-"*len(err_s) + "\n"

    for i in range(0, exp, 1):
        tam = max(8 - len(str(i+1)) - 1, 0)
        err_s += "|" + " "*tam + str(i+1) + " |"
        for j in range(0, r, 1):
            tam = max(7 - len(str(erros[i][j])), 0)
            err_s += " "*tam + str(erros[i][j]) + " |"
        err_s += "\n"
    
    return err_s


def get_ss(efeitos, erros, k, r):
    ss = []

    for i in range(1, len(efeitos)):
        ss.append(round((2**k)*r*(efeitos[i]**2), 2))
    
    sse = 0
    for i in range(2**k):
        for j in range(r):
            sse += erros[i][j]**2
    
    ss.append(round(sse, 2))

    return ss


def get_ss_string(ss, labels):
    sst = round(sum(ss), 2)

    ss_s = "-"*31 + "\n" 
    ss_s += "|" + " "*9 + "|" + " "*3 + "ABS" + " "*3 + "|" + " "*4 + "%" + " "*4 + "|\n"
    ss_s += "-"*31 + "\n" 
    ss_s += "|     SST |"
    tam = max(8 - len(str(sst)), 0)
    ss_s += " "*tam + str(sst) + " |    100% |\n"

    size = len(labels)

    for i in range(1, size, 1):
        ss_s += "|"
        tam = 8 - len("SS"+labels[i])
        ss_s += " "*tam + "SS" + labels[i] + " |"
        tam = max(8 - len(str(ss[i-1])), 0)
        ss_s += " "*tam + str(ss[i-1]) + " |"
        pct = round((ss[i-1]/sst)*100, 2)
        tam = max(7 - len(str(pct)), 0)
        ss_s += " "*tam + str(pct) + "% |\n"
    
    ss_s += "|     SSE |"
    tam = max(8 - len(str(ss[size-1])), 0)
    ss_s += " "*tam + str(ss[size-1]) + " |"
    pct = round((ss[size-1]/sst)*100, 2)
    tam = max(7 - len(str(pct)), 0)
    ss_s += " "*tam + str(pct) + "% |\n"

    return ss_s


def main():
    header_projec = "       Projeto 2^kr Fatorial       "
    print("\n" + len(header_projec)*"-" + "\n" + header_projec + "\n" + len(header_projec)*"-")
    
    fatores = int(input("Informe a quantidade de fatores (2 a 5): "))
    replicas = int(input("Informe a quantidade de replicas (1 a 3): "))

    if(fatores <2 or fatores>5 or replicas <1 or replicas>3):
        print("A entrada informada não é válida!")
    
    log =  ""
    labels, combinacoes = get_combinacoes(fatores, replicas)   

    y_medidos = ler_medidas(fatores)
    y_media = get_mean_y(y_medidos, replicas)
    
    efeitos = get_efeitos(labels, combinacoes, y_media, fatores)

    header = get_header(labels, replicas, 2, True)
    enum = "\nTABELA DE SINAIS E VALORES MEDUDOS E ESTIMADOS: \n"
    comb_s = get_table_body(fatores, replicas, combinacoes, y_medidos, y_media)
    print(enum + header + "\n" + comb_s)

    log += enum + header + "\n" + comb_s

    ef_s = get_efeitos_string(labels, efeitos)
    enum = "\nVALORES DOS EFEITOS: \n"
    print(enum + ef_s)

    log += enum + ef_s

    erros = get_erros(y_media, y_medidos, fatores)
    err_s = get_erros_string(erros, replicas, fatores)
    enum = "\nERROS EXPERIMENTAIS: \n"
    print(enum + err_s)

    log += enum + err_s

    ss = get_ss(efeitos, erros, fatores, replicas)
    ss_s = get_ss_string(ss, labels)
    enum = "\nPORÇÃO DE VARIAÇÃO:\n"
    print(enum + ss_s)

    log += enum + ss_s

    print("Informações salvas em log.txt!\n")
    with open("log.txt", "w", encoding="utf-8") as arquivo:
        arquivo.write(log)


if __name__ == "__main__":
    main()