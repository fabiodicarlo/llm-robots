import json
from difflib import SequenceMatcher
import re


def get_json(string):
    try:
        start_index = string.find("json") + len("json")
        end_index = string.find("```", start_index)
        json_string = string[start_index:end_index].strip()
        json_string = json_string.replace("'", "\"")
    except:
        # Se si verifica un errore, provo a trovare il JSON senza considerare il tag "json"
        start_index = string.find("{")
        end_index = string.find("}", start_index) + 1
        json_string = string[start_index:end_index].strip()
        json_string = json_string.replace("'", "\"")

    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        print("Errore durante il parsing del JSON:", str(e))
        return None


def calculate_similarity_ratio(string1, string2):
    return SequenceMatcher(None, string1, string2).ratio()


def calculate_json_value_similarity(json_string, req):
    try:
        # Tentativo di caricare la stringa come JSON
        json_object = get_json(json_string)

        # Calcola la percentuale di somiglianza dei valori rispetto all'array input_strings
        value_similarities = []

        input_json = json.loads(req)
        similarity_ratios = []
        for key in input_json:
            input_value = input_json[key]
            json_value = json_object.get(key, "")
            value_similarity = calculate_similarity_ratio(str(json_value).lower(), str(input_value).lower()) * 100
            similarity_ratios.append(value_similarity)
        value_similarity = sum(similarity_ratios) / len(similarity_ratios)
        value_similarities.append(value_similarity)

        # Calcola la media delle percentuali di somiglianza dei valori
        values_similarity = sum(value_similarities) / len(value_similarities)
        return values_similarity
    except (ValueError, TypeError):
        print("Errore", TypeError)
        return 0
