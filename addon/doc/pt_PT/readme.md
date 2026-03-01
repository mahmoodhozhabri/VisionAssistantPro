# Documentação do Vision Assistant Pro

**Vision Assistant Pro** é um assistente de IA avançado e multimodal para NVDA. Utiliza motores de IA de classe mundial para fornecer leitura inteligente de ecrã, tradução, ditado por voz e análise de documentos.

_Este complemento foi lançado à comunidade em homenagem ao Dia Internacional das Pessoas com Deficiência._

## 1. Instalação e Configuração

Aceda a **Menu NVDA > Preferências > Definições > Vision Assistant Pro**.

### 1.1 Definições de Ligação

- **Fornecedor:** Selecione o seu serviço de IA preferido. Os fornecedores suportados incluem **Google Gemini**, **OpenAI**, **Mistral**, **Groq** e **Personalizado** (servidores compatíveis com OpenAI como Ollama/LM Studio).
- **Nota Importante:** Recomendamos fortemente a utilização do **Google Gemini** para o melhor desempenho e precisão (especialmente para análise de imagens/ficheiros).
- **Chave API:** Obrigatória. Pode introduzir várias chaves (separadas por vírgulas ou novas linhas) para rotação automática.
- **Obter Modelos:** Após introduzir a sua chave API, prima este botão para transferir a lista mais recente de modelos disponíveis do fornecedor.
- **Modelo de IA:** Selecione o modelo principal utilizado para chat geral e análise.

### 1.2 Encaminhamento Avançado de Modelos (Fornecedores Nativos)

_Disponível para Gemini, OpenAI, Groq e Mistral._

> **⚠️ Aviso:** Estas definições destinam-se **apenas a utilizadores avançados**. Se não tiver a certeza do que faz um modelo específico, deixe esta opção **desmarcada**. Selecionar um modelo incompatível para uma tarefa (por exemplo, um modelo apenas de texto para Vision) causará erros e impedirá o funcionamento do complemento.

Marque **"Encaminhamento Avançado de Modelos (Específico por Tarefa)"** para desbloquear controlo detalhado. Isto permite selecionar modelos específicos na lista pendente para diferentes tarefas:

- **Modelo OCR / Vision:** Escolha um modelo especializado para analisar imagens.
- **Speech-to-Text (STT):** Escolha um modelo específico para ditado.
- **Text-to-Speech (TTS):** Escolha um modelo para gerar áudio.
  _Nota: Funcionalidades não suportadas (por exemplo, TTS para Groq) serão ocultadas automaticamente._

### 1.3 Configuração Avançada de Endpoints (Fornecedor Personalizado)

_Disponível apenas quando "Personalizado" está selecionado._

> **⚠️ Aviso:** Esta secção permite configuração manual da API e foi concebida para **utilizadores experientes** que executam servidores locais ou proxies. URLs ou nomes de modelo incorretos irão quebrar a ligação. Se não souber exatamente o que são estes endpoints, mantenha esta opção **desmarcada**.

Marque **"Configuração Avançada de Endpoints"** para introduzir manualmente os detalhes do servidor. Ao contrário dos fornecedores nativos, aqui deve **escrever** os URLs e Nomes de Modelo específicos:

- **URL da Lista de Modelos:** O endpoint para obter os modelos disponíveis.
- **URL do Endpoint OCR/STT/TTS:** URLs completos para serviços específicos (por exemplo, `http://localhost:11434/v1/audio/speech`).
- **Modelos Personalizados:** Escreva manualmente o nome do modelo (por exemplo, `llama3:8b`) para cada tarefa.

### 1.4 Preferências Gerais

- **Motor OCR:** Escolha entre **Chrome (Rápido)** para resultados rápidos ou **Gemini (Formatado)** para melhor preservação do esquema.
  - _Nota:_ Se selecionar "Gemini (Formatado)" mas o fornecedor estiver definido como OpenAI/Groq, o complemento encaminhará inteligentemente a imagem para o modelo de visão do fornecedor ativo.
- **Voz TTS:** Selecione o estilo de voz preferido. Esta lista é atualizada dinamicamente com base no fornecedor ativo.
- **Criatividade (Temperatura):** Controla a aleatoriedade da IA. Valores mais baixos são melhores para tradução/OCR precisa.
- **URL de Proxy:** Configure esta opção se os serviços de IA estiverem restritos na sua região (suporta proxies locais como `127.0.0.1` ou URLs de ponte).

## 2. Camada de Comandos e Atalhos

Para evitar conflitos de teclado, este complemento utiliza uma **Camada de Comandos**.

1. Prima **NVDA + Shift + V** (Tecla Mestra) para ativar a camada (ouvirá um sinal sonoro).
2. Solte as teclas e, em seguida, prima uma das seguintes teclas individuais:

| Tecla         | Função                            | Descrição                                                                               |
| ------------- | --------------------------------- | --------------------------------------------------------------------------------------- |
| **T**         | Tradutor Inteligente              | Traduz o texto sob o cursor de navegação ou seleção.                                    |
| **Shift + T** | Tradutor da Área de Transferência | Traduz o conteúdo atualmente na área de transferência.                                  |
| **R**         | Refinador de Texto                | Resumir, Corrigir Gramática, Explicar ou executar **Prompts Personalizados**.           |
| **V**         | Vision do Objeto                  | Descreve o objeto atual do navegador.                                                   |
| **O**         | Vision de Ecrã Completo           | Analisa todo o esquema e conteúdo do ecrã.                                              |
| **Shift + V** | Análise de Vídeo Online           | Analisa vídeos do **YouTube**, **Instagram**, **TikTok** ou **Twitter (X)**.            |
| **D**         | Leitor de Documentos              | Leitor avançado para PDF e imagens com seleção de intervalo de páginas.                 |
| **F**         | OCR de Ficheiro                   | Reconhecimento direto de texto a partir de imagens, PDF ou ficheiros TIFF selecionados. |
| **A**         | Transcrição de Áudio              | Transcreve ficheiros MP3, WAV ou OGG para texto.                                        |
| **C**         | Solucionador de CAPTCHA           | Captura e resolve CAPTCHAs (Suporta portais governamentais).                            |
| **S**         | Ditado Inteligente                | Converte fala em texto. Prima para iniciar a gravação, novamente para parar/escrever.   |
| **L**         | Relatório de Estado               | Anuncia o progresso atual (por exemplo, "A analisar...", "Inativo").                    |
| **U**         | Verificar Atualizações            | Verifica manualmente no GitHub a versão mais recente do complemento.                    |
| **Espaço**    | Recuperar Último Resultado        | Mostra a última resposta da IA num diálogo de chat para revisão ou seguimento.          |
| **H**         | Ajuda de Comandos                 | Apresenta uma lista de todos os atalhos disponíveis dentro da camada de comandos.       |

### 2.1 Atalhos do Leitor de Documentos (Dentro do Visualizador)

- **Ctrl + PageDown:** Ir para a página seguinte.
- **Ctrl + PageUp:** Ir para a página anterior.
- **Alt + A:** Abrir um diálogo de chat para colocar perguntas sobre o documento.
- **Alt + R:** Forçar uma **Nova Análise com IA** utilizando o fornecedor ativo.
- **Alt + G:** Gerar e guardar um ficheiro de áudio de alta qualidade (WAV/MP3). _Oculto se o fornecedor não suportar TTS._
- **Alt + S / Ctrl + S:** Guardar o texto extraído como ficheiro TXT ou HTML.

## 3. Prompts Personalizados e Variáveis

Pode gerir os prompts em **Definições > Prompts > Gerir Prompts...**.

### Variáveis Suportadas

- `[selection]`: Texto atualmente selecionado.
- `[clipboard]`: Conteúdo da área de transferência.
- `[screen_obj]`: Captura de ecrã do objeto de navegação.
- `[screen_full]`: Captura de ecrã completa.
- `[file_ocr]`: Selecionar ficheiro de imagem/PDF para extração de texto.
- `[file_read]`: Selecionar documento para leitura (TXT, Código, PDF).
- `[file_audio]`: Selecionar ficheiro de áudio para análise (MP3, WAV, OGG).

---

**Nota:** É necessária uma ligação ativa à internet para todas as funcionalidades de IA. Documentos com várias páginas são processados automaticamente.

## 4. Suporte e Comunidade

Mantenha-se atualizado com as últimas notícias, funcionalidades e lançamentos:

- **Canal Telegram:** [t.me/VisionAssistantPro](https://t.me/VisionAssistantPro)
- **GitHub Issues:** Para relatórios de erros e pedidos de funcionalidades.

---

## Alterações na versão 5.0

- **Arquitetura Multi-Fornecedor**: Adicionado suporte completo para **OpenAI**, **Groq** e **Mistral**, juntamente com Google Gemini. Os utilizadores podem agora escolher o backend de IA preferido.
- **Encaminhamento Avançado de Modelos**: Utilizadores de fornecedores nativos (Gemini, OpenAI, etc.) podem agora selecionar modelos específicos a partir de uma lista pendente para diferentes tarefas (OCR, STT, TTS).
- **Configuração Avançada de Endpoints**: Utilizadores do fornecedor personalizado podem introduzir manualmente URLs e nomes de modelo específicos para controlo granular sobre servidores locais ou de terceiros.
- **Visibilidade Inteligente de Funcionalidades**: O menu de definições e a interface do Leitor de Documentos ocultam automaticamente funcionalidades não suportadas (como TTS) com base no fornecedor selecionado.
- **Obtenção Dinâmica de Modelos**: O complemento obtém agora a lista de modelos disponíveis diretamente da API do fornecedor, garantindo compatibilidade com novos modelos assim que são lançados.
- **OCR e Tradução Híbridos**: Lógica otimizada para usar Google Translate para maior rapidez ao utilizar OCR do Chrome, e tradução com IA ao utilizar motores Gemini/Groq/OpenAI.
- **"Nova Análise com IA" Universal**: A funcionalidade de nova análise do Leitor de Documentos já não está limitada ao Gemini. Agora utiliza o fornecedor de IA atualmente ativo para reprocessar páginas.

## Alterações na versão 4.6

- **Recuperação Interativa de Resultados:** Adicionada a tecla **Espaço** à camada de comandos, permitindo aos utilizadores reabrir instantaneamente a última resposta da IA numa janela de chat para perguntas de seguimento, mesmo quando o modo "Saída Direta" está ativo.
- **Centro da Comunidade Telegram:** Adicionado um link para o "Canal Oficial do Telegram" no menu Ferramentas do NVDA, proporcionando uma forma rápida de se manter atualizado com as últimas notícias, funcionalidades e lançamentos.
- **Maior Estabilidade de Respostas:** Otimizada a lógica principal das funcionalidades de Tradução, OCR e Vision para garantir desempenho mais fiável e uma experiência mais fluida ao utilizar saída direta por voz.
- **Melhoria nas Orientações da Interface:** Atualizadas as descrições nas definições e documentação para explicar melhor o novo sistema de recuperação e como funciona em conjunto com as definições de saída direta.

## Alterações na versão 4.5

- **Gestor Avançado de Prompts:** Introduzido um diálogo de gestão dedicado nas definições para personalizar prompts de sistema predefinidos e gerir prompts definidos pelo utilizador com suporte completo para adicionar, editar, reordenar e pré-visualizar.
- **Suporte Abrangente de Proxy:** Resolvidos problemas de conectividade de rede garantindo que as definições de proxy configuradas pelo utilizador são rigorosamente aplicadas a todos os pedidos de API, incluindo tradução, OCR e geração de voz.
- **Migração Automática de Dados:** Integrado um sistema de migração inteligente para atualizar automaticamente configurações de prompts antigas para um formato JSON v2 robusto na primeira execução, sem perda de dados.
- **Compatibilidade Atualizada (2025.1):** Definida a versão mínima necessária do NVDA para 2025.1 devido a dependências de bibliotecas em funcionalidades avançadas como o Leitor de Documentos, garantindo desempenho estável.
- **Interface de Definições Otimizada:** Simplificada a interface de definições ao reorganizar a gestão de prompts num diálogo separado, proporcionando uma experiência de utilizador mais limpa e acessível.
- **Guia de Variáveis de Prompt:** Adicionado um guia incorporado nos diálogos de prompts para ajudar os utilizadores a identificar e utilizar facilmente variáveis dinâmicas como [selection], [clipboard] e [screen_obj].

## Alterações na versão 4.0.3

- **Maior Resiliência de Rede:** Adicionado um mecanismo de repetição automática para melhor lidar com ligações à internet instáveis e erros temporários do servidor, garantindo respostas de IA mais fiáveis.
- **Diálogo Visual de Tradução:** Introduzida uma janela dedicada para resultados de tradução. Os utilizadores podem agora navegar e ler traduções longas linha a linha, de forma semelhante aos resultados de OCR.
- **Vista Formatada Agregada:** A funcionalidade "Ver Formatado" no Leitor de Documentos apresenta agora todas as páginas processadas numa única janela organizada com cabeçalhos de página claros.
- **Fluxo de Trabalho OCR Otimizado:** Ignora automaticamente a seleção de intervalo de páginas para documentos de página única, tornando o processo de reconhecimento mais rápido e contínuo.
- **Estabilidade de API Melhorada:** Alterado para um método de autenticação baseado em cabeçalhos mais robusto, resolvendo possíveis erros "Todas as Chaves API falharam" causados por conflitos de rotação de chaves.
- **Correções de Erros:** Resolvidos vários possíveis bloqueios, incluindo um problema durante a finalização do complemento e um erro de foco no diálogo de chat.

## Alterações na versão 4.0.1

- **Leitor de Documentos Avançado:** Um novo visualizador poderoso para PDF e imagens com seleção de intervalo de páginas, processamento em segundo plano e navegação contínua com `Ctrl+PageUp/Down`.
- **Novo Submenu Ferramentas:** Adicionado um submenu dedicado "Vision Assistant" no menu Ferramentas do NVDA para acesso mais rápido às funcionalidades principais, definições e documentação.
- **Personalização Flexível:** Pode agora escolher o seu motor OCR e voz TTS preferidos diretamente no painel de definições.
- **Suporte para Múltiplas Chaves API:** Adicionado suporte para múltiplas chaves API do Gemini. Pode introduzir uma chave por linha ou separá-las por vírgulas nas definições.
- **Motor OCR Alternativo:** Introduzido um novo motor OCR para garantir reconhecimento de texto fiável mesmo ao atingir limites de quota da API Gemini.
- **Rotação Inteligente de Chaves API:** Alterna automaticamente e memoriza a chave API funcional mais rápida para contornar limites de quota.
- **Documento para MP3/WAV:** Integrada capacidade de gerar e guardar ficheiros de áudio de alta qualidade nos formatos MP3 (128kbps) e WAV diretamente no leitor.
- **Suporte para Instagram Stories:** Adicionada a capacidade de descrever e analisar Instagram Stories utilizando os respetivos URLs.
- **Suporte para TikTok:** Introduzido suporte para vídeos TikTok, permitindo descrição visual completa e transcrição de áudio dos clips.
- **Diálogo de Atualização Redesenhado:** Apresenta uma nova interface acessível com uma caixa de texto rolável para ler claramente as alterações de versão antes da instalação.
- **Estado e UX Unificados:** Padronizados os diálogos de ficheiros em todo o complemento e melhorado o comando 'L' para relatar progresso em tempo real.

## Alterações na versão 3.6.0

- **Sistema de Ajuda:** Adicionado um comando de ajuda (`H`) dentro da Camada de Comandos para fornecer uma lista de fácil acesso de todos os atalhos e respetivas funções.
- **Análise de Vídeo Online:** Suporte expandido para incluir vídeos do **Twitter (X)**. Também melhorada a deteção de URLs e estabilidade para uma experiência mais fiável.
- **Contribuição para o Projeto:** Adicionado um diálogo opcional de donativo para utilizadores que desejem apoiar futuras atualizações e o crescimento contínuo do projeto.

## Alterações na versão 3.5.0

\* \*\*Camada de Comandos:\*\* Introduzido um sistema de Camada de Comandos (predefinição: `NVDA+Shift+V`) para agrupar atalhos sob uma única tecla mestra. Por exemplo, em vez de premir `NVDA+Control+Shift+T` para tradução, agora prime `NVDA+Shift+V` seguido de `T`. \* \*\*Análise de Vídeo Online:\*\* Adicionada uma nova funcionalidade para analisar vídeos do YouTube e Instagram diretamente através de um URL.

## Alterações na versão 3.1.0

- **Modo de Saída Direta:** Adicionada uma opção para ignorar o diálogo de chat e ouvir as respostas da IA diretamente por voz para uma experiência mais rápida e fluida.
- **Integração com a Área de Transferência:** Adicionada uma nova definição para copiar automaticamente as respostas da IA para a área de transferência.

## Alterações na versão 3.0

- **Novos Idiomas:** Adicionadas traduções em **Persa** e **Vietnamita**.
- **Modelos de IA Expandidos:** Reorganizada a lista de seleção de modelos com prefixos claros (`[Free]`, `[Pro]`, `[Auto]`) para ajudar os utilizadores a distinguir entre modelos gratuitos e limitados por taxa (pagos). Adicionado suporte para **Gemini 3.0 Pro** e **Gemini 2.0 Flash Lite**.
- **Estabilidade do Ditado:** Melhorada significativamente a estabilidade do Ditado Inteligente. Adicionada uma verificação de segurança para ignorar clips de áudio com menos de 1 segundo, prevenindo alucinações da IA e erros vazios.
- **Gestão de Ficheiros:** Corrigido um problema em que o envio de ficheiros com nomes não ingleses falhava.
- **Otimização de Prompts:** Melhorada a lógica de Tradução e estruturados os resultados de Vision.

## Alterações na versão 2.9

- **Adicionadas traduções em Francês e Turco.**
- **Vista Formatada:** Adicionado um botão "Ver Formatado" nos diálogos de chat para visualizar a conversa com formatação adequada (Cabeçalhos, Negrito, Código) numa janela padrão navegável.
- **Definição Markdown:** Adicionada uma nova opção "Limpar Markdown no Chat" nas Definições. Ao desmarcar esta opção, os utilizadores podem ver a sintaxe Markdown bruta (por exemplo, `**`, `#`) na janela de chat.
- **Gestão de Diálogos:** Corrigido um problema em que as janelas "Refinar Texto" ou de chat abriam várias vezes ou não recebiam foco corretamente.
- **Melhorias de UX:** Padronizados os títulos dos diálogos de ficheiros para "Abrir" e removidos anúncios de voz redundantes (por exemplo, "A abrir menu...") para uma experiência mais fluida.

## Alterações na versão 2.8

- Adicionada tradução em Italiano.
- **Relatório de Estado:** Adicionado um novo comando (NVDA+Control+Shift+I) para anunciar o estado atual do complemento (por exemplo, "A enviar...", "A analisar...").
- **Exportação HTML:** O botão "Guardar Conteúdo" nos diálogos de resultados guarda agora a saída como ficheiro HTML formatado, preservando estilos como cabeçalhos e texto a negrito.
- **Interface de Definições:** Melhorado o esquema do painel de Definições com agrupamento acessível.
- **Novos Modelos:** Adicionado suporte para gemini-flash-latest e gemini-flash-lite-latest.
- **Idiomas:** Adicionado Nepalês aos idiomas suportados.
- **Lógica do Menu Refinar:** Corrigido um erro crítico em que os comandos "Refinar Texto" falhavam se o idioma da interface do NVDA não fosse Inglês.
- **Ditado:** Melhorada a deteção de silêncio para evitar saída de texto incorreta quando não há entrada de voz.
- **Definições de Atualização:** "Verificar atualizações ao iniciar" está agora desativado por predefinição para cumprir as políticas da Loja de Complementos.
- Limpeza de Código.

## Alterações na versão 2.7

- Migrada a estrutura do projeto para o modelo oficial de Complementos NV Access para melhor conformidade com os padrões.
- Implementada lógica de repetição automática para erros HTTP 429 (Limite de Taxa) para garantir fiabilidade durante picos de tráfego.
- Otimizados prompts de tradução para maior precisão e melhor gestão da lógica "Smart Swap".
- Atualizada a tradução Russa.

## Alterações na versão 2.6

- Adicionado suporte à tradução Russa (Obrigado a nvda-ru).
- Atualizadas mensagens de erro para fornecer feedback mais descritivo sobre conectividade.
- Alterado o idioma de destino predefinido para Inglês.

## Alterações na versão 2.5

- Adicionado Comando Nativo de OCR de Ficheiro (NVDA+Control+Shift+F).
- Adicionado botão "Guardar Chat" aos diálogos de resultados.
- Implementado suporte completo de localização (i18n).
- Migrado feedback de áudio para o módulo nativo de tons do NVDA.
- Alterado para a API de Ficheiros Gemini para melhor gestão de ficheiros PDF e áudio.
- Corrigido bloqueio ao traduzir texto contendo chavetas.

## Alterações na versão 2.1.1

- Corrigido um problema em que a variável [file_ocr] não funcionava corretamente dentro de Prompts Personalizados.

## Alterações na versão 2.1

- Padronizados todos os atalhos para utilizar NVDA+Control+Shift para eliminar conflitos com o esquema Portátil do NVDA e atalhos do sistema.

## Alterações na versão 2.0

- Implementado sistema integrado de Atualização Automática.
- Adicionada Cache Inteligente de Tradução para recuperação instantânea de texto previamente traduzido.
- Adicionada Memória de Conversa para refinar resultados contextualmente nos diálogos de chat.
- Adicionado comando dedicado de Tradução da Área de Transferência (NVDA+Control+Shift+Y).
- Otimizados prompts de IA para impor estritamente a saída no idioma de destino.
- Corrigido bloqueio causado por caracteres especiais no texto de entrada.

## Alterações na versão 1.5

- Adicionado suporte para mais de 20 novos idiomas.
- Implementado Diálogo Interativo de Refinamento para perguntas de seguimento.
- Adicionada funcionalidade nativa de Ditado Inteligente.
- Adicionada categoria "Vision Assistant" ao diálogo Gestos de Entrada do NVDA.
- Corrigidos bloqueios COMError em aplicações específicas como Firefox e Word.
- Adicionado mecanismo de repetição automática para erros de servidor.

## Alterações na versão 1.0

- Lançamento inicial.
