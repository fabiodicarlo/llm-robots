from gpt4all import GPT4All
import matplotlib.pyplot as plt
import time
import cpuinfo
from data.accuracy import calculate_json_value_similarity
# Test da effettuare (easy, medium, hard)
from data.easy import requests, correct_answers

y = []
x = []

for model in GPT4All.list_models():
    name_model = model['filename']

    similarity_percentage = 0
    try:
        gptj = GPT4All(name_model)
    except:
        continue

    var = 0
    req_count = 0
    while True:
        req = requests(req_count)
        req_count += 1
        if req is None:
            break
        try:
            var += 1
            file_size = int(model['filesize']) / (1024 * 1024 * 1024)
            start_time = time.time()
            result = gptj.generate(req)
            end_time = time.time()
            elapsed_time = end_time - start_time
            if elapsed_time < 1: continue
            similarity_percentage += calculate_json_value_similarity(req(req_count), correct_answers(req_count))
        except:
            continue
    if var > 0:
        y.append(name_model)
        x.append(similarity_percentage / var)

# Creazione del grafico a barre verticale
colors = ['red', 'blue', 'green', 'yellow', 'orange']

fig, ax = plt.subplots(figsize=(10, 6))  # Imposta la dimensione della figura
bars = ax.bar(y, x, color=colors[:len(y)])  # Barre verticali con colori diversi

# Impostazione delle etichette dell'asse x
plt.xlabel("Model name")
# Rotazione e allineamento delle etichette sull'asse x
plt.xticks(rotation=45, ha='right')

# Impostazione delle etichette dell'asse y
plt.ylabel("Accuracy (%)")
plt.title(cpuinfo.get_cpu_info()['brand_raw'] + ' (' + cpuinfo.get_cpu_info()['arch'] + ') - Family: ' + str(
    cpuinfo.get_cpu_info()['family']))

# Ottimizza la disposizione del grafico per evitare sovrapposizioni
plt.tight_layout()

plt.savefig('easy_req_accuracy.png')
plt.close()
