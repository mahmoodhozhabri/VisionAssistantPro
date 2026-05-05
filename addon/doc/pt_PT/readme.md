# Documentação do Vision Assistant Pro

O **Vision Assistant Pro** é um assistente de IA multimodal avançado para o NVDA. Utiliza motores de IA de classe mundial para fornecer leitura de ecrã inteligente, tradução, ditado por voz e análise de documentos.

_Este suplemento foi lançado para a comunidade em honra do Dia Internacional das Pessoas com Deficiência._

## 1. Configuração

Aceda ao **Menu NVDA > Preferências > Definições > Vision Assistant Pro**.

### 1.1 Definições de Ligação

- **Fornecedor:** Selecione o seu serviço de IA preferido. Os fornecedores suportados incluem **Google Gemini**, **OpenAI**, **Mistral**, **Groq** e **Personalizado** (servidores compatíveis com OpenAI, como Ollama/LM Studio).
- **Nota Importante:** Recomendamos vivamente o uso do **Google Gemini** para obter o melhor desempenho e precisão (especialmente para análise de imagens/ficheiros).
- **Chave de API (API Key):** Obrigatória. Pode introduzir várias chaves (separadas por vírgulas ou novas linhas) para rotação automática.
- **Procurar Modelos (Fetch Models):** Após introduzir a sua chave de API, prima este botão para descarregar a lista mais recente de modelos disponíveis do fornecedor.
- **Modelo de IA:** Selecione o modelo principal utilizado para chat geral e análise.

### 1.2 Encaminhamento Avançado de Modelos

_Disponível para todos os fornecedores, incluindo Gemini, OpenAI, Groq, Mistral e Personalizado._

> **⚠️ Aviso:** Estas definições destinam-se apenas a **utilizadores avançados**. Se não tiver a certeza do que um modelo específico faz, deixe esta opção **desmarcada**. Selecionar um modelo incompatível para uma tarefa (ex: um modelo apenas de texto para Visão) causará erros e interromperá o funcionamento do suplemento.

Marque **"Encaminhamento Avançado de Modelos (Específico por tarefa)"** para desbloquear o controlo detalhado. Isto permite selecionar modelos específicos da lista pendente para diferentes tarefas:

- **Modelo de OCR / Visão:** Escolha um modelo especializado para analisar imagens.
- **Fala para Texto (STT):** Escolha um modelo específico para ditado.
- **Texto para Fala (TTS):** Escolha um modelo para gerar áudio.
- **Modelo de Operador de IA:** Selecione um modelo específico para tarefas de operação autónoma do computador.
  _Nota: Funcionalidades não suportadas (ex: TTS para Groq) serão ocultadas automaticamente._

### 1.3 Configuração Avançada de Endpoint (Fornecedor Personalizado)

_Disponível apenas quando "Personalizado" está selecionado._

> **⚠️ Aviso:** Esta secção permite a configuração manual da API e foi concebida para **utilizadores experientes** que executam servidores locais ou proxies. URLs ou nomes de modelos incorretos interromperão a conectividade. Se não sabe exatamente o que são estes endpoints, mantenha esta opção **desmarcada**.

Marque **"Configuração Avançada de Endpoint"** para introduzir manualmente os detalhes do servidor. Ao contrário dos fornecedores nativos, aqui deve **escrever** os URLs e nomes de modelos específicos:

- **URL da Lista de Modelos:** O endpoint para obter os modelos disponíveis.
- **URL de Endpoint OCR/STT/TTS:** URLs completas para serviços específicos (ex: `http://localhost:11434/v1/audio/speech`).
- **Modelos Personalizados:** Escreva manualmente o nome do modelo (ex: `llama3:8b`) para cada tarefa.

### 1.4 Preferências Gerais

- **Motor de OCR:** Escolha entre **Chrome (Rápido)** para resultados velozes ou **IA (Avançado)** para uma preservação superior do esquema (layout).
  - _Nota:_ Se selecionar "IA (Avançado)", mas o seu fornecedor estiver configurado como OpenAI/Groq, o suplemento encaminhará inteligentemente a imagem para o modelo de visão do seu fornecedor ativo.
- **Voz TTS:** Selecione o seu estilo de voz preferido. Esta lista é atualizada dinamicamente com base no seu fornecedor ativo.
- **Criatividade (Temperatura):** Controla a aleatoriedade da IA. Valores mais baixos são melhores para tradução/OCR precisos.
- **URL de Proxy:** Configure isto se os serviços de IA forem restritos na sua região (suporta proxies locais como `127.0.0.1` ou URLs de ponte).

## 2. Camada de Comando e Atalhos

Para evitar conflitos de teclado, este suplemento utiliza uma **Camada de Comando**.

1. Prima **NVDA + Shift + V** (Tecla Mestra) para ativar a camada (ouvirá um sinal sonoro).
2. Solte as teclas e prima uma das seguintes teclas individuais:

| Tecla         | Função                            | Descrição                                                                               |
| :------------ | :-------------------------------- | :-------------------------------------------------------------------------------------- |
| **Shift + A** | **Operador de IA**                | **Operação Autónoma:** Diga à IA para realizar uma tarefa no seu ecrã.                  |
| **E**         | **Explorador de UI**              | **Clique Interativo:** Identifica e clica em elementos de interface em qualquer app.    |
| **T**         | Tradutor Inteligente              | Traduz o texto sob o cursor de navegação ou seleção.                                    |
| **Shift + T** | Tradutor de Área de Transferência | Traduz o conteúdo que está atualmente na área de transferência.                         |
| **R**         | Refinador de Texto                | Resumir, Corrigir Gramática, Explicar ou executar **Prompts Personalizados**.           |
| **V**         | Visão de Objeto                   | Descreve o objeto de navegação atual.                                                   |
| **O**         | Visão de Ecrã Inteiro             | Analisa o esquema e o conteúdo de todo o ecrã.                                          |
| **Shift + V** | Análise de Vídeo Online           | Analisa vídeos do **YouTube**, **Instagram**, **TikTok** ou **Twitter (X)**.            |
| **D**         | Leitor de Documentos              | Leitor avançado para PDF e imagens com seleção de intervalo de páginas.                 |
| **F**         | **Ação de Ficheiro Inteligente**  | Reconhecimento contextual de ficheiros de imagem, PDF ou TIFF selecionados.             |
| **A**         | Transcrição de Áudio              | Transcreve ficheiros MP3, WAV ou OGG para texto.                                        |
| **C**         | Solucionador de CAPTCHA           | Captura e resolve CAPTCHAs (Suporta portais governamentais).                            |
| **S**         | Ditado Inteligente                | Converte fala em texto. Prima para iniciar a gravação, e novamente para parar/escrever. |
| **L**         | Relatório de Estado               | Anuncia o progresso atual (ex: "A analisar...", "Inativo").                             |
| **U**         | Verificar Atualização             | Verifica manualmente no GitHub a versão mais recente do suplemento.                     |
| **Espaço**    | Relembrar Último Resultado        | Mostra a última resposta da IA num diálogo de chat para revisão ou acompanhamento.      |
| **H**         | Ajuda de Comandos                 | Exibe uma lista de todos os atalhos disponíveis.                                        |

### 2.1 Atalhos do Leitor de Documentos (Dentro do Visualizador)

- **Ctrl + PageDown:** Ir para a página seguinte.
- **Ctrl + PageUp:** Ir para a página anterior.
- **Alt + A:** Abre um diálogo de chat para fazer perguntas sobre o documento.
- **Alt + R:** Força um **Re-exame com IA** utilizando o seu fornecedor ativo.
- **Alt + G:** Gera e guarda um ficheiro de áudio de alta qualidade (WAV/MP3). _Oculto se o fornecedor não suportar TTS._
- **Alt + S / Ctrl + S:** Guarda o texto extraído como um ficheiro TXT ou HTML.

## 3. Prompts Personalizados e Variáveis

Pode gerir os prompts em **Definições > Prompts > Gerenciar Prompts...**.

### Variáveis Suportadas

- `[selection]`: Texto selecionado no momento.
- `[clipboard]`: Conteúdo da área de transferência.
- `[screen_obj]`: Captura de ecrã do objeto de navegação.
- `[screen_full]`: Captura de ecrã inteiro.
- `[file_ocr]`: Selecionar ficheiro de imagem/PDF para extração de texto.
- `[file_read]`: Selecionar documento para leitura (TXT, Código, PDF).
- `[file_audio]`: Selecionar ficheiro de áudio para análise (MP3, WAV, OGG).

---

**Nota:** É necessária uma ligação ativa à internet para todas as funcionalidades de IA. Documentos de várias páginas são processados automaticamente.

## 4. Suporte e Comunidade

Mantenha-se atualizado com as últimas notícias, funcionalidades e lançamentos:

- **Canal no Telegram:** [t.me/VisionAssistantPro](https://t.me/VisionAssistantPro)
- **Issues no GitHub:** Para relatórios de erros e pedidos de novas funcionalidades.

---

## Mudanças para a 5.5 (A Atualização de Automação)

- **Operador de IA (Controlo Autónomo - Shift+A):** Esta é a joia da coroa da v5.5. O Vision Assistant Pro deixou de ser um assistente passivo para se tornar o seu **Operador de IA** pessoal. Não se limita a descrever o ecrã — assume o comando.
  - _Como funciona:_ Agora pode dar instruções verbais para operar o seu PC. Por exemplo, numa aplicação completamente inacessível onde o seu leitor de ecrã permanece silencioso, pode premir **Shift+A** e escrever: _"Clica no botão Definições"_ ou _"Procura o campo de busca, escreve 'Últimas Notícias' e prime enter."_ A IA identifica visualmente os elementos, move o rato e executa a tarefa por si.
  - _Nota de Desempenho:_ Esta funcionalidade está otimizada para o **Gemini 3.0 Flash (Preview)**, entregando respostas incrivelmente rápidas e inteligentes que podem lidar até com os esquemas de UI mais complexos.
  - **\*⚠️ Aviso de Utilização de API:** Como o Operador de IA precisa de "ver" exatamente o que está a acontecer para ser preciso, envia uma captura de ecrã de alta resolução em cada passo. Por favor, note que o uso frequente consumirá a sua quota de API muito mais depressa do que as tarefas padrão baseadas em texto.
- **Explorador Visual de UI (E):** Cansado de navegar por "botões sem etiqueta"? Prima **E** para ativar o Explorador de UI. A IA examinará a janela inteira e gerará uma lista de todos os elementos clicáveis que encontrar — incluindo ícones, gráficos e menus. Basta escolher um item da lista e o Operador de IA clicará nele por si. É como ter uma "camada de acessibilidade" sobre qualquer app.
- **Ação de Ficheiro Inteligente Contextual (F):** A tecla "F" foi completamente remodelada. Já não assume que deseja apenas OCR. Quando seleciona uma única imagem, agora pergunta inteligentemente a sua intenção: pode escolher uma **Descrição Visual Detalhada** para entender a cena ou uma **Extração de Texto Estruturada (OCR)** para leitura. O menu adapta-se dinamicamente com base no tipo de ficheiro e no seu motor de IA ativo.
- **Otimização do Núcleo:** Realizámos uma limpeza profunda na lógica interna do suplemento, removendo funções legadas não utilizadas e código redundante. Isto resulta numa experiência mais leve, rápida e fiável para todos os utilizadores.

## Mudanças para a 5.0

- **Arquitetura Multi-Fornecedor**: Adicionado suporte total para **OpenAI**, **Groq** e **Mistral** a par do Google Gemini. Os utilizadores agora podem escolher o seu backend de IA preferido.
- **Encaminhamento Avançado de Modelos**: Utilizadores de fornecedores nativos (Gemini, OpenAI, etc.) agora podem selecionar modelos específicos de uma lista pendente para diferentes tarefas (OCR, STT, TTS).
- **Configuração Avançada de Endpoint**: Utilizadores de fornecedores personalizados podem introduzir manualmente URLs e nomes de modelos específicos para um controlo granular sobre servidores locais ou de terceiros.
- **Visibilidade Inteligente de Funcionalidades**: O menu de definições e a interface do Leitor de Documentos agora ocultam automaticamente funcionalidades não suportadas (como TTS) com base no fornecedor selecionado.
- **Obtenção Dinâmica de Modelos**: O suplemento agora obtém a lista de modelos disponíveis diretamente da API do fornecedor, garantindo compatibilidade com novos modelos assim que forem lançados.
- **OCR e Tradução Híbridos**: Lógica otimizada para utilizar o Google Tradutor para velocidade ao usar o OCR do Chrome, e tradução baseada em IA ao utilizar os motores Gemini/Groq/OpenAI.
- **"Re-scan com IA" Universal**: O recurso de re-exame do Leitor de Documentos já não está limitado ao Gemini. Agora utiliza qualquer fornecedor de IA que esteja ativo no momento para reprocessar as páginas.

## Mudanças para a 4.6

- **Recuperação Interativa de Resultados:** Adicionada a tecla **Espaço** à camada de comando, permitindo que os utilizadores reabram instantaneamente a última resposta da IA numa janela de chat para perguntas de acompanhamento, mesmo quando o modo "Saída Direta" está ativo.
- **Hub da Comunidade no Telegram:** Adicionada uma ligação para o "Canal Oficial no Telegram" no menu Ferramentas do NVDA, fornecendo uma maneira rápida de se manter atualizado com as últimas notícias, funcionalidades e lançamentos.
- **Estabilidade de Resposta Aprimorada:** Otimizada a lógica central para as funcionalidades de Tradução, OCR e Visão para garantir um desempenho mais fiável e uma experiência mais fluida ao utilizar a saída de fala direta.
- **Orientação de Interface Melhorada:** Atualizadas as descrições de definições e a documentação para melhor explicar o novo sistema de recuperação e como funciona em conjunto com as definições de saída direta.

## Mudanças para a 4.5

- **Gestor de Prompts Avançado:** Introduzido um diálogo de gestão dedicado nas definições para personalizar prompts padrão do sistema e gerir prompts definidos pelo utilizador com suporte total para adicionar, editar, reordenar e pré-visualizar.
- **Suporte Abrangente a Proxy:** Resolvidos problemas de conectividade de rede garantindo que as definições de proxy configuradas pelo utilizador sejam aplicadas estritamente a todos os pedidos de API, incluindo tradução, OCR e geração de fala.
- **Migração Automática de Dados:** Integrado um sistema de migração inteligente para atualizar automaticamente as configurações de prompt legadas para um formato JSON v2 robusto na primeira execução, sem perda de dados.
- **Compatibilidade Atualizada (2025.1):** Definida a versão mínima do NVDA para 2025.1 devido a dependências de biblioteca em funcionalidades avançadas como o Leitor de Documentos para garantir um desempenho estável.
- **Interface de Definições Otimizada:** Simplificada a interface de definições reorganizando o gerenciamento de prompts num diálogo separado, proporcionando uma experiência de utilizador mais limpa e acessível.
- **Guia de Variáveis de Prompt:** Adicionado um guia integrado nos diálogos de prompt para ajudar os utilizadores a identificar e utilizar facilmente variáveis dinâmicas como [selection], [clipboard] e [screen_obj].

## Mudanças para a 4.0.3

- **Resiliência de Rede Aprimorada:** Adicionado um mecanismo de tentativa automática para lidar melhor com ligações de internet instáveis e erros temporários do servidor, garantindo respostas de IA mais confiáveis.
- **Diálogo de Tradução Visual:** Introduzida uma janela dedicada para resultados de tradução. Os utilizadores agora podem navegar facilmente e ler traduções longas linha por linha, de forma semelhante aos resultados de OCR.
- **Visualização Formatada Agregada:** A funcionalidade "Ver Formatado" no Leitor de Documentos agora exibe todas as páginas processadas numa única janela organizada com cabeçalhos de página claros.
- **Fluxo de Trabalho de OCR Otimizado:** Ignora automaticamente a seleção de intervalo de páginas para documentos de página única, tornando o processo de reconhecimento mais rápido e fluido.
- **Estabilidade de API Melhorada:** Mudança para um método de autenticação baseado em cabeçalho mais robusto, resolvendo possíveis erros de "Todas as chaves de API falharam" causados por conflitos de rotação de chaves.
- **Correções de Bugs:** Resolvidos vários erros (crashes) potenciais, incluindo um problema durante o encerramento do suplemento e um erro de foco no diálogo de chat.

## Mudanças para a 4.0.1

- **Leitor de Documentos Avançado:** Um novo e poderoso visualizador para PDF e imagens com seleção de intervalo de páginas, processamento em segundo plano e navegação fluida via `Ctrl+PageUp/Down`.
- **Novo Submenu de Ferramentas:** Adicionado um submenu dedicado "Vision Assistant" sob o menu Ferramentas do NVDA para acesso mais rápido às funcionalidades principais, definições e documentação.
- **Customização Flexível:** Agora pode escolher o seu motor de OCR preferido e a voz TTS diretamente do painel de definições.
- **Suporte a Múltiplas Chaves de API:** Adicionado suporte para várias chaves de API do Gemini. Pode introduzir uma chave por linha ou separá-las por vírgulas nas definições.
- **Motor de OCR Alternativo:** Introduzido um novo motor de OCR para garantir o reconhecimento de texto confiável mesmo ao atingir os limites de quota da API do Gemini.
- **Rotação Inteligente de Chaves de API:** Alterna automaticamente para a chave de API que estiver a funcionar mais rápido e memoriza-a para contornar limites de quota.
- **Documento para MP3/WAV:** Capacidade integrada de gerar e guardar ficheiros de áudio de alta qualidade nos formatos MP3 (128kbps) e WAV diretamente no leitor.
- **Suporte a Stories do Instagram:** Adicionada a capacidade de descrever e analisar Stories do Instagram utilizando os seus URLs.
- **Suporte ao TikTok:** Introduzido suporte para vídeos do TikTok, permitindo descrição visual completa e transcrição de áudio dos clipes.
- **Diálogo de Atualização Redesenhado:** Apresenta uma nova interface acessível com uma caixa de texto rolável para ler claramente as mudanças de versão antes de instalar.
- **Estado e UX Unificados:** Padronização dos diálogos de ficheiros em todo o suplemento e aprimoramento do comando 'L' para relatar o progresso em tempo real.

## Mudanças para a 3.6.0

- **Sistema de Ajuda:** Adicionado um comando de ajuda (`H`) dentro da Camada de Comando para fornecer uma lista de fácil acesso de todos os atalhos e as suas funções.
- **Análise de Vídeo Online:** Suporte expandido para incluir vídeos do **Twitter (X)**. Também foi melhorada a deteção de URL e a estabilidade para uma experiência mais confiável.
- **Contribuição ao Projeto:** Adicionado um diálogo opcional de doação para utilizadores que desejam apoiar as futuras atualizações e o crescimento contínuo do projeto.

## Mudanças para a 3.5.0

- **Camada de Comando:** Introduzido um sistema de Camada de Comando (predefinição: `NVDA+Shift+V`) para agrupar atalhos sob uma única tecla mestra. Por exemplo, em vez de premir `NVDA+Control+Shift+T` para tradução, agora prime `NVDA+Shift+V` seguido de `T`.
- **Análise de Vídeo Online:** Adicionado um novo recurso para analisar vídeos do YouTube e Instagram diretamente fornecendo um URL.

## Mudanças para a 3.1.0

- **Modo de Saída Direta:** Adicionada uma opção para saltar o diálogo de chat e ouvir as respostas da IA diretamente via fala para uma experiência mais rápida e fluida.
- **Integração com Área de Transferência:** Adicionada uma nova definição para copiar automaticamente as respostas da IA para a área de transferência.

## Mudanças para a 3.0

- **Novos Idiomas:** Adicionadas traduções para **Persa** e **Vietnamita**.
- **Modelos de IA Expandidos:** Reorganizada a lista de seleção de modelos com prefixos claros (`[Free]`, `[Pro]`, `[Auto]`) para ajudar os utilizadores a distinguir entre modelos gratuitos e limitados (pagos). Adicionado suporte para **Gemini 3.0 Pro** e **Gemini 2.0 Flash Lite**.
- **Estabilidade do Ditado:** Estabilidade do Ditado Inteligente significativamente melhorada. Adicionada uma verificação de segurança para ignorar clipes de áudio menores que 1 segundo, evitando alucinações da IA e erros de áudio vazio.
- **Manuseamento de Ficheiros:** Corrigido um problema em que o upload de ficheiros com nomes não em inglês falhava.
- **Otimização de Prompts:** Lógica de Tradução melhorada e resultados de Visão estruturados.

## Mudanças para a 2.9

- **Adicionadas traduções em Francês e Turco.**
- **Visualização Formatada:** Adicionado um botão "Ver Formatado" nos diálogos de chat para visualizar a conversa com estilo adequado (Cabeçalhos, Negrito, Código) numa janela de navegação padrão.
- **Definição de Markdown:** Adicionada uma nova opção "Limpar Markdown no Chat" nas Definições. Desmarcar isto permite que os utilizadores vejam a sintaxe Markdown bruta (ex: `**`, `#`) na janela de chat.
- **Gestão de Diálogos:** Corrigido um problema em que as janelas de "Refinar Texto" ou de chat abriam várias vezes ou falhavam em focar corretamente.
- **Melhorias de UX:** Padronização dos títulos dos diálogos de ficheiro para "Abrir" e remoção de anúncios de voz redundantes (ex: "A abrir o menu...") para uma experiência mais suave.

## Mudanças para a 2.8

- Adicionada tradução em Italiano.
- **Relatório de Estado:** Adicionado um novo comando (NVDA+Control+Shift+I) para anunciar o estado atual do suplemento (ex: "A carregar...", "A analisar...").
- **Exportação HTML:** O botão "Guardar Conteúdo" nos diálogos de resultado agora guarda a saída como um ficheiro HTML formatado, preservando estilos como cabeçalhos e negrito.
- **UI de Definições:** Esquema do painel de Definições melhorado com agrupamento acessível.
- **Novos Modelos:** Adicionado suporte para gemini-flash-latest e gemini-flash-lite-latest.
- **Idiomas:** Adicionado Nepalês aos idiomas suportados.
- **Lógica do Menu de Refino:** Corrigido um erro crítico onde os comandos "Refinar Texto" falhavam se o idioma da interface do NVDA não fosse o inglês.
- **Ditado:** Deteção de silêncio melhorada para evitar saída de texto incorreta quando não é introduzida fala.
- **Definições de Atualização:** "Procurar atualizações ao iniciar" agora está desativado por predefinição para cumprir as políticas da Add-on Store.
- Limpeza de código.

## Mudanças para a 2.7

- Migração da estrutura do projeto para o Template oficial de Suplementos da NV Access para melhor conformidade com os padrões.
- Implementada lógica de tentativa automática para erros HTTP 429 (Limite de Taxa) para garantir fiabilidade durante tráfego elevado.
- Prompts de tradução otimizados para maior precisão e melhor tratamento da lógica de "Troca Inteligente".
- Tradução russa atualizada.

## Mudanças para a 2.6

- Adicionado suporte à tradução russa (Obrigado ao nvda-ru).
- Mensagens de erro atualizadas para fornecer feedback mais descritivo sobre a conectividade.
- Idioma de destino predefinido alterado para Inglês.

## Mudanças para a 2.5

- Adicionado Comando de OCR de Ficheiro Nativo (NVDA+Control+Shift+F).
- Adicionado botão "Guardar Chat" aos diálogos de resultado.
- Implementado suporte total à localização (i18n).
- Migração do feedback de áudio para o módulo de tons nativos do NVDA.
- Mudança para a API de Ficheiros do Gemini para melhor tratamento de ficheiros PDF e de áudio.
- Corrigido erro (crash) ao traduzir texto contendo chavetas.

## Mudanças para a 2.1.1

- Corrigido um problema em que a variável [file_ocr] não funcionava corretamente dentro dos Prompts Personalizados.

## Mudanças para a 2.1

- Padronização de todos os atalhos para utilizar NVDA+Control+Shift para eliminar conflitos com o esquema de Portátil (Laptop) do NVDA e teclas de atalho do sistema.

## Mudanças para a 2.0

- Implementado sistema de Atualização Automática integrado.
- Adicionado Cache de Tradução Inteligente para recuperação instantânea de textos traduzidos anteriormente.
- Adicionada Memória de Conversa para refinar contextualmente os resultados nos diálogos de chat.
- Adicionado comando dedicado de Tradução de Área de Transferência (NVDA+Control+Shift+Y).
- Prompts de IA otimizados para impor estritamente a saída no idioma de destino.
- Corrigido erro (crash) provocado por caracteres especiais no texto de entrada.

## Mudanças para a 1.5

- Adicionado suporte para mais de 20 novos idiomas.
- Implementado Diálogo de Refino Interativo para perguntas de acompanhamento.
- Adicionado recurso de Ditado Inteligente Nativo.
- Adicionada categoria "Vision Assistant" ao diálogo de Gestos de Entrada do NVDA.
- Corrigidos erros (crashes) de COMError em aplicações específicas como Firefox e Word.
- Adicionado mecanismo de tentativa automática para erros do servidor.

## Mudanças para a 1.0

- Lançamento inicial.
