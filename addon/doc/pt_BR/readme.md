# Documentação do Vision Assistant Pro

## Vision Assistant Pro

**Vision Assistant Pro** é um assistente de IA avançado e multimodal para o NVDA. Ele utiliza os modelos Gemini do Google para oferecer leitura inteligente de tela, tradução, ditado por voz e recursos de análise de documentos.

_Este complemento foi lançado para a comunidade em homenagem ao Dia Internacional das Pessoas com Deficiência._

## 1. Configuração & Ajustes

Acesse **Menu do NVDA > Preferências > Configurações > Vision Assistant Pro**.

- **Chave de API:** Obrigatória. Obtenha uma chave gratuita no [Google AI Studio](https://aistudio.google.com/).
- **Modelo:** Escolha `gemini-2.5-flash-lite` (mais rápido) ou os modelos Flash padrão.
- **Idiomas:** Defina os idiomas de Origem, Destino e Resposta da IA.
- **Troca Inteligente (Smart Swap):** Alterna automaticamente os idiomas se o texto de origem corresponder ao idioma de destino.

## 2. Atalhos Globais

Para garantir máxima compatibilidade com layouts de notebook, todos os atalhos usam **NVDA + Control + Shift**.

| Atalho | Função | Descrição |
| --- | --- | --- |
| NVDA+Ctrl+Shift+T | Tradutor Inteligente | Traduz o texto sob o cursor de navegação. Prioriza texto selecionado. |
| NVDA+Ctrl+Shift+Y | Tradutor da Área de Transferência | Traduz o conteúdo da área de transferência. |
| NVDA+Ctrl+Shift+S | Ditado Inteligente | Converte fala em texto. Pressione uma vez para iniciar e novamente para parar e digitar. |
| NVDA+Ctrl+Shift+R | Refinador de Texto | Resume, corrige gramática, explica ou executa **Prompts Personalizados**. |
| NVDA+Ctrl+Shift+C | Solucionador de CAPTCHA | Captura e resolve CAPTCHAs automaticamente. |
| NVDA+Ctrl+Shift+V | Visão de Objeto | Descreve o objeto do navegador com chat de acompanhamento. |
| NVDA+Ctrl+Shift+O | Visão de Tela Inteira | Analisa todo o layout e conteúdo da tela. |
| NVDA+Ctrl+Shift+D | Análise de Documento | Converse com arquivos PDF/TXT/MD/PY. |
| NVDA+Ctrl+Shift+F | OCR de Arquivo | OCR direto a partir de arquivos de imagem/PDF. |
| NVDA+Ctrl+Shift+A | Transcrição de Áudio | Transcreve arquivos MP3/WAV/OGG. |
| NVDA+Ctrl+Shift+L | Última Tradução | Releia a última tradução sem usar a API. |
| NVDA+Ctrl+Shift+U | Verificação de Atualizações | Verifica no GitHub a versão mais recente. |
| NVDA+Ctrl+Shift+I | Relato de Status | Anuncia o status atual (ex.: “Enviando...”, “Ocioso”). |

## 3. Prompts Personalizados & Variáveis

Crie comandos em Configurações: `Nome:Texto do Prompt` (separe com `|` ou novas linhas).

### Variáveis Disponíveis

- [selection] - Texto atualmente selecionado (Tipo: Texto)
- [clipboard] - Conteúdo da área de transferência (Tipo: Texto)
- [screen_obj] - Captura de tela do objeto do navegador (Tipo: Imagem)
- [screen_full] - Captura de tela inteira (Tipo: Imagem)
- [file_ocr] - Selecionar imagem/PDF/TIFF (padrão: "Extrair texto") (Tipo: Imagem, PDF, TIFF)
- [file_read] - Selecionar documento de texto (Tipo: TXT, Código, PDF)
- [file_audio] - Selecionar arquivo de áudio (Tipo: MP3, WAV, OGG)

### Exemplos de Prompts Personalizados

- **OCR Rápido:** `Meu OCR:[file_ocr]`
- **Traduzir Imagem:** `Traduzir Img:Extraia o texto desta imagem e traduza para persa. [file_ocr]`
- **Analisar Áudio:** `Resumir Áudio:Ouça esta gravação e resuma os pontos principais. [file_audio]`
- **Depurador de Código:** `Depurar:Encontre erros neste código e explique-os: [selection]`

**Nota:** Uma conexão ativa com a internet é necessária para todos os recursos de IA. Arquivos TIFF com múltiplas páginas são processados automaticamente.

## Alterações na versão 3.0

- **Novos Idiomas:** Adicionadas traduções para **persa** e **vietnamita**.
- **Modelos de IA Expandidos:** Reorganizada a lista de seleção de modelos com prefixos claros (`[Free]`, `[Pro]`, `[Auto]`) para ajudar os usuários a distinguir entre modelos gratuitos e limitados por taxa (pagos). Adicionado suporte ao **Gemini 3.0 Pro** e **Gemini 2.0 Flash Lite**.
- **Estabilidade do Ditado:** Melhorada significativamente a estabilidade do Ditado Inteligente. Adicionada uma verificação de segurança para ignorar clipes de áudio com menos de 1 segundo, evitando alucinações da IA e erros vazios.
- **Manipulação de Arquivos:** Corrigido um problema em que o envio de arquivos com nomes que não estavam em inglês falhava.
- **Otimização de Prompts:** Melhorada a lógica de tradução e estruturados os resultados de Visão.

## Alterações na versão 2.9

- **Adicionadas traduções para francês e turco.**
- **Visualização Formatada:** Adicionado um botão “Visualizar Formatado” nas janelas de chat para ver a conversa com estilo adequado (Títulos, Negrito, Código) em uma janela padrão navegável.
- **Configuração de Markdown:** Adicionada uma nova opção “Limpar Markdown no Chat” em Configurações. Ao desmarcar, os usuários podem ver a sintaxe Markdown bruta (ex.: `**`, `#`) na janela de chat.
- **Gerenciamento de Diálogos:** Corrigido um problema em que as janelas “Refinar Texto” ou de chat abriam múltiplas vezes ou não recebiam foco corretamente.
- **Melhorias de UX:** Padronizados os títulos das caixas de diálogo de arquivos para “Abrir” e removidos anúncios de fala redundantes (ex.: “Abrindo menu...”) para uma experiência mais fluida.

## Alterações na versão 2.8

- Adicionada tradução para italiano.
- **Relato de Status:** Adicionado um novo comando (NVDA+Control+Shift+I) para anunciar o status atual do complemento (ex.: “Enviando...”, “Analisando...”).
- **Exportação HTML:** O botão “Salvar Conteúdo” nas janelas de resultado agora salva a saída como um arquivo HTML formatado, preservando estilos como títulos e texto em negrito.
- **Interface de Configurações:** Melhorado o layout do painel de Configurações com agrupamento acessível.
- **Novos Modelos:** Adicionado suporte a gemini-flash-latest e gemini-flash-lite-latest.
- **Idiomas:** Adicionado o nepalês aos idiomas suportados.
- **Lógica do Menu Refinar:** Corrigido um bug crítico em que os comandos “Refinar Texto” falhavam se o idioma da interface do NVDA não fosse inglês.
- **Ditado:** Melhorada a detecção de silêncio para evitar saída incorreta de texto quando não há fala.
- **Configurações de Atualização:** “Verificar atualizações ao iniciar” agora vem desativado por padrão para cumprir as políticas da Loja de Complementos.
- Limpeza de código.

## Alterações na versão 2.7

- Migrada a estrutura do projeto para o modelo oficial de Complementos da NV Access, garantindo melhor conformidade com os padrões.
- Implementada lógica automática de nova tentativa para erros HTTP 429 (Limite de Taxa), garantindo confiabilidade durante picos de tráfego.
- Otimizados os prompts de tradução para maior precisão e melhor tratamento da lógica de “Troca Inteligente”.
- Atualizada a tradução para russo.

## Alterações na versão 2.6

- Adicionado suporte à tradução para russo (agradecimentos ao nvda-ru).
- Atualizadas mensagens de erro para fornecer feedback mais descritivo sobre conectividade.
- Alterado o idioma de destino padrão para inglês.

## Alterações na versão 2.5

- Adicionado comando nativo de OCR de arquivos (NVDA+Control+Shift+F).
- Adicionado botão “Salvar Chat” nas janelas de resultado.
- Implementado suporte completo à localização (i18n).
- Migrado o feedback de áudio para o módulo nativo de tons do NVDA.
- Alterada a API para Gemini File API, melhorando o tratamento de arquivos PDF e de áudio.
- Corrigido travamento ao traduzir textos contendo chaves `{}`.

## Alterações na versão 2.1.1

- Corrigido um problema em que a variável `[file_ocr]` não funcionava corretamente dentro de Prompts Personalizados.

## Alterações na versão 2.1

- Padronizados todos os atalhos para usar NVDA+Control+Shift, eliminando conflitos com o layout de notebook do NVDA e atalhos do sistema.

## Alterações na versão 2.0

- Implementado sistema interno de atualização automática.
- Adicionado cache de Tradução Inteligente para recuperação instantânea de textos traduzidos anteriormente.
- Adicionada Memória de Conversa para refinar resultados contextualmente nas janelas de chat.
- Adicionado comando dedicado de tradução da área de transferência (NVDA+Control+Shift+Y).
- Otimizados os prompts de IA para impor rigorosamente a saída no idioma de destino.
- Corrigido travamento causado por caracteres especiais no texto de entrada.

## Alterações na versão 1.5

- Adicionado suporte para mais de 20 novos idiomas.
- Implementado diálogo interativo de refinamento para perguntas de acompanhamento.
- Adicionado recurso nativo de Ditado Inteligente.
- Adicionada a categoria “Vision Assistant” ao diálogo de Gestos de Entrada do NVDA.
- Corrigidos travamentos COMError em aplicativos específicos como Firefox e Word.
- Adicionado mecanismo automático de nova tentativa para erros de servidor.

## Alterações na versão 1.0

- Lançamento inicial.
