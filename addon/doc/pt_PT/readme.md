# Documentação do Vision Assistant Pro

<!-- DOWNLOAD_COUNT_START --> Total Downloads: 62,863 <!-- DOWNLOAD_COUNT_END -->

O **Vision Assistant Pro** é um assistente de IA multimodal avançado para o NVDA. Utiliza motores de IA de classe mundial para oferecer leitura de ecrã inteligente, tradução, ditado por voz e análise de documentos.

_Este extra foi disponibilizado à comunidade em homenagem ao Dia Internacional das Pessoas com Deficiência._

## 1. Configuração e Instalação

Vá a **Menu NVDA > Preferências > Definições > Vision Assistant Pro**. A janela de diálogo de definições está organizada em 9 separadores acessíveis: **Conexão**, **Assistente Live**, **Comportamento da IA**, **Idiomas de Tradução**, **Leitor de Documentos**, **Vídeo**, **CAPTCHA**, **Instruções** e **Avançado**.

### 1.1 Separador de Conexão

- **Provedor:** Selecione o seu serviço de IA preferido. Os provedores suportados incluem **Google Gemini**, **OpenAI**, **Mistral**, **Groq**, **MiniMax** e **Personalizado** (servidores compatíveis com OpenAI como Ollama, LM Studio, Jan.ai ou KoboldCPP).
- **Chave da API:** Introduza uma ou várias chaves de API (separadas por vírgulas ou quebras de linha) para rotação automática.
- **Obter Modelos:** Prima este botão após introduzir a sua chave de API para transferir a lista de modelos mais recente disponível no provedor.
- **Modelo de IA:** Selecione o modelo principal utilizado para conversação geral e análise.
- **Advanced Model Routing (Task-specific):** Optionally select dedicated models from dropdowns for OCR, STT, TTS, AI Operator, Video, and Live Assistant tasks. For Gemini, models are dynamically categorized by capability without clutter.
- **Definições de Provedor Personalizado:** Configure pontos de extremidade (endpoints) locais ou personalizados. Inclui **Configurar IA Local** (configuração com um clique para Ollama, LM Studio, Jan.ai ou KoboldCPP) e **Configuração Avançada de Endpoint**.
- **Proxy Configuration:** Full support for tunneling and endpoint redirection across the entire add-on (including the Live Assistant, Ambient Observer, and TTS). Enter your **Proxy URL** and select your **Proxy Mode**:
  - **Auto-detect:** Automatically detects whether the URL is a forward proxy or reverse proxy.
  - **SOCKS5 Proxy:** Forces forward tunneling via SOCKS5 with RFC 1929 username/password authentication and domain name resolution.
  - **HTTP Proxy:** Forces forward tunneling via an HTTP proxy with Basic authentication.
  - **Reverse Proxy:** Direct endpoint replacement for custom AI gateways and self-hosted mirrors (credentials are disabled in this mode).
- **Test Proxy Connection:** A non-blocking button that tests connectivity and measures server latency in milliseconds (spoken via NVDA).
- **Opções de Conexão e Saída:** Configure o URL do Proxy, a verificação de atualizações ao iniciar, o Markdown Limpo no Chat, Copiar respostas da IA para a área de transferência e a Saída Direta (Sem Janela de Chat).
- **Guardar Histórico de Conversas:** Mantenha as suas conversas na lista de Histórico.

### 1.2 Separador Assistente Live

- **Assistente em Direto: Saída Direta (Sem Janela):** Iniciar o Assistente em Direto sem a sua janela de conversação; abra-a mais tarde com a tecla Relembrar Último Resultado (`Espaço`).
- **Premir para Falar:** Ativar ou desativar o modo premir para falar. Quando ativado, o seu microfone apenas envia áudio enquanto mantiver a tecla atribuída premida.
- **Tecla Premir para Falar:** Prima as teclas para gravar o atalho (por exemplo, `F12` ou `Ctrl+F12`) — pode até atribuir um modificador isolado como `Ctrl Esquerdo`. Mantenha a tecla premida para falar e solte-a para terminar; um sinal sonoro curto confirma cada clique e libertação.

Nota: Este separador só aparece quando o **Google Gemini** (ou um fornecedor personalizado compatível com o Gemini) é o seu fornecedor ativo.

### 1.3 Separador de Comportamento de IA

- **Criatividade (Temperatura):** Controla a aleatoriedade e criatividade da IA (de 0,0 a 2,0). Valores mais baixos produzem resultados de tradução e OCR mais determinísticos e precisos.

### 1.4 Separador de Idiomas de Tradução

- **Idioma de Origem:** Selecione o seu idioma de entrada predefinido.
- **Idioma de Destino:** Selecione o seu idioma principal de tradução.
- **Idioma de Resposta da IA:** Selecione o idioma para as respostas gerais da IA.
- **Troca Inteligente:** Troca automaticamente os idiomas de origem e destino com base no texto detetado.

### 1.5 Separador do Leitor de Documentos

- **Motor de OCR:** Escolha entre **Chrome (Rápido)** para resultados rápidos ou **IA (Avançado)** para uma preservação superior da estrutura da página.
- **Tamanho do Lote do OCR:** Especifique o número de páginas por pedido (defina como 0 para processamento num único pedido).
- **Descrever Imagens Inline:** Ative ou desative descrições de imagens no próprio texto durante a extração de documentos.
- **Exportar Números de Página:** Ative ou desative os números de página e separadores na saída de documentos com várias páginas.
- **Voz TTS:** Selecione o estilo de voz predefinido para a geração de áudio.
- **Guardar Documentos no Histórico:** Mantenha os documentos abertos na lista de Histórico; os textos de OCR em cache e os dados de retoma do documento continuam a ser guardados.

### 1.6 Separador de Vídeo

- **Tamanho do Bloco de Vídeo:** Duração dos segmentos em minutos para a geração de Audiodescrição (defina como 0 para processar o ficheiro inteiro).
- **Adicionar Lista de Personagens:** Opção para adicionar um dicionário de personagens como a primeira entrada das legendas.
- **Adicionar Aviso de IA:** Opção para inserir um aviso de responsabilidade sobre IA no início das legendas SRT do vídeo.
- **Dicionário de Personagens e Gestão de Séries:** Adicione, edite, importe ou gira nomes de personagens, descrições físicas e papéis por série — a IA associa automaticamente os personagens detetados ao seu dicionário e une os novos à medida que analisa mais episódios. As suas notas manuais são sempre preservadas com prioridade sobre as atualizações da IA, enquanto as descrições físicas se mantêm atualizadas ao longo dos episódios.

### 1.7 Separador CAPTCHA

- **Ativar Resolução Visual de CAPTCHA:** Ative ou desative a resolução automática de desafios visuais (hCaptcha, reCAPTCHA).
- **Método de CAPTCHA de Texto:** Escolha entre capturar o **Objeto do Navegador** ou o **Ecrã Inteiro**.

### 1.8 Separador de Prompts

- **Gerir Prompts:** Abre uma janela dedicada para personalizar as prompts predefinidas do sistema ou criar, editar, reordenar e pré-visualizar prompts personalizadas do utilizador com variáveis dinâmicas (ex.: `[selection]`, `[screen_fg_obj]`).
- **Atalhos para Comandos Personalizados:** Atribua um atalho de teclado dedicado a qualquer comando personalizado diretamente no Gestor de Comandos. Prima as teclas para os gravar — teclas individuais funcionam dentro da Camada de Comandos (e globalmente como `NVDA + Shift + tecla`), enquanto combinações como `Control + Shift + 1` funcionam globalmente por si só.
- **Per-Prompt Feedback Behavior:** Choose how each prompt outputs its result individually (Global setting, Copy to clipboard, Direct Output / NVDA message, Copy to clipboard + Direct Output, or Chat window).

### 1.9 Separador Avançado e Registo Global

Aceda ao separador **Avançado** para configurar o registo de eventos (logging) global do extra:

- **Ativar ficheiro de registo dedicado:** Ative ou desative o registo de todos os eventos operacionais, tráfego da API e erros de todos os módulos do extra num ficheiro separado (`vision_assistant.log`).
- **Nível de Registo:** Selecione o nível de detalhe entre **Depuração (Todos os Detalhes)**, **Informação (Informação Geral)**, **Aviso (Apenas Avisos)** e **Erro (Apenas Erros)**.
- **Manter Registos Durante:** Defina períodos de retenção automática para eliminar registos mais antigos (de 1 hora a 90 dias).
- **Controlos de Gestão de Registos:** Utilize **Abrir Ficheiro de Registo**, **Abrir Pasta de Registos** ou **Limpar Ficheiro de Registo** para inspecionar ou apagar dados de registo diretamente sem reiniciar o NVDA ou interferir com os registos padrão do NVDA.
- **Diretório de Dados Unificado:** Todos os ficheiros de dados do add-on (histórico, séries, etiquetas, progresso de OCR, caches e registos) são guardados numa única pasta `VisionAssistant` dentro do seu diretório de configuração do NVDA — mantendo tudo organizado e tornando as cópias de segurança manuais extremamente simples.

### 1.10 Cópia de Segurança e Restauração de Definições

O separador **Avançado** também inclui uma secção de **Cópia de Segurança e Restauração**:

- **Cópia de segurança:** Guarda a sua configuração num único ficheiro JSON. Ao clicar, pode escolher o que incluir: **Tudo** (definições, etiquetas personalizadas, progresso de OCR e histórico) ou **Apenas Definições**.
- **Restaurar:** Carrega uma cópia de segurança guardada anteriormente para restaurar a sua configuração e dados a qualquer momento, em qualquer computador ou após reinstalar o NVDA. Ser-lhe-á pedida confirmação primeiro, pois a restauração substitui todas as suas definições e dados atuais.

## 2. Gestor de Chaves da API Gemini

Creating a Gemini API key on **aistudio.google.com** used to be the hardest step of the add-on. With a screen reader the pages were confusing, and some people simply could not create a key at all. The **Gemini API Key Manager** solves that problem. Press **G** in the Command Layer, or open **NVDA Menu > Preferences > Settings > Vision Assistant > Connection** and press **Get a Gemini API Key...**.

- **Signing in:** When you open the manager, your default browser opens directly with Google's secure sign-in page. Sign in with your Google account — no external tools, SDKs, or command-line setups are required. The account you are signed in with is always shown on the **Sign Out** button.
- **Creating a key:** After signing in, you can create a key immediately with **New Project and Key** without any prior setup. If you already have existing projects, they appear in a simple list where you can select one and press **Create Key for Selected Project**.
- **What happens next:** The new key is copied to the clipboard straight away, saved inside the add-on for later, and you are asked once whether to add it to the add-on's key list. That is all you need — no web pages to hunt through.
- **Working with your keys:** **Copy Key for Selected Project** copies the key of the project you have selected, **Copy Last Created Key** copies the key you created a moment ago, and **Export Saved Keys to CSV...** saves everything you have created to a file.
- **Deleting a key:** **Delete a Key...** shows the keys that exist on the selected project, asks you which one to remove, and confirms before deleting. Deleting a key also removes it from the add-on's key list, so no broken key is ever left in the rotation. Keys created outside the add-on can be deleted too, as long as your account has permission on that project.
- **Signing out:** **Sign Out** removes the stored sign-in information from your computer, so you can switch to another account whenever you like.

## 3. Camada de Comandos e Atalhos

Para evitar conflitos de teclado, este extra utiliza uma **Camada de Comandos**.

1. Prima **NVDA + Shift + V** (Tecla Mestra) para ativar a camada (ouvirá um sinal sonoro).
2. Largue as teclas e, em seguida, prima uma das seguintes teclas individuais:

| Tecla                  | Função                                 | Descrição                                                                                                                                                                                                                                                               |
| ---------------------- | -------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Shift + A**          | **Operador de IA**                     | **Operação Autónoma:** Indica à IA para realizar uma tarefa no seu ecrã. Pressionar novamente cancela instantaneamente as operações ativas.                                                                             |
| **E**                  | **Explorador de IU**                   | **Clique Interativo:** Identifica e clica em elementos da IU em qualquer aplicação.                                                                                                                                                     |
| **T**                  | Tradutor Inteligente                   | Traduz o texto sob o cursor do navegador ou a seleção.                                                                                                                                                                                                  |
| **Shift + T**          | Clipboard Translator                   | Traduz o conteúdo atualmente na área de transferência.                                                                                                                                                                                                  |
| **R**                  | Aperfeiçoador de Texto                 | Resume, corrige a gramática, explica ou executa **Prompts Personalizados**.                                                                                                                                                                             |
| **V**                  | Visão de Objetos                       | Descreve o objeto do navegador atual.                                                                                                                                                                                                                   |
| **O**                  | Full Screen Vision                     | Analisa o esquema e o conteúdo de todo o ecrã.                                                                                                                                                                                                          |
| **Shift + V**          | Análise de Vídeo                       | Analisa ficheiros de vídeo locais ou vídeos online do **YouTube**, **Instagram**, **TikTok** ou **Twitter (X)**.                                                                                                                     |
| **Control + V**        | Gravação de Vídeo Local                | Grava um vídeo silencioso do seu ecrã e analisa as ações e o esquema.                                                                                                                                                                                   |
| **D**                  | Leitor de Documentos                   | Leitor avançado para PDF, imagens e ficheiros de texto simples/HTML com seleção de intervalo de páginas.                                                                                                                                                |
| **F**                  | **Ação Inteligente em Ficheiros**      | Reconhecimento sensível ao contexto a partir de imagens, PDFs ou ficheiros TIFF selecionados.                                                                                                                                                           |
| **M**                  | Transcrição e Dobragem de Média        | Transcreve ou dobra ficheiros de áudio/vídeo (MP3, WAV, MP4, etc.) para o seu idioma de destino.                                                                                                                     |
| **C**                  | Resolvedor de CAPTCHA                  | Captura e resolve CAPTCHAs.                                                                                                                                                                                                                             |
| **Shift + C**          | Chat Direto                            | Abre uma interface de chat direta baseada em texto com a IA.                                                                                                                                                                                            |
| **S**                  | Ditado Inteligente                     | Converte voz em texto. Pressione para iniciar a gravação, novamente para parar/escrever.                                                                                                                                                |
| **Control+T**          | Tradução por Voz                       | Transcreve, traduz e escreve o resultado com base nas suas definições de idioma.                                                                                                                                                                        |
| **Control+L**          | **Assistente em Direto**               | **Copiloto em Tempo Real (apenas Gemini):** Inicia ou termina uma conversação de voz e ecrã em direto com o assistente de IA.                                                                                        |
| **Control+A**          | **Operador em Direto**                 | **Controlo Autónomo do Computador (apenas Gemini):** Inicia ou termina uma sessão de operador em direto para delegar ecrã e ações à IA.                                                                              |
| **G**                  | **Gestor de Chaves da API Gemini**     | **Crie a sua chave de API sem a web (apenas Gemini):** Abre o gestor que configura o que o seu computador precisa, abre o navegador para iniciar sessão e cria, copia ou elimina uma chave para o projeto escolhido. |
| **I**                  | Relatório de Estado                    | Anuncia o progresso atual (por exemplo, "A verificar...", "Inativo").                                                                                                                |
| **L**                  | **Etiquetar Objeto**                   | **Etiquetagem Semântica por IA:** Etiqueta permanentemente o objeto do navegador ou ícone atualmente focado.                                                                                                                            |
| **Shift + L**          | **Gerir/Verificar Etiquetas**          | Abre o Gestor de Etiquetas (se existirem) ou verifica a aplicação à procura de elementos não etiquetados.                                                                                                                            |
| **U**                  | Procurar Atualizações                  | Procura manualmente no GitHub a versão mais recente do extra.                                                                                                                                                                                           |
| **Espaço**             | Relembrar Último Resultado             | Mostra a última resposta da IA numa caixa de diálogo de conversação para revisão ou continuação.                                                                                                                                                        |
| **H**                  | Ajuda dos Comandos                     | Apresenta uma lista de todos os atalhos disponíveis.                                                                                                                                                                                                    |
| **Control + H**        | **Histórico**                          | Abre a caixa de diálogo do Histórico com a lista das suas conversações e documentos anteriores, com filtros e opções para eliminar/limpar.                                                                                                              |
| **Alt + S**            | Configurações                          | Abre a caixa de diálogo de configurações do Vision Assistant Pro.                                                                                                                                                                                       |
| **Alt + Q**            | Relatório de Chaves com Quota Esgotada | Informa o número de chaves da API Gemini que excederam a quota diária, os modelos afetados e o tempo de reposição.                                                                                                                                      |
| **Alt + M**            | Auditoria de Encaminhamento            | Informa os modelos de IA atualmente selecionados no encaminhamento avançado para tarefas especializadas (ignorando os padrões).                                                                                                      |
| **Cima / Baixo**       | Navegação pelas Definições Rápidas     | Navega entre as categorias de definições rápidas (Fornecedor, Modelo, Saída)... na camada.                                                                                           |
| **Esquerda / Direita** | Alterar Definição Rápida               | Altera o valor da definição rápida atualmente selecionada.                                                                                                                                                                                              |

## 4. Conversação e Histórico

As janelas de conversação e o diálogo de Histórico funcionam em todas as funcionalidades, permitindo-lhe rever conversas e retomar exatamente onde parou.

### 3.1 Atalhos da Janela de Conversação

Quando uma janela de conversação está aberta (Conversação Direta, conversação de documento, refinar e semelhantes), pode rever a conversa com:

- **Alt + Down:** Read the next message.
- **Alt + Up:** Ler a mensagem anterior.
- **Alt + C:** Copiar a mensagem atual.

### 3.2 Histórico (Control + H)

Prima **Control + H** na Camada de Comandos para abrir a caixa de diálogo do **Histórico** com as suas conversas e documentos anteriores, filtráveis por tipo (Tudo / Conversas / Documentos). Abra uma conversa para continuar o diálogo — incluindo os ficheiros anexados, que são reanexados automaticamente — ou abra um documento e continue a leitura. Prima **Delete** em qualquer item para o remover, ou **Limpar tudo** para esvaziar a lista. Para os documentos, a tecla Delete pergunta se pretende remover apenas a entrada do histórico ou também limpar o texto de OCR em cache desse documento, para que a próxima abertura volte a analisá-lo do zero — com a opção **Não voltar a perguntar** para memorizar a sua escolha.

Também pode escolher o que a lista memoriza. **Guardar histórico de conversas** (separador Conexão) e **Guardar documentos no histórico** (separador Leitor de Documentos) estão ambos ativados por predefinição, e ambos podem ser alternados nas Definições Rápidas. A opção de documento afeta apenas a entrada do Histórico — os textos de OCR em cache e os dados de retoma do documento são sempre mantidos.

## 5. Operador de IA - Controlo Autónomo do Computador

O **Operador de IA** transforma o Vision Assistant Pro num assistente ativo capaz de interagir com o seu computador em seu nome, deixando de ser um mero leitor passivo. Pode pedir-lhe para descrever o ecrã, responder a perguntas sobre o que vê ou até assumir o controlo — clicando em botões, arrastando itens, escrevendo texto e navegando pelas aplicações utilizando comandos em linguagem natural.

A maior vantagem? Funciona perfeitamente em software completamente inacessível. Se estiver preso numa aplicação personalizada, num ambiente de trabalho remoto ou num site onde o seu leitor de ecrã fica totalmente em silêncio, o operador não se importa. Como "vê" o ecrã visualmente, consegue encontrar, ler e interagir com elementos que não têm qualquer etiqueta de acessibilidade.

### 4.1 Como Funciona

1. Prima **NVDA + Shift + V** e, em seguida, prima **Shift + A** (ou utilize o atalho direto) para abrir a janela do Operador de IA.
2. Escreva o que pretende fazer em linguagem simples (ex.: "Clicar no botão Guardar", "O que diz a mensagem de erro?" ou "Mudar o nome do ficheiro para final.pdf").
3. A IA irá analisar o seu ecrã, identificar os elementos relevantes e executar a ação ou fornecer a resposta. Se uma tarefa exigir vários passos, o operador continuará a trabalhar até estar concluída.
4. Prima **Shift + A** novamente a qualquer momento para abortar instantaneamente uma operação em curso.

### 4.2 Ações Suportadas

O operador compreende uma grande variedade de comandos:

- **Descrever e Responder**: "Descreve a disposição do ecrã" ou "O que diz a mensagem de erro?"
- **Clicar**: "Clica no botão Guardar"
- **Clique Direito**: "Clica com o botão direito no ficheiro"
- **Duplo Clique**: "Dá duplo clique no documento"
- **Arrastar e Largar**: "Arrastar o documento para a pasta Arquivo"
- **Escrever**: "Escreve 'Olá Mundo' na caixa de pesquisa"
- **Rolar (Scroll)**: "Rolar para baixo três vezes"
- **Premir Tecla**: "Prima Enter", "Prima Tab", "Prima Escape"
- **Tarefas de Vários Passos**: "Abre o Explorador de Ficheiros, encontra o relatório e muda o nome para final.pdf"

### 4.3 Notas Importantes

- **⚠️ Aviso de Utilização da API**: Como o operador precisa de "ver" exatamente o que está a acontecer no ecrã, envia uma captura de ecrã em alta resolução a cada passo. A utilização frequente consumirá a sua quota de API muito mais rapidamente do que as funcionalidades de texto padrão.
- **Aplicações de Administrador**: Se o NVDA não estiver a ser executado com privilégios de Administrador, o operador poderá não conseguir interagir com janelas que exijam permissões elevadas. Esta é uma limitação de segurança do Windows e não um erro do extra.
- **Boas Práticas**: Para obter os melhores resultados, dê comandos claros e específicos. "Clica no botão azul Submeter no fundo do formulário" funcionará quase sempre melhor do que apenas "Clica no botão".

### 4.4 Operador em Direto (Control+A)

O Assistente em Direto transforma o Vision Assistant Pro num copiloto interativo em tempo real.
_(Nota: Esta funcionalidade é exclusiva do Google Gemini e de provedores Personalizados compatíveis com o Gemini)._

- **Activation:** Press **Control+A** in the Command Layer to start a live operator session; press it again to end it.
- **How it works:** Ask in plain language, for example "open Chrome and search for a website" or "rename this file to final". The operator looks at the screen, carries out the steps one by one, and keeps working through multi-step requests until the task is done.
- **Announcements:** Every step is spoken in the Live Assistant's own voice, and it tells you when the task is finished, or why it could not be done.
- **CAPTCHA:** If a CAPTCHA appears, the operator tries your built-in **CAPTCHA solver** first; if it cannot solve it, it asks you to complete the accessible challenge yourself.
- **Stopping:** Press **Stop operator action** in the Live Assistant window to cancel the current task.
- **Settings:** The operator's own instruction can be edited in the Prompt Manager (section **Live**, **Live Operator Instruction**). The **Live Direct Output (No Window)** switch is available in Quick Settings as well.

## 6. Análise de Vídeo e Audiodescrição

> **Nota:** As funcionalidades de Análise de Vídeo e Audiodescrição são executadas exclusivamente pelo provedor **Google Gemini**. Certifique-se de que o seu provedor ativo nas definições do extra está definido como Google Gemini.

O Vision Assistant Pro introduz capacidades potentes de processamento de vídeo concebidas especificamente para utilizadores cegos. Pode analisar tanto vídeos online como gravações de ecrã locais para fornecer descrições visuais altamente detalhadas e gerar guiões profissionais de Audiodescrição (SRT).

### 5.1 Gravação de Ecrã Local (Control + V)

Se encontrar um vídeo silencioso, uma animação ou um tutorial no seu ecrã, pode capturá-lo diretamente:

1. Prima **NVDA + Shift + V** para entrar na Camada de Comandos e, em seguida, prima **Control + V**.
2. O extra irá gravar silenciosamente o seu ecrã em segundo plano.
3. Prima **Control + V** novamente para parar a gravação.
4. A IA irá depois analisar o segmento de vídeo gravado e fornecer uma descrição altamente detalhada da cena, das personagens e das ações.

### 5.2 Análise de Vídeo (Shift + V)

Pode analisar tanto ficheiros de vídeo locais como vídeos online. Basta selecionar um ficheiro de vídeo local no Explorador do Windows ou copiar uma ligação de vídeo online para a sua área de transferência. Também pode premir **Shift + V** em qualquer lugar (como dentro de um reprodutor multimédia) para abrir uma janela onde pode procurar um ficheiro de vídeo ou colar um URL manualmente.

- **Plataformas Online Suportadas:** YouTube, Instagram, TikTok e Twitter (X).
- A IA detetará automaticamente o ficheiro local ou o URL, processará o vídeo e fornecerá uma descrição visual abrangente e um resumo em áudio.
- **Cache de Ficheiros de Vídeo por 48 Horas:** Os vídeos enviados para o Gemini são guardados em cache durante 48 horas! Pode recriar ficheiros SRT ou MP3 para o mesmo vídeo sem ter de voltar a enviá-lo — mesmo após reiniciar o NVDA. A cache depende da chave e é automaticamente invalidada quando a sua chave de API é alterada.

### 5.3 Geração de Audiodescrição (SRT)

Para uma experiência mais estruturada, o extra pode gerar guiões profissionais de Audiodescrição no formato padrão SubRip (SRT).

- **Sincronização Inteligente por Pausas:** A IA escuta a faixa de áudio e ancora especificamente as suas descrições visuais em pausas naturais e intervalos silenciosos, de modo a minimizar inteligentemente a sobreposição com os diálogos.
- **Rastreio de Personagens**: O motor realiza uma pré-análise para extrair personagens distintos com base em traços faciais imutáveis. Constrói um dicionário global para rastrear e etiquetar com precisão os personagens em diferentes cenas sem confusão. Também rastreia a **primeira aparição** de cada personagem, descrevendo o seu aspeto físico apenas uma vez — no momento em que aparecem pela primeira vez — e utilizando apenas os nomes definidos nas cenas posteriores para manter a narrativa dinâmica e natural.
- **OCR de Texto Literal:** Qualquer texto que apareça no ecrã (sinais, telemóveis, créditos) é rigorosamente citado de forma literal.
- **Como Utilizar:** Para ouvir a legenda gerada, basta colocar o ficheiro `.srt` na mesma pasta do seu ficheiro de vídeo e dar-lhe exatamente o mesmo nome. Depois, configure o seu reprodutor multimédia (ex.: VLC ou PotPlayer) para encaminhar o texto das legendas diretamente para o seu leitor de ecrã ou motor TTS durante a reprodução.
- **Experiência de Guardar Melhorada:** Ao guardar ficheiros SRT ou MP3, a caixa de diálogo para guardar ficheiros abre agora, por predefinição, na pasta do vídeo de origem, quer tenha aberto o vídeo através da caixa de diálogo de ficheiros ou com Shift+V a partir do Explorador.

### 5.4 Narração de Áudio Sincronizada (Exportação em MP3)

Para além de criar ficheiros SRT em texto, o extra funciona como uma ferramenta completa de produção de Audiodescrição, sintetizando as descrições em voz e misturando-as com o vídeo. Pode agora escolher o **Gemini Live TTS** como motor de voz, o qual utiliza a API do Gemini Live para gerar narrações de voz altamente realistas e ilimitadas. Ao gerar um MP3 para ficheiros de vídeo locais, dispõe de vários modos de mistura:

- **AD Padrão (Misturar Voz):** A narração é sobreposta diretamente sobre o áudio do vídeo. Ser-lhe-á perguntado se pretende aplicar **Atenuação de Áudio (Ducking)** (reduzir o volume de fundo durante as descrições) para garantir que a narração seja percetível.
- **AD Alargada (Pausa no Áudio)**: O motor pausa o áudio do vídeo original durante as descrições, garantindo que nunca perde uma única palavra do diálogo original nem da narração da IA. A deteção de silêncio utiliza agora o modelo neuronal **Silero VAD** (transferido automaticamente na primeira utilização, tal como o ffmpeg e o eSpeak) para uma temporização precisa dos intervalos — distinguindo pausas naturais de diálogo de música e ruído de fundo.
- **Vídeos do YouTube:** Para fontes do YouTube (que não são transferidas localmente), a exportação MP3 conterá estritamente a faixa de voz de IA sincronizada, sem o áudio de fundo do vídeo.

## 7. Transcrição e Dobragem de Média (M)

O Transcritor de Áudio foi completamente reconstruído para suportar ficheiros de áudio e vídeo (MP3, WAV, MP4, MKV, etc.). Prima **M** na Camada de Comandos para selecionar um ficheiro multimédia e escolha um dos 3 modos de operação distintos:

1. **Transcrever (Idioma Original)**: Transcreve com precisão a fala no seu idioma original.
2. **Transcrever e Traduzir (Idioma de Destino)**: Transcreve a fala e traduz-a para o seu idioma de destino configurado.
3. **Dobrar e Traduzir (Idioma de Destino)** _(Apenas Gemini)_: Uma nova funcionalidade potente que transcreve a fala, traduz-a para o seu idioma de destino e sintetiza uma dobragem em áudio falado utilizando o motor TTS do extra.

## 8) Leitor Avançado de Documentos e Imagens

O **Leitor de Documentos** transforma os seus documentos em texto limpo e legível — para que possa ler, traduzir e ouvir qualquer coisa, desde um livro digitalizado a um monte de fotos. Suporta PDFs de várias páginas, imagens complexas, formatos HEIC do iPhone e até ficheiros de texto simples (`.txt`) e HTML (`.html`, `.htm`), que são abertos instantaneamente sem OCR ou processamento por IA. Selecione vários ficheiros de uma só vez e eles serão unidos num único documento contínuo pela ordem das páginas. Estão disponíveis três motores de OCR — **Chrome (Rápido)**, **IA (Avançado)** para uma preservação de esquema superior, e **Nenhum (Extrair Camada de Texto)** para PDFs pesquisáveis — selecionados em Definições → Leitor de Documentos.

### Como Funciona

1. Prima **NVDA + Shift + V**, depois **D** para abrir o Leitor de Documentos — ou selecione primeiro um ficheiro no Explorador de Ficheiros e prima **D** / **F** para ignorar totalmente o diálogo de ficheiro.
2. Escolha um ou mais PDFs ou imagens. O add-on analisa-os e anuncia o número total de páginas.
3. No diálogo de **Opções**, escolha o intervalo de páginas (De/Para). Também pode marcar **Traduzir Saída** e escolher o idioma de destino, ou alternar **Descrever imagens embutidas durante o OCR**.
4. A extração de texto é iniciada em segundo plano e em lotes. Pode fechar a janela a qualquer momento e continuar mais tarde — nada será perdido.
5. Assim que as páginas estiverem prontas, leia-as no visualizador: navegue entre páginas, vá para qualquer página, faça perguntas à IA, guarde o texto ou gere uma narração em áudio.

### 7.1 Processamento em Lote e Retoma

Não precisa de ler um documento massivo todo de uma vez. Escolha um intervalo de páginas (por exemplo, `1-20`) ou mantenha os valores predefinidos para processar tudo, e a IA extrai todas as páginas em segundo plano. Se o NVDA crashar ou se interromper a verificação, o suplemento lembra-se do seu progresso e oferece-se para **Retomar** exatamente onde ficou — mesmo após reinícios. Os documentos concluídos também são colocados em cache, pelo que reabri-los (a partir de Documentos Recentes ou através de **D**) carrega o texto instantaneamente sem voltar a executar o OCR, a menos que os ficheiros de origem tenham sofrido alterações.

### 7.2 Ação Inteligente em Ficheiros

Nem sempre precisa de abrir o documento primeiro. No Explorador de Ficheiros do Windows, basta selecionar um PDF, imagem ou ficheiro de texto/HTML e premir **D** (Leitor de Documentos) — ou selecionar um PDF ou imagem e premir **F** (Ação Inteligente em Ficheiros) — dentro da Camada de Comandos. O suplemento ignora instantaneamente a caixa de diálogo de ficheiros e começa a processar o ficheiro selecionado. Selecionar vários ficheiros de uma vez processa-os em conjunto como um único documento.

### 7.3 Controlos e Atalhos do Visualizador de Documentos

Quando a janela do Leitor de Documentos estiver aberta, pode utilizar o seguinte:

#### Atalhos de teclado

- **Ctrl + PageDown / Ctrl + PageUp:** Avança para a página seguinte / anterior.
- **Seta para baixo / Seta para cima:** Quando o cursor atingir a última linha de uma página, prima **Seta para baixo** para ir para a página seguinte; prima **Seta para cima** no topo de uma página para regressar à anterior.
- **Alt + A:** Abrir uma janela de conversa para fazer perguntas sobre o documento.
- **Alt + R:** Forçar uma **Nova Análise com IA** utilizando o seu provedor ativo.
- **Alt + G:** Gera e guarda um ficheiro de áudio de alta qualidade (WAV/MP3). _(Oculto se o fornecedor não suportar TTS)._
- **Alt + S / Ctrl + S:** Guardar o texto extraído como um ficheiro TXT ou HTML.

#### Botões e controlos

- **Ir para:** Escolha qualquer página no seletor de páginas.
- **Ver formatado:** Veja o documento completo combinado como texto formatado.
- **Tentar novamente páginas com falha:** Tente novamente apenas os lotes que falharam devido a um erro temporário do servidor (por exemplo, grande afluência). Este botão aparece automaticamente quando necessário.
- **Voz de TTS / Motor de TTS:** Escolha a voz e, no Gemini, escolha entre **TTS padrão** e transmissão **Gemini Live**.
- **Anterior / Seguinte:** Navegue entre páginas (igual aos atalhos Ctrl+PageUp/Down).

### 7.4 Documentos Recentes (D)

Ao premir **D** na Camada de Comandos, os seus documentos lidos recentemente são listados em primeiro lugar. Escolha um para continuar a partir da página em que estava — mesmo que o OCR já tenha terminado — ou prima **Abrir ficheiro...** (`Ctrl + O`) para procurar um ficheiro como habitualmente.

## 9. Etiquetagem Semântica por IA e Explorador de IU

Preso numa aplicação cheia de "botão sem etiqueta" por todo o lado? O motor de Etiquetagem Semântica por IA resolve isto definitivamente.

### 8.1 Etiquetagem Permanente de Objetos (L)

Foque o seu leitor de ecrã num gráfico ou botão sem etiqueta e prima **L** na Camada de Comandos. A IA analisará o botão visualmente, determinará a sua função e aplicará uma etiqueta permanente.
_Ao contrário das ferramentas de etiquetagem mais antigas dos leitores de ecrã, este extra utiliza um sistema híbrido avançado de "Assinatura de Objeto" (AutomationId/ControlID). As suas etiquetas personalizadas resistirão ao redimensionamento de janelas, à alteração de monitores e às atualizações das aplicações!_

### 8.2 Verificação Completa da Aplicação (Shift + L)

Prima **Shift + L** para analisar toda a janela ativa de uma só vez. A IA encontrará todos os elementos sem etiqueta e nomeá-los-á inteligentemente de uma só assentada. Mais tarde, poderá gerir, renomear ou eliminar em lote estas etiquetas no Gestor de Etiquetas integrado.

### 8.3 Explorador de IU (E)

Precisa de interagir com um elemento sem navegar até ele manualmente? Prima **E** para ativar o Explorador de UI. A IA analisará o ecrã e gerará uma lista acessível de todos os elementos clicáveis (ignorando ruídos do sistema como as barras de tarefas). Escolha um item da lista e o extra clicará nele instantaneamente por si.

## 10. Assistente de Voz em Direto

The Live Assistant turns Vision Assistant Pro into a real-time, interactive copilot.
_(Note: This feature is exclusive to Google Gemini and Gemini-compatible Custom providers)._

- **Ativação:** Prima **Control + L** na Camada de Comandos para abrir a janela do Assistente em Direto.
- **Interação em Tempo Real:** Fale naturalmente através do seu microfone. A IA escutará a sua voz e analisará o seu ecrã ativo em simultâneo. Pode fazer perguntas como "O que estou a ver?" ou "Lê o terceiro parágrafo para mim."
- **Prima para falar:** Ative o **Prima para falar** no separador de definições do Assistente Live (ou alterne diretamente na janela do Assistente Live), depois mantenha premida a tecla atribuída para falar e liberte-a para terminar. Isto mantém o microfone sem som até premir a tecla — perfeito para ambientes ruidosos.
- **Entrada de Câmara Web:** Marque **Utilizar &câmara web** na janela do Assistente em Direto para enviar a imagem da sua câmara para a IA em vez do seu ecrã — pergunte sobre objetos físicos, documentos impressos ou o que o rodeia. Se o ffmpeg ainda não estiver instalado, ao marcar a caixa este é transferido uma vez com a sua permissão; a opção fica desativada quando nenhuma câmara é detetada ou quando as definições de privacidade do Windows bloqueiam o acesso à câmara.
- **Personalização:** Dentro da janela, pode alterar o Estilo de Voz da IA (ex.: Profissional, Amigável, Animado) e ajustar a sua "Profundidade do Pensamento" para controlar o nível de raciocínio antes de responder.

## 11. Observador Ambiental (Assistente em Segundo Plano)

The Ambient Observer turns Vision Assistant Pro into your background eyes, without any conversation: it keeps listening and watching while you work, reports what changes, and stays silent when nothing happens.
_(Note: This feature is exclusive to Google Gemini and Gemini-compatible Custom providers)._

- **Correções de Erros e Melhorias de Estabilidade**: Foi corrigido um bloqueio durante a geração de MP3 ao fechar a caixa de diálogo de progresso a meio da tarefa, resolvido um problema de condição de corrida (race condition) no armazenamento do dicionário de personagens, adicionada a comunicação adequada de erros para falhas na codificação de MP3 e corrigido o ciclo de espera do leitor de documentos para respeitar o cancelamento do utilizador.
- **Modes:** **Audio Translation Only** translates what it hears, **Screen Watcher Only** reports screen changes, and **Webcam Watcher Only** opens the Live Assistant window with your camera and Push to Talk, so you can ask questions about what the camera sees.
- **Audio Source:** In the audio mode, choose whether to translate your **Microphone** or the **System Audio (Loopback)**. The small loopback library is downloaded once on first use, with your permission.
- **Context:** For the screen and webcam modes, pick an optional **About what I am doing** option (for example watching a film, following a meeting or call, reading a label, or checking your appearance) to focus the reports; you can also type your own context.
- **Reporting:** The add-on compares every new frame with the previous one and sends it to the AI only when the picture really changed, so a static screen never costs you requests. The AI then reports only what is new and never repeats itself.
- **Welcome Message:** Except in the translation mode, the observer greets you briefly when it starts, so you know it is listening.
- **Settings:** In **Settings > Live Assistant**, set the **Observer Mode**, the **Frame Interval** (1 to 10 seconds) and the **Reporting Style** (brief or detailed). The observer instruction and each context text can be edited in the Prompt Manager (section **Ambient**).

## 12. Prompts e Variáveis Personalizados

Pode gerir as prompts em **Definições > Prompts > Gerir Prompts...**.

- **Filter:** The **Default Prompts** tab has a **Filter** list above the prompt list that shows **All** prompts or only one section at a time (for example **Ambient**), so long lists stay easy to navigate.

### Atalhos de Prompts Personalizados

Atribua um atalho de teclado próprio a qualquer instrução personalizada diretamente no Gestor de Instruções e execute-a instantaneamente com a sua seleção ou contexto atual:

- **Tecla única** (por exemplo, `1`, `p` ou `F3`): Funciona dentro da Camada de Comandos e também globalmente como `NVDA + Shift + tecla`.
- **Combinação de teclas** (por exemplo, `Control + Shift + 1`, `Alt + P` ou `Insert + 1`): Funciona globalmente por si só.

### Per-Prompt Feedback Behavior

Each custom prompt can individually define its output delivery behavior:

- **Global setting:** Follows the general Connection output setting (Direct Output or Chat window).
- **Copy to clipboard:** Copies the AI response directly to the clipboard without opening a window.
- **Direct Output (NVDA message):** Speaks/brailles the AI response directly via NVDA speech.
- **Copy to clipboard and Direct Output:** Copies the response to the clipboard and speaks it directly.
- **Chat window:** Always opens the result in an interactive conversation window.

### Variáveis Suportadas

- `[selection]`: Texto atualmente selecionado.
- `[text]`: Complete text content of the currently focused edit field (automatically ignores protected password boxes).
- `[currentURL]`: Webpage or document URL from supported web browsers (Chrome, Edge, Firefox).
- `[clipboard]`: Conteúdo da área de transferência.
- `[clipboard_image]`: Imagem atualmente na área de transferência.
- `[screen_obj]`: Captura de ecrã do objeto de navegação.
- `[screen_fg_obj]`: Captura de ecrã da janela ativa em primeiro plano.
- `[screen_full]`: Captura do ecrã inteiro.
- `[file_ocr]`: Selecionar ficheiro de imagem/PDF para extração de texto.
- `[file_read]`: Selecionar documento para leitura (TXT, Código, PDF).
- `[file_audio]`: Selecionar ficheiro de áudio para análise (MP3, WAV, OGG).
- `[ambient_screen]`: Starts continuous Screen Observer background session.
- `[ambient_webcam]`: Starts continuous Webcam Observer background session (checks Push to Talk from settings).
- `[ambient_audio]`: Starts live Audio Observer translation session.
- `[loopback]`: Uses system audio playback as sound source (for `[ambient_audio]`).
- `[mic]`: Uses microphone as sound source (for `[ambient_audio]` and `[ambient_webcam]`).
- `[brief]`: Sets observer reporting style to brief (single sentence).
- `[detailed]`: Sets observer reporting style to detailed (2-3 sentences).
- `[lang:code]`: Specifies target language code for audio translation (e.g., `[lang:fa]`, `[lang:en]`).
- `{target_lang}`: Idioma de destino atual.
- `{source_lang}`: Idioma de origem atual.
- `{response_lang}`: Idioma atual de resposta da IA.
- `{swap_target}`: Idioma alternativo para a tradução com troca inteligente.
- `{swap_instruction}`: Bloco de instruções de tradução com troca inteligente.

_Note on Ambient Prompts:_ Prompts containing ambient variables act as a toggle — pressing the shortcut while active immediately stops the session. Incompatible combinations (such as combining static screenshot variables like `[screen_full]` with ambient observer modes, combining multiple ambient modes, or adding prompt instructions to `[ambient_audio]`) are strictly validated and prevented when saving.

## 13. Casos de Uso no Mundo Real (Que funcionalidade devo utilizar?)

O Vision Assistant Pro está repleto de ferramentas avançadas. Eis alguns cenários comuns para o ajudar a escolher a opção certa:

- **Scenario: You want to understand the complete layout of a complicated window or inaccessible app.**
  _Solution:_ Press **O** (Full Screen Vision). The AI will analyze the entire screen and describe exactly where elements, texts, and buttons are positioned.

- **Scenario: You found an image on a webpage or an unlabeled graphic in a document.**
  _Solution:_ Move your navigator object to the graphic and press **V** (Object Vision). The AI will describe specifically what that image contains.

- **Scenario: You want to watch a movie or video clip with audio descriptions.**
  _Solution:_ Press **Shift + V** on your video and choose **"Generate Audio Description (SRT File)"**. When it finishes, click **"Generate Synced Narration (MP3)"** and select **"Extended AD"**. The add-on will create an audio track that intelligently pauses the movie's dialogue to describe the visual scenes.

- **Scenario: You encountered an app full of "unlabeled buttons".**
  _Solution:_ Press **L** to permanently label the specific button using AI. Or, press **Shift + L** to scan and label the entire window at once. If you just want to click something quickly, press **E** (UI Explorer) to get a list of all clickable items.

- **Scenario: You need to bypass an inaccessible CAPTCHA.**
  _Solution:_ Press **C** (CAPTCHA Solver). The AI will automatically capture the CAPTCHA, solve it, and inject the answer into the correct field.

- **Scenario: You want to read a long, 50-page PDF document.**
  _Solution:_ Press **D** (Document Reader), set your provider to Google Gemini, and enter the page range `1-50`. The add-on will extract the text accurately in the background.

- **Scenario: You are watching a silent video tutorial or animation on your screen.**
  _Solution:_ Press **Control + V** to start recording the screen. Let the tutorial play, then press **Control + V** again. The AI will explain exactly what was demonstrated.

- **Scenario: You encounter an unexpected error, API connection failure, or want to diagnose issues with custom local servers.**
  _Solution:_ Go to **Settings > Advanced**, check **"Enable dedicated log file"**, and set the **Log Level** to **"Debug"**. Perform the action again, then click **"Open Log File"** to inspect technical details or attach `vision_assistant.log` to a support ticket.

***

**Nota:** É necessária uma ligação ativa à Internet para todas as funcionalidades de IA. Os documentos de várias páginas são processados automaticamente.

## 14. Suporte e Comunidade

Mantenha-se atualizado com as últimas notícias, funcionalidades e lançamentos:

- **Canal do Telegram:** [t.me/VisionAssistantPro](https://t.me/VisionAssistantPro)
- **GitHub Issues:** Para relatórios de erros e pedidos de novas funcionalidades.

### Relatar Erros e Registos

Ao abrir um pedido de assistência (issue) no GitHub ou ao solicitar suporte, inclua detalhes sobre o seu provedor de IA ativo, modelo e versão do NVDA. Se estiver a ter problemas de ligação ou fechos inesperados, ative o ficheiro de registo dedicado em **Definições > Avançado**, recrie o problema e anexe o seu ficheiro `vision_assistant.log` para nos ajudar a resolver o problema mais rapidamente.

## 15. Apoiadores do Projeto

Um agradecimento do fundo do coração aos membros da nossa comunidade que apoiam o desenvolvimento contínuo e a manutenção deste projeto através das suas generosas contribuições financeiras:

- **@Alyabani94**
- **Ali Alamri**
- **Ilya**
- **leonardo0216**
- **Sergei Fleytin**
- **Arne Siebert**
- **Schalkefan**
- **Rainer Brell**
- **[avalai.org](https://avalai.org)**

_Se desejar apoiar o projeto financeiramente e ver o seu nome aqui, pode encontrar a opção **Doar** no menu Ferramentas do NVDA (sub-menu Vision Assistant) ou durante o processo de configuração após a instalação._

---

## Alterações para 2026.10.15

- **The Most Requested Fix — Creating a Gemini API Key Is Finally Easy**: Getting an API key on **aistudio.google.com** used to be the hardest step of all. With a screen reader the pages were confusing, and some people simply could not create a key at all. That problem is now solved directly inside the add-on. Press **G** in the Command Layer (or use **Get a Gemini API Key...** in Settings), sign in through your default browser with zero external setup, and your key is created and configured with one confirmation — even if you never had a project before.
- **Ambient Observer**: The background assistant is here. Press **Shift+O** in the Command Layer to start it, and press it again to stop it. It can translate what it hears (your microphone or the sound of the system), watch the screen and tell you what changed, or open the Live Assistant with your webcam and Push to Talk so you can ask about whatever the camera sees. It sends a picture only when something really changed, so a still screen costs you nothing, and it stays quiet when nothing is happening. You can also launch and toggle the observer directly through Custom Prompts and dedicated shortcut keys using `[ambient_screen]`, `[ambient_webcam]`, or `[ambient_audio]` along with modifiers (`[loopback]`, `[mic]`, `[brief]`, `[detailed]`, `[lang:code]`), with automatic validation against conflicting variable combinations.
- **Live Operator**: The Live Assistant can now carry out what you ask on your computer while you talk to it. Press **Control+A** in the Command Layer to start a live operator session, then just ask in plain language. It works through multi-step requests, says every step in the Live Assistant’s own voice, takes care of the key combinations it needs, and decides by itself when the task is finished. **Live Direct Output (No Window)** is in Quick Settings too.
- **Dicionário de Personagens e Gestão de Séries**: A caixa de diálogo de Análise de Vídeo inclui agora um poderoso sistema de **Dicionário de Personagens**! Adicione, edite, importe ou gira nomes de personagens, descrições físicas e papéis por série — a IA associa automaticamente os personagens detetados ao seu dicionário e une os novos à medida que analisa mais episódios. As suas notas manuais são sempre preservadas com prioridade sobre as atualizações da IA, enquanto as descrições físicas se mantêm atualizadas ao longo dos episódios. O dicionário é guardado por série e reutilizado para cada vídeo dessa série. Na lista de personagens, prima **F2** para editar o personagem selecionado e **Delete** para o remover.
- **SOCKS5, HTTP, and Reverse Proxy Support with Latency Testing**: Seamlessly bypass network restrictions with complete proxy support across the entire add-on — including the Live Assistant, Ambient Observer, and TTS generation! Choose from 4 operating modes in General settings: **Auto-detect**, **SOCKS5 Proxy**, **HTTP Proxy**, or **Reverse Proxy**. SOCKS5 supports RFC 1929 username/password authentication and domain tunneling; HTTP proxy supports Basic authentication. A new **Test Proxy Connection** button runs in the background and announces your connection latency in milliseconds.
- **Cache de Ficheiros de Vídeo por 48 Horas**: Os vídeos enviados para o Gemini são agora guardados em cache durante 48 horas! Pode recriar ficheiros SRT ou MP3 para o mesmo vídeo sem ter de voltar a enviá-lo — mesmo após reiniciar o NVDA. A cache depende da chave e é automaticamente invalidada quando a sua chave de API é alterada.
- **Deteção de Silêncio com IA (Silero VAD)**: A AD Alargada utiliza agora o modelo neuronal Silero VAD para uma deteção de silêncio precisa — distinguindo pausas naturais de diálogo de música e ruído de fundo. O modelo é transferido automaticamente na primeira utilização (com a sua permissão), tal como o ffmpeg e o eSpeak.
- **Vídeo de Câmara Web para o Assistente em Direto**: A janela do Assistente em Direto tem agora uma caixa de seleção **Utilizar &câmara web** para enviar a imagem da sua câmara web para a IA em vez do seu ecrã — perfeito para fazer perguntas sobre objetos físicos, documentos ou o que o rodeia. Se o ffmpeg ainda não estiver instalado, ao marcar a caixa este é transferido (uma única vez, com a sua permissão). A opção fica desativada quando nenhuma câmara é detetada ou quando as definições de privacidade do Windows bloqueiam o acesso à câmara, apresentando um botão para abrir as definições de privacidade da câmara. Se a câmara estiver ativada mas não produzir fotogramas, o problema é registado no diário do NVDA para diagnóstico, em vez de voltar silenciosamente para o ecrã.
- **Audio Output Device Selection**: You can now select a dedicated audio output device for the Live Assistant and Ambient Observer. Choose between NVDA's default output, Windows Sound Mapper, or any connected physical sound card (like USB headphones or external speakers) in the Live Settings tab, directly inside the Live Assistant dialog, or on the fly via Quick Settings (NVDA+Shift+V then Up/Down/Left/Right).
- **Prompt Manager**: The Default Prompts tab has a **Filter** list now, so you can show all prompts or just one section (for example **Ambient**). You can also edit the observer’s context texts and the new **Live Operator Instruction** there.
- **Smart Model Filtering in Advanced Routing**: Advanced Model Routing dropdowns now dynamically categorize Gemini models by capability without clutter. The Live Assistant only displays genuine bidirectional live and native-audio models, TTS only displays dedicated speech synthesis models, STT prioritizes Transcribe and multimodal models, and Video Analysis, OCR, and AI Operator cleanly filter out single-purpose utility models (such as image generation, video generation, and embedding models). Future models are detected automatically based on capability without requiring version updates.
- **Rastreio da Primeira Aparição de Personagens**: A IA descreve agora a aparência física de cada personagem apenas uma vez — na sua primeira aparição no vídeo. As aparições subsequentes utilizam apenas os nomes, eliminando descrições repetitivas ao longo dos segmentos e mantendo a narrativa dinâmica e natural.
- **Diretório de Dados Unificado**: Todos os ficheiros de dados do add-on (histórico, séries, etiquetas, progresso de OCR, caches e registos) foram migrados para uma única pasta `VisionAssistant` dentro do seu diretório de configuração do NVDA — mantendo tudo organizado e tornando as cópias de segurança manuais extremamente simples.
- **Experiência de Guardar Vídeos Melhorada**: Ao guardar ficheiros SRT ou MP3, a caixa de diálogo para guardar ficheiros abre agora, por predefinição, na pasta do vídeo de origem, quer abra o vídeo através da caixa de diálogo de ficheiros ou com Shift+V a partir do Explorador.
- **Eliminar Documentos Com ou Sem o Respetivo Texto em Cache**: A caixa de diálogo do Histórico (`Control + H`) oferece agora duas formas de eliminar um documento — prima Delete e escolha **Eliminar apenas do histórico** ou **Eliminar do histórico e do texto em cache**. A segunda opção limpa o texto de OCR em cache desse documento, pelo que a próxima abertura voltará a analisá-lo do zero — ideal após uma verificação com fraca qualidade. A caixa de seleção **Não voltar a perguntar** memoriza a sua escolha para eliminações futuras. Os seus dados de retoma de operações interrompidas nunca são alterados.
- **Cache de OCR no Leitor de Documentos Inteligente em Relação ao Motor e Com Fusão**: O texto de OCR em cache é agora guardado por motor de OCR, pelo que alternar o motor de OCR volta a analisar sempre com o novo motor em vez de reproduzir o resultado antigo. Voltar a abrir um documento apresenta novamente a caixa de diálogo do intervalo de páginas (pré-preenchida com a sua última escolha), reutilizando instantaneamente as páginas já analisadas e analisando apenas as que faltam — a cache junta as páginas uma a uma em vez de ser substituída, mantendo assim cada intervalo lido para mais tarde.
- **PDF Compression in Document Reader**: Added an optional **Compress PDF pages before processing** setting in the Document Reader's page range dialog. When uploading large or high-resolution scanned PDF documents to Gemini or Mistral, pages are automatically downscaled and re-compressed to dramatically reduce upload payload size, speed up processing, and prevent network timeouts. The option is disabled by default and automatically hidden when using the Chrome engine or base64-based image providers.
- **Per-Prompt Feedback Behavior Customization**: Customize how each custom prompt delivers its output individually! In the custom prompt editor, choose between **Global setting**, **Copy to clipboard**, **Direct Output (NVDA message)**, **Copy to clipboard and Direct Output**, or **Chat window**. This allows specific prompts to speak directly without opening a window while others open a full chat.
- **New Dynamic Prompt Variables (`[currentURL]` & `[text]`)**: Custom Prompts now support `[currentURL]` to capture the active document URL across Google Chrome, Mozilla Firefox, and Microsoft Edge, and `[text]` to dynamically insert the full text content of the currently focused edit field (ignoring protected password boxes).
- **Twitter/X Video Downloader Overhaul**: Restored downloading and analysis of Twitter/X videos following upstream scraper failures. Video extraction now utilizes the robust FixTweet API to directly fetch highest-quality MP4 streams from Twitter's CDN, complete with automatic TwitSave fallback and proxy support.
- **Instagram Video Downloader Fix**: Restored downloading and analysis of Instagram Reels and video URLs following upstream form changes on the downloader service.
- **Fixes & Performance**: Push to Talk answers the moment you press the key, the Live Assistant no longer starts a reply in the middle of a sentence, the observer no longer reports the previous picture, and the Thinking Depth list only offers what your model actually supports. The AI Operator can scroll left and right too. Fixed an `AttributeError` when analyzing online videos, and prevented custom prompts without text selection from accidentally injecting background window titles into AI requests.

## Alterações para 2026.09.01

- **Histórico (Control + H)**: A Camada de Comandos inclui agora uma janela de diálogo do **Histórico** (`Control + H`) que lista as suas conversas e documentos anteriores com filtros para Tudo, Conversas e Documentos. Reabra qualquer conversa com o seu histórico completo — os ficheiros anexados são reanexados automaticamente — ou reabra um documento e continue a leitura. Prima **Delete** em qualquer item para o remover, ou limpe tudo de uma só vez.
- **Documentos recentes no Leitor**: Ao premir **D** na Camada de Comandos, são agora apresentados os seus documentos lidos recentemente em primeiro lugar. Escolha um para continuar a partir da página em que estava — mesmo quando o OCR já tiver terminado — ou prima **Abrir ficheiro...** (`Ctrl + O`) para procurar como habitualmente.
- **Prima para falar no Assistente Live**: Assuma o controlo total das suas conversas em tempo real! Ative o **Prima para falar** no novo separador de definições do Assistente Live e atribua qualquer tecla — ou até uma tecla modificadora isolada como `Ctrl Esquerdo` — para falar. Mantenha a tecla premida para falar e liberte-a quando terminar, com um sinal sonoro curto a cada ativação e libertação. Aparece também um botão de alternância correspondente diretamente na janela do Assistente Live, permitindo alternar entre o modo prima para falar e o modo de microfone aberto sem sair da conversa.
- **Áudio nativo do Gemini 2.5 Flash**: O Assistente Live suporta agora o modelo de áudio nativo do Gemini 2.5 Flash (`gemini-2.5-flash-native-audio-preview-12-2025`) para conversas de voz de baixa latência e mais naturais. Pode mudar para este modelo em **Definições → Encaminhamento Avançado de Modelos → Modelo do Assistente Live (Apenas Gemini)**, ou manter em "Auto" para permanecer no modelo recomendado.
- **Cópia de Segurança e Restauro de Definições**: Adicionado um poderoso sistema de cópia de segurança e restauro no separador **Avançado**! Pode agora guardar todas as definições do seu add-on — incluindo chaves de API, modelos, pedidos personalizados (prompts) e preferências — num único ficheiro JSON, e restaurá-las perfeitamente a qualquer momento, em qualquer máquina ou após reinstalar o NVDA. Ao fazer a cópia de segurança, pode escolher o que incluir: **Tudo** (definições, etiquetas personalizadas, progresso de OCR e histórico) ou **Apenas Definições**.
- **Leitura direta de texto e HTML**: O Leitor de Documentos pode agora abrir ficheiros de texto simples (`.txt`) e HTML (`.html`, `.htm`) diretamente! Deteta automaticamente a codificação do ficheiro, remove scripts e elementos de formatação desnecessários e divide o conteúdo de forma inteligente em páginas legíveis — reimportando inclusive os seus próprios ficheiros exportados enquanto preserva a estrutura de páginas — para que possa lê-los instantaneamente sem necessidade de OCR ou processamento por IA!
- **TTS Gemini Live para o Leitor de Documentos**: O botão "Gerar Áudio" suporta agora o Gemini Live — um motor de síntese de voz por transmissão de alta qualidade e com ritmo natural! Quando o Gemini é o seu fornecedor ativo, pode escolher entre o TTS Padrão e o Gemini Live diretamente no leitor, sendo a sua seleção memorizada para a próxima vez!
- **Atalhos de Prompts Personalizados**: You can now assign a shortcut key to any of your custom prompts right from the Prompt Manager! Give every prompt its own dedicated key or key combination to run it instantly, automatically capturing your current selection or context with zero extra steps!
- **Navegação nas mensagens do chat**: Reveja qualquer conversa sem usar as mãos! Dentro de qualquer janela de chat (Chat direto, chat do documento, refinar e mais), prima `Alt + Seta para baixo` para ouvir a mensagem seguinte e `Alt + Seta para cima` para ouvir a anterior — com prefixos claros de "Você" / "IA" e anúncios de limite de "Primeira mensagem" / "Última mensagem" à medida que navega.
- **Copiar mensagem do chat (Alt + C)**: Ao rever uma conversa com `Alt + Seta para cima/baixo`, prima `Alt + C` para copiar a mensagem em que se encontra para a área de transferência — respeitando a sua definição de Markdown Limpo — com uma confirmação falada.
- **Instrução do sistema do Chat Direto**: O Chat Direto (`Shift+C`) tem agora a sua própria instrução do sistema editável — "Instrução do Chat Direto" — que define a personalidade do assistente e o idioma de resposta para todas as conversas. Pode personalizá-la no separador Instruções Padrão do Gestor de Instruções.
- **Navegação de páginas pelo cursor no Leitor de Documentos**: Ler documentos com várias páginas tornou-se ainda mais fluido! No Visualizador de Documentos, quando o cursor atinge a última linha de uma página e prima `Seta para baixo`, o leitor avança automaticamente para a página seguinte. Premir `Seta para cima` no início de uma página leva-o de volta à página anterior sem interrupções — sem necessidade de alternar de página manualmente durante a leitura!
- **Novas alternâncias nas Definições Rápidas**: Copiar respostas da IA para a área de transferência, Saída Direta (sem janela de chat), Markdown Limpo no Chat e Troca Inteligente podem agora ser ativados e desativados instantaneamente a partir das Definições Rápidas da camada de comandos!
- **Separador de definições do Assistente Live**: O Assistente Live tem agora o seu próprio separador de definições dedicado! A opção "Assistente Live: Saída Direta (Sem Janela)" foi movida do separador Conexão para aqui, e o separador é apresentado apenas quando o Google Gemini (ou um fornecedor Personalizado compatível com o Gemini) for o seu fornecedor ativo.

## Alterações para 2026.08.06

- **Etiquetagem no Explorador de UI**: Agora pode adicionar etiquetas diretamente aos elementos encontrados dentro do Explorador de UI! Foi adicionado um novo botão "Adicionar Etiqueta" e a interface permanece aberta de forma inteligente mantendo o foco, para que possa etiquetar rapidamente vários objetos sem interrupções.
- **Melhoria na Camada de Definições Rápidas**: A camada do Vision Assistant (`Insert+Shift+V`) é agora persistente e altamente interativa! Pode utilizar as setas `Cima/Baixo` para navegar entre as definições rápidas (Provedor, Modelo, Idioma de Resposta da IA, Modelo TTS) e as setas `Esquerda/Direita` para alterar instantaneamente os seus valores com um feedback de voz inteligente e conciso. As suas seleções entram em vigor imediatamente (incluindo a ativação automática do encaminhamento avançado, quando necessário) e a camada permanece ativa enquanto configura.
- **Conversa Direta (`Shift+C`)**: Adicionado um novo comando à camada! Prima `Shift+C` para abrir instantaneamente uma janela de "Conversa Direta". Isto fornece de imediato uma interface de conversação limpa e baseada em texto com a IA, sem necessitar de uma imagem ou documento como ponto de partida.
- **Recuperação Perfeita do Histórico de Conversa**: Corrigido um erro grave onde a pressão da tecla `Espaço` para recordar o último resultado perdia o histórico de conversa subsequente. Agora, o extra rastreia globalmente a sua conversação. Se conversar, fechar a janela e premir `Espaço` para a recordar, todo o seu histórico de trocas de mensagens é perfeitamente restaurado! Funciona para Conversa Direta, Análise de Visão, Conversa sobre Documentos e Tradução.
- **Descrições de Imagens Inline no OCR**: Adicionada uma funcionalidade opcional para descrever imagens no próprio texto durante o OCR de documentos. Pode ativar ou desativar esta definição nas definições de OCR do extra, nas opções do Leitor de Documentos antes da extração ou rapidamente na camada de Definições Rápidas.
- **Tradução por Voz (`Control+T`)**: Adicionada uma nova e potente funcionalidade! Dite a sua fala e traduza-a e escreva-a instantaneamente através de IA com base nos seus idiomas de origem e destino configurados.
- **Melhorias no Transferidor de Atualizações**: A janela de transferência de atualizações exibe agora corretamente o progresso da transferência em percentagens e foi corrigido um erro em que surgia uma mensagem fantasma "A transferir atualização" ao cancelar a instalação.
- **Melhorias no Transferidor do eSpeak-NG**: Adicionado o acompanhamento do progresso em percentagem para as transferências do eSpeak-NG.
- **Resiliência no OCR em Lote**: Corrigido um problema no OCR em lote de ficheiros PDF onde o processo parava se a chave de API ativa atingisse a quota a meio; agora muda automaticamente para a próxima chave disponível e retoma o processo.
- **Suporte a CAPTCHA Visual**: Adicionado um suporte robusto para a resolução de CAPTCHAs visuais. Tenta resolver automaticamente desafios complexos de imagem, como o hCaptcha e reCAPTCHA, melhorando significativamente a acessibilidade em formulários web difíceis.
- **Reformulação do Transcritor de Áudio**: O módulo Transcritor de Áudio foi completamente reconstruído e agora suporta ficheiros de áudio e vídeo. Possui 3 modos de operação distintos: "Transcrever (Idioma Original)", "Transcrever e Traduzir (Idioma de Destino)" e uma nova e potente opção "Dobrar e Traduzir (Idioma de Destino)" (exclusiva do Gemini) que gera uma dobragem de áudio traduzida da fala original.
- **Números de Página Opcionais no Leitor de Documentos**: Adicionada uma nova definição para alternar a inclusão de números de página e separadores na saída de documentos com várias páginas. Pode gerir facilmente esta opção a partir das definições principais ou alterá-la na camada de Definições Rápidas. Esta funcionalidade aplica-se tanto à exportação de ficheiros de texto/HTML como à janela "Ver Formatado", permitindo-lhe ler documentos combinados sem interrupções.
- **Gemini Live TTS Ilimitado para Descrições de Vídeo**: Agora pode selecionar o "Gemini Live TTS" como motor de voz ao gerar Narração de Áudio Sincronizada (MP3) para vídeos. Isto utiliza a API do Gemini Live para sintetizar audiodescrições de alta qualidade sem qualquer limite de carateres ou restrição de duração.
- **Modularização da Base de Código**: Reestruturação da arquitetura do extra de um único ficheiro para uma estrutura modular multificheiro para melhorar a sua manutenção.
- **Redesenho da Interface de Definições**: Redesenho completo da janela de Definições para utilizar uma interface moderna baseada em separadores em vez de uma disposição agrupada, proporcionando uma melhor organização e navegação mais fácil, mantendo todas as opções existentes.
- **Registo em Ficheiro Dedicado e Global**: Adicionado um sistema opcional de registo global em ficheiro sob o novo separador de definições "Avançado". Captura automaticamente eventos operacionais, tráfego de API e erros em todos os módulos do extra num ficheiro dedicado (`vision_assistant.log`). Suporta níveis de detalhe configuráveis (Depuração, Informação, Aviso, Erro), períodos de retenção automatizados (1 hora a 90 dias) e abertura ou limpeza direta do registo a partir das definições sem qualquer impacto no desempenho ou interferência com o registo do NVDA.
- **Acompanhamento do Progresso de Envio no Gemini**: Adicionados anúncios de progresso em percentagem e em tempo real ao enviar ficheiros grandes (vídeo, áudio, documentos) para a API do Google Gemini.

## Alterações para 2026.07.15

- **Filtragem Inteligente de Modelos de API**: Reformulação completa do sistema de filtragem de modelos para utilizar uma abordagem pura de lista negra em vez de listas brancas. Adicionadas palavras-chave de filtragem mais fortes (`embedding`, `bison`, `gecko`, `audio`, `realtime`, `babbage`, `moderation`, `deep`, `antigravity`, `computer`) para garantir que o menu suspenso de modelos de conversa principal permaneça limpo e preparado para o futuro, mantendo todos os modelos especializados acessíveis na secção de Encaminhamento Avançado.
- **Pesquisa no Encaminhamento Avançado**: Todos os menus suspensos do Encaminhamento Avançado de Modelos (OCR, STT, TTS, Operador, Vídeo, Em Direto) e o seletor de Variantes do eSpeak são agora totalmente pesquisáveis. Pode escrever rapidamente para filtrar e encontrar o modelo ou variante pretendido.
- **Novos Atalhos na Camada de Comandos**:
  - **Definições (`Alt + S`)**: Abre instantaneamente a janela de definições do Vision Assistant Pro.
  - **Relatório de Chaves com Quota Esgotada (`Alt + Q`)**: Informa o número exato de chaves de API do Gemini que excederam a sua quota diária, identificando em que modelo específico esgotaram, e anuncia a hora exata da respetiva reinicialização.
  - **Auditoria de Encaminhamento (`Alt + M`)**: Audita e anuncia a sua configuração atual do Encaminhamento Avançado, lendo quais os modelos que estão ativamente selecionados para tarefas especializadas (ignorando as definições padrão).
- **Reformulação Completa do Analisador de Vídeo**: O Analisador de Vídeo foi completamente transformado! Anteriormente, fornecia apenas uma descrição básica de vídeos online. Agora, é um conjunto completo de processamento de vídeo adaptado para utilizadores cegos:
  - **Gravação de Ecrã Local (`Control+V`)**: Agora pode gravar vídeos silenciosos diretamente a partir do seu ecrã. A IA analisará o segmento gravado e fornecerá uma descrição altamente detalhada da cena, disposição e ações.
  - **Geração de Audiodescrição (SRT)**: O extra pode agora gerar guiões de Audiodescrição altamente detalhados (no formato padrão SRT) para vídeos, com sincronização inteligente por pausas para ancorar as descrições nas pausas naturais da faixa de áudio, e OCR literal para qualquer texto no ecrã.
  - **Narração de Áudio Sincronizada (Exportação MP3)**: Para além de legendas em texto, o extra pode sintetizar a Audiodescrição em voz, misturá-la automaticamente com a faixa de áudio original do vídeo, aplicar atenuação de áudio (reduzir o volume de fundo durante as descrições) e exportar o resultado sincronizado final como um ficheiro MP3!
  - **Ação de Ficheiro de Vídeo Inteligente**: Se focar um ficheiro de vídeo local e premir o atalho de vídeo, o extra detetá-lo-á automaticamente e processará o ficheiro diretamente.
  - **Rastreio Avançado de Personagens**: A IA realiza agora uma análise prévia para extração de personagens. Constrói um dicionário global de personagens e rastreia as personagens com precisão, segmento a segmento, sem confundir identidades.
  - **Configuração da Análise de Vídeo**: Adicionadas novas definições para controlar o tamanho dos blocos SRT, legendagem de personagens e avisos de responsabilidade.
  - **Encaminhamento de Modelos Expandido**: Agora pode selecionar explicitamente modelos de vídeo especializados (`gemini_video_model`, `custom_video_model`) nas definições do Encaminhamento Avançado de Modelos.
- **Gestão Inteligente de Quotas da API**: Gestão melhorada dos erros 429 (Limite Diário Excedido) ao rastrear as quotas por modelo. Se uma chave atingir o seu limite diário num modelo, entra inteligentemente em quarentena apenas para esse modelo específico, deixando a chave disponível para utilização com outros modelos.

## Alterações para 5.5.2

- **Retomar Análises Incompletas**: Adicionada uma funcionalidade de retoma tanto para o Leitor de Documentos como para as Ações de Ficheiros Inteligentes. Se uma análise for interrompida, pode agora continuar a partir de onde parou em vez de recomeçar do zero.
- **Nova Variável `[screen_fg_obj]`**: Adicionada uma variável de prompt personalizada para capturar uma imagem apenas da janela ativa em primeiro plano, em vez de todo o ecrã.
- **Tentativas Inteligentes e Rotação de Chaves**: O extra tenta novamente de forma silenciosa até 5 vezes na mesma chave ao encontrar sobrecargas temporárias no servidor (como "alta procura" ou respostas malformadas). Se as tentativas falharem, muda automaticamente para a chave de API seguinte na sua lista.
- **Deteção da Cortina de Ecrã**: Adicionada uma verificação para evitar tirar capturas de ecrã quando a Cortina de Ecrã está ativa (quer esteja ativada permanentemente ou temporariamente através de atalho). O extra irá avisá-lo e parar a ação, evitando que envie imagens pretas e desperdice tokens da API.
- **Ajustes no Leitor de Documentos**: A janela de intervalo de páginas de PDF agora pré-seleciona automaticamente o idioma de destino predefinido a partir das definições do extra. Foi também melhorada a gestão de processos em segundo plano para garantir que param de forma limpa quando o leitor é fechado.
- **Integração Nativa do OCR da Mistral**: Integrada a API nativa de OCR de Documentos da Mistral. Os documentos de várias páginas são automaticamente reunidos, enviados e processados em lotes utilizando o ponto de extremidade especializado `/v1/ocr` da Mistral, enquanto as imagens de uma página são processadas diretamente sem conversões para PDF desnecessárias [1].
- **Manipuladores Dinâmicos de URL Personalizado**: A alteração do URL da API personalizada limpa agora instantaneamente a lista de modelos em cache e restaura a caixa de texto para introdução manual do modelo. Isto garante total compatibilidade com pontos de extremidade personalizados (como o Cloudflare AI Gateway) que não suportam o ponto de extremidade de listagem padrão `/v1/models`.
- **Reformulação do Motor de Entrada do Operador de IA**: Reescrita completa do sistema subjacente de simulação de rato e teclado para o Operador de IA. Substituída a API legada `mouse_event` pela moderna API `SendInput` do Windows, proporcionando uma compatibilidade significativamente superior com aplicações modernas, janelas protegidas por UAC e ecrãs com alta densidade de píxeis (High-DPI).
- **Correção de Operações de Arrastar e Largar**: As ações de arrastar e largar no Operador de IA são agora totalmente estáveis e fiáveis. O novo motor utiliza curvas suaves e naturais, posicionamento preciso do cursor, temporização otimizada e uma técnica inteligente de "pressionamento" para garantir que o Windows e as aplicações reconhecem e executam corretamente os gestos de arrastar e largar sem falhar a meio do caminho.
- **Suporte a Múltiplos Monitores**: O Operador de IA suporta agora totalmente configurações de múltiplos monitores. Os movimentos do rato e cliques funcionam corretamente em todos os monitores através do sinalizador `MOUSEEVENTF_VIRTUALDESK`, garantindo um posicionamento preciso independentemente de em que monitor está a aplicação de destino.
- **Simulação de Teclado Melhorada**: Melhorada a injeção de premiações de teclas para suportar totalmente as "Teclas Estendidas" (tais como teclas de Seta, Home, End, Page Up/Down, Insert, Delete e F1-F12). Isto garante que os comandos de navegação e atalhos enviados pelo Operador de IA funcionam sem falhas em todas as aplicações.
- **Suporte a Imagens HEIC/HEIF**: Adicionado suporte nativo para os formatos de foto do iPhone. Agora pode selecionar diretamente ficheiros `.heic` e `.heif` para descrição por IA, OCR ou Leitura de Documentos sem necessidade de conversão prévia.

## Alterações para 5.5 (A Atualização de Automação)

- **Assistente em Direto**: Adicionada uma funcionalidade de assistente de ecrã e voz em tempo real, disponível exclusivamente para o provedor Google Gemini (ou provedores personalizados compatíveis com o Gemini). Inclui personalização interativa de voz e de profundidade do pensamento diretamente dentro da janela, com reconexão automática ao alterar as definições.
- **Fornecedor de IA MiniMax**: Integração do MiniMax como fornecedor de pleno direito com suporte multimodal completo (conversação, visão, OCR), TTS personalizado utilizando mais de 300 vozes dinâmicas e remoção automática de blocos de raciocínio (por ex., ` thinking... response`) nos resultados.
- **Tradução no Visualizador de Documentos**: Corrigida uma falha silenciosa de tradução para utilizadores do NVDA que não usam inglês, garantindo que o código de idioma padrão de 2 letras seja enviado para o Google Tradutor em vez do nome do idioma localizado.
- **Nova Tentativa na Análise de PDF em Lote**: Implementada uma lógica de nova tentativa separada, silenciosa e altamente otimizada para a análise em lote de documentos PDF, evitando envios redundantes e janelas de erro incómodas durante as novas tentativas.
- **Estado do Visualizador de Documentos**: Corrigido um erro onde o estado geral do extra (verificado via `I`) permanecia bloqueado em "Processamento em Lote Iniciado" durante análises longas de documentos.
- **Resolução de Erro de Processos (Threading)**: Corrigida uma falha grave de asserção de processos `IsMain() failed in wxTimerImpl` ao abrir documentos a partir de uma tarefa em segundo plano, através da transição da fila de retorno da interface gráfica para `wx.CallAfter`.

## Alterações para 5.0

- **Pré-Verificação de Etiquetas Duplicadas**: Corrigido um problema na etiquetagem individual onde a verificação de duplicados utilizava chaves de coordenadas antigas, fazendo com que o NVDA fizesse pedidos de IA duplicados para objetos já etiquetados em vez de anunciar a etiqueta existente.
- **Conversa sobre Documentos para Provedores não-Gemini**: Corrigida uma verificação rigorosa da chave de API na Conversa sobre Documentos (`on_ask`) para garantir que os utilizadores de OpenAI, Groq ou provedores Personalizados locais (como o Ollama) possam conversar com documentos com sucesso sem serem bloqueados.
- **Tradução Rápida de OCR do Chrome**: Restaurada a API de tradução gratuita e sem necessidade de chave para o OCR do Chrome. A tradução do texto extraído ignora agora a IA do Gemini, poupando quotas de API e acelerando o processo de tradução.
- **Filtro Alfanumérico do CAPTCHA**: Corrigida a lógica de filtragem no resolutor de CAPTCHA para garantir que os carateres não alfanuméricos sejam devidamente limpos em todas as situações.
- **Atualização da Ajuda da Camada de Comandos**: Corrigido o atalho do anúncio de estado no menu de ajuda de `L` para `I` e adicionados ambos os comandos de etiquetagem (`L` e `Shift+L`) à lista.

## Alterações para 4.6

- **Correção do Raciocínio dos Modelos Gemma 4**: Corrigido um problema com os modelos Gemma 4 onde todo o processo de pensamento interno era exibido como resposta final, ou onde desativar o raciocínio resultava em respostas em branco. O extra agora isola e extrai corretamente apenas a resposta de texto limpa final.
- **OCR em Lote no Explorador de Ficheiros**: Agora pode selecionar várias fotos ou PDFs diretamente no Explorador de Ficheiros do Windows e extrair texto ou analisá-los em lote. O extra filtrará e processará automaticamente apenas os formatos de ficheiro suportados.

## Alterações para 4.5

- **Integração Universal de IA Local (Configurar IA Local)**: Adicionado um novo botão **"Configurar IA Local"** nas Definições do Provedor Personalizado. Os utilizadores podem agora configurar automaticamente motores de IA locais, incluindo **Ollama**, **LM Studio**, **Jan.ai** e **KoboldCPP** de forma instantânea.
- **Avanço Inteligente de Proxy Local**: Reconstrução da lógica de ligação com um mecanismo avançado de avanço de proxy. O extra é agora inteligente o suficiente para ignorar completamente os proxies do sistema Windows para ligações de loopback locais, garantindo ligações estáveis à IA local mesmo quando a sua VPN ou modo TUN está ativo.
- **Etiquetagem por IA Ultraestável (v2)**: Substituição das chaves de coordenadas absolutas de ecrã por um sistema híbrido e avançado de **Assinatura de Objeto**. As etiquetas dependem agora de identificadores programáticos (UIA **AutomationId** ou Win32 **ControlID**) e de coordenadas relativas à janela, tornando as suas etiquetas personalizadas completamente resistentes ao redimensionamento de janelas, à movimentação, à mudança de monitor ou à alteração de escala.
- **Migração Automática e Transparente de Etiquetas**: A atualização é totalmente transparente. O extra migrará automaticamente as suas etiquetas antigas baseadas em coordenadas para o novo formato estável de impressão digital em segundo plano assim que focar o objeto pela primeira vez, com zero perda de dados.

## Alterações para 4.0.3

- **Apresentação da Etiquetagem Semântica por IA**: Os utilizadores podem agora etiquetar permanentemente botões e ícones sem nome utilizando a IA. Prima **L** para etiquetar o objeto de navegação atual (suportando tanto o foco do Tab como a navegação por objetos) ou **Shift+L** para analisar e etiquetar toda a aplicação de uma só vez.
- **Gestão Inteligente de Etiquetas**: Adicionada uma nova janela do Gestor de Etiquetas totalmente acessível (através de **Shift+L** se existirem etiquetas) para ver, renomear ou eliminar etiquetas personalizadas em lote.
- **Análise Direta de Ficheiros (Avanço da Janela de Ficheiros)**: O extra é agora inteligente o suficiente para detetar se está focado num ficheiro PDF ou de imagem no Explorador de Ficheiros do Windows. Premir **F (Ação de Ficheiro Inteligente)** ou **D (Leitor de Documentos)** num ficheiro selecionado processá-lo-á imediatamente, ignorando completamente a janela padrão "Abrir".

## Alterações para 4.0.1

- **Adicionado Motor OCR "Nenhum (Extrair Camada de Texto)"**: Os utilizadores podem agora extrair texto diretamente de PDFs pesquisáveis sem utilizar créditos de IA, melhorando significativamente a velocidade e a privacidade para documentos baseados em texto.
- **Precisão Refinada do Explorador de UI**: Melhorada a prompt do Explorador de UI para identificar melhor os tipos de elementos (como Itens de Lista) e relatar com precisão estados como "(Ativado)", "(Selecionado)" ou "(Expandido)", ignorando os componentes do sistema Windows como a Barra de Tarefas e o Relógio.
- **Lembrete de Configuração de Instalação**: Adicionada uma notificação após a instalação para guiar os utilizadores ao menu de definições para configurarem as suas chaves de API e preferências.

## Alterações para 3.6.0

- **Correção na Escrita do Operador de IA:** Corrigido um erro onde a letra 'v' era digitada em vez de colar o texto em determinados sistemas. Esta correção resolve conflitos de temporização que ocorriam durante uma carga elevada do sistema.
- **Estabilidade Melhorada:** Adicionada uma gestão de erros robusta para operações na área de transferência para evitar falhas do extra quando a área de transferência do sistema está temporariamente bloqueada por outras aplicações.
- **Otimização de Temporização:** Ajustados os atrasos internos para eventos de teclado de modo a garantir maior fiabilidade em diferentes velocidades do sistema e melhor compatibilidade com Gestores da Área de Transferência de terceiros.

## Alterações para 3.5.0

- **Operador de IA (Controlo Autónomo - Shift+A):** Esta é a joia da coroa da v5.5. O Vision Assistant Pro passou de um assistente passivo a o seu **Operador de IA** pessoal. Não se limita a descrever o ecrã — assume o comando.
  - _Como funciona:_ Pode agora dar instruções por texto/voz para operar o seu PC. Por exemplo, numa aplicação completamente inacessível onde o seu leitor de ecrã permanece em silêncio, pode premir **Shift+A** e escrever: _"Clica no botão Definições"_ ou _"Procura o campo de pesquisa, escreve 'Últimas Notícias' e prima Enter."_ A IA identifica visualmente os elementos, move o rato e executa a tarefa por si.
  - _Nota de Desempenho:_ Esta funcionalidade está otimizada para o **Gemini 3.0 Flash (Preview)**, oferecendo respostas incrivelmente rápidas e inteligentes que conseguem lidar até com as disposições de interface de utilizador mais complexas.
  - **⚠️ Aviso de Utilização de API:** Como o Operador de IA precisa de "ver" exatamente o que está a acontecer para ser preciso, envia uma captura de ecrã de alta resolução a cada passo. Tenha em conta que a utilização frequente consumirá a sua quota de API muito mais rapidamente do que as tarefas normais de texto.
- **Explorador Visual de UI (E):** Cansado de navegar por "botões sem etiqueta"? Prima **E** para ativar o Explorador de UI. A IA analisará toda a janela e gerará uma lista de cada elemento clicável que encontrar — incluindo ícones, gráficos e menus. Basta escolher um item da lista e o Operador de IA clicará nele por si. É como ter uma "camada acessível" sobre qualquer aplicação.
- **Ação de Ficheiro Inteligente com Sensibilidade ao Contexto (F):** A tecla "F" foi completamente reformulada. Já não assume que quer apenas OCR. Ao selecionar uma imagem, pergunta agora inteligentemente qual a sua intenção: pode escolher uma **Descrição Visual Detalhada** para compreender a cena ou uma **Extração de Texto Estruturado (OCR)** para leitura. O menu adapta-se dinamicamente com base no tipo de ficheiro e no seu motor de IA ativo.
- **Otimização Principal:** Realizámos uma limpeza profunda da lógica interna do extra, removendo funções legadas não utilizadas e código redundante. Isto resulta numa experiência mais leve, rápida e fiável para todos os utilizadores.

## Alterações para 3.1.0

- **Arquitetura Multiprovedor**: Adicionado suporte total para **OpenAI**, **Groq** e **Mistral**, em conjunto com o Google Gemini. Os utilizadores podem agora escolher a sua plataforma de IA preferida.
- **Encaminhamento Avançado de Modelos**: Os utilizadores de provedores nativos (Gemini, OpenAI, etc.) podem agora selecionar modelos específicos num menu suspenso para diferentes tarefas (OCR, STT, TTS).
- **Configuração Avançada de Pontos de Extremidade**: Os utilizadores de provedores personalizados podem introduzir manualmente URLs específicos e nomes de modelos para um controlo detalhado sobre servidores locais ou de terceiros.
- **Visibilidade Inteligente de Funcionalidades**: O menu de definições e a interface do Leitor de Documentos ocultam agora automaticamente as funcionalidades não suportadas (como o TTS) com base no provedor selecionado.
- **Obtenção Dinâmica de Modelos**: O extra obtém agora a lista de modelos disponíveis diretamente da API do provedor, garantindo compatibilidade com novos modelos assim que são lançados.
- **OCR e Tradução Híbridos**: Otimizada a lógica para utilizar o Google Tradutor para maior velocidade ao usar o OCR do Chrome, e tradução baseada em IA ao utilizar os motores Gemini/Groq/OpenAI.
- **"Analisar Novamente com IA" Universal**: A funcionalidade de reanalisar do Leitor de Documentos já não está limitada ao Gemini. Agora utiliza qualquer provedor de IA que esteja ativo no momento para reprocessar as páginas.

## Alterações para 3.0

- **Recuperação Interativa de Resultados:** Adicionada a tecla **Espaço** à camada de comandos, permitindo aos utilizadores reabrir instantaneamente a última resposta da IA numa janela de conversa para perguntas adicionais, mesmo quando o modo "Saída Direta" está ativo.
- **Central da Comunidade no Telegram:** Adicionada uma ligação para o "Canal Oficial no Telegram" no menu Ferramentas do NVDA, proporcionando uma forma rápida de se manter atualizado com as últimas notícias, funcionalidades e lançamentos.
- **Estabilidade de Resposta Melhorada:** Otimizada a lógica principal para as funcionalidades de Tradução, OCR e Visão para garantir um desempenho mais fiável e uma experiência mais fluida ao utilizar a saída direta por voz.
- **Orientação de Interface Melhorada:** Atualizadas as descrições de definições e documentação para explicar melhor o novo sistema de recuperação de histórico e como funciona juntamente com as definições de saída direta.

## Alterações para 2.9

- **Gestor Avançado de Prompts:** Introduzida uma janela de gestão dedicada nas definições para personalizar as prompts padrão do sistema e gerir prompts definidas pelo utilizador, com suporte total para adicionar, editar, reordenar e pré-visualizar.
- **Suporte Abrangente a Proxy:** Resolvidos problemas de ligação à rede garantindo que as definições de proxy configuradas pelo utilizador são rigorosamente aplicadas a todos os pedidos de API, incluindo tradução, OCR e geração de voz.
- **Migração Automática de Dados:** Integrado um sistema de migração inteligente para atualizar automaticamente configurações de prompts antigas para um formato JSON v2 robusto logo na primeira execução, sem perda de dados.
- **Compatibilidade Atualizada (2025.1):** Definida a versão mínima do NVDA requerida para 2025.1 devido a dependências de bibliotecas em funcionalidades avançadas como o Leitor de Documentos, garantindo um desempenho estável.
- **Interface de Definições Otimizada:** Simplificada a interface de definições ao reorganizar a gestão de prompts numa janela separada, proporcionando uma experiência de utilização mais limpa e acessível.
- **Guia de Variáveis de Prompt:** Adicionado um guia integrado dentro das janelas de prompt para ajudar os utilizadores a identificar e utilizar facilmente variáveis dinâmicas como [selection], [clipboard] e [screen_obj].

## Alterações para 2.8

- **Resiliência de Rede Melhorada:** Adicionado um mecanismo de nova tentativa automática para lidar melhor com ligações de Internet instáveis e erros temporários do servidor, garantindo respostas de IA mais fiáveis.
- **Janela de Tradução Visual:** Introduzida uma janela dedicada para os resultados de tradução. Os utilizadores podem agora navegar facilmente e ler traduções longas linha a linha, de forma semelhante aos resultados de OCR.
- **Vista Formatada Agregada:** A funcionalidade "Ver Formatado" no Leitor de Documentos apresenta agora todas as páginas processadas numa única janela organizada, com cabeçalhos de página claros.
- **Fluxo de Trabalho de OCR Otimizado:** Ignora automaticamente a seleção de intervalo de páginas para documentos de página única, tornando o processo de reconhecimento mais rápido e fluido.
- **Estabilidade de API Melhorada:** Alterado para um método de autenticação baseado em cabeçalho mais robusto, resolvendo potenciais erros de "Todas as chaves de API falharam" causados por conflitos na rotação de chaves.
- **Correção de Erros:** Resolvidas várias falhas potenciais, incluindo um problema durante o encerramento do extra e um erro de foco na janela de conversa.

## Alterações para 6.5.0

- **Leitor Avançado de Documentos:** Um novo e potente visualizador de PDF e imagens com seleção de intervalo de páginas, processamento em segundo plano e navegação fluida com `Ctrl+PageUp/PageDown`.
- **Novo Submenu de Ferramentas:** Adicionado um submenu dedicado "Vision Assistant" no menu Ferramentas do NVDA para um acesso mais rápido às funcionalidades principais, definições e documentação.
- **Personalização Flexível:** Pode agora escolher o seu motor de OCR e voz TTS preferidos diretamente no painel de definições.
- **Suporte a Múltiplas Chaves de API:** Adicionado suporte para várias chaves de API do Gemini. Pode introduzir uma chave por linha ou separá-las por vírgulas nas definições.
- **Motor OCR Alternativo:** Introduzido um novo motor de OCR para garantir o reconhecimento de texto fiável mesmo ao atingir os limites de quota da API do Gemini.
- **Rotação Inteligente de Chaves de API:** Muda automaticamente para a chave de API funcional mais rápida e memoriza-a para ultrapassar os limites de quota.
- **Documento para MP3/WAV:** Capacidade integrada para gerar e guardar ficheiros de áudio de alta qualidade em formatos MP3 (128kbps) e WAV diretamente dentro do leitor.
- **Suporte a Histórias do Instagram:** Adicionada a capacidade de descrever e analisar Histórias do Instagram utilizando os seus URLs.
- **Suporte ao TikTok:** Introduzido suporte para vídeos do TikTok, permitindo uma descrição visual completa e transcrição de áudio dos vídeos.
- **Janela de Atualização Redesenhada:** Apresenta uma nova interface acessível com uma caixa de texto com deslocamento para ler claramente as alterações de versão antes de instalar.
- **Estado e Experiência Unificados:** Janelas de ficheiro padronizadas em todo o extra e melhoria do comando 'L' para reportar o progresso em tempo real.

## Alterações para 2.6

- **Sistema de Ajuda:** Adicionado um comando de ajuda (`H`) na Camada de Comandos para disponibilizar uma lista de fácil acesso com todos os atalhos e as suas respetivas funções.
- **Análise de Vídeos Online:** Expandido o suporte para incluir vídeos do **Twitter (X)**. Também foi melhorada a deteção de URLs e a estabilidade para uma experiência mais fiável.
- **Contribuição para o Projeto:** Adicionada uma janela opcional de doação para utilizadores que desejem apoiar as futuras atualizações e o crescimento contínuo do projeto.

## Alterações para 2.5

\*   \*\*Camada de Comandos:\*\* Introduzido um sistema de Camada de Comandos (predefinição: `NVDA+Shift+V`) para agrupar atalhos sob uma única tecla principal. Por exemplo, em vez de premir `NVDA+Control+Shift+T` para traduzir, passa a premir `NVDA+Shift+V` seguido de `T`.
\*   \*\*Análise de Vídeos Online:\*\* Adicionada uma nova funcionalidade para analisar vídeos do YouTube e Instagram diretamente através do fornecimento de um URL.

## Alterações para 2.1.1

- **Modo de Saída Direta:** Adicionada uma opção para ignorar a janela de conversa e ouvir as respostas da IA diretamente por voz, proporcionando uma experiência mais rápida e fluida.
- **Integração com a Área de Transferência:** Adicionada uma nova definição para copiar automaticamente as respostas da IA para a área de transferência.

## Alterações para 2.1

- **Novos Idiomas:** Adicionadas traduções para **Persa** e **Vietnamita**.
- **Modelos de IA Expandidos:** Reorganizada a lista de seleção de modelos com prefixos claros (`[Free]`, `[Pro]`, `[Auto]`) para ajudar os utilizadores a distinguir entre modelos gratuitos e modelos com limite de utilização (pagos). Adicionado suporte para o **Gemini 3.0 Pro** e **Gemini 2.0 Flash Lite**.
- **Estabilidade do Ditado:** Melhoria significativa na estabilidade do Ditado Inteligente. Adicionada uma verificação de segurança para ignorar clipes de áudio com menos de 1 segundo, evitando alucinações da IA e erros de resposta em branco.
- **Gestão de Ficheiros:** Corrigido um problema em que o envio de ficheiros com nomes em carateres não-ingleses falhava.
- **Otimização de Prompts:** Melhorada a lógica de Tradução e a estrutura dos resultados de Visão.

## Alterações para 2.0

- **Adicionadas traduções para Francês e Turco.**
- **Vista Formatada:** Adicionado o botão "Ver Formatado" nas janelas de conversa para visualizar a conversação com a devida formatação (Cabeçalhos, Negrito, Código) numa janela navegável padrão.
- **Definição de Markdown:** Adicionada a nova opção "Limpar Markdown na Conversa" nas Definições. Desativar esta opção permite aos utilizadores verem a sintaxe Markdown pura (ex.: `**`, `#`) na janela de conversa.
- **Gestão de Janelas:** Corrigido um problema em que as janelas de "Refinar Texto" ou de conversa abriam múltiplas vezes ou falhavam ao colocar o foco corretamente.
- **Melhorias de Experiência de Utilizador:** Padronizados os títulos das janelas de ficheiros para "Abrir" e removidos anúncios de voz redundantes (ex.: "A abrir menu...") para uma navegação mais fluida.

## Alterações para 1.5

- Adicionada tradução para Italiano.
- **Relatório de Estado:** Adicionado um novo comando (NVDA+Control+Shift+I) para anunciar o estado atual do extra (ex.: "A enviar...", "A analisar...").
- **Exportação em HTML:** O botão "Guardar Conteúdo" nas janelas de resultados guarda agora a saída como um ficheiro HTML formatado, preservando estilos como cabeçalhos e texto em negrito.
- **Interface de Definições:** Melhorada a disposição do painel de Definições com agrupamentos acessíveis.
- **Novos Modelos:** Adicionado suporte para gemini-flash-latest e gemini-flash-lite-latest.
- **Idiomas:** Adicionado o Nepalês à lista de idiomas suportados.
- **Lógica do Menu de Refinamento:** Corrigido um erro crítico em que os comandos de "Refinar Texto" falhavam se o idioma da interface do NVDA não fosse o Inglês.
- **Ditado:** Melhorada a deteção de silêncio para evitar a geração de texto incorreto quando não há entrada de voz.
- **Definições de Atualização:** A opção "Procurar atualizações ao iniciar" está agora desativada por predefinição para cumprir as políticas da Loja de Extras do NVDA.
- Limpeza de Código.

## Alterações para 1.0

- Migrada a estrutura do projeto para o modelo oficial de extras da NV Access para melhor conformidade com os padrões.
- Implementada lógica de nova tentativa automática para erros HTTP 429 (Limite de Taxa Excedido) para garantir a fiabilidade durante períodos de tráfego elevado.
- Otimizadas as prompts de tradução para maior precisão e melhor gestão da lógica de "Troca Inteligente".
- Atualizada a tradução para Russo.

## Alterações para 6.0

- Adicionado suporte à tradução em Russo (Agradecimentos a nvda-ru).
- Atualizadas as mensagens de erro para fornecer informações mais descritivas relativamente à conetividade.
- Alterado o idioma de destino predefinido para Inglês.

## Alterações para 5.6

- Adicionado o Comando de OCR de Ficheiro Nativo (NVDA+Control+Shift+F).
- Adicionado o botão "Guardar Conversa" às janelas de resultados.
- Implementado suporte completo de internacionalização (i18n).
- Migrado o feedback sonoro para o módulo nativo de tons do NVDA.
- Alterado para a API de Ficheiros do Gemini para um melhor manuseamento de ficheiros PDF e de áudio.
- Corrigida uma falha no sistema ao traduzir texto que contivesse chavetas.

## Alterações para 2026.10.01

- Corrigido um problema em que a variável [file_ocr] não funcionava corretamente dentro das Prompts Personalizadas.

## Alterações para 2026.09.01

- Padronizados todos os atalhos para utilizar NVDA+Control+Shift de modo a eliminar conflitos com a disposição para Portátil do NVDA e teclas de atalho do sistema.

## Alterações para 2.7

- Implementado um sistema integrado de Atualização Automática.
- Adicionada a Cache de Tradução Inteligente para recuperação instantânea de texto traduzido anteriormente.
- Adicionada Memória de Conversação para refinar contextualmente os resultados nas janelas de conversa.
- Adicionado comando dedicado para Tradução da Área de Transferência (NVDA+Control+Shift+Y).
- Otimizadas as prompts da IA para impor rigorosamente a saída no idioma de destino.
- Corrigida uma falha causada por carateres especiais no texto de entrada.

## Alterações para 6.1.2

- Adicionado suporte para mais de 20 novos idiomas.
- Implementada a Janela Interativa de Refinamento para perguntas adicionais.
- Adicionada a funcionalidade nativa de Ditado Inteligente.
- Adicionada a categoria "Vision Assistant" à janela de Gestos de Entrada do NVDA.
- Corrigidas falhas por COMError em aplicações específicas como o Firefox e o Word.
- Adicionado mecanismo de nova tentativa automática para erros do servidor.

## Alterações para 7.0.0

- Lançamento inicial.
