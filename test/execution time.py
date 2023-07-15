from gpt4all import GPT4All
import matplotlib.pyplot as plt
import time
import cpuinfo
from data.easy import requests

n_threads = 28

y = []
x = []
for model in GPT4All.list_models():
    name_model = model['filename']

    try:
        gptj = GPT4All(name_model, n_threads=n_threads)
        start_time = time.time()

        result = gptj.generate(requests(0))
        end_time = time.time()
        elapsed_time = end_time - start_time

        y.append(name_model)
        x.append(elapsed_time)
    except:
        continue


# Creazione del grafico a barre verticale
colors = ['red', 'blue', 'green', 'yellow', 'orange']

# Imposta la dimensione della figura
fig, ax = plt.subplots(figsize=(10, 6))

# Barre verticali con colori diversi
bars = ax.bar(y, x, color=colors[:len(y)])

# Impostazione delle etichette dell'asse x
plt.xlabel("Model name")
# Rotazione e allineamento delle etichette sull'asse x
plt.xticks(rotation=45, ha='right')

# Impostazione delle etichette dell'asse y
plt.ylabel("Execution time (seconds)")
plt.title(cpuinfo.get_cpu_info()['brand_raw'] + ' (' + cpuinfo.get_cpu_info()['arch'] + ') - Family: ' + str(
    cpuinfo.get_cpu_info()['family']))

# Ottimizza la disposizione del grafico per evitare sovrapposizioni
plt.tight_layout()

plt.savefig('execution_time.png')
plt.close()
