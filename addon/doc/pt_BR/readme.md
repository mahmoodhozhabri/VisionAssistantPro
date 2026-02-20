# Documentação do Vision Assistant Pro

**Vision Assistant Pro** é um assistente de IA avançado e multimodal para o NVDA. Ele utiliza os modelos Gemini do Google para fornecer capacidades inteligentes de leitura de tela, tradução, ditado por voz e análise de documentos.

_Este add-on foi lançado para a comunidade em homenagem ao Dia Internacional da Pessoa com Deficiência._

## 1. Configuração & Ajustes

Vá para **Menu NVDA > Preferências > Configurações > Vision Assistant Pro**.

- **Chave API:** Obrigatória. Você pode inserir múltiplas chaves (separadas por vírgulas ou linhas). O assistente alternará automaticamente entre elas se um limite de cota for atingido.
- **Modelo de IA:** Escolha entre os modelos **Flash** (Mais rápido/Gratuito), **Lite**, ou **Pro** (Alta Inteligência).
- **URL do Proxy:** Opcional. Use se o Google estiver bloqueado na sua região. Deve ser um endereço web que funcione como ponte para a API Gemini.
- **Motor OCR:** Escolha entre **Chrome (Rápido)** para resultados rápidos ou **Gemini (Formatado)** para melhor preservação de layout e reconhecimento de tabelas.
- **Voz TTS:** Selecione o estilo de voz preferido para gerar arquivos de áudio a partir das páginas de documentos.
- **Troca Inteligente:** Alterna automaticamente idiomas se o texto de origem coincidir com o idioma de destino.
- **Saída Direta:** Ignora a janela de chat e anuncia a resposta da IA diretamente via fala. **Nota:** Mesmo neste modo, você pode pressionar **Espaço** na camada de comando para reabrir o último resultado em um diálogo de chat.
- **Integração com Área de Transferência:** Copia automaticamente a resposta da IA para a área de transferência.

## 2. Camada de Comando & Atalhos

Para evitar conflitos de teclado, este add-on utiliza uma **Camada de Comando**.

1. Pressione **NVDA + Shift + V** (Tecla Mestre) para ativar a camada (você ouvirá um bip).
2. Solte as teclas e pressione uma das seguintes teclas únicas:

| Tecla         | Função                            | Descrição                                                                                |
| ------------- | --------------------------------- | ---------------------------------------------------------------------------------------- |
| **T**         | Tradutor Inteligente              | Traduz o texto sob o cursor do NVDA ou a seleção.                                        |
| **Shift + T** | Tradutor da Área de Transferência | Traduz o conteúdo atualmente na área de transferência.                                   |
| **R**         | Refinador de Texto                | Resume, Corrige Gramática, Explica ou executa **Prompts Personalizados**.                |
| **V**         | Visão do Objeto                   | Descreve o objeto atual do NVDA.                                                         |
| **O**         | Visão de Tela Cheia               | Analisa todo o layout e conteúdo da tela.                                                |
| **Shift + V** | Análise de Vídeo Online           | Analisa vídeos do **YouTube**, **Instagram**, **TikTok** ou **Twitter (X)**.             |
| **D**         | Leitor de Documentos              | Leitor avançado de PDFs e imagens com seleção de intervalo de páginas.                   |
| **F**         | OCR de Arquivo                    | Reconhecimento direto de texto em imagem, PDF ou arquivos TIFF selecionados.             |
| **A**         | Transcrição de Áudio              | Transcreve arquivos MP3, WAV ou OGG para texto.                                          |
| **C**         | Solucionador de CAPTCHA           | Captura e resolve CAPTCHAs na tela ou em objetos do NVDA.                                |
| **S**         | Ditado Inteligente                | Converte fala em texto. Pressione para iniciar a gravação, novamente para parar/digitar. |
| **L**         | Relatório de Status               | Anuncia o progresso atual (ex.: "Escaneando...", "Ocioso").                              |
| **U**         | Verificar Atualizações            | Verifica manualmente no GitHub a versão mais recente do add-on.                          |
| **Espaço**    | Recordar Último Resultado         | Mostra a última resposta da IA em um diálogo de chat para revisão ou acompanhamento.     |
| **H**         | Ajuda de Comandos                 | Exibe uma lista de todos os atalhos disponíveis na camada de comando.                    |

### 2.1 Atalhos do Leitor de Documentos (Dentro do Visualizador)

Após abrir um documento com o comando **D**:

- **Ctrl + PageDown:** Avança para a próxima página (anuncia o número da página).
- **Ctrl + PageUp:** Volta para a página anterior (anuncia o número da página).
- **Alt + A:** Abre um diálogo de chat para fazer perguntas sobre o documento.
- **Alt + R:** Força um novo escaneamento da página atual ou de todas as páginas usando o motor Gemini.
- **Alt + G:** Gera e salva um arquivo de áudio de alta qualidade (WAV) do conteúdo.
- **Alt + S / Ctrl + S:** Salva o texto extraído como arquivo TXT ou HTML.

## 3. Prompts Personalizados & Variáveis

Abra **Configurações > Prompts > Gerenciar Prompts...** para configurar prompts do sistema e personalizados.

- **Aba Prompts Padrão:** edite os prompts internos. Você pode resetar um prompt individual ou todos os padrões.
- **Aba Prompts Personalizados:** adicione, edite, remova e reordene prompts personalizados.
- **Botão Guia de Variáveis:** abre uma janela de ajuda com todas as variáveis suportadas e tipos de entrada.

### Variáveis Disponíveis

| Variável        | Descrição                                   | Tipo de Entrada   |
| --------------- | ------------------------------------------- | ----------------- |
| `[selection]`   | Texto atualmente selecionado                | Texto             |
| `[clipboard]`   | Conteúdo da área de transferência           | Texto             |
| `[screen_obj]`  | Captura de tela do objeto do NVDA           | Imagem            |
| `[screen_full]` | Captura de tela completa                    | Imagem            |
| `[file_ocr]`    | Seleciona imagem/PDF para extração de texto | Imagem, PDF, TIFF |
| `[file_read]`   | Seleciona documento para leitura            | TXT, Código, PDF  |
| `[file_audio]`  | Seleciona arquivo de áudio para análise     | MP3, WAV, OGG     |

### Exemplos de Prompts Personalizados

- **OCR Rápido:** `Meu OCR:[file_ocr]`
- **Traduzir Imagem:** `Traduzir Img:Extrair texto desta imagem e traduzir para inglês. [file_ocr]`
- **Analisar Áudio:** `Resumir Áudio:Ouça esta gravação e resuma os pontos principais. [file_audio]`
- **Depurador de Código:** `Depurar:Encontre erros neste código e explique-os: [selection]`

---

**Nota:** Uma conexão ativa à internet é necessária para todos os recursos de IA. Documentos com múltiplas páginas e TIFFs são processados automaticamente.

## 4. Suporte & Comunidade

Fique atualizado com as últimas notícias, recursos e lançamentos:

- **Canal no Telegram:** [t.me/VisionAssistantPro](https://t.me/VisionAssistantPro)
- **Issues no GitHub:** Para relatórios de bugs e solicitações de recursos.

## Alterações na versão 4.6

- **Recordar Resultado Interativo:** Adicionado a tecla **Espaço** na camada de comando, permitindo reabrir instantaneamente a última resposta da IA em uma janela de chat para acompanhamento, mesmo com "Saída Direta" ativa.

- **Hub da Comunidade no Telegram:** Adicionado link "Canal Oficial do Telegram" no menu Ferramentas do NVDA, oferecendo acesso rápido a notícias e lançamentos.
- **Estabilidade de Resposta Aprimorada:** Otimizada a lógica principal de Tradução, OCR e Visão para maior confiabilidade e experiência mais fluida com saída de voz direta.
- **Guia de Interface Melhorado:** Atualizadas descrições de configurações e documentação para explicar melhor o sistema de recordação e seu funcionamento junto à saída direta.

## Alterações na versão 4.5

- **Gerenciador Avançado de Prompts:** Diálogo dedicado para personalizar prompts do sistema padrão e gerenciar prompts do usuário com suporte completo a adicionar, editar, reordenar e visualizar.

- **Suporte Completo a Proxy:** Resolvidos problemas de conectividade garantindo que configurações de proxy do usuário sejam aplicadas em todas as requisições de API, incluindo tradução, OCR e geração de fala.
- **Migração Automática de Dados:** Sistema inteligente que atualiza prompts antigos para formato JSON v2 na primeira execução sem perda de dados.
- **Compatibilidade Atualizada (2025.1):** Versão mínima do NVDA definida para 2025.1 devido a dependências de bibliotecas em recursos avançados como o Leitor de Documentos.
- **Interface de Configurações Otimizada:** Reorganização do gerenciamento de prompts em um diálogo separado para uma experiência mais limpa e acessível.
- **Guia de Variáveis de Prompt:** Guia incorporado dentro dos diálogos de prompt para identificar e usar variáveis dinâmicas como [selection], [clipboard] e [screen_obj].

## Alterações na versão 4.0.3

- **Resiliência de Rede Aprimorada:** Mecanismo de tentativa automática para conexões instáveis e erros temporários do servidor.

- **Diálogo de Tradução Visual:** Janela dedicada para resultados de tradução, permitindo navegação linha a linha em traduções longas, semelhante ao OCR.
- **Visualização Formatada Agregada:** "Ver Formatado" no Leitor de Documentos mostra todas as páginas processadas em uma única janela organizada com cabeçalhos claros.
- **Fluxo de OCR Otimizado:** Pula automaticamente a seleção de intervalo de páginas em documentos de página única.
- **Estabilidade de API Aprimorada:** Autenticação baseada em cabeçalhos para resolver erros "Todas as chaves API falharam" causados por rotação de chave.
- **Correção de Bugs:** Resolvidos crashes potenciais, incluindo erro de foco no diálogo de chat e término do add-on.

## Alterações na versão 4.0.1

- **Leitor de Documentos Avançado:** Novo visualizador para PDFs e imagens com seleção de intervalo de páginas, processamento em segundo plano e navegação contínua `Ctrl+PageUp/Down`.

- **Novo Submenu de Ferramentas:** Submenu dedicado "Vision Assistant" no menu Ferramentas do NVDA para acesso rápido a recursos, configurações e documentação.
- **Personalização Flexível:** Agora é possível escolher motor OCR e voz TTS diretamente no painel de configurações.
- **Suporte a Múltiplas Chaves API:** Suporte a múltiplas chaves Gemini, uma por linha ou separadas por vírgulas.
- **Motor OCR Alternativo:** Novo motor OCR para garantir reconhecimento de texto mesmo com limites de cota do Gemini.
- **Rotação Inteligente de Chaves API:** Alterna automaticamente para a chave mais rápida disponível.
- **Documento para MP3/WAV:** Gera e salva arquivos de áudio de alta qualidade em MP3 (128kbps) e WAV diretamente no leitor.
- **Suporte a Stories do Instagram:** Descrição e análise de Stories via URL.
- **Suporte a TikTok:** Análise completa de vídeos com descrição visual e transcrição de áudio.
- **Diálogo de Atualização Redesenhado:** Interface acessível com caixa de texto rolável para leitura clara das mudanças antes da instalação.
- **Status & UX Unificado:** Padronização de diálogos de arquivo e aprimoramento do comando 'L' para reportar progresso em tempo real.

## Alterações na versão 3.6.0

- **Sistema de Ajuda:** Comando de ajuda (`H`) na Camada de Comando com lista de todos os atalhos e funções.

- **Análise de Vídeo Online:** Suporte expandido para vídeos do **Twitter (X)**. Detecção de URL melhorada para maior confiabilidade.
- **Contribuição para o Projeto:** Diálogo opcional de doação para apoiar atualizações e crescimento contínuo do projeto.

## Alterações na versão 3.5.0

- **Camada de Comando:** Sistema de Camada de Comando (padrão: `NVDA+Shift+V`) para agrupar atalhos sob uma tecla mestre. Ex.: `NVDA+Shift+V` seguido de `T` para tradução.

- **Análise de Vídeo Online:** Análise de vídeos do YouTube e Instagram via URL.

## Alterações na versão 3.1.0

- **Modo Saída Direta:** Resposta da IA diretamente via fala sem abrir diálogo de chat.

- **Integração com Área de Transferência:** Copia automaticamente respostas da IA para a área de transferência.

## Alterações na versão 3.0

- **Novos Idiomas:** Adicionadas traduções para **Persa** e **Vietnamita**.

- **Modelos de IA Expandido:** Lista reorganizada com prefixos claros `[Free]`, `[Pro]`, `[Auto]`. Suporte para **Gemini 3.0 Pro** e **Gemini 2.0 Flash Lite**.
- **Estabilidade do Ditado:** Verificação de áudio inferior a 1 segundo para evitar erros ou respostas vazias.
- **Manipulação de Arquivos:** Corrigido problema com arquivos com nomes não ingleses.
- **Otimização de Prompts:** Lógica de tradução e resultados de visão estruturados.

## Alterações na versão 2.9

- **Traduções em Francês e Turco adicionadas.**

- **Visualização Formatada:** Botão "Ver Formatado" em diálogos de chat para visualizar conversa com estilo (Títulos, Negrito, Código).
- **Configuração Markdown:** Nova opção "Limpar Markdown no Chat". Desmarcar mostra o Markdown cru.
- **Gestão de Diálogos:** Corrigido problema de múltiplas janelas de "Refinar Texto".
- **Melhorias de UX:** Padronização de títulos de diálogos e remoção de anúncios de fala redundantes.

## Alterações na versão 2.8

- Adicionada tradução italiana.

- **Relatório de Status:** Novo comando (NVDA+Control+Shift+I) para anunciar status do add-on.
- **Exportação HTML:** Botão "Salvar Conteúdo" salva saída como HTML formatado.
- **Interface de Configurações:** Agrupamento acessível aprimorado.
- **Novos Modelos:** Suporte para gemini-flash-latest e gemini-flash-lite-latest.
- **Idiomas:** Adicionado Nepali.
- **Lógica do Menu Refine:** Corrigido bug crítico em comandos "Refine Text".
- **Ditado:** Detecção de silêncio aprimorada.
- **Atualizar Configurações:** "Verificar atualizações ao iniciar" desativado por padrão.
- Limpeza de código.

## Alterações na versão 2.7

- Estrutura do projeto migrada para o Template oficial NV Access Add-on.

- Lógica de retry automático para HTTP 429 implementada.
- Prompts de tradução otimizados para maior precisão e melhor lógica de "Smart Swap".
- Tradução russa atualizada.

## Alterações na versão 2.6

- Suporte a tradução russa adicionado (Obrigado nvda-ru).

- Mensagens de erro atualizadas para feedback descritivo sobre conectividade.
- Idioma alvo padrão alterado para inglês.

## Alterações na versão 2.5

- Comando OCR de Arquivo Nativo (NVDA+Control+Shift+F) adicionado.

- Botão "Salvar Chat" adicionado em diálogos de resultado.
- Suporte completo a localização (i18n).
- Feedback de áudio migrado para módulo de tons nativo do NVDA.
- API Gemini para arquivos PDF e áudio.
- Corrigido crash ao traduzir textos com chaves `{}`.

## Alterações na versão 2.1.1

- Corrigido problema com variável [file_ocr] em Prompts Personalizados.

## Alterações na versão 2.1

- Todos os atalhos padronizados para NVDA+Control+Shift para evitar conflitos.

## Alterações na versão 2.0

- Sistema de Auto-Atualização incorporado.

- Cache de Tradução Inteligente adicionado.
- Memória de Conversa para refinar resultados em chat.
- Comando de Tradução da Área de Transferência dedicado (NVDA+Control+Shift+Y).
- Prompts de IA otimizados para saída no idioma alvo.
- Corrigido crash causado por caracteres especiais no texto.

## Alterações na versão 1.5

- Suporte para mais de 20 novos idiomas.

- Diálogo Interativo Refine para perguntas de acompanhamento.
- Ditado Inteligente nativo adicionado.
- Categoria "Vision Assistant" no diálogo de Gestos de Entrada do NVDA.
- Corrigido crash COMError em apps como Firefox e Word.
- Mecanismo de retry automático para erros de servidor.

## Alterações na versão 1.0

- Lançamento inicial.
