# Documentação do Vision Assistant Pro

O **Vision Assistant Pro** é um assistente de IA multimodal avançado para o NVDA. Utiliza motores de IA de classe mundial para fornecer leitura de ecrã inteligente, tradução, ditado de voz e análise de documentos.

_Este suplemento foi lançado para a comunidade em homenagem ao Dia Internacional das Pessoas com Deficiência._

## 1. Configuração e Instalação

Aceda ao **Menu do NVDA > Preferências > Definições > Vision Assistant Pro**.

### 1.1 Definições de Conexão
- **Provedor:** Selecione o seu serviço de IA preferido. Os provedores suportados incluem o **Google Gemini**, **OpenAI**, **Mistral**, **Groq**, **MiniMax** e **Personalizado** (servidores compatíveis com OpenAI como Ollama, LM Studio, Jan.ai ou KoboldCPP).
- **Nota Importante:** Recomendamos vivamente a utilização do **Google Gemini** para obter o melhor desempenho e precisão (especialmente para a análise de imagens/ficheiros).
- **Chave de API:** Obrigatório. Pode introduzir várias chaves (separadas por vírgulas ou quebras de linha) para rotação automática.
- **Procurar Modelos:** Após introduzir a sua chave de API, prima este botão para descarregar a lista mais recente de modelos disponíveis do provedor.
- **Modelo de IA:** Selecione o modelo principal utilizado para chat geral e análise.

### 1.2 Encaminhamento Avançado de Modelos
*Disponível para todos os provedores, incluindo Gemini, OpenAI, Groq, Mistral e Personalizado.*

> **⚠️ Aviso:** Estas definições destinam-se **apenas a utilizadores avançados**. Se não tiver a certeza do que um modelo específico faz, por favor, deixe esta opção **desmarcada**. Selecionar um modelo incompatível para uma tarefa (por exemplo, um modelo apenas de texto para Visão) causará erros e fará com que o suplemento deixe de funcionar.

Assinale **"Encaminhamento Avançado de Modelos (Específico por Tarefa)"** para desbloquear o controlo detalhado. Isto permite-lhe selecionar modelos específicos da lista suspensa para diferentes tarefas:
- **Modelo de OCR / Visão:** Escolha um modelo especializado para analisar imagens.
- **Conversão de Fala em Texto (STT):** Escolha um modelo específico para ditado.
- **Conversão de Texto em Fala (TTS):** Escolha um modelo para gerar áudio.
- **Modelo de Operador de IA:** Selecione um modelo específico para tarefas de operação autónoma do computador.
*Nota: As funcionalidades não suportadas (por exemplo, TTS para o Groq) serão ocultadas automaticamente.*

### 1.3 Configuração Avançada de Endpoint (Provedor Personalizado)
*Disponível apenas quando "Personalizado" estiver selecionado.*

> **⚠️ Aviso:** Esta secção permite a configuração manual da API e foi concebida para **utilizadores experientes** que executam servidores locais ou proxies. URLs ou nomes de modelos incorretos quebrarão a conectividade. Se não sabe exatamente o que são estes endpoints, mantenha esta opção **desmarcada**.

Assinale **"Configuração Avançada de Endpoint"** para introduzir manualmente os detalhes do servidor. Ao contrário dos provedores nativos, aqui deve **digitar** as URLs e os nomes dos modelos específicos:
- **URL da Lista de Modelos:** O endpoint para procurar os modelos disponíveis.
- **URL do Endpoint de OCR/STT/TTS:** URLs completas para serviços específicos (por exemplo, `http://localhost:11434/v1/audio/speech`).
- **Modelos Personalizados:** Digite manualmente o nome do modelo (por exemplo, `llama3:8b`) para cada tarefa.

### 1.3.1 Configurar IA Local (Configuração Numa Única Ação)
Para tornar a integração de IA local e completamente offline extremamente simples, está disponível um botão dedicado **"Configurar IA Local"** dentro das Definições do Provedor Personalizado.

Se estiver a executar um servidor de modelo de IA local no seu computador:
1. Selecione **Personalizado** como o seu Provedor.
2. Prima o botão **Configurar IA Local**.
3. Escolha o seu motor de IA local na caixa de diálogo acessível:
   - **Ollama** (predefinição para `http://127.0.0.1:11434`)
   - **LM Studio** (predefinição para `http://127.0.0.1:1234`)
   - **Jan.ai** (predefinição para `http://127.0.0.1:1337`)
   - **KoboldCPP** (predefinição para `http://127.0.0.1:5001`)
4. O suplemento configurará instantaneamente a URL local correta, o tipo de API e procurará automaticamente os seus modelos offline ativos para preencher a caixa de seleção do **Modelo de IA**.

*Nota sobre Rede e Proxies:* Este motor de conexão local possui um sistema avançado de desvio de proxy. Mesmo que esteja a utilizar uma VPN ativa no sistema ou um proxy em modo TUN, os seus pedidos de IA local irão ignorá-lo completamente, garantindo ligações offline estáveis sem erros do tipo 502 Bad Gateway.

### 1.4 Preferências Gerais
- **Motor de OCR:** Escolha entre **Chrome (Rápido)** para resultados céleres ou **IA (Avançado)** para uma preservação superior do layout.
    - *Nota:* Se selecionar "IA (Avançado)", mas o seu provedor estiver configurado como OpenAI/Groq, o suplemento encaminhará inteligentemente a imagem para o modelo de visão do seu provedor ativo.
- **Voz do TTS:** Selecione o seu estilo de voz preferido. Esta lista é atualizada dinamicamente com base no seu provedor ativo.
- **Criatividade (Temperatura):** Controla a aleatoriedade da IA. Valores mais baixos são melhores para uma tradução/OCR precisos.
- **URL do Proxy:** Configure isto se os serviços de IA forem restritos na sua região (suporta proxies locais como `127.0.0.1` ou URLs de ponte).

## 2. Camada de Comando e Atalhos

Para evitar conflitos de teclado, este suplemento utiliza uma **Camada de Comando**.
1. Prima **NVDA + Shift + V** (Tecla Mestre) para ativar a camada (ouvirá um sinal sonoro).
2. Solte as teclas e, em seguida, prima uma das seguintes teclas individuais:

| Tecla         | Função                   | Descrição                                                                   |
|---------------|--------------------------|-----------------------------------------------------------------------------|
| **Shift + A** | **Operador de IA** | **Operação Autónoma:** Diga à IA para realizar uma tarefa no seu ecrã. Premir novamente aborta instantaneamente as operações ativas. |
| **E** | **Explorador de UI** | **Clique Interativo:** Identifica e clica em elementos da interface do utilizador em qualquer aplicação. |
| **T** | Tradutor Inteligente     | Traduz o texto sob o cursor de navegação ou seleção.                        |
| **Shift + T** | Tradutor de Transferência| Traduz o conteúdo que se encontra atualmente na área de transferência.       |
| **R** | Refinador de Texto       | Resume, corrige gramática, explica ou executa **Prompts Personalizados**.    |
| **V** | Visão de Objeto          | Descreve o objeto de navegação atual.                                       |
| **O** | Visão de Ecrã Inteiro    | Analisa o layout e o conteúdo de todo o ecrã.                               |
| **Shift + V** | Análise de Vídeo Online  | Analisa vídeos do **YouTube**, **Instagram**, **TikTok** ou **Twitter (X)**. |
| **D** | Leitor de Documentos     | Leitor avançado para PDF e imagens com seleção de intervalo de páginas.     |
| **F** | **Ação de Ficheiro Intel.** | Reconhecimento sensível ao contexto de ficheiros de imagem, PDF ou TIFF selecionados. |
| **A** | Transcrição de Áudio     | Transcreve ficheiros MP3, WAV ou OGG em texto.                               |
| **C** | Solucionador de CAPTCHA  | Captura e resolve CAPTCHAs (Suporta portais governamentais).                |
| **S** | Ditado Inteligente       | Converte fala em texto. Prima para iniciar a gravação e novamente para parar/digitar. |
| **Control+L** | **Assistente ao Vivo** | **Copiloto em Tempo Real (Apenas Gemini):** Inicia ou encerra uma conversa de voz e ecrã ao vivo com o assistente de IA. |
| **I** | Relatório de Status      | Anuncia o progresso atual (por exemplo, "A analisar...", "Inativo").        |
| **L** | **Rotular Objeto** | **Rotulagem Semântica por IA:** Rotula permanentemente o elemento/ícone focado atual. |
| **Shift + L** | **Gerir/Procurar Rótulos** | Abre o Gerenciador de Rótulos (se existirem rótulos) ou procura elementos sem nome na aplicação. |
| **U** | Verificar Atualização    | Verifica manualmente no GitHub a versão mais recente do suplemento.         |
| **Espaço** | Chamar Último Resultado  | Mostra a última resposta da IA numa caixa de diálogo para revisão ou acompanhamento. |
| **H** | Ajuda de Comandos        | Exibe uma lista com todos os atalhos disponíveis.                           |

### 2.1 Atalhos do Leitor de Documentos (Dentro do Visualizador)
- **Ctrl + PageDown:** Move para a página seguinte.
- **Ctrl + PageUp:** Move para a página anterior.
- **Alt + A:** Abre uma caixa de diálogo de chat para fazer perguntas sobre o documento.
- **Alt + R:** Força um **Reexame com IA** utilizando o seu provedor ativo.
- **Alt + G:** Gera e guarda um ficheiro de áudio de alta qualidade (WAV/MP3). *Oculto se o provedor não suportar TTS.*
- **Alt + S / Ctrl + S:** Guarda o texto extraído como um ficheiro TXT ou HTML.

## 3. Prompts Personalizados e Variáveis

Pode gerir os prompts em **Definições > Prompts > Gerir Prompts...**.

### Variáveis Suportadas
- `[selection]`: Texto atualmente selecionado.
- `[clipboard]`: Conteúdo da área de transferência.
- `[screen_obj]`: Captura de ecrã do objeto de navegação.
- `[screen_full]`: Captura de ecrã em ecrã inteiro.
- `[file_ocr]`: Seleciona um ficheiro de imagem/PDF para extração de texto.
- `[file_read]`: Seleciona um documento para leitura (TXT, Código, PDF).
- `[file_audio]`: Seleciona um ficheiro de áudio para análise (MP3, WAV, OGG).

***
**Nota:** É necessária uma ligação ativa à internet para todas as funcionalidades de IA. Documentos com múltiplas páginas são processados automaticamente.

## 4. Suporte e Comunidade

Mantenha-se atualizado com as últimas notícias, funcionalidades e lançamentos:
- **Canal do Telegram:** [t.me/VisionAssistantPro](https://t.me/VisionAssistantPro)
- **Problemas no GitHub (Issues):** Para relatórios de bugs e pedidos de novas funcionalidades.

## 5. Apoiantes do Projeto

Um agradecimento sincero aos membros da nossa comunidade que apoiam o desenvolvimento contínuo e a manutenção deste projeto através das suas generosas contribuições financeiras:

* **@Alyabani94**
* **Ali Alamri**
* **Ilya**
* **Apoiante Anónimo** (`UQDd...CnMY`)
* **leonardo0216**

*Se desejar apoiar o projeto financeiramente e ver o seu nome aqui, poderá encontrar a opção **Doar** no menu Ferramentas do NVDA (submenu Vision Assistant) ou durante o processo de configuração após a instalação.*

---
## Alterações para a versão 6.5.0

* **Assistente ao Vivo**: Adicionada a funcionalidade de assistente de voz e ecrã em tempo real, disponível exclusivamente para o provedor Google Gemini (ou provedores personalizados compatíveis com o Gemini). Inclui personalização de voz interativa e profundidade de raciocínio diretamente na caixa de diálogo, com reconexão automática ao alterar as definições.
* **Provedor de IA MiniMax**: Integrado o MiniMax como um provedor equivalente com suporte multimodal completo (chat, visão, OCR), TTS personalizado utilizando mais de 300+ vozes dinâmicas e remoção automática de blocos de raciocínio (ex: `<think>...</think>`) das respostas.
* **Tradução do Visualizador de Documentos**: Corrigida uma falha silenciosa de tradução para utilizadores do NVDA que não utilizam o idioma inglês, garantindo que o código de idioma padrão de 2 letras é enviado ao Google Tradutor em vez do nome do idioma localizado.
* **Tentativa de Análise em Lote de PDF**: Implementada uma lógica de nova tentativa silenciosa, separada e altamente otimizada para a análise em lote de documentos PDF, a fim de evitar uploads redundantes e popups de erro incómodos durante as tentativas.
* **Status do Visualizador de Documentos**: Corrigido um bug onde o status geral do plugin (verificado via `I`) ficava bloqueado em "Processamento em Lote Iniciado" durante a análise de documentos longos.
* **Falha de Threading Resolvida**: Corrigida uma falha grave de asserção de thread `IsMain() failed in wxTimerImpl` ao abrir documentos a partir de uma thread em segundo plano, transferindo a fila de retorno da GUI para `wx.CallAfter`.

## Alterações para a versão 6.1.2

* **Pré-Verificação de Rótulos Duplicados**: Corrigido um problema na rotulagem individual onde a verificação de duplicados utilizava chaves de coordenadas antigas, fazendo com que o NVDA fizesse pedidos de IA duplicados para objetos já rotulados em vez de anunciar o rótulo existente.
* **Chat de Documentos para Provedores Não-Gemini**: Corrigida uma verificação estrita de chave de API no Chat de Documentos (`on_ask`) para garantir que os utilizadores de provedores OpenAI, Groq ou Custom locais (como Ollama) possam conversar com documentos com sucesso, sem serem bloqueados.
* **Tradução de OCR Rápido do Chrome**: Restaurada a API de tradução gratuita e sem necessidade de chave para o OCR do Chrome. A tradução do texto extraído agora ignora a IA do Gemini, economizando cotas de API e acelerando o processo de tradução.
* **Filtro Alfanumérico de CAPTCHA**: Corrigida a lógica de filtragem no solucionador de CAPTCHA para garantir que os caracteres não alfanuméricos sejam devidamente limpos em todas as situações.
* **Atualização da Ajuda da Camada de Comando**: Corrigido o atalho de anúncio de status no menu de ajuda de `L` para `I`, e adicionados ambos os comandos de rotulagem (`L` e `Shift+L`) à lista.

## Alterações para a versão 6.1.1

* **Correção de Saída de Raciocínio do Gemma 4**: Corrigido um problema com os modelos Gemma 4 onde todo o processo de pensamento interno era exibido como a resposta final, ou onde desativar o raciocínio resultava em respostas vazias. O suplemento agora isola e extrai corretamente apenas a resposta de texto limpa final.
* **OCR em Lote a partir do Explorador de Ficheiros**: Agora pode selecionar várias fotos ou PDFs diretamente no Explorador de Ficheiros do Windows e extrair o texto ou analisá-los em lote. O suplemento filtrará e processará automaticamente apenas os formatos de ficheiro suportados.

## Alterações para a versão 6.1.0

* **Integração Universal de IA Local (Configurar IA Local)**: Adicionado um novo botão **"Configurar IA Local"** nas Definições do Provedor Personalizado. Os utilizadores agora podem configurar automaticamente motores de IA locais, incluindo **Ollama**, **LM Studio**, **Jan.ai** e **KoboldCPP** instantaneamente.
* **Desvio Inteligente de Proxy Local**: Reconstruída a lógica de conexão com um mecanismo avançado de desvio de proxy. O suplemento agora é inteligente o suficiente para ignorar completamente os proxies do sistema Windows em conexões de loopback local, garantindo ligações estáveis de IA local mesmo quando a sua VPN/modo TUN estiver ativa.
* **Rotulagem por IA Ultra-Estável (v2)**: Substituídas as chaves de coordenadas absolutas do ecrã por um sistema híbrido avançado de **Assinatura de Objeto**. Os rótulos agora dependem de identificadores programáticos (UIA **AutomationId** ou Win32 **ControlID**) e coordenadas relativas à janela, tornando os seus rótulos personalizados totalmente resistentes ao redimensionamento de janelas, movimentação, alternância de monitores ou alteração de escala.
* **Migração Automática de Rótulos Sem Interrupções**: A atualização é totalmente transparente. O suplemento migrará automaticamente os seus rótulos antigos baseados em coordenadas legadas para o novo formato de impressão digital estável em segundo plano no primeiro foco, com zero perda de dados.

## Alterações para a versão 6.0

* **Apresentando a Rotulagem Semântica por IA**: Os utilizadores agora podem rotular permanentemente botões e ícones sem nome usando IA. Pressione **L** para rotular o objeto de navegação atual (suportando tanto o foco por Tab quanto a navegação de objetos) ou **Shift+L** para analisar e rotular a aplicação inteira de uma vez.
* **Gestão Inteligente de Rótulos**: Adicionada uma nova caixa de diálogo do Gestor de Rótulos totalmente acessível (via **Shift+L** se existirem rótulos) para visualizar, renomear ou eliminar em lote os rótulos personalizados.
* **Análise Direta de Ficheiros (Ignorando a Caixa de Diálogo de Ficheiro)**: O suplemento agora é inteligente o suficiente para detectar se está focado num ficheiro PDF ou de imagem no Explorador de Ficheiros do Windows. Pressionar **F (Ação de Ficheiro Inteligente)** ou **D (Leitor de Documentos)** num ficheiro destacado irá processá-lo imediatamente, ignorando completamente a caixa de diálogo padrão "Abrir".

## Alterações para a versão 5.6

* **Adicionado Motor de OCR "Nenhum (Extrair Camada de Texto)"**: Os utilizadores agora podem extrair texto diretamente de PDFs pesquisáveis sem gastar créditos de IA, melhorando significativamente a velocidade e a privacidade para documentos baseados em texto.
* **Precisão Refinada do Explorador de UI**: Melhorado o prompt do Explorador de UI para identificar melhor os tipos de elementos (como Itens de Lista) e relatar com precisão estados como "(Marcado)", "(Selecionado)" ou "(Expandido)", ignorando componentes do sistema Windows como a Barra de Tarefas e o Relógio.
* **Lembrete de Configuração de Instalação**: Adicionada uma notificação após a instalação para guiar os utilizadores ao menu de definições para configurar as suas chaves de API e preferências.

## Alterações para a versão 5.5.2

* **Corrigido Problema de Digitação do Operador de IA:** Resolvido um bug onde a letra 'v' era digitada em vez de colar o texto em determinados sistemas. Esta correção aborda conflitos de tempo que ocorriam durante alta carga do sistema.
* **Estabilidade Aprimorada:** Adicionado tratamento de erros robusto para operações de área de transferência para evitar bloqueios do suplemento quando a área de transferência do sistema estiver temporariamente bloqueada por outras aplicações.
* **Otimização de Tempo:** Ajustados os atrasos internos para eventos de teclado para garantir maior fiabilidade em diferentes velocidades de sistema e melhor compatibilidade com gestores de área de transferência de terceiros.

## Alterações para a versão 5.5 (A Atualização de Automação)

* **Operador de IA (Controlo Autónomo - Shift+A):** Esta é a joia da coroa da v5.5. O Vision Assistant Pro deixou de ser um assistente passivo para se tornar o seu **Operador de IA** pessoal. Não se limita a descrever o ecrã — ele assume o comando.
    * *Como funciona:* Agora pode dar instruções verbais para operar o seu PC. Por exemplo, numa aplicação completamente inacessível onde o seu leitor de ecrã fica mudo, pode pressionar **Shift+A** e digitar: *"Clique no botão Definições"* ou *"Encontre o campo de pesquisa, digite 'Últimas Notícias' e pressione enter."* A IA identifica visualmente os elementos, move o rato e executa a tarefa por si.
    * *Nota de Desempenho:* Este recurso é otimizado para o **Gemini 3.0 Flash (Preview)**, entregando respostas incrivelmente rápidas e inteligentes que podem lidar até com os layouts de interface mais complexos.
    * **⚠️ Aviso de Utilização da API:** Como o Operador de IA precisa de "ver" exatamente o que está a acontecer para ser preciso, ele envia uma captura de ecrã em alta resolução a cada passo. Por favor, note que o uso frequente consumirá a sua cota de API muito mais rápido do que as tarefas padrão baseadas em texto.
* **Explorador Visual de UI (E):** Cansado de navegar por "botões sem nome"? Pressione **E** para ativar o Explorador de UI. A IA analisará a janela inteira e gerará uma lista de todos os elementos clicáveis que encontrar — incluindo ícones, gráficos e menus. Basta escolher um item da lista e o Operador de IA clicará nele por si. É como ter uma "camada acessível" sobre qualquer aplicação.
* **Ação de Ficheiro Inteligente Sensível ao Contexto (F):** A tecla "F" foi completamente reformulada. Já não assume que deseja apenas o OCR. Quando seleciona uma única imagem, ela agora pergunta inteligentemente a sua intenção: pode escolher uma **Descrição Visual Detalhada** para entender a cena ou uma **Extração de Texto Estruturada (OCR)** para leitura. O menu adapta-se dinamicamente com base no tipo de ficheiro e no seu motor de IA ativo.
* **Otimização do Núcleo:** Realizámos uma limpeza profunda na lógica interna do suplemento, removendo funções legadas não utilizadas e código redundante. Isto resulta numa experiência mais enxuta, rápida e fiável para todos os utilizadores.

## Alterações para a versão 5.0

* **Arquitetura Multi-Provedor**: Adicionado suporte completo para **OpenAI**, **Groq** e **Mistral** junto ao Google Gemini. Os utilizadores agora podem escolher o seu backend de IA preferido.
* **Roteamento Avançado de Modelos**: Utilizadores de provedores nativos (Gemini, OpenAI, etc.) agora podem selecionar modelos específicos de uma lista suspensa para diferentes tarefas (OCR, STT, TTS).
* **Configuração Avançada de Endpoint**: Utilizadores de provedores personalizados podem inserir manualmente URLs específicas e nomes de modelos para um controlo granular sobre servidores locais ou de terceiros.
* **Visibilidade Inteligente de Recursos**: O menu de definições e a interface do Leitor de Documentos agora ocultam automaticamente recursos não suportados (como TTS) com base no provedor selecionado.
* **Busca Dinâmica de Modelos**: O suplemento agora procura a lista de modelos disponíveis diretamente da API do provedor, garantindo compatibilidade com novos modelos assim que forem lançados.
* **OCR e Tradução Híbridos**: Otimizada a lógica para usar o Google Tradutor para maior velocidade ao usar o OCR do Chrome, e tradução alimentada por IA ao usar os motores Gemini/Groq/OpenAI.
* **"Re-escanear com IA" Universal**: O recurso de reexame do Leitor de Documentos já não está limitado ao Gemini. Ele agora utiliza qualquer provedor de IA que estiver ativo no momento para reprocessar as páginas.

## Alterações para a versão 4.6
* **Chamada Interativa de Resultados:** Adicionada a tecla **Espaço** à camada de comando, permitindo que os utilizadores reabram instantaneamente a última resposta da IA numa janela de chat para perguntas de acompanhamento, mesmo quando o modo "Saída Direta" estiver ativo.
* **Central da Comunidade no Telegram:** Adicionado um link para o "Canal Oficial do Telegram" no menu Ferramentas do NVDA, oferecendo uma maneira rápida de se manter atualizado com as últimas notícias, recursos e lançamentos.
* **Estabilidade de Resposta Aprimorada:** Otimizada a lógica central dos recursos de Tradução, OCR e Visão para garantir um desempenho mais confiável e uma experiência mais suave ao usar a saída de fala direta.
* **Orientação de Interface Melhorada:** Atualizadas as descrições de configurações e documentação para explicar melhor o novo sistema de chamada de resultados e como ele funciona em conjunto com as configurações de saída direta.

## Alterações para a versão 4.5
* **Gestor de Prompts Avançado:** Introduzida uma caixa de diálogo de gestão dedicada nas definições para personalizar os prompts padrão do sistema e gerir prompts definidos pelo utilizador com suporte completo para adicionar, editar, reordenar e pré-visualizar.
* **Suporte Abrangente a Proxy:** Resolvidos os problemas de conectividade de rede garantindo que as definições de proxy definidas pelo utilizador sejam aplicadas estritamente a todos os pedidos de API, incluindo tradução, OCR e geração de fala.
* **Migração Automatizada de Dados:** Integrado um sistema de migração inteligente para atualizar automaticamente as configurações de prompts legados para um formato JSON v2 robusto na primeira execução, sem perda de dados.
* **Compatibilidade Atualizada (2025.1):** Definida a versão mínima do NVDA necessária para 2025.1 devido a dependências de biblioteca em recursos avançados como o Leitor de Documentos, garantindo um desempenho estável.
* **Interface de Definições Otimizada:** Simplificada a interface de definições ao reorganizar a gestão de prompts numa caixa de diálogo separada, proporcionando uma experiência de utilizador mais limpa e acessível.
* **Guia de Variáveis de Prompt:** Adicionado um guia integrado dentro das caixas de diálogo de prompt para ajudar os utilizadores a identificar e usar facilmente variáveis dinâmicas como [selection], [clipboard] e [screen_obj].

## Alterações para a versão 4.0.3
* **Resiliência de Rede Aprimorada:** Adicionado um mecanismo de nova tentativa automática para lidar melhor com ligações instáveis de internet e erros temporários do servidor, garantindo respostas de IA mais confiáveis.
* **Caixa de Diálogo de Tradução Visual:** Introduzida uma janela dedicada para os resultados de tradução. Os utilizadores agora podem navegar facilmente e ler traduções longas linha por linha, de forma semelhante aos resultados de OCR.
* **Visualização Formatada Agregada:** O recurso "Visualizar Formatado" no Leitor de Documentos agora exibe todas as páginas processadas numa única janela organizada com cabeçalhos de página claros.
* **Fluxo de Trabalho de OCR Otimizado:** Ignora automaticamente a seleção de intervalo de páginas para documentos de página única, tornando o processo de reconhecimento mais rápido e fluido.
* **Estabilidade de API Melhorada:** Alterado para um método de autenticação baseado em cabeçalho mais robusto, resolvendo potenciais erros de "Todas as chaves de API falharam" causados por conflitos de rotação de chaves.
* **Correções de Bugs:** Resolvidos vários bloqueios potenciais, incluindo um problema durante o encerramento do suplemento e um erro de foco na caixa de diálogo de chat.

## Alterações para a versão 4.0.1
* **Leitor de Documentos Avançado:** um novo e poderoso visualizador para PDF e imagens com seleção de intervalo de páginas, processamento em segundo plano e navegação fluida com `Ctrl+PageUp/Down`.
* **Novo Submenu de Ferramentas:** Adicionado um submenu dedicado "Vision Assistant" sob o menu Ferramentas do NVDA para um acesso mais rápido aos recursos principais, configurações e documentação.
* **Personalização Flexível:** Agora pode escolher o seu mecanismo de OCR e voz de TTS preferidos diretamente no painel de definições.
* **Suporte a Múltiplas Chaves de API:** Adicionado suporte para várias chaves de API do Gemini. Pode inserir uma chave por linha ou separá-las com vírgulas nas definições.
* **Mecanismo de OCR Alternativo:** Introduzido um novo mecanismo de OCR para garantir o reconhecimento confiável de texto mesmo ao atingir os limites de cota da API do Gemini.
* **Rotação Inteligente de Chaves de API:** Alterna automaticamente e memoriza a chave de API em funcionamento mais rápida para contornar os limites de cota.
* **Documento para MP3/WAV:** Capacidade integrada de gerar e guardar ficheiros de áudio de alta qualidade nos formatos MP3 (128kbps) e WAV diretamente dentro do leitor.
* **Suporte a Stories do Instagram:** Adicionada a capacidade de descrever e analisar Stories do Instagram utilizando as suas URLs.
* **Suporte ao TikTok:** Introduzido o suporte para vídeos do TikTok, permitindo a descrição visual completa e a transcrição de áudio dos clipes.
* **Caixa de Diálogo de Atualização Redesenhada:** Apresenta uma nova interface acessível com uma caixa de texto rolável para ler claramente as alterações da versão antes de instalar.
* **Status Unificado e UX:** Padronizadas as caixas de diálogo de ficheiros em todo o suplemento e aprimorado o comando 'L' para relatar o progresso em tempo real.

## Alterações para a versão 3.6.0
* **Sistema de Ajuda:** Adicionado um comando de ajuda (`H`) dentro da Camada de Comando para fornecer uma lista de fácil acesso com todos os atalhos e as suas funções.
* **Análise de Vídeo Online:** Expandido o suporte para incluir vídeos do **Twitter (X)**. Também foi melhorada a detecção de URL e a estabilidade para uma experiência mais confiável.
* **Contribuição para o Projeto:** Adicionada uma caixa de diálogo de doação opcional para utilizadores que desejam apoiar as atualizações futuras e o crescimento contínuo do projeto.

## Alterações para a versão 3.5.0
* **Camada de Comando:** Introduzido um sistema de Camada de Comando (predefinição: `NVDA+Shift+V`) para agrupar atalhos sob uma única tecla mestre. Por exemplo, em vez de pressionar `NVDA+Control+Shift+T` para tradução, agora pressiona `NVDA+Shift+V` seguido por `T`.
* **Análise de Vídeo Online:** Adicionado um novo recurso para analisar vídeos do YouTube e do Instagram diretamente fornecendo uma URL.

## Alterações para a versão 3.1.0
* **Modo de Saída Direta:** Adicionada uma opção para ignorar a caixa de diálogo de chat e ouvir as respostas da IA diretamente via fala para uma experiência mais rápida e integrada.
* **Integração com a Área de Transferência:** Adicionada uma nova configuração para copiar automaticamente as respostas da IA para a área de transferência.

## Alterações para a versão 3.0

* **Novos Idiomas:** Adicionadas traduções para o **Persa** e **Vietnamita**.
* **Modelos de IA Expandidos:** Reorganizada a lista de seleção de modelos com prefixos claros (`[Free]`, `[Pro]`, `[Auto]`) para ajudar os utilizadores a distinguir entre modelos gratuitos e com limite de taxa (pagos). Adicionado suporte para o **Gemini 3.0 Pro** e **Gemini 2.0 Flash Lite**.
* **Estabilidade do Ditado:** Melhorada significativamente a estabilidade do Ditado Inteligente. Adicionada uma verificação de segurança para ignorar clipes de áudio com menos de 1 segundo, evitando alucinações da IA e erros de conteúdo vazio.
* **Manipulação de Ficheiros:** Corrigido um problema onde o envio de ficheiros com nomes que não estivessem em inglês falhava.
* **Otimização de Prompts:** Melhorada a lógica de Tradução e estruturação dos resultados de Visão.

## Alterações para a versão 2.9

* **Adicionadas traduções para o Francês e Turco.**
* **Visualização Formatada:** Adicionado um botão "Visualizar Formatado" nas caixas de diálogo de chat para exibir a conversa com a estilização adequada (Cabeçalhos, Negrito, Código) numa janela padrão navegável.
* **Configuração de Markdown:** Adicionada uma nova opção "Limpar Markdown no Chat" nas Definições. Desmarcar isto permite que os utilizadores vejam a sintaxe Markdown bruta (ex: `**`, `#`) na janela de chat.
* **Gestão de Caixas de Diálogo:** Corrigido um problema onde as janelas de "Refinar Texto" ou de chat abriam várias vezes ou falhavam em obter o foco corretamente.
* **Melhorias de UX:** Padronizados os títulos das caixas de diálogo de ficheiro para "Abrir" e removidos anúncios de fala redundantes (ex: "A abrir menu...") para uma experiência mais fluida.

## Alterações para a versão 2.8
* Adicionada tradução para o Italiano.
* **Relatório de Status:** Adicionado um novo comando (NVDA+Control+Shift+I) para anunciar o status atual do suplemento (ex: "A enviar...", "A analisar...").
* **Exportação em HTML:** O botão "Salvar Conteúdo" nas caixas de diálogo de resultado agora guarda a saída como um ficheiro HTML formatado, preservando estilos como cabeçalhos e texto em negrito.
* **Interface de Definições:** Melhorado o layout do painel de Definições com agrupamento acessível.
* **Novos Modelos:** Adicionado suporte para gemini-flash-latest e gemini-flash-lite-latest.
* **Idiomas:** Adicionado o Nepalês aos idiomas suportados.
* **Lógica do Menu Refinar:** Corrigido um bug crítico onde os comandos "Refinar Texto" falhavam se o idioma da interface do NVDA não fosse o inglês.
* **Ditado:** Melhorada a detecção de silêncio para evitar saídas de texto incorretas quando nenhuma fala é inserida.
* **Configurações de Atualização:** A opção "Verificar atualizações na inicialização" agora vem desativada por padrão para cumprir as políticas da Loja de Complementos (Add-on Store).
* Limpeza de código.

## Alterações para a versão 2.7
* Migrada a estrutura do projeto para o Modelo de Suplemento oficial da NV Access (Add-on Template) para melhor conformidade com as normas.
* Implementada uma lógica de nova tentativa automática para erros HTTP 429 (Limite de Taxa) para garantir a confiabilidade durante períodos de alto tráfego.
* Otimizados os prompts de tradução para maior precisão e melhor manuseio da lógica "Smart Swap".
* Atualizada a tradução para o Russo.

## Alterações para a versão 2.6
* Adicionado suporte de tradução para o Russo (Agradecimentos ao nvda-ru).
* Atualizadas as mensagens de erro para fornecer um feedback mais descritivo sobre a conectividade.
* Alterado o idioma de destino padrão para o Inglês.

## Alterações para a versão 2.5
* Adicionado Comando de OCR de Ficheiro Nativo (NVDA+Control+Shift+F).
* Adicionado o botão "Salvar Chat" às caixas de diálogo de resultado.
* Implementado suporte completo de localização (i18n).
* Migrado o feedback de áudio para o módulo de tons nativo do NVDA.
* Alterado para a API de Ficheiros do Gemini para um melhor manuseio de ficheiros PDF e de áudio.
* Corrigido bloqueio ao traduzir textos que continham chavetas `{ }`.

## Alterações para a versão 2.1.1
* Corrigido um problema onde a variável [file_ocr] não funcionava corretamente dentro dos Prompts Personalizados.

## Alterações para a versão 2.1
* Padronizados todos os atalhos para usar NVDA+Control+Shift para eliminar conflitos com o layout de Teclado Portátil do NVDA e teclas de atalho do sistema.

## Alterações para a versão 2.0
* Implementado sistema integrado de Atualização Automática.
* Adicionado Cache de Tradução Inteligente para recuperação instantânea de textos traduzidos anteriormente.
* Adicionada Memória de Conversação para refinar contextualmente os resultados nas caixas de diálogo de chat.
* Adicionado comando Dedicado de Tradução da Área de Trabalho (NVDA+Control+Shift+Y).
* Otimizados os prompts de IA para impor estritamente a saída no idioma de destino.
* Corrigido bloqueio causado por caracteres especiais no texto de entrada.

## Alterações para a versão 1.5
* Adicionado suporte para mais de 20 novos idiomas.
* Implementada Caixa de Diálogo de Refinamento Interativo para perguntas de acompanhamento.
* Adicionado recurso Nativo de Ditado Inteligente.
* Adicionada a categoria "Vision Assistant" à caixa de diálogo de Gestos de Entrada do NVDA.
* Corrigidos bloqueios por COMError em aplicações específicas como Firefox e Word.
* Adicionado mecanismo de nova tentativa automática para erros do servidor.

## Alterações para a versão 1.0
* Lançamento inicial.
