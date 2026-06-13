# Documentação do Vision Assistant Pro

O **Vision Assistant Pro** é um assistente de IA multimodal avançado para NVDA. Ele utiliza mecanismos de IA de classe mundial para fornecer leitura inteligente de tela, tradução, ditado por voz e análise de documentos.

_Este complemento foi lançado para a comunidade em homenagem ao Dia Internacional das Pessoas com Deficiência._

## 1. Configuração e Ajustes

Vá para **Menu do NVDA > Preferências > Configurações > Vision Assistant Pro**.

### 1.1 Configurações de Conexão

- **Provedor:** Selecione seu serviço de IA preferido. Os provedores suportados incluem **Google Gemini**, **OpenAI**, **Mistral**, **Groq** e **Custom** (servidores compatíveis com OpenAI, como Ollama, LM Studio, Jan.ai ou KoboldCPP).
- **Nota Importante:** Recomendamos fortemente o uso do **Google Gemini** para melhor desempenho e precisão (especialmente para análise de imagens/arquivos).
- **Chave da API:** Obrigatória. Você pode inserir várias chaves (separadas por vírgulas ou novas linhas) para rotação automática.
- **Buscar Modelos:** Após inserir sua chave da API, pressione este botão para baixar a lista mais recente de modelos disponíveis do provedor.
- **Modelo de IA:** Selecione o modelo principal usado para bate-papo geral e análises.

### 1.2 Roteamento Avançado de Modelos

\*Disponível para todos os provedores, incluindo Gemini, OpenAI, Groq, Mistral e Custom.\_

> **⚠️ Aviso:** Estas configurações destinam-se apenas a **usuários avançados**. Se você não tiver certeza sobre o que um modelo específico faz, deixe esta opção **desmarcada**. Selecionar um modelo incompatível para uma tarefa (por exemplo, um modelo somente de texto para Visão) causará erros e fará o complemento parar de funcionar.

Marque **"Roteamento Avançado de Modelos (Específico por Tarefa)"** para desbloquear controle detalhado. Isso permite selecionar modelos específicos da lista suspensa para diferentes tarefas:

- **Modelo OCR / Visão:** Escolha um modelo especializado para analisar imagens.
- **Speech-to-Text (STT):** Escolha um modelo específico para ditado.
- **Text-to-Speech (TTS):** Escolha um modelo para gerar áudio.
- **Modelo Operador de IA:** Selecione um modelo específico para tarefas autônomas de operação do computador.
  _Nota: Recursos não suportados (por exemplo, TTS para Groq) serão ocultados automaticamente._

### 1.3 Configuração Avançada de Endpoint (Provedor Custom)

\*Disponível apenas quando "Custom" estiver selecionado.\_

> **⚠️ Aviso:** Esta seção permite configuração manual da API e foi projetada para **usuários avançados** que executam servidores locais ou proxies. URLs ou nomes de modelos incorretos quebrarão a conectividade. Se você não souber exatamente o que são esses endpoints, deixe esta opção **desmarcada**.

Marque **"Configuração Avançada de Endpoint"** para inserir manualmente os detalhes do servidor. Diferentemente dos provedores nativos, aqui você deve **digitar** as URLs específicas e os Nomes dos Modelos:

- **URL da Lista de Modelos:** O endpoint para buscar modelos disponíveis.
- **URL do Endpoint OCR/STT/TTS:** URLs completas para serviços específicos (por exemplo, `http://localhost:11434/v1/audio/speech`).
- **Modelos Personalizados:** Digite manualmente o nome do modelo (por exemplo, `llama3:8b`) para cada tarefa.

### 1.3.1 Configurar IA Local (Configuração em Uma Ação)

Para tornar a integração de IA local e completamente offline extremamente simples, um botão dedicado **"Configurar IA Local"** está disponível dentro das Configurações do Provedor Custom.

Se você estiver executando um servidor local de modelos de IA no seu computador:

1. Selecione **Custom** como seu Provedor.
2. Pressione o botão **Configurar IA Local**.
3. Escolha seu mecanismo local de IA na caixa de diálogo acessível:
   - **Ollama** (padrão para `http://127.0.0.1:11434`)
   - **LM Studio** (padrão para `http://127.0.0.1:1234`)
   - **Jan.ai** (padrão para `http://127.0.0.1:1337`)
   - **KoboldCPP** (padrão para `http://127.0.0.1:5001`)
4. O complemento configurará instantaneamente a URL local correta, o tipo de API e buscará automaticamente seus modelos offline ativos para preencher a caixa de seleção **Modelo de IA**.

_Nota sobre Rede e Proxies:_ Este mecanismo de conexão local possui um sistema avançado de bypass de proxy. Mesmo que você esteja usando uma VPN ativa ou proxy em modo TUN, suas requisições locais de IA irão ignorá-los completamente, garantindo conexões offline estáveis sem erros 502 Bad Gateway.

### 1.4 Preferências Gerais

- **Motor OCR:** Escolha entre **Chrome (Rápido)** para resultados rápidos ou **IA (Avançado)** para preservação superior de layout.
  - _Nota:_ Se você selecionar "IA (Avançado)" mas seu provedor estiver configurado como OpenAI/Groq, o complemento encaminhará inteligentemente a imagem para o modelo de visão do provedor ativo.
- **Voz TTS:** Selecione seu estilo de voz preferido. Esta lista é atualizada dinamicamente com base no seu provedor ativo.
- **Criatividade (Temperatura):** Controla a aleatoriedade da IA. Valores menores são melhores para tradução/OCR precisos.
- **URL do Proxy:** Configure isso caso os serviços de IA sejam restritos na sua região (suporta proxies locais como `127.0.0.1` ou URLs bridge).

## 2. Camada de Comandos e Atalhos

Para evitar conflitos de teclado, este complemento usa uma **Camada de Comandos**.

1. Pressione **NVDA + Shift + V** (Tecla Mestra) para ativar a camada (você ouvirá um bipe).
2. Solte as teclas e pressione uma das seguintes teclas únicas:

| Tecla         | Função                            | Descrição                                                                                                                             |
| ------------- | --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| **Shift + A** | **Operador de IA**                | **Operação Autônoma:** Diga à IA para executar uma tarefa na sua tela. Pressionar novamente aborta instantaneamente operações ativas. |
| **E**         | **Explorador de UI**              | **Clique Interativo:** Identifica e clica em elementos da interface em qualquer aplicativo.                                           |
| **T**         | Tradutor Inteligente              | Traduz o texto sob o cursor do navegador ou seleção.                                                                                  |
| **Shift + T** | Tradutor da Área de Transferência | Traduz o conteúdo atualmente na área de transferência.                                                                                |
| **R**         | Refinador de Texto                | Resume, Corrige Gramática, Explica ou executa **Prompts Personalizados**.                                                             |
| **V**         | Visão de Objeto                   | Descreve o objeto atual do navegador.                                                                                                 |
| **O**         | Visão de Tela Completa            | Analisa todo o layout e conteúdo da tela.                                                                                             |
| **Shift + V** | Análise de Vídeo Online           | Analisa vídeos do **YouTube**, **Instagram**, **TikTok** ou **Twitter (X)**.                                                          |
| **D**         | Leitor de Documentos              | Leitor avançado para PDFs e imagens com seleção de intervalo de páginas.                                                              |
| **F**         | **Ação Inteligente de Arquivo**   | Reconhecimento sensível ao contexto de imagens, PDFs ou arquivos TIFF selecionados.                                                   |
| **A**         | Transcrição de Áudio              | Transcreve arquivos MP3, WAV ou OGG em texto.                                                                                         |
| **C**         | Solucionador de CAPTCHA           | Captura e resolve CAPTCHAs (suporta portais governamentais).                                                                          |
| **S**         | Ditado Inteligente                | Converte fala em texto. Pressione para iniciar a gravação e novamente para parar/digitar.                                             |
| **I**         | Relatório de Status               | Anuncia o progresso atual (por exemplo, "Escaneando...", "Ocioso").                                                                   |
| **L**         | **Rotular Objeto**                | **Rotulagem Semântica por IA:** Rotula permanentemente o elemento/ícone atualmente focado.                                            |
| **Shift + L** | **Gerenciar/Escanear Rótulos**    | Abre o Gerenciador de Rótulos (se existirem rótulos) ou escaneia o aplicativo em busca de elementos sem nome.                         |
| **U**         | Verificar Atualizações            | Verifica manualmente no GitHub a versão mais recente do complemento.                                                                  |
| **Espaço**    | Recuperar Último Resultado        | Mostra a última resposta da IA em uma caixa de diálogo de chat para revisão ou continuação.                                           |
| **H**         | Ajuda de Comandos                 | Exibe uma lista de todos os atalhos disponíveis.                                                                                      |

### 2.1 Atalhos do Leitor de Documentos (Dentro do Visualizador)

- **Ctrl + PageDown:** Ir para a próxima página.
- **Ctrl + PageUp:** Ir para a página anterior.
- **Alt + A:** Abrir uma caixa de diálogo de chat para fazer perguntas sobre o documento.
- **Alt + R:** Forçar um **Novo Escaneamento com IA** usando seu provedor ativo.
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

**Nota:** Uma conexão ativa com a internet é necessária para todos os recursos de IA. Documentos com múltiplas páginas são processados automaticamente.

## 4. Suporte e Comunidade

Mantenha-se atualizado com as últimas notícias, recursos e lançamentos:

- **Canal do Telegram:** [t.me/VisionAssistantPro](https://t.me/VisionAssistantPro)
- **Issues do GitHub:** Para relatórios de bugs e solicitações de recursos.

## 5. Apoiadores do Projeto

Um sincero agradecimento aos membros da nossa comunidade que apoiam o desenvolvimento contínuo e a manutenção deste projeto por meio de suas generosas contribuições financeiras:

- **@Alyabani94**
- **Ali Alamri**
- **Ilya**

_Se você deseja apoiar financeiramente o projeto e ver seu nome aqui, pode encontrar a opção **Doar** no menu Ferramentas do NVDA (submenu Vision Assistant) ou durante o processo de configuração após a instalação._

---

## Mudanças da versão 6.1.0

- **Integração Universal de IA Local (Configurar IA Local):** Adicionado um novo botão **"Configurar IA Local"** nas Configurações do Provedor Custom. Os usuários agora podem configurar automaticamente mecanismos locais de IA, incluindo **Ollama**, **LM Studio**, **Jan.ai** e **KoboldCPP** instantaneamente.
- **Bypass Inteligente de Proxy Local:** Reconstruída a lógica de conexão com um mecanismo avançado de bypass de proxy. O complemento agora é inteligente o suficiente para ignorar completamente os proxies do sistema Windows em conexões locais loopback, garantindo conexões estáveis com IA local mesmo quando VPN/TUN-mode estiver ativo.
- **Rotulagem de IA Ultraestável (v2):** Substituídas as chaves absolutas de coordenadas de tela por um avançado sistema híbrido de **Assinatura de Objeto**. Os rótulos agora dependem de identificadores programáticos (UIA **AutomationId** ou Win32 **ControlID**) e coordenadas relativas à janela, tornando seus rótulos personalizados completamente resistentes a redimensionamento de janelas, movimentação, troca de monitor ou escalonamento.
- **Migração Automática e Transparente de Rótulos:** A atualização é completamente transparente. O complemento migrará automaticamente seus antigos rótulos baseados em coordenadas para o novo formato estável em segundo plano ao primeiro foco, sem perda de dados.

## Mudanças da versão 6.0

- **Introdução à Rotulagem Semântica por IA:** Agora os usuários podem rotular permanentemente botões e ícones sem nome usando IA. Pressione **L** para rotular o objeto atual do navegador (suportando foco por Tab e navegação por objetos) ou **Shift+L** para escanear e rotular todo o aplicativo de uma só vez.
- **Gerenciamento Inteligente de Rótulos:** Adicionado um novo Gerenciador de Rótulos totalmente acessível (via **Shift+L** se existirem rótulos) para visualizar, renomear ou excluir rótulos personalizados em lote.
- **Análise Direta de Arquivos (Ignorar Caixa de Diálogo de Arquivo):** O complemento agora é inteligente o suficiente para detectar se você está focando atualmente em um arquivo PDF ou imagem no Explorador de Arquivos do Windows. Pressionar **F (Ação Inteligente de Arquivo)** ou **D (Leitor de Documentos)** em um arquivo destacado irá processá-lo imediatamente, ignorando totalmente a caixa de diálogo padrão "Abrir".

## Mudanças da versão 5.6

- **Adicionado Motor OCR "Nenhum (Extrair Camada de Texto)":** Os usuários agora podem extrair texto diretamente de PDFs pesquisáveis sem usar créditos de IA, melhorando significativamente a velocidade e privacidade para documentos baseados em texto.
- **Precisão Refinada do Explorador de UI:** Melhorado o prompt do Explorador de UI para identificar melhor tipos de elementos (como Itens de Lista) e relatar corretamente estados como "(Marcado)", "(Selecionado)" ou "(Expandido)", ignorando componentes do sistema Windows como Barra de Tarefas e Relógio.
- **Lembrete de Configuração Pós-Instalação:** Adicionada uma notificação após a instalação para orientar os usuários ao menu de configurações para configurar suas chaves de API e preferências.

## Mudanças da versão 5.5.2

- **Corrigido Problema de Digitação do Operador de IA:** Resolvido um bug onde a letra 'v' era digitada em vez de colar texto em determinados sistemas. Esta correção resolve conflitos de tempo que ocorriam durante alta carga do sistema.
- **Estabilidade Aprimorada:** Adicionado tratamento robusto de erros para operações da área de transferência, evitando travamentos do complemento quando a área de transferência do sistema estiver temporariamente bloqueada por outros aplicativos.
- **Otimização de Temporização:** Ajustados atrasos internos para eventos de teclado a fim de garantir maior confiabilidade em diferentes velocidades de sistema e melhor compatibilidade com Gerenciadores de Área de Transferência de terceiros.

## Mudanças da versão 5.5 (A Atualização de Automação)

- **Operador de IA (Controle Autônomo - Shift+A):** Esta é a joia da coroa da v5.5. O Vision Assistant Pro evoluiu de um assistente passivo para se tornar seu **Operador de IA** pessoal. Ele não apenas descreve a tela — ele assume o comando.
  - _Como funciona:_ Agora você pode dar instruções verbais para operar seu PC. Por exemplo, em um aplicativo completamente inacessível onde seu leitor de tela permanece silencioso, você pode pressionar **Shift+A** e digitar: _"Clique no botão Configurações"_ ou _"Encontre o campo de busca, digite 'Últimas Notícias' e pressione enter."_ A IA identifica visualmente os elementos, move o mouse e executa a tarefa para você.
  - _Nota de Desempenho:_ Este recurso é otimizado para **Gemini 3.0 Flash (Preview)**, fornecendo respostas incrivelmente rápidas e inteligentes capazes de lidar até mesmo com layouts de UI mais complexos.
  - **⚠️ Aviso sobre Uso da API:** Como o Operador de IA precisa "ver" exatamente o que está acontecendo para ser preciso, ele envia uma captura de tela em alta resolução a cada etapa. Observe que o uso frequente consumirá sua cota de API muito mais rapidamente do que tarefas padrão baseadas em texto.
- **Explorador Visual de UI (E):** Cansado de navegar por "botões sem rótulo"? Pressione **E** para ativar o Explorador de UI. A IA escaneará toda a janela e gerará uma lista de todos os elementos clicáveis que encontrar — incluindo ícones, gráficos e menus. Basta escolher um item da lista, e o Operador de IA clicará nele para você. É como ter uma "camada acessível" sobre qualquer aplicativo.
- **Ação Inteligente de Arquivo Sensível ao Contexto (F):** A tecla "F" foi completamente reformulada. Ela não assume mais que você deseja apenas OCR. Ao selecionar uma única imagem, agora ela pergunta inteligentemente sua intenção: você pode escolher uma **Descrição Visual Detalhada** para entender a cena ou uma **Extração Estruturada de Texto (OCR)** para leitura. O menu adapta-se dinamicamente com base no tipo de arquivo e no mecanismo de IA ativo.
- **Otimização do Núcleo:** Foi realizada uma limpeza profunda da lógica interna do complemento, removendo funções legadas não utilizadas e código redundante. Isso resulta em uma experiência mais leve, rápida e confiável para todos os usuários.

## Mudanças da versão 5.0

- **Arquitetura Multi-Provedor:** Adicionado suporte completo para **OpenAI**, **Groq** e **Mistral** juntamente com o Google Gemini. Agora os usuários podem escolher seu backend de IA preferido.
- **Roteamento Avançado de Modelos:** Usuários de provedores nativos (Gemini, OpenAI etc.) agora podem selecionar modelos específicos em listas suspensas para diferentes tarefas (OCR, STT, TTS).
- **Configuração Avançada de Endpoint:** Usuários do provedor Custom podem inserir manualmente URLs específicas e nomes de modelos para controle granular sobre servidores locais ou de terceiros.
- **Visibilidade Inteligente de Recursos:** O menu de configurações e a UI do Leitor de Documentos agora ocultam automaticamente recursos não suportados (como TTS) com base no provedor selecionado.
- **Busca Dinâmica de Modelos:** O complemento agora busca a lista de modelos disponíveis diretamente da API do provedor, garantindo compatibilidade com novos modelos assim que forem lançados.
- **OCR e Tradução Híbridos:** Otimizada a lógica para usar Google Translate por velocidade ao usar OCR do Chrome, e tradução baseada em IA ao usar mecanismos Gemini/Groq/OpenAI.
- **"Novo Escaneamento com IA" Universal:** O recurso de reescaneamento do Leitor de Documentos não está mais limitado ao Gemini. Agora utiliza qualquer provedor de IA atualmente ativo para reprocessar páginas.

## Mudanças da versão 4.6

- **Recuperação Interativa de Resultados:** Adicionada a tecla **Espaço** à camada de comandos, permitindo aos usuários reabrir instantaneamente a última resposta da IA em uma janela de chat para perguntas de acompanhamento, mesmo quando o modo "Saída Direta" estiver ativo.

-* **Hub da Comunidade no Telegram:** Adicionado um link para o "Canal Oficial do Telegram" no menu Ferramentas do NVDA, oferecendo uma forma rápida de acompanhar as últimas notícias, recursos e lançamentos.

- **Orientação Melhorada da Interface:** Atualizadas as descrições de configurações e a documentação para explicar melhor o novo sistema de recuperação e como ele funciona junto às configurações de saída direta.

## Mudanças da versão 4.5

- **Gerenciador Avançado de Prompts:** Introduzida uma caixa de diálogo dedicada nas configurações para personalizar prompts padrão do sistema e gerenciar prompts definidos pelo usuário com suporte completo para adicionar, editar, reorganizar e visualizar.

- **Suporte Abrangente a Proxy:** Resolvidos problemas de conectividade de rede garantindo que as configurações de proxy definidas pelo usuário sejam aplicadas rigorosamente a todas as requisições de API, incluindo tradução, OCR e geração de fala.
- **Migração Automática de Dados:** Integrado um sistema inteligente de migração para atualizar automaticamente configurações legadas de prompts para um robusto formato JSON v2 na primeira execução, sem perda de dados.
- **Compatibilidade Atualizada (2025.1):** Definida a versão mínima exigida do NVDA como 2025.1 devido às dependências de bibliotecas em recursos avançados como o Leitor de Documentos, garantindo desempenho estável.
- **Interface de Configurações Otimizada:** Simplificada a interface de configurações reorganizando o gerenciamento de prompts em uma caixa de diálogo separada, proporcionando uma experiência mais limpa e acessível.
- **Guia de Variáveis de Prompt:** Adicionado um guia integrado nas caixas de diálogo de prompts para ajudar os usuários a identificar e usar facilmente variáveis dinâmicas como [selection], [clipboard] e [screen_obj].

## Mudanças da versão 4.0.3

- **Resiliência de Rede Aprimorada:** Adicionado um mecanismo automático de repetição para lidar melhor com conexões de internet instáveis e erros temporários do servidor, garantindo respostas de IA mais confiáveis.

- **Caixa de Diálogo de Tradução Visual:** Introduzida uma janela dedicada para resultados de tradução. Agora os usuários podem navegar e ler traduções longas linha por linha, semelhante aos resultados de OCR.
- **Visualização Formatada Agregada:** O recurso "Visualizar Formatado" no Leitor de Documentos agora exibe todas as páginas processadas em uma única janela organizada com cabeçalhos claros de página.
- **Fluxo OCR Otimizado:** Ignora automaticamente a seleção de intervalo de páginas para documentos de página única, tornando o processo de reconhecimento mais rápido e fluido.
- **Estabilidade Aprimorada da API:** Alterado para um método de autenticação mais robusto baseado em cabeçalhos, resolvendo possíveis erros "Todas as Chaves de API falharam" causados por conflitos de rotação de chaves.
- **Correções de Bugs:** Resolvidos vários possíveis travamentos, incluindo um problema durante o encerramento do complemento e um erro de foco na caixa de diálogo de chat.

## Mudanças da versão 4.0.1

- **Leitor Avançado de Documentos:** Um novo e poderoso visualizador para PDFs e imagens com seleção de intervalo de páginas, processamento em segundo plano e navegação fluida com `Ctrl+PageUp/Down`.

- **Novo Submenu Ferramentas:** Adicionado um submenu dedicado "Vision Assistant" no menu Ferramentas do NVDA para acesso mais rápido aos principais recursos, configurações e documentação.
- **Personalização Flexível:** Agora você pode escolher seu motor OCR e voz TTS preferidos diretamente no painel de configurações.
- **Suporte a Múltiplas Chaves de API:** Adicionado suporte a múltiplas chaves Gemini API. Você pode inserir uma chave por linha ou separá-las por vírgulas nas configurações.
- **Motor OCR Alternativo:** Introduzido um novo motor OCR para garantir reconhecimento de texto confiável mesmo ao atingir limites de cota da API Gemini.
- **Rotação Inteligente de Chaves API:** Alterna automaticamente e memoriza a chave API funcional mais rápida para contornar limites de cota.
- **Documento para MP3/WAV:** Integrada capacidade de gerar e salvar arquivos de áudio de alta qualidade nos formatos MP3 (128kbps) e WAV diretamente dentro do leitor.
- **Suporte a Stories do Instagram:** Adicionada a capacidade de descrever e analisar Stories do Instagram usando suas URLs.
- **Suporte ao TikTok:** Introduzido suporte para vídeos do TikTok, permitindo descrição visual completa e transcrição de áudio dos clipes.
- **Caixa de Diálogo de Atualização Redesenhada:** Possui uma nova interface acessível com caixa de texto rolável para leitura clara das mudanças de versão antes da instalação.
- **Status e UX Unificados:** Padronizados diálogos de arquivo em todo o complemento e aprimorado o comando 'L' para relatar progresso em tempo real.

## Mudanças da versão 3.6.0

- **Sistema de Ajuda:** Adicionado um comando de ajuda (`H`) dentro da Camada de Comandos para fornecer uma lista de fácil acesso com todos os atalhos e suas funções.

- **Análise de Vídeo Online:** Expandido o suporte para incluir vídeos do **Twitter (X)**. Também melhorada a detecção de URLs e estabilidade para uma experiência mais confiável.
- **Contribuição para o Projeto:** Adicionada uma caixa de diálogo opcional de doação para usuários que desejam apoiar futuras atualizações e crescimento contínuo do projeto.

## Mudanças da versão 3.5.0

\* \*\*Camada de Comandos:\*\* Introduzido um sistema de Camada de Comandos (padrão: `NVDA+Shift+V`) para agrupar atalhos sob uma única tecla mestra. Por exemplo, em vez de pressionar `NVDA+Control+Shift+T` para tradução, agora você pressiona `NVDA+Shift+V` seguido de `T`. \* \*\*Análise de Vídeo Online:\*\* Adicionado um novo recurso para analisar vídeos do YouTube e Instagram diretamente fornecendo uma URL.

## Mudanças da versão 3.1.0

- **Modo de Saída Direta:** Adicionada uma opção para ignorar a caixa de diálogo de chat e ouvir respostas da IA diretamente via fala, proporcionando uma experiência mais rápida e fluida.

- **Integração com Área de Transferência:** Adicionada uma nova configuração para copiar automaticamente respostas da IA para a área de transferência.

## Mudanças da versão 3.0

- **Novos Idiomas:** Adicionadas traduções em **Persa** e **Vietnamita**.
- **Modelos de IA Expandidos:** Reorganizada a lista de seleção de modelos com prefixos claros (`[Free]`, `[Pro]`, `[Auto]`) para ajudar usuários a distinguir entre modelos gratuitos e limitados por taxa (pagos). Adicionado suporte para **Gemini 3.0 Pro** e **Gemini 2.0 Flash Lite**.
- **Estabilidade do Ditado:** Melhorada significativamente a estabilidade do Ditado Inteligente. Adicionada uma verificação de segurança para ignorar clipes de áudio menores que 1 segundo, prevenindo alucinações da IA e erros vazios.
- **Manipulação de Arquivos:** Corrigido um problema onde uploads de arquivos com nomes não ingleses falhavam.
- **Otimização de Prompts:** Melhorada a lógica de Tradução e estruturados os resultados de Visão.

## Mudanças da versão 2.9

- **Adicionadas traduções em francês e turco.**
- **Visualização Formatada:** Adicionado um botão "Visualizar Formatado" nas caixas de diálogo de chat para visualizar a conversa com estilo adequado (Cabeçalhos, Negrito, Código) em uma janela padrão navegável.
- **Configuração Markdown:** Adicionada uma nova opção "Limpar Markdown no Chat" nas Configurações. Desmarcando esta opção, os usuários poderão ver a sintaxe Markdown bruta (por exemplo, `**`, `#`) na janela de chat.
- **Gerenciamento de Diálogos:** Corrigido um problema onde as janelas "Refinar Texto" ou chat abriam múltiplas vezes ou falhavam ao receber foco corretamente.
- **Melhorias de UX:** Padronizados os títulos das caixas de diálogo de arquivo para "Abrir" e removidos anúncios de fala redundantes (por exemplo, "Abrindo menu...") para uma experiência mais fluida.

## Mudanças da versão 2.8

- Adicionada tradução em italiano.

- **Relatório de Status:** Adicionado um novo comando (NVDA+Control+Shift+I) para anunciar o status atual do complemento (por exemplo, "Enviando...", "Analisando...").
- **Exportação HTML:** O botão "Salvar Conteúdo" nas caixas de diálogo de resultado agora salva a saída como arquivo HTML formatado, preservando estilos como cabeçalhos e texto em negrito.
- **UI de Configurações:** Melhorado o layout do painel de Configurações com agrupamento acessível.
- **Novos Modelos:** Adicionado suporte para gemini-flash-latest e gemini-flash-lite-latest.
- **Idiomas:** Adicionado Nepali aos idiomas suportados.
- **Lógica do Menu Refinar:** Corrigido um bug crítico onde os comandos "Refinar Texto" falhavam se o idioma da interface do NVDA não fosse inglês.
- **Ditado:** Melhorada a detecção de silêncio para evitar saída incorreta de texto quando não houver fala.
- **Configurações de Atualização:** "Verificar atualizações na inicialização" agora está desativado por padrão para cumprir políticas da Loja de Complementos.
- Limpeza de código.

## Mudanças da versão 2.7

- Migrada a estrutura do projeto para o modelo oficial de complementos NV Access para melhor conformidade com padrões.

- Implementada lógica automática de repetição para erros HTTP 429 (Limite de Taxa) para garantir confiabilidade durante alto tráfego.
- Otimizados prompts de tradução para maior precisão e melhor manipulação da lógica "Smart Swap".
- Atualizada tradução russa.

## Mudanças da versão 2.6

- Adicionado suporte para tradução em russo (Obrigado ao nvda-ru).

- Atualizadas mensagens de erro para fornecer feedback mais descritivo sobre conectividade.
- Alterado o idioma de destino padrão para inglês.

## Mudanças da versão 2.5

- Adicionado comando OCR de Arquivo Nativo (NVDA+Control+Shift+F).

- Adicionado botão "Salvar Chat" nas caixas de diálogo de resultado.
- Implementado suporte completo à localização (i18n).
- Migrado feedback de áudio para o módulo nativo de tons do NVDA.
- Alterado para Gemini File API para melhor manipulação de arquivos PDF e áudio.
- Corrigido travamento ao traduzir texto contendo chaves.

## Mudanças da versão 2.1.1

- Corrigido um problema onde a variável [file_ocr] não funcionava corretamente dentro de Prompts Personalizados.

## Mudanças da versão 2.1

- Padronizados todos os atalhos para usar NVDA+Control+Shift para eliminar conflitos com o layout Laptop do NVDA e atalhos do sistema.

## Mudanças da versão 2.0

- Implementado sistema integrado de Atualização Automática.

- Adicionado Cache Inteligente de Tradução para recuperação instantânea de textos traduzidos anteriormente.
- Adicionada Memória de Conversa para refinar resultados contextualmente em caixas de diálogo de chat.
- Adicionado comando dedicado de Tradução da Área de Transferência (NVDA+Control+Shift+Y).
- Otimizados prompts de IA para reforçar estritamente a saída no idioma de destino.
- Corrigido travamento causado por caracteres especiais no texto de entrada.

## Mudanças da versão 1.5

- Adicionado suporte para mais de 20 novos idiomas.

- Implementado Diálogo Interativo de Refinamento para perguntas de acompanhamento.
- Adicionado recurso nativo de Ditado Inteligente.
- Adicionada categoria "Vision Assistant" à caixa de diálogo Gestos de Entrada do NVDA.
- Corrigidos travamentos COMError em aplicativos específicos como Firefox e Word.
- Adicionado mecanismo automático de repetição para erros de servidor.

## Mudanças da versão 1.0

- Lançamento inicial.
