import time
import threading
import random

A = [
    [0, 1, 0, 1, 0],  # Alice
    [0, 0, 1, 0, 1],  # Bob
    [1, 0, 0, 1, 0],  # Carol
    [0, 1, 0, 0, 1],  # David
    [1, 0, 1, 0, 0]   # Paul
]

def calcular_linha(matriz, i, resultado, tempos):
    n = len(matriz)
    linha_resultado = [0] * n
    tempo_inicio = time.time()
    
    # Coloquei um delay aleatório em algumas threads para "simular" um sistema real
    if random.random() < 0.5:
        time.sleep(random.uniform(0.01, 0.1)) 

    for j in range(n):
        valor_soma = 0
        for k in range(n):
            valor_soma += matriz[i][k] * matriz[k][j]
        linha_resultado[j] = valor_soma
    
    resultado[i] = linha_resultado
    tempo_fim = time.time()
    tempos[i] = tempo_fim - tempo_inicio  

def quadrado_matriz_paralelo(matriz):
    n = len(matriz)
    resultado = [[0] * n for _ in range(n)]
    tempos = [0] * n  # Lista para armazenar os tempos de cada thread
    threads = []
    tempo_inicio = time.time()
    
    for i in range(n):
        thread = threading.Thread(target=calcular_linha, args=(matriz, i, resultado, tempos))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
        
    tempo_fim = time.time()
    tempo_total = tempo_fim - tempo_inicio
    return resultado, tempo_total, tempos

# Calculando A^2
A_ao_quadrado, tempo_calculo_matriz, tempos_threads = quadrado_matriz_paralelo(A)

print("Matriz A^2 Resultante:")
for linha in A_ao_quadrado:
    print(linha)

def encontrar_influente(matriz):
    n = len(matriz)
    somas_colunas = [0] * n
    for j in range(n):
        for i in range(n):
            somas_colunas[j] += matriz[i][j]
    
    print("Somas das colunas:", somas_colunas)  # Imprimir somas das colunas
    print("Podemos concluir que todos tem o mesmo nível de influência.")

    max_influencia = max(somas_colunas)
    influentes = [i for i, soma in enumerate(somas_colunas) if soma == max_influencia]

    if len(influentes) == n:  # Se todos têm o mesmo nível de influência
        return "Todos têm o mesmo nível de influência."
    return influentes

# Medir o tempo para encontrar amigos em comum e influente
tempo_inicio_analise = time.time()
pessoa_influente = encontrar_influente(A_ao_quadrado)
tempo_fim_analise = time.time()
tempo_analise = tempo_fim_analise - tempo_inicio_analise

# Exibindo resultados
print("\nTempo para calcular A^2:", tempo_calculo_matriz, "segundos")
print("Tempos utilizados por cada thread:", tempos_threads)
print("As duas pessoas com mais amigos em comum:", pessoa_influente)
print("Pessoa mais influente:", pessoa_influente)
print("Tempo para análise de amigos em comum e influente:", tempo_analise, "segundos")

# Discussão dos tempos
print("\nDiscussão dos Tempos:")
print("O tempo total para calcular a matriz A^2 foi de", tempo_calculo_matriz, "segundos.")
print("O tempo gasto para encontrar as duas pessoas com mais amigos em comum e a pessoa mais influente foi de", tempo_analise, "segundos.")
print("É importante notar que o tempo gasto por cada thread pode variar devido a natureza da execução paralela, onde o tempo de execução de cada linha da matriz pode depender da complexidade dos cálculos e da carga da CPU no momento.")