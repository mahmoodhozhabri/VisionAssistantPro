# Documentação do Vision Assistant Pro

O **Vision Assistant Pro** é um assistente de IA multimodal avançado para o NVDA. Utiliza motores de IA de classe mundial para fornecer leitura inteligente do ecrã, tradução, ditado por voz e análise de documentos.

_Este extra foi lançado para a comunidade em honra do Dia Internacional das Pessoas com Deficiência._

## 1. Configuração e Ajustes

Aceda a **Menu do NVDA > Preferências > Definições > Vision Assistant Pro**.

### 1.1 Definições de Ligação

- **Fornecedor:** Selecione o seu serviço de IA preferido. Os fornecedores suportados incluem **Google Gemini**, **OpenAI**, **Mistral**, **Groq** e **Custom** (servidores compatíveis com OpenAI, como Ollama, LM Studio, Jan.ai ou KoboldCPP).
- **Nota Importante:** Recomendamos fortemente a utilização do **Google Gemini** para melhor desempenho e precisão (especialmente para análise de imagens/ficheiros).
- **Chave API:** Obrigatória. Pode introduzir várias chaves (separadas por vírgulas ou novas linhas) para rotação automática.
- **Obter Modelos:** Após introduzir a sua chave API, prima este botão para descarregar a lista mais recente de modelos disponíveis do fornecedor.
- **Modelo de IA:** Selecione o modelo principal utilizado para conversação geral e análise.

### 1.2 Encaminhamento Avançado de Modelos

_Disponível para todos os fornecedores, incluindo Gemini, OpenAI, Groq, Mistral e Custom._

> **⚠️ Aviso:** Estas definições destinam-se apenas a **utilizadores avançados**. Se não tiver a certeza do que faz um modelo específico, deixe esta opção **desmarcada**. Selecionar um modelo incompatível para uma tarefa (por exemplo, um modelo apenas de texto para Visão) irá causar erros e impedir o funcionamento do extra.

Assinale **"Encaminhamento Avançado de Modelos (Específico por Tarefa)"** para desbloquear controlo detalhado. Isto permite-lhe selecionar modelos específicos da lista suspensa para diferentes tarefas:

- **Modelo OCR / Visão:** Escolha um modelo especializado para analisar imagens.
- **Speech-to-Text (STT):** Escolha um modelo específico para ditado.
- **Text-to-Speech (TTS):** Escolha um modelo para gerar áudio.
- **Modelo Operador de IA:** Selecione um modelo específico para tarefas autónomas de operação do computador.
  _Nota: Funcionalidades não suportadas (por exemplo, TTS para Groq) serão automaticamente ocultadas._

### 1.3 Configuração Avançada de Endpoint (Fornecedor Custom)

_Disponível apenas quando "Custom" estiver selecionado._

> **⚠️ Aviso:** Esta secção permite configuração manual da API e foi concebida para **utilizadores avançados** que executam servidores locais ou proxies. URLs ou nomes de modelos incorretos irão quebrar a conectividade. Se não souber exatamente o que são estes endpoints, deixe esta opção **desmarcada**.

Assinale **"Configuração Avançada de Endpoint"** para introduzir manualmente os detalhes do servidor. Ao contrário dos fornecedores nativos, aqui deve **escrever** os URLs específicos e os Nomes dos Modelos:

- **URL da Lista de Modelos:** O endpoint para obter modelos disponíveis.
- **URL do Endpoint OCR/STT/TTS:** URLs completos para serviços específicos (por exemplo, `http://localhost:11434/v1/audio/speech`).
- **Modelos Personalizados:** Introduza manualmente o nome do modelo (por exemplo, `llama3:8b`) para cada tarefa.

### 1.3.1 Configurar IA Local (Configuração numa Só Ação)

Para tornar a integração de IA local e completamente offline extremamente simples, está disponível um botão dedicado **"Configurar IA Local"** dentro das Definições do Fornecedor Custom.

Se estiver a executar um servidor local de modelos de IA no seu computador:

1. Selecione **Custom** como o seu Fornecedor.
2. Prima o botão **Configurar IA Local**.
3. Escolha o seu motor local de IA na caixa de diálogo acessível:
   - **Ollama** (por defeito em `http://127.0.0.1:11434`)
   - **LM Studio** (por defeito em `http://127.0.0.1:1234`)
   - **Jan.ai** (por defeito em `http://127.0.0.1:1337`)
   - **KoboldCPP** (por defeito em `http://127.0.0.1:5001`)
4. O extra irá configurar instantaneamente o URL local correto, o tipo de API e obter automaticamente os seus modelos offline ativos para preencher a caixa de seleção **Modelo de IA**.

_Nota sobre Rede e Proxies:_ Este motor de ligação local possui um mecanismo avançado de bypass de proxy. Mesmo que esteja a utilizar uma VPN ativa ou proxy em modo TUN, os seus pedidos locais de IA irão ignorá-los completamente, garantindo ligações offline estáveis sem erros 502 Bad Gateway.

### 1.4 Preferências Gerais

- **Motor OCR:** Escolha entre **Chrome (Rápido)** para resultados rápidos ou **IA (Avançado)** para preservação superior do esquema.
  - _Nota:_ Se selecionar "IA (Avançado)" mas o seu fornecedor estiver definido como OpenAI/Groq, o extra irá encaminhar inteligentemente a imagem para o modelo de visão do fornecedor ativo.
- **Voz TTS:** Selecione o seu estilo de voz preferido. Esta lista é atualizada dinamicamente com base no seu fornecedor ativo.
- **Criatividade (Temperatura):** Controla a aleatoriedade da IA. Valores mais baixos são melhores para tradução/OCR precisos.
- **URL do Proxy:** Configure esta opção caso os serviços de IA estejam restringidos na sua região (suporta proxies locais como `127.0.0.1` ou URLs bridge).

## 2. Camada de Comandos e Atalhos

Para evitar conflitos de teclado, este extra utiliza uma **Camada de Comandos**.

1. Prima **NVDA + Shift + V** (Tecla Mestre) para ativar a camada (irá ouvir um sinal sonoro).
2. Solte as teclas e prima uma das seguintes teclas individuais:

| Tecla         | Função                            | Descrição                                                                                                                             |
| ------------- | --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| **Shift + A** | **Operador de IA**                | **Operação Autónoma:** Diga à IA para executar uma tarefa no seu ecrã. Premir novamente interrompe instantaneamente operações ativas. |
| **E**         | **Explorador de UI**              | **Clique Interativo:** Identifica e clica em elementos da interface em qualquer aplicação.                                            |
| **T**         | Tradutor Inteligente              | Traduz o texto sob o cursor de navegação ou seleção.                                                                                  |
| **Shift + T** | Tradutor da Área de Transferência | Traduz o conteúdo atualmente na área de transferência.                                                                                |
| **R**         | Refinador de Texto                | Resume, Corrige Gramática, Explica ou executa **Prompts Personalizados**.                                                             |
| **V**         | Visão de Objeto                   | Descreve o objeto atual do navegador.                                                                                                 |
| **O**         | Visão de Ecrã Completo            | Analisa todo o esquema e conteúdo do ecrã.                                                                                            |
| **Shift + V** | Análise de Vídeo Online           | Analisa vídeos do **YouTube**, **Instagram**, **TikTok** ou **Twitter (X)**.                                                          |
| **D**         | Leitor de Documentos              | Leitor avançado para PDFs e imagens com seleção de intervalo de páginas.                                                              |
| **F**         | **Ação Inteligente de Ficheiro**  | Reconhecimento sensível ao contexto de imagens, PDFs ou ficheiros TIFF selecionados.                                                  |
| **A**         | Transcrição de Áudio              | Transcreve ficheiros MP3, WAV ou OGG em texto.                                                                                        |
| **C**         | Solucionador de CAPTCHA           | Captura e resolve CAPTCHAs (suporta portais governamentais).                                                                          |
| **S**         | Ditado Inteligente                | Converte fala em texto. Prima para iniciar a gravação e novamente para parar/escrever.                                                |
| **I**         | Relatório de Estado               | Anuncia o progresso atual (por exemplo, "A analisar...", "Inativo").                                                                  |
| **L**         | **Etiquetar Objeto**              | **Etiquetagem Semântica por IA:** Etiqueta permanentemente o elemento/ícone atualmente focado.                                        |
| **Shift + L** | **Gerir/Analisar Etiquetas**      | Abre o Gestor de Etiquetas (se existirem etiquetas) ou analisa a aplicação em busca de elementos sem nome.                            |
| **U**         | Verificar Atualizações            | Verifica manualmente no GitHub a versão mais recente do extra.                                                                        |
| **Espaço**    | Recuperar Último Resultado        | Mostra a última resposta da IA numa caixa de diálogo de conversação para revisão ou continuação.                                      |
| **H**         | Ajuda de Comandos                 | Mostra uma lista de todos os atalhos disponíveis.                                                                                     |

### 2.1 Atalhos do Leitor de Documentos (Dentro do Visualizador)

- **Ctrl + PageDown:** Mover para a página seguinte.
- **Ctrl + PageUp:** Mover para a página anterior.
- **Alt + A:** Abrir uma caixa de diálogo de conversação para fazer perguntas sobre o documento.
- **Alt + R:** Forçar uma **Nova Análise com IA** utilizando o fornecedor ativo.
- **Alt + G:** Gerar e guardar um ficheiro de áudio de alta qualidade (WAV/MP3). _Oculto se o fornecedor não suportar TTS._
- **Alt + S / Ctrl + S:** Guardar o texto extraído como ficheiro TXT ou HTML.

## 3. Prompts Personalizados e Variáveis

Pode gerir prompts em **Definições > Prompts > Gerir Prompts...**.

### Variáveis Suportadas

- `[selection]`: Texto atualmente selecionado.
- `[clipboard]`: Conteúdo da área de transferência.
- `[screen_obj]`: Captura de ecrã do objeto do navegador.
- `[screen_full]`: Captura de ecrã completa.
- `[file_ocr]`: Selecionar ficheiro de imagem/PDF para extração de texto.
- `[file_read]`: Selecionar documento para leitura (TXT, Código, PDF).
- `[file_audio]`: Selecionar ficheiro de áudio para análise (MP3, WAV, OGG).

---

**Nota:** É necessária uma ligação ativa à internet para todas as funcionalidades de IA. Documentos com múltiplas páginas são processados automaticamente.

## 4. Suporte e Comunidade

Mantenha-se atualizado com as últimas notícias, funcionalidades e lançamentos:

- **Canal Telegram:** [t.me/VisionAssistantPro](https://t.me/VisionAssistantPro)
- **Issues do GitHub:** Para relatórios de erros e pedidos de funcionalidades.

## 5. Apoiantes do Projeto

Um sincero agradecimento aos membros da nossa comunidade que apoiam o desenvolvimento contínuo e a manutenção deste projeto através das suas generosas contribuições financeiras:

- **@Alyabani94**
- **Ali Alamri**
- **Ilya**

_Se desejar apoiar financeiramente o projeto e ver o seu nome aqui, pode encontrar a opção **Donate** no menu Ferramentas do NVDA (submenu Vision Assistant) ou durante o processo de configuração após a instalação._

---

## Alterações da versão 6.1.0

- **Integração Universal de IA Local (Configurar IA Local):** Adicionado um novo botão **"Configurar IA Local"** nas Definições do Fornecedor Custom. Os utilizadores podem agora configurar automaticamente motores locais de IA, incluindo **Ollama**, **LM Studio**, **Jan.ai** e **KoboldCPP**, instantaneamente.
- **Bypass Inteligente de Proxy Local:** Reconstruída a lógica de ligação com um mecanismo avançado de bypass de proxy. O extra é agora suficientemente inteligente para ignorar completamente os proxies do sistema Windows em ligações locais loopback, garantindo ligações estáveis à IA local mesmo quando a VPN/TUN-mode está ativa.
- **Etiquetagem de IA Ultraestável (v2):** Substituídas as chaves absolutas de coordenadas do ecrã por um avançado sistema híbrido de **Assinatura de Objeto**. As etiquetas dependem agora de identificadores programáticos (UIA **AutomationId** ou Win32 **ControlID**) e coordenadas relativas à janela, tornando as suas etiquetas personalizadas completamente resistentes ao redimensionamento de janelas, movimentação, troca de monitor ou escala.
- **Migração Automática e Transparente de Etiquetas:** A atualização é completamente transparente. O extra irá migrar automaticamente as suas antigas etiquetas baseadas em coordenadas para o novo formato estável em segundo plano no primeiro foco, sem qualquer perda de dados.

## Alterações da versão 6.0

- **Introdução da Etiquetagem Semântica por IA:** Os utilizadores podem agora etiquetar permanentemente botões e ícones sem nome utilizando IA. Prima **L** para etiquetar o objeto atual do navegador (suportando tanto foco por Tab como navegação por objetos) ou **Shift+L** para analisar e etiquetar toda a aplicação de uma só vez.
- **Gestão Inteligente de Etiquetas:** Adicionada uma nova caixa de diálogo totalmente acessível de Gestão de Etiquetas (através de **Shift+L** se existirem etiquetas) para visualizar, renomear ou eliminar etiquetas personalizadas em lote.
- **Análise Direta de Ficheiros (Ignorar Caixa de Diálogo Abrir):** O extra é agora suficientemente inteligente para detetar se está atualmente focado num ficheiro PDF ou imagem no Explorador de Ficheiros do Windows. Premir **F (Ação Inteligente de Ficheiro)** ou **D (Leitor de Documentos)** num ficheiro selecionado irá processá-lo imediatamente, ignorando completamente a caixa de diálogo padrão "Abrir".

## Alterações da versão 5.6

- **Adicionado Motor OCR "Nenhum (Extrair Camada de Texto)":** Os utilizadores podem agora extrair texto diretamente de PDFs pesquisáveis sem utilizar créditos de IA, melhorando significativamente a velocidade e privacidade para documentos baseados em texto.
- **Precisão Refinada do Explorador de UI:** Melhorado o prompt do Explorador de UI para identificar melhor tipos de elementos (como Itens de Lista) e reportar corretamente estados como "(Marcado)", "(Selecionado)" ou "(Expandido)", ignorando componentes do sistema Windows como a Barra de Tarefas e o Relógio.
- **Lembrete de Configuração Pós-Instalação:** Adicionada uma notificação após a instalação para orientar os utilizadores até ao menu de definições para configurarem as suas chaves API e preferências.

## Alterações da versão 5.5.2

- **Corrigido Problema de Escrita do Operador de IA:** Resolvido um erro onde a letra 'v' era escrita em vez de colar texto em determinados sistemas. Esta correção resolve conflitos de temporização que ocorriam durante elevada carga do sistema.
- **Estabilidade Melhorada:** Adicionado tratamento robusto de erros para operações da área de transferência, evitando falhas do extra quando a área de transferência do sistema está temporariamente bloqueada por outras aplicações.
- **Otimização de Temporização:** Ajustados atrasos internos para eventos de teclado de forma a garantir maior fiabilidade em diferentes velocidades de sistema e melhor compatibilidade com gestores de área de transferência de terceiros.

## Alterações da versão 5.5 (A Atualização de Automação)

- **Operador de IA (Controlo Autónomo - Shift+A):** Esta é a joia da coroa da v5.5. O Vision Assistant Pro evoluiu de um assistente passivo para se tornar o seu **Operador de IA** pessoal. Não se limita a descrever o ecrã — assume o controlo.
  - _Como funciona:_ Pode agora dar instruções verbais para operar o seu PC. Por exemplo, numa aplicação completamente inacessível onde o seu leitor de ecrã permanece silencioso, pode premir **Shift+A** e escrever: _"Clique no botão Definições"_ ou _"Encontre o campo de pesquisa, escreva 'Últimas Notícias' e prima Enter."_ A IA identifica visualmente os elementos, move o rato e executa a tarefa por si.
  - _Nota de Desempenho:_ Esta funcionalidade está otimizada para **Gemini 3.0 Flash (Preview)**, oferecendo respostas incrivelmente rápidas e inteligentes capazes de lidar até com os esquemas de UI mais complexos.
  - **⚠️ Aviso sobre Utilização da API:** Como o Operador de IA precisa de "ver" exatamente o que está a acontecer para ser preciso, envia uma captura de ecrã em alta resolução a cada passo. Tenha em atenção que a utilização frequente irá consumir a sua quota API muito mais rapidamente do que tarefas padrão baseadas em texto.
- **Explorador Visual de UI (E):** Cansado de navegar por "botões sem etiqueta"? Prima **E** para ativar o Explorador de UI. A IA irá analisar toda a janela e gerar uma lista de todos os elementos clicáveis que encontrar — incluindo ícones, gráficos e menus. Basta escolher um item da lista e o Operador de IA clicará nele por si. É como ter uma "camada acessível" sobre qualquer aplicação.
- **Ação Inteligente de Ficheiro Sensível ao Contexto (F):** A tecla "F" foi completamente reformulada. Já não assume que apenas pretende OCR. Ao selecionar uma única imagem, pergunta agora inteligentemente qual é a sua intenção: pode escolher uma **Descrição Visual Detalhada** para compreender a cena ou uma **Extração Estruturada de Texto (OCR)** para leitura. O menu adapta-se dinamicamente com base no tipo de ficheiro e no motor de IA ativo.
- **Otimização do Núcleo:** Foi realizada uma limpeza profunda da lógica interna do extra, removendo funções antigas não utilizadas e código redundante. Isto resulta numa experiência mais leve, rápida e fiável para todos os utilizadores.

## Alterações da versão 5.0

- **Arquitetura Multi-Fornecedor:** Adicionado suporte completo para **OpenAI**, **Groq** e **Mistral** juntamente com o Google Gemini. Os utilizadores podem agora escolher o seu backend de IA preferido.
- **Encaminhamento Avançado de Modelos:** Os utilizadores de fornecedores nativos (Gemini, OpenAI, etc.) podem agora selecionar modelos específicos a partir de listas suspensas para diferentes tarefas (OCR, STT, TTS).
- **Configuração Avançada de Endpoint:** Os utilizadores do fornecedor Custom podem introduzir manualmente URLs específicos e nomes de modelos para controlo granular sobre servidores locais ou de terceiros.
- **Visibilidade Inteligente de Funcionalidades:** O menu de definições e a UI do Leitor de Documentos ocultam agora automaticamente funcionalidades não suportadas (como TTS) com base no fornecedor selecionado.
- **Obtenção Dinâmica de Modelos:** O extra obtém agora a lista de modelos disponíveis diretamente da API do fornecedor, garantindo compatibilidade com novos modelos assim que são lançados.
- **OCR e Tradução Híbridos:** Otimizada a lógica para utilizar Google Translate pela rapidez ao usar OCR do Chrome, e tradução baseada em IA ao utilizar motores Gemini/Groq/OpenAI.
- **"Nova Análise com IA" Universal:** A funcionalidade de nova análise do Leitor de Documentos deixou de estar limitada ao Gemini. Agora utiliza qualquer fornecedor de IA atualmente ativo para reprocessar páginas.

## Alterações da versão 4.6

- **Recuperação Interativa de Resultados:** Adicionada a tecla **Espaço** à camada de comandos, permitindo aos utilizadores reabrir instantaneamente a última resposta da IA numa janela de conversação para perguntas de seguimento, mesmo quando o modo "Saída Direta" está ativo.
- **Centro da Comunidade no Telegram:** Adicionado um link para o "Canal Oficial do Telegram" no menu Ferramentas do NVDA, fornecendo uma forma rápida de acompanhar as últimas notícias, funcionalidades e lançamentos.
- **Estabilidade Melhorada das Respostas:** Otimizada a lógica central das funcionalidades de Tradução, OCR e Visão para garantir desempenho mais fiável e uma experiência mais fluida ao utilizar saída direta por voz.
- **Orientação Melhorada da Interface:** Atualizadas as descrições das definições e a documentação para explicar melhor o novo sistema de recuperação e como funciona juntamente com as definições de saída direta.

## Alterações da versão 4.5

- **Gestor Avançado de Prompts:** Introduzida uma caixa de diálogo dedicada nas definições para personalizar prompts padrão do sistema e gerir prompts definidos pelo utilizador com suporte completo para adicionar, editar, reorganizar e pré-visualizar.
- **Suporte Abrangente a Proxy:** Resolvidos problemas de conectividade de rede garantindo que as definições de proxy configuradas pelo utilizador são rigorosamente aplicadas a todos os pedidos API, incluindo tradução, OCR e geração de voz.
- **Migração Automática de Dados:** Integrado um sistema inteligente de migração para atualizar automaticamente configurações antigas de prompts para um robusto formato JSON v2 na primeira execução, sem perda de dados.
- **Compatibilidade Atualizada (2025.1):** Definida a versão mínima requerida do NVDA como 2025.1 devido às dependências de bibliotecas em funcionalidades avançadas como o Leitor de Documentos, garantindo desempenho estável.
- **Interface de Definições Otimizada:** Simplificada a interface de definições reorganizando a gestão de prompts numa caixa de diálogo separada, proporcionando uma experiência mais limpa e acessível.
- **Guia de Variáveis de Prompt:** Adicionado um guia integrado nas caixas de diálogo de prompts para ajudar os utilizadores a identificar e utilizar facilmente variáveis dinâmicas como [selection], [clipboard] e [screen_obj].

## Alterações da versão 4.0.3

- **Maior Resiliência de Rede:** Adicionado um mecanismo automático de repetição para lidar melhor com ligações à internet instáveis e erros temporários do servidor, garantindo respostas de IA mais fiáveis.
- **Caixa de Diálogo de Tradução Visual:** Introduzida uma janela dedicada para resultados de tradução. Os utilizadores podem agora navegar e ler traduções longas linha a linha, de forma semelhante aos resultados OCR.
- **Visualização Formatada Agregada:** A funcionalidade "Ver Formatado" no Leitor de Documentos apresenta agora todas as páginas processadas numa única janela organizada com cabeçalhos claros de página.
- **Fluxo OCR Otimizado:** Ignora automaticamente a seleção do intervalo de páginas para documentos de página única, tornando o processo de reconhecimento mais rápido e fluido.
- **Estabilidade API Melhorada:** Alterado para um método de autenticação mais robusto baseado em cabeçalhos, resolvendo possíveis erros "Todas as Chaves API falharam" causados por conflitos de rotação de chaves.
- **Correções de Erros:** Resolvidas várias falhas potenciais, incluindo um problema durante o encerramento do extra e um erro de foco na caixa de diálogo de conversação.

## Alterações da versão 4.0.1

- **Leitor Avançado de Documentos:** Um poderoso novo visualizador para PDFs e imagens com seleção de intervalo de páginas, processamento em segundo plano e navegação fluida com `Ctrl+PageUp/Down`.
- **Novo Submenu Ferramentas:** Adicionado um submenu dedicado "Vision Assistant" no menu Ferramentas do NVDA para acesso mais rápido às funcionalidades principais, definições e documentação.
- **Personalização Flexível:** Pode agora escolher o seu motor OCR e voz TTS preferidos diretamente no painel de definições.
- **Suporte para Múltiplas Chaves API:** Adicionado suporte para múltiplas chaves Gemini API. Pode introduzir uma chave por linha ou separá-las por vírgulas nas definições.
- **Motor OCR Alternativo:** Introduzido um novo motor OCR para garantir reconhecimento de texto fiável mesmo ao atingir limites de quota da API Gemini.
- **Rotação Inteligente de Chaves API:** Alterna automaticamente e memoriza a chave API funcional mais rápida para contornar limites de quota.
- **Documento para MP3/WAV:** Integrada capacidade de gerar e guardar ficheiros de áudio de alta qualidade nos formatos MP3 (128kbps) e WAV diretamente dentro do leitor.
- **Suporte para Stories do Instagram:** Adicionada a capacidade de descrever e analisar Stories do Instagram utilizando os seus URLs.
- **Suporte TikTok:** Introduzido suporte para vídeos TikTok, permitindo descrição visual completa e transcrição áudio dos clipes.
- **Caixa de Diálogo de Atualização Redesenhada:** Inclui uma nova interface acessível com caixa de texto deslocável para leitura clara das alterações de versão antes da instalação.
- **Estado e UX Unificados:** Normalizadas as caixas de diálogo de ficheiros em todo o extra e melhorado o comando 'L' para reportar progresso em tempo real.

## Alterações da versão 3.6.0

- **Sistema de Ajuda:** Adicionado um comando de ajuda (`H`) dentro da Camada de Comandos para fornecer uma lista de fácil acesso com todos os atalhos e respetivas funções.
- **Análise de Vídeo Online:** Expandido o suporte para incluir vídeos do **Twitter (X)**. Também melhorada a deteção de URLs e estabilidade para uma experiência mais fiável.
- **Contribuição para o Projeto:** Adicionada uma caixa de diálogo opcional de donativo para utilizadores que desejem apoiar futuras atualizações e o crescimento contínuo do projeto.

## Alterações da versão 3.5.0

\* \*\*Camada de Comandos:\*\* Introduzido um sistema de Camada de Comandos (por defeito: `NVDA+Shift+V`) para agrupar atalhos sob uma única tecla mestre. Por exemplo, em vez de premir `NVDA+Control+Shift+T` para tradução, passa agora a premir `NVDA+Shift+V` seguido de `T`. \* \*\*Análise de Vídeo Online:\*\* Adicionada uma nova funcionalidade para analisar vídeos do YouTube e Instagram diretamente através de um URL.

## Alterações da versão 3.1.0

- **Modo de Saída Direta:** Adicionada uma opção para ignorar a caixa de diálogo de conversação e ouvir respostas da IA diretamente através de voz para uma experiência mais rápida e fluida.
- **Integração com a Área de Transferência:** Adicionada uma nova definição para copiar automaticamente respostas da IA para a área de transferência.

## Alterações da versão 3.0

- **Novos Idiomas:** Adicionadas traduções em **Persa** e **Vietnamita**.
- **Modelos de IA Expandidos:** Reorganizada a lista de seleção de modelos com prefixos claros (`[Free]`, `[Pro]`, `[Auto]`) para ajudar os utilizadores a distinguir entre modelos gratuitos e limitados por taxa (pagos). Adicionado suporte para **Gemini 3.0 Pro** e **Gemini 2.0 Flash Lite**.
- **Estabilidade do Ditado:** Melhorada significativamente a estabilidade do Ditado Inteligente. Adicionada uma verificação de segurança para ignorar clipes áudio inferiores a 1 segundo, prevenindo alucinações da IA e erros vazios.
- **Gestão de Ficheiros:** Corrigido um problema em que o envio de ficheiros com nomes não ingleses falhava.
- **Otimização de Prompts:** Melhorada a lógica de Tradução e estruturados os resultados de Visão.

## Alterações da versão 2.9

- **Adicionadas traduções em francês e turco.**
- **Visualização Formatada:** Adicionado um botão "Ver Formatado" nas caixas de diálogo de conversação para visualizar a conversa com estilo adequado (Cabeçalhos, Negrito, Código) numa janela navegável padrão.
- **Definição Markdown:** Adicionada uma nova opção "Limpar Markdown no Chat" nas Definições. Ao desmarcar esta opção, os utilizadores poderão ver sintaxe Markdown em bruto (por exemplo, `**`, `#`) na janela de conversação.
- **Gestão de Caixas de Diálogo:** Corrigido um problema em que as janelas "Refinar Texto" ou conversação abriam múltiplas vezes ou não recebiam corretamente o foco.
- **Melhorias de UX:** Normalizados os títulos das caixas de diálogo de ficheiros para "Abrir" e removidos anúncios redundantes por voz (por exemplo, "A abrir menu...") para uma experiência mais fluida.

## Alterações da versão 2.8

- Adicionada tradução italiana.
- **Relatório de Estado:** Adicionado um novo comando (NVDA+Control+Shift+I) para anunciar o estado atual do extra (por exemplo, "A carregar...", "A analisar...").
- **Exportação HTML:** O botão "Guardar Conteúdo" nas caixas de diálogo de resultados guarda agora a saída como ficheiro HTML formatado, preservando estilos como cabeçalhos e texto a negrito.
- **UI de Definições:** Melhorado o esquema do painel de Definições com agrupamento acessível.
- **Novos Modelos:** Adicionado suporte para gemini-flash-latest e gemini-flash-lite-latest.
- **Idiomas:** Adicionado Nepalês aos idiomas suportados.
- **Lógica do Menu Refinar:** Corrigido um erro crítico onde os comandos "Refinar Texto" falhavam se o idioma da interface do NVDA não fosse inglês.
- **Ditado:** Melhorada a deteção de silêncio para evitar saída incorreta de texto quando não existe fala.
- **Definições de Atualização:** "Verificar atualizações ao iniciar" encontra-se agora desativado por defeito para cumprir as políticas da Loja de Extras.
- Limpeza de código.

## Alterações da versão 2.7

- Migrada a estrutura do projeto para o modelo oficial de extras NV Access para melhor conformidade com normas.
- Implementada lógica automática de repetição para erros HTTP 429 (Limite de Taxa) para garantir fiabilidade durante tráfego elevado.
- Otimizados prompts de tradução para maior precisão e melhor tratamento da lógica "Smart Swap".
- Atualizada a tradução russa.

## Alterações da versão 2.6

- Adicionado suporte para tradução russa (Obrigado ao nvda-ru).
- Atualizadas mensagens de erro para fornecer feedback mais descritivo relativamente à conectividade.
- Alterado o idioma de destino por defeito para inglês.

## Alterações da versão 2.5

- Adicionado comando OCR Nativo de Ficheiros (NVDA+Control+Shift+F).
- Adicionado botão "Guardar Conversação" nas caixas de diálogo de resultados.
- Implementado suporte completo de localização (i18n).
- Migrado feedback áudio para o módulo nativo de tons do NVDA.
- Alterado para Gemini File API para melhor tratamento de ficheiros PDF e áudio.
- Corrigida falha ao traduzir texto contendo chavetas.

## Alterações da versão 2.1.1

- Corrigido um problema em que a variável [file_ocr] não funcionava corretamente dentro de Prompts Personalizados.

## Alterações da versão 2.1

- Normalizados todos os atalhos para utilizar NVDA+Control+Shift para eliminar conflitos com o esquema Laptop do NVDA e atalhos do sistema.

## Alterações da versão 2.0

- Implementado sistema integrado de Atualização Automática.
- Adicionada Cache Inteligente de Tradução para recuperação instantânea de textos previamente traduzidos.
- Adicionada Memória de Conversação para refinar resultados contextualmente nas caixas de diálogo de conversação.
- Adicionado comando dedicado de Tradução da Área de Transferência (NVDA+Control+Shift+Y).
- Otimizados prompts de IA para reforçar estritamente a saída no idioma de destino.
- Corrigida falha causada por caracteres especiais no texto introduzido.

## Alterações da versão 1.5

- Adicionado suporte para mais de 20 novos idiomas.
- Implementada Caixa de Diálogo Interativa de Refinamento para perguntas de seguimento.
- Adicionada funcionalidade nativa de Ditado Inteligente.
- Adicionada categoria "Vision Assistant" à caixa de diálogo Gestos de Entrada do NVDA.
- Corrigidas falhas COMError em aplicações específicas como Firefox e Word.
- Adicionado mecanismo automático de repetição para erros de servidor.

## Alterações da versão 1.0

- Lançamento inicial.
