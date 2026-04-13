# Pipeline pessoal

Exemplo simples de pipeline de dados local, permite a extração e categorização de elementos de arquivos `.md` e `.pdf` e realizar nomeação de entidade rotulada (NER).

## Funcionamento

por padrão uma estrutura com as seguintes pastas, uma pasta onde arquivos serão inseridos, uma pasta de arquivos temporários onde os dados brutos serão armazenados, e uma pasta de output onde os arquivos serão armazenados em formato `.csv`

```
📂 data
├── 📂 input
├── 📂 output
└── 📂 tmp
```

## Configuração

existem 2 arquivos de configuração, um focado nos caminhos, onde as pastas de input e output podem ser configuradas e um arquivo para condiguração do modelo com base no **gliner**, com os campos:

* Qual o modelo que será utilizado.
* Qual máquina (cpu, gpu, etc etc) será usada.
* quais os rótulos queremos para as entidades.