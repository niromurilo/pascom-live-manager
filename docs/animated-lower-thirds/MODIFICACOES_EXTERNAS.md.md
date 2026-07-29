# Modificações em Dependências Externas

> Este documento registra alterações realizadas em projetos de terceiros utilizadas pelo Pascom Live Manager.

---

# Animated Lower Thirds

## Arquivo

control-panel.html

## Objetivo

Investigar a possibilidade de automatizar o processo de Import do Animated Lower Thirds, eliminando a necessidade de intervenção manual do operador.

## Alteração realizada

Foi criada uma Prova de Conceito (PoC) adicionando um script JavaScript responsável por:

- ler periodicamente um arquivo JSON local;
- utilizar o endereço `http://absolute/`;
- detectar alterações no conteúdo;
- reutilizar a função `writeLocalStorage()` existente;
- preservar o funcionamento original do botão **Import**.

## Resultado

❌ A abordagem foi descartada.

Os testes mostraram limitações da arquitetura do Animated Lower Thirds executado como **Custom Browser Dock** no OBS Studio, impossibilitando uma automação confiável do processo de Import.

## Decisão

O Pascom Live Manager passou a gerar automaticamente o arquivo JSON de importação.

A etapa de clicar em **Import** permanece manual por decisão de projeto, registrada também em `docs/Decisoes.md`.

---

## Futuras modificações

Novas alterações em dependências externas deverão ser registradas neste documento.