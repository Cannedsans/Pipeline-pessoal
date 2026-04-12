from src import  __main__
from src.extract import extract_data
from src.transform import transform_data
from src.load import load_data

modelConf = __main__.configs['model']
pathConf = __main__.configs['paths']

if __name__ == "__main__":
    print("Iniciando pipeline!")
    
    extract_data(pathConf['input'],pathConf['output'])
    
    print("Dados extraidos, iniciando a classificação por IA")
    
    dados_pipeline = transform_data(modelConf['model'],modelConf['machine'],modelConf['labels'])
    
    print("Inicinado salvamento dos dados em um csv!")
    
    load_data(dados_pipeline, pathConf['output'])