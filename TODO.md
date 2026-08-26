VERSÃO 1.0.0

☑ Interface gráfica
☑ Revisar interface_grafica.py
☐ Revisar services/preparacao.py
☐ Revisar animated_lower_thirds.py
☐ Revisar buscar_liturgia.py
☐ Revisar gerador_descricao.py
☐ Remover prints
☐ Remover código morto
☐ Gerar executável
☐ Criar instalador
☐ README
☐ CHANGELOG
☐ ROADMAP
☐ Release v1.0

# TODO — Pascom Live Manager

## ⚠️ IMPORTANTE — Pré-requisito

- [ ] **Documentar que o projeto depende do Animated Lower Thirds configurado no OBS Studio.**
- [ ] Antes de utilizar o Pascom Live Manager, o operador deve ter:
  - Animated Lower Thirds instalado.
  - `control-panel.html` configurado no OBS.
  - `browser-source.html` adicionado como Fonte de Navegador na cena.
  - Browser Source configurado com a resolução correta da transmissão.
  - O Browser Source apontando para a instalação correta do Animated Lower Thirds.
- [ ] Documentar a configuração específica utilizada no projeto.
- [ ] Explicar que, dependendo da versão/configuração do OBS, pode ser necessário utilizar o caminho `file:///...` no Browser Source em vez de marcar "Arquivo local". Isso é uma questão conhecida do Animated Lower Thirds em versões mais novas do OBS. citeturn0search2turn0search3
- [ ] Explicar que os arquivos gerados pelo projeto precisam estar em um local que o Animated Lower Thirds consiga acessar.
- [ ] Idealmente, no futuro, eliminar a necessidade de copiar manualmente os arquivos para a pasta original do Animated Lower Thirds.

---

# 🔴 Prioridade alta

## 1. Corrigir integração com Animated Lower Thirds

- [ ] Descobrir exatamente por que o JSON gerado não é carregado automaticamente pelo Animated.
- [ ] Fazer o programa descobrir automaticamente a pasta de instalação do Animated Lower Thirds.
- [ ] Permitir configurar manualmente essa pasta caso ela não seja encontrada.
- [ ] Copiar/sincronizar automaticamente o JSON gerado para a pasta correta do Animated.
- [ ] Evitar que o usuário precise copiar arquivos manualmente.
- [ ] Validar se o `browser-source.html` está sendo carregado pelo OBS antes de considerar a preparação concluída.
- [ ] Mostrar uma mensagem clara caso o Animated Lower Thirds não esteja configurado.

## 2. Corrigir os Lower Thirds

- [ ] Corrigir o mapeamento dos campos `alt-X-name`, `alt-X-info` e slots.
- [ ] Garantir que o painel 1 represente corretamente o título/celebrante.
- [ ] Garantir que o painel 2 contenha:
  - Primeira Leitura
  - Salmo Responsorial
  - Segunda Leitura, quando existir
  - Evangelho
  - Preces, quando cadastradas
- [ ] Garantir que o painel 3 contenha o PIX.
- [ ] Testar cada slot individualmente dentro do Animated.
- [ ] Testar a troca entre slots durante uma transmissão.
- [ ] Garantir que slots utilizados no dia anterior não permaneçam ativos.
- [ ] Revisar a função `_limpar_slots_dinamicos()`.
- [ ] Remover código antigo/redundante relacionado a `_resetar_slots_do_painel()` se ele não for mais utilizado.

## 3. Corrigir o relatório

- [ ] Corrigir o `relatorio.txt`.
- [ ] Fazer o relatório representar exatamente os dados que foram colocados no JSON.
- [ ] Mostrar claramente:
  - Título da transmissão
  - Descrição
  - Painel 1
  - Painel 2 + todos os slots
  - Painel 3
  - Logos utilizados
  - Local do JSON
- [ ] Conferir se o relatório não está mostrando dados antigos do `animated.json`.
- [ ] Fazer o relatório ser gerado a partir dos mesmos dados usados para gerar o JSON.

---

# 🟠 Integração de arquivos

- [x] Copiar logos configurados para a pasta de saída.
- [x] Gerar caminhos dos logos em formato URI.
- [x] Logos funcionando no Animated Lower Thirds.
- [ ] Copiar automaticamente o JSON para a pasta correta do Animated Lower Thirds.
- [ ] Definir claramente qual é a pasta de saída oficial do projeto.
- [ ] Evitar caminhos relativos quebrados.
- [ ] Trabalhar corretamente com caminhos contendo espaços, `OneDrive`, acentos etc.
- [ ] Testar o projeto em outra instalação do Windows.
- [ ] Evitar depender de caminhos específicos do computador do desenvolvedor.

---

# 🟡 Liturgia

- [x] Buscar a liturgia.
- [x] Extrair primeira leitura.
- [x] Extrair salmo responsorial.
- [x] Extrair segunda leitura quando existir.
- [x] Extrair evangelho.
- [x] Adicionar preces.
- [ ] Testar domingos com segunda leitura.
- [ ] Testar dias de semana sem segunda leitura.
- [ ] Testar diferentes formatos de citações bíblicas.
- [ ] Melhorar tratamento de erros quando o site da liturgia mudar.
- [ ] Criar testes para diferentes dias litúrgicos.

---

# 🟡 Configuração da paróquia

- [x] Configuração do nome da paróquia.
- [x] Configuração do PIX.
- [x] Configuração das preces.
- [x] Configuração dos logos.
- [ ] Melhorar tela/arquivo de configuração.
- [ ] Validar todos os caminhos de logos antes da transmissão.
- [ ] Mostrar ao usuário quais configurações estão faltando.
- [ ] Permitir alterar as configurações sem editar código.

---

# 🟢 Título e descrição

- [x] Gerar título automaticamente.
- [x] Gerar descrição automaticamente.
- [x] Salvar `titulo.txt`.
- [x] Salvar `descricao.txt`.
- [ ] Revisar textos gerados.
- [ ] Criar modelos configuráveis para título.
- [ ] Criar modelos configuráveis para descrição.
- [ ] Permitir personalização por paróquia.

---

# 🔵 Arquitetura do projeto

- [x] Separação entre CLI/GUI e lógica de negócio.
- [x] `preparacao.py` como ponto principal da preparação.
- [x] Uso de `Resultado` para retorno de operações.
- [x] Separação da lógica de liturgia.
- [x] Separação da geração dos Lower Thirds.
- [ ] Revisar imports e dependências.
- [ ] Remover funções não utilizadas.
- [ ] Padronizar nomes dos módulos.
- [ ] Adicionar type hints onde faltarem.
- [ ] Melhorar mensagens de erro.
- [ ] Criar testes automatizados.
- [ ] Criar `requirements.txt`.
- [ ] Criar `.env.example`, se necessário.
- [ ] Criar documentação de instalação.

---

# 🔵 CLI / GUI

- [ ] Finalizar CLI.
- [ ] Criar/terminar GUI.
- [ ] Permitir escolher paróquia.
- [ ] Permitir informar celebrante.
- [ ] Permitir visualizar os dados antes de gerar.
- [ ] Mostrar progresso da preparação.
- [ ] Mostrar erros de forma amigável.
- [ ] Mostrar onde os arquivos foram gerados.
- [ ] Permitir abrir a pasta de saída.
- [ ] Permitir abrir o relatório.
- [ ] Adicionar botão para preparar transmissão.
- [ ] Adicionar botão para atualizar/regerar os Lower Thirds.

---

# 🧪 Testes

- [ ] Testar geração do JSON.
- [ ] Testar validação do JSON.
- [ ] Testar relatório.
- [ ] Testar logos.
- [ ] Testar PIX.
- [ ] Testar celebrante.
- [ ] Testar preces.
- [ ] Testar liturgia com segunda leitura.
- [ ] Testar liturgia sem segunda leitura.
- [ ] Testar slots antigos.
- [ ] Testar caminhos com espaços.
- [ ] Testar caminhos no OneDrive.
- [ ] Testar instalação em outro computador.
- [ ] Testar integração real com OBS.
- [ ] Testar exibição dos Lower Thirds durante uma transmissão.

---

# 📦 Distribuição

- [ ] Criar instalador ou pacote `.zip`.
- [ ] Incluir documentação.
- [ ] Criar estrutura de pastas padrão.
- [ ] Detectar instalação do OBS.
- [ ] Detectar Animated Lower Thirds.
- [ ] Configurar automaticamente os arquivos necessários.
- [ ] Criar configuração inicial automática.
- [ ] Criar backup dos arquivos antes de substituir configurações.
- [ ] Criar versão do projeto.
- [ ] Criar changelog.

---

# 📚 Documentação

- [ ] Criar `README.md` profissional.
- [ ] Explicar o objetivo do Pascom Live Manager.
- [ ] Explicar os requisitos.
- [ ] Explicar instalação do Python.
- [ ] Explicar instalação/configuração do Animated Lower Thirds.
- [ ] Explicar configuração do OBS.
- [ ] Explicar configuração da paróquia.
- [ ] Explicar como gerar a transmissão.
- [ ] Explicar onde ficam os arquivos gerados.
- [ ] Explicar solução de problemas.
- [ ] Adicionar screenshots do OBS.
- [ ] Adicionar exemplo de configuração.
- [ ] Criar seção **"Antes de usar"** destacando que o Animated Lower Thirds precisa estar configurado no OBS.

---

# 🚀 Futuro

- [ ] Atualização automática dos Lower Thirds no OBS.
- [ ] Integração mais direta com o Animated Lower Thirds.
- [ ] Configuração automática do Browser Source.
- [ ] Controle dos Lower Thirds diretamente pelo Pascom Live Manager.
- [ ] Gerenciamento de várias paróquias.
- [ ] Histórico das transmissões.
- [ ] Banco de dados para configurações.
- [ ] Agendamento de transmissões.
- [ ] Integração com YouTube.
- [ ] Automação de publicação.
- [ ] Logs da aplicação.
- [ ] Sistema de atualização do programa.

---

## Estado atual

### ✅ Funcionando
- Busca da liturgia.
- Geração de título.
- Geração de descrição.
- Geração dos Lower Thirds.
- Geração dos arquivos JSON.
- Configuração dos logos.
- Cópia dos logos.
- Logos aparecendo corretamente no Animated Lower Thirds.

### ⚠️ Precisa ser corrigido
- Integração automática do JSON com o Animated Lower Thirds.
- Exibição automática dos Lower Thirds.
- Relatório gerado.
- Dependência de copiar manualmente os arquivos para a pasta original do Animated.

### 📌 Regra importante para documentação

> **O Pascom Live Manager depende do Animated Lower Thirds configurado no OBS Studio. O Animated Lower Thirds deve estar instalado e configurado antes da utilização do projeto. O Browser Source utilizado pelo OBS deve apontar para a instalação correta do Animated Lower Thirds.**

O Animated Lower Thirds oficialmente funciona através de um painel de controle e de uma Browser Source dentro do OBS, então essa dependência deve ficar explícita na documentação do projeto. citeturn0search1turn0search7