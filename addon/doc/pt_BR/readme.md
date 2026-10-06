# Documentação do Vision Assistant Pro

<!-- DOWNLOAD_COUNT_START --> Total de downloads: 75.451 <!-- DOWNLOAD_COUNT_END -->

O **Vision Assistant Pro** é um assistente de IA multimodal avançado para o NVDA. Ele utiliza motores de IA de classe mundial para oferecer leitura de tela inteligente, tradução, ditado por voz e análise de documentos.

_Este complemento foi disponibilizado à comunidade em homenagem ao Dia Internacional das Pessoas com Deficiência._

## 1. Configuração e Instalação

Acesse o **Menu do NVDA > Preferências > Configurações > Vision Assistant Pro**. A caixa de diálogo de configurações está organizada em 9 abas acessíveis: **Conexão**, **Assistente ao Vivo**, **Comportamento da IA**, **Idiomas de Tradução**, **Leitor de Documentos**, **Vídeo**, **CAPTCHA**, **Prompts** e **Avançado**.

### 1.1 Aba Conexão

- **Provedor:** Selecione o seu serviço de IA preferido. Os provedores suportados incluem **Google Gemini**, **OpenAI**, **Mistral**, **Groq**, **MiniMax** e **Personalizado** (servidores compatíveis com a OpenAI, como Ollama, LM Studio, Jan.ai ou KoboldCPP).
- **Chave da API:** Insira uma ou mais chaves de API (separadas por vírgulas ou quebras de linha) para rotação automática.
- **Obter Modelos:** Pressione este botão após inserir sua chave de API para baixar a lista de modelos mais recente disponível no provedor.
- **Modelo de IA:** Selecione o modelo principal utilizado para bate-papo geral e análise.
- **Roteamento Avançado de Modelos (Específico por Tarefa):** Opcionalmente, selecione modelos dedicados nos menus suspensos para tarefas de OCR, STT, TTS, Operador de IA, Vídeo e Assistente ao Vivo. Para o Gemini, os modelos são categorizados dinamicamente por capacidade, sem poluição visual.
- **Configurações de Provedor Personalizado:** Configure pontos de extremidade (endpoints) locais ou personalizados. Inclui **Configurar IA Local** (configuração com um clique para Ollama, LM Studio, Jan.ai ou KoboldCPP) e **Configuração Avançada de Endpoint**.
- **Configuração de Proxy:** Suporte completo para tunelamento e redirecionamento de endpoints em todo o add-on (incluindo o Assistente ao Vivo, Observador Ambiente e TTS). Insira a sua **URL do Proxy** e selecione o seu **Modo de Proxy**:
  - **Detecção automática:** Detecta automaticamente se a URL é um proxy direto (forward proxy) ou um proxy reverso (reverse proxy).
  - **Proxy SOCKS5:** Força o tunelamento direto via SOCKS5 com autenticação de usuário/senha da RFC 1929 e resolução de nomes de domínio.
  - **Proxy HTTP:** Força o tunelamento direto via proxy HTTP com autenticação Básica (Basic).
  - **Proxy Reverso:** Substituição direta de endpoint para gateways de IA personalizados e espelhos (mirrors) auto-hospedados (as credenciais são desativadas neste modo).
- **Testar Conexão de Proxy:** Um botão não bloqueante que testa a conectividade e mede a latência do servidor em milissegundos (anunciada via NVDA).
- **Opções de Conexão e Saída:** Configure a URL do Proxy, verificação de atualizações ao iniciar, Limpar Markdown no Bate-Papo, Copiar respostas da IA para a área de transferência e Saída Direta (Sem Janela de Bate-Papo).
- **Salvar conversas no histórico:** Mantenha suas conversas no histórico.

### 1.2 Aba Assistente ao Vivo

- **Assistente ao Vivo: Saída Direta (Sem Janela):** Inicia o Assistente ao Vivo sem a janela de conversa; abra-a mais tarde com a tecla de Chamar Último Resultado (`Espaço`).
- **Pressionar para Falar:** Alterna o modo pressionar para falar. Quando ativado, o microfone envia áudio apenas enquanto você mantém a tecla atribuída pressionada.
- **Tecla Pressionar para Falar:** Pressione as teclas para gravar o atalho (por exemplo `F12` ou `Ctrl+F12`) — você pode até atribuir uma tecla modificadora isolada, como `Ctrl Esquerdo`. Mantenha a tecla pressionada para falar e solte-a para finalizar; um sinal sonoro curto confirma cada toque e liberação.

Nota: Esta aba aparece apenas quando o **Google Gemini** (ou um provedor Personalizado compatível com o Gemini) estiver ativo.

### 1.3 Aba Comportamento da IA

- **Criatividade (Temperatura):** Controla a aleatoriedade e criatividade da IA (de 0,0 a 2,0). Valores mais baixos produzem resultados de tradução e OCR mais determinísticos e precisos.

### 1.4 Aba Idiomas de Tradução

- **Idioma de Origem:** Selecione seu idioma de entrada padrão.
- **Idioma de Destino:** Selecione seu idioma principal de tradução.
- **Idioma de Resposta da IA:** Selecione o idioma para as respostas gerais da IA.
- **Troca Inteligente:** Alterna automaticamente os idiomas de origem e destino com base no texto detectado.

### 1.5 Aba Leitor de Documentos

- **Mecanismo de OCR:** Escolha entre **Chrome (Rápido)** para resultados rápidos ou **IA (Avançado)** para superior preservação de layout.
- **Tamanho do Lote do OCR:** Especifique o número de páginas por solicitação (defina como 0 para processamento em uma única solicitação).
- **Descrever Imagens Inline:** Alterna as descrições de imagens no próprio texto durante a extração do documento.
- **Exportar Números de Página:** Alterna a inclusão de números de página e separadores na saída de documentos com várias páginas.
- **Voz TTS:** Selecione o estilo de voz padrão para a geração de áudio.
- **Salvar documentos no histórico:** Mantenha os documentos abertos na lista do histórico; o texto OCR em cache e os dados de retomada ainda são salvos.

### 1.6 Aba Vídeo

- **Tamanho do Bloco de Vídeo:** Duração dos segmentos em minutos para a geração de Audiodescrição (defina como 0 para processar o arquivo inteiro).
- **Adicionar Lista de Personagens:** Opção para adicionar um dicionário de personagens como a primeira entrada de legenda.
- **Adicionar Aviso de IA:** Opção para inserir um aviso sobre o uso de IA no início das legendas SRT do vídeo.
- **Dicionário de personagens e gerenciamento de séries:** Adicione, edite, importe ou gerencie nomes de personagens, descrições físicas e papéis por série — a IA associa automaticamente os personagens encontrados ao seu dicionário e mescla novos conforme você analisa mais episódios. Suas notas manuais são sempre preservadas com prioridade sobre as atualizações da IA, enquanto as descrições físicas permanecem atualizadas ao longo dos episódios.

### 1.7 Aba CAPTCHA

- **Ativar Resolução Visual de CAPTCHA:** Alterna a resolução automática de desafios visuais (hCaptcha, reCAPTCHA).
- **Método de CAPTCHA de Texto:** Escolha entre capturar o **Objeto do Navegador** ou a **Tela Inteira**.

### 1.8 Aba Prompts

- **Gerenciar Prompts:** Abre uma caixa de diálogo dedicada para personalizar os prompts padrão do sistema ou criar, editar, reordenar e pré-visualizar prompts personalizados do usuário com variáveis dinâmicas (ex.: `[selection]`, `[screen_fg_obj]`).
- **Atalhos de Prompts Personalizados:** Atribua uma tecla de atalho dedicada a qualquer prompt personalizado diretamente no Gerenciador de Prompts. Pressione as teclas para gravá-las — teclas únicas são executadas dentro da Camada de Comandos (e globalmente como `NVDA + Shift + tecla`), enquanto combinações como `Control + Shift + 1` são executadas globalmente de forma independente.
- **Comportamento de Feedback por Prompt:** Escolha como cada prompt exibe seu resultado individualmente (Configuração global, Copiar para a área de transferência, Saída direta / Mensagem do NVDA, Copiar para a área de transferência + Saída direta, ou Janela de chat).

### 1.9 Aba Avançado e Log Global

Navegue até a aba **Avançado** para configurar o log global de eventos do complemento:

- **Ativar arquivo de log dedicado:** Alterna o registro de todos os eventos operacionais, tráfego da API e erros de todos os módulos do complemento em um arquivo separado (`vision_assistant.log`).
- **Nível do Log:** Selecione o nível de detalhe entre **Depuração (Todos os Detalhes)**, **Informação (Informação Geral)**, **Aviso (Apenas Avisos)** e **Erro (Apenas Erros)**.
- **Manter Logs Durante:** Defina períodos de retenção automática para limpar registros antigos automaticamente (variando de 1 hora a 90 dias).
- **Controles de Gerenciamento de Logs:** Use **Abrir Arquivo de Log**, **Abrir Pasta de Logs** ou **Limpar Arquivo de Log** para inspecionar ou apagar dados de log diretamente, sem reiniciar o NVDA ou interferir com os logs padrão do NVDA.
- **Diretório de dados unificado:** Todos os arquivos de dados do complemento (histórico, séries, rótulos, progresso do OCR, caches e logs) são armazenados em uma única pasta `VisionAssistant` dentro do seu diretório de configuração do NVDA — mantendo tudo organizado e tornando os backups manuais muito fáceis.

### 1.10 Backup e Restauração de Configurações

A aba **Avançado** também inclui uma seção de **Backup e Restauração**:

- **Backup:** Salva sua configuração em um único arquivo JSON. Ao clicar, você escolhe o que incluir: **Tudo** (configurações, etiquetas personalizadas, progresso do OCR e histórico) ou **Apenas Configurações**.
- **Restaurar:** Carrega um backup salvo anteriormente para restaurar sua configuração e dados a qualquer momento, em qualquer máquina ou após reinstalar o NVDA. Você deverá confirmar primeiro, pois a restauração substitui todas as suas configurações e dados atuais.

## 2. Gerenciador de Chaves de API Gemini

Criar uma chave de API do Gemini no **aistudio.google.com** costumava ser a etapa mais difícil do add-on. Com um leitor de telas as páginas eram confusas, e algumas pessoas simplesmente não conseguiam criar uma chave de jeito nenhum. O **Gerenciador de Chaves de API do Gemini** resolve esse problema. Pressione **G** na Camada de Comandos, ou abra **Menu NVDA > Preferências > Configurações > Assistente de Visão > Conexão** e pressione **Obter uma Chave de API do Gemini...**.

- **Acessando a conta:** Ao abrir o gerenciador, o seu navegador padrão é aberto diretamente na página de login seguro do Google. Faça login com a sua conta do Google — não são necessárias ferramentas externas, SDKs ou configurações de linha de comando. A conta na qual você está conectado é sempre exibida no botão **Sair da conta**.
- **Criando uma chave:** Após fazer login, você pode criar uma chave imediatamente com **Novo Projeto e Chave**, sem nenhuma configuração prévia. Se você já possui projetos existentes, eles aparecem em uma lista simples na qual você pode selecionar um e pressionar **Criar Chave para o Projeto Selecionado**.
- **O que acontece a seguir:** A nova chave é copiada diretamente para a área de transferência, salva dentro do add-on para uso posterior, e você é perguntado uma vez se deseja adicioná-la à lista de chaves do add-on. Isso é tudo o que você precisa — sem páginas da web para procurar.
- **Trabalhando com suas chaves:** **Copiar Chave do Projeto Selecionado** copia a chave do projeto que você selecionou, **Copiar Última Chave Criada** copia a chave que você acabou de criar e **Exportar Chaves Salvas para CSV...** salva tudo o que você criou em um arquivo.
- **Excluindo uma chave:** **Excluir uma Chave...** exibe as chaves existentes no projeto selecionado, pergunta qual você deseja remover e pede confirmação antes de excluir. Excluir uma chave também a remove da lista de chaves do add-on, para que nenhuma chave inválida seja deixada na rotação. Chaves criadas fora do add-on também podem ser excluídas, desde que sua conta tenha permissão nesse projeto.
- **Saindo da conta:** **Sair da conta** remove as informações de login armazenadas no seu computador, para que você possa alternar para outra conta sempre que quiser.

## 3. Camada de Comandos e Atalhos

Para evitar conflitos de teclado, este complemento utiliza uma **Camada de Comandos**.

1. Pressione **NVDA + Shift + V** (Tecla Mestra) para ativar a camada (você ouvirá um sinal sonoro).
2. Solte as teclas e, em seguida, pressione uma das seguintes teclas individuais:

| Tecla                  | Função                                  | Descrição                                                                                                                                                                                                                                                             |
| ---------------------- | --------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Shift + A**          | **Operador de IA**                      | **Operação Autônoma:** Peça à IA para realizar uma tarefa na tela. Pressionar novamente aborta instantaneamente as operações ativas.                                                                                  |
| **E**                  | **Explorador de UI**                    | **Clique Interativo:** Identifica e clica em elementos da interface em qualquer aplicativo.                                                                                                                                           |
| **T**                  | Tradutor Inteligente                    | Traduz o texto sob o cursor de navegação ou seleção.                                                                                                                                                                                                  |
| **Shift + T**          | Tradutor da Área de Transferência       | Traduz o conteúdo atualmente na área de transferência.                                                                                                                                                                                                |
| **R**                  | Refinador de Texto                      | Resumir, Corrigir Gramática, Explicar ou executar **Prompts Personalizados**.                                                                                                                                                                         |
| **V**                  | Visão do Objeto                         | Descreve o objeto de navegação atual.                                                                                                                                                                                                                 |
| **O**                  | Visão de Tela Inteira                   | Analisa o layout e o conteúdo de toda a tela.                                                                                                                                                                                                         |
| **Shift + V**          | Análise de Vídeo                        | Analisa arquivos de vídeo locais ou vídeos online do **YouTube**, **Instagram**, **TikTok** ou **Twitter (X)**.                                                                                                                    |
| **Control + V**        | Gravação de Vídeo Local                 | Grava um vídeo silencioso da sua tela e analisa as ações e o layout.                                                                                                                                                                                  |
| **D**                  | Leitor de Documentos                    | Leitor avançado para PDF, imagens e arquivos de texto simples/HTML com seleção de intervalo de páginas.                                                                                                                                               |
| **F**                  | **Ação de Arquivo Inteligente**         | Reconhecimento sensível ao contexto de arquivos de imagem, PDF ou TIFF selecionados.                                                                                                                                                                  |
| **M**                  | Transcrição e Dublagem de Mídia         | Transcreve ou dubla arquivos de áudio/vídeo (MP3, WAV, MP4, etc.) para o seu idioma de destino.                                                                                                                    |
| **C**                  | Solucionador de CAPTCHA                 | Captura e resolve CAPTCHAs.                                                                                                                                                                                                                           |
| **Shift + C**          | Chat direto                             | Abre uma interface de bate-papo por texto direta com a IA.                                                                                                                                                                                            |
| **S**                  | Ditado Inteligente                      | Converte voz em texto. Pressione para iniciar a gravação e novamente para parar/digitar.                                                                                                                                              |
| **Control+T**          | Tradução por Voz                        | Transcreve, traduz e digita o resultado com base nas suas configurações de idioma.                                                                                                                                                                    |
| **Control+L**          | **Assistente ao Vivo**                  | **Copiloto em Tempo Real (Apenas Gemini):** Inicia ou encerra uma conversa de voz e tela ao vivo com o assistente de IA.                                                                                           |
| **Control+A**          | **Operador em Tempo Real**              | **Controle Autônomo do Computador (somente Gemini):** Inicia ou encerra uma sessão de operador ao vivo para delegar tela e ações à IA.                                                                             |
| **G**                  | **Gerenciador de Chaves de API Gemini** | **Crie sua chave de API sem a web (somente Gemini):** Abre o gerenciador que configura o que seu computador precisa, abre o navegador para fazer login e cria, copia ou exclui uma chave para o projeto escolhido. |
| **I**                  | Relatório de Status                     | Anuncia o progresso atual (por exemplo, "Verificando...", "Ocioso").                                                                                                               |
| **L**                  | **Rotular Objeto**                      | **Rotulagem Semântica por IA:** Rotula permanentemente o objeto do navegador ou ícone com foco atual.                                                                                                                                 |
| **Shift + L**          | **Gerenciar/Examinar Rótulos**          | Abre o Gerenciador de Rótulos (se existirem) ou examina o aplicativo em busca de elementos não rotulados.                                                                                                                          |
| **U**                  | Verificar Atualizações                  | Verifica manualmente no GitHub a versão mais recente do complemento.                                                                                                                                                                                  |
| **Espaço**             | Relembrar Último Resultado              | Exibe a última resposta da IA em um diálogo de bate-papo para revisão ou continuação.                                                                                                                                                                 |
| **H**                  | Ajuda dos Comandos                      | Exibe uma lista de todos os atalhos disponíveis.                                                                                                                                                                                                      |
| **Control + H**        | **Histórico**                           | Abre o diálogo de Histórico listando seus bate-papos e documentos anteriores com filtros de tipo e opções de exclusão/limpeza.                                                                                                                        |
| **Alt + S**            | Configurações                           | Abre o diálogo de configurações do Vision Assistant Pro.                                                                                                                                                                                              |
| **Alt + Q**            | Relatório de Chaves com Cota Esgotada   | Informa o número de chaves de API Gemini que excederam sua cota diária, quais modelos foram afetados e seu tempo de redefinição.                                                                                                                      |
| **Alt + M**            | Auditoria de Roteamento                 | Informa os modelos de IA selecionados atualmente no roteamento avançado para tarefas especializadas (ignorando os padrões).                                                                                                        |
| **Cima / Baixo**       | Navegação pelas Configurações Rápidas   | Navega entre as categorias de configurações rápidas (Provedor, Modelo, Saída)... na camada.                                                                                        |
| **Esquerda / Direita** | Alterar Configuração Rápida             | Altera o valor da configuração rápida atualmente selecionada.                                                                                                                                                                                         |

## 4. Bate-Papo e Histórico

As janelas de bate-papo e a caixa de diálogo do Histórico funcionam em todos os recursos, permitindo que você revise conversas e continue exatamente de onde parou.

### 3.1 Atalhos da Janela de Bate-Papo

Quando uma janela de bate-papo estiver aberta (Bate-Papo Direto, bate-papo de documento, refinamento e similares), você poderá revisar a conversa com:

- **Alt + Seta para Baixo:** Lê a próxima mensagem.
- **Alt + Seta para Cima:** Lê a mensagem anterior.
- **Alt + C:** Copia a mensagem atual.

### 3.2 Histórico (Control + H)

Pressione **Control + H** na Camada de Comandos para abrir a janela de **Histórico** com suas conversas e documentos anteriores, com opção de filtragem por tipo (Tudo / Conversas / Documentos). Abra uma conversa para continuar de onde parou — incluindo seus arquivos anexados, que são reanexados automaticamente — ou abra um documento e continue lendo. Pressione **Delete** em qualquer item para removê-lo, ou **Limpar tudo** para esvaziar a lista. Para documentos, a tecla Delete pergunta se você deseja remover apenas a entrada do histórico ou também limpar o texto do OCR em cache desse documento, para que a próxima abertura o analise novamente do zero — com uma opção **Não perguntar novamente** para lembrar sua escolha.

Você também pode escolher o que a lista armazena. **Salvar conversas no histórico** (aba Conexão) e **Salvar documentos no histórico** (aba Leitor de Documentos) vêm ativados por padrão, e ambos podem ser alternados nas Configurações Rápidas. A opção de documentos afeta apenas a entrada no Histórico — o texto OCR em cache e os dados de retomada são sempre mantidos.

## 5. Operador de IA - Controle Autônomo do Computador

O **Operador de IA** transforma o Vision Assistant Pro de um leitor passivo em um assistente ativo capaz de interagir com o seu computador em seu nome. Você pode pedir a ele para descrever a tela, responder a perguntas sobre o que vê ou até mesmo assumir o controle — clicando em botões, arrastando itens, digitando textos e navegando pelos aplicativos usando comandos em linguagem natural.

A maior vantagem? Funciona perfeitamente em softwares completamente inacessíveis. Se você estiver preso em um aplicativo personalizado, em uma área de trabalho remota ou em um site onde o seu leitor de tela fica totalmente silencioso, o operador não se importa. Como ele "vê" a tela visualmente, consegue encontrar, ler e interagir com elementos que não possuem nenhuma etiqueta de acessibilidade.

### 4.1 Como Funciona

1. Pressione **NVDA + Shift + V** e, em seguida, pressione **Shift + A** (ou use o atalho direto) para abrir a caixa de diálogo do Operador de IA.
2. Digite o que deseja fazer em linguagem simples (ex.: "Clique no botão Salvar", "O que diz a mensagem de erro?" ou "Renomeie o arquivo para final.pdf").
3. A IA analisará sua tela, identificará os elementos relevantes e executará a ação ou fornecerá a resposta. Se uma tarefa exigir várias etapas, o operador continuará trabalhando até que esteja concluída.
4. Pressione **Shift + A** novamente a qualquer momento para abortar instantaneamente uma operação em andamento.

### 4.2 Ações Suportadas

O operador compreende uma ampla variedade de comandos:

- **Descrever e Responder**: "Descreva o layout da tela" ou "O que diz a mensagem de erro?"
- **Clique**: "Clique no botão Salvar"
- **Clique com Botão Direito**: "Clique com o botão direito no arquivo"
- **Duplo Clique**: "Dê um duplo clique no documento"
- **Arrastar e Soltar**: "Arraste o documento para a pasta Arquivo"
- **Digitar**: "Digite 'Olá Mundo' na caixa de pesquisa"
- **Rolar (Scroll)**: "Role para baixo três vezes"
- **Pressionar Tecla**: "Pressione Enter", "Pressione Tab", "Pressione Esc"
- **Tarefas de Múltiplas Etapas**: "Abra o Explorador de Arquivos, encontre o relatório e renomeie-o para final.pdf"

### 4.3 Notas Importantes

- **⚠️ Aviso de Uso da API**: Como o operador precisa "ver" exatamente o que está acontecendo na tela, ele envia uma captura de tela em alta resolução a cada etapa. O uso frequente consumirá sua cota de API muito mais rápido do que os recursos padrão baseados em texto.
- **Aplicativos com Privilégios de Administrador**: Se o NVDA não estiver sendo executado com privilégios de Administrador, o operador pode não conseguir interagir com janelas que exijam permissões elevadas. Essa é uma limitação de segurança do Windows e não um erro do complemento.
- **Melhores Práticas**: Para obter os melhores resultados, dê comandos claros e específicos. "Clique no botão azul Enviar na parte inferior do formulário" quase sempre funcionará melhor do que apenas "Clique no botão".

### 4.4 Operador em Tempo Real (Control+A)

O Assistente em Tempo Real transforma o Vision Assistant Pro em um copiloto interativo em tempo real.
_(Nota: Este recurso é exclusivo do Google Gemini e de provedores Personalizados compatíveis com o Gemini)._

- **Ativação:** Pressione **Control+A** na Camada de Comandos para iniciar uma sessão do operador ao vivo; pressione novamente para encerrá-la.
- **Como funciona:** Pergunte em linguagem simples, por exemplo "abra o Chrome e pesquise por um site" ou "renomeie este arquivo para final". O operador analisa a tela, executa as etapas uma a uma e continua trabalhando em solicitações de várias etapas até que a tarefa seja concluída.
- **Anúncios:** Cada etapa é falada pela própria voz do Assistente ao Vivo, e ele informa quando a tarefa for concluída ou o motivo pelo qual não pôde ser realizada.
- **CAPTCHA:** Se um CAPTCHA aparecer, o operador tenta primeiro o seu **solucionador de CAPTCHA** integrado; se não conseguir resolvê-lo, ele pede que você mesmo conclua o desafio acessível.
- **Interrupção:** Pressione **Parar ação do operador** na janela do Assistente ao Vivo para cancelar a tarefa atual.
- **Configurações:** A própria instrução do operador pode ser editada no Gerenciador de Prompts (seção **Ao Vivo**, **Instrução do Operador Ao Vivo**). A opção **Saída Direta ao Vivo (Sem Janela)** também está disponível nas Configurações Rápidas.

## 6. Análise de Vídeo e Audiodescrição

> **Nota:** Os recursos de Análise de Vídeo e Audiodescrição são executados estritamente pelo provedor **Google Gemini**. Certifique-se de que o seu provedor ativo nas configurações do complemento esteja definido como Google Gemini.

O Vision Assistant Pro introduz recursos poderosos de processamento de vídeo projetados especificamente para usuários cegos. Ele pode analisar tanto vídeos online quanto gravações de tela locais para fornecer descrições visuais altamente detalhadas e gerar roteiros profissionais de Audiodescrição (SRT).

### 5.1 Gravação de Tela Local (Control + V)

Se você encontrar um vídeo silencioso, uma animação ou um tutorial em sua tela, pode capturá-lo diretamente:

1. Pressione **NVDA + Shift + V** para entrar na Camada de Comandos e, em seguida, pressione **Control + V**.
2. O complemento gravará sua tela silenciosamente em segundo plano.
3. Pressione **Control + V** novamente para parar a gravação.
4. A IA analisará o segmento de vídeo gravado e fornecerá uma descrição altamente detalhada da cena, dos personagens e das ações.

### 5.2 Análise de Vídeo (Shift + V)

Você pode analisar tanto arquivos de vídeo locais quanto vídeos online. Basta selecionar um arquivo de vídeo local no Explorador de Arquivos do Windows ou copiar um link de vídeo online para a área de transferência. Você também pode pressionar **Shift + V** em qualquer lugar (como dentro de um reprodutor de mídia) para abrir uma caixa de diálogo onde pode procurar por um arquivo de vídeo ou colar uma URL manualmente.

- **Plataformas Online Suportadas:** YouTube, Instagram, TikTok e Twitter (X).
- A IA detectará automaticamente o arquivo local ou a URL, processará o vídeo e fornecerá uma descrição visual abrangente e um resumo em áudio.
- **Cache de arquivos de vídeo por 48 horas:** Os vídeos enviados para o Gemini ficam no cache por 48 horas! Você pode gerar novamente os arquivos SRT ou MP3 para o mesmo vídeo sem precisar enviá-lo de novo — mesmo após reiniciar o NVDA. O cache reconhece a sua chave de API e é limpo automaticamente quando ela é alterada.

### 5.3 Geração de Audiodescrição (SRT)

Para uma experiência mais estruturada, o complemento pode gerar roteiros profissionais de Audiodescrição no formato padrão SubRip (SRT).

- **Sincronização Inteligente por Pausas:** A IA escuta a faixa de áudio e ancora especificamente suas descrições visuais em pausas naturais e intervalos silenciosos para minimizar inteligentemente a sobreposição com os diálogos.
- **Rastreamento de personagens**: O motor realiza uma pré-análise para extrair personagens distintos com base em características faciais imutáveis. Ele constrói um dicionário global para rastrear e rotular com precisão os personagens em diferentes cenas sem confusão. Ele também rastreia a **primeira aparição** de cada personagem, descrevendo o seu visual físico apenas uma vez — no momento em que aparecem pela primeira vez — e usando apenas os nomes estabelecidos em cenas posteriores para manter a narrativa dinâmica e natural.
- **OCR de Texto Literal:** Qualquer texto que apareça na tela (placas, celulares, créditos) é rigorosamente citado de forma literal.
- **Como Usar:** Para ouvir a legenda gerada, basta colocar o arquivo `.srt` na mesma pasta do seu arquivo de vídeo e dar a ele exatamente o mesmo nome. Depois, configure seu reprodutor de mídia (ex.: VLC ou PotPlayer) para encaminhar o texto das legendas diretamente para o seu leitor de tela ou motor TTS durante a reprodução.
- **Experiência de salvamento aprimorada:** Ao salvar arquivos SRT ou MP3, a janela de salvamento agora abre na pasta do vídeo de origem por padrão, independentemente de você ter aberto o vídeo pela janela de arquivo ou por Shift+V no Explorer.

### 5.4 Narração de Áudio Sincronizada (Exportação em MP3)

Além de criar arquivos SRT em texto, o complemento funciona como uma ferramenta completa de produção de Audiodescrição, sintetizando as descrições em voz e misturando-as com o vídeo. Você agora pode escolher o **Gemini Live TTS** como motor de voz, o qual utiliza a API do Gemini Live para gerar narrações de voz altamente realistas e ilimitadas. Ao gerar um MP3 para arquivos de vídeo locais, você dispõe de vários modos de mixagem:

- **AD Padrão (Misturar Voz):** A narração é sobreposta diretamente sobre o áudio do vídeo. Será perguntado se você deseja aplicar **Atenuação de Áudio (Ducking)** (reduzir o volume de fundo durante as descrições) para garantir que a narração fique clara.
- **Áudio descrição estendida (pausar áudio)**: O motor pausa o áudio do vídeo original durante as descrições, garantindo que você nunca perca uma única palavra do diálogo original ou da narração da IA. A detecção de silêncio agora usa o modelo neural **Silero VAD** (baixado automaticamente no primeiro uso, assim como o ffmpeg e o eSpeak) para uma precisão exata no tempo de pausa — distinguindo pausas naturais no diálogo de músicas e ruídos de fundo.
- **Vídeos do YouTube:** Para fontes do YouTube (que não são baixadas localmente), a exportação MP3 conterá estritamente a faixa de voz da IA sincronizada, sem o áudio de fundo do vídeo.

## 7. Transcrição e Dublagem de Mídia (M)

O Transcritor de Áudio foi completamente reconstruído para suportar arquivos de áudio e vídeo (MP3, WAV, MP4, MKV, etc.). Pressione **M** na Camada de Comandos para selecionar um arquivo de mídia e escolha um dos 3 modos de operação distintos:

1. **Transcrever (Idioma Original)**: Transcreve com precisão a fala em seu idioma original.
2. **Transcrever e Traduzir (Idioma de Destino)**: Transcreve a fala e a traduz para o seu idioma de destino configurado.
3. **Dublar e Traduzir (Idioma de Destino)** _(Apenas Gemini)_: Um novo recurso poderoso que transcreve a fala, traduz para o seu idioma de destino e sintetiza uma dublagem em áudio falado utilizando o motor TTS do complemento.

## 8) Leitor Avançado de Documentos e Imagens

O **Leitor de Documentos** transforma seus documentos em texto limpo e legível — para que você possa ler, traduzir e ouvir qualquer coisa, desde um livro escaneado até uma pilha de fotos. Ele manipula PDFs de várias páginas, imagens complexas, formatos HEIC do iPhone e até arquivos de texto simples (`.txt`) e HTML (`.html`, `.htm`), que são abertos instantaneamente sem OCR ou processamento de IA. Selecione vários arquivos de uma vez e eles serão mesclados em um único documento contínuo na ordem das páginas. Três motores de OCR estão disponíveis — **Chrome (Rápido)**, **IA (Avançado)** para preservação superior de layout e **Nenhum (Extrair Camada de Texto)** para PDFs pesquisáveis — selecionados em Configurações → Leitor de Documentos.

### Como Funciona

1. Pressione **NVDA + Shift + V** e, em seguida, **D** para abrir o Leitor de Documentos — ou selecione um arquivo no Explorador de Arquivos primeiro e pressione **D** / **F** para ignorar completamente a caixa de seleção de arquivos.
2. Escolha um ou mais PDFs ou imagens. O complemento os analisará e anunciará a contagem total de páginas.
3. Na caixa de diálogo **Opções**, escolha o intervalo de páginas (De/Para). Você também pode marcar **Traduzir Resultado** e escolher o idioma de destino, ou alternar **Descrever imagens embutidas durante o OCR**.
4. A extração de texto começa em segundo plano em lotes. Você pode fechar a janela a qualquer momento e continuar mais tarde — nada é perdido.
5. Assim que as páginas estiverem prontas, leia-as no visualizador: mova-se entre as páginas, vá para qualquer página, faça perguntas à IA, salve o texto ou gere uma narração em áudio.

### 7.1 Processamento em Lote e Retomada

Você não precisa ler um documento enorme de uma só vez. Escolha um intervalo de páginas (ex.: `1-20`) ou mantenha os padrões para processar tudo, e a IA extrairá todas as páginas em segundo plano. Se o NVDA travar ou se você interromper a análise, o complemento se lembrará do seu progresso e oferecerá a opção de **Retomar** exatamente de onde parou — mesmo após reiniciar. Documentos concluídos também são mantidos em cache, portanto, reabri-los (a partir dos Documentos Recentes ou via **D**) carrega o texto instantaneamente sem executar o OCR novamente, a menos que os arquivos de origem tenham sido alterados.

### 7.2 Ação Inteligente em Arquivos

Você nem sempre precisa abrir o documento primeiro. No Explorador de Arquivos do Windows, basta selecionar um arquivo PDF, imagem ou texto/HTML e pressionar **D** (Leitor de Documentos) — ou selecionar um PDF ou imagem e pressionar **F** (Ação de Arquivo Inteligente) — dentro da Camada de Comandos. O complemento ignora instantaneamente a caixa de seleção de arquivos e começa a processar o arquivo selecionado. Selecionar vários arquivos de uma vez os processa juntos como um único documento.

### 7.3 Controles e Atalhos do Visualizador de Documentos

Quando a janela do Leitor de Documentos estiver aberta, você poderá usar os seguintes recursos:

#### Atalhos de Teclado

- **Ctrl + PageDown / Ctrl + PageUp:** Move para a próxima página / página anterior.
- **Seta para Baixo / Seta para Cima:** Quando o cursor atingir a última linha de uma página, pressione **Seta para Baixo** para ir para a próxima página; pressione **Seta para Cima** no topo de uma página para voltar à anterior.
- **Alt + A:** Abre uma caixa de diálogo de bate-papo para fazer perguntas sobre o documento.
- **Alt + R:** Força uma **Nova Análise com IA** utilizando o seu provedor ativo.
- **Alt + G:** Gera e salva um arquivo de áudio de alta qualidade (WAV/MP3). _(Oculto se o provedor não suportar TTS)._
- **Alt + S / Ctrl + S:** Salva o texto extraído como um arquivo TXT ou HTML.

#### Botões e Controles

- **Ir para:** Escolha qualquer página no seletor de páginas.
- **Ver Formatado:** Veja o documento inteiro combinado como texto formatado.
- **Tentar Novamente Páginas com Falha:** Tenta novamente apenas os lotes que falharam devido a um erro temporário do servidor (ex.: alta demanda). Este botão aparece automaticamente quando necessário.
- **Voz do TTS / Motor de TTS:** Escolha a voz e, no Gemini, escolha entre **TTS Padrão** e transmissão em tempo real via **Gemini Live**.
- **Anterior / Próxima:** Alterna entre as páginas (mesmo funcionamento dos atalhos Ctrl+PageUp/PageDown).

### 7.4 Documentos Recentes (D)

Pressionar **D** na Camada de Comandos lista primeiramente os seus documentos lidos recentemente. Escolha um para continuar a partir da página em que parou — mesmo que o OCR já tenha sido concluído — ou pressione **Abrir Arquivo...** (`Ctrl + O`) para procurar por um arquivo normalmente.

## 9. Rotulagem Semântica por IA e Explorador de IU

Preso em um aplicativo cheio de "botão sem rótulo" por toda parte? O motor de Rotulagem Semântica por IA resolve isso definitivamente.

### 8.1 Rotulagem Permanente de Objetos (L)

Foque o seu leitor de tela em um gráfico ou botão sem rótulo e pressione **L** na Camada de Comandos. A IA analisará o botão visualmente, determinará sua função e aplicará um rótulo permanente.
_Ao contrário das ferramentas de rotulagem mais antigas dos leitores de tela, este complemento utiliza um sistema híbrido avançado de "Assinatura de Objeto" (AutomationId/ControlID). Seus rótulos personalizados resistirão ao redimensionamento de janelas, à troca de monitores e às atualizações dos aplicativos!_

### 8.2 Verificação Completa do Aplicativo (Shift + L)

Pressione **Shift + L** para analisar toda a janela ativa de uma só vez. A IA encontrará todos os elementos sem rótulo e os nomeará inteligentemente de uma só vez. Mais tarde, você poderá gerenciar, renomear ou excluir em lote esses rótulos no Gerenciador de Rótulos integrado.

### 8.3 Explorador de IU (E)

Precisa interagir com um elemento sem navegar até ele manualmente? Pressione **E** para ativar o Explorador de Interface. A IA analisará a tela e gerará uma lista acessível de todos os elementos clicáveis (ignorando ruídos do sistema como as barras de tarefas). Escolha um item da lista e o complemento clicará nele instantaneamente para você.

## 10. Assistente de Voz em Tempo Real

O Assistente ao Vivo transforma o Vision Assistant Pro em um copiloto interativo em tempo real.
_(Nota: Este recurso é exclusivo do Google Gemini e de provedores personalizados compatíveis com o Gemini)._

- **Ativação:** Pressione **Control + L** na Camada de Comandos para abrir a caixa de diálogo do Assistente em Tempo Real.
- **Interação em Tempo Real:** Fale naturalmente através do seu microfone. A IA ouvirá sua voz e analisará sua tela ativa simultaneamente. Você pode fazer perguntas como "O que estou vendo?" ou "Leia o terceiro parágrafo para mim."
- **Pressionar para Falar (Push to Talk):** Ative o **Pressionar para Falar** na aba de configurações do Assistente em Tempo Real (ou alterne diretamente dentro da janela do Assistente em Tempo Real), depois segure a tecla atribuída para falar e solte-a para finalizar. Isso mantém o microfone mudo até que você pressione a tecla — perfeito para ambientes barulhentos.
- **Entrada de webcam:** Marque **Usar &webcam** na janela do Live Assistant para enviar a imagem da sua câmera para a IA em vez da sua tela — pergunte sobre objetos físicos, documentos impressos ou ao seu redor. Se o ffmpeg ainda não estiver instalado, marcar a caixa o baixa uma vez com a sua permissão; a opção fica desativada quando nenhuma câmera é detectada ou quando as configurações de privacidade do Windows bloqueiam o acesso à câmera.
- **Personalização:** Dentro da caixa de diálogo, você pode alterar o Estilo de Voz da IA (ex.: Profissional, Amigável, Animado) e ajustar sua "Profundidade de Raciocínio" para controlar o nível de análise antes de responder.

## 11. Observador Ambiental (Assistente em Segundo Plano)

O Observador de Ambiente transforma o Vision Assistant Pro nos seus olhos em segundo plano, sem qualquer conversa: ele continua ouvindo e observando enquanto você trabalha, relata o que muda e permanece em silêncio quando nada acontece.
_(Nota: Este recurso é exclusivo do Google Gemini e de provedores personalizados compatíveis com o Gemini)._

- **Correções de bugs e melhorias de estabilidade**: Corrigido um travamento durante a geração de MP3 ao fechar a janela de progresso no meio da tarefa, resolvido um problema de condição de corrida (race condition) no armazenamento do dicionário de personagens, adicionada notificação adequada de erros para falhas na codificação de MP3 e corrigido o loop de espera do leitor de documentos para respeitar o cancelamento do usuário.
- **Modos:** **Apenas Tradução de Áudio** traduz o que ouve, **Apenas Observador de Tela** relata as alterações na tela e **Apenas Observador de Webcam** abre a janela do Assistente ao Vivo com a sua câmera e o recurso Falar ao Pressionar (Push to Talk), para que você possa fazer perguntas sobre o que a câmera está vendo.
- **Fonte de Áudio:** No modo de áudio, escolha se deseja traduzir o seu **Microfone** ou o **Áudio do Sistema (Loopback)**. A biblioteca leve de loopback é baixada uma única vez no primeiro uso, mediante a sua permissão.
- **Contexto:** Para os modos de tela e webcam, escolha uma opção opcional em **Sobre o que estou fazendo** (por exemplo, assistindo a um filme, acompanhando uma reunião ou chamada, lendo um rótulo ou verificando sua aparência) para direcionar os relatórios; você também pode digitar seu próprio contexto.
- **Relatórios:** O add-on compara cada novo quadro com o anterior e o envia para a IA apenas quando a imagem realmente muda, garantindo que uma tela estática nunca consuma chamadas de API desnecessárias. A IA então relata apenas o que há de novo e nunca se repete.
- **Mensagem de Boas-Vindas:** Exceto no modo de tradução, o observador saúda você brevemente quando é iniciado, para que saiba que ele está ouvindo.
- **Configurações:** Em **Configurações > Assistente ao Vivo**, defina o **Modo Observador**, o **Intervalo de Quadros** (1 a 10 segundos) e o **Estilo de Relatório** (resumido ou detalhado). A instrução do observador e cada texto de contexto podem ser editados no Gerenciador de Prompts (seção **Ambiente**).

## 12. Prompts Personalizados e Variáveis

Você pode gerenciar os prompts em **Configurações > Prompts > Gerenciar Prompts...**.

- **Filtro:** A aba **Prompts Padrão** possui uma lista de **Filtro** acima da lista de prompts que exibe **Todos** os prompts ou apenas uma seção por vez (por exemplo, **Ambiente**), mantendo a navegação simples mesmo em listas longas.

### Atalhos de Prompts Personalizados

Atribua a qualquer prompt personalizado sua própria tecla de atalho diretamente no Gerenciador de Prompts e execute-o instantaneamente com sua seleção ou contexto atual:

- **Tecla única** (ex.: `1`, `p` ou `F3`): Funciona dentro da Camada de Comandos e também globalmente como `NVDA + Shift + tecla`.
- **Combinação de teclas** (ex.: `Control + Shift + 1`, `Alt + P` ou `Insert + 1`): Funciona de forma global e independente.

### Comportamento do Feedback por Prompt

Cada prompt personalizado pode definir individualmente seu comportamento de exibição de saída:

- **Configuração global:** Segue a configuração geral de saída da Conexão (Saída Direta ou Janela de Chat).
- **Copiar para a área de transferência:** Copia a resposta da IA diretamente para a área de transferência sem abrir uma janela.
- **Saída Direta (mensagem do NVDA):** Fala/exibe em braille a resposta da IA diretamente por meio do leitor de telas NVDA.
- **Copiar para a área de transferência e Saída Direta:** Copia a resposta para a área de transferência e a fala diretamente.
- **Janela de Chat:** Sempre abre o resultado em uma janela de conversa interativa.

### Variáveis Suportadas

- `[selection]`: Texto atualmente selecionado.
- `[texto]`: Conteúdo de texto completo do campo de edição atualmente selecionado (ignora automaticamente campos de senha protegidos).
- `[currentURL]`: URL da página web ou do documento em navegadores web compatíveis (Chrome, Edge, Firefox).
- `[clipboard]`: Conteúdo da área de transferência.
- `[clipboard_image]`: Imagem atualmente na área de transferência.
- `[screen_obj]`: Captura de tela do objeto de navegação.
- `[screen_fg_obj]`: Captura de tela da janela ativa em primeiro plano.
- `[screen_full]`: Captura da tela inteira.
- `[file_ocr]`: Selecionar arquivo de imagem/PDF para extração de texto.
- `[file_read]`: Selecionar documento para leitura (TXT, Código, PDF).
- `[file_audio]`: Selecionar arquivo de áudio para análise (MP3, WAV, OGG).
- `[ambient_screen]`: Inicia uma sessão contínua do Observador de Tela em segundo plano.
- `[ambient_webcam]`: Inicia uma sessão contínua do Observador de Webcam em segundo plano (verifica a opção Pressionar para Falar nas configurações).
- `[ambient_audio]`: Inicia uma sessão de tradução em tempo real do Observador de Áudio.
- `[loopback]`: Usa a reprodução do áudio do sistema como fonte de som (para `[ambient_audio]`).
- [mic]: Usa o microfone como fonte de som (para [ambient_audio] e [ambient_webcam]).
- `[brief]`: Define o estilo de relatório do observador como sucinto (uma única frase).
- `[detailed]`: Define o estilo de relatório do observador como detalhado (2 a 3 frases).
- `[lang:code]`: Especifica o código do idioma de destino para a tradução de áudio (por exemplo, `[lang:fa]`, `[lang:en]`).
- `{target_lang}`: Idioma de destino atual.
- `{source_lang}`: Idioma de origem atual.
- `{response_lang}`: Idioma atual de resposta da IA.
- `{swap_target}`: Idioma alternativo para a tradução com troca inteligente.
- `{swap_instruction}`: Bloco de instruções para tradução com troca inteligente.

_Nota sobre Prompts de Ambiente:_ Prompts que contêm variáveis de ambiente funcionam como um alternador — pressionar o atalho enquanto a sessão estiver ativa irá interrompê-la imediatamente. Combinações incompatíveis (como combinar variáveis de captura de tela estáticas, como `[screen_full]`, com modos de observador de ambiente, combinar múltiplos modos de ambiente ou adicionar instruções de prompt ao `[ambient_audio]`) são estritamente validadas e impedidas no momento do salvamento.

## 13. Casos de Uso no Mundo Real (Qual recurso devo usar?)

O Vision Assistant Pro está repleto de ferramentas avançadas. Aqui estão alguns cenários comuns para ajudar você a escolher a opção certa:

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

**Nota:** É necessária uma conexão ativa com a internet para todos os recursos de IA. Documentos de várias páginas são processados automaticamente.

## 14. Suporte e Comunidade

Mantenha-se atualizado com as últimas notícias, recursos e lançamentos:

- **Canal no Telegram:** [t.me/VisionAssistantPro](https://t.me/VisionAssistantPro)
- **Issues no GitHub:** Para relatórios de erros e solicitações de recursos.

### Relatando Erros e Logs

Ao abrir um chamado (issue) no GitHub ou solicitar suporte, inclua detalhes sobre seu provedor de IA ativo, modelo e versão do NVDA. Se estiver enfrentando problemas de conexão ou fechamentos inesperados, habilite o arquivo de log dedicado em **Configurações > Avançado**, reproduza o problema e anexe seu arquivo `vision_assistant.log` para nos ajudar a resolver o problema mais rapidamente.

## 15. Apoiadores do Projeto

Um agradecimento do fundo do coração aos membros da nossa comunidade que apoiam o desenvolvimento contínuo e a manutenção deste projeto por meio de suas generosas contribuições financeiras:

- **@Alyabani94**
- **Ali Alamri**
- **Ilya**
- **leonardo0216**
- **Sergei Fleytin**
- **Arne Siebert**
- **Schalkefan**
- Bate-Papo Direto
- **[avalai.org](https://avalai.org)**

_Se você deseja apoiar o projeto financeiramente e ver seu nome aqui, poderá encontrar a opção **Doar** no menu Ferramentas do NVDA ((sub-menu Vision Assistant) ou durante o processo de configuração após a instalação._

---

## Alterações para 2026.10.15

- **A Correção Mais Solicitada — Criar uma Chave de API do Gemini Finalmente Ficou Fácil**: Obter uma chave de API no **aistudio.google.com** costumava ser a etapa mais difícil de todas. Com um leitor de telas as páginas eram confusas e algumas pessoas simplesmente não conseguiam criar uma chave de forma alguma. Esse problema agora está resolvido diretamente dentro do add-on. Pressione **G** na Camada de Comando (ou use **Obter uma Chave de API do Gemini...** nas Configurações), faça login pelo seu navegador padrão sem nenhuma configuração externa, e sua chave será criada e configurada com apenas uma confirmação — mesmo que você nunca tenha tido um projeto antes.
- **Observador de Ambiente**: O assistente em segundo plano está ativo. Pressione **Shift+O** na Camada de Comando para iniciá-lo e pressione novamente para pará-lo. Ele pode traduzir o que ouve (seu microfone ou o áudio do sistema), observar a tela e informar o que mudou, ou abrir o Assistente ao Vivo com sua webcam e a função Pressionar para Falar para que você possa perguntar sobre qualquer coisa que a câmera estiver mostrando. Ele envia uma imagem apenas quando algo realmente muda, portanto, uma tela estática não consome nada e ele permanece em silêncio quando nada está acontecendo. Você também pode iniciar e alternar o observador diretamente por meio de Prompts Personalizados e teclas de atalho dedicadas usando `[ambient_screen]`, `[ambient_webcam]` ou `[ambient_audio]`, juntamente com modificadores (`[loopback]`, `[mic]`, `[brief]`, `[detailed]`, `[lang:code]`), com validação automática contra combinações conflitantes de variáveis.
- **Operador ao Vivo**: O Assistente ao Vivo agora pode executar o que você pedir no seu computador enquanto você conversa com ele. Pressione **Control+A** na Camada de Comando para iniciar uma sessão de operador ao vivo e, em seguida, basta perguntar em linguagem natural. Ele executa solicitações de várias etapas, narra cada passo com a própria voz do Assistente ao Vivo, cuida das combinações de teclas necessárias e decide por conta própria quando a tarefa foi concluída. **Saída Direta ao Vivo (Sem Janela)** também está nas Configurações Rápidas.
- **Dicionário de personagens e gerenciamento de séries**: A janela de Análise de Vídeo agora inclui um poderoso sistema de **Dicionário de Personagens**! Adicione, edite, importe ou gerencie nomes de personagens, descrições físicas e papéis por série — a IA associa automaticamente os personagens encontrados ao seu dicionário e mescla novos conforme você analisa mais episódios. Suas notas manuais são sempre preservadas com prioridade sobre as atualizações da IA, enquanto as descrições físicas permanecem atualizadas ao longo dos episódios. O dicionário é salvo por série e reutilizado para cada vídeo dessa série. Na lista de personagens, pressione **F2** para editar o personagem selecionado e **Delete** para removê-lo.
- **Suporte a Proxy SOCKS5, HTTP e Proxy Reverso com Teste de Latência**: Contorne restrições de rede sem complicações com suporte completo a proxies em todo o add-on — incluindo o Assistente ao Vivo, Observador de Ambiente e geração de TTS! Escolha entre 4 modos de operação nas Configurações Gerais: **Detecção automática**, **Proxy SOCKS5**, **Proxy HTTP** ou **Proxy Reverso**. O SOCKS5 oferece suporte à autenticação de nome de usuário e senha no padrão RFC 1929 e ao tunelamento de domínios; o proxy HTTP oferece suporte à autenticação Básica (Basic authentication). Um novo botão **Testar Conexão de Proxy** é executado em segundo plano e anuncia a latência da sua conexão em milissegundos.
- **Cache de arquivos de vídeo por 48 horas**: Os vídeos enviados para o Gemini agora ficam no cache por 48 horas! Você pode gerar novamente os arquivos SRT ou MP3 para o mesmo vídeo sem precisar enviá-lo de novo — mesmo após reiniciar o NVDA. O cache reconhece a sua chave de API e é limpo automaticamente quando ela é alterada.
- **Detecção de silêncio por IA (Silero VAD)**: A áudio descrição estendida agora usa o modelo neural Silero VAD para uma detecção de silêncio precisa — distinguindo pausas naturais no diálogo de músicas e ruídos de fundo. O modelo é baixado automaticamente no primeiro uso (com a sua permissão), assim como o ffmpeg e o eSpeak.
- **Vídeo da webcam para o Live Assistant**: A janela do Live Assistant agora possui a caixa de seleção **Usar &webcam** para enviar a imagem da sua webcam para a IA em vez da sua tela — perfeito para fazer perguntas sobre objetos físicos, documentos ou ao seu redor. Se o ffmpeg ainda não estiver instalado, marcar a caixa o baixa (uma única vez, com a sua permissão). A opção fica desativada quando nenhuma câmera é detectada ou quando as configurações de privacidade do Windows bloqueiam o acesso à câmera, exibindo um botão para abrir as configurações de privacidade da câmera. Se a câmera estiver ativada, mas não produzir quadros, o problema é registrado no log do NVDA para diagnóstico em vez de alternar silenciosamente de volta para a tela.
- **Seleção de Dispositivo de Saída de Áudio**: Agora você pode selecionar um dispositivo de saída de áudio dedicado para o Assistente ao Vivo e o Observador de Ambiente. Escolha entre a saída padrão do NVDA, o Mapeador de Som do Windows ou qualquer placa de som física conectada (como fones de ouvido USB ou caixas de som externas) na guia Configurações do Assistente ao Vivo, diretamente no diálogo do Assistente ao Vivo ou rapidamente pelas Configurações Rápidas (NVDA+Shift+V e, em seguida, Cima/Baixo/Esquerda/Direita).
- **Gerenciador de Prompts**: A guia Prompts Padrão agora possui uma lista de **Filtros**, para que você possa exibir todos os prompts ou apenas uma seção específica (por exemplo, **Ambiente**). Você também pode editar os textos de contexto do observador e as novas **Instruções do Operador ao Vivo** nessa mesma tela.
- **Filtragem Inteligente de Modelos no Roteamento Avançado**: As caixas de seleção do Roteamento Avançado de Modelos agora categorizam dinamicamente os modelos do Gemini por funcionalidade, mantendo a interface limpa e organizada. O Assistente ao Vivo exibe apenas modelos bidirecionais ao vivo e de áudio nativo autênticos, o TTS exibe apenas modelos dedicados à síntese de voz, o STT prioriza modelos Transcribe e multimodais, e a Análise de Vídeo, OCR e Operador de IA filtram e excluem com precisão modelos utilitários de finalidade única (como modelos de geração de imagem, geração de vídeo e embedding). Novos modelos lançados no futuro serão detectados automaticamente com base em suas funcionalidades, sem a necessidade de atualizar a versão do add-on.
- **Rastreamento da primeira aparição do personagem**: A IA agora descreve a aparência física de cada personagem apenas uma vez — na sua primeira aparição no vídeo. As aparições subsequentes usam apenas os nomes, eliminando descrições repetitivas ao longo dos segmentos e mantendo a narrativa dinâmica e natural.
- **Diretório de dados unificado**: Todos os arquivos de dados do complemento (histórico, séries, rótulos, progresso do OCR, caches e logs) foram migrados para uma única pasta `VisionAssistant` dentro do seu diretório de configuração do NVDA — mantendo tudo organizado e tornando os backups manuais muito fáceis.
- **Experiência de salvamento de vídeo aprimorada**: Ao salvar arquivos SRT ou MP3, a janela de salvamento agora abre na pasta do vídeo de origem por padrão, independentemente de você abrir o vídeo pela janela de arquivo ou por Shift+V no Explorer.
- **Excluir documentos com ou sem o texto em cache**: A janela do Histórico (`Control + H`) agora oferece duas maneiras de excluir um documento — pressione Delete e escolha **Excluir apenas do histórico** ou **Excluir do histórico e do texto em cache**. A segunda opção limpa o texto OCR em cache desse documento, para que a próxima abertura o analise novamente do zero — ideal após uma digitalização ruim. A caixa de seleção **Não perguntar novamente** lembra sua escolha para exclusões futuras. Seus dados de retomada de operações interrompidas nunca são alterados.
- **Cache do OCR inteligente por motor e cumulativo no Leitor de Documentos**: O texto do OCR em cache agora é armazenado por motor de OCR, portanto, alternar o motor de OCR sempre realiza uma nova leitura com o novo motor em vez de reproduzir o resultado antigo. Ao reabrir um documento, a janela de intervalo de páginas é exibida novamente (pré-preenchida com sua última escolha), reutilizando instantaneamente as páginas já digitalizadas e lendo apenas as que faltam — o cache mescla página por página em vez de ser substituído, assim cada intervalo que você lê é mantido para uso posterior.
- **Compactação de PDF no Leitor de Documentos**: Adicionada a opção **Compactar páginas do PDF antes do processamento** no diálogo de intervalo de páginas do Leitor de Documentos. Ao enviar documentos PDF digitalizados grandes ou de alta resolução para o Gemini ou Mistral, as páginas são reduzidas e recompactadas automaticamente para diminuir drasticamente o tamanho do arquivo enviado, acelerar o processamento e evitar limites de tempo de conexão (timeouts). A opção fica desativada por padrão e é ocultada automaticamente ao usar o motor do Chrome ou provedores de imagem baseados em base64.
- **Personalização do Comportamento de Resposta por Prompt**: Personalize individualmente como cada prompt customizado entrega seu resultado! No editor de prompts customizados, escolha entre **Configuração global**, **Copiar para a área de transferência**, **Saída direta (mensagem do NVDA)**, **Copiar para a área de transferência e Saída direta** ou **Janela de chat**. Isso permite que prompts específicos sejam lidos diretamente sem abrir uma janela, enquanto outros abrem um chat completo.
- **Novas Variáveis Dinâmicas para Prompts (`[currentURL]` e `[text]`)**: Os Prompts Customizados agora suportam a variável `[currentURL]`, que captura a URL do documento ativo no Google Chrome, Mozilla Firefox e Microsoft Edge, e a variável `[text]`, que insere dinamicamente todo o texto do campo de edição em foco (ignorando campos de senha protegidos).
- **Reformulação do Download de Vídeos do Twitter/X**: Restaurado o download e a análise de vídeos do Twitter/X após falhas na extração do serviço anterior. A extração de vídeos agora utiliza a robusta API do FixTweet para obter diretamente os fluxos MP4 de maior qualidade da CDN do Twitter, contando com suporte a proxy e alternância automática (fallback) para o TwitSave caso necessário.
- **Correção do Download de Vídeos do Instagram**: Restaurado o download e a análise de Reels e URLs de vídeos do Instagram após mudanças nos formulários do serviço de extração.
- **Correções e Desempenho**: O Pressione para Falar (Push to Talk) responde no exato instante em que você pressiona a tecla, o Assistente ao Vivo não inicia mais uma resposta no meio de uma frase, o observador não relata mais a imagem anterior e a lista de Profundidade de Raciocínio (Thinking Depth) oferece apenas as opções suportadas pelo modelo selecionado. O Operador de IA agora também pode rolar a tela para a esquerda e para a direita. Corrigido um erro de atributo (`AttributeError`) ao analisar vídeos online e evitada a inserção acidental do título da janela em segundo plano nas requisições de IA quando um prompt customizado for executado sem texto selecionado.

## Alterações para 2026.09.01

- **Histórico (Control + H)**: A Camada de Comandos agora inclui uma caixa de diálogo de **Histórico** (`Control + H`) que lista seus bate-papos e documentos anteriores com filtros para Todos, Bate-papos e Documentos. Reabra qualquer bate-papo com sua conversa completa — os arquivos anexados são reanexados automaticamente — ou reabra um documento e continue a leitura. Pressione **Delete** em qualquer item para removê-lo ou limpe tudo de uma só vez.
- **Documentos Recentes no Leitor**: Pressionar **D** na Camada de Comandos agora exibe primeiramente seus documentos lidos recentemente. Escolha um para continuar a partir da página em que parou — mesmo quando o OCR já tiver sido concluído — ou pressione **Abrir Arquivo...** (`Ctrl + O`) para procurar normalmente.
- **Pressionar para Falar no Assistente em Tempo Real**: Tenha controle total de suas conversas ao vivo! Habilite o **Pressionar para Falar (Push to Talk)** na nova aba de configurações do Assistente em Tempo Real e atribua qualquer tecla — ou até mesmo uma tecla modificadora isolada como `Ctrl Esquerdo` — para falar. Mantenha a tecla pressionada para falar e solte-a quando terminar, com um curto sinal sonoro a cada pressionamento e liberação. Uma opção correspondente também aparece diretamente na janela do Assistente em Tempo Real, permitindo alternar entre o modo pressionar para falar e o microfone aberto sem sair da conversa.
- **Áudio Nativo do Gemini 2.5 Flash**: O Assistente em Tempo Real agora suporta o modelo de áudio nativo do Gemini 2.5 Flash (`gemini-2.5-flash-native-audio-preview-12-2025`) para conversas de voz naturais e com baixa latência. Você pode alternar para ele em **Configurações → Roteamento Avançado de Modelos → Modelo do Assistente em Tempo Real (somente Gemini)**, ou manter em "Auto" para permanecer no modelo recomendado.
- **Backup e restauração de configurações**: Adicionado um poderoso sistema de backup e restauração na guia **Avançado**! Agora você pode salvar todas as configurações do seu complemento — incluindo chaves de API, modelos, prompts personalizados e preferências — em um único arquivo JSON e restaurá-las perfeitamente a qualquer momento, em qualquer máquina ou após reinstalar o NVDA. Ao fazer o backup, você escolhe o que incluir: **Tudo** (configurações, rótulos personalizados, progresso do OCR e histórico) ou **Apenas configurações**.
- **Leitura Direta de Texto e HTML**: O Leitor de Documentos agora pode abrir arquivos de texto puro (`.txt`) e HTML (`.html`, `.htm`) diretamente! Ele detecta automaticamente a codificação do arquivo, remove scripts e sujeiras de formatação, e divide o conteúdo de forma inteligente em páginas legíveis — inclusive reimportando seus próprios arquivos exportados mantendo a estrutura das páginas —, para que você possa lê-los instantaneamente sem necessidade de OCR ou processamento por IA!
- **TTS do Gemini Live para o Leitor de Documentos**: O botão "Gerar Áudio" agora suporta o Gemini Live — um motor de síntese de voz via transmissão de alta qualidade e ritmo natural! Quando o Gemini for seu provedor ativo, você pode escolher entre o TTS Padrão e o Gemini Live diretamente no leitor, e sua seleção será lembrada para a próxima vez!
- **Atalhos de Prompts Personalizados**: You can now assign a shortcut key to any of your custom prompts right from the Prompt Manager! Give every prompt its own dedicated key or key combination to run it instantly, automatically capturing your current selection or context with zero extra steps!
- **Navegação pelas Mensagens do Bate-Papo**: Revise qualquer conversa sem usar as mãos! Dentro de qualquer janela de bate-papo (Bate-Papo Direto, bate-papo de documento, refinamento e mais), pressione `Alt + Seta para Baixo` para ouvir a próxima mensagem e `Alt + Seta para Cima` para ouvir a anterior — com prefixos claros de "Você" / "IA" e anúncios de limites de "Primeira mensagem" / "Última mensagem" à medida que navega.
- **Copiar Mensagem do Bate-Papo (Alt + C)**: Ao revisar uma conversa com `Alt + Seta para Cima/Baixo`, pressione `Alt + C` para copiar a mensagem em que você está atualmente para a área de transferência — respeitando sua configuração de Markdown Limpo — com uma confirmação falada.
- **Prompt de Sistema do Bate-Papo Direto**: O Bate-Papo Direto (`Shift+C`) agora tem seu próprio prompt de sistema editável — "Instrução do Bate-Papo Direto" — que define a persona do assistente e o idioma de resposta para cada conversa. Você pode personalizá-lo na aba Prompts Padrão do Gerenciador de Prompts.
- **Navegação de Página pelo Cursor no Leitor de Documentos**: Ler documentos de várias páginas ficou ainda mais fluido! No Visualizador de Documentos, quando seu cursor atinge a última linha de uma página e você pressiona `Seta para Baixo`, o leitor pula automaticamente para a próxima página. Pressionar `Seta para Cima` no início de uma página retorna sem interrupções para a anterior — sem necessidade de alternar páginas manualmente durante a leitura!
- **Novas Alternâncias nas Configurações Rápidas**: Copiar respostas da IA para a área de transferência, Saída Direta (sem janela de bate-papo), Markdown Limpo no Bate-Papo e Troca Inteligente agora podem ser ativados e desativados instantaneamente nas Configurações Rápidas da camada de comandos!
- **Aba de Configurações do Assistente em Tempo Real**: O Assistente em Tempo Real agora possui sua própria aba de configurações dedicada! A opção "Assistente em Tempo Real: Saída Direta (Sem Janela)" foi movida da aba Conexão para cá, e a aba é exibida apenas quando o Google Gemini (ou um provedor Personalizado compatível com Gemini) for o seu provedor ativo.

## Alterações para 2026.08.06

- **Rotulagem no Explorador de Interface**: Agora você pode adicionar rótulos diretamente aos elementos encontrados dentro do Explorador de Interface! Foi adicionado um novo botão "Adicionar Rótulo", e a interface permanece aberta de forma inteligente mantendo o foco para que você possa rotular rapidamente vários objetos sem interrupções.
- **Melhoria na Camada de Configurações Rápidas**: A camada do Vision Assistant (`Insert+Shift+V`) agora é persistente e altamente interativa! Você pode utilizar as setas para `Cima/Baixo` para navegar entre as configurações rápidas (Provedor, Modelo, Idioma de Resposta da IA, Modelo de TTS) e as setas para `Esquerda/Direita` para alterar instantaneamente seus valores com um retorno de voz inteligente e conciso. Suas seleções entram em vigor imediatamente (incluindo a ativação automática do roteamento avançado, quando necessário) e a camada permanece ativa enquanto você configura.
- **Bate-Papo Direto (`Shift+C`)**: Adicionado um novo comando à camada! Pressione `Shift+C` para abrir instantaneamente uma janela de "Bate-Papo Direto". Isso fornece de imediato uma interface de conversa limpa e baseada em texto com a IA, sem necessitar de uma imagem ou documento como ponto de partida.
- **Restauração Perfeita do Histórico do Bate-Papo**: Corrigido um erro grave onde pressionar a tecla `Espaço` para restaurar o último resultado perdia o histórico da conversa subsequente. Agora, o complemento rastreia globalmente sua conversa. Se você conversar, fechar a caixa de diálogo e pressionar `Espaço` para restaurá-la, todo o seu histórico de trocas de mensagens será perfeitamente restaurado! Funciona para Bate-Papo Direto, Análise de Visão, Bate-Papo sobre Documentos e Tradução.
- **Descrições de Imagens no Texto (Inline) no OCR**: Adicionado um recurso opcional para descrever imagens no próprio texto durante o OCR de documentos. Você pode ativar ou desativar esta configuração nas configurações de OCR do complemento, nas opções do Leitor de Documentos antes da extração ou rapidamente na camada de Configurações Rápidas.
- **Tradução por Voz (`Control+T`)**: Adicionado um novo e poderoso recurso! Dite sua fala e ela será traduzida e digitada instantaneamente via IA com base nos seus idiomas de origem e destino configurados.
- **Melhorias no Gerenciador de Download de Atualizações**: A caixa de diálogo de download de atualizações agora exibe corretamente o progresso em porcentagens, e foi corrigido um erro em que uma mensagem fantasma "Baixando atualização" aparecia ao cancelar a instalação.
- **Melhorias no Gerenciador de Download do eSpeak-NG**: Adicionado o acompanhamento do progresso em porcentagem para os downloads do eSpeak-NG.
- **Resiliência no OCR em Lote**: Corrigido um problema no OCR em lote de arquivos PDF onde o processo parava se a chave de API ativa atingisse a cota na metade; agora o sistema alterna automaticamente para a próxima chave disponível e retoma o processo.
- **Suporte a CAPTCHA Visual**: Adicionado suporte robusto para resolução de CAPTCHAs visuais. O sistema tenta resolver automaticamente desafios complexos de imagem, como hCaptcha e reCAPTCHA, melhorando significativamente a acessibilidade em formulários web desafiadores.
- **Reformulação do Transcritor de Áudio**: O módulo Transcritor de Áudio foi completamente reconstruído e agora suporta arquivos de áudio e vídeo. Ele possui 3 modos de operação distintos: "Transcrever (Idioma Original)", "Transcrever e Traduzir (Idioma de Destino)" e uma nova e poderosa opção "Dublar e Traduzir (Idioma de Destino)" (exclusiva do Gemini) que gera uma dublagem de áudio traduzida da fala original.
- **Números de Página Opcionais no Leitor de Documentos**: Adicionada uma nova configuração para alternar a inclusão de números de página e separadores na saída de documentos com várias páginas. Você pode gerenciar facilmente essa opção nas configurações principais ou alterná-la na camada de Configurações Rápidas. Este recurso se aplica tanto à exportação de arquivos de texto/HTML quanto à janela "Ver Formatado", permitindo ler documentos combinados de forma contínua.
- **Gemini Live TTS Ilimitado para Descrições de Vídeo**: Agora você pode selecionar o "Gemini Live TTS" como motor de voz ao gerar Narração de Áudio Sincronizada (MP3) para vídeos. Isso utiliza a API do Gemini Live para sintetizar audiodescrições de alta qualidade sem limites de caracteres ou restrições de duração.
- **Modularização do Código-Fonte**: A estrutura do complemento foi refatorada de um único arquivo para uma arquitetura modular de múltiplos arquivos, melhorando sua manutenibilidade.
- **Redesign da Interface de Configurações**: A caixa de diálogo de Configurações foi completamente redesenhada para usar uma interface moderna baseada em abas em vez de um layout agrupado, proporcionando melhor organização e navegação mais fácil, mantendo todas as opções existentes.
- **Registro de Log Global e em Arquivo Dedicado**: Adicionado um sistema opcional de registro global em arquivo na nova aba de configurações "Avançado". Captura automaticamente eventos operacionais, tráfego de API e erros em todos os módulos do complemento em um arquivo dedicado (`vision_assistant.log`). Suporta níveis configuráveis de detalhamento do log (Depuração, Informação, Aviso, Erro), períodos de retenção automatizados (1 hora a 90 dias) e abertura ou limpeza direta do log a partir das configurações, sem nenhum impacto no desempenho ou interferência nos logs do NVDA.
- **Acompanhamento do Progresso de Envio no Gemini**: Adicionados anúncios de progresso em porcentagem e em tempo real ao enviar arquivos grandes (vídeo, áudio, documentos) para a API do Google Gemini.

## Alterações para 2026.07.15

- **Filtragem Inteligente de Modelos de API**: Reformulação completa do sistema de filtragem de modelos para utilizar uma abordagem de lista negra pura em vez de listas brancas. Adicionadas palavras-chave de filtragem mais fortes (`embedding`, `bison`, `gecko`, `audio`, `realtime`, `babbage`, `moderation`, `deep`, `antigravity`, `computer`) para garantir que o menu suspenso do modelo de bate-papo principal permaneça limpo e preparado para o futuro, mantendo todos os modelos especializados acessíveis na seção de Roteamento Avançado.
- **Pesquisa no Roteamento Avançado**: Todos os menus suspensos do Roteamento Avançado de Modelos (OCR, STT, TTS, Operador, Vídeo, Tempo Real) e o seletor de Variantes do eSpeak agora são totalmente pesquisáveis. Você pode digitar rapidamente para filtrar e encontrar o modelo ou variante desejado.
- **Novos Atalhos na Camada de Comandos**:
  - **Configurações (`Alt + S`)**: Abre instantaneamente a caixa de diálogo de configurações do Vision Assistant Pro.
  - **Relatório de Chaves com Cota Esgotada (`Alt + Q`)**: Informa o número exato de chaves de API do Gemini que excederam sua cota diária, identificando em qual modelo específico esgotaram, e anuncia o horário exato da sua reinicialização.
  - **Auditoria de Roteamento (`Alt + M`)**: Audita e anuncia sua configuração atual do Roteamento Avançado, lendo quais modelos estão ativamente selecionados para tarefas especializadas (ignorando as configurações padrão).
- **Reformulação Completa do Analisador de Vídeo**: O Analisador de Vídeo foi completamente transformado! Anteriormente, ele fornecia apenas uma descrição básica de vídeos online. Agora, é um pacote completo de processamento de vídeo sob medida para usuários cegos:
  - **Gravação de Tela Local (`Control+V`)**: Agora você pode gravar vídeos silenciosos diretamente da sua tela. A IA analisará o segmento gravado e fornecerá uma descrição altamente detalhada da cena, estrutura e ações.
  - **Geração de Audiodescrição (SRT)**: O complemento agora pode gerar roteiros de Audiodescrição altamente detalhados (no formato padrão SRT) para vídeos, com sincronização inteligente de pausas para ancorar as descrições nas pausas naturais da faixa de áudio, e OCR literal para qualquer texto na tela.
  - **Narração de Áudio Sincronizada (Exportação em MP3)**: Além das legendas em texto, o complemento pode sintetizar a Audiodescrição em voz, misturá-la automaticamente com a faixa de áudio original do vídeo, aplicar atenuador de áudio (reduzindo o volume de fundo durante as descrições) e exportar o resultado sincronizado final como um arquivo MP3!
  - **Ação Inteligente de Arquivo de Vídeo**: Se você focar em um arquivo de vídeo local e pressionar o atalho de vídeo, o complemento irá detectá-lo automaticamente e processará o arquivo diretamente.
  - **Rastreamento Avançado de Personagens**: A IA agora realiza uma análise prévia para extração de personagens. Ela constrói um dicionário global de personagens e rastreia cada um com precisão, segmento por segmento, sem confundir identidades.
  - **Configuração da Análise de Vídeo**: Adicionadas novas configurações para controlar o tamanho dos blocos SRT, legendagem de personagens e avisos de responsabilidade.
  - **Roteamento Expandido de Modelos**: Agora você pode selecionar explicitamente modelos de vídeo especializados (`gemini_video_model`, `custom_video_model`) nas configurações de Roteamento Avançado de Modelos.
- **Gerenciamento Inteligente de Cotas de API**: Tratamento aprimorado para erros 429 (Limite Diário Excedido) ao rastrear cotas por modelo. Se uma chave atingir seu limite diário em um modelo, ela entra inteligentemente em quarentena apenas para aquele modelo específico, mantendo a chave disponível para uso com outros modelos.

## Alterações para 5.5.2

- **Retomada de Análises Incompletas**: Adicionado um recurso de retomada tanto para o Leitor de Documentos quanto para as Ações Inteligentes de Arquivos. Se uma análise for interrompida, agora você pode continuar de onde parou em vez de recomeçar do zero.
- **Nova Variável `[screen_fg_obj]`**: Adicionada uma variável de prompt personalizada para capturar uma imagem apenas da janela ativa em primeiro plano, em vez da tela inteira.
- **Tentativas Inteligentes e Rotação de Chaves**: O complemento agora tenta novamente de forma silenciosa até 5 vezes na mesma chave ao encontrar sobrecargas temporárias no servidor (como "alta demanda" ou respostas malformadas). Se as tentativas falharem, ele alterna automaticamente para a próxima chave de API da sua lista.
- **Detecção de Cortina de Tela**: Adicionada uma verificação para evitar tirar capturas de tela quando a Cortina de Tela estiver ativa (seja ativada permanentemente ou alternada temporariamente pelo atalho). O complemento emitirá um aviso e interromperá a ação, evitando o envio de imagens pretas e o desperdício de tokens de API.
- **Ajustes no Leitor de Documentos**: A caixa de diálogo de intervalo de páginas de PDF agora pré-seleciona automaticamente o idioma de destino padrão das configurações do complemento. Também foi aprimorado o gerenciamento de threads para garantir que as tarefas em segundo plano sejam encerradas de forma limpa quando o leitor for fechado.
- **Integração Nativa do OCR da Mistral**: Integrada a API nativa de OCR de Documentos da Mistral. Os documentos de várias páginas são mesclados, enviados e processados em lotes automaticamente utilizando o endpoint especializado `/v1/ocr` da Mistral, enquanto imagens de página única são processadas diretamente, sem conversões desnecessárias para PDF [1].
- **Manipuladores Dinâmicos de URL Personalizada**: A alteração da URL de API personalizada agora limpa instantaneamente a lista de modelos em cache e restaura a caixa de texto para entrada manual do modelo. Isso garante total compatibilidade com endpoints personalizados (como o Cloudflare AI Gateway) que não suportam o endpoint de listagem padrão `/v1/models`.
- **Reformulação do Motor de Entrada do Operador de IA**: Reescrita completa do sistema subjacente de simulação de mouse e teclado para o Operador de IA. Substituída a API legada `mouse_event` pela moderna API `SendInput` do Windows, trazendo uma compatibilidade significativamente superior com aplicativos modernos, janelas protegidas por UAC e telas de alta densidade de pixels (High-DPI).
- **Correção nas Operações de Arrastar e Soltar**: As ações de arrastar e soltar no Operador de IA agora são totalmente estáveis e confiáveis. O novo motor utiliza curvas de atenuação suaves e naturais, posicionamento preciso do cursor, temporização otimizada e uma técnica inteligente de toque para garantir que o Windows e os aplicativos reconheçam e executem corretamente os gestos de arrastar e soltar sem falhar no meio do caminho.
- **Suporte a Múltiplos Monitores**: O Operador de IA agora suporta totalmente configurações de múltiplos monitores. Os movimentos do mouse e cliques funcionam corretamente em todos os monitores através da flag `MOUSEEVENTF_VIRTUALDESK`, garantindo um posicionamento preciso independentemente do monitor em que o aplicativo de destino esteja.
- **Simulação de Teclado Aprimorada**: Aprimorada a injeção de teclas para suportar totalmente as "Teclas Estendidas" (como teclas de Seta, Home, End, Page Up/Down, Insert, Delete e F1-F12). Isso garante que os comandos de navegação e atalhos enviados pelo Operador de IA funcionem sem falhas em todos os aplicativos.
- **Suporte a Imagens HEIC/HEIF**: Adicionado suporte nativo para os formatos de foto do iPhone. Agora você pode selecionar diretamente arquivos `.heic` e `.heif` para descrição por IA, OCR ou Leitura de Documentos sem necessidade de conversão prévia.

## Alterações para 5.5 (A Atualização de Automação)

- **Assistente em Tempo Real**: Adicionado um recurso de assistente de tela e voz em tempo real, disponível exclusivamente para o provedor Google Gemini (ou provedores personalizados compatíveis com o Gemini). Inclui personalização interativa de voz e de profundidade de pensamento diretamente na caixa de diálogo, com reconexão automática ao alterar as configurações.
- **Provedor de IA MiniMax**: Integração do MiniMax como um provedor equivalente com suporte multimodal completo (chat, visão, OCR), TTS personalizado com mais de 300 vozes dinâmicas e remoção automática de blocos de raciocínio (ex.: ` thinking... resposta`) dos resultados.
- **Tradução no Visualizador de Documentos**: Corrigida uma falha silenciosa de tradução para usuários do NVDA que não usam inglês, garantindo que o código de idioma padrão de 2 letras seja enviado para o Google Tradutor em vez do nome do idioma localizado.
- **Nova Tentativa na Análise de PDF em Lote**: Implementada uma lógica de nova tentativa separada, silenciosa e altamente otimizada para a análise em lote de documentos PDF, evitando envios redundantes e janelas de erro incômodas durante as novas tentativas.
- **Status do Visualizador de Documentos**: Corrigido um erro onde o status geral do complemento (verificado via `I`) permanecia travado em "Processamento em Lote Iniciado" durante análises longas de documentos.
- **Resolução de Falha de Threads**: Corrigida uma falha grave de asserção de threads `IsMain() failed in wxTimerImpl` ao abrir documentos a partir de uma thread em segundo plano, através da transição da fila de retorno da interface gráfica para `wx.CallAfter`.

## Alterações para 5.0

- **Pré-Verificação de Rótulos Duplicados**: Corrigido um problema na rotulagem individual onde a verificação de duplicados utilizava chaves de coordenadas antigas, fazendo com que o NVDA fizesse solicitações de IA duplicadas para objetos já rotulados em vez de anunciar o rótulo existente.
- **Bate-Papo de Documentos para Provedores não-Gemini**: Corrigida uma verificação rigorosa da chave de API no Bate-Papo de Documentos (`on_ask`) para garantir que usuários do OpenAI, Groq ou provedores Personalizados locais (como o Ollama) possam conversar com documentos com sucesso sem serem bloqueados.
- **Tradução Rápida de OCR do Chrome**: Restaurada a API de tradução gratuita e sem necessidade de chave para o OCR do Chrome. A tradução do texto extraído agora ignora a IA do Gemini, economizando cotas de API e acelerando o processo de tradução.
- **Filtro Alfanumérico do CAPTCHA**: Corrigida a lógica de filtragem no resolutor de CAPTCHA para garantir que os caracteres não alfanuméricos sejam devidamente limpos em todas as situações.
- **Atualização da Ajuda da Camada de Comandos**: Corrigido o atalho do anúncio de status no menu de ajuda de `L` para `I` e adicionados ambos os comandos de rotulagem (`L` e `Shift+L`) à lista.

## Alterações para 4.6

- **Correção do Raciocínio dos Modelos Gemma 4**: Corrigido um problema com os modelos Gemma 4 onde todo o processo de pensamento interno era exibido como resposta final, ou onde desativar o raciocínio resultava em respostas em branco. O complemento agora isola e extrai corretamente apenas a resposta de texto limpa final.
- **OCR em Lote no Explorador de Arquivos**: Agora você pode selecionar várias fotos ou PDFs diretamente no Explorador de Arquivos do Windows e extrair texto ou analisá-los em lote. O complemento filtrará e processará automaticamente apenas os formatos de arquivo suportados.

## Alterações para 4.5

- **Integração Universal de IA Local (Configurar IA Local)**: Adicionado um novo botão **"Configurar IA Local"** nas Configurações do Provedor Personalizado. Os usuários agora podem configurar automaticamente motores de IA locais, incluindo **Ollama**, **LM Studio**, **Jan.ai** e **KoboldCPP** de forma instantânea.
- **Bypass Inteligente de Proxy Local**: Reconstruída a lógica de conexão com um mecanismo avançado de bypass de proxy. O complemento agora é inteligente o suficiente para ignorar completamente os proxies do sistema Windows para conexões de loopback locais, garantindo conexões estáveis com a IA local mesmo quando sua VPN ou modo TUN estiver ativo.
- **Rotulagem por IA Ultraestável (v2)**: Substituição das chaves de coordenadas absolutas de tela por um sistema híbrido e avançado de **Assinatura de Objeto**. Os rótulos dependem agora de identificadores programáticos (UIA **AutomationId** ou Win32 **ControlID**) e de coordenadas relativas à janela, tornando seus rótulos personalizados completamente resistentes ao redimensionamento de janelas, à movimentação, à alteração de monitor ou de escala.
- **Migração Automática e Transparente de Rótulos**: A atualização é totalmente transparente. O complemento migrará automaticamente seus rótulos antigos baseados em coordenadas para o novo formato estável de impressão digital em segundo plano assim que você focar o objeto pela primeira vez, com zero perda de dados.

## Alterações para 4.0.3

- **Apresentando a Rotulagem Semântica por IA**: Os usuários agora podem rotular permanentemente botões e ícones sem nome utilizando a IA. Pressione **L** para rotular o objeto de navegação atual (suportando tanto o foco do Tab quanto a navegação por objetos) ou **Shift+L** para analisar e rotular todo o aplicativo de uma só vez.
- **Gerenciamento Inteligente de Rótulos**: Adicionada uma nova caixa de diálogo do Gerenciador de Rótulos totalmente acessível (através de **Shift+L** se existirem rótulos) para ver, renomear ou excluir rótulos personalizados em lote.
- **Análise Direta de Arquivos (Bypass da Caixa de Diálogo de Arquivos)**: O complemento agora é inteligente o suficiente para detectar se você está focado em um arquivo PDF ou de imagem no Explorador de Arquivos do Windows. Pressionar **F (Ação Inteligente de Arquivo)** ou **D (Leitor de Documentos)** em um arquivo selecionado irá processá-lo imediatamente, ignorando completamente a caixa de diálogo padrão "Abrir".

## Alterações para 4.0.1

- **Adicionado Motor OCR "Nenhum (Extrair Camada de Texto)"**: Os usuários podem agora extrair texto diretamente de PDFs pesquisáveis sem utilizar créditos de IA, melhorando significativamente a velocidade e a privacidade para documentos baseados em texto.
- **Precisão Refinada do Explorador de UI**: Aprimorado o prompt do Explorador de UI para identificar melhor os tipos de elementos (como Itens de Lista) e relatar com precisão estados como "(Marcado)", "(Selecionado)" ou "(Expandido)", ignorando os componentes do sistema Windows como a Barra de Tarefas e o Relógio.
- **Lembrete de Configuração de Instalação**: Adicionada uma notificação após a instalação para guiar os usuários ao menu de configurações para configurarem suas chaves de API e preferências.

## Alterações para 3.6.0

- **Correção na Digitação do Operador de IA:** Corrigido um erro onde a letra 'v' era digitada em vez de colar o texto em determinados sistemas. Esta correção resolve conflitos de temporização que ocorriam durante uma carga elevada do sistema.
- **Estabilidade Aprimorada:** Adicionado um tratamento de erros robusto para operações na área de transferência para evitar falhas do complemento quando a área de transferência do sistema estiver temporariamente bloqueada por outros aplicativos.
- **Otimização de Temporização:** Ajustados os atrasos internos para eventos de teclado de modo a garantir maior confiabilidade em diferentes velocidades do sistema e melhor compatibilidade com Gerenciadores da Área de Transferência de terceiros.

## Alterações para 3.5.0

- **Operador de IA (Controle Autônomo - Shift+A):** Esta é a joia da coroa da v5.5. O Vision Assistant Pro deixou de ser um assistente passivo para se tornar seu **Operador de IA** pessoal. Ele não se limita a descrever a tela — ele assume o comando.
  - _Como funciona:_ Você agora pode dar instruções por texto ou voz para operar seu PC. Por exemplo, em um aplicativo completamente inacessível onde seu leitor de tela permanece em silêncio, você pode pressionar **Shift+A** e digitar: _"Clique no botão Configurações"_ ou _"Encontre o campo de pesquisa, digite 'Últimas Notícias' e pressione Enter."_ A IA identifica visualmente os elementos, move o mouse e executa a tarefa por você.
  - _Nota de Desempenho:_ Este recurso está otimizado para o **Gemini 3.0 Flash (Preview)**, oferecendo respostas incrivelmente rápidas e inteligentes que conseguem lidar até com os layouts de interface de usuário mais complexos.
  - **⚠️ Aviso de Uso da API:** Como o Operador de IA precisa "ver" exatamente o que está acontecendo para ser preciso, ele envia uma captura de tela de alta resolução a cada passo. Observe que o uso frequente consumirá sua cota de API muito mais rapidamente do que as tarefas normais de texto.
- **Explorador Visual de UI (E):** Cansado de navegar por "botões sem rótulo"? Pressione **E** para ativar o Explorador de UI. A IA analisará toda a janela e gerará uma lista de cada elemento clicável que encontrar — incluindo ícones, gráficos e menus. Basta escolher um item da lista e o Operador de IA clicará nele para você. É como ter uma "camada acessível" sobre qualquer aplicativo.
- **Ação Inteligente de Arquivo com Sensibilidade ao Contexto (F):** A tecla "F" foi completamente reformulada. Ela não assume mais que você quer apenas OCR. Ao selecionar uma única imagem, agora pergunta inteligentemente qual é a sua intenção: você pode escolher uma **Descrição Visual Detalhada** para entender a cena ou uma **Extração de Texto Estruturada (OCR)** para leitura. O menu adapta-se dinamicamente com base no tipo de arquivo e no seu motor de IA ativo.
- **Otimização Principal:** Realizamos uma limpeza profunda da lógica interna do complemento, removendo funções legadas não utilizadas e código redundante. Isso resulta em uma experiência mais leve, rápida e confiável para todos os usuários.

## Alterações para 3.1.0

- **Arquitetura Multiprovedor**: Adicionado suporte total para **OpenAI**, **Groq** e **Mistral**, em conjunto com o Google Gemini. Os usuários agora podem escolher sua plataforma de IA preferida.
- **Roteamento Avançado de Modelos**: Os usuários de provedores nativos (Gemini, OpenAI, etc.) podem agora selecionar modelos específicos em um menu suspenso para diferentes tarefas (OCR, STT, TTS).
- **Configuração Avançada de Endpoints**: Os usuários de provedores personalizados podem inserir manualmente URLs específicas e nomes de modelos para um controle detalhado sobre servidores locais ou de terceiros.
- **Visibilidade Inteligente de Recursos**: O menu de configurações e a interface do Leitor de Documentos agora ocultam automaticamente os recursos não suportados (como o TTS) com base no provedor selecionado.
- **Busca Dinâmica de Modelos**: O complemento obtém agora a lista de modelos disponíveis diretamente da API do provedor, garantindo compatibilidade com novos modelos assim que são lançados.
- **OCR e Tradução Híbridos**: Otimizada a lógica para utilizar o Google Tradutor para maior velocidade ao usar o OCR do Chrome, e tradução baseada em IA ao utilizar os motores Gemini/Groq/OpenAI.
- **"Analisar Novamente com IA" Universal**: O recurso de reanalisar do Leitor de Documentos não está mais limitado ao Gemini. Ele agora utiliza qualquer provedor de IA que estiver ativo no momento para reprocessar as páginas.

## Alterações para 3.0

- **Recuperação Interativa de Resultados:** Adicionada a tecla **Espaço** à camada de comandos, permitindo aos usuários reabrir instantaneamente a última resposta da IA em uma janela de bate-papo para perguntas adicionais, mesmo quando o modo "Saída Direta" estiver ativo.
- **Central da Comunidade no Telegram:** Adicionado um link para o "Canal Oficial no Telegram" no menu Ferramentas do NVDA, proporcionando uma forma rápida de se manter atualizado com as últimas notícias, recursos e lançamentos.
- **Estabilidade de Resposta Aprimorada:** Otimizada a lógica principal para os recursos de Tradução, OCR e Visão para garantir um desempenho mais confiável e uma experiência mais fluida ao utilizar a saída direta de voz.
- **Orientação de Interface Aprimorada:** Atualizadas as descrições das configurações e a documentação para explicar melhor o novo sistema de recuperação de histórico e como ele funciona junto com as configurações de saída direta.

## Alterações para 2.9

- **Gerenciador Avançado de Prompts:** Introduzida uma caixa de diálogo de gerenciamento dedicada nas configurações para personalizar os prompts padrão do sistema e gerenciar prompts definidos pelo usuário, com suporte total para adicionar, editar, reordenar e pré-visualizar.
- **Suporte Abrangente a Proxy:** Resolvidos problemas de conexão de rede garantindo que as configurações de proxy definidas pelo usuário sejam rigorosamente aplicadas a todas as requisições de API, incluindo tradução, OCR e geração de voz.
- **Migração Automática de Dados:** Integrado um sistema de migração inteligente para atualizar automaticamente configurações de prompts antigas para um formato JSON v2 robusto na primeira execução, sem perda de dados.
- **Compatibilidade Atualizada (2025.1):** Definida a versão mínima do NVDA necessária para 2025.1 devido a dependências de bibliotecas em recursos avançados como o Leitor de Documentos, garantindo um desempenho estável.
- **Interface de Configurações Otimizada:** Simplificada a interface de configurações ao reorganizar o gerenciamento de prompts em uma caixa de diálogo separada, proporcionando uma experiência de uso mais limpa e acessível.
- **Guia de Variáveis de Prompt:** Adicionado um guia integrado nas caixas de diálogo de prompt para ajudar os usuários a identificar e utilizar facilmente variáveis dinâmicas como [selection], [clipboard] e [screen_obj].

## Alterações para 2.8

- **Resiliência de Rede Aprimorada:** Adicionado um mecanismo de nova tentativa automática para lidar melhor com conexões de internet instáveis e erros temporários do servidor, garantindo respostas de IA mais confiáveis.
- **Janela de Tradução Visual:** Introduzida uma janela dedicada para os resultados de tradução. Os usuários podem agora navegar facilmente e ler traduções longas linha por linha, de forma semelhante aos resultados de OCR.
- **Visualização Formatada Agregada:** O recurso "Ver Formatado" no Leitor de Documentos exibe agora todas as páginas processadas em uma única janela organizada, com cabeçalhos de página claros.
- **Fluxo de Trabalho de OCR Otimizado:** Ignora automaticamente a seleção de intervalo de páginas para documentos de página única, tornando o processo de reconhecimento mais rápido e fluido.
- **Estabilidade da API Aprimorada:** Alterado para um método de autenticação baseado em cabeçalho mais robusto, resolvendo potenciais erros de "Todas as chaves de API falharam" causados por conflitos na rotação de chaves.
- **Correções de Erros:** Resolvidas várias falhas potenciais, incluindo um problema durante o encerramento do complemento e um erro de foco na caixa de diálogo de bate-papo.

## Alterações para 6.5.0

- **Leitor Avançado de Documentos:** Um novo e potente visualizador de PDF e imagens com seleção de intervalo de páginas, processamento em segundo plano e navegação fluida com `Ctrl+PageUp/PageDown`.
- **Novo Submenu de Ferramentas:** Adicionado um submenu dedicado "Vision Assistant" no menu Ferramentas do NVDA para um acesso mais rápido aos recursos principais, configurações e documentação.
- **Personalização Flexível:** Você pode agora escolher seu motor de OCR e voz TTS preferidos diretamente no painel de configurações.
- **Suporte a Múltiplas Chaves de API:** Adicionado suporte para várias chaves de API do Gemini. Você pode inserir uma chave por linha ou separá-las por vírgulas nas configurações.
- **Motor OCR Alternativo:** Introduzido um novo motor de OCR para garantir um reconhecimento de texto confiável mesmo ao atingir os limites de cota da API do Gemini.
- **Rotação Inteligente de Chaves de API:** Alterna automaticamente para a chave de API funcional mais rápida e memoriza-a para ultrapassar os limites de cota.
- **Documento para MP3/WAV:** Recurso integrado para gerar e salvar arquivos de áudio de alta qualidade nos formatos MP3 (128kbps) e WAV diretamente no leitor.
- **Suporte a Stories do Instagram:** Adicionada a capacidade de descrever e analisar Stories do Instagram utilizando suas URLs.
- **Suporte ao TikTok:** Introduzido suporte para vídeos do TikTok, permitindo uma descrição visual completa e transcrição de áudio dos vídeos.
- **Janela de Atualização Redesenhada:** Apresenta uma nova interface acessível com uma caixa de texto rolável para ler claramente as alterações de versão antes de instalar.
- **Status e UX Unificados:** Caixas de diálogo de arquivo padronizadas em todo o complemento e aprimoramento do comando 'L' para relatar o progresso em tempo real.

## Alterações para 2.6

- **Sistema de Ajuda:** Adicionado um comando de ajuda (`H`) na Camada de Comandos para fornecer uma lista de fácil acesso com todos os atalhos e suas respectivas funções.
- **Análise de Vídeos Online:** Expandido o suporte para incluir vídeos do **Twitter (X)**. Também foram melhoradas a detecção de URLs e a estabilidade para uma experiência mais confiável.
- **Contribuição para o Projeto:** Adicionada uma caixa de diálogo opcional de doação para usuários que desejem apoiar as futuras atualizações e o crescimento contínuo do projeto.

## Alterações para 2.5

\*   \*\*Camada de Comandos:\*\* Introduzido um sistema de Camada de Comandos (padrão: `NVDA+Shift+V`) para agrupar atalhos sob uma única tecla principal. Por exemplo, em vez de pressionar `NVDA+Control+Shift+T` para traduzir, você agora pressiona `NVDA+Shift+V` seguido de `T`.
\*   \*\*Análise de Vídeos Online:\*\* Adicionado um novo recurso para analisar vídeos do YouTube e Instagram diretamente fornecendo uma URL.

## Alterações para 2.1.1

- **Modo de Saída Direta:** Adicionada uma opção para ignorar a caixa de diálogo de bate-papo e ouvir as respostas da IA diretamente por voz, proporcionando uma experiência mais rápida e fluida.
- **Integração com a Área de Transferência:** Adicionada uma nova configuração para copiar automaticamente as respostas da IA para a área de transferência.

## Alterações para 2.1

- **Novos Idiomas:** Adicionadas traduções para **Persa** e **Vietnamita**.
- **Modelos de IA Expandidos:** Reorganizada a lista de seleção de modelos com prefixos claros (`[Free]`, `[Pro]`, `[Auto]`) para ajudar os usuários a distinguir entre modelos gratuitos e modelos com limite de taxa (pagos). Adicionado suporte para o **Gemini 3.0 Pro** e **Gemini 2.0 Flash Lite**.
- **Estabilidade do Ditado:** Melhoria significativa na estabilidade do Ditado Inteligente. Adicionada uma verificação de segurança para ignorar clipes de áudio com menos de 1 segundo, evitando alucinações da IA e erros de resposta em branco.
- **Gerenciamento de Arquivos:** Corrigido um problema em que o envio de arquivos com nomes em caracteres não-ingleses falhava.
- **Otimização de Prompts:** Melhorada a lógica de Tradução e a estrutura dos resultados de Visão.

## Alterações para 2.0

- **Adicionadas traduções para Francês e Turco.**
- **Visualização Formatada:** Adicionado o botão "Ver Formatado" nas caixas de diálogo de bate-papo para visualizar a conversa com a devida formatação (Cabeçalhos, Negrito, Código) em uma janela navegável padrão.
- **Configuração de Markdown:** Adicionada a nova opção "Limpar Markdown no Bate-Papo" nas Configurações. Desmarcar esta opção permite aos usuários verem a sintaxe Markdown pura (ex.: `**`, `#`) na janela de bate-papo.
- **Gerenciamento de Janelas:** Corrigido um problema em que as janelas de "Refinar Texto" ou de bate-papo abriam múltiplas vezes ou falhavam ao colocar o foco corretamente.
- **Melhorias na Experiência do Usuário:** Padronizados os títulos das caixas de diálogo de arquivos para "Abrir" e removidos anúncios de voz redundantes (ex.: "Abrindo menu...") para uma navegação mais fluida.

## Alterações para 1.5

- Adicionada tradução para Italiano.
- **Relatório de Status:** Adicionado um novo comando (NVDA+Control+Shift+I) para anunciar o status atual do complemento (ex.: "Enviando...", "Analisando...").
- **Exportação em HTML:** O botão "Salvar Conteúdo" nas caixas de diálogo de resultados salva agora a saída como um arquivo HTML formatado, preservando estilos como cabeçalhos e texto em negrito.
- **Interface de Configurações:** Melhorada a disposição do painel de Configurações com agrupamentos acessíveis.
- **Novos Modelos:** Adicionado suporte para gemini-flash-latest e gemini-flash-lite-latest.
- **Idiomas:** Adicionado o Nepalês à lista de idiomas suportados.
- **Lógica do Menu de Refinamento:** Corrigido um erro crítico em que os comandos de "Refinar Texto" falhavam se o idioma da interface do NVDA não fosse o Inglês.
- **Ditado:** Melhorada a detecção de silêncio para evitar a geração de texto incorreto quando não há entrada de voz.
- **Configurações de Atualização:** A opção "Procurar atualizações ao iniciar" está agora desativada por padrão para cumprir as políticas da Loja de Complementos do NVDA.
- Limpeza de Código.

## Alterações para 1.0

- Migrada a estrutura do projeto para o modelo oficial de complementos da NV Access para melhor conformidade com os padrões.
- Implementada lógica de nova tentativa automática para erros HTTP 429 (Limite de Taxa Excedido) para garantir a confiabilidade durante períodos de tráfego elevado.
- Otimizadas as prompts de tradução para maior precisão e melhor gerenciamento da lógica de "Troca Inteligente".
- Atualizada a tradução para Russo.

## Alterações para 6.0

- Adicionado suporte à tradução em Russo (Agradecimentos a nvda-ru).
- Atualizadas as mensagens de erro para fornecer informações mais descritivas relativamente à conectividade.
- Alterado o idioma de destino padrão para Inglês.

## Alterações para 5.6

- Adicionado o Comando de OCR de Arquivo Nativo (NVDA+Control+Shift+F).
- Adicionado o botão "Salvar Bate-Papo" às caixas de diálogo de resultados.
- Implementado suporte completo de internacionalização (i18n).
- Migrado o retorno sonoro para o módulo nativo de tons do NVDA.
- Alterado para a API de Arquivos do Gemini para um melhor manuseio de arquivos PDF e de áudio.
- Corrigida uma falha (crash) ao traduzir textos que contêm chaves.

## Alterações para 2026.10.01

- Corrigido um problema em que a variável [file_ocr] não funcionava corretamente dentro das Prompts Personalizadas.

## Alterações para 2026.09.01

- Padronizados todos os atalhos para utilizar NVDA+Control+Shift de modo a eliminar conflitos com o layout para Notebook do NVDA e teclas de atalho do sistema.

## Alterações para 2.7

- Implementado um sistema integrado de Atualização Automática.
- Adicionada a Cache de Tradução Inteligente para recuperação instantânea de texto traduzido anteriormente.
- Adicionada Memória de Conversa para refinar contextualmente os resultados nas caixas de diálogo de bate-papo.
- Adicionado comando dedicado para Tradução da Área de Transferência (NVDA+Control+Shift+Y).
- Otimizadas as prompts da IA para impor rigorosamente a saída no idioma de destino.
- Corrigida uma falha causada por caracteres especiais no texto de entrada.

## Alterações para 6.1.2

- Adicionado suporte para mais de 20 novos idiomas.
- Implementada a Caixa de Diálogo Interativa de Refinamento para perguntas adicionais.
- Adicionado o recurso nativo de Ditado Inteligente.
- Adicionada a categoria "Vision Assistant" à caixa de diálogo de Gestos de Entrada do NVDA.
- Corrigidas falhas por COMError em aplicativos específicos como o Firefox e o Word.
- Adicionado mecanismo de nova tentativa automática para erros do servidor.

## Alterações para 7.0.0

- Lançamento inicial.
