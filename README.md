# Pascom Live Manager

Sistema em Python para automatizar a preparação das transmissões da PASCOM utilizando OBS Studio e Animated Lower Thirds.

## Objetivo

Automatizar tarefas repetitivas da preparação das transmissões ao vivo, reduzindo erros e economizando tempo.

## Funcionalidades

- Busca automática da Liturgia do Dia (Canção Nova)
- Geração automática de título, descrição e resumo da transmissão
- Geração de JSON para importação no Animated Lower Thirds
- Cópia dos logos configurados pela paróquia para a pasta de saída
- Salvamento das configurações locais da paróquia
- Interface gráfica para preparar a transmissão
- Instalador automático para Windows
- Testes automatizados

## Estrutura de Pastas
```bash
.
├── services/             # Serviços de orquestração
│   └── preparacao.py
├── tests/                # Testes automatizados
├── assets/               # Logos e ícones padrão
├── output/               # Arquivos gerados para a transmissão (auto-gerado)
├── docs/                 # Documentação detalhada
├── Installer/            # Scripts do instalador (Inno Setup)
├── README.md
├── requirements.txt
├── config.py
├── configuracao_paroquia.example.json
└── ...
```

## Instalação

### Usando o Instalador (Windows)

1. Baixe o instalador (`.zip`) na aba [Releases](https://github.com/niromurilo/pascom-live-manager/releases).
2. Extraia o `.zip` e execute o instalador, seguindo as instruções.

### Instalação Manual (Desenvolvedores)

1. Clone o repositório:
```bash
   git clone https://github.com/niromurilo/pascom-live-manager.git pascom-live-manager
   cd pascom-live-manager
```
2. Crie um ambiente virtual e instale as dependências:
```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
```

## Uso

1. Execute o Pascom Live Manager:
```bash
   python main.py
```
2. Configure logos, preces e chave PIX da paróquia pela interface gráfica — as configurações ficam salvas automaticamente para as próximas execuções.
3. Clique em **Preparar transmissão**.
4. O programa irá gerar, na pasta de saída escolhida:
   - Título (`titulo.txt`)
   - Descrição (`descricao.txt`)
   - Resumo (`resumo.txt`)
   - JSON para o Animated Lower Thirds (`animated_lower_thirds_liturgia.json`)
   - Cópia dos logos configurados
5. No OBS, abra o painel do Animated Lower Thirds e importe manualmente o JSON gerado.

## Tecnologias

- Python 3.12+
- obsws-python
- BeautifulSoup
- Requests
- Dataclasses
- OBS Studio
- Animated Lower Thirds

## Testes

Execute todos os testes com:
```bash
pytest tests/
```

## Roadmap

- [ ] Revisar interface gráfica
- [ ] Revisar e refatorar módulos principais
- [ ] Remover prints e código morto
- [ ] Gerar executável e instalador
- [ ] Melhorar documentação e exemplos

Veja o arquivo `TODO.md` e a pasta `docs/` para detalhes.

## Contribuição

Pull requests são bem-vindos! Siga o fluxo:

- Crie uma branch a partir da `main`
- Faça commits claros e objetivos (seguindo [Conventional Commits](https://www.conventionalcommits.org/))
- Abra um Pull Request

## Licença

MIT