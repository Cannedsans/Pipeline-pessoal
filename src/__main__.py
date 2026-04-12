import yaml, os

# Carregamento das configurações da pipeline

configs = {}

for file in os.listdir('config/'):
    path = os.path.join('config', file)
    
    with open(path, 'r') as conf:
        name = os.path.splitext(file)[0]
        data = yaml.safe_load(conf)
        configs[name] = data
        
# Sessão de teste das configurções
# execute: "uvr src/__main__.py" para conferir se as configurações foram carregadas
if __name__ == "__main__":
    print(configs)