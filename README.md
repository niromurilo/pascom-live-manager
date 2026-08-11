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

```
.
├── src/                  # Código-fonte principal
│   ├── preparacao.py
│   ├── ...
├── services/             # Serviços de orquestração
│   └── preparacao.py
├── tests/                # Testes automatizados
├── assets/               # Logos e ícones
├── output/               # Arquivos gerados para transmissão
├── docs/                 # Documentação detalhada
├── build/                # Build temporário (auto-gerado)
├── dist/                 # Distribuição (auto-gerado)
├── Installer/            # Scripts e arquivos do instalador
├── README.md
├── requirements.txt
├── config.py
├── configurar_paroquia.example.json
└── ...
```

## Instalação

### Usando o Instalador (Windows)

1. Baixe o instalador na pasta `Installer/` ou em [Releases](./docs/Releases.md).
2. Execute o instalador e siga as instruções.

### Instalação Manual (Desenvolvedores)

1. Clone o repositório:
   ```bash
   git clone https://github.com/niromurilo/pascom-live-manager.git
   cd pascom-live-manager
   ```
2. Crie um ambiente virtual e instale as dependências:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. (Opcional) Configure o arquivo `configurar_paroquia.json` com os dados da sua paróquia.

## Uso

1. Execute o Pascom Live Manager:
   ```bash
   python main.py
   ```
2. Configure logos, preces e chave PIX da paróquia pela interface gráfica.
3. Clique em **Preparar transmissão**.
4. O programa irá gerar:
   - Título (`titulo.txt`)
   - Descrição (`descricao.txt`)
   - Resumo (`resumo.txt`)
   - JSON para o Animated Lower Thirds (`animated_lower_thirds_liturgia.json`)
   - Cópia dos logos para a pasta de saída
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
- Crie uma branch a partir da main
- Faça commits claros e objetivos
- Abra um Pull Request

## Licença

MIT

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
