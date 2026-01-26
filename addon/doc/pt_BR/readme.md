# Documentação do Vision Assistant Pro

**Vision Assistant Pro** é um assistente de IA avançado e multimodal para o NVDA. Ele utiliza os modelos Gemini do Google para fornecer leitura inteligente de tela, tradução, ditado por voz e recursos de análise de documentos.

_Este complemento foi lançado para a comunidade em homenagem ao Dia Internacional das Pessoas com Deficiência._

## 1. Instalação e Configuração

Acesse **Menu do NVDA > Preferências > Configurações > Vision Assistant Pro**.

- **Chave de API:** Obrigatória. Você pode inserir várias chaves (separadas por vírgulas ou por novas linhas). O assistente alternará automaticamente entre elas se um limite de cota for atingido.
- **Modelo de IA:** Escolha entre os modelos **Flash** (Mais rápido/Gratuito), **Lite** ou **Pro** (Alta Inteligência).
- **URL de Proxy:** Opcional. Use isto se o Google estiver bloqueado na sua região. Deve ser um endereço web que atue como ponte para a API do Gemini.
- **Motor de OCR:** Escolha entre **Chrome (Rápido)** para resultados rápidos ou **Gemini (Formatado)** para melhor preservação de layout e reconhecimento de tabelas.
- **Voz TTS:** Selecione o estilo de voz preferido para gerar arquivos de áudio a partir das páginas de documentos.
- **Troca Inteligente:** Alterna automaticamente os idiomas se o texto de origem corresponder ao idioma de destino.
- **Saída Direta:** Ignora a janela de chat e anuncia a resposta da IA diretamente por fala.
- **Integração com a Área de Transferência:** Copia automaticamente a resposta da IA para a área de transferência.

## 2. Camada de Comandos e Atalhos

Para evitar conflitos de teclado, este complemento utiliza uma **Camada de Comandos**.

1. Pressione **NVDA + Shift + V** (Tecla Mestra) para ativar a camada (você ouvirá um bip).
2. Solte as teclas e, em seguida, pressione uma das seguintes teclas únicas:

| Tecla         | Função                            | Descrição                                                                                 |
| ------------- | --------------------------------- | ----------------------------------------------------------------------------------------- |
| **T**         | Tradutor Inteligente              | Traduz o texto sob o cursor de navegação ou a seleção.                                    |
| **Shift + T** | Tradutor da Área de Transferência | Traduz o conteúdo atualmente na área de transferência.                                    |
| **R**         | Refinador de Texto                | Resumir, corrigir gramática, explicar ou executar **Prompts Personalizados**.             |
| **V**         | Visão de Objetos                  | Descreve o objeto atual do navegador.                                                     |
| **O**         | Visão de Tela Inteira             | Analisa todo o layout e conteúdo da tela.                                                 |
| **Shift + V** | Análise de Vídeo Online           | Analisa vídeos do **YouTube**, **Instagram** ou **Twitter (X)** via URL.                  |
| **D**         | Leitor de Documentos              | Leitor avançado para PDF e imagens com seleção de intervalo de páginas.                   |
| **F**         | OCR de Arquivo                    | Reconhecimento direto de texto a partir de imagens, PDFs ou arquivos TIFF selecionados.   |
| **A**         | Transcrição de Áudio              | Transcreve arquivos MP3, WAV ou OGG para texto.                                           |
| **C**         | Solucionador de CAPTCHA           | Captura e resolve CAPTCHAs na tela ou no objeto do navegador.                             |
| **S**         | Ditado Inteligente                | Converte fala em texto. Pressione para iniciar a gravação e novamente para parar/digitar. |
| **L**         | Relatório de Status               | Anuncia o progresso atual (ex.: "Escaneando...", "Ocioso").                               |
| **U**         | Verificação de Atualizações       | Verifica manualmente no GitHub a versão mais recente do complemento.                      |
| **H**         | Ajuda de Comandos                 | Exibe uma lista de todos os atalhos disponíveis dentro da camada de comandos.             |

### 2.1 Atalhos do Leitor de Documentos (Dentro do Visualizador)

Depois que um documento é aberto pelo comando **D**:

- **Ctrl + PageDown:** Ir para a próxima página (anuncia o número da página).
- **Ctrl + PageUp:** Ir para a página anterior (anuncia o número da página).
- **Alt + A:** Abrir um diálogo de chat para fazer perguntas sobre o documento.
- **Alt + R:** Forçar uma nova varredura da página atual ou de todas as páginas usando o motor Gemini.
- **Alt + G:** Gerar e salvar um arquivo de áudio de alta qualidade (WAV) a partir do conteúdo.
- **Alt + S / Ctrl + S:** Salvar o texto extraído como um arquivo TXT ou HTML.

## 3. Prompts Personalizados e Variáveis

Você pode criar comandos personalizados poderosos de IA nas Configurações usando o formato: `Nome:Texto do Prompt` (separe vários comandos com `|` ou novas linhas).

### Variáveis Disponíveis

| Variável        | Descrição                                    | Tipo de Entrada   |
| --------------- | -------------------------------------------- | ----------------- |
| `[selection]`   | Texto atualmente selecionado                 | Texto             |
| `[clipboard]`   | Conteúdo da área de transferência            | Texto             |
| `[screen_obj]`  | Captura de tela do objeto do navegador       | Imagem            |
| `[screen_full]` | Captura de tela da tela inteira              | Imagem            |
| `[file_ocr]`    | Selecionar imagem/PDF para extração de texto | Imagem, PDF, TIFF |
| `[file_read]`   | Selecionar documento para leitura            | TXT, Código, PDF  |
| `[file_audio]`  | Selecionar arquivo de áudio para análise     | MP3, WAV, OGG     |

### Exemplos de Prompts Personalizados

- **OCR Rápido:** `Meu OCR:[file_ocr]`
- **Traduzir Imagem:** `Traduzir Img:Extraia o texto desta imagem e traduza para o inglês. [file_ocr]`
- **Analisar Áudio:** `Resumir Áudio:Ouça esta gravação e resuma os pontos principais. [file_audio]`
- **Depurador de Código:** `Depurar:Encontre erros neste código e explique-os: [selection]`

---

**Nota:** É necessária uma conexão ativa com a internet para todos os recursos de IA. Documentos com várias páginas e arquivos TIFF são processados automaticamente.

## Alterações na versão 4.0.1

- **Leitor Avançado de Documentos:** Novo visualizador poderoso para PDFs e imagens, com seleção de intervalo de páginas, processamento em segundo plano e navegação fluida com `Ctrl+PageUp/Down`.
- **Novo Submenu de Ferramentas:** Adicionado um submenu dedicado "Vision Assistant" no menu Ferramentas do NVDA para acesso mais rápido aos recursos principais, configurações e documentação.
- **Personalização Flexível:** Agora é possível escolher o motor de OCR e a voz TTS preferidos diretamente no painel de configurações.
- **Suporte a Múltiplas Chaves de API:** Adicionado suporte a várias chaves de API do Gemini. Você pode inserir uma chave por linha ou separá-las por vírgulas nas configurações.
- **Motor de OCR Alternativo:** Introduzido um novo motor de OCR para garantir reconhecimento confiável mesmo ao atingir limites de cota da API Gemini.
- **Rotação Inteligente de Chaves de API:** Alterna automaticamente e memoriza a chave de API mais rápida em funcionamento para contornar limites de cota.
- **Documento para MP3/WAV:** Capacidade integrada de gerar e salvar arquivos de áudio de alta qualidade nos formatos MP3 (128 kbps) e WAV diretamente no leitor.
- **Suporte a Stories do Instagram:** Adicionada a capacidade de descrever e analisar Stories do Instagram usando suas URLs.
- **Suporte ao TikTok:** Introduzido suporte a vídeos do TikTok, permitindo descrição visual completa e transcrição de áudio dos clipes.
- **Diálogo de Atualização Redesenhado:** Nova interface acessível com caixa de texto rolável para leitura clara das alterações antes da instalação.
- **Status Unificado e UX:** Padronização dos diálogos de arquivo em todo o complemento e melhoria do comando `L` para relatar progresso em tempo real.

## Alterações na versão 3.6.0

- **Sistema de Ajuda:** Adicionado um comando de ajuda (`H`) dentro da Camada de Comandos para acesso rápido à lista de atalhos e funções.
- **Análise de Vídeo Online:** Suporte expandido para vídeos do **Twitter (X)**, com melhorias na detecção de URLs e estabilidade.
- **Contribuição para o Projeto:** Adicionado um diálogo opcional de doação para apoiar futuras atualizações e o crescimento contínuo do projeto.

## Alterações na versão 3.5.0

\* **Camada de Comandos:** Introdução do sistema de Camada de Comandos (padrão: `NVDA+Shift+V`) para agrupar atalhos sob uma única tecla mestra. \* **Análise de Vídeo Online:** Novo recurso para analisar vídeos do YouTube e Instagram diretamente por URL.

## Alterações na versão 3.1.0

- **Modo de Saída Direta:** Opção para ignorar o diálogo de chat e ouvir as respostas da IA diretamente por fala.
- **Integração com a Área de Transferência:** Nova configuração para copiar automaticamente as respostas da IA para a área de transferência.

## Alterações na versão 3.0

- **Novos Idiomas:** Adicionadas traduções para **Persa** e **Vietnamita**.
- **Modelos de IA Expandidos:** Reorganização da lista de modelos com prefixos claros (`[Free]`, `[Pro]`, `[Auto]`) e suporte ao **Gemini 3.0 Pro** e **Gemini 2.0 Flash Lite**.
- **Estabilidade do Ditado:** Melhorias significativas no Ditado Inteligente, com verificação de segurança para ignorar áudios menores que 1 segundo.
- **Manipulação de Arquivos:** Correção de falha ao enviar arquivos com nomes não ingleses.
- **Otimização de Prompts:** Melhoria da lógica de tradução e estruturação dos resultados de Visão.

## Alterações na versão 2.9

- **Adicionadas traduções em Francês e Turco.**
- **Visualização Formatada:** Botão "Ver Formatado" nos diálogos de chat para exibir a conversa com estilo adequado.
- **Configuração de Markdown:** Nova opção "Limpar Markdown no Chat" nas Configurações.
- **Gerenciamento de Diálogos:** Correção de problemas de abertura múltipla e foco.
- **Melhorias de UX:** Padronização dos títulos dos diálogos e remoção de anúncios de fala redundantes.

## Alterações na versão 2.8

- Tradução para Italiano adicionada.
- **Relatório de Status:** Novo comando para anunciar o status atual do complemento.
- **Exportação HTML:** O botão "Salvar Conteúdo" agora salva a saída como HTML formatado.
- **Interface de Configurações:** Layout do painel de configurações aprimorado com agrupamentos acessíveis.
- **Novos Modelos:** Suporte a gemini-flash-latest e gemini-flash-lite-latest.
- **Idiomas:** Adicionado Nepali.
- **Lógica do Menu Refinar:** Correção de um erro crítico quando o idioma da interface do NVDA não era inglês.
- **Ditado:** Melhoria na detecção de silêncio para evitar saída incorreta.
- **Configurações de Atualização:** A verificação de atualizações na inicialização agora vem desativada por padrão.
- Limpeza de código.

## Alterações na versão 2.7

- Migração da estrutura do projeto para o modelo oficial de complementos da NV Access.
- Implementação de lógica de repetição automática para erros HTTP 429 (limite de taxa).
- Otimização dos prompts de tradução para maior precisão e melhor lógica de "Troca Inteligente".
- Tradução russa atualizada.

## Alterações na versão 2.6

- Adicionado suporte à tradução russa (agradecimentos ao nvda-ru).
- Mensagens de erro atualizadas com feedback mais descritivo sobre conectividade.
- Idioma de destino padrão alterado para inglês.

## Alterações na versão 2.5

- Adicionado comando nativo de OCR de arquivos (NVDA+Control+Shift+F).
- Botão "Salvar Chat" nos diálogos de resultado.
- Implementado suporte completo à localização (i18n).
- Migração do feedback de áudio para o módulo nativo de tons do NVDA.
- Uso da API de Arquivos do Gemini para melhor manuseio de PDFs e áudios.
- Correção de falha ao traduzir texto contendo chaves.

## Alterações na versão 2.1.1

- Correção de um problema em que a variável [file_ocr] não funcionava corretamente em Prompts Personalizados.

## Alterações na versão 2.1

- Padronização de todos os atalhos para NVDA+Control+Shift, eliminando conflitos com o layout Laptop do NVDA e atalhos do sistema.

## Alterações na versão 2.0

- Sistema de atualização automática integrado.
- Cache inteligente de tradução para recuperação instantânea.
- Memória de conversas para refinar resultados contextualmente.
- Comando dedicado de tradução da área de transferência (NVDA+Control+Shift+Y).
- Otimização dos prompts de IA para impor rigorosamente o idioma de saída.
- Correção de falha causada por caracteres especiais no texto de entrada.

## Alterações na versão 1.5

- Suporte a mais de 20 novos idiomas.
- Implementação de diálogo interativo de refinamento para perguntas de acompanhamento.
- Adicionado recurso nativo de Ditado Inteligente.
- Categoria "Vision Assistant" adicionada aos gestos de entrada do NVDA.
- Correção de falhas COMError em aplicativos específicos como Firefox e Word.
- Adicionado mecanismo automático de repetição para erros de servidor.

## Alterações na versão 1.0

- Lançamento inicial.
