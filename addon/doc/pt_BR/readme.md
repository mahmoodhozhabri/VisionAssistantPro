# Documentação do Vision Assistant Pro

**Vision Assistant Pro** é um assistente de IA avançado e multimodal para NVDA. Ele utiliza mecanismos de IA de classe mundial para fornecer leitura de tela inteligente, tradução, ditado por voz e análise de documentos.

_Este complemento foi lançado para a comunidade em homenagem ao Dia Internacional das Pessoas com Deficiência._

## 1. Configuração e Ajustes

Vá para **Menu do NVDA > Preferências > Configurações > Vision Assistant Pro**.

### 1.1 Configurações de Conexão

- **Provedor:** Selecione seu serviço de IA preferido. Os provedores suportados incluem **Google Gemini**, **OpenAI**, **Mistral**, **Groq** e **Personalizado** (servidores compatíveis com OpenAI como Ollama/LM Studio).
- **Nota Importante:** Recomendamos fortemente o uso do **Google Gemini** para melhor desempenho e precisão (especialmente para análise de imagens/arquivos).
- **Chave de API:** Obrigatória. Você pode inserir várias chaves (separadas por vírgulas ou novas linhas) para rotação automática.
- **Buscar Modelos:** Após inserir sua chave de API, pressione este botão para baixar a lista mais recente de modelos disponíveis do provedor.
- **Modelo de IA:** Selecione o modelo principal usado para chat e análise geral.

### 1.2 Roteamento Avançado de Modelos (Provedores Nativos)

_Disponível para Gemini, OpenAI, Groq e Mistral._

> **⚠️ Aviso:** Estas configurações destinam-se apenas a **usuários avançados**. Se você não tiver certeza sobre o que um modelo específico faz, deixe esta opção **desmarcada**. Selecionar um modelo incompatível para uma tarefa (por exemplo, um modelo apenas de texto para Vision) causará erros e impedirá o funcionamento do complemento.

Marque **"Roteamento Avançado de Modelos (Específico por Tarefa)"** para desbloquear controle detalhado. Isso permite selecionar modelos específicos na lista suspensa para diferentes tarefas:

- **Modelo de OCR / Visão:** Escolha um modelo especializado para analisar imagens.
- **Speech-to-Text (STT):** Escolha um modelo específico para ditado.
- **Text-to-Speech (TTS):** Escolha um modelo para gerar áudio.
  _Observação: Recursos não suportados (por exemplo, TTS para Groq) serão ocultados automaticamente._

### 1.3 Configuração Avançada de Endpoint (Provedor Personalizado)

_Disponível apenas quando "Personalizado" estiver selecionado._

> **⚠️ Aviso:** Esta seção permite configuração manual da API e foi projetada para **usuários avançados** que executam servidores locais ou proxies. URLs ou nomes de modelo incorretos interromperão a conectividade. Se você não souber exatamente o que são esses endpoints, mantenha esta opção **desmarcada**.

Marque **"Configuração Avançada de Endpoint"** para inserir manualmente os detalhes do servidor. Diferentemente dos provedores nativos, aqui você deve **digitar** as URLs e os Nomes de Modelo específicos:

- **URL da Lista de Modelos:** Endpoint para buscar os modelos disponíveis.
- **URL do Endpoint OCR/STT/TTS:** URLs completas para serviços específicos (por exemplo, `http://localhost:11434/v1/audio/speech`).
- **Modelos Personalizados:** Digite manualmente o nome do modelo (por exemplo, `llama3:8b`) para cada tarefa.

### 1.4 Preferências Gerais

- **Mecanismo de OCR:** Escolha entre **Chrome (Rápido)** para resultados rápidos ou **Gemini (Formatado)** para melhor preservação de layout.
  - _Observação:_ Se você selecionar "Gemini (Formatado)", mas seu provedor estiver definido como OpenAI/Groq, o complemento direcionará inteligentemente a imagem para o modelo de visão do provedor ativo.
- **Voz TTS:** Selecione seu estilo de voz preferido. Esta lista é atualizada dinamicamente com base no seu provedor ativo.
- **Criatividade (Temperatura):** Controla a aleatoriedade da IA. Valores mais baixos são melhores para tradução/OCR precisos.
- **URL de Proxy:** Configure se os serviços de IA forem restritos em sua região (suporta proxies locais como `127.0.0.1` ou URLs de ponte).

## 2. Camada de Comando e Atalhos

Para evitar conflitos de teclado, este complemento usa uma **Camada de Comando**.

1. Pressione **NVDA + Shift + V** (Tecla Mestra) para ativar a camada (você ouvirá um sinal sonoro).
2. Solte as teclas e, em seguida, pressione uma das seguintes teclas únicas:

| Tecla         | Função                            | Descrição                                                                                |
| ------------- | --------------------------------- | ---------------------------------------------------------------------------------------- |
| **T**         | Tradutor Inteligente              | Traduz o texto sob o cursor do navegador ou seleção.                                     |
| **Shift + T** | Tradutor da Área de Transferência | Traduz o conteúdo atualmente na área de transferência.                                   |
| **R**         | Refinador de Texto                | Resume, Corrige Gramática, Explica ou executa **Prompts Personalizados**.                |
| **V**         | Visão do Objeto                   | Descreve o objeto atual do navegador.                                                    |
| **O**         | Visão de Tela Inteira             | Analisa todo o layout e conteúdo da tela.                                                |
| **Shift + V** | Análise de Vídeo Online           | Analisa vídeos do **YouTube**, **Instagram**, **TikTok** ou **Twitter (X)**.             |
| **D**         | Leitor de Documentos              | Leitor avançado para PDF e imagens com seleção de intervalo de páginas.                  |
| **F**         | OCR de Arquivo                    | Reconhecimento direto de texto de arquivos de imagem, PDF ou TIFF selecionados.          |
| **A**         | Transcrição de Áudio              | Transcreve arquivos MP3, WAV ou OGG em texto.                                            |
| **C**         | Solucionador de CAPTCHA           | Captura e resolve CAPTCHAs (suporta portais governamentais).                             |
| **S**         | Ditado Inteligente                | Converte fala em texto. Pressione para iniciar a gravação, novamente para parar/digitar. |
| **L**         | Relatório de Status               | Anuncia o progresso atual (por exemplo, "Escaneando...", "Inativo").                     |
| **U**         | Verificar Atualização             | Verifica manualmente no GitHub a versão mais recente do complemento.                     |
| **Espaço**    | Recuperar Último Resultado        | Mostra a última resposta da IA em uma janela de chat para revisão ou acompanhamento.     |
| **H**         | Ajuda de Comandos                 | Exibe uma lista de todos os atalhos disponíveis na camada de comando.                    |

### 2.1 Atalhos do Leitor de Documentos (Dentro do Visualizador)

- **Ctrl + PageDown:** Ir para a próxima página.
- **Ctrl + PageUp:** Ir para a página anterior.
- **Alt + A:** Abrir uma janela de chat para fazer perguntas sobre o documento.
- **Alt + R:** Forçar uma **Nova varredura com IA** usando seu provedor ativo.
- **Alt + G:** Gerar e salvar um arquivo de áudio de alta qualidade (WAV/MP3). _Oculto se o provedor não suportar TTS._
- **Alt + S / Ctrl + S:** Salvar o texto extraído como arquivo TXT ou HTML.

## 3. Prompts Personalizados e Variáveis

Você pode gerenciar prompts em **Configurações > Prompts > Gerenciar Prompts...**.

### Variáveis Suportadas

- `[selection]`: Texto atualmente selecionado.
- `[clipboard]`: Conteúdo da área de transferência.
- `[screen_obj]`: Captura de tela do objeto do navegador.
- `[screen_full]`: Captura de tela completa.
- `[file_ocr]`: Selecionar arquivo de imagem/PDF para extração de texto.
- `[file_read]`: Selecionar documento para leitura (TXT, Código, PDF).
- `[file_audio]`: Selecionar arquivo de áudio para análise (MP3, WAV, OGG).

---

**Observação:** Uma conexão ativa com a internet é necessária para todos os recursos de IA. Documentos com várias páginas são processados automaticamente.

## 4. Suporte e Comunidade

Mantenha-se atualizado com as últimas notícias, recursos e lançamentos:

- **Canal no Telegram:** [t.me/VisionAssistantPro](https://t.me/VisionAssistantPro)
- **Issues no GitHub:** Para relatórios de bugs e solicitações de recursos.

---

## Alterações na versão 5.0

- **Arquitetura Multi-Provedor**: Adicionado suporte completo para **OpenAI**, **Groq** e **Mistral** junto com Google Gemini. Os usuários agora podem escolher seu backend de IA preferido.
- **Roteamento Avançado de Modelos**: Usuários de provedores nativos (Gemini, OpenAI, etc.) agora podem selecionar modelos específicos em uma lista suspensa para diferentes tarefas (OCR, STT, TTS).
- **Configuração Avançada de Endpoint**: Usuários do provedor personalizado podem inserir manualmente URLs específicas e nomes de modelo para controle granular sobre servidores locais ou de terceiros.
- **Visibilidade Inteligente de Recursos**: O menu de configurações e a interface do Leitor de Documentos agora ocultam automaticamente recursos não suportados (como TTS) com base no provedor selecionado.
- **Busca Dinâmica de Modelos**: O complemento agora obtém a lista de modelos disponíveis diretamente da API do provedor, garantindo compatibilidade com novos modelos assim que forem lançados.
- **OCR e Tradução Híbridos**: Otimizou a lógica para usar o Google Tradutor por velocidade ao usar OCR do Chrome e tradução com IA ao usar mecanismos Gemini/Groq/OpenAI.
- **"Nova varredura com IA" Universal**: O recurso de nova varredura do Leitor de Documentos não está mais limitado ao Gemini. Agora utiliza qualquer provedor de IA atualmente ativo para reprocessar páginas.

## Alterações na versão 4.6

- **Recuperação Interativa de Resultados:** Adicionada a tecla **Espaço** à camada de comando, permitindo que os usuários reabram instantaneamente a última resposta da IA em uma janela de chat para perguntas de acompanhamento, mesmo quando o modo "Saída Direta" está ativo.
- **Hub da Comunidade no Telegram:** Adicionado um link para o "Canal Oficial no Telegram" no menu Ferramentas do NVDA, oferecendo uma maneira rápida de se manter atualizado com as últimas notícias, recursos e lançamentos.
- **Estabilidade Aprimorada de Respostas:** Otimizada a lógica principal para recursos de Tradução, OCR e Visão para garantir desempenho mais confiável e uma experiência mais fluida ao usar saída direta por voz.
- **Melhoria na Orientação da Interface:** Atualizadas as descrições das configurações e a documentação para explicar melhor o novo sistema de recuperação e como ele funciona junto com as configurações de saída direta.

## Alterações na versão 4.5

- **Gerenciador Avançado de Prompts:** Introduzida uma caixa de diálogo dedicada nas configurações para personalizar prompts de sistema padrão e gerenciar prompts definidos pelo usuário com suporte completo para adicionar, editar, reordenar e visualizar.
- **Suporte Abrangente a Proxy:** Resolvidos problemas de conectividade de rede garantindo que as configurações de proxy definidas pelo usuário sejam estritamente aplicadas a todas as solicitações de API, incluindo tradução, OCR e geração de fala.
- **Migração Automática de Dados:** Integrado um sistema inteligente de migração para atualizar automaticamente configurações legadas de prompts para um formato JSON v2 robusto na primeira execução sem perda de dados.
- **Compatibilidade Atualizada (2025.1):** Definida a versão mínima exigida do NVDA como 2025.1 devido a dependências de biblioteca em recursos avançados como o Leitor de Documentos, garantindo desempenho estável.
- **Interface de Configurações Otimizada:** Simplificada a interface de configurações reorganizando o gerenciamento de prompts em uma caixa de diálogo separada, proporcionando uma experiência de usuário mais limpa e acessível.
- **Guia de Variáveis de Prompt:** Adicionado um guia integrado nas caixas de diálogo de prompt para ajudar os usuários a identificar e usar facilmente variáveis dinâmicas como [selection], [clipboard] e [screen_obj].

## Alterações na versão 4.0.3

- **Maior Resiliência de Rede:** Adicionado um mecanismo automático de repetição para lidar melhor com conexões de internet instáveis e erros temporários do servidor, garantindo respostas de IA mais confiáveis.
- **Janela Visual de Tradução:** Introduzida uma janela dedicada para resultados de tradução. Agora os usuários podem navegar e ler traduções longas linha por linha, semelhante aos resultados de OCR.
- **Visualização Formatada Agregada:** O recurso "Visualizar Formatado" no Leitor de Documentos agora exibe todas as páginas processadas em uma única janela organizada com cabeçalhos de página claros.
- **Fluxo de Trabalho de OCR Otimizado:** Ignora automaticamente a seleção de intervalo de páginas para documentos de uma única página, tornando o processo de reconhecimento mais rápido e contínuo.
- **Estabilidade de API Aprimorada:** Alterado para um método de autenticação baseado em cabeçalho mais robusto, resolvendo possíveis erros de "All API Keys failed" causados por conflitos de rotação de chaves.
- **Correções de Bugs:** Resolvidos vários possíveis travamentos, incluindo um problema durante o encerramento do complemento e um erro de foco na janela de chat.

## Alterações na versão 4.0.1

- **Leitor de Documentos Avançado:** Um novo e poderoso visualizador para PDF e imagens com seleção de intervalo de páginas, processamento em segundo plano e navegação contínua `Ctrl+PageUp/Down`.
- **Novo Submenu Ferramentas:** Adicionado um submenu dedicado "Vision Assistant" no menu Ferramentas do NVDA para acesso mais rápido aos principais recursos, configurações e documentação.
- **Personalização Flexível:** Agora você pode escolher seu mecanismo de OCR e voz TTS preferidos diretamente no painel de configurações.
- **Suporte a Múltiplas Chaves de API:** Adicionado suporte para múltiplas chaves de API do Gemini. Você pode inserir uma chave por linha ou separá-las com vírgulas nas configurações.
- **Mecanismo Alternativo de OCR:** Introduzido um novo mecanismo de OCR para garantir reconhecimento de texto confiável mesmo ao atingir limites de cota da API do Gemini.
- **Rotação Inteligente de Chaves de API:** Alterna automaticamente e memoriza a chave de API funcional mais rápida para contornar limites de cota.
- **Documento para MP3/WAV:** Integrada a capacidade de gerar e salvar arquivos de áudio de alta qualidade nos formatos MP3 (128kbps) e WAV diretamente no leitor.
- **Suporte a Stories do Instagram:** Adicionada a capacidade de descrever e analisar Stories do Instagram usando suas URLs.
- **Suporte ao TikTok:** Introduzido suporte para vídeos do TikTok, permitindo descrição visual completa e transcrição de áudio dos clipes.
- **Janela de Atualização Redesenhada:** Apresenta uma nova interface acessível com uma caixa de texto rolável para ler claramente as alterações da versão antes de instalar.
- **Status e UX Unificados:** Padronizou as caixas de diálogo de arquivos em todo o complemento e aprimorou o comando 'L' para relatar progresso em tempo real.

## Alterações na versão 3.6.0

- **Sistema de Ajuda:** Adicionado um comando de ajuda (`H`) dentro da Camada de Comando para fornecer uma lista de todos os atalhos e suas funções de fácil acesso.
- **Análise de Vídeo Online:** Suporte expandido para incluir vídeos do **Twitter (X)**. Também melhorou a detecção de URL e a estabilidade para uma experiência mais confiável.
- **Contribuição para o Projeto:** Adicionada uma caixa de diálogo opcional de doação para usuários que desejam apoiar futuras atualizações e crescimento contínuo do projeto.

## Alterações na versão 3.5.0

\* \*\*Camada de Comando:\*\* Introduzido um sistema de Camada de Comando (padrão: `NVDA+Shift+V`) para agrupar atalhos sob uma única tecla mestra. Por exemplo, em vez de pressionar `NVDA+Control+Shift+T` para tradução, agora você pressiona `NVDA+Shift+V` seguido de `T`. \* \*\*Análise de Vídeo Online:\*\* Adicionado um novo recurso para analisar vídeos do YouTube e Instagram diretamente fornecendo uma URL.

## Alterações na versão 3.1.0

- **Modo de Saída Direta:** Adicionada uma opção para ignorar a janela de chat e ouvir as respostas da IA diretamente por voz para uma experiência mais rápida e contínua.
- **Integração com Área de Transferência:** Adicionada uma nova configuração para copiar automaticamente as respostas da IA para a área de transferência.

## Alterações na versão 3.0

- **Novos Idiomas:** Adicionadas traduções em **Persa** e **Vietnamita**.
- **Modelos de IA Expandidos:** Reorganizada a lista de seleção de modelos com prefixos claros (`[Free]`, `[Pro]`, `[Auto]`) para ajudar os usuários a distinguir entre modelos gratuitos e limitados por taxa (pagos). Adicionado suporte para **Gemini 3.0 Pro** e **Gemini 2.0 Flash Lite**.
- **Estabilidade do Ditado:** Melhorada significativamente a estabilidade do Ditado Inteligente. Adicionada uma verificação de segurança para ignorar clipes de áudio com menos de 1 segundo, evitando alucinações da IA e erros vazios.
- **Manipulação de Arquivos:** Corrigido um problema em que o envio de arquivos com nomes não ingleses falhava.
- **Otimização de Prompts:** Melhorada a lógica de Tradução e estruturados os resultados de Visão.

## Alterações na versão 2.9

- **Adicionadas traduções em Francês e Turco.**
- **Visualização Formatada:** Adicionado um botão "Visualizar Formatado" nas janelas de chat para visualizar a conversa com estilo adequado (Títulos, Negrito, Código) em uma janela padrão navegável.
- **Configuração de Markdown:** Adicionada uma nova opção "Limpar Markdown no Chat" nas Configurações. Desmarcar isso permite que os usuários vejam a sintaxe Markdown bruta (por exemplo, `**`, `#`) na janela de chat.
- **Gerenciamento de Janelas:** Corrigido um problema em que as janelas "Refinar Texto" ou de chat abriam várias vezes ou não focavam corretamente.
- **Melhorias de UX:** Padronizados os títulos das caixas de diálogo de arquivo para "Abrir" e removidos anúncios de fala redundantes (por exemplo, "Abrindo menu...") para uma experiência mais fluida.

## Alterações na versão 2.8

- Adicionada tradução para Italiano.
- **Relatório de Status:** Adicionado um novo comando (NVDA+Control+Shift+I) para anunciar o status atual do complemento (por exemplo, "Enviando...", "Analisando...").
- **Exportação em HTML:** O botão "Salvar Conteúdo" nas janelas de resultados agora salva a saída como um arquivo HTML formatado, preservando estilos como títulos e texto em negrito.
- **Interface de Configurações:** Melhorado o layout do painel de Configurações com agrupamento acessível.
- **Novos Modelos:** Adicionado suporte para gemini-flash-latest e gemini-flash-lite-latest.
- **Idiomas:** Adicionado Nepali aos idiomas suportados.
- **Lógica do Menu Refinar:** Corrigido um bug crítico em que os comandos "Refinar Texto" falhavam se o idioma da interface do NVDA não fosse Inglês.
- **Ditado:** Melhorada a detecção de silêncio para evitar saída incorreta de texto quando nenhuma fala é inserida.
- **Configurações de Atualização:** "Verificar atualizações na inicialização" agora está desativado por padrão para cumprir as políticas da Loja de Complementos.
- Limpeza de código.

## Alterações na versão 2.7

- Estrutura do projeto migrada para o Modelo Oficial de Complemento da NV Access para melhor conformidade com padrões.
- Implementada lógica automática de repetição para erros HTTP 429 (Limite de Taxa) para garantir confiabilidade durante alto tráfego.
- Otimizados prompts de tradução para maior precisão e melhor tratamento da lógica "Smart Swap".
- Atualizada tradução em Russo.

## Alterações na versão 2.6

- Adicionado suporte à tradução em Russo (Obrigado ao nvda-ru).
- Atualizadas mensagens de erro para fornecer feedback mais descritivo sobre conectividade.
- Alterado o idioma de destino padrão para Inglês.

## Alterações na versão 2.5

- Adicionado Comando Nativo de OCR de Arquivo (NVDA+Control+Shift+F).
- Adicionado botão "Salvar Chat" nas janelas de resultados.
- Implementado suporte completo à localização (i18n).
- Migrado feedback de áudio para o módulo nativo de tons do NVDA.
- Alterado para Gemini File API para melhor manipulação de arquivos PDF e de áudio.
- Corrigido travamento ao traduzir texto contendo chaves `{}`.

## Alterações na versão 2.1.1

- Corrigido um problema em que a variável [file_ocr] não funcionava corretamente dentro de Prompts Personalizados.

## Alterações na versão 2.1

- Padronizados todos os atalhos para usar NVDA+Control+Shift para eliminar conflitos com o layout Laptop do NVDA e atalhos do sistema.

## Alterações na versão 2.0

- Implementado sistema integrado de Atualização Automática.
- Adicionado Cache Inteligente de Tradução para recuperação instantânea de texto previamente traduzido.
- Adicionada Memória de Conversa para refinar resultados contextualmente nas janelas de chat.
- Adicionado comando dedicado de Tradução da Área de Transferência (NVDA+Control+Shift+Y).
- Otimizados prompts de IA para impor estritamente a saída no idioma de destino.
- Corrigido travamento causado por caracteres especiais no texto de entrada.

## Alterações na versão 1.5

- Adicionado suporte para mais de 20 novos idiomas.
- Implementado Diálogo Interativo de Refinamento para perguntas de acompanhamento.
- Adicionado recurso nativo de Ditado Inteligente.
- Adicionada categoria "Vision Assistant" na janela de Gestos de Entrada do NVDA.
- Corrigidos travamentos COMError em aplicativos específicos como Firefox e Word.
- Adicionado mecanismo automático de repetição para erros do servidor.

## Alterações na versão 1.0

- Lançamento inicial.
