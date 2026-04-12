import pandas as pd

unicos_texto = set()
unicos_list = []

def load_data(all_pipeline_entities, outputPath='data/output'):    
    for entity in all_pipeline_entities:
        text = entity["text"].strip().lower()
        label = entity["label"].strip().lower()
        
        if text not in unicos_texto:
            unicos_texto.add(text)
            
            unicos_list.append({
                'entidade': entity["text"],
                'rótulo': entity["label"],
                'confiança': entity["score"],
                'Arquivo Fonte': entity.get('source_file', 'N/A')
            })
            
        df_pipeline = pd.DataFrame(unicos_list)
        
        df_pipeline.to_csv(str(outputPath + "/dados.csv"), encoding='utf-8')