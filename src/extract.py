import os
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

tempPath = "data/tmp"

def extract_data(inputPath, outputPath):
    print("iniciando o pipeline!")
    os.makedirs(inputPath, exist_ok=True)
    os.makedirs(tempPath, exist_ok=True)
    os.makedirs(outputPath, exist_ok=True)

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
    
    print("Dados extraidos com sucesso!")