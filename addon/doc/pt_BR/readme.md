# Vision Assistant Pro Documentation

## Vision Assistant Pro

**Vision Assistant Pro** é um assistente de IA avançado e multimodal para o NVDA. Ele utiliza os modelos Gemini do Google para fornecer leitura de tela inteligente, tradução, ditado por voz e análise de documentos.

*Este complemento foi lançado para a comunidade em homenagem ao Dia Internacional das Pessoas com Deficiência.*

## 1. Configuração e Ajustes

Vá para **Menu NVDA > Preferências > Configurações > Vision Assistant Pro**.

* **Chave de API:** Obrigatória. Obtenha uma chave gratuita no [Google AI Studio](https://aistudio.google.com/).
* **Modelo:** Escolha `gemini-2.5-flash-lite` (mais rápido) ou modelos Flash padrão.
* **Idiomas:** Defina os idiomas de origem, destino e resposta da IA.
* **Troca Inteligente (Smart Swap):** Alterna automaticamente os idiomas caso o texto de origem coincida com o idioma de destino.

## 2. Atalhos Globais

Para garantir máxima compatibilidade com layouts de laptop, todos os atalhos usam **NVDA + Control + Shift**.

| Atalho            | Função                            | Descrição                                                                               |
| ----------------- | --------------------------------- | --------------------------------------------------------------------------------------- |
| NVDA+Ctrl+Shift+T | Tradutor Inteligente              | Traduz o texto sob o cursor de navegação. Prioriza o texto selecionado.                 |
| NVDA+Ctrl+Shift+Y | Tradutor da Área de Transferência | Traduz o conteúdo da área de transferência. **Recomendado para navegadores.**           |
| NVDA+Ctrl+Shift+S | Ditado Inteligente                | Converte fala em texto. Pressione uma vez para iniciar, novamente para parar e digitar. |
| NVDA+Ctrl+Shift+R | Refinador de Texto                | Resume, corrige gramática, explica ou executa **Prompts Personalizados**.               |
| NVDA+Ctrl+Shift+C | Solucionador de CAPTCHA           | Captura e resolve CAPTCHA automaticamente.                                              |
| NVDA+Ctrl+Shift+V | Visão de Objetos                  | Descreve o objeto do navegador com chat de acompanhamento.                              |
| NVDA+Ctrl+Shift+O | Visão da Tela Inteira             | Analisa o layout e conteúdo da tela inteira.                                            |
| NVDA+Ctrl+Shift+D | Análise de Documentos             | Conversa com arquivos PDF/TXT/MD/PY.                                                    |
| NVDA+Ctrl+Shift+F | OCR de Arquivo                    | OCR direto de imagem/arquivo PDF.                                                       |
| NVDA+Ctrl+Shift+A | Transcrição de Áudio              | Transcreve arquivos MP3/WAV/OGG.                                                        |
| NVDA+Ctrl+Shift+L | Última Tradução                   | Reproduz a última tradução sem usar a API.                                              |
| NVDA+Ctrl+Shift+U | Verificação de Atualizações       | Verifica a versão mais recente no GitHub.                                               |
| NVDA+Ctrl+Shift+I | Relatório de Status               | Anuncia o status atual (ex.: “Enviando…”, “Ocioso”).                                    |

## 3. Prompts Personalizados & Variáveis

Crie comandos em Configurações: `Nome:Texto do Prompt` (separados por `|` ou linhas novas).

### Variáveis Disponíveis

| Variável        | Descrição                                           | Tipo de Entrada   |
| --------------- | --------------------------------------------------- | ----------------- |
| `[selection]`   | Texto atualmente selecionado                        | Texto             |
| `[clipboard]`   | Conteúdo da área de transferência                   | Texto             |
| `[screen_obj]`  | Captura do objeto do navegador                      | Imagem            |
| `[screen_full]` | Captura da tela inteira                             | Imagem            |
| `[file_ocr]`    | Seleciona imagem/PDF/TIFF (padrão: “Extrair texto”) | Imagem, PDF, TIFF |
| `[file_read]`   | Seleciona documento de texto                        | TXT, Código, PDF  |
| `[file_audio]`  | Seleciona arquivo de áudio                          | MP3, WAV, OGG     |

### Exemplos de Prompts Personalizados

* **OCR Rápido:** `Meu OCR:[file_ocr]`
* **Traduzir Imagem:** `Traduzir Img:Extraia o texto desta imagem e traduza para persa. [file_ocr]`
* **Analisar Áudio:** `Sumário do Áudio:Ouça esta gravação e resuma os pontos principais. [file_audio]`
* **Depurar Código:** `Debug:Encontre erros neste código e explique-os: [selection]`

**Nota:** Upload de arquivos limitado a 15MB. Requer internet. TIFF com múltiplas páginas é suportado.

## Alterações da Versão 2.8

* Adicionada tradução para italiano.
* **Relatório de Status:** Novo comando (NVDA+Control+Shift+I) para anunciar o status atual do complemento (ex.: “Enviando…”, “Analisando…”).
* **Exportar HTML:** O botão “Salvar Conteúdo” agora salva a saída como HTML formatado, preservando estilos como títulos e negrito.
* **Interface de Configurações:** Layout aprimorado com agrupamento acessível.
* **Novos Modelos:** Suporte para gemini-flash-latest e gemini-flash-lite-latest.
* **Idiomas:** Adicionado o idioma nepali.
* **Lógica do Menu Refine:** Corrigido bug crítico onde “Refinar Texto” falhava se o idioma do NVDA não fosse inglês.
* **Ditado:** Detecção de silêncio aprimorada para evitar texto incorreto quando não há fala.
* **Configurações de Atualização:** “Verificar atualizações na inicialização” agora vem desativado por padrão para cumprir políticas da Add-on Store.
* Limpeza de código.

## Alterações da Versão 2.7

* Estrutura do projeto migrada para o modelo oficial de complementos da NV Access para melhor conformidade.
* Implementada lógica automática de repetição para erros HTTP 429 (limite de requisições).
* Otimização de prompts de tradução para maior precisão e melhor lógica do “Smart Swap”.
* Tradução russa atualizada.

## Alterações da Versão 2.6

* Adicionado suporte à tradução para russo (Obrigado ao nvda-ru).
* Mensagens de erro atualizadas com feedback mais claro sobre conectividade.
* Idioma de destino padrão alterado para inglês.

## Alterações da Versão 2.5

* Adicionado comando nativo de OCR de arquivo (NVDA+Control+Shift+F).
* Adicionado botão “Salvar Chat” nos diálogos de resultado.
* Implementado suporte completo à localização (i18n).
* Feedback de áudio migrado para o módulo nativo de tons do NVDA.
* Alterado para a API de Arquivos do Gemini para melhor manipulação de PDFs e áudios.
* Corrigido travamento ao traduzir texto contendo chaves ({ }).

## Alterações da Versão 2.1.1

* Corrigido erro onde a variável `[file_ocr]` não funcionava corretamente em Prompts Personalizados.

## Alterações da Versão 2.1

* Padronizados todos os atalhos para NVDA+Control+Shift para eliminar conflitos com o layout Laptop e teclas do sistema.

## Alterações da Versão 2.0

* Implementado sistema de Autoatualização integrado.
* Adicionado Cache de Tradução Inteligente para recuperar instantaneamente traduções anteriores.
* Adicionada Memória de Conversa para refinar resultados contextualmente nos diálogos de chat.
* Adicionado comando dedicado para tradução da área de transferência (NVDA+Control+Shift+Y).
* Otimização dos prompts de IA para impor rigorosamente o idioma de destino.
* Corrigido travamento causado por caracteres especiais no texto de entrada.

## Alterações da Versão 1.5

* Adicionado suporte para mais de 20 novos idiomas.
* Implementado diálogo interativo de Refinamento para perguntas de acompanhamento.
* Adicionada função nativa de Ditado Inteligente.
* Adicionada categoria “Vision Assistant” ao diálogo de gestos de entrada do NVDA.
* Corrigidos travamentos COMError em aplicativos como Firefox e Word.
* Adicionado mecanismo automático de repetição para erros de servidor.

## Alterações da Versão 1.0

* Lançamento inicial.
