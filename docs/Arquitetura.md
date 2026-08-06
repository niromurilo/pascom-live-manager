# Arquitetura

## Estrutura atual

- `main.py`: entrada da interface gráfica
- `interface_grafica.py`: tela principal em Tkinter
- `services/preparacao.py`: orquestração da preparação da transmissão
- `buscar_liturgia.py`: busca e extração da liturgia
- `animated_lower_thirds.py`: geração e validação do JSON
- `gerador_descricao.py`: geração de título e descrição
- `paroquia_config.py`: persistência local das configurações da paróquia
- `tests/`: testes automatizados mínimos

## Módulos

- Liturgia
- Animated Lower Thirds
- Preparação da transmissão
- Configuração da paróquia
- Utilitários

## Fluxo atual

Usuário
-> Interface gráfica
-> Serviço de preparação
-> Busca da liturgia
-> Geração de arquivos e JSON
-> Cópia dos logos configurados
-> Import manual do JSON no Animated Lower Thirds
-> OBS
