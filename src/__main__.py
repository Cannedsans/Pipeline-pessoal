import yaml
import os
from .extract import extract_data
from .transform import transform_data
from .load import load_data

# Se a pasta 'config' estiver dentro de 'src/', usamos isso:
CONFIG_PATH = 'config/'

configs = {}

# Verificação para debug
if not os.path.exists(CONFIG_PATH):
    print(f"ERRO: Pasta não encontrada em: {CONFIG_PATH}")
else:
    for file in os.listdir(CONFIG_PATH):
        if file.endswith('.yml') or file.endswith('.yaml'):
            path = os.path.join(CONFIG_PATH, file)
            with open(path, 'r') as conf:
                name = os.path.splitext(file)[0]
                data = yaml.safe_load(conf)
                configs[name] = data

# 2. Mova o print para FORA do if __name__ == "__main__" para testar no import
# Ou mantenha dentro, mas certifique-se de que o loop acima funcionou.
if __name__ == "__main__":
    print("Executando o __init__.py diretamente:")
    print(f"Arquivos em config: {os.listdir(CONFIG_PATH) if os.path.exists(CONFIG_PATH) else 'Nenhum'}")
    print(f"Configs carregadas: {configs}")

__all__ = ['configs', 'extract_data', 'transform_data', 'load_data']