"""
Nome: Rebeca Madi Oliveira
Matrícula: 22400981

Instruções para a execução:
- Crie um ambiente virtual python: python -m venv avd
- Ative o ambiente: source avd/bin/activate
- Instale as bibliotecas: 
    - pip install scipy
"""

import random
import math
from scipy import stats

confianca = 0.95
lmbda = 9
mu = 10

def valor_aleatorio(taxa):
    u = random.random()
    return -math.log(1 - u) / taxa

def gerar_cliente():
    chegada = valor_aleatorio(lmbda)
    servico = valor_aleatorio(mu)
    return chegada, servico

def processar_cliente(tempo_chegada, tempo_execucao, tempo_ultimo_fim):
    tempo_inicio = max(tempo_chegada, tempo_ultimo_fim)
    tempo_fim = tempo_inicio + tempo_execucao
    tempo_espera = tempo_inicio - tempo_chegada
    return tempo_fim, tempo_espera

def ic_t_student(tempos):
    tam_amostra = len(tempos)
    media_amostra = sum(tempos) / tam_amostra
    soma_quadrados = sum((x - media_amostra) ** 2 for x in tempos)
    dp_amostra = (soma_quadrados / (tam_amostra - 1)) ** 0.5
    erro_padrao = dp_amostra / (tam_amostra ** 0.5)
    intervalo = stats.t.interval(confianca, tam_amostra - 1, loc=media_amostra, scale=erro_padrao)
    h = (intervalo[1] - intervalo[0]) / 2
    return media_amostra, h, intervalo

def simulacao_chow_robbins(d):
    print(f"\n--- Simulando para d = {d} ---")

    tempo_atual = 0
    fim_anterior = 0
    tempos_espera = []

    n = 0
    h = float('inf')

    while n < 30 or h > d:
        chegada, servico = gerar_cliente()
        tempo_atual += chegada
        fim_anterior, espera = processar_cliente(tempo_atual, servico, fim_anterior)
        tempos_espera.append(espera)
        n += 1

        if n >= 30:
            media, h, ic = ic_t_student(tempos_espera)

    print(f"Tempo médio de espera: {media:.5f} s")
    print(f"Intervalo de confiança 95%: ({ic[0]:.5f}, {ic[1]:.5f})")
    print(f"Número de clientes simulados (n): {n}")
    return n, media, h, ic

def main():
    print("SIMULAÇÃO COM HORIZONTE INFINITO E PARADA DE CHOW E ROBBINS")
    print(f"Taxa de chegada (λ): {lmbda}")
    print(f"Taxa de serviço (μ): {mu}")
    valor_esperado = lmbda / (mu * (mu - lmbda))
    print(f"Tempo médio de espera teórico: {valor_esperado:.5f} s")

    ds = [1, 0.5, 0.1, 0.05]
    for d in ds:
        simulacao_chow_robbins(d)

if __name__ == "__main__":
    main()


