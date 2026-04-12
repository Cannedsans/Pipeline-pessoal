import os,json, pandas as pd
from gliner import GLiNER
from unstructured_ingest.pipeline.pipeline import Pipeline
from unstructured_ingest.interfaces import ProcessorConfig
from unstructured_ingest.processes.connectors.local import (
    LocalIndexerConfig,
    LocalDownloaderConfig,
    LocalConnectionConfig,
    LocalUploaderConfig
)
from unstructured_ingest.processes.partitioner import PartitionerConfig
from unstructured_ingest.processes.filter import FiltererConfig

labels = ["Formato de arquivo", "Ferramenta", "Linguagem de programação"]
all_pipeline_entities = []

inputPath = "input"
outputPath = "output"
tempPath = "tmp"

os.makedirs(inputPath, exist_ok=True)
os.makedirs(tempPath, exist_ok=True)
os.makedirs(outputPath, exist_ok=True)

if __name__ == "__main__":
    Pipeline.from_configs(
        context=ProcessorConfig(),
        indexer_config=LocalIndexerConfig(input_path=inputPath),
        downloader_config=LocalDownloaderConfig(),
        source_connection_config=LocalConnectionConfig(),
        filterer_config=FiltererConfig(
            file_glob=["*.pdf","*.md"],
            max_file_size=10000000
        ),
        partitioner_config=PartitionerConfig(
            partition_by_api=False,
            strategy="fast",
            ocr_languages=["por"],
            additional_partition_args={
                "split_pdf_page": True,
                "split_pdf_allow_failed": True,
                "split_pdf_concurrency_level": 5
            }
        ),
        uploader_config=LocalUploaderConfig(output_dir=tempPath)
    ).run()
    print("pipeline executado!, iniciando processamento com IA")
    
    try:
        if 'model' not in locals() or model is None:
            model = GLiNER.from_pretrained("urchade/gliner_medium-v2.1")
            model.to("cpu")
    except NameError:
        model = GLiNER.from_pretrained("urchade/gliner_medium-v2.1")
        model.to("cpu")
        
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
                    
    print("Procecamento com IA concluído!")               
    
    unicos_texto = set()
    
    unicos_list = []
    
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
        
    print(f"Dados salvos em {outputPath} com sucesso!")