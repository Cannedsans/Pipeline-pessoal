import os,json, pandas as pd
from gliner import GLiNER

tempPath = "data/tmp"
all_pipeline_entities = []

def transform_data(modelName,machine='cpu',labels=[]):
    print("pipeline executado!, iniciando processamento com IA")
    
    try:
        if 'model' not in locals() or model is None:
            model = GLiNER.from_pretrained(modelName)
            model.to(machine)
    except NameError:
        model = GLiNER.from_pretrained("urchade/gliner_medium-v2.1")
        model.to(machine)
        
    for file in os.listdir(tempPath):
        filepath = os.path.join(tempPath,file)
        
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        for element in data:
            text = element.get("text", "")
            
            if text:
                entities = model.predict_entities(text, labels, threshold=0.7)
                for entity in entities:
                    entity['source_file'] = filepath
                    entity['element_id'] = element.get('element_id')
                    entity['element_type'] = element.get('type')
                    all_pipeline_entities.append(entity)
    
    return all_pipeline_entities