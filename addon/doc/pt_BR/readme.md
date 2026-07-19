# Documentação do Vision Assistant Pro

O **Vision Assistant Pro** é um assistente de IA multimodal avançado para o NVDA. Ele utiliza mecanismos de IA de classe mundial para fornecer leitura de tela inteligente, tradução, ditado por voz e análise de documentos.

_Este complemento foi lançado para a comunidade em homenagem ao Dia Internacional das Pessoas com Deficiência._

## 1. Configuração

Vá para **Menu do NVDA > Preferências > Configurações > Vision Assistant Pro**.

### 1.1 Configurações de Conexão

- **Provedor:** Selecione o seu serviço de IA de preferência. Os provedores suportados incluem **Google Gemini**, **OpenAI**, **Mistral**, **Groq**, **MiniMax** e **Personalizado** (servidores compatíveis com OpenAI, como Ollama, LM Studio, Jan.ai ou KoboldCPP).
- **Nota Importante:** Recomendamos fortemente o uso do **Google Gemini** para obter o melhor desempenho e precisão (especialmente para análise de imagens/arquivos).
- **Chave de API:** Obrigatória. Você pode inserir várias chaves (separadas por vírgulas ou quebras de linha) para rotação automática.
- **Buscar Modelos:** Após inserir sua chave de API, pressione este botão para baixar a lista mais recente de modelos disponíveis do provedor.
- **Modelo de IA:** Selecione o modelo principal usado para chat geral e análise.

### 1.2 Roteamento Avançado de Modelos

*Disponível para todos os provedores, incluindo Gemini, OpenAI, Groq, Mistral e Personalizado._

> **⚠️ Aviso:** Estas configurações são destinadas **apenas para usuários avançados**. Se você não tiver certeza do que um modelo específico faz, por favor, deixe esta opção **desmarcada**. Selecionar um modelo incompatível para uma tarefa (por exemplo, um modelo apenas de texto para Visão) causará erros e fará o complemento parar de funcionar.

Marque **"Roteamento Avançado de Modelos (Específico por Tarefa)"** para liberar o controle detalhado. Isso permite que você selecione modelos específicos na lista suspensa para diferentes tarefas:

- **Modelo de OCR / Visão:** Escolha um modelo especializado para analisar imagens.
- **Conversão de Fala em Texto (STT):** Escolha um modelo específico para ditado.
- **Conversão de Texto em Fala (TTS):** Escolha um modelo para gerar áudio.
- **Modelo do Operador de IA:** Selecione un modelo específico para tarefas de operação autônoma do computador.
- **Modelo de Vídeo:** Selecione um modelo específico para análise de vídeo e geração de audiodescrição.
_Nota: Recursos não suportados (por exemplo, TTS para o Groq) serão ocultados automaticamente._

### 1.3 Configuração Avançada de Endpoint (Provedor Personalizado)

*Disponível apenas quando "Personalizado" estiver selecionado._

> **⚠️ Aviso:** Esta seção permite a configuração manual da API e foi projetada para **usuários experientes** que executam servidores locais ou proxies. URLs ou nomes de modelos incorretos interromperão a conectividade. Se você não sabe exatamente o que são esses endpoints, mantenha isso **desmarcado**.

Marque **"Configuração Avançada de Endpoint"** para inserir manualmente os detalhes do servidor. Diferente dos provedores nativos, aqui você deve **digitar** as URLs e os Nomes dos Modelos específicos:

- **URL da Lista de Modelos:** O endpoint para buscar os modelos disponíveis.
- **URL do Endpoint de OCR/STT/TTS:** URLs completas para serviços específicos (por exemplo, `http://localhost:11434/v1/audio/speech`).
- **Modelos Personalizados:** Digite manualmente o nome do modelo (por exemplo, `llama3:8b`) para cada tarefa.

### 1.3.1 Configurar IA Local (Configuração em Uma Ação)

Para tornar a integração de IA local e totalmente offline extremamente simples, um botão dedicado **"Configurar IA Local"** está disponível dentro das Configurações do Provedor Personalizado.

Se você estiver executando um servidor de modelo de IA local no seu computador:

1. Selecione **Personalizado** como seu Provedor.
2. Pressione o botão **Configurar IA Local**.
3. Escolha o seu mecanismo de IA local na caixa de diálogo acessível:
   - **Ollama** (padrão para `http://127.0.0.1:11434`)
   - **LM Studio** (padrão para `http://127.0.0.1:1234`)
   - **Jan.ai** (padrão para `http://127.0.0.1:1337`)
   - **KoboldCPP** (padrão para `http://127.0.0.1:5001`)
4. O complemento configurará instantaneamente a URL local correta, o tipo de API e buscará automaticamente seus modelos offline ativos para preencher a caixa de seleção **Modelo de IA**.

_Nota sobre Rede e Proxies:_ Este mecanismo de conexão local possui um sistema avançado de desvio de proxy. Mesmo que você esteja usando uma VPN de sistema ativa ou um proxy em modo TUN, suas requisições de IA locais irão ignorá-lo completamente, garantindo conexões offline estáveis sem erros do tipo "502 Bad Gateway".

### 1.4 Preferências Gerais

- **Mecanismo de OCR:** Escolha entre **Chrome (Rápido)** para resultados céleres ou **IA (Avançado)** para uma preservação superior do layout.
- **Voz do TTS:** Selecione o seu estilo de voz preferido. Esta lista é atualizada dinamicamente com base no seu provedor ativo.
- **Criatividade (Temperatura):** Controla a aleatoriedade da IA. Valores mais baixos são melhores para traduções/OCR mais precisos.
- **URL do Proxy:** Configure isso se os serviços de IA forem restritos na sua região (suporta proxies locais como `127.0.0.1` ou URLs de ponte).
- **Saída Direta (Sem Janela de Chat):** Marque isso se você quiser que a IA apenas leia o resultado em voz alta sem abrir uma janela de chat interativa.
- **Copiar respostas da IA para a área de transferência:** Copia automaticamente cada resposta da IA para a área de transferência do seu sistema para facilitar a colagem.
- **Limpar Markdown no Chat:** Desmarque isso se preferir ver os símbolos de formatação brutos em vez de uma visualização de texto limpa e formatada.

## 2. Camada de Comando e Atalhos

Para evitar conflitos de teclado, este complemento usa uma **Camada de Comando**.

1. Pressione **NVDA + Shift + V** (Tecla Mestra) para ativar a camada (você ouvirá um bipe).
2. Solte as teclas e pressione uma das seguintes teclas individuais:

| Tecla           | Função                         | Descrição                                                                                                       |
| --------------- | ------------------------------ | --------------------------------------------------------------------------------------------------------------- |
| **Shift + A**   | **Operador de IA**             | **Operação Autônoma:** Diga à IA para realizar uma tarefa na sua tela. Pressionar novamente aborta a operação.  |
| **E**           | **Explorador de IU**           | **Clique Interativo:** Identifica e clica em elementos de interface em qualquer aplicativo.                     |
| **T**           | Tradutor Inteligente           | Traduz o texto sob o cursor de navegação ou seleção.                                                            |
| **Shift + T**   | Tradutor de Área de Transf.    | Traduz o conteúdo atualmente na área de transferência.                                                          |
| **R**           | Refinador de Texto             | Resume, corrige gramática, explica ou executa **Comandos Personalizados**.                                      |
| **V**           | Visão de Objeto                | Descreve o objeto de navegação atual.                                                                           |
| **O**           | Visão de Tela Cheia            | Analisa o layout e o conteúdo de toda a tela.                                                                   |
| **Shift + V**   | Análise de Vídeo               | Analisa arquivos de vídeo locais ou vídeos online do **YouTube**, **Instagram**, **TikTok** ou **Twitter (X)**. |
| **Control + V** | Gravação de Vídeo Local        | Grava um vídeo silencioso da sua tela e analisa as ações e o layout.                                            |
| **D**           | Leitor de Documentos           | Leitor avançado para PDFs e imagens com seleção de intervalo de páginas.                                        |
| **F**           | **Ação de Arquivo Intel.**     | Reconhecimento contextual de arquivos de imagem, PDF ou TIFF selecionados.                                      |
| **A**           | Transcrição de Áudio           | Transcreve arquivos MP3, WAV ou OGG em texto.                                                                   |
| **C**           | Solucionador de CAPTCHA        | Captura e resolve CAPTCHAs (Suporta portais governamentais).                                                    |
| **S**           | Ditado Inteligente             | Converte fala em texto. Pressione para iniciar a gravação, e novamente para parar/digitar.                      |
| **Control+L**   | **Assistente ao Vivo**         | **Copiloto em Tempo Real (Apenas Gemini):** Inicia ou encerra uma conversa de voz e tela com a IA.              |
| **I**           | Relatório de Status            | Anuncia o progresso atual (por exemplo, "Escaneando...", "Inativo").                                            |
| **L**           | **Rotular Objeto**             | **Rotulagem Semântica por IA:** Rotula permanentemente o elemento/ícone atualmente focado.                      |
| **Shift + L**   | **Gerenciar/Escanear Rótulos** | Abre o Gerenciador de Rótulos (se existirem) ou escaneia o aplicativo em busca de elementos sem nome.           |
| **U**           | Verificar Atualizações         | Verifica manualmente o GitHub em busca da versão mais recente do complemento.                                   |
| **Espaço**      | Chamar Último Resultado        | Mostra a última resposta da IA em uma janela de chat para revisão ou acompanhamento.                            |
| **H**           | Ajuda de Comandos              | Exibe uma lista com todos os atalhos disponíveis.                                                               |
| **Alt + S**     | Configurações                  | Abre a caixa de diálogo de configurações do Vision Assistant Pro.                                               |
| **Alt + Q**     | Relatório de Cota Esgotada     | Relata o número de chaves de API do Gemini que excederam a cota diária e o tempo de redefinição delas.          |
| **Alt + M**     | Auditoria de Roteamento        | Relata os modelos de IA atualmente selecionados no roteamento avançado.                                         |

## 3. Operador de IA - Controle Autônomo de Computador

O **Operador de IA** transforma o Vision Assistant Pro de um leitor passivo em um assistente ativo que pode interagir com o computador em seu nome. Você pode pedir para ele descrever a tela, responder a perguntas sobre o que ele vê ou até mesmo assumir o controle — clicando em botões, arrastando itens, digitando texto e navegando pelos aplicativos usando comandos em linguagem natural.

A maior vantagem? Ele funciona perfeitamente em softwares completamente inacessíveis. Se você estiver travado em um aplicativo proprietário, em uma área de trabalho remota ou em um site onde o seu leitor de tela fica totalmente silencioso, o operador não se importa. Como ele "vê" a tela visualmente, ele consegue encontrar, ler e interagir com elementos que possuem zero rótulos de acessibilidade.

### Como Funciona

1. Pressione **NVDA + Shift + V**, depois pressione **Shift + A** (or use o atalho direto) para abrir a caixa de diálogo do Operador de IA.
2. Digite o que deseja fazer em linguagem simples (por exemplo, "Clique no botão Salvar", "O que diz a mensagem de erro?" ou "Renomeie o arquivo para final.pdf").
3. A IA analisará sua tela, identificará os elementos relevantes e executará a ação ou fornecerá a resposta. Se uma tarefa exigir várias etapas, o operador continuará trabalhando até que ela seja concluída.
4. Pressione **Shift + A** novamente a qualquer momento para abortar instantaneamente uma operação em andamento.

### Ações Suportadas

O operador compreende uma ampla gama de comandos:

- **Descrever e Responder**: "Descreva o layout da tela" ou "O que diz a mensagem de erro?"
- **Clicar**: "Clique no botão Salvar"
- **Clique com o Botão Direito**: "Clique com o botão direito no arquivo"
- **Clique Duplo**: "Clique duas vezes no documento"
- **Arrastar e Soltar**: "Arraste o documento para a pasta Arquivo"
- **Digitar**: "Digite 'Olá Mundo' na caixa de pesquisa"
- **Rolar**: "Role para baixo três vezes"
- **Pressionar Teclas**: "Pressione Enter", "Pressione Tab", "Pressione Escape"
- **Tarefas de Várias Etapas**: "Abra o Explorador de Arquivos, encontre o relatório e renomeie-o para final.pdf"

### Notas Importantes

- **⚠️ Aviso de Uso da API**: Como o operador precisa "ver" exatamente o que está acontecendo na tela, ele envia uma captura de tela de alta resolução a cada etapa. O uso frequente consumirá sua cota de API muito mais rápido do que os recursos padrão baseados em texto.
- **Aplicativos com Privilégios de Administrador**: Se o NVDA não estiver sendo executado com privilégios de Administrador, o operador pode não conseguir interagir com janelas que exigem permissões elevadas. Esta é uma limitação de segurança do Windows, não um bug do complemento.
- **Boas Práticas**: Para obter os melhores resultados, dê comandos claros e específicos. "Clique no botão azul Enviar na parte inferior do formulário" quase sempre funcionará melhor do que apenas "Clique no botão".

## 4. Análise de Vídeo e Audiodescrição

> **Nota:** Os recursos de Análise de Vídeo e Audiodescrição são movidos estritamente pelo provedor **Google Gemini**. Certifique-se de que o seu provedor ativo nas configurações do complemento esteja definido como Google Gemini.

O Vision Assistant Pro introduz recursos poderosos de processamento de vídeo projetados especificamente para usuários cegos. Ele pode analisar tanto vídeos online quanto gravações de tela locais para fornecer descrições visuais altamente detalhadas e gerar roteiros profissionais de Audiodescrição (SRT).

### 4.1 Gravação de Tela Local (Control + V)

Se você se deparar com um vídeo silencioso, uma animação ou um tutorial na sua tela, você pode capturá-lo diretamente:

1. Pressione **NVDA + Shift + V** para entrar na Camada de Comando, e depois pressione **Control + V**.
2. O complemento gravará silenciosamente a sua tela em segundo plano.
3. Pressione **Control + V** novamente para parar a gravação.
4. A IA irá então analisar o segmento de vídeo gravado e fornecerá uma descrição altamente detalhada da cena, dos personagens e das ações.

### 4.2 Análise de Vídeo (Shift + V)

Você pode analisar tanto arquivos de vídeo locais quanto vídeos online. Basta selecionar um arquivo de vídeo local no Windows Explorer ou copiar o link de um vídeo online para a sua área de transferência. Você também pode pressionar **Shift + V** em qualquer lugar (como dentro de um player de mídia) para abrir uma caixa de diálogo onde poderá navegar por um arquivo de vídeo ou colar uma URL manualmente.

- **Plataformas Online Suportadas:** YouTube, Instagram, TikTok e Twitter (X).
- A IA detectará automaticamente o arquivo local ou a URL, processará o vídeo e fornecerá uma descrição visual abrangente e um resumo do áudio.

### 4.3 Geração de Audiodescrição (SRT)

Para uma experiência mais estruturada, o complemento pode gerar roteiros profissionais de Audiodescrição no formato padrão SubRip (SRT).

- **Sincronização Inteligente de Intervalos:** A IA ouve a faixa de áudio e ancora especificamente suas descrições visuais nas pausas naturais e intervalos de silêncio para minimizar de forma inteligente a sobreposição com os diálogos.
- **Rastreamento de Personagens:** O mecanismo realiza uma varredura prévia para extrair personagens distintos com base em características faciais imutáveis. Ele constrói um dicionário global para rastrear e rotular com precisão os personagens em diferentes cenas, sem confusões.
- **OCR de Texto Literal:** Qualquer texto que apareça na tela (placas, celulares, créditos) é estritamente citado de forma literal.
- **Como Usar:** Para ouvir a legenda gerada, basta colocar o arquivo `.srt` na mesma pasta do seu arquivo de vídeo e dar a ele exatamente o mesmo nome. Em seguida, configure seu player de mídia (por exemplo, VLC ou PotPlayer) para direcionar o texto da legenda diretamente para o seu leitor de tela ou mecanismo de TTS durante a reprodução.

### 4.4 Narração de Áudio Sincronizada (Exportação para MP3)

Além de apenas criar arquivos SRT baseados em texto, o complemento funciona como uma ferramenta completa de produção de Audiodescrição, sintetizando as descrições em fala e mixando-as com o vídeo. Ao gerar um MP3 para arquivos de vídeo locais, você tem vários modos de mixagem:

- **AD Padrão (Mixar Voz):** A narração é sobreposta diretamente ao áudio do vídeo. Você será perguntado se deseja aplicar o **Audio Ducking** (reduzir o volume do fundo durante as descrições) para garantir que a narração fique clara.
- **AD Estendida (Pausar Áudio):** O mecanismo pausa o áudio do vídeo original durante as descrições, garantindo que você nunca perca uma única palavra do diálogo original ou da narração da IA.
- **Vídeos do YouTube:** Para fontes do YouTube (que não são baixadas localmente), a exportação em MP3 conterá estritamente a faixa de voz da IA sincronizada, sem o áudio do vídeo de fundo.

## 5. Leitor Avançado de Documentos e Imagens

O Vision Assistant Pro inclui um Leitor de Documentos altamente otimizado, projetado para PDFs de várias páginas, imagens complexas e até formatos HEIC do iPhone.

### 5.1 Processamento em Lote e Retomada

Você não precisa ler um documento enorme de uma só vez. Insira um intervalo de páginas (por exemplo, `1-20`) e a IA processará todas as páginas em segundo plano. Se o NVDA travar ou você interromper a varredura, o complemento se lembrará do seu progresso e oferecerá a opção de **Retomar** exatamente de onde você parou!

### 5.2 Ação de Arquivo Inteligente

Você nem sempre precisa abrir o documento primeiro. No Explorador de Arquivos do Windows, basta destacar um PDF ou imagem e pressionar **D** (Leitor de Documentos) ou **F** (Ação de Arquivo Inteligente) dentro da Camada de Comando. O complemento ignorará instantaneamente a caixa de diálogo de arquivo e começará a processar o arquivo destacado.

### 5.3 Atalhos do Visualizador de Documentos

Quando a janela do Leitor de Documentos estiver aberta, você poderá usar os seguintes atalhos:

- **Ctrl + PageDown:** Move para a próxima página.
- **Ctrl + PageUp:** Move para a página anterior.
- **Alt + A:** Abre uma janela de chat para fazer perguntas sobre o documento.
- **Alt + R:** Força um **Re-escaneamento com IA** usando seu provedor ativo.
- **Alt + G:** Gera e salva um arquivo de áudio de alta qualidade (WAV/MP3). _(Oculto se o provedor não suportar TTS)._
- **Alt + S / Ctrl + S:** Salva o texto extraído como um arquivo TXT ou HTML.

## 6. Rotulagem Semântica por IA e Explorador de IU

Está travado em um aplicativo cheio de "botões sem rótulo" por toda parte? O mecanismo de Rotulagem Semântica por IA resolve isso permanentemente.

### 6.1 Rotulagem Permanente de Objetos (L)

Foques seu leitor de tela em um gráfico ou botão sem rótulo e pressione **L** na Camada de Comando. A IA olhará para o botão visualmente, determinará sua função e aplicará um rótulo permanente.
_Ao contrário das ferramentas de rotulagem mais antigas dos leitores de tela, este complemento usa um sistema híbrido avançado de "Assinatura de Objeto" (AutomationId/ControlID). Seus rótulos personalizados sobreviverão ao redimensionamento de janelas, troca de monitores e atualizações de aplicativos!_

### 6.2 Varredura Completa do Aplicativo (Shift + L)

Pressione **Shift + L** para escanear toda a janela ativa de uma vez. A IA encontrará todos os elementos sem rótulo e os nomeará de forma inteligente de uma só vez. Mais tarde, você poderá gerenciar, renomear ou excluir em lote esses rótulos a partir do Gerenciador de Rótulos integrado.

### 6.3 Explorador de IU (E)

Precisa interagir com um elemento sem navegar até ele manualmente? Pressione **E** para ativar o Explorador de IU. A IA escaneará a tela e gerará uma lista acessível de cada elemento clicável (ignorando ruídos do sistema como barras de tarefas). Escolha um item da lista e o complemento clicará nele instantaneamente para você.

## 7. Assistente de Voz ao Vivo

O Assistente ao Vivo transforma o Vision Assistant Pro em um copiloto interativo em tempo real.
_(Nota: Este recurso é exclusivo para o Google Gemini e provedores Personalizados compatíveis com o Gemini)._

- **Ativação:** Pressione **Control + L** na Camada de Comando para abrir a caixa de diálogo do Assistente ao Vivo.
- **Interação em Tempo Real:** Fale naturalmente pelo seu microfone. A IA ouvirá simultaneamente a sua voz e olhará para a sua tela ativa. Você pode fazer perguntas como "O que estou olhando?" ou "Leia o terceiro parágrafo para mim".
- **Personalização:** Dentro da caixa de diálogo, você pode alterar o Estilo de Voz da IA (por exemplo, Profissional, Amigável, Animado) e ajustar sua "Profundidade de Pensamento" para controlar o quão profundamente ela raciocina antes de responder.

## 8. Comandos Personalizados e Variáveis

Você pode gerenciar seus comandos em **Configurações > Comandos > Gerenciar Comandos...**.

### Variáveis Suportadas

- `[selection]`: Texto atualmente selecionado.
- `[clipboard]`: Conteúdo da área de transferência.
- `[clipboard_image]`: Imagem atualmente na área de transferência.
- `[screen_obj]`: Captura de tela do objeto de navegação.
- `[screen_fg_obj]`: Captura de tela da janela em primeiro plano ativa.
- `[screen_full]`: Captura de tela da tela cheia.
- `[file_ocr]`: Selecionar arquivo de imagem/PDF para extração de texto.
- `[file_read]`: Selecionar documento para leitura (TXT, Código, PDF).
- `[file_audio]`: Selecionar arquivo de áudio para análise (MP3, WAV, OGG).
- `{target_lang}`: Idioma de destino atual.
- `{source_lang}`: Idioma de origem atual.
- `{response_lang}`: Idioma atual da resposta da IA.
- `{swap_target}`: Idioma alternativo para tradução com troca inteligente (smart swap).
- `{swap_instruction}`: Bloco de instrução de tradução com troca inteligente.

## 9. Casos de Uso Reais (Qual recurso devo usar?)

O Vision Assistant Pro está repleto de ferramentas avançadas. Aqui estão alguns cenários comuns para ajudar você a escolher a ferramenta certa:

- **Cenário: Você quer entender o layout completo de uma janela complicada ou de um aplicativo inacessível.**
  _Solução:_ Pressione **O** (Visão de Tela Cheia). A IA analisará a tela inteira e descreverá exatamente onde os elementos, textos e botões estão posicionados.

- **Cenário: Você encontrou uma imagem em uma página da web ou um gráfico sem rótulo em um documento.**
  _Solução:_ Mova o seu objeto de navegação até o gráfico e pressione **V** (Visão de Objeto). A IA descreverá especificamente o que essa imagem contém.

- **Cenário: Você quer assistir a um filme ou clipe de vídeo com audiodescrição.**
  _Solução:_ Pressione **Shift + V** no seu vídeo e escolha **"Gerar Audiodescrição (Arquivo SRT)"**. Quando terminar, clique em **"Gerar Narração Sincronizada (MP3)"** e selecione **"AD Estendida"**. O complemento criará uma faixa de áudio que pausa inteligentemente o diálogo do filme para descrever as cenas visuais.

- **Cenário: Você se deparou com um aplicativo cheio de "botões sem rótulo".**
  _Solução:_ Pressione **L** para rotular permanentemente o botão específico usando IA. Ou pressione **Shift + L** para escanear e rotular a janela inteira de uma só vez. Se você quer apenas clicar em algo rapidamente, pressione **E** (Explorador de IU) para obter uma lista de todos os itens clicáveis.

- **Cenário: Você precisa burlar um CAPTCHA inacessível.**
  _Solução:_ Pressione **C** (Solucionador de CAPTCHA). A IA capturará automaticamente o CAPTCHA, irá resolvê-lo e inserirá a resposta no campo correto.

- **Cenário: Você precisa ler um documento PDF longo de 50 páginas.**
  _Solução:_ Pressione **D** (Leitor de Documentos), defina seu provedor como Google Gemini e insira o intervalo de páginas `1-50`. O complemento extrairá o texto com precisão em segundo plano.

- **Cenário: Você está assistindo a um tutorial de vídeo silencioso ou a uma animação na sua tela.**
  _Solução:_ Pressione **Control + V** para iniciar a gravação da tela. Deixe o tutorial rodar e, em seguida, pressione **Control + V** novamente. A IA explicará exatamente o que foi demonstrado.

***
**Nota:** Uma conexão ativa com a internet é necessária para todos os recursos de IA. Documentos de várias páginas são processados automaticamente.

## 10. Suporte e Comunidade

Fique atualizado com as últimas notícias, recursos e lançamentos:

- **Canal no Telegram:** [t.me/VisionAssistantPro](https://t.me/VisionAssistantPro)
- **Issues no GitHub:** Para relatórios de bugs e solicitações de recursos.

## 11. Apoiadores do Projeto

Um agradecimento sincero aos membros da nossa comunidade que apoiam o desenvolvimento contínuo e a manutenção deste projeto por meio de suas generosas contribuições financeiras:

- **@Alyabani94**
- **Ali Alamri**
- **Ilya**
- **Apoiador Anônimo** (`UQDd...CnMY`)
- **leonardo0216**
- **Sergei Fleytin**
- **Suman Gayen**

_Se você deseja apoiar o projeto financeiramente e ver seu nome aqui, você pode encontrar a opção **Doar** no menu Ferramentas do NVDA (submenu Vision Assistant) ou durante o processo de configuração após a instalação._

## Alterações para 2026.07.15

- **Filtragem Inteligente de Modelos da API**: Reformulação completa do sistema de filtragem de modelos para usar uma abordagem pura de lista de bloqueio (blacklist) em vez de listas de permissão (whitelists). Adicionadas palavras-chave de filtragem mais fortes (`embedding`, `bison`, `gecko`, `audio`, `realtime`, `babbage`, `moderation`, `deep`, `antigravity`, `computer`) para garantir que a lista suspensa do modelo principal de chat permaneça perfeitamente limpa e à prova de futuro, mantendo todos os modelos especializados acessíveis na seção de Roteamento Avançado.
- **Busca no Roteamento Avançado**: Todas as listas suspensas do Roteamento Avançado de Modelos (OCR, STT, TTS, Operador, Vídeo, Ao Vivo) e o seletor de Variantes do eSpeak agora são totalmente pesquisáveis. Você pode digitar rapidamente para filtrar e encontrar o modelo ou variante desejado.
- **Novos Atalhos da Camada de Comando**:
  - **Configurações (`Alt + S`)**: Abre instantaneamente a caixa de diálogo de configurações do Vision Assistant Pro.
  - **Relatório de Chaves com Cota Esgotada (`Alt + Q`)**: Relata o número exato de chaves de API do Gemini que excederam sua cota diária, identificando em qual modelo específico elas estão esgotadas, e anuncia o horário exato de redefinição delas.
  - **Auditoria de Roteamento (`Alt + M`)**: Audita e anuncia sua configuração atual de Roteamento Avançado, lendo quais modelos estão ativamente selecionados para tarefas especializadas (ignorando as configurações padrão).
- **Reformulação Completa do Analisador de Vídeo**: O Analisador de Vídeo foi completamente transformado! Anteriormente, ele fornecia apenas uma descrição básica de vídeos online. Agora, trata-se de um pacote abrangente de processamento de vídeo sob medida para usuários cegos:
  - **Gravação de Tela Local (`Control+V`)**: Agora você pode gravar vídeos silenciosos diretamente da sua tela. A IA analisará o segmento gravado e fornecerá uma descrição altamente detalhada da cena, do layout e das ações.
  - **Geração de Audiodescrição (SRT)**: O complemento agora pode gerar roteiros de Audiodescrição altamente detalhados (no formato padrão SRT) para vídeos, com sincronização inteligente de intervalos para ancorar as descrições de forma inteligente nas pausas naturais da faixa de áudio, além de OCR literal para qualquer texto na tela.
  - **Narração de Áudio Sincronizada (Exportação para MP3)**: Além de legendas baseadas em texto, o complemento pode sintetizar a Audiodescrição em fala, mixá-la automaticamente com a faixa de áudio original do vídeo, aplicar audio ducking (reduzir o volume do fundo durante as descrições) e exportar o resultado final sincronizado como um arquivo MP3!
  - **Ação Inteligente de Arquivo de Vídeo**: Se você focar em um arquivo de vídeo local e pressionar o atalho de vídeo, o complemento o detectará automaticamente e processará o arquivo diretamente.
  - **Rastreamento Avançado de Personagens**: A IA agora realiza uma varredura prévia de extração de personagens. Ela constrói um dicionário global de personagens e rastreia os personagens com precisão, segmento por segmento, sem confundir as identidades.
  - **Configuração do Analisador de Vídeo**: Adicionadas novas configurações para controlar o tamanho dos blocos do SRT, legendagem de personagens e avisos legais.
  - **Roteamento Estendido de Modelos**: Agora você pode selecionar explicitamente modelos de vídeo especializados (`gemini_video_model`, `custom_video_model`) nas configurações de Roteamento Avançado de Modelos.
- **Gerenciamento Inteligente de Cota da API**: Tratamento aprimorado de erros 429 (Limite Diário) rastreando as cotas por modelo. Se uma chave atingir seu limite diário em um modelo, ela será inteligentemente colocada em quarentena apenas para aquele modelo específico, deixando a chave disponível para uso com outros modelos.

## Alterações para 7.0.0

- **Retomada de Varreduras Inacabadas**: Adicionado um recurso de retomada tanto para o Leitor de Documentos quanto para as Ações Inteligentes de Arquivos. Se uma varredura for interrompida, agora você pode continuar de onde ela parou, em vez de começar do zero.
- **Nova Variável `[screen_fg_obj]`**: Adicionada uma variável de comando personalizado para capturar uma foto apenas da janela ativa em primeiro plano, em vez da tela inteira.
- **Tentativas Inteligentes e Rotação de Chaves**: O complemento agora tenta novamente em silêncio até 5 vezes com a mesma chave ao encontrar sobrecargas temporárias no servidor (como "alta demanda" ou respostas malformadas). Se as tentativas falharem, ele muda automaticamente para a próxima chave de API da sua lista.
- **Detecção de Cortina de Tela**: Adicionada uma verificação para evitar a captura de telas quando a Cortina de Tela estiver ativa (seja ativada permanentemente ou alternada temporariamente pelo atalho). O complemento emitirá um aviso e interromperá a ação, evitando que você envie imagens pretas e desperdice tokens de API.
- **Ajustes no Leitor de Documentos**: A caixa de diálogo de intervalo do PDF agora pré-seleciona automaticamente o idioma de destino padrão das configurações do seu complemento. Também foi aprimorado o gerenciamento de threads para garantir que as tarefas em segundo plano parem de forma limpa quando o leitor for fechado.
- **Integração Nativa de OCR do Mistral**: Integrada a API nativa de OCR de Documentos do Mistral. Documentos de várias páginas são mesclados, enviados e processados automaticamente em lotes usando o endpoint especializado `/v1/ocr` do Mistral, enquanto imagens de página única são processadas diretamente sem conversões desnecessárias para PDF.
- **Manipuladores Dinâmicos de URL Personalizada**: Modificar a URL da API Personalizada agora limpa instantaneamente a lista de modelos em cache e restaura a caixa de texto de inserção manual de modelos. Isso garante total compatibilidade com endpoints personalizados (como o Cloudflare AI Gateway) que não suportam o endpoint padrão de listagem `/v1/models`.
- **Mecanismo de Entrada Reformulado do Operador de IA**: O sistema subjacente de simulação de mouse e teclado para o Operador de IA foi completamente reconstituído. A API herdada `mouse_event` foi substituída pela moderna API `SendInput` do Windows, trazendo uma compatibilidade significativamente maior com aplicativos modernos, janelas protegidas por UAC e telas de alta densidade de pixels (High-DPI).
- **Operações de Arrastar e Soltar Corrigidas**: As ações de arrastar e soltar no Operador de IA agora são totalmente estáveis e confiáveis. O novo mecanismo utiliza curvas naturais de suavização ("easing"), posicionamento preciso do cursor, temporização otimizada e uma técnica inteligente de "toque leve" para garantir que o Windows e os aplicativos reconheçam e executem corretamente os gestos de arrastar e soltar sem falhar no meio do caminho.
- **Suporte a Múltiplos Monitores**: O Operador de IA agora suporta totalmente configurações de múltiplos monitores. Os movimentos e cliques do mouse funcionam corretamente em todos os monitores usando a flag `MOUSEEVENTF_VIRTUALDESK`, garantindo o posicionamento preciso independentemente de em qual monitor o aplicativo alvo esteja.
- **Simulação de Teclado Aprimorada**: Injeção de teclas aprimorada para suportar totalmente as "Teclas Estendidas" (como as setas direcionais, Home, End, Page Up/Down, Insert, Delete e F1-F12). Isso garante que os comandos de navegação e atalhos enviados pelo Operador de IA funcionem perfeitamente em todos os aplicativos.
- **Suporte a Imagens HEIC/HEIF**: Adicionado suporte nativo para formatos de fotos do iPhone. Agora você pode selecionar diretamente arquivos `.heic` e `.heif` para descrição por IA, OCR ou Leitura de Documentos sem necessidade de conversão prévia.

## Alterações para 6.5.0

- **Assistente ao Vivo**: Adicionado um recurso de assistente de voz e tela em tempo real, disponível exclusivamente para o provedor Google Gemini (ou provedores personalizados compatíveis com o Gemini). Inclui personalização interativa de voz e de profundidade de pensamento diretamente na caixa de diálogo, com reconexão automática ao alterar as configurações.
- **Provedor MiniMax AI**: Integrado o MiniMax como um provedor de mesmo nível com suporte multimodal completo (chat, visão, OCR), TTS personalizado usando mais de 300+ vozes dinâmicas e remoção automática de blocos de raciocínio (ex: `<think>...</think>`) das respostas.
- **Tradução do Visualizador de Documentos**: Corrigida uma falha silenciosa de tradução para usuários do NVDA que não utilizam o idioma inglês, garantindo que o código padrão de 2 letras do idioma seja enviado ao Google Tradutor em vez do nome localizado do idioma.
- **Nova Tentativa de Varredura em Lote de PDF**: Implementada uma lógica de nova tentativa separada, altamente otimizada e silenciosa para a varredura em lote de documentos PDF, evitando uploads redundantes e pop-ups de erro disruptivos durante as tentativas.
- **Status do Visualizador de Documentos**: Corrigido um bug onde o status geral do plugin (verificado através da tecla `I`) permanecia travado em "Processamento em Lote Iniciado" durante varreduras de documentos longos.
- **Falha de Threading Resolvida**: Corrigida uma falha grave de asserção de thread `IsMain() failed in wxTimerImpl` ao abrir documentos a partir de uma thread em segundo plano, transitando a fila de retorno da GUI para `wx.CallAfter`.

## Alterações para 6.1.2

- **Pré-Verificação de Rótulos Duplicados**: Corrigido um problema na rotulagem individual onde a verificação de duplicados usava chaves de coordenadas antigas, fazendo com que o NVDA fizesse requisições de IA duplicadas para objetos já rotulados em vez de anunciar o rótulo existente.
- **Chat de Documentos para Provedores não-Gemini**: Corrigida uma verificação estrita de chave de API no Chat de Documentos (`on_ask`) para garantir que os usuários dos provedores OpenAI, Groq ou Personalizados locais (como o Ollama) possam conversar com documentos com sucesso sem serem bloqueados.
- **Tradução Rápida do OCR do Chrome**: Restaurada a API de tradução gratuita e sem necessidade de chave para o OCR do Chrome. A tradução do texto extraído agora ignora a IA do Gemini, economizando cotas de API e acelerando o processo de tradução.
- **Filtro Alfanumérico de CAPTCHA**: Corrigida a lógica de filtragem no solucionador de CAPTCHA para garantir que os caracteres não alfanuméricos sejam devidamente limpos em todas as situações.
- **Atualização da Ajuda da Camada de Comando**: Corrigido o atalho do anúncio de status no menu de ajuda de `L` para `I`, e adicionados ambos os comandos de rotulagem (`L` e `Shift+L`) à lista.

## Alterações para 6.1.1

- **Correção do Output de Pensamento do Gemma 4**: Corrigido um problema com os modelos Gemma 4 onde todo o processo interno de pensamento era exibido como a resposta final, ou onde desativar o pensamento resultava em respostas vazias. O complemento agora isola e extrai corretamente apenas a resposta de texto limpa final.
- **OCR em Lote a partir do Explorador de Arquivos**: Agora você pode selecionar várias fotos ou PDFs diretamente no Explorador de Arquivos do Windows e extrair o texto ou analisá-los em lote. O complemento filtrará e processará automaticamente apenas os formatos de arquivo suportados.

## Alterações para 6.1.0

- **Integração Universal de IA Local (Configurar IA Local)**: Adicionado um novo botão **"Configurar IA Local"** nas Configurações do Provedor Personalizado. Os usuários agora podem configurar automaticamente mecanismos de IA locais, incluindo **Ollama**, **LM Studio**, **Jan.ai** e **KoboldCPP** instantaneamente.
- **Desvio Inteligente de Proxy Local**: Reconstruída a lógica de conexão com um mecanismo avançado de desvio de proxy. O complemento agora é inteligente o suficiente para ignorar completamente os proxies do sistema Windows para conexões de loopback locais, garantindo conexões estáveis com a IA local mesmo quando a sua VPN ou modo TUN estiver ativo.
- **Rotulagem por IA Ultra-Estável (v2)**: Substituídas as chaves de coordenadas absolutas da tela por um sistema híbrido avançado de **Assinatura de Objeto**. Os rótulos agora dependem de identificadores programáticos (UIA **AutomationId** ou Win32 **ControlID**) e coordenadas relativas à janela, tornando seus rótulos personalizados completamente resistentes ao redimensionamento, movimentação, troca de monitores ou redimensionamento de janelas.
- **Migração Automática de Rótulos Perfeita**: A atualização é completamente transparente. O complemento migrará automaticamente seus rótulos antigos baseados em coordenadas herdadas para o novo formato estável de impressão digital em segundo plano logo no primeiro foco, com zero perda de dados.

## Alterações para 6.0

- **Apresentando a Rotulagem Semântica por IA**: Os usuários agora podem rotular permanentemente botões e ícones sem nome usando IA. Pressione **L** para rotular o objeto de navegação atual (suportando tanto o foco por Tab quanto a navegação de objetos) ou **Shift+L** para escanear e rotular o aplicativo inteiro de uma vez.
- **Gerenciamento Inteligente de Rótulos**: Adicionada uma nova caixa de diálogo do Gerenciador de Rótulos totalmente acessível (via **Shift+L** se os rótulos existirem) para visualizar, renomear ou excluir em lote os rótulos personalizados.
- **Análise Direta de Arquivos (Ignorar Caixa de Diálogo de Arquivo)**: O complemento agora é inteligente o suficiente para detectar se você está focado atualmente em um arquivo PDF ou de imagem no Explorador de Arquivos do Windows. Pressionar **F (Ação de Arquivo Inteligente)** ou **D (Leitor de Documentos)** em um arquivo destacado irá processá-lo imediatamente, ignorando completamente a caixa de diálogo padrão de "Abrir".

## Alterações para 5.6

- **Adicionado o Mecanismo de OCR "Nenhum (Extrair Camada de Texto)"**: Os usuários agora podem extrair texto diretamente de PDFs pesquisáveis sem gastar créditos de IA, melhorando significativamente a velocidade e a privacidade para documentos baseados em texto.
- **Precisão Refinada do Explorador de IU**: Melhorado o comando do Explorador de IU para identificar melhor os tipos de elementos (como Itens de Lista) e relatar estados com precisão como "(Marcado)", "(Selecionado)" ou "(Expandido)", enquanto ignora componentes do sistema Windows como a Barra de Tarefas e o Relógio.
- **Lembrete de Configuração de Instalação**: Adicionada uma notificação após a instalação para guiar os usuários ao menu de configurações para configurar suas chaves de API e preferências.

## Alterações para 5.5.2

- **Correção do Problema de Digitação no Operador de IA:** Resolvido um bug onde a letra 'v' era digitada em vez de colar o texto em determinados sistemas. Esta correção aborda conflitos de temporização que ocorriam durante alta carga do sistema.
- **Estabilidade Aprimorada:** Adicionado um tratamento robusto de erros para operações de área de transferência para evitar travamentos do complemento quando a área de transferência do sistema estiver temporariamente bloqueada por outros aplicativos.
- **Otimização de Tempo:** Ajustados os atrasos internos para eventos de teclado para garantir maior confiabilidade em diferentes velocidades de sistema e melhor compatibilidade com Gerenciadores de Área de Transferência de terceiros.

## Alterações para 5.5 (A Atualização de Automação)

- **Operador de IA (Controle Autônomo - Shift+A):** Esta é a joia da coroa da v5.5. O Vision Assistant Pro deixou de ser um assistente passivo para se tornar o seu **Operador de IA** pessoal. Ele não apenas descreve a tela — ele assume o comando.
  - _Como funciona:_ Agora você pode dar instruções verbais para operar o seu PC. Por exemplo, em um aplicativo completamente inacessível onde o seu leitor de tela permanece silencioso, você pode pressionar **Shift+A** e digitar: _"Clique no botão Configurações"_ ou _"Encontre o campo de pesquisa, digite 'Últimas Notícias' e pressione enter."_ A IA identifica visualmente os elementos, move o mouse e executa a tarefa para você.
  - _Nota de Desempenho:_ Este recurso é otimizado para o **Gemini 3.0 Flash (Preview)**, entregando respostas incrivelmente rápidas e inteligentes que podem lidar até mesmo com os layouts de interface mais complexos.
  - **⚠️ Aviso de Uso da API:** Como o Operador de IA precisa "ver" exatamente o que está acontecendo para ser preciso, ele envia uma captura de tela de alta resolução a cada etapa. Por favor, note que o uso frequente consumirá sua cota de API muito mais rápido do que as tarefas padrão baseadas em texto.
- **Explorador de IU Visual (E):** Cansado de navegar por "botões sem rótulo"? Pressione **E** para ativar o Explorador de IU. A IA escaneará a janela inteira e gerará uma lista de cada elemento clicável que ela vê — incluindo ícones, gráficos e menus. Basta escolher um item da lista e o Operador de IA clicará nele para você. É como ter uma "camada acessível" por cima de qualquer aplicativo.
- **Ação de Arquivo Inteligente Sensível ao Contexto (F):** A tecla "F" foi completamente reformulada. Ela não assume mais que você deseja apenas OCR. Quando você seleciona uma única imagem, ela agora pergunta inteligentemente sobre a sua intenção: você pode escolher uma **Descrição Visual Detalhada** para entender a cena ou uma **Extração de Texto Estruturada (OCR)** para leitura. O menu se adapta dinamicamente com base no tipo de arquivo e no seu mecanismo de IA ativo.
- **Otimização do Núcleo:** Realizamos uma limpeza profunda na lógica interna do complemento, removendo funções herdadas não utilizadas e códigos redundantes. Isso resulta em uma experiência mais leve, rápida e confiável para todos os usuários.

## Alterações para 5.0

- **Arquitetura Multi-Provedor**: Adicionado suporte completo para **OpenAI**, **Groq** e **Mistral** junto ao Google Gemini. Os usuários agora podem escolher o backend de IA de sua preferência.
- **Roteamento Avançado de Modelos**: Usuários de provedores nativos (Gemini, OpenAI, etc.) agora podem selecionar modelos específicos de uma lista suspensa para diferentes tarefas (OCR, STT, TTS).
- **Configuração Avançada de Endpoint**: Usuários de provedores personalizados podem inserir manualmente URLs e nomes de modelos específicos para um controle granular sobre servidores locais ou de terceiros.
- **Visibilidade Inteligente de Recursos**: O menu de configurações e a IU do Leitor de Documentos agora ocultam automaticamente recursos não suportados (como TTS) com base no provedor selecionado.
- **Busca Dinâmica de Modelos**: O complemento agora busca a lista de modelos disponíveis diretamente da API do provedor, garantindo compatibilidade com novos modelos assim que forem lançados.
- **OCR e Tradução Híbridos**: Otimizada a lógica para usar o Google Tradutor por velocidade ao usar o OCR do Chrome, e tradução alimentada por IA ao usar os mecanismos Gemini/Groq/OpenAI.
- **"Re-escanear com IA" Universal**: O recurso de re-escanear do Leitor de Documentos não está mais limitado ao Gemini. Ele agora utiliza o provedor de IA que estiver ativo no momento para reprocessar as páginas.

## Alterações para 4.6

- **Chamar Resultado Interativo:** Adicionada a tecla **Espaço** à camada de comando, permitindo que os usuários reabram instantaneamente a última resposta da IA em uma janela de chat para perguntas de acompanhamento, mesmo quando o modo "Saída Direta" estiver ativo.
- **Hub da Comunidade no Telegram:** Adicionado um link para o "Canal Oficial do Telegram" no menu Ferramentas do NVDA, fornecendo uma maneira rápida de se manter atualizado com as últimas notícias, recursos e lançamentos.
- **Estabilidade de Resposta Aprimorada:** Otimizada a lógica central dos recursos de Tradução, OCR e Visão para garantir um desempenho mais confiável e uma experiência mais suave ao usar a saída direta de fala.
- **Orientação de Interface Aprimorada:** Atualizadas as descrições de configurações e a documentação para explicar melhor o novo sistema de chamada de resultados e como ele funciona junto com as configurações de saída direta.

## Alterações para 4.5

- **Gerenciador de Comandos Avançado:** Introduzida uma caixa de diálogo de gerenciamento dedicada nas configurações para customizar os comandos padrão do sistema e gerenciar comandos definidos pelo usuário, com suporte completo para adicionar, editar, reordenar e visualizar.
- **Suporte Abrangente a Proxy:** Resolvidos problemas de conectividade de rede garantindo que as configurações de proxy configuradas pelo usuário sejam estritamente aplicadas a todas as requisições de API, incluindo tradução, OCR e geração de fala.
- **Migração Automática de Dados:** Integrado um sistema de migração inteligente para atualizar automaticamente as configurações de comandos herdadas para um formato JSON v2 robusto na primeira execução, sem perda de dados.
- **Compatibilidade Atualizada (2025.1):** Definida a versão mínima exigida do NVDA para 2025.1 devido a dependências de bibliotecas em recursos avançados, como o Leitor de Documentos, para garantir um desempenho estável.
- **Interface de Configurações Otimizada:** Simplificada a interface de configurações ao reorganizar o gerenciamento de comandos em uma caixa de diálogo separada, proporcionando uma experiência de usuário mais limpa e acessível.
- **Guia de Variáveis de Comando:** Adicionado um guia integrado nas caixas de diálogo de comandos para ajudar os usuários a identificar e usar facilmente variáveis dinâmicas como [selection], [clipboard] e [screen_obj].

## Alterações para 4.0.3

- **Resiliência de Rede Aprimorada:** Adicionado um mecanismo de nova tentativa automática para lidar melhor com conexões de internet instáveis e erros temporários do servidor, garantindo respostas de IA mais confiáveis.
- **Janela de Tradução Visual:** Introduzida uma janela dedicada para resultados de tradução. Os usuários agora podem navegar facilmente e ler traduções longas linha por linha, de forma semelhante aos resultados de OCR.
- **Visualização Formatada Agregada:** O recurso "Visualizar Formatado" no Leitor de Documentos agora exibe todas as páginas processadas em uma única janela organizada, com cabeçalhos de página claros.
- **Fluxo de Trabalho de OCR Otimizado:** Ignora automaticamente a seleção do intervalo de páginas para documentos de página única, tornando o processo de reconhecimento mais rápido e fluido.
- **Estabilidade de API Aprimorada:** Mudança para um método de autenticação baseado em cabeçalho mais robusto, resolvendo potenciais erros de "Todas as chaves de API falharam" causados por conflitos de rotação de chaves.
- **Correções de Bugs:** Resolvidos vários travamentos potenciais, incluindo um problema durante o encerramento do complemento e um erro de foco na caixa de diálogo de chat.

## Alterações para 4.0.1

- **Leitor de Documentos Avançado:** Um novo e poderoso visualizador de PDFs e imagens com seleção de intervalo de páginas, processamento em segundo plano e navegação fluida com `Ctrl+PageUp/Down`.
- **Novo Submenu de Ferramentas:** Adicionado um submenu dedicado "Vision Assistant" sob o menu Ferramentas do NVDA para um acesso mais rápido aos recursos principais, configurações e documentação.
- **Customização Flexível:** Agora você pode escolher o seu mecanismo de OCR e voz de TTS preferidos diretamente do painel de configurações.
- **Suporte a Múltiplas Chaves de API:** Adicionado suporte para múltiplas chaves de API do Gemini. Você pode inserir uma chave por linha ou separá-las com vírgulas nas configurações.
- **Mecanismo de OCR Alternativo:** Introduzido um novo mecanismo de OCR para garantir um reconhecimento de texto confiável mesmo ao atingir os limites de cota da API do Gemini.
- **Rotação Inteligente de Chaves de API:** Alterna automaticamente e lembra a chave de API em funcionamento mais rápida para ignorar os limites de cota.
- **Documento para MP3/WAV:** Capacidade integrada de gerar e salvar arquivos de áudio de alta qualidade nos formatos MP3 (128kbps) e WAV diretamente dentro do leitor.
- **Suporte a Stories do Instagram:** Adicionada a capacidade de descrever e analisar Stories do Instagram usando suas URLs.
- **Suporte ao TikTok:** Introduzido suporte para vídeos do TikTok, permitindo a descrição visual completa e transcrição de áudio dos clipes.
- **Caixa de Diálogo de Atualização Redesenhada:** Apresenta uma nova interface acessível com uma caixa de texto rolável para ler claramente as alterações da versão antes de instalar.
- **Status Unificado e UX:** Padronizadas as caixas de diálogo de arquivos em todo o complemento e aprimorado o comando 'L' para relatar o progresso em tempo real.

## Alterações para 3.6.0

- **Sistema de Ajuda:** Adicionado um comando de ajuda (`H`) dentro da Camada de Comando para fornecer uma lista de fácil acesso com todos os atalhos e suas funções.
- **Análise de Vídeo Online:** Suporte expandido para incluir vídeos do **Twitter (X)**. Também foi aprimorada a detecção de URL e a estabilidade para uma experiência mais confiável.
- **Contribuição com o Projeto:** Adicionada uma caixa de diálogo opcional de doação para usuários que desejam apoiar as futuras atualizações e o crescimento contínuo do projeto.

## Alterações para 3.5.0

- **Camada de Comando:** Introduzido um sistema de Camada de Comando (padrão: `NVDA+Shift+V`) para agrupar atalhos sob uma única tecla mestra. Por exemplo, em vez de pressionar `NVDA+Control+Shift+T` para tradução, agora você pressiona `NVDA+Shift+V` seguido por `T`.
- **Análise de Vídeo Online:** Adicionado um novo recurso para analisar vídeos do YouTube e Instagram diretamente fornecendo uma URL.

## Alterações para 3.1.0

- **Modo de Saída Direta:** Adicionada uma opção para ignorar a caixa de diálogo de chat e ouvir as respostas da IA diretamente via fala para uma experiência mais rápida e fluida.
- **Integração com a Área de Transferência:** Adicionada uma nova configuração para copiar automaticamente as respostas da IA para a área de transferência.

## Alterações para 3.0

- **Novos Idiomas:** Adicionadas traduções para **Persa** e **Vietnamita**.
- **Modelos de IA Expandidos:** Reorganizada a lista de seleção de modelos com prefixos claros (`[Free]`, `[Pro]`, `[Auto]`) para ajudar os usuários a distinguir entre modelos gratuitos e com limite de taxa (pagos). Adicionado suporte para o **Gemini 3.0 Pro** e **Gemini 2.0 Flash Lite**.
- **Estabilidade de Ditado:** Melhorada significativamente a estabilidade do Ditado Inteligente. Adicionada uma verificação de segurança para ignorar clipes de áudio com menos de 1 segundo, evitando alucinações da IA e erros vazios.
- **Manipulação de Arquivos:** Corrigido um problema onde o envio de arquivos com nomes que não estivessem em inglês falhava.
- **Otimização de Comandos:** Lógica de tradução aprimorada e resultados de Visão estruturados.

## Alterações para 2.9

- **Adicionadas traduções para Francês e Turco.**
- **Visualização Formatada:** Adicionado um botão "Visualizar Formatado" nas caixas de diálogo de chat para visualizar a conversa com a estilização adequada (Cabeçalhos, Negrito, Código) em uma janela de navegação padrão.
- **Configuração de Markdown:** Adicionada uma nova opção "Limpar Markdown no Chat" nas Configurações. Desmarcar isso permite que os usuários vejam a sintaxe bruta do Markdown (ex: `**`, `#`) na janela de chat.
- **Gerenciamento de Caixas de Diálogo:** Corrigido um problema onde as janelas de "Refinar Texto" ou de chat abriam várias vezes ou falhavam em focar corretamente.
- **Melhorias de UX:** Padronizados os títulos das caixas de diálogo de arquivos para "Abrir" e removidos anúncios de fala redundantes (ex: "Abrindo menu...") para uma experiência mais suave.

## Alterações para 2.8

- Adicionada tradução para o Italiano.
- **Relatório de Status:** Adicionado um novo comando (NVDA+Control+Shift+I) para anunciar o status atual do complemento (ex: "Enviando...", "Analisando...").
- **Exportação em HTML:** O botão "Salvar Conteúdo" nas caixas de diálogo de resultados agora salva a saída como um arquivo HTML formatado, preservando estilos como cabeçalhos e texto em negrito.
- **IU de Configurações:** Layout do painel de Configurações aprimorado com agrupamento acessível.
- **Novos Modelos:** Adicionado suporte para o gemini-flash-latest e gemini-flash-lite-latest.
- **Idiomas:** Adicionado o Nepalês aos idiomas suportados.
- **Lógica do Menu Refinar:** Corrigido um bug crítico onde os comandos "Refinar Texto" falhavam se o idioma da interface do NVDA não fosse o inglês.
- **Ditado:** Detecção de silêncio aprimorada para evitar saídas de texto incorretas quando nenhuma fala é inserida.
- **Configurações de Atualização:** A opção "Verificar atualizações ao iniciar" agora vem desativada por padrão para cumprir com as políticas da Add-on Store.
- Limpeza de código.

## Alterações para 2.7

- Migrada a estrutura do projeto para o Modelo de Complemento oficial da NV Access para melhor conformidade com os padrões.
- Implementada uma lógica de nova tentativa automática para erros HTTP 429 (Limite de Taxa) para garantir a confiabilidade durante períodos de alto tráfego.
- Otimizados os comandos de tradução para maior precisão e melhor manuseio da lógica de "Troca Inteligente" (Smart Swap).
- Atualizada a tradução para o Russo.

## Alterações para 2.6

- Adicionado suporte de tradução para o Russo (Agradecimentos ao nvda-ru).
- Atualizadas as mensagens de erro para fornecer um feedback mais descritivo em relação à conectividade.
- Alterado o idioma de destino padrão para o Inglês.

## Alterações para 2.5

- Adicionado o Comando de OCR de Arquivo Nativo (NVDA+Control+Shift+F).
- Adicionado o botão "Salvar Chat" às caixas de diálogo de resultados.
- Implementado suporte completo a localização (i18n).
- Migrado o feedback de áudio para o módulo de tons nativos do NVDA.
- Mudança para a API de Arquivos do Gemini para uma melhor manipulação de PDFs e arquivos de áudio.
- Corrigido um travamento ao traduzir textos que continham chaves.

## Alterações para 2.1.1

- Corrigido um problema onde a variável `[file_ocr]` não funcionava corretamente dentro dos Comandos Personalizados.

## Alterações para 2.1

- Padronizados todos os atalhos para usar NVDA+Control+Shift para eliminar conflitos com o layout de Laptop do NVDA e teclas de atalho do sistema.

## Alterações para 2.0

- Implementado sistema integrado de Atualização Automática.
- Adicionado o Cache de Tradução Inteligente para recuperação instantânea de textos traduzidos anteriormente.
- Adicionada a Memória de Conversa para refinar contextualmente os resultados nas caixas de diálogo de chat.
- Adicionado Comando Dedicado de Tradução da Área de Transferência (NVDA+Control+Shift+Y).
- Otimizados os comandos de IA para impor estritamente a saída no idioma de destino.
- Corrigido um travamento causado por caracteres especiais no texto de entrada.

## Alterações para 1.5

- Adicionado suporte para mais de 20 novos idiomas.
- Implementada a Caixa de Diálogo Interativa de Refinamento para perguntas de acompanhamento.
- Adicionado o recurso de Ditado Inteligente Nativo.
- Adicionada a categoria "Vision Assistant" à caixa de diálogo de Gestos de Entrada do NVDA.
- Corrigidos travamentos por COMError em aplicativos específicos como Firefox e Word.
- Adicionado mecanismo de nova tentativa automática para erros do servidor.

## Alterações para 1.0

- Lançamento inicial.
