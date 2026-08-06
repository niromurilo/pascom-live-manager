# Pascom Live Manager

Sistema em Python para automatizar a preparação das transmissões da PASCOM utilizando OBS Studio e Animated Lower Thirds.

## Objetivo

Automatizar tarefas repetitivas da preparação das transmissões ao vivo, reduzindo erros e economizando tempo.

## Status

Em desenvolvimento (MVP)

## Funcionalidades

- Buscar automaticamente a Liturgia do Dia
- Gerar automaticamente título, descrição e resumo da transmissão
- Gerar JSON para importação manual no Animated Lower Thirds
- Copiar os logos configurados pela paróquia para a pasta de saída
- Salvar configurações locais da paróquia entre execuções
- Fornecer uma interface gráfica para preparar a transmissão

## Fluxo atual

1. Execute o Pascom Live Manager.
2. Configure logos, preces e chave PIX da paróquia.
3. Clique em **Preparar transmissão**.
4. O programa gera título, descrição, resumo, JSON e copia os logos para a pasta de saída.
5. No OBS, abra o painel do Animated Lower Thirds e importe manualmente o JSON gerado.

## Tecnologias

- Python
- OBS Studio
- Animated Lower Thirds
- Git
- GitHub

## Instalação

```bash
git clone ...
cd pascom-live-manager

python -m venv .venv
pip install -r requirements.txt
python main.py
```

## Testes

```bash
python -m unittest discover -s tests
```

## Roadmap

Consulte a pasta `/docs`.

## Licença

MIT
