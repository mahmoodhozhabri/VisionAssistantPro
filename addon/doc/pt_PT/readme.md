# Documentação do Vision Assistant Pro

O **Vision Assistant Pro** é um assistente de IA multimodal avançado para o NVDA. Aproveita motores de IA de classe mundial para fornecer leitura de ecrã inteligente, tradução, ditação por voz e análise de documentos.

_Este extra foi lançado para a comunidade em homenagem ao Dia Internacional das Pessoas com Deficiência._

## 1. Configuração

Aceda a **Menu do NVDA > Preferências > Definições > Vision Assistant Pro**.

### 1.1 Definições de Conexão

- **Fornecedor:** Selecione o seu serviço de IA preferido. Os fornecedores suportados incluem o **Google Gemini**, **OpenAI**, **Mistral**, **Groq**, **MiniMax** e **Personalizado** (servidores compatíveis com OpenAI como Ollama, LM Studio, Jan.ai ou KoboldCPP).
- **Nota Importante:** Recomendamos vivamente a utilização do **Google Gemini** para obter o melhor desempenho e precisão (especialmente para análise de imagens/ficheiros).
- **Chave de API:** Obrigatória. Pode introduzir múltiplas chaves (separadas por vírgulas ou quebras de linha) para rotação automática.
- **Procurar Modelos:** Após introduzir a sua chave de API, prima este botão para transferir a lista mais recente de modelos disponíveis do fornecedor.
- **Modelo de IA:** Selecione o modelo principal utilizado para chat geral e análise.

### 1.2 Encaminhamento Avançado de Modelos

*Disponível para todos os fornecedores, incluindo Gemini, OpenAI, Groq, Mistral e Personalizado._

> **⚠️ Aviso:** Estas definições destinam-se **apenas a utilizadores avançados**. Se não tiver a certeza do que um modelo específico faz, por favor, deixe esta opção **desmarcada**. A seleção de um modelo incompatível para uma tarefa (por exemplo, um modelo de apenas texto para Visão) causará erros e fará com que o extra deixe de funcionar.

Marque **"Encaminhamento Avançado de Modelos (Específico por tarefa)"** para desbloquear um controlo detalhado. Isto permite-lhe selecionar modelos específicos da lista pendente para diferentes tarefas:

- **Modelo de OCR / Visão:** Escolha um modelo especializado para analisar imagens.
- **Conversão de Voz em Texto (STT):** Escolha um modelo específico para ditação.
- **Conversão de Texto em Voz (TTS):** Escolha um modelo para gerar áudio.
- **Modelo do Operador de IA:** Selecione un modelo específico para tarefas de operação autónoma do computador.
- **Modelo de Vídeo:** Selecione um modelo específico para análise de vídeo e geração de audiodescrição.
_Nota: Funcionalidades não suportadas (por exemplo, TTS para o Groq) serão ocultadas automaticamente._

### 1.3 Configuração Avançada de Endpoint (Fornecedor Personalizado)

*Disponível apenas quando "Personalizado" está selecionado._

> **⚠️ Aviso:** Esta secção permite a configuração manual da API e foi concebida para **utilizadores experientes** que executam servidores locais ou proxies. URLs ou nomes de modelos incorretos irão quebrar a conectividade. Se não souber exatamente o que são estes endpoints, mantenha esta opção **desmarcada**.

Marque **"Configuração Avançada de Endpoint"** para introduzir manualmente os detalhes do servidor. Ao contrário dos fornecedores nativos, aqui deve **escrever** os URLs e nomes de modelos específicos:

- **URL da Lista de Modelos:** O endpoint para procurar os modelos disponíveis.
- **URL do Endpoint de OCR/STT/TTS:** URLs completos para serviços específicos (por exemplo, `http://localhost:11434/v1/audio/speech`).
- **Modelos Personalizados:** Escreva manualmente o nome do modelo (por exemplo, `llama3:8b`) para cada tarefa.

### 1.3.1 Configurar IA Local (Configuração Numa Única Ação)

Para tornar a integração de IA local e completamente offline extremamente simples, está disponível um botão dedicado **"Configurar IA Local"** dentro das Definições do Fornecedor Personalizado.

Se estiver a executar um servidor de modelos de IA local no seu computador:

1. Selecione **Personalizado** como o seu Fornecedor.
2. Prima o botão **Configurar IA Local**.
3. Escolha o seu motor de IA local a partir do diálogo acessível:
   - **Ollama** (predefinido para `http://127.0.0.1:11434`)
   - **LM Studio** (predefinido para `http://127.0.0.1:1234`)
   - **Jan.ai** (predefinido para `http://127.0.0.1:1337`)
   - **KoboldCPP** (predefinido para `http://127.0.0.1:5001`)
4. O extra configurará instantaneamente o URL local correto, o tipo de API e procurará automaticamente os seus modelos offline ativos para preencher a caixa de seleção do **Modelo de IA**.

_Nota sobre Rede e Proxies:_ Este motor de conexão local possui um mecanismo avançado de desvio de proxy. Mesmo que tenha uma VPN de sistema ativa ou um proxy em modo TUN, os seus pedidos de IA local irão ignorá-lo completamente, garantindo ligações offline estáveis sem erros 502 Bad Gateway.

### 1.4 Preferências Gerais

- **Motor de OCR:** Escolha entre **Chrome (Rápido)** para resultados céleres ou **AI (Avançado)** para uma preservação superior do esquema visual.
- **Voz do TTS:** Selecione o seu estilo de voz preferido. Esta lista é atualizada dinamicamente com base no seu fornecedor ativo.
- **Criatividade (Temperatura):** Controla a aleatoriedade da IA. Valores mais baixos são melhores para traduções/OCR precisos.
- **URL do Proxy:** Configure esta opção se os serviços de IA estiverem restritos na sua região (suporta proxies locais como `127.0.0.1` ou URLs de ponte).
- **Saída Direta (Sem Janela de Chat):** Marque esta opção se pretender que a IA apenas leia o resultado em voz alta, sem abrir uma janela de chat interativa.
- **Copiar respostas da IA para a área de transferência:** Copia automaticamente todas as respostas da IA para a área de transferência do seu sistema para facilitar a colagem.
- **Limpar Markdown no Chat:** Desmarque esta opção se preferir ver os símbolos de formatação originais em vez de uma visualização de texto limpa e formatada.

## 2. Camada de Comando e Atalhos

Para evitar conflitos de teclado, este extra utiliza uma **Camada de Comando**.

1. Prima **NVDA + Shift + V** (Tecla Mestre) para ativar a camada (ouvirá um sinal sonoro).
2. Solte as teclas e, em seguida, prima uma das seguintes teclas individuais:

| Tecla           | Função                                 | Descrição                                                                                                                            |
| --------------- | -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| **Shift + A**   | **Operador de IA**                     | **Operação Autónoma:** Diga à IA para realizar uma tarefa no seu ecrã. Premir novamente aborta instantaneamente as operações ativas. |
| **E**           | **Explorador de IU**                   | **Clique Interativo:** Identifica e clica em elementos da interface do utilizador em qualquer aplicação.                             |
| **T**           | Tradutor Inteligente                   | Traduz o texto sob o cursor do navegador ou a seleção.                                                                               |
| **Shift + T**   | Tradutor da Área de Transferência      | Traduz o conteúdo que se encontra atualmente na área de transferência.                                                               |
| **R**           | Refinador de Texto                     | Resume, corrige a gramática, explica ou executa **Prompts Personalizados**.                                                          |
| **V**           | Visão de Objetos                       | Descreve o objeto atual do navegador.                                                                                                |
| **O**           | Visão de Ecrã Inteiro                  | Analisa todo o esquema visual e conteúdo do ecrã.                                                                                    |
| **Shift + V**   | Análise de Vídeo                       | Analisa ficheiros de vídeo locais ou vídeos online do **YouTube**, **Instagram**, **TikTok** ou **Twitter (X)**.                     |
| **Control + V** | Gravação de Vídeo Local                | Grava um vídeo silencioso do seu ecrã e analisa as ações e o esquema visual.                                                         |
| **D**           | Leitor de Documentos                   | Leitor avançado para PDF e imagens com seleção de intervalo de páginas.                                                              |
| **F**           | **Ação Inteligente de Ficheiros**      | Reconhecimento contextual de ficheiros de imagem, PDF ou TIFF selecionados.                                                          |
| **A**           | Transcrição de Áudio                   | Transcreve ficheiros MP3, WAV ou OGG para texto.                                                                                     |
| **C**           | Resolução de CAPTCHAs                  | Captura e resolve CAPTCHAs (Suporta portais governamentais).                                                                         |
| **S**           | Ditação Inteligente                    | Converte voz em texto. Prima para iniciar a gravação, novamente para parar/escrever.                                                 |
| **Control+L**   | **Assistente em Direto**               | **Copiloto em Tempo Real (apenas Gemini):** Inicia ou termina uma conversa em direto por voz e ecrã com o assistente de IA.          |
| **I**           | Relatório de Estado                    | Anuncia o progresso atual (por exemplo, "A analisar...", "Inativo").                                                                 |
| **L**           | **Etiquetar Objeto**                   | **Etiquetagem Semântica por IA:** Etiqueta permanentemente o elemento/ícone atualmente focado.                                       |
| **Shift + L**   | **Gerir/Procurar Etiquetas**           | Abre o Gestor de Etiquetas (se existirem etiquetas) ou examina a aplicação à procura de elementos sem nome.                          |
| **U**           | Verificar Atualizações                 | Verifica manualmente o GitHub para obter a versão mais recente do extra.                                                             |
| **Espaço**      | Relembrar Último Resultado             | Mostra a última resposta da IA num diálogo de chat para revisão ou acompanhamento.                                                   |
| **H**           | Ajuda de Comandos                      | Apresenta uma lista de todos os atalhos disponíveis.                                                                                 |
| **Alt + S**     | Definições                             | Abre o diálogo de definições do Vision Assistant Pro.                                                                                |
| **Alt + Q**     | Relatório de Chaves com Quota Excedida | Comunica o número de chaves de API do Gemini que excederam a sua quota diária e o respetivo tempo de reposição.                      |
| **Alt + M**     | Auditoria de Encaminhamento            | Comunica os modelos de IA atualmente selecionados no encaminhamento avançado.                                                        |

## 3. Operador de IA - Controlo Autónomo do Computador

O **Operador de IA** transforma o Vision Assistant Pro de um leitor passivo num assistente ativo que pode interagir com o seu computador em seu nome. Pode pedir-lhe para descrever o ecrã, responder a perguntas sobre o que vê ou até mesmo assumir o controlo — clicando em botões, arrastando itens, escrevendo texto e navegando pelas aplicações através de comandos em linguagem natural.

A maior vantagem? Funciona perfeitamente em software completamente inacessível. Se estiver bloqueado numa aplicação personalizada, num ambiente de trabalho remoto ou num sítio Web onde o seu leitor de ecrã fica totalmente silencioso, o operador não se importa. Como "vê" o ecrã visualmente, consegue encontrar, ler e interagir com elementos que têm zero etiquetas de acessibilidade.

### Como Funciona

1. Prima **NVDA + Shift + V** e, em seguida, prima **Shift + A** (ou utilize o atalho direto) para abrir o diálogo do Operador de IA.
2. Escreva o que deseja fazer em linguagem simples (por exemplo, "Clicar no botão Guardar", "O que diz a mensagem de erro?" ou "Mudar o nome do ficheiro para final.pdf").
3. A IA analisará o seu ecrã, identificará os elementos relevantes e executará a ação ou fornecerá a resposta. Se uma tarefa exigir múltiplos passos, o operador continuará a trabalhar até que esteja concluída.
4. Prima **Shift + A** novamente a qualquer momento para abortar instantaneamente uma operação em curso.

### Ações Suportadas

O operador compreende uma vasta gama de comandos:

- **Descrever e Responder**: "Descrever o esquema visual do ecrã" ou "O que diz a mensagem de erro?"
- **Clicar**: "Clicar no botão Guardar"
- **Clique Direito**: "Clicar com o botão direito no ficheiro"
- **Duplo Clique**: "Clicar duas vezes no documento"
- **Arrastar e Largar**: "Arrastar o documento para a pasta Arquivo"
- **Escrever**: "Escrever 'Olá Mundo' na caixa de pesquisa"
- **Deslocar (Scroll)**: "Deslocar para baixo três vezes"
- **Premir Teclas**: "Premir Enter", "Premir Tab", "Premir Escape"
- **Tarefas de Múltiplos Passos**: "Abrir o Explorador de Ficheiros, encontrar o relatório e mudar o nome para final.pdf"

### Notas Importantes

- **⚠️ Aviso de Utilização da API**: Como o operador precisa de "ver" exatamente o que está a acontecer no ecrã, envia uma captura de ecrã de alta resolução a cada passo. A utilização frequente consumirá a sua quota de API muito mais rapidamente do que as funcionalidades padrão baseadas em texto.
- **Aplicações em Modo de Administrador**: Se o NVDA não estiver a ser executado com privilégios de Administrador, o operador poderá não conseguir interagir com janelas que exijam permissões elevadas. Esta é uma limitação de segurança do Windows e não um erro do extra.
- **Boas Práticas**: Para obter os melhores resultados, forneça comandos claros e específicos. "Clicar no botão azul Submeter na parte inferior do formulário" funcionará quase sempre melhor do que apenas "Clicar no botão".

## 4. Análise de Vídeo e Audiodescrição

> **Nota:** As funcionalidades de Análise de Vídeo e Audiodescrição são alimentadas estritamente pelo fornecedor **Google Gemini**. Certifique-se de que o seu fornecedor ativo nas definições do extra está configurado como Google Gemini.

O Vision Assistant Pro introduz capacidades poderosas de processamento de vídeo concebidas especificamente para utilizadores cegos. Pode analisar tanto vídeos online como gravações de ecrã locais para fornecer descrições visuais altamente detalhadas e gerar guiões profissionais de Audiodescrição (SRT).

### 4.1 Gravação de Ecrã Local (Control + V)

Se encontrar um vídeo silencioso, uma animação ou um tutorial no seu ecrã, pode capturá-lo diretamente:

1. Prima **NVDA + Shift + V** para entrar na Camada de Comando e, em seguida, prima **Control + V**.
2. O extra gravará o seu ecrã silenciosamente em segundo plano.
3. Prima **Control + V** novamente para parar a gravação.
4. A IA analisará então o segmento de vídeo gravado e fornecerá uma descrição altamente detalhada da cena, das personagens e das ações.

### 4.2 Análise de Vídeo (Shift + V)

Pode analisar tanto ficheiros de vídeo locais como vídeos online. Basta selecionar um ficheiro de vídeo local no Explorador do Windows ou copiar o link de um vídeo online para a sua área de transferência. Também pode premir **Shift + V** em qualquer lugar (como dentro de um reprodutor de multimédia) para abrir um diálogo onde pode procurar um ficheiro de vídeo ou colar um URL manualmente.

- **Plataformas Online Suportadas:** YouTube, Instagram, TikTok e Twitter (X).
- A IA detetará automaticamente o ficheiro local ou o URL, processará o vídeo e fornecerá uma descrição visual abrangente e um resumo áudio.

### 4.3 Geração de Audiodescrição (SRT)

Para uma experiência mais estruturada, o extra pode gerar guiões profissionais de Audiodescrição no formato padrão SubRip (SRT).

- **Temporização Inteligente de Pausas:** A IA ouve a faixa de áudio e ancora especificamente as suas descrições visuais nas pausas naturais e intervalos de silêncio para minimizar de forma inteligente a sobreposição com os diálogos.
- **Rastreio de Personagens:** O motor realiza uma análise prévia para extrair personagens distintas com base em características faciais imutáveis. Cria um dicionário global para rastrear e etiquetar com precisão as personagens ao longo de diferentes cenas, sem confusões.
- **OCR de Texto Ipsis Verbis:** Qualquer texto que apareça no ecrã (sinais, telemóveis, créditos) é estritamente citado palavra por palavra.
- **Como Utilizar:** Para ouvir a legenda gerada, basta colocar o ficheiro `.srt` na mesma pasta que o seu ficheiro de vídeo e dar-lhe exatamente o mesmo nome. Depois, configure o seu reprodutor de multimédia (por exemplo, VLC ou PotPlayer) para encaminhar o texto da legenda diretamente para o seu leitor de ecrã ou motor de TTS durante a reprodução.

### 4.4 Narração de Áudio Sincronizada (Exportação para MP3)

Além de apenas criar ficheiros SRT baseados em texto, o extra funciona como uma ferramenta completa de produção de Audiodescrição, sintetizando as descrições em voz e misturando-as com o vídeo. Ao gerar um MP3 para ficheiros de vídeo locais, dispõe de múltiplos modos de mistura:

- **AD Padrão (Misturar Voz):** A narração é sobreposta diretamente na faixa de áudio do vídeo. Ser-lhe-á perguntado se deseja aplicar o **Audio Ducking** (reduzir o volume de fundo durante as descrições) para garantir que a narração seja clara.
- **AD Estendida (Pausar Áudio):** O motor pausa o áudio original do vídeo durante as descrições, garantindo que nunca perde uma única palavra do diálogo original ou da narração da IA.
- **Vídeos do YouTube:** Para fontes do YouTube (que não são descarregadas localmente), a exportação para MP3 conterá estritamente a faixa de voz da IA sincronizada, sem o áudio de fundo do vídeo.

## 5. Leitor Avançado de Documentos e Imagens

O Vision Assistant Pro inclui um Leitor de Documentos altamente otimizado, concebido para PDFs de várias páginas, imagens complexas e até formatos HEIC do iPhone.

### 5.1 Processamento em Lote e Retoma

Não precisa de ler um documento massivo de uma só vez. Introduza um intervalo de páginas (por exemplo, `1-20`) e a IA processará todas as páginas em segundo plano. Se o NVDA falhar ou se interromper a análise, o extra lembrar-se-á do seu progresso e oferecer-se-á para **Retomar** exatamente de onde parou!

### 5.2 Ação Inteligente de Ficheiros

Nem sempre precisa de abrir o documento primeiro. No Explorador de Ficheiros do Windows, basta selecionar um PDF ou imagem e premir **D** (Leitor de Documentos) ou **F** (Ação Inteligente de Ficheiros) dentro da Camada de Comando. O extra contornará instantaneamente o diálogo de ficheiro e começará a processar o ficheiro selecionado.

### 5.3 Atalhos do Visualizador de Documentos

Quando a janela do Leitor de Documentos estiver aberta, pode utilizar os seguintes atalhos:

- **Ctrl + PageDown:** Mudar para a página seguinte.
- **Ctrl + PageUp:** Mudar para a página anterior.
- **Alt + A:** Abrir um diálogo de chat para fazer perguntas sobre o documento.
- **Alt + R:** Forçar uma **Nova análise com IA** utilizando o seu fornecedor ativo.
- **Alt + G:** Gerar e guardar um ficheiro de áudio de alta qualidade (WAV/MP3). _(Oculto se o fornecedor não suportar TTS)._
- **Alt + S / Ctrl + S:** Guardar o texto extraído como um ficheiro TXT ou HTML.

## 6. Etiquetagem Semântica por IA e Explorador de IU

Bloqueado numa aplicação com "botão sem etiqueta" por todo o lado? O motor de Etiquetagem Semântica por IA resolve isto permanentemente.

### 6.1 Etiquetagem Permanente de Objetos (L)

Foque o seu leitor de ecrã num gráfico ou botão sem etiqueta e prima **L** na Camada de Comando. A IA olhará para o botão visualmente, determinará a sua função e aplicará uma etiqueta permanente.
_Ao contrário das antigas ferramentas de etiquetagem dos leitores de ecrã, este extra utiliza um sistema híbrido avançado de "Assinatura do Objeto" (AutomationId/ControlID). As suas etiquetas personalizadas sobreviverão ao redimensionamento de janelas, à troca de monitores e às atualizações da aplicação!_

### 6.2 Análise Completa da Aplicação (Shift + L)

Prima **Shift + L** para analisar toda a janela ativa de uma só vez. A IA encontrará todos os elementos sem etiqueta e nomeá-los-á inteligentemente de uma só assentada. Mais tarde, poderá gerir, renomear ou eliminar em lote estas etiquetas a partir do Gestor de Etiquetas integrado.

### 6.3 Explorador de IU (E)

Precisa de interagir com um elemento sem navegar até ele manualmente? Prima **E** para ativar o Explorador de IU. A IA analisará o ecrã e gerará uma lista acessível de todos os elementos clicáveis (ignorando o ruído do sistema, como as barras de tarefas). Escolha um item da lista e o extra clicará instantaneamente nele por si.

## 7. Assistente de Voz em Direto

O Assistente em Direto transforma o Vision Assistant Pro num copiloto interativo em tempo real.
_(Nota: Esta funcionalidade é exclusiva do Google Gemini e de fornecedores Personalizados compatíveis com o Gemini)._

- **Ativação:** Prima **Control + L** na Camada de Comando para abrir o diálogo do Assistente em Direto.
- **Interação em Tempo Real:** Fale naturalmente através do seu microfone. A IA ouvirá simultaneamente a sua voz e olhará para o seu ecrã ativo. Pode fazer perguntas como "O que estou a ver?" ou "Lê-me o terceiro parágrafo".
- **Personalização:** Dentro do diálogo, pode alterar o Estilo de Voz da IA (por exemplo, Profissional, Amigável, Animado) e ajustar a sua "Profundidade de Pensamento" para controlar o quão profundamente ela raciocina antes de responder.

## 8. Prompts Personalizados e Variáveis

Pode gerir os prompts em **Definições > Prompts > Gerir Prompts...**.

### Variáveis Suportadas

- `[selection]`: Texto selecionado atualmente.
- `[clipboard]`: Conteúdo da área de transferência.
- `[clipboard_image]`: Imagem atualmente na área de transferência.
- `[screen_obj]`: Captura de ecrã do objeto do navegador.
- `[screen_fg_obj]`: Captura de ecrã da janela de primeiro plano ativa.
- `[screen_full]`: Captura de ecrã de ecrã inteiro.
- `[file_ocr]`: Selecionar ficheiro de imagem/PDF para extração de texto.
- `[file_read]`: Selecionar documento para leitura (TXT, Código, PDF).
- `[file_audio]`: Selecionar ficheiro de áudio para análise (MP3, WAV, OGG).
- `{target_lang}`: Idioma de destino atual.
- `{source_lang}`: Idioma de origem atual.
- `{response_lang}`: Idioma de resposta da IA atual.
- `{swap_target}`: Idioma de recurso para tradução com troca inteligente.
- `{swap_instruction}`: Bloco de instruções de tradução com troca inteligente.

## 9. Casos de Uso do Mundo Real (Que funcionalidade devo utilizar?)

O Vision Assistant Pro está repleto de ferramentas avançadas. Eis alguns cenários comuns para o ajudar a escolher a ferramenta certa:

- **Cenário: Pretende compreender o esquema visual completo de uma janela complicada ou de uma aplicação inacessível.**
  _Solução:_ Prima **O** (Visão de Ecrã Inteiro). A IA analisará todo o ecrã e descreverá exatamente onde estão posicionados os elementos, textos e botões.

- **Cenário: Encontrou uma imagem numa página Web ou um gráfico sem etiqueta num documento.**
  _Solução:_ Mova o seu objeto do navegador para o gráfico e prima **V** (Visão de Objetos). A IA descreverá especificamente o que essa imagem contém.

- **Cenário: Deseja ver um filme ou um videoclipe com audiodescrições.**
  _Solução:_ Prima **Shift + V** no seu vídeo e escolha **"Gerar Audiodescrição (Ficheiro SRT)"**. Quando terminar, clique em **"Gerar Narração Sincronizada (MP3)"** e selecione **"AD Estendida"**. O extra criará uma faixa de áudio que pausa inteligentemente o diálogo do filme para descrever as cenas visuais.

- **Cenário: Encontrou uma aplicação cheia de "botões sem etiqueta".**
  _Solução:_ Prima **L** para etiquetar permanentemente o botão específico utilizando IA. Ou prima **Shift + L** para analisar e etiquetar toda a janela de uma só vez. Se apenas quiser clicar em algo rapidamente, prima **E** (Explorador de IU) para obter uma lista de todos os itens clicáveis.

- **Cenário: Precisa de contornar um CAPTCHA inacessível.**
  _Solução:_ Prima **C** (Resolução de CAPTCHAs). A IA capturará automaticamente o CAPTCHA, irá resolvê-lo e injetará a resposta no campo correto.

- **Cenário: Pretende ler um documento PDF longo de 50 páginas.**
  _Solução:_ Prima **D** (Leitor de Documentos), configure o seu fornecedor como Google Gemini e introduza o intervalo de páginas `1-50`. O extra extrairá o texto com precisão em segundo plano.

- **Cenário: Está a ver um tutorial em vídeo silencioso ou uma animação no seu ecrã.**
  _Solução:_ Prima **Control + V** para iniciar a gravação do ecrã. Deixe o tutorial decorrer e, em seguida, prima **Control + V** novamente. A IA explicará exatamente o que foi demonstrado.

***
**Nota:** É necessária uma ligação ativa à Internet para todas as funcionalidades de IA. Os documentos de várias páginas são processados automaticamente.

## 10. Suporte e Comunidade

Mantenha-se atualizado com as últimas notícias, funcionalidades e lançamentos:

- **Canal do Telegram:** [t.me/VisionAssistantPro](https://t.me/VisionAssistantPro)
- **Problemas no GitHub (Issues):** For relatórios de erros e pedidos de funcionalidades.

## 11. Apoiantes do Projeto

Um agradecimento sincero aos membros da nossa comunidade que apoiam o desenvolvimento contínuo e a manutenção deste projeto através das suas generosas contribuições financeiras:

- **@Alyabani94**
- **Ali Alamri**
- **Ilya**
- **Apoiante Anónimo** (`UQDd...CnMY`)
- **leonardo0216**
- **Sergei Fleytin**
- **Suman Gayen**

_Se desejar apoiar financeiramente o projeto e ver o seu nome aqui, pode encontrar a opção **Doar** no menu Ferramentas do NVDA (submenu Vision Assistant) ou durante o processo de configuração após a instalação._

## Alterações para 2026.07.15

- **Filtragem Inteligente de Modelos de API**: Reformulação completa do sistema de filtragem de modelos para utilizar uma abordagem puramente baseada em lista de bloqueio (blacklist) em vez de listas de permissão (whitelists). Foram adicionadas palavras-chave de filtragem mais fortes (`embedding`, `bison`, `gecko`, `audio`, `realtime`, `babbage`, `moderation`, `deep`, `antigravity`, `computer`) para garantir que a lista pendente do modelo de chat principal permaneça perfeitamente limpa e preparada para o futuro, mantendo todos os modelos especializados acessíveis na secção de Encaminhamento Avançado.
- **Pesquisa no Encaminhamento Avançado**: Todas as listas pendentes do Encaminhamento Avançado de Modelos (OCR, STT, TTS, Operador, Vídeo, Live) e o seletor de Variantes do eSpeak são agora totalmente pesquisáveis. Pode digitar rapidamente para filtrar e encontrar o modelo ou variante desejado.
- **Novos Atalhos da Camada de Comando**:
  - **Definições (`Alt + S`)**: Abre instantaneamente o diálogo de definições do Vision Assistant Pro.
  - **Relatório de Chaves com Quota Excedida (`Alt + Q`)**: Comunica o número exato de chaves de API do Gemini que excederam a sua quota diária, identificando em que modelo específico se esgotaram, e anuncia o seu tempo exato de reposição.
  - **Auditoria de Encaminhamento (`Alt + M`)**: Audita e anuncia a sua configuração atual de Encaminhamento Avançado, lendo quais os modelos que estão ativamente selecionados para tarefas especializadas (ignorando as definições predefinidas).
- **Reformulação Completa do Analisador de Vídeo**: O Analisador de Vídeo foi completamente transformado! Anteriormente, fornecia apenas uma descrição básica de vídeos online. Agora, é uma suite abrangente de processamento de vídeo adaptada para utilizadores cegos:
  - **Gravação de Ecrã Local (`Control+V`)**: Agora pode gravar vídeos silenciosos diretamente do seu ecrã. A IA analisará o segmento gravado e fornecerá uma descrição altamente detalhada da cena, do esquema visual e das ações.
  - **Geração de Audiodescrição (SRT)**: O extra pode agora gerar guiões de Audiodescrição altamente detalhados (no formato padrão SRT) para vídeos, com uma temporização inteligente de pausas para ancorar as descrições de forma inteligente nos intervalos naturais da faixa de áudio, além de OCR ipsis verbis para qualquer texto no ecrã.
  - **Narração de Áudio Sincronizada (Exportação para MP3)**: Para além das legendas baseadas em texto, o extra pode sintetizar a Audiodescrição em voz, misturá-la automaticamente com a faixa de áudio original do vídeo, aplicar audio ducking (reduzir o volume de fundo durante as descrições) e exportar o resultado final sincronizado como um ficheiro MP3!
  - **Ação Inteligente de Ficheiros de Vídeo**: Se focar um ficheiro de vídeo local e premir o atalho de vídeo, o extra detetá-lo-á automaticamente e processará o ficheiro diretamente.
  - **Rastreio Avançado de Personagens**: A IA realiza agora uma análise prévia de extração de personagens. Cria um dicionário global de personagens e rastreia-as com precisão segmento por segmento, sem confundir identidades.
  - **Configuração da Análise de Vídeo**: Adicionadas novas definições para controlar o tamanho dos blocos de SRT, legendagem de personagens e avisos legais.
  - **Encaminhamento de Modelos Estendido**: Agora pode selecionar explicitamente modelos de vídeo especializados (`gemini_video_model`, `custom_video_model`) nas definições de Encaminhamento Avançado de Modelos.
- **Gestão Inteligente de Quotas da API**: Manipulação aprimorada de erros 429 (Limite Diário) através do rastreio de quotas por modelo. Se uma chave atingir o seu limite diário num modelo, é inteligentemente colocada em quarentena apenas para esse modelo específico, deixando a chave disponível para utilização com outros modelos.

## Alterações para 7.0.0

- **Retoma de Análises Inacabadas**: Adicionada uma funcionalidade de retoma tanto para o Leitor de Documentos como para as Ações Inteligentes de Ficheiros. Se uma análise for interrompida, pode agora continuar a partir do ponto onde parou, em vez de recomeçar do zero.
- **Nova Variável `[screen_fg_obj]`**: Adicionada uma variável de prompt personalizada para capturar uma imagem de apenas a janela de primeiro plano ativa, em vez do ecrã inteiro.
- **Tentativas Inteligentes e Rotação de Chaves**: O extra tenta agora silenciosamente até 5 vezes na mesma chave ao atingir sobrecargas temporárias do servidor (como "alta procura" ou respostas malformadas). Se as tentativas falharem, muda automaticamente para a chave de API seguinte na sua lista.
- **Deteção de Cortina de Ecrã**: Adicionada uma verificação para impedir a captura de imagens quando a Cortina de Ecrã estiver ativa (quer esteja permanentemente ativada ou ligada temporariamente com o atalho). Irá avisá-lo e parar, evitando que envie imagens pretas e desperdice tokens de API.
- **Ajustes no Leitor de Documentos**: O diálogo de intervalo de páginas do PDF agora pré-seleciona automaticamente o idioma de destino predefinido das definições do seu extra. Também foi melhorada a gestão de threads para garantir que as tarefas em segundo plano param de forma limpa quando o leitor é fechado.
- **Integração Nativa de OCR do Mistral**: Integrada a API nativa de OCR de Documentos do Mistral. Os documentos de várias páginas são fundidos automaticamente, carregados e processados em lotes utilizando o endpoint especializado `/v1/ocr` do Mistral, enquanto as imagens de página única são processadas diretamente sem conversões desnecessárias para PDF [1].
- **Manipuladores Dinâmicos de URL Personalizado**: A modificação do URL da API Personalizada agora limpa instantaneamente a lista de modelos em cache e restaura a caixa de texto de introdução manual de modelos. Isto garante total compatibilidade com endpoints personalizados (como o Cloudflare AI Gateway) que não suportam o endpoint padrão de listagem `/v1/models`.
- **Motor de Introdução do Operador de IA Reformulado**: O sistema subjacente de simulação de rato e teclado para o Operador de IA foi completamente rescrito. Substituiu-se a API antiga `mouse_event` pela API moderna `SendInput` do Windows, trazendo uma compatibilidade significativamente maior com aplicações modernas, janelas protegidas por UAC e ecrãs com alta densidade de píxeis (DPI).
- **Operações de Arrastar e Largar Corrigidas**: As ações de arrastar e largar no Operador de IA são agora totalmente estáveis e fiáveis. O novo motor utiliza curvas de transição ("easing") naturais, posicionamento preciso do cursor, temporização otimizada e uma técnica inteligente de "toque" para garantir que o Windows e as aplicações reconhecem e executam corretamente os gestos de arrastar e largar sem falhar a meio do caminho.
- **Suporte Multi-Monitor**: O Operador de IA suporta agora totalmente configurações com múltiplos monitores. Os movimentos e cliques do rato funcionam corretamente em todos os monitores utilizando a flag `MOUSEEVENTF_VIRTUALDESK`, garantindo o posicionamento preciso independentemente do monitor onde a aplicação alvo se encontra.
- **Simulação de Teclado Melhorada**: Melhorada a injeção de teclas para suportar totalmente "Teclas Estendidas" (tais como as setas, Home, End, Page Up/Down, Insert, Delete e F1-F12). Isto garante que os comandos de navegação e atalhos enviados pelo Operador de IA funcionam na perfeição em todas as aplicações.
- **Suporte para Imagens HEIC/HEIF**: Adicionado suporte nativo para os formatos de fotografia do iPhone. Pode agora selecionar diretamente ficheiros `.heic` e `.heif` para descrição por IA, OCR ou Leitura de Documentos sem necessidade de conversão prévia.

## Alterações para 6.5.0

- **Assistente em Direto**: Adicionada uma funcionalidade de assistente de voz e ecrã em tempo real, disponível exclusivamente para o fornecedor Google Gemini (or fornecedores personalizados compatíveis com o Gemini). Inclui personalização interativa da voz e da profundidade de pensamento diretamente dentro do diálogo, com religação automática ao alterar as definições.
- **Fornecedor de IA MiniMax**: Integrado o MiniMax como um fornecedor homólogo com suporte multimodal completo (chat, visão, OCR), TTS personalizado com mais de 300+ vozes dinâmicas e remoção automática de blocos de raciocínio (ex: `<think>...</think>`) dos resultados.
- **Tradução do Visualizador de Documentos**: Corrigida uma falha silenciosa na tradução para utilizadores do NVDA que não utilizam o inglês, garantindo que o código de idioma padrão de 2 letras é enviado para o Google Tradutor em vez do nome do idioma localizado.
- **Nova Tentativa de Análise em Lote de PDF**: Implementada uma lógica de nova tentativa separada, silenciosa e altamente otimizada para a análise em lote de documentos PDF, de forma a evitar carregamentos redundantes e janelas pop-up de erro incómodas durante as tentativas.
- **Estado do Visualizador de Documentos**: Corrigido um erro onde o estado geral do plugin (verificado através de `I`) ficava bloqueado em "Processamento em Lote Iniciado" durante análises de documentos longos.
- **Resolvido Bloqueio de Threads**: Corrigido um bloqueio grave de asserção de thread `IsMain() failed in wxTimerImpl` ao abrir documentos a partir de uma thread em segundo plano, transitando a fila de chamadas da GUI para `wx.CallAfter`.

## Alterações para 6.1.2

- **Pré-Verificação de Etiquetas Duplicadas**: Corrigido um problema na etiquetagem individual onde a verificação de duplicados utilizava chaves de coordenadas antigas, fazendo com que o NVDA fizesse pedidos de IA duplicados para objetos já etiquetados em vez de anunciar a etiqueta existente.
- **Chat de Documentos para Fornecedores Não-Gemini**: Corrigida uma verificação estrita da chave de API no Chat de Documentos (`on_ask`) para garantir que os utilizadores no OpenAI, Groq ou fornecedores Personalizados locais (como o Ollama) conseguem conversar com os documentos com sucesso sem serem bloqueados.
- **Tradução Rápida de OCR do Chrome**: Restaurada a API de tradução gratuita e sem chave para o OCR do Chrome. A tradução do texto extraído agora ignora a IA do Gemini, poupando quotas de API e acelerando o processo de tradução.
- **Filtro Alfanumérico de CAPTCHA**: Corrigida a lógica de filtragem no resolvedor de CAPTCHAs para garantir que os caracteres não alfanuméricos são devidamente limpos em todas as situações.
- **Atualização da Ajuda da Camada de Comando**: Corrigido o atalho do anúncio de estado no menu de ajuda de `L` para `I`, e adicionados ambos os comandos de etiquetagem (`L` e `Shift+L`) à lista.

## Alterações para 6.1.1

- **Correção do Resultado de Pensamento do Gemma 4**: Corrigido um problema com os modelos Gemma 4 onde todo o processo interno de pensamento era exibido como a resposta final, ou onde desativar o pensamento resultava em respostas vazias. O extra agora isola e extrai corretamente apenas a resposta de texto limpa final.
- **OCR em Lote a partir do Explorador de Ficheiros**: Agora pode selecionar múltiplas fotografias ou PDFs diretamente no Explorador de Ficheiros do Windows e extrair texto ou analisá-los em lote. O extra filtrará e processará automaticamente apenas os formatos de ficheiro suportados.

## Alterações para 6.1.0

- **Integração Universal de IA Local (Configurar IA Local)**: Adicionado um novo botão **"Configurar IA Local"** nas Definições do Fornecedor Personalizado. Os utilizadores podem agora configurar automaticamente motores de IA locais, incluindo o **Ollama**, **LM Studio**, **Jan.ai** e **KoboldCPP** instantaneamente.
- **Desvio Inteligente de Proxy Local**: Reconfigurada a lógica de conexão com um mecanismo avançado de desvio de proxy. O extra é agora inteligente o suficiente para ignorar completamente os proxies do sistema Windows para ligações de loopback local, garantindo ligações estáveis à IA local mesmo quando a sua VPN/modo TUN está ativo.
- **Etiquetagem por IA Ultra-Estável (v2)**: Substituição das chaves de coordenadas de ecrã absolutas por um sistema híbrido avançado de **Assinatura do Objeto**. As etiquetas baseiam-se agora em identificadores programáticos (UIA **AutomationId** ou Win32 **ControlID**) e coordenadas relativas à janela, tornando as suas etiquetas personalizadas completamente resistentes ao redimensionamento de janelas, movimentação, troca de monitores ou redimensionamento de escala.
- **Migração Automática e Transparente de Etiquetas**: A atualização é completamente transparente. O extra migrará automaticamente as suas etiquetas antigas baseadas em coordenadas para o novo formato estável de assinatura em segundo plano no primeiro foco, com zero perda de dados.

## Alterações para 6.0

- **Apresentação da Etiquetagem Semântica por IA**: Os utilizadores podem agora etiquetar permanentemente botões e ícones sem nome utilizando IA. Prima **L** para etiquetar o objeto atual do navegador (suportando tanto o foco por Tab como a navegação de objetos) ou **Shift+L** para analisar e etiquetar toda a aplicação de uma só vez.
- **Gestão Inteligente de Etiquetas**: Adicionado um novo diálogo de Gestor de Etiquetas totalmente acessível (através de **Shift+L** se existirem etiquetas) para visualizar, renomear ou eliminar em lote etiquetas personalizadas.
- **Análise Direta de Ficheiros (Ignorar Diálogo de Ficheiro)**: O extra é agora inteligente o suficiente para detetar se está atualmente focado num ficheiro PDF ou de imagem no Explorador de Ficheiros do Windows. Premir **F (Ação Inteligente de Ficheiros)** ou **D (Leitor de Documentos)** num ficheiro selecionado irá processá-lo imediatamente, ignorando completamente o diálogo padrão "Abrir".

## Alterações para 5.6

- **Adicionado Motor de OCR "Nenhum (Extrair Camada de Texto)"**: Os utilizadores podem agora extrair texto diretamente de PDFs pesquisáveis sem gastar créditos de IA, melhorando significativamente a velocidade e a privacidade dos documentos baseados em texto.
- **Precisão Refinada do Explorador de IU**: Melhorado o prompt do Explorador de IU para identificar melhor os tipos de elementos (como Itens de Lista) e comunicar com precisão estados como "(Marcado)", "(Selecionado)" ou "(Expandido)", ignorando componentes do sistema Windows como a Barra de Tarefas e o Relógio.
- **Lembrete de Configuração de Instalação**: Adicionada uma notificação após a instalação para guiar os utilizadores ao menu de definições para configurarem as suas chaves de API e preferências.

## Alterações para 5.5.2

- **Corrigido Problema de Escrita do Operador de IA**: Resolvido um erro onde a letra 'v' era digitada em vez de colar texto em determinados sistemas. Esta correção aborda conflitos de temporização que ocorriam durante uma elevada carga do sistema.
- **Estabilidade Melhorada**: Adicionada uma manipulação robusta de erros para operações da área de transferência para evitar bloqueios do extra quando a área de transferência do sistema está temporariamente bloqueada por outras aplicações.
- **Otimização de Temporização**: Ajustados os atrasos internos para eventos de teclado para garantir maior fiabilidade em diferentes velocidades do sistema e melhor compatibilidade com Gestores de Área de Transferência de terceiros.

## Alterações para 5.5 (A Atualização de Automação)

- **Operador de IA (Controlo Autónomo - Shift+A):** Esta é a joia da coroa da v5.5. O Vision Assistant Pro evoluiu de um assistente passivo para se tornar o seu **Operador de IA** pessoal. Não se limita a descrever o ecrã — ele assume o comando.
  - _Como funciona:_ Agora pode dar instruções verbais para operar o seu PC. Por exemplo, numa aplicação completamente inacessível onde o seu leitor de ecrã fica silencioso, pode premir **Shift+A** e digitar: _"Clicar no botão Definições"_ ou _"Encontrar o campo de pesquisa, digitar 'Últimas Notícias' e premir enter."_ A IA identifica visualmente os elementos, move o rato e executa a tarefa por si.
  - _Nota de Desempenho:_ Esta funcionalidade está otimizada para o **Gemini 3.0 Flash (Preview)**, fornecendo respostas incrivelmente rápidas e inteligentes que conseguem lidar até com os esquemas de IU mais complexos.
  - **⚠️ Aviso de Utilização da API:** Como o Operador de IA precisa de "ver" exatamente o que está a acontecer para ser preciso, envia uma captura de ecrã de alta resolução a cada passo. Tenha em atenção que a utilização frequente consumirá a sua quota de API muito mais rapidamente do que as tarefas padrão baseadas em texto.
- **Explorador Visual de IU (E):** Cansado de navegar por "botões sem etiqueta"? Prima **E** para ativar o Explorador de IU. A IA analisará a janela inteira e gerará uma lista de todos os elementos clicáveis que vê — incluindo ícones, gráficos e menus. Basta escolher um item da lista e o Operador de IA clicará nele por si. É como ter uma "camada acessível" por cima de qualquer aplicação.
- **Ação Inteligente de Ficheiros Contextual (F):** A tecla "F" foi completamente reformulada. Já não assume que deseja apenas o OCR. Quando seleciona uma única imagem, agora pergunta inteligentemente qual é a sua intenção: pode escolher uma **Descrição Visual Detalhada** para compreender a cena ou uma **Extração de Texto Estruturada (OCR)** para leitura. O menu adapta-se dinamicamente com base no tipo de ficheiro e no seu motor de IA ativo.
- **Otimização do Núcleo:** Realizámos uma limpeza profunda na lógica interna do extra, removendo funções antigas não utilizadas e código redundante. Isto resulta numa experiência mais leve, rápida e fiável para todos os utilizadores.

## Alterações para 5.0

- **Arquitetura Multi-Fornecedor**: Adicionado suporte completo para o **OpenAI**, **Groq** e **Mistral** a par do Google Gemini. Os utilizadores podem agora escolher a sua plataforma de IA preferida.
- **Encaminhamento Avançado de Modelos**: Os utilizadores de fornecedores nativos (Gemini, OpenAI, etc.) podem agora selecionar modelos específicos a partir de uma lista pendente para diferentes tarefas (OCR, STT, TTS).
- **Configuração Avançada de Endpoint**: Os utilizadores de fornecedores personalizados podem introduzir manualmente URLs e nomes de modelos específicos para um controlo granular sobre servidores locais ou de terceiros.
- **Visibilidade Inteligente de Funcionalidades**: O menu de definições e a IU do Leitor de Documentos agora ocultam automaticamente as funcionalidades não suportadas (como o TTS) com base no fornecedor selecionado.
- **Procura Dinâmica de Modelos**: O extra agora procura a lista de modelos disponíveis diretamente a partir da API do fornecedor, garantindo a compatibilidade com novos modelos assim que são lançados.
- **OCR e Tradução Híbridos**: Otimizada a lógica para utilizar o Google Tradutor por uma questão de velocidade ao utilizar o OCR do Chrome, e tradução baseada em IA ao utilizar os motores Gemini/Groq/OpenAI.
- **"Nova Análise com IA" Universal**: A funcionalidade de nova análise do Leitor de Documentos já não está limitada ao Gemini. Agora utiliza o fornecedor de IA que estiver ativamente selecionado para reprocessar as páginas.

## Alterações para 4.6

- **Rechamada Interativa de Resultados:** Adicionada a tecla **Espaço** à camada de comando, permitindo aos utilizadores reabrir instantaneamente a última resposta da IA numa janela de chat para perguntas de acompanhamento, mesmo quando o modo "Saída Direta" está ativo.
- **Centro de Comunidade do Telegram:** Adicionado um link para o "Canal Oficial do Telegram" no menu Ferramentas do NVDA, fornecendo uma forma rápida de se manter atualizado com as últimas notícias, funcionalidades e lançamentos.
- **Estabilidade de Resposta Melhorada:** Otimizada a lógica central das funcionalidades de Tradução, OCR e Visão para garantir um desempenho mais fiável e uma experiência mais suave ao utilizar a saída direta de voz.
- **Orientação de Interface Aprimorada:** Atualizadas as descrições das definições e a documentação para explicar melhor o novo sistema de rechamada e como este funciona em conjunto com as definições de saída direta.

## Alterações para 4.5

- **Gestor Avançado de Prompts:** Introduzido um diálogo de gestão dedicado nas definições para personalizar os prompts padrão do sistema e gerir os prompts definidos pelo utilizador com suporte total para adicionar, editar, reordenar e pré-visualizar.
- **Suporte Abrangente de Proxy:** Resolvidos os problemas de conectividade de rede, garantindo que as definições de proxy configuradas pelo utilizador são estritamente aplicadas a todos os pedidos de API, incluindo tradução, OCR e geração de voz.
- **Migração Automática de Dados:** Integrado um sistema de migração inteligente para atualizar automaticamente as configurações antigas de prompts para um formato JSON v2 robusto na primeira execução, sem perda de dados.
- **Compatibilidade Atualizada (2025.1):** Definida a versão mínima do NVDA necessária para a 2025.1 devido a dependências de bibliotecas em funcionalidades avançadas, como o Leitor de Documentos, para garantir um desempenho estável.
- **Interface de Definições Otimizada:** Simplificada a interface de definições ao reorganizar a gestão de prompts num diálogo separado, proporcionando uma experiência de utilizador mais limpa e acessível.
- **Guia de Variáveis de Prompt:** Adicionado um guia integrado dentro dos diálogos de prompt para ajudar os utilizadores a identificar e utilizar facilmente variáveis dinâmicas como [selection], [clipboard] e [screen_obj].

## Alterações para 4.0.3

- **Resiliência de Rede Melhorada:** Adicionado um mecanismo de nova tentativa automática para lidar melhor com ligações de internet instáveis e erros temporários do servidor, garantindo respostas de IA mais fiáveis.
- **Diálogo Visual de Tradução:** Introduzida uma janela dedicada para os resultados de tradução. Os utilizadores podem agora navegar e ler facilmente traduções longas linha por linha, de forma semelhante aos resultados de OCR.
- **Visualização Formatada Agregada:** A funcionalidade "Ver Formatado" no Leitor de Documentos agora exibe todas as páginas processadas numa única janela organizada com cabeçalhos de página claros.
- **Fluxo de Trabalho de OCR Otimizado:** Ignora automaticamente a seleção do intervalo de páginas para documentos de página única, tornando o processo de reconhecimento mais rápido e fluido.
- **Estabilidade da API Melhorada:** Alteração para um método de autenticação baseado em cabeçalhos mais robusto, resolvendo potenciais erros de "Todas as chaves de API falharam" causados por conflitos na rotação de chaves.
- **Correções de Erros:** Resolvidos vários bloqueios potenciais, incluindo um problema durante o encerramento do extra e um erro de foco no diálogo de chat.

## Alterações para 4.0.1

- **Leitor Avançado de Documentos:** Um novo e poderoso visualizador para PDF e imagens com seleção de intervalo de páginas, processamento em segundo plano e navegação fluida com `Ctrl+PageUp/Down`.
- **Novo Submenu de Ferramentas:** Adicionado um submenu dedicado "Vision Assistant" sob o menu Ferramentas do NVDA para um acesso mais rápido às principais funcionalidades, definições e documentação.
- **Personalização Flexível:** Pode agora escolher o seu motor de OCR e voz de TTS preferidos diretamente a partir do painel de definições.
- **Suporte para Múltiplas Chaves de API:** Adicionado suporte para múltiplas chaves de API do Gemini. Pode introduzir uma chave por linha ou separá-las com vírgulas nas definições.
- **Motor de OCR Alternativo:** Introduzido um novo motor de OCR para garantir um reconhecimento de texto fiável mesmo ao atingir os limites de quota da API do Gemini.
- **Rotação Inteligente de Chaves de API:** Altera automaticamente para a chave de API funcional mais rápida e memoriza-a para contornar os limites de quota.
- **Documento para MP3/WAV:** Capacidade integrada para gerar e guardar ficheiros de áudio de alta qualidade nos formatos MP3 (128kbps) e WAV diretamente dentro do leitor.
- **Suporte para Histórias do Instagram:** Adicionada a capacidade de descrever e analisar Histórias do Instagram utilizando os respetivos URLs.
- **Suporte para TikTok:** Introduzido o suporte para vídeos do TikTok, permitindo a descrição visual completa e a transcrição de áudio dos clipes.
- **Diálogo de Atualização Redesenhado:** Apresenta uma nova interface acessível com uma caixa de texto rolável para ler claramente as alterações da versão antes de instalar.
- **Estado e UX Unificados:** Padronizados os diálogos de ficheiro em todo o extra e aprimorado o comando 'L' para reportar o progresso em tempo real.

## Alterações para 3.6.0

- **Sistema de Ajuda:** Adicionado um comando de ajuda (`H`) dentro da Camada de Comando para fornecer uma lista de fácil acesso de todos os atalhos e as suas funções.
- **Análise de Vídeo Online:** Expandido o suporte para incluir vídeos do **Twitter (X)**. Também foi melhorada a deteção de URLs e a estabilidade para uma experiência mais fiável.
- **Contribuição para o Projeto:** Adicionado um diálogo opcional de doação para utilizadores que desejem apoiar as futuras atualizações e o crescimento contínuo do projeto.

## Changes for 3.5.0

- **Camada de Comando:** Introduzido um sistema de Camada de Comando (predefinido: `NVDA+Shift+V`) para agrupar atalhos sob uma única tecla mestre. Por exemplo, em vez de premir `NVDA+Control+Shift+T` para tradução, agora prime `NVDA+Shift+V` seguido de `T`.
- **Análise de Vídeo Online:** Adicionada uma nova funcionalidade para analisar vídeos do YouTube e do Instagram diretamente ao fornecer um URL.

## Alterações para 3.1.0

- **Modo de Saída Direta:** Adicionada uma opção para ignorar o diálogo de chat e ouvir as respostas da IA diretamente via voz para uma experiência mais rápida e fluida.
- **Integração com a Área de Transferência:** Adicionada uma nova definição para copiar automaticamente as respostas da IA para a área de transferência.

## Alterações para 3.0

- **Novos Idiomas:** Adicionadas as traduções em **Persa** e **Vietnamita**.
- **Modelos de IA Expandidos:** Reorganizada a lista de seleção de modelos com prefixos claros (`[Free]`, `[Pro]`, `[Auto]`) para ajudar os utilizadores a distinguir entre modelos gratuitos e limitados por taxa (pagos). Adicionado suporte para o **Gemini 3.0 Pro** e **Gemini 2.0 Flash Lite**.
- **Estabilidade de Ditação:** Melhorada significativamente a estabilidade da Ditação Inteligente. Adicionada uma verificação de segurança para ignorar clipes de áudio com menos de 1 segundo, prevenindo alucinações da IA e erros vazios.
- **Manipulação de Ficheiros:** Corrigido um problema onde o carregamento de ficheiros com nomes que não estavam em inglês falhava.
- **Otimização de Prompts:** Lógica de tradução melhorada e resultados de Visão estruturados.

## Alterações para 2.9

- **Adicionadas as traduções em Francês e Turco.**
- **Visualização Formatada:** Adicionado um botão "Ver Formatado" nos diálogos de chat para visualizar a conversa com a estilização correta (Títulos, Negrito, Código) numa janela padrão navegável.
- **Definição de Markdown:** Adicionada uma nova opção "Limpar Markdown no Chat" nas Definições. Desmarcar esta opção permite aos utilizadores ver a sintaxe Markdown em bruto (ex: `**`, `#`) na janela de chat.
- **Gestão de Diálogos:** Corrigido um problema onde as janelas de "Refinar Texto" ou de chat abriam múltiplas vezes ou falhavam ao focar corretamente.
- **Melhorias de UX:** Padronizados os títulos dos diálogos de ficheiro para "Abrir" e removidos os anúncios de voz redundantes (ex: "A abrir o menu...") para uma experiência mais suave.

## Alterações para 2.8

- Adicionada a tradução em Italiano.
- **Relatório de Estado:** Adicionado um novo comando (NVDA+Control+Shift+I) para anunciar o estado atual do extra (ex: "A carregar...", "A analisar...").
- **Exportação para HTML:** O botão "Guardar Conteúdo" nos diálogos de resultados agora guarda a saída como um ficheiro HTML formatado, preservando estilos como títulos e texto em negrito.
- **IU das Definições:** Layout do painel de Definições melhorado com agrupamento acessível.
- **Novos Modelos:** Adicionado suporte para gemini-flash-latest e gemini-flash-lite-latest.
- **Idiomas:** Adicionado o Nepalês aos idiomas suportados.
- **Lógica do Menu Refinar:** Corrigido um erro crítico onde os comandos de "Refinar Texto" falhavam se o idioma da interface do NVDA não fosse o inglês.
- **Ditação:** Melhorada a deteção de silêncio para evitar saídas de texto incorretas quando nenhuma voz é introduzida.
- **Definições de Atualização:** A opção "Verificar atualizações ao iniciar" está agora desativada por predefinição para cumprir as políticas da Loja de Extras.
- Limpeza de Código.

## Alterações para 2.7

- Migração da estrutura do projeto para o Modelo de Extra Oficial da NV Access para uma melhor conformidade com os padrões.
- Implementada uma lógica de nova tentativa automática para erros HTTP 429 (Limite de Taxa) para garantir a fiabilidade durante períodos de tráfego elevado.
- Otimização dos prompts de tradução para maior precisão e melhor manipulação da lógica "Smart Swap".
- Atualizada a tradução em Russo.

## Alterações para 2.6

- Adicionado suporte para a tradução em Russo (Obrigado ao nvda-ru).
- Atualizadas as mensagens de erro para fornecer um feedback mais descritivo sobre a conectividade.
- Alterado o idioma de destino predefinido para Inglês.

## Alterações para 2.5

- Adicionado o Comando Nativo de OCR de Ficheiro (NVDA+Control+Shift+F).
- Adicionado o botão "Guardar Chat" aos diálogos de resultados.
- Implementado suporte completo de localização (i18n).
- Migração do feedback de áudio para o módulo de tons nativos do NVDA.
- Mudança para a API de Ficheiros do Gemini para uma melhor manipulação de ficheiros PDF e de áudio.
- Corrigido o bloqueio ao traduzir texto que continha chavetas.

## Alterações para 2.1.1

- Corrigido um problema onde a variável [file_ocr] não funcionava corretamente dentro de Prompts Personalizados.

## Alterações para 2.1

- Padronizados todos os atalhos para utilizar NVDA+Control+Shift de modo a eliminar conflitos com o layout de Portátil do NVDA e com as teclas de atalho do sistema.

## Alterações para 2.0

- Implementado o sistema de Atualização Automática integrado.
- Adicionada a Cache de Tradução Inteligente para a recuperação instantânea de texto traduzido anteriormente.
- Adicionada a Memória de Conversação para refinar contextualmente os resultados nos diálogos de chat.
- Adicionado o comando de Tradução da Área de Transferência Dedicado (NVDA+Control+Shift+Y).
- Otimizados os prompts de IA para impor estritamente a saída no idioma de destino.
- Corrigido o bloqueio causado por caracteres especiais no texto de entrada.

## Alterações para 1.5

- Adicionado suporte para mais de 20 novos idiomas.
- Implementado o Diálogo Interativo de Refinação para perguntas de acompanhamento.
- Adicionada a funcionalidade Nativa de Ditação Inteligente.
- Adicionada a categoria "Vision Assistant" ao diálogo de Gestos de Entrada do NVDA.
- Corrigidos os bloqueios por COMError em aplicações específicas como o Firefox e o Word.
- Adicionado o mecanismo de nova tentativa automática para erros do servidor.

## Alterações para 1.0

- Lançamento inicial.
