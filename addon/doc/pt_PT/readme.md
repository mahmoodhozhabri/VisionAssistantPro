# Documentação do Vision Assistant Pro

**Vision Assistant Pro** é um assistente de IA avançado e multimodal para o NVDA. Utiliza os modelos Gemini da Google para fornecer leitura inteligente do ecrã, tradução, ditado por voz e capacidades de análise de documentos.

_Este complemento foi disponibilizado à comunidade em homenagem ao Dia Internacional das Pessoas com Deficiência._

## 1. Instalação e Configuração

Aceda a **Menu do NVDA > Preferências > Definições > Vision Assistant Pro**.

- **Chave de API:** Obrigatória. Pode introduzir várias chaves (separadas por vírgulas ou por novas linhas). O assistente alternará automaticamente entre elas se for atingido um limite de quota.
- **Modelo de IA:** Escolha entre os modelos **Flash** (Mais rápido/Gratuito), **Lite** ou **Pro** (Alta Inteligência).
- **URL de Proxy:** Opcional. Utilize esta opção se a Google estiver bloqueada na sua região. Deve ser um endereço web que funcione como ponte para a API do Gemini.
- **Motor de OCR:** Escolha entre **Chrome (Rápido)** para resultados imediatos ou **Gemini (Formatado)** para melhor preservação do layout e reconhecimento de tabelas.
- **Voz TTS:** Selecione o estilo de voz preferido para gerar ficheiros de áudio a partir das páginas dos documentos.
- **Troca Inteligente:** Alterna automaticamente os idiomas se o texto de origem corresponder ao idioma de destino.
- **Saída Direta:** Ignora a janela de chat e anuncia a resposta da IA diretamente por voz.
- **Integração com a Área de Transferência:** Copia automaticamente a resposta da IA para a área de transferência.

## 2. Camada de Comandos e Atalhos

Para evitar conflitos de teclado, este complemento utiliza uma **Camada de Comandos**.

1. Prima **NVDA + Shift + V** (Tecla Mestra) para ativar a camada (irá ouvir um sinal sonoro).
2. Solte as teclas e, de seguida, prima uma das seguintes teclas individuais:

| Tecla         | Função                            | Descrição                                                                                |
| ------------- | --------------------------------- | ---------------------------------------------------------------------------------------- |
| **T**         | Tradutor Inteligente              | Traduz o texto sob o cursor de navegação ou a seleção.                                   |
| **Shift + T** | Tradutor da Área de Transferência | Traduz o conteúdo atualmente na área de transferência.                                   |
| **R**         | Refinador de Texto                | Resumir, corrigir gramática, explicar ou executar **Prompts Personalizados**.            |
| **V**         | Visão de Objetos                  | Descreve o objeto atual do navegador.                                                    |
| **O**         | Visão de Ecrã Completo            | Analisa todo o layout e conteúdo do ecrã.                                                |
| **Shift + V** | Análise de Vídeo Online           | Analisa vídeos do **YouTube**, **Instagram** ou **Twitter (X)** através de URL.          |
| **D**         | Leitor de Documentos              | Leitor avançado para PDF e imagens com seleção de intervalo de páginas.                  |
| **F**         | OCR de Ficheiros                  | Reconhecimento direto de texto a partir de imagens, PDFs ou ficheiros TIFF selecionados. |
| **A**         | Transcrição de Áudio              | Transcreve ficheiros MP3, WAV ou OGG para texto.                                         |
| **C**         | Resolvedor de CAPTCHA             | Captura e resolve CAPTCHAs no ecrã ou no objeto do navegador.                            |
| **S**         | Ditado Inteligente                | Converte fala em texto. Prima para iniciar a gravação e novamente para parar/escrever.   |
| **L**         | Relatório de Estado               | Anuncia o progresso atual (ex.: "A analisar...", "Inativo").                             |
| **U**         | Verificação de Atualizações       | Verifica manualmente no GitHub a versão mais recente do complemento.                     |
| **H**         | Ajuda de Comandos                 | Apresenta uma lista de todos os atalhos disponíveis dentro da camada de comandos.        |

### 2.1 Atalhos do Leitor de Documentos (Dentro do Visualizador)

Depois de um documento ser aberto através do comando **D**:

- **Ctrl + PageDown:** Avançar para a página seguinte (anuncia o número da página).
- **Ctrl + PageUp:** Recuar para a página anterior (anuncia o número da página).
- **Alt + A:** Abrir um diálogo de chat para colocar perguntas sobre o documento.
- **Alt + R:** Forçar uma nova análise da página atual ou de todas as páginas utilizando o motor Gemini.
- **Alt + G:** Gerar e guardar um ficheiro de áudio de alta qualidade (WAV) a partir do conteúdo.
- **Alt + S / Ctrl + S:** Guardar o texto extraído como ficheiro TXT ou HTML.

## 3. Prompts Personalizados e Variáveis

Pode criar comandos de IA personalizados nas Definições utilizando o formato: `Nome:Texto do Prompt` (separe vários comandos com `|` ou novas linhas).

### Variáveis Disponíveis

| Variável        | Descrição                                    | Tipo de Entrada   |
| --------------- | -------------------------------------------- | ----------------- |
| `[selection]`   | Texto atualmente selecionado                 | Texto             |
| `[clipboard]`   | Conteúdo da área de transferência            | Texto             |
| `[screen_obj]`  | Captura de ecrã do objeto do navegador       | Imagem            |
| `[screen_full]` | Captura de ecrã do ecrã completo             | Imagem            |
| `[file_ocr]`    | Selecionar imagem/PDF para extração de texto | Imagem, PDF, TIFF |
| `[file_read]`   | Selecionar documento para leitura            | TXT, Código, PDF  |
| `[file_audio]`  | Selecionar ficheiro de áudio para análise    | MP3, WAV, OGG     |

### Exemplos de Prompts Personalizados

- **OCR Rápido:** `Meu OCR:[file_ocr]`
- **Traduzir Imagem:** `Traduzir Img:Extrair o texto desta imagem e traduzir para inglês. [file_ocr]`
- **Analisar Áudio:** `Resumir Áudio:Ouvir esta gravação e resumir os pontos principais. [file_audio]`
- **Depurador de Código:** `Depurar:Encontrar erros neste código e explicá-los: [selection]`

---

**Nota:** É necessária uma ligação ativa à internet para todas as funcionalidades de IA. Documentos com várias páginas e ficheiros TIFF são processados automaticamente.

## Alterações na versão 4.0.1

- **Leitor Avançado de Documentos:** Novo visualizador poderoso para PDFs e imagens, com seleção de intervalo de páginas, processamento em segundo plano e navegação fluida com `Ctrl+PageUp/Down`.
- **Novo Submenu de Ferramentas:** Adicionado um submenu dedicado "Vision Assistant" no menu Ferramentas do NVDA para acesso mais rápido às funcionalidades principais, definições e documentação.
- **Personalização Flexível:** Possibilidade de escolher diretamente o motor de OCR e a voz TTS preferidos no painel de definições.
- **Suporte a Múltiplas Chaves de API:** Adicionado suporte a várias chaves de API do Gemini.
- **Motor de OCR Alternativo:** Introduzido um novo motor de OCR para garantir reconhecimento fiável mesmo ao atingir limites de quota da API Gemini.
- **Rotação Inteligente de Chaves de API:** Alterna automaticamente e memoriza a chave de API mais rápida em funcionamento.
- **Documento para MP3/WAV:** Capacidade integrada de gerar e guardar ficheiros de áudio de alta qualidade nos formatos MP3 (128 kbps) e WAV.
- **Suporte a Stories do Instagram:** Capacidade de descrever e analisar Stories do Instagram através das respetivas URLs.
- **Suporte ao TikTok:** Introduzido suporte a vídeos do TikTok, com descrição visual completa e transcrição de áudio.
- **Diálogo de Atualização Redesenhado:** Nova interface acessível com caixa de texto deslocável para leitura clara das alterações.
- **Estado Unificado e UX:** Normalização dos diálogos de ficheiros e melhoria do comando `L` para relatar progresso em tempo real.

## Alterações na versão 3.6.0

- **Sistema de Ajuda:** Adicionado um comando de ajuda (`H`) dentro da Camada de Comandos.
- **Análise de Vídeo Online:** Suporte alargado a vídeos do **Twitter (X)**, com melhorias na deteção de URLs e estabilidade.
- **Contribuição para o Projeto:** Adicionado um diálogo opcional de donativos para apoiar o desenvolvimento futuro do projeto.

## Alterações na versão 3.5.0

\* **Camada de Comandos:** Introdução do sistema de Camada de Comandos (predefinição: `NVDA+Shift+V`). \* **Análise de Vídeo Online:** Novo recurso para analisar vídeos do YouTube e Instagram diretamente através de URL.

## Alterações na versão 3.1.0

- **Modo de Saída Direta:** Opção para ignorar o diálogo de chat e ouvir as respostas da IA diretamente por voz.
- **Integração com a Área de Transferência:** Nova definição para copiar automaticamente as respostas da IA para a área de transferência.

## Alterações na versão 3.0

- **Novos Idiomas:** Adicionadas traduções para **Persa** e **Vietnamita**.
- **Modelos de IA Expandidos:** Reorganização da lista de modelos e suporte para **Gemini 3.0 Pro** e **Gemini 2.0 Flash Lite**.
- **Estabilidade do Ditado:** Melhorias significativas no Ditado Inteligente.
- **Gestão de Ficheiros:** Correção de falhas ao carregar ficheiros com nomes não ingleses.
- **Otimização de Prompts:** Melhoria da lógica de tradução e estruturação dos resultados de Visão.

## Alterações na versão 2.9

- **Adicionadas traduções em Francês e Turco.**
- **Visualização Formatada:** Botão "Ver Formatado" nos diálogos de chat.
- **Definição de Markdown:** Nova opção "Limpar Markdown no Chat".
- **Gestão de Diálogos:** Correções relacionadas com abertura múltipla e foco.
- **Melhorias de UX:** Normalização dos títulos dos diálogos e remoção de anúncios de voz redundantes.

## Alterações na versão 2.8

- Tradução italiana adicionada.
- **Relatório de Estado:** Novo comando para anunciar o estado atual do complemento.
- **Exportação HTML:** O botão "Guardar Conteúdo" passa a guardar a saída como HTML formatado.
- **Interface de Definições:** Layout do painel de definições melhorado com agrupamentos acessíveis.
- **Novos Modelos:** Suporte para gemini-flash-latest e gemini-flash-lite-latest.
- **Idiomas:** Adicionado Nepalês.
- **Lógica do Menu Refinar:** Correção de um erro crítico quando o idioma da interface do NVDA não era inglês.
- **Ditado:** Melhoria na deteção de silêncio.
- **Definições de Atualização:** A verificação de atualizações no arranque passa a estar desativada por predefinição.
- Limpeza de código.

## Alterações na versão 2.7

- Migração da estrutura do projeto para o modelo oficial de complementos da NV Access.
- Implementação de lógica de nova tentativa automática para erros HTTP 429 (limite de taxa).
- Otimização dos prompts de tradução para maior precisão e melhor lógica de "Troca Inteligente".
- Tradução russa atualizada.

## Alterações na versão 2.6

- Adicionado suporte à tradução russa (agradecimentos ao nvda-ru).
- Mensagens de erro atualizadas com feedback mais descritivo sobre conectividade.
- Idioma de destino predefinido alterado para inglês.

## Alterações na versão 2.5

- Adicionado comando nativo de OCR de ficheiros (NVDA+Control+Shift+F).
- Botão "Guardar Chat" nos diálogos de resultados.
- Implementado suporte completo à localização (i18n).
- Migração do feedback de áudio para o módulo nativo de tons do NVDA.
- Utilização da API de Ficheiros do Gemini.
- Correção de falha ao traduzir texto com chavetas.

## Alterações na versão 2.1.1

- Correção de um problema em que a variável [file_ocr] não funcionava corretamente em Prompts Personalizados.

## Alterações na versão 2.1

- Padronização de todos os atalhos para NVDA+Control+Shift, eliminando conflitos com o layout Laptop do NVDA e atalhos do sistema.

## Alterações na versão 2.0

- Implementação de sistema de atualização automática integrado.
- Cache inteligente de tradução para recuperação imediata.
- Memória de conversas para refinar resultados de forma contextual.
- Comando dedicado de tradução da área de transferência (NVDA+Control+Shift+Y).
- Otimização dos prompts de IA para impor rigorosamente o idioma de saída.
- Correção de falhas causadas por caracteres especiais no texto de entrada.

## Alterações na versão 1.5

- Suporte para mais de 20 novos idiomas.
- Implementação de diálogo interativo de refinamento.
- Adicionado recurso nativo de Ditado Inteligente.
- Categoria "Vision Assistant" adicionada aos gestos de entrada do NVDA.
- Correção de falhas COMError em aplicações específicas como Firefox e Word.
- Adicionado mecanismo automático de nova tentativa para erros de servidor.

## Alterações na versão 1.0

- Lançamento inicial.
