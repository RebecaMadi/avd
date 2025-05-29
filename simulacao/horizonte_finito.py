"""
Nome: Rebeca Madi Oliveira
Matrícula: 22400981

Instruções para a execução:
- Crie um ambiente virtual python: python -m venv avd
- Ative o ambiente: source avd/bin/activate
- Instale as bibliotecas: 
    - pip install matplotlib  
    - pip install scipy
"""

import random
import math
import matplotlib.pyplot as plt
from scipy import stats

confianca = 0.95
lmbda = 9
mu = 10

def valor_aleatorio(taxa):
    u = random.random()
    return -math.log(1 - u) / taxa

def mm1(n):
    tempos_chegada = []
    tempos_execucao = []
    tempo = 0

    for _ in range(n):
        chegada = valor_aleatorio(lmbda)
        tempo += chegada
        tempos_chegada.append(tempo)
        execucao = valor_aleatorio(mu)
        tempos_execucao.append(execucao)

    tempos_inicio = [0.0] * n
    tempos_fim = [0.0] * n
    tempos_espera = [0.0] * n

    for i in range(n):
        if i == 0:
            tempos_inicio[i] = tempos_chegada[i]
        else:
            tempos_inicio[i] = max(tempos_chegada[i], tempos_fim[i - 1])
        tempos_fim[i] = tempos_inicio[i] + tempos_execucao[i]
        tempos_espera[i] = tempos_inicio[i] - tempos_chegada[i]

    return tempos_espera

def ic_t_student(tempos):
    tam_amostra = len(tempos)
    media_amostra = sum(tempos) / tam_amostra
    soma_quadrados = sum((x - media_amostra) ** 2 for x in tempos)
    dp_amostra = (soma_quadrados / (tam_amostra - 1)) ** 0.5
    erro_padrao = dp_amostra / (tam_amostra ** 0.5)
    intervalo = stats.t.interval(confianca, tam_amostra - 1, loc=media_amostra, scale=erro_padrao)
    h = (intervalo[1] - intervalo[0]) / 2
    return media_amostra, h, intervalo

def simulacao():
    print("SIMULAÇAO HORIZONTE FINITO")
    print(f"Valor da taxa de entrada: {lmbda}")
    print(f"Valor da taxa de serviço: {mu}")

    valor_esperado = lmbda / (mu * (mu - lmbda))
    tamanhos = [10**3, 10**5, 10**7, 10**8]
    medias = []
    H = []

    for n in tamanhos:
        print(f"\nSimulando para n = {n}...")
        tempos = mm1(n)
        media, h, ic = ic_t_student(tempos)

        print(f"Tempo médio de espera: {media:.5f} s")
        print(f"Intervalo de confiança 95%: ({ic[0]:.5f}, {ic[1]:.5f})")
        print(f"Tempo esperado (teórico): {valor_esperado:.5f} s")

        medias.append(media)
        H.append(h)

    plt.errorbar(tamanhos, medias, yerr=H, fmt='o-', capsize=5, label='Simulação')
    plt.xscale('log')
    plt.axhline(y=valor_esperado, color='r', linestyle='--', label='Valor teórico')
    plt.xlabel('Tamanho da amostra (10^n)')
    plt.ylabel('Tempo médio de espera')
    plt.title('Convergência da média do tempo de espera na fila M/M/1')
    plt.legend()
    plt.grid(True)
    plt.show()



simulacao()
