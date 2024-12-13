import json

def contar_departamentos(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    count = 0

    def verificar_valor(value):
        nonlocal count
        if isinstance(value, str) and (value.startswith('DEPARTAMENTO') or value.startswith('DEPTO')):
            count += 1

    for value in data.items():
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    for v in item.values():
                        verificar_valor(v)
                else:
                    verificar_valor(item)
        else:
            verificar_valor(value)

    return count

if __name__ == "__main__":
    filepath = 'teste/opcoes_formulario.json'
    total = contar_departamentos(filepath)
    print(f"Total de valores que começam com 'DEPARTAMENTO' ou 'DEPTO': {total}")
