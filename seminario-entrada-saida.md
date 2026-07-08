# Seminário: Entrada/Saída - Cap. 7

**Disciplina:** Organização de Computadores (Adam)
**Apresentação:** 02/07/2026
**Grupo:** 4

## Entregas

- [ ] Seminário - parte teórica (mín. 30min)
- [ ] Atividade prática (mín. 30min)
- [x] Questionário avaliativo (5-10 questões) — entregar até 30/06
- [x] Material Notion - https://app.notion.com/p/Sistemas-de-Entrada-Sa-da-395ec95514fc805bbecad83311a99918?source=copy_link

## 1. Dispositivos externos, transdutores e módulos de E/S

Os sistemas de computação necessitam de um terceiro pilar organizacional, além da CPU e da memória principal, que são os módulos de Entrada/Saída. Cada módulo opera como um intermediador lógico acoplado ao barramento do sistema ou a um comutador central, sendo responsável pelo controle de um ou mais dispositivos periféricos. Conectar dispositivos externos diretamente aos barramentos de alta velocidade do sistema é inviável devido à variabilidade dos métodos operacionais, à grande incompatibilidade entre as taxas de transferência de dados e às discrepâncias estruturais de formatos e comprimentos de palavra.

Dessa forma, para compreender o grau de sofisticação dos mecanismos atuais de interconexão, torna-se necessário examinar a taxonomia clássica proposta por William Stallings, que descreve a evolução histórica da função de Entrada/Saída. Com o avanço dos sistemas computacionais, buscou-se reduzir a responsabilidade da CPU pelo controle de temporização e pelo gerenciamento dos dispositivos periféricos, transferindo essas atribuições para módulos especializados. Segundo essa classificação, esse processo evolutivo pode ser dividido em seis etapas distintas.

1. **Controle direto pela CPU:** A CPU controla diretamente o dispositivo periférico. Toda a lógica de temporização, ativação de linhas magnéticas ou mecânicas e amostragem de dados depende de instruções executadas pelo processador central, mantendo-o ocupado integralmente durante a operação.
2. **Adição de um controlador/módulo de E/S (sem interrupções):** Introduz-se um módulo de E/S ou controlador intermediário. A CPU passa a utilizar E/S programada. Embora o hardware do módulo gerencie os detalhes físicos do periférico, a CPU ainda precisa gastar ciclos de processamento testando repetidamente os bits de estado (*polling*) para saber quando a operação terminou.
3. **E/S dirigida por interrupções:** A mesma estrutura da etapa anterior é aprimorada com linhas de sinalização física de interrupção. A CPU emite o comando de E/S, executa outras tarefas úteis de computação e é alertada pelo módulo de E/S via interrupção de hardware apenas quando os dados estão prontos para transferência, o que elimina a espera ociosa.
4. **Acesso direto à memória (DMA):** O módulo de E/S ganha a capacidade de interagir diretamente com a memória principal do sistema através de um controlador de DMA. A CPU intervém apenas no início (configurando ponteiros e tamanho do bloco) e no fim da transferência. O bloco de dados é movido diretamente entre o periférico e a memória sem transitar pelos registradores internos da CPU.
5. **Canais de E/S (módulos baseados em processadores):** O módulo de E/S é aprimorado para se tornar um processador de propósito específico integrado, dotado de um conjunto de instruções especializado (conhecido como Canal de E/S). A CPU executa um programa de canal residente na memória principal, e o canal assume o controle completo de sequências complexas de comandos de E/S.
6. **Processadores de E/S autônomos:** O módulo de E/S passa a possuir sua própria memória local dedicada (além de sua unidade de processamento), operando virtualmente como um sistema computacional autônomo dentro do ecossistema principal. Essa arquitetura minimiza quase a zero a interferência na CPU principal, sendo bastante utilizada para gerenciar matrizes de discos volumosas e redes de alta capacidade.

```
+-------------------------------------------------------------+
|                     Barramento do Sistema                   |
+-----+----------------------+--------------------------+-----+
      |                      |                          |
Linhas de Dados       Linhas de Endereço        Linhas de Controle
      |                      |                          |
+-----+----------------------+--------------------------+-----+
|                        MÓDULO DE E/S                        |
|                                                             |
|  +--------------------+  +--------------------+  +-------+  |
|  | Reg. Dados Interno |  | Reg. Estado/Contr. |  | Lógica|  |
|  +--------------------+  +--------------------+  | de    |  |
|           ^                         ^            | Inter-|  |
|           |                         |            | face  |  |
|           +-------------------------+------------|       |  |
|                                                  +-------+  |
+----------------------------+--------------------------------+
                             |
                   +---------+---------+
                   |  Sinais de E/S:   |
                   |  Dados, Estado    |
                   |  e Controle       |
                   +---------+---------+
                             |
+----------------------------v--------------------------------+
|                     DISPOSITIVO PERIFÉRICO                  |
|                                                             |
|  +--------------------+  +--------------------+  +-------+  |
|  | Lógica de Controle |  |  Buffer de Dados   |  | Trans-|  |
|  +--------------------+  +--------------------+  | dutor |  |
|                                                  +-------+  |
+-------------------------------------------------------------+
```

Independentemente do grau de complexidade ou da geração tecnológica da arquitetura, Stallings formaliza que um módulo de E/S deve desempenhar obrigatoriamente cinco funções nucleares para garantir a viabilidade operacional do sistema.

- **Controle e temporização:** Coordenar o fluxo de tráfego entre os recursos internos do computador (como memória e CPU) e os dispositivos externos. Essa função é muito importante para sincronizar barramentos de velocidades heterogêneas e evitar colisões ou perdas de dados.
- **Comunicação com a CPU:** Operar o diálogo lógico com o processador central, o que envolve a decodificação de comandos enviados pelo barramento de controle; a troca de dados através do barramento de dados; o relatório contínuo de estado (*status*), indicando se o módulo está ocupado, pronto ou em condição de erro; e o reconhecimento do endereço atribuído ao periférico.
- **Comunicação com o dispositivo externo:** Traduzir as requisições lógicas do sistema em comandos físicos específicos (sinais de controle, ordens de posicionamento) e ler o estado operacional reportado pelos transdutores do periférico.
- **Buffering de dados:** Atuar como uma área de armazenamento temporário de dados. Como as taxas de transferência da memória principal e da CPU são ordens de grandeza superiores às velocidades dos periféricos (como unidades mecânicas ou interfaces seriais), o módulo acumula os dados no *buffer* para que eles possam ser transmitidos em rajadas de alta velocidade no barramento, o que otimiza a utilização do sistema.
- **Detecção de erros:** Identificar e reportar falhas operacionais, as quais podem ser anomalias mecânicas/físicas inerentes ao dispositivo (como falta de papel em impressoras ou setores defeituosos em mídias) ou erros de transmissão de dados (como corrupção de bits, detectados por meio de técnicas de paridade, *checksum* ou CRC).

### Transição de barramentos compartilhados para links ponto a ponto e buffering

No nível físico e de sinalização, a arquitetura de E/S clássica com barramentos paralelos compartilhados introduzia o problema do desalinhamento de clock (*clock skew*) e a limitação de largura de banda imposta pela capacitância das múltiplas trilhas metálicas concorrentes. Os módulos de E/S modernos evoluíram para interfaces seriais de alta velocidade baseadas em pacotes estruturados sobre links ponto a ponto.

A função de buffering de dados, descrita na literatura como um registrador temporário de 8 a 16 bits para dispositivos seriais, escalou em sistemas modernos para buffers baseados em filas FIFO estáticas de alta velocidade implementadas em silício dentro de controladores e circuitos integrados específicos de aplicação (ASICs). O módulo de E/S atua como um regulador de vazão ativo, gerenciando o controle de fluxo baseado em créditos virtuais no barramento, impedindo que rajadas transitórias de dados originadas no barramento de sistema saturem o transdutor do dispositivo externo, ou vice-versa.

### Classificações de dispositivos externos

| **Classe de Periférico** | **Alvo Primário** | **Taxa de Dados Típica** | **Natureza da Latência** | **Mecanismo de Transdução** | **Exemplo de Aplicação** |
| --- | --- | --- | --- | --- | --- |
| **Inteligível ao Humano** | Usuário final. | Baixa (Bps a KBps). | Alta e determinada pela percepção humana. | Conversão de sinais elétricos em energia mecânica, luminosa ou acústica. | Teclados mecânicos, monitores OLED, displays de smartphones. |
| **Inteligível à Máquina** | Controladores e unidades lógicas. | Alta (MBps a GBps). | Crítica e altamente dependente da física do meio. | Conversão de padrões magnéticos, ópticos ou variações de carga de silício em bits. | Unidades de disco rígido, drives SSD NVMe, sensores industriais. |
| **Comunicação** | Sistemas remotos e redes. | Ultra-Alta (1 Gbps a 400+ Gbps). | Baixa e crítica para o processamento de pacotes. | Conversão de impulsos elétricos internos em ondas de radiofrequência ou pulsos fotônicos. | Controladores Ethernet, chips transceptores ópticos, módulos Wi-Fi 7. |

### Dinâmica de operação: fluxos de caracteres vs. Transdução de blocos

Do ponto de vista operacional clássico enfatizado por Stallings, a interface com dispositivos inteligíveis ao humano (cujo exemplo arquetípico é o conjunto teclado/monitor) baseia-se fortemente na transmissão de fluxos de caracteres codificados. Historicamente, adota-se o *International Reference Alphabet* (IRA) ou o padrão ASCII, onde cada pressionamento de tecla gera um código binário de 7 ou 8 bits enviado ao módulo de E/S, exigindo pouca largura de banda, mas demandando mapeamento de interrupções em tempo real.

Em contrapartida, os dispositivos inteligíveis à máquina (notoriamente os drives de disco rígido e unidades de armazenamento magnético/óptico) operam na escala de blocos de dados (setores). O módulo de E/S interage controlando transdutores eletrônicos ou eletromecânicos (como cabeças de leitura/escrita e braços móveis), convertendo fluxos de bits e variações de propriedades físicas do meio em registros lógicos organizados. Essa categoria exige buffers de memória substancialmente maiores e mecanismos complexos de verificação de erros (como ECC) embutidos no próprio controlador do dispositivo.

Em datacenters corporativos de nuvem em hiperescala, os controladores de armazenamento corporativo implementam a abstração do módulo de E/S ao isolar os canais físicos de barramento de sistema (PCIe) das matrizes de memória flash NAND. Esses controladores agregam múltiplos canais internos, gerenciam algoritmos de correção de erros por hardware (ECC BCH ou LDPC) e realizam o buffering em memórias DRAM voláteis locais integradas ao encapsulamento do controlador, impedindo que as oscilações microscópicas de leitura física das células flash afetem a estabilidade e a latência de acesso do barramento principal do host.

## 2. E/S programada e modos de mapeamento de endereços

Com a técnica de E/S programada, os dados trafegam diretamente entre os registradores internos do processador e o módulo de E/S. O processador possui controle estrito sobre a operação de transferência, executando repetidamente um laço de instruções ativas para ler e inspecionar o bit de estado (*READY/BUSY*) do periférico até que o dispositivo esteja apto a receber ou enviar novas palavras de dados.

O mapeamento desse fluxo pode ocorrer por meio de duas filosofias de endereçamento distintas, que são a E/S mapeada em memória (*Memory-Mapped I/O* - MMIO) e a E/S independente ou isolada (*Isolated I/O*).

```
Memory-Mapped I/O (Espaço Unificado):
0x00000000 +-----------------------------------+
           |    Memória RAM Principal (DRAM)   |
           |                                   |
0x0001FF00 +-----------------------------------+
           |   Registradores do Módulo de E/S  | (Acessados via instruções normais
0x0001FFFF +-----------------------------------+  de CPU como MOV ou LDR)
           |    Memória RAM Principal (DRAM)   |
0xFFFFFFFF +-----------------------------------+

Isolated I/O (Espaços de Endereçamento Segregados):
Espaço de Memória Físico                   Espaço de E/S Dedicado
0x00000000 +-------------------------+     0x0000 +-------------------------+
           |       Memória RAM       |            | Registradores de E/S    | (Acessado apenas por
           |       Principal         |            | (Portas de E/S)         |  instruções especiais
           |         (DRAM)          |     0xFFFF +-------------------------+  como IN e OUT)
0xFFFFFFFF +-------------------------+
```

### Mecânica de MMIO e coerência de cache

A filosofia de projeto da E/S mapeada em memória trata os registradores de controle, estado e dados dos periféricos como posições de memória física comuns. A principal vantagem desse design é a unificação do conjunto de instruções, o que permite que o repertório de comandos de manipulação de memória da CPU (instruções de leitura, escrita, operações aritméticas diretas e modos de endereçamento indireto) seja aplicado diretamente para interagir com o hardware.

A maior desvantagem reside na alocação de faixas do espaço de endereçamento linear da CPU e no impacto causado no subsistema de memória virtual e caches de dados. No nível da unidade de gerenciamento de memória (MMU), as páginas de endereços físicas reservadas para MMIO devem ser categorizadas explicitamente nas tabelas de páginas como *Uncacheable* (não-cacheáveis) e *Strongly Ordered* (fortemente ordenadas) ou *Device Memory*.

Se essa classificação não for aplicada, a CPU fará o cache dos valores lidos dos registradores do periférico na cache L1/L2 interna. Como resultado, as operações subsequentes de leitura lerão dados defasados da cache em vez do valor atualizado dinamicamente pelo transdutor físico do dispositivo externo.

Adicionalmente, as operações de escrita permaneceriam temporariamente retidas na cache interna em modo *write-back*, impedindo que os sinais de comando chegassem ao periférico de forma instantânea. Em sistemas modernos de arquitetura superescalar com execução fora de ordem (*Out-of-Order Execution*), a presença de instruções MMIO exige o uso imperativo de barreiras de memória (*Memory Barriers* ou instruções de *fence*) no nível da engenharia de software para garantir a correta ordenação temporal dos acessos aos registradores de hardware, impedindo que leituras e escritas críticas ao periférico sejam reordenadas pelo pipeline da CPU.

### MMIO (*Memory-Mapped I/O*) vs. E/S isolada

| **Critério de Análise** | **Memory-Mapped I/O (MMIO)** | **Isolated I/O (E/S Independente)** |
| --- | --- | --- |
| **Estrutura de Endereçamento** | Espaço de endereçamento de memória unificado com a RAM física. | Espaço de portas de E/S segregado da memória física. |
| **Conjunto de Instruções** | Usa qualquer instrução de acesso à memória (ex: `MOV`, `LDR`, `STR`). | Usa instruções específicas de E/S da arquitetura (ex: `IN`, `OUT` no x86). |
| **Linhas de Controle do Barramento** | Uma única linha de controle de leitura/gravação unificada. | Linhas de leitura/escrita separadas para memória e para portas de E/S. |
| **Impacto no Espaço de Endereço** | Consome porções do espaço de endereçamento da CPU. | Preserva o espaço de endereçamento de memória intacto. |
| **Uso em Arquiteturas Modernas** | Padrão absoluto em arquiteturas RISC (ARM, RISC-V, MIPS). | Restrito a legados e legibilidade retrocompatível na arquitetura x86. |

Em microcontroladores modernos baseados em arquiteturas ARM Cortex-M0/M4/M7, amplamente utilizados em sistemas embarcados e sensores inteligentes de Internet das Coisas (IoT), todos os periféricos de comunicação interna (UART, SPI, I2C) e interfaces GPIO (*General Purpose Input/Output*) são controlados estritamente via MMIO. Os drivers de dispositivo são mapeados associando ponteiros em linguagem C para estruturas contendo qualificadores `volatile` apontando diretamente para as coordenadas físicas de memória reservadas aos registradores de E/S, forçando o compilador a emitir instruções diretas de carga e descarga na memória e impedindo otimizações indevidas do compilador.

Enquanto as arquiteturas de sistemas embarcados modernos empregam o mapeamento em memória de forma nativa como no ARM Cortex, a literatura clássica de Stallings adota o Intel 82C55A PPI (Programmable Peripheral Interface) como o exemplo definitivo de implementação de E/S programada no ecossistema x86 original.

O 82C55A expõe internamente quatro registradores programáveis de 8 bits para o barramento do sistema (Canais A, B, C e um Registrador de Controle), acessados por meio de instruções específicas de E/S isolada (`IN` e `OUT`). Através de E/S programada pura, o programador deve enviar uma palavra de controle para configurar se as portas físicas operarão como entrada ou saída e, subsequentemente, executar laços de software contínuos para ler os estados de prontidão de periféricos legados (como teclados matriciais ou sensores paralelos), o que demonstra o comportamento assíncrono e de alto consumo de CPU característico dessa técnica antes do advento das interrupções generalizadas.

## 3. E/S controlada por interrupção e evolução dos co-processadores de interrupção

Para mitigar a ineficiência inerente da E/S programada, onde a CPU permanece presa em laços ociosos de verificação de estado, adota-se a técnica de E/S controlada por interrupção. O processador emite o comando ao módulo de E/S e prossegue imediatamente com a execução de outras tarefas úteis.

Quando o periférico está pronto para transferir os dados, o módulo de E/S sinaliza eletronicamente o processador através de uma linha de requisição de interrupção. A CPU desvia o fluxo de controle atual para uma rotina de tratamento de interrupção específica (ISR) que executa a transação e retorna a execução original do programa sem perda de contexto.

```
+-------------------------------------------------------------+
|                     BARRAMENTO DE SISTEMA                   |
+------------------------------+------------------------------+
                               |
                   +-----------v-----------+
                   |     I/O APIC (PCH)    | (Controlador de interrupções
                   +-----------+-----------+  de sistema no chipset)
                               |
               In-Band PCIe    | (Redirecionamento de Interrupção
               MSI-X Message   |  via barramento de sistema)
                               v
+-------------------------------------------------------------+
|                         CPU MULTICORE                       |
|                                                             |
|  +--------------------+             +--------------------+  |
|  |  Núcleo 0 (Core 0) |             |  Núcleo 1 (Core 1) |  |
|  |  +--------------+  |             |  +--------------+  |  |
|  |  |  Local APIC  |  |             |  |  Local APIC  |  |  |
|  |  +-------+------+  |             |  +-------+------+  |  |
|  +----------|---------+             +----------|---------+  |
|             v                                  v            |
|       MSI Vector 64                      MSI Vector 82      |
|    (Assigned to Core 0)               (Assigned to Core 1)  |
+-------------------------------------------------------------+
```

### Técnicas de identificação de dispositivos e vetorização

Quando múltiplos periféricos compartilham a capacidade de interromper a CPU, o sistema enfrenta um desafio de projeto de hardware, que é determinar com exatidão qual módulo gerou a requisição de interrupção em um dado momento. Stallings divide as soluções para esse problema em quatro categorias clássicas de engenharia.

1. **Múltiplas linhas de interrupção físicas:** A abordagem mais direta consiste em fornecer linhas de requisição físicas dedicadas e independentes no barramento entre cada módulo de E/S e a CPU. Embora seja extremamente rápida, é uma solução inviável para sistemas complexos devido à limitação física de pinagem no encapsulamento do processador.
2. **Varredura de software (*Software Poll*):** Quando uma interrupção ocorre, a CPU desvia a execução para uma rotina geral de serviço cuja primeira tarefa é interrogar sequencialmente cada módulo de E/S, lendo seus registradores de estado até encontrar o bit que indica a autoria da interrupção. É uma alternativa barata em termos de hardware, mas penaliza severamente a latência do sistema devido ao tempo gasto no laço de checagem via código.
3. **Encadeamento de margarida (*Daisy Chain* / Interrupção Vetorizada):** Trata-se de uma solução de arbitragem em série feita por hardware. A linha de requisição de interrupção é comum a todos os módulos. Quando a CPU aceita a interrupção, ela emite um sinal de reconhecimento (*Interrupt Acknowledge*) que se propaga sequencialmente de módulo em módulo através de um circuito em série. O primeiro módulo da fila que tiver uma interrupção pendente intercepta esse sinal e impede sua propagação. Como resposta, ele coloca seu "vetor de interrupção" (um identificador único ou endereço da rotina de tratamento) diretamente no barramento de dados para que a CPU o leia.
4. **Arbitragem de Barramento (*Bus Arbitration* / Interrupção Vetorizada):** Utiliza mecanismos de arbitragem paralela ou centralizada integrados ao barramento do sistema. Para poder sinalizar uma interrupção, o módulo de E/S deve primeiro disputar e ganhar o controle do barramento de sistema (tornando-se o mestre do barramento). Ao conseguir o controle, o módulo ativa a linha de interrupção e disponibiliza seu vetor diretamente nas linhas de dados.

### A evolução de PIC para APIC e MSI-X

O tratamento de interrupções clássico em arquiteturas de computadores x86 baseava-se em chips controladores programáveis de interrupção (PIC) externos dedicados, como o Intel 82C59A, operando em uma topologia em cascata para suportar até 15 linhas físicas de IRQ (*Interrupt Request*). Com a ascensão dos processadores multicore modernos, essa arquitetura centralizada tornou-se obsoleta, sendo substituída pelo APIC (*Advanced Programmable Interrupt Controller*), composto por unidades locais (*Local APIC* - LAPIC) integradas individualmente em cada núcleo da CPU e um bloco *I/O APIC* situado no chipset de controle do sistema.

A maior inovação em sistemas contemporâneos foi o abandono das linhas físicas analógicas de interrupção em barramentos paralelos, dando lugar às Interrupções Sinalizadas por Mensagem (*Message Signaled Interrupts* - MSI e MSI-X) no barramento PCI Express. O MSI e o MSI-X operam eliminando as trilhas de cobre dedicadas à sinalização de interrupções físicas de pinos (*out-of-band*). No lugar delas, o dispositivo de E/S realiza uma escrita de dados na banda principal do barramento PCIe (*in-band*) apontando para um endereço de memória especial pertencente ao LAPIC do processador.

O MSI-X expande de forma expressiva o MSI clássico. Enquanto o MSI está restrito a 32 vetores alocados consecutivamente, o MSI-X suporta até 2048 vetores de interrupção por dispositivo físico. Cada vetor possui um endereço de memória física de destino de 64 bits e uma palavra de dados específica definidos em uma tabela dinâmica mantida na memória interna do periférico. Isso permite que os sistemas operacionais modernos associem cada fila de interrupção a um núcleo de CPU distinto (*IRQ Affinity*), distribuindo o processamento de forma equitativa e evitando rajadas de interrupções em um único núcleo que possam causar contenção de cache e degradação severa das latências de cauda de aplicações de alto desempenho.

### Mecanismos de sinalização de interrupção

| **Atributo Técnico** | **Intel 82C59A (PIC Legado)** | **MSI (PCI 2.2)** | **MSI-X (PCI 3.0 / PCIe)** |
| --- | --- | --- | --- |
| **Linhas Físicas** | 8 canais por chip em barramento paralelo dedicado. | Zero linhas dedicadas; usa escrita de dados em barramento compartilhado. | Zero linhas dedicadas; usa escrita de dados estruturada em tabela interna. |
| **Capacidade de Vetores** | Máximo de 15 IRQs em configuração master/slave. | Até 32 vetores por dispositivo de hardware. | Até 2048 vetores de sinalização independentes. |
| **Afinidade de Núcleo** | Centralizado em uma única CPU monolítica. | Restrito a um único núcleo ou conjunto fixo de núcleos simultaneamente. | Flexível; cada interrupção pode ser direcionada a qualquer núcleo individual. |
| **Mapeamento de Destino** | Mapeado por pinagem e portas de controle físicas. | Endereço físico e palavra de dados fixos gravados na inicialização. | Tabela na memória do dispositivo mapeada dinamicamente por vetor. |

Placas de rede de alto desempenho de 100 GbE para servidores de computação em nuvem utilizam o MSI-X extensivamente. O driver de rede aloca múltiplos canais independentes de recebimento (Rx) e transmissão (Tx), atribuindo a cada um um vetor MSI-X exclusivo. À medida que os pacotes de rede chegam, a placa de rede distribui as interrupções de hardware resultantes de forma uniforme entre as dezenas de núcleos disponíveis do processador host, o que garante vazão máxima estável e paralelismo real no processamento de rede de espaço de usuário.

## 4. Acesso Direto à Memória (DMA), Scatter-Gather e virtualização via IOMMU

O DMA elimina a desvantagem inerente à E/S controlada por interrupções em fluxos de transferência de alto volume, onde cada byte ou palavra que transita da memória principal para o periférico deve passar obrigatoriamente pelos registradores da CPU.

O módulo de DMA funciona como um coprocessador especialista, assumindo o controle temporário dos barramentos do sistema para transferir blocos de dados contínuos diretamente entre os periféricos e a memória física RAM através da técnica de roubo de ciclo (*cycle stealing*).

```
                            SISTEMA MULTIPROCESSADOR
+-----------------------------------------------------------------------------+
|  +--------------------+                               +------------------+  |
|  |     CPU Core       |                               |      IOMMU       |  |
|  +---------+----------+                               +--------+---------+  |
|            |                                                   ^            |
|            v  Tradução MMU                                     |            |
|    +---------------+                                           |            |
|    | Virtual Memory|                                           | Tradução   |
|    +---------------+                                           | IOVA -> SPA|
|            |                                                   |            |
|            +---------> --------+            |
+-----------------------------------------------------------------------------+
                                     |
                                     v
+-----------------------------------------------------------------------------+
|                      Memória RAM Principal (DRAM)                           |
+------------------------------------+----------------------------------------+
                                     ^
                                     | Escrita direta na RAM (SPA)
                                     |
+------------------------------------+----------------------------------------+
|                               PCIe Bus                                      |
+------------------------------------+----------------------------------------+
                                     ^
                                     | Transação com endereço IOVA
                                     |
+------------------------------------+----------------------------------------+
|                        Dispositivo Periférico PCIe                          |
+-----------------------------------------------------------------------------+
```

### Mecânica de tradução IOMMU, Scatter-Gather e isolamento de VM

Os sistemas modernos evoluíram do DMA físico de blocos sequenciais lineares, controlado por controladores herdados como o Intel 8237A, para arquiteturas baseadas em *Scatter-Gather DMA* (DMA de Dispersão e Coleta). O *Scatter-Gather* opera por meio de anéis de descritores alocados na memória do sistema. Cada descritor aponta para um endereço de memória não contíguo e especifica a quantidade de dados. O módulo de DMA executa varreduras sequenciais nessa lista de descritores físicos, encadeando a transferência de múltiplas regiões de RAM fragmentadas em uma única transação coesa do ponto de vista do dispositivo.

A grande revolução em termos de segurança e suporte à virtualização de hardware foi a introdução das Unidades de Gerenciamento de Memória de Entrada/Saída (IOMMU), denominadas *Intel VT-d*, *AMD-Vi* ou *ARM SMMU*. Em um sistema desprovido de IOMMU, qualquer dispositivo PCIe dotado de capacidade de DMA manipula diretamente endereços físicos do sistema (*System Physical Addresses* - SPA). Isso gera riscos de segurança graves, permitindo ataques de DMA onde um firmware comprometido no periférico ou um bug em driver sob o sistema operacional principal sobrescreva regiões confidenciais do kernel na RAM.

A IOMMU atua como uma barreira lógica inserida na raiz do barramento PCIe. Sob esse modelo, os periféricos passam a referenciar os endereços em um espaço virtual específico de E/S chamado de Endereço Virtual de E/S (*I/O Virtual Address* - IOVA). Quando o dispositivo inicia um ciclo de DMA PCIe apontando para um IOVA, a IOMMU intercepta a transação e realiza a tradução para o endereço físico SPA correspondente usando uma tabela de páginas de E/S em formato de árvore na memória.

Essa tradução impõe custos de latência de barramento. Para atenuar a necessidade de leituras recorrentes das tabelas de tradução na DRAM, as IOMMUs utilizam caches internos de tradução conhecidos como IOTLBs (*I/O Translation Lookaside Buffers*). Em servidores de alta concorrência em nuvem, a constante alocação, invalidação e desalocação de buffers IOVAs causa *flushes* frequentes no IOTLB, introduzindo overhead de tradução que pode reduzir a vazão do barramento de dados.

Sistemas operacionais de alto rendimento utilizam modos otimizados de controle.

- **Modo Pass-Through (*intel_iommu=on iommu=pt*):** Habilita a IOMMU apenas para isolamento de dispositivos delegados a máquinas virtuais, ignorando a tradução em dispositivos que operam nativamente no host para evitar penalidades de tradução baseada em tabelas de páginas.
- **Modo Diferido (*Lazy/Deferred Mode*):** Em vez de realizar chamadas imediatas e dispendiosas para invalidar o IOTLB a cada desalocação de página, as solicitações são retidas em lote para mitigar o overhead de barramento.

### Tecnologias de controle de DMA

| **Característica de E/S** | **DMA Clássico (ex: Intel 8237A)** | **Scatter-Gather DMA** | **DMA com Suporte IOMMU (VT-d/AMD-Vi)** |
| --- | --- | --- | --- |
| **Referência de Endereço** | Endereço Físico Contíguo do Sistema (SPA). | Cadeias de Endereços Físicos do Sistema (Listas de Descritores). | Endereço Virtual de Dispositivo (IOVA) traduzido pela IOMMU. |
| **Isolamento de Segurança** | Inexistente; o periférico possui acesso irrestrito a toda a RAM física. | Inexistente; livre acesso aos limites físicos especificados nos descritores. | Completo; o hardware restringe acessos apenas a páginas explicitamente mapeadas. |
| **Virtualização de VMs** | Exige emulação total por software ou intervenção pesada do hypervisor. | Exige manipulação complexa de descritores virtuais por software. | Nativa e Direta; viabiliza o *PCIe Passthrough* e *SR-IOV* de alto desempenho. |
| **Penalidade de Latência** | Nula no nível de barramento. | Baixo impacto gerado pela varredura de descritores no anel. | Moderada devido à tradução e possíveis faltas no IOTLB (*IOTLB Misses*). |

A virtualização por hardware é a principal aplicação da tecnologia IOMMU. Em datacenters baseados em hipervisores como KVM ou VMware ESXi, o uso da IOMMU viabiliza a passagem direta de placas de rede ou GPUs diretamente para sistemas operacionais convidados (*Guest OS*) sem qualquer sobrecarga de software.

A IOMMU assegura de forma rigorosa que a máquina virtual convidada gerencie o dispositivo através do seu próprio driver de forma nativa e segura, impedindo que acessos de DMA iniciados pelo dispositivo ultrapassem os limites da memória física previamente alocados àquela partição virtual de servidor.

### Controlador Intel 8237A

Para ilustrar a viabilização física da arquitetura de DMA em sistemas comerciais (particularmente na linha x86 clássica), Stallings destaca o circuito integrado Intel 8237A. Este componente atua como um controlador externo que assume temporariamente o papel de mestre do barramento do sistema. Para que a CPU delegue o controle, ela configura o 8237A através de registradores internos específicos mapeados em portas de E/S:

- **Command & Status Registers:** Controlam o modo de operação do chip e reportam o estado atual das transferências.
- **Current Address Register:** Armazena o endereço de memória atual de onde ou para onde os dados serão transferidos (um para cada um de seus 4 canais independentes).
- **Current Word Count Register:** Registra o número de transferências restantes, decrementando-se a cada ciclo.

A dinâmica de sinalização do 8237A ocorre em um protocolo de quatro etapas. Primeiramente, o periférico solicita o serviço ativando a linha *DMA Request* (DREQ). O controlador 8237A avalia a prioridade e ativa a linha *Hold* (HOLD) conectada diretamente à CPU. O processador central, ao concluir seu ciclo de barramento atual, responde ativando a linha *Hold Acknowledge* (HLDA) e colocando suas linhas de dados, endereço e controle em alta impedância (tri-state). A partir deste instante, o 8237A assume o controle total do barramento, gerando os endereços e os sinais de leitura/escrita para realizar o roubo de ciclo. Quando a contagem do registrador chega a zero, o controlador gera um sinal de *Terminal Count* (TC) e dispara uma interrupção para avisar a CPU que o bloco foi transferido com sucesso.

## 5. Acesso Direto à Cache (DCA) e engenharia de ultra-baixa latência

Em redes modernas de ultra-alta velocidade operando sob vazões de 40 Gbps, 100 Gbps ou 400 Gbps, o acesso contínuo à DRAM física como destino de DMA impõe um grande gargalo térmico e de latência para o barramento de sistema da CPU.

O DCA soluciona essa restrição ao permitir que os pacotes de dados de E/S provenientes de dispositivos PCIe contornem a DRAM principal e sejam injetados diretamente na cache de último nível (LLC - Last Level Cache/L3) compartilhada do processador.

```
Mecanismo de Escrita PCIe sob Intel DDIO (DCA Ativo):
+------------------------------------+
|  Interface Física PCIe Gen 5 / 6   |
+-----------------+------------------+
                  |
                  |  Gravação de Bloco (64 Bytes - Linha de Cache)
                  v
+-----------------+---------------------------------------------------+
|               COERÊNCIA DE CACHE E AGENTE DE ANEL                   |
+-----------------+---------------------------------------------------+
                  |
                  |-- Acerto de Cache (Cache Hit na L3)
                  |   --> Sobrescreve dados via Write-Update na L3.
                  |
                  +-- Falha de Cache (Cache Miss na L3)
                      --> Aloca dinamicamente linha em subconjunto
                          restrito de caminhos da L3 (Write-Allocate).
                  |
                  v
+-----------------+---------------------------------------------------+
|               CACHE DE ÚLTIMO NÍVEL (LLC / L3 COMPARTILHADA)       |
+---------------------------------------------------------------------+
                  |
                  +--- Despejo ou Write-Back posterior para DRAM
                  |
                  v
+-----------------+---------------------------------------------------+
|                 DRAM (Memória Principal Off-Chip)                   |
+---------------------------------------------------------------------+
```

### Arquitetura interna do Intel DDIO, Cache Pollution e tunagem

A implementação física mais proeminente da tecnologia DCA é a tecnologia *Intel Data Direct I/O* (Intel DDIO), inserida em nível de hardware nas famílias de processadores Xeon. O DDIO redefine o tráfego clássico de E/S, em que o controlador de interconexão integrada mapeia dinamicamente as regiões de cache L3 compartilhada como o destino primário para leituras e escritas das placas de interface de rede PCIe (NICs) e de armazenamento.

Quando um dispositivo PCIe inicia uma operação de escrita para host, o comportamento lógico é regido pelas regras de coerência de cache e alocação dinâmica da cache L3.

1. **Cenário de acerto de cache (PCIe Write Hit):** O endereço correspondente ao buffer de destino do driver já reside em uma linha de cache alocada na L3. A transação do barramento PCIe atualiza imediatamente a L3 sem acessar o barramento de DRAM. A documentação denomina esse fluxo como atualização de escrita (*Write Update*).
2. **Cenário de falha de cache (PCIe Write Miss):** O endereço físico de destino do buffer não está alocado em nenhum bloco de L3. Em vez de enviar os dados para a DRAM off-chip, o controlador de DDIO intercepta a transação e realiza de maneira proativa uma alocação de escrita (*Write Allocate*). A linha de dados de 64 bytes é gravada diretamente na cache L3 em um dos caminhos associativos previamente disponibilizados, marcando-a como modificada (*dirty*) em modo *write-back* sem atualizar a DRAM.

Isso demonstra grande vantagem quantitativa na latência de acesso.

$$
\tau_{L3} \approx 6,72\text{ ns} \quad (20\text{ ciclos de clock a } 3\text{ GHz}) \quad \ll \quad \tau_{DRAM} \approx 50\text{ a } 100\text{ ns}
$$

Apesar do ganho evidente de vazão, o DDIO pode induzir patologias severas em sistemas com tráfego de rede extremo (acima de 100 Gbps). A chamada poluição de cache (*Cache Pollution*) ocorre quando a chegada massiva de pacotes de rede sobrescreve bastante as linhas da cache L3, expulsando blocos de dados contendo variáveis de estado de processos de aplicação concorrentes de alta prioridade. O que resulta, pois, em falhas de cache sistemáticas da CPU ao retomar tarefas de processamento de dados, elevando as latências de cauda da aplicação em cerca de 30% sob taxas de 200 Gbps.

Para contornar esse efeito, o engenheiro de software deve adotar estratégias de tunagem avançadas, como:

- **Dimensionamento de buffers de anel:** Configurar tamanhos de anéis de descritores de pacotes inferiores à fração máxima de caminhos disponíveis reservados ao DDIO.
- **Particionamento físico de L3 via Intel Cache Allocation Technology (CAT):** Isolar e fixar de forma lógica faixas específicas de caminhos associativos de L3 para o controlador de E/S, blindando os núcleos de execução que lidam com a lógica computacional da aplicação.

### Evolução do Acesso à Cache em E/S

| **Aspecto de Engenharia** | **DMA Clássico (Sem DCA)** | **DCA Baseado em Pré-Busca (DCA Prefetch)** | **Intel DDIO (True DCA)** |
| --- | --- | --- | --- |
| **Destino de Escrita Primário** | Memória Principal RAM (DRAM). | Memória RAM acompanhada de envio de sinal ao barramento de cache. | Cache de Último Nível L3 diretamente. |
| **Mecanismo Operacional** | Acesso físico direto e controle de coerência via barramento do sistema. | Controlador de memória emite uma dica de pré-busca (*Prefetch Hint*) à CPU para antecipar a carga. | Alocação ativa (*Write-Allocate*) na L3 sem passar pela DRAM em falhas de cache. |
| **Acesso de Leitura da CPU** | Provoca falha de cache compulsória na L3; exige busca de dados em DRAM. | Reduz falhas na cache L3 caso o dado já tenha sido pré-carregado. | Acerto de cache absoluto na L3; latência reduzida a nível de nanossegundos. |
| **Vazão de DRAM** | Sobrecarga de barramento; dados trafegam continuamente na DRAM. | Parcialmente reduzida; leituras redundantes da CPU continuam ocorrendo se houver atraso na pré-busca. | Praticamente zero viagens à DRAM física nos cenários ideais. |

A engenharia de baixa latência em datacenters utiliza o Intel DDIO como base fundamental para o funcionamento de mecanismos de desvio de kernel como o DPDK (*Data Plane Development Kit*). O DPDK emprega drivers em laço contínuo (*Poll Mode Drivers* - PMDs) rodando em espaço de usuário sob núcleos de processadores dedicados. À medida que a placa de rede de alta velocidade injeta os pacotes de rede na cache L3 via DDIO, o PMD lê instantaneamente a carga útil sem qualquer interrupção de hardware ou chamada de sistema ao kernel, alcançando vazão de linha de 100 Gbps+.

## 6. Processadores e canais de E/S

Com a evolução das técnicas de processamento de E/S, a arquitetura dos computadores passou de controladores simples para o modelo de canais de E/S. O canal de E/S opera como um processador copartícipe autônomo e de propósito específico, dotado de seu próprio conjunto de instruções de manipulação de barramento especializado para operações de E/S.

A CPU primária não executa rotinas de E/S de baixo nível; em vez disso, ela inicializa o canal indicando a localização de um Programa de Canal (*Channel Program*) alocado na memória principal física do sistema e prossegue de forma paralela com as tarefas de processamento de alto nível.

```
                     ARQUITETURA DE MAINFRAME
+-------------------------------------------------------------+
|                         CPU Host                            |
+------------------------------+------------------------------+
                               |
                               | 1. Emite Instrução de Inicialização
                               |    (Aponta para o Channel Program na RAM)
                               v
+------------------------------+------------------------------+
|                    Memória RAM Principal                    |
|                                                             |
|  +-------------------------------------------------------+  |
|  |       Channel Program (Cadeia de Instruções CCW):     |  |
|  |  -> -> |  |
|  +-------------------------------------------------------+  |
+------------------------------+------------------------------+
                               ^
                               | 2. Busca e Executa Instruções CCW
                               v
+------------------------------+------------------------------+
|                         Canal de E/S                        |
+--------+-------------------------------------------+--------+
         |                                           |
         | Modo Seletor                              | Modo Multiplexador
         v                                           v
+--------+-----------+                      +--------+-----------+
|  Controlador E/S   |                      |  Controlador E/S   |
+--------+-----------+                      +--------+-----------+
         | (Dedicado a um                            | (Intercala bytes/blocos
         v  dispositivo de alta velocidade)          v  de vários periféricos)
+--------+-----------+                      +--------+-----------+
|    Fita / Disco    |                      | Impressoras / Term.|
+--------------------+                      +--------------------+
```

### Offloading e programas de canal

A arquitetura de canais de E/S exemplifica a ideia de descarregamento de processamento (*I/O Offloading*). Em computadores de grande porte de arquitetura IBM System/360 a zArchitecture modernos, a CPU não interage de forma direta com sinais de controle mecânicos, trilhas físicas de disco ou barramentos de rede.

O Programa de Canal é constituído por uma sequência lógica de Palavras de Comando de Canal (*Channel Command Words* - CCWs). Essas instruções instruem de forma exata o hardware do canal sobre quais setores ler, quais blocos varrer, onde alocar os dados de recebimento na memória principal e quais ações corretivas de hardware tomar em caso de falhas ou erros de verificação redundante cíclica (CRC).

Os canais organizam-se funcionalmente em duas grandes classes:

- **Canal seletor:** Dedica-se de forma exclusiva e ininterrupta à transferência de dados com um único dispositivo de alta velocidade a cada vez, controlando um pequeno cluster de controladores.
- **Canal multiplexador:** Capaz de gerenciar canais de dados com múltiplos dispositivos em paralelo. Apresenta-se nas variações de *Multiplexador de Byte* (para periféricos lentos como terminais analógicos ou leitores óticos de controle de fluxo de dados) e *Multiplexador de Bloco* (intercalando registros e blocos de dados completos em transações síncronas rápidas de múltiplos periféricos rápidos de armazenamento).

### Tipos de canais de E/S

| **Critério de Desempenho** | **Canal Seletor** | **Canal Multiplexador de Byte** | **Canal Multiplexador de Bloco** |
| --- | --- | --- | --- |
| **Alvo de Periféricos** | Dispositivos dedicados de alta velocidade. | Múltiplos dispositivos concorrentes de baixa velocidade. | Múltiplos dispositivos concorrentes de alta velocidade. |
| **Mecanismo de Multiplexação** | Monopólio físico do barramento de canal durante a transferência inteira. | Intercalação de bytes individuais das portas ativas. | Intercalação de blocos inteiros de dados originados em periféricos diferentes. |
| **Volume de Dados Típico** | Grandes rajadas contínuas de blocos físicos. | Transmissões de dados discretas e esparsas. | Grandes rajadas de dados estruturadas em múltiplos discos ou fitas. |
| **Eficiência de Barramento** | Moderada; o canal fica ocioso se o dispositivo tiver atrasos físicos. | Alta para periféricos lentos; barramento sempre ativo. | Máxima largura de banda aproveitada para múltiplos caminhos. |

Em datacenters corporativos que operam serviços bancários legados críticos sobre arquiteturas IBM Mainframe z14/z15/z16, todo o processamento de bancos de dados relacionais maciços (como DB2) é descarregado de forma automatizada para co-processadores dedicados chamados SAP (*System Assist Processors*), que executam milhares de instruções CCW em paralelo para transferir trilhas lógicas inteiras de matrizes de discos de armazenamento corporativo conectadas a canais de fibra para os buffers de memória física principal da máquina virtual, sem roubar nenhum ciclo computacional das CPUs principais dedicadas ao processamento transacional de negócios.

## 7. Padrões de interconexão externa e tecidos de rede de alta velocidade

Os barramentos de interconexão externa estabelecem as interfaces físicas, elétricas e de sinalização de dados que interligam os controladores internos aos dispositivos periféricos e equipamentos remotos. A evolução desses padrões migrou de barramentos paralelos compartilhados de curta distância, limitados fisicamente por capacitância e degradação eletromagnética de sinais elétricos, para a padronização de interfaces seriais baseadas em pacotes de alta frequência de transmissão e comutação inteligente em malha.

```
                     EVOLUÇÃO DOS TECIDOS DE CONECTIVIDADE
+-----------------------------------------------------------------------------+
|                               PCIe Gen 6                                    |
|   - Interface física e elétrica baseada em link serial ponto a ponto        |
|   - Codificação elétro-analógica PAM-4 com sinalização de 64 GT/s           |
+-------------------------------------+---------------------------------------+
                                      |
                                      | Camada de Transporte Física
                                      v
+-------------------------------------+---------------------------------------+
|                    COMPUTE EXPRESS LINK (CXL v3.1)                          |
|                                                                             |
|  +-----------------------+  +-----------------------+  +-----------------+  |
|  |        CXL.io         |  |       CXL.cache       |  |     CXL.mem     |  |
|  | - Transações normais  |  | - Acesso coerente     |  | - CPU acessa    |  |
|  |   de controle PCIe.   |  |   do acelerador à L3. |  |   RAM do acc.   |  |
|  +-----------------------+  +-----------------------+  +-----------------+  |
+-----------------------------------------------------------------------------+
```

### PAM-4, CXL protocols, InfiniBand Architecture e desagregação

Um dos mais modernos barramentos internos e periféricos são o *PCI Express Gen 6* e a tecnologia *Compute Express Link* (CXL). O PCIe Gen 6 nao faz uso da sinalização clássica baseada em dois níveis de tensão (NRZ - *Non-Return-to-Zero*) e adota a Modulação por Amplitude de Pulso de 4 Níveis (PAM-4). O PAM-4 modula dois bits lógicos em um único ciclo analógico de transmissão por par diferencial de cobre elétrico em frequências extremas, alcançando velocidades de 64 GT/s por via (*lane*) com o uso de Correção Antecipada de Erros (*Forward Error Correction* - FEC).

O *Compute Express Link* (CXL) opera de forma paralela sobre a infraestrutura física e analógica de links diferenciais do PCIe Gen 5 e Gen 6, mas introduz uma pilha de transação flexível baseada em sub-protocolos dinamicamente multiplexados em flits (unidades de controle de fluxo de dados de alta eficiência elétrico-lógica).

- **CXL.io:** Idêntico ao protocolo transacional clássico do PCIe, atuando na inicialização física, descoberta, mapeamento de memória em registradores de controle e tratamento clássico de DMA sem coerência nativa.
- **CXL.cache:** Permite que aceleradores de hardware periféricos acessem de forma coerente a memória do processador host, minimizando as latências de busca com mecanismos de consulta e invalidação ativa.
- **CXL.mem:** Possibilita que a CPU host trate a memória local de alta velocidade integrada ao acelerador (ex: HBM ou DRAM secundária) como se fosse parte integrante da memória física RAM de sistema, acessando-a por instruções nativas de *load/store*.

O CXL classifica os dispositivos em três categorias primárias:

- **Dispositivos tipo 1 (SmartNICs):** Não contam com memória local substancial; utilizam CXL.cache para processar dados de rede diretamente na cache do host.
- **Dispositivos tipo 2 (GPUs e FPGAs de alto desempenho):** Possuem sua própria memória HBM/GDDR e utilizam todos os três sub-protocolos para manter a coerência contínua entre a RAM do host e a memória local do acelerador.
- **Dispositivos tipo 3 (expansores de memória):** Módulos que disponibilizam bancos adicionais de memória DDR5 volátil ou não volátil à CPU conectada via barramento CXL.mem, permitindo o pooling dinâmico e o compartilhamento de memória física entre múltiplos hosts em arquiteturas de computação desagregada.

Em paralelo, a tecnologia *InfiniBand* destaca-se como o tecido de rede de alta velocidade por excelência para computação científica e redes de inteligência artificial. Operando sobre arquiteturas redundantes de comutação baseada em malhas inteligentes e controle de fluxo baseado em créditos, o InfiniBand suporta taxas latências de sub-microssegundos de transporte e canais nativos de RDMA de alta vazão, eliminando a sobrecarga computacional de processamento das pilhas TCP/IP clássicas do sistema operacional.

### Barramentos e tecidos de conectividade de alto desempenho

| **Padrão de Conectividade** | **Meio Físico Primário** | **Largura de Banda Unidirecional Máxima (Típica)** | **Tipo de Sinalização / Codificação** | **Principais Sub-Protocolos Ativos** | **Cenário de Uso Corporativo** |
| --- | --- | --- | --- | --- | --- |
| **PCIe Gen 6** | Par diferencial elétrico curto / Fibra óptica emergente. | Até 128 GB/s (em modo x16 links físicos). | PAM-4 (Modulação de 4 níveis) com FEC. | Transações de leitura/escrita não-coerentes baseadas em TLP. | Conectividade física de SSDs NVMe e placas aceleradoras. |
| **CXL v3.1** | Infraestrutura física compartilhada do PCIe Gen 5/6. | Até 256 GB/s (link x16 PCIe Gen 6). | PAM-4 / Flit encapsulation de alta eficiência. | CXL.io, CXL.cache e CXL.mem multiplexados. | Pooling dinâmico de RAM de alta capacidade e conexões de aceleradores. |
| **InfiniBand NDR** | Cabos de cobre elétricos ativos (DAC) ou transceptores de fibra óptica. | Até 400 Gbps por via de conexão física. | Sinalização óptica coerente de alta velocidade baseada em transações de crédito. | Protocolos proprietários InfiniBand de transporte nativo. | Interconexão de clusters de GPU e redes de IA de alto rendimento. |
| **Ethernet 400G** | Cabos de fibra óptica multimodo ou cabos de cobre elétricos. | Até 400 Gbps por canal físico de rede. | Modulação PAM-4 em múltiplos canais multiplexados de fibra. | Pilhas clássicas de enlace e rede Ethernet (IEEE 802.3). | Comunicação inter-rack de longa distância e backbone de internet. |

### Padrões de conectividade de uso geral e periféricos de consumo

Enquanto soluções metalógicas como CXL e malhas InfiniBand imperam no ecossistema de alto desempenho de data centers, o modelo clássico de E/S consolida padrões universais voltados ao mercado consumidor e redes locais de computadores.

- **Universal Serial Bus (USB):** Desenvolvido para mitigar a proliferação de portas dedicadas (seriais e paralelas), o USB evoluiu para uma arquitetura serial assimétrica assíncrona baseada em uma topologia em árvore com hubs. A partir da especificação USB 3.0 (*SuperSpeed*), introduziu o modo de transmissão *Full-Duplex* com codificação 8b/10b, atingindo taxas nominais de 5 Gbps e incorporando pacotes de controle de fluxo para gerenciamento eficiente de energia.
- **FireWire (IEEE 1394):** Diferencia-se historicamente por sua arquitetura orientada a processamento distribuído com topologia em encadeamento (*daisy-chain*). Não exige um *host* centralizado (CPU) ativo para arbitrar a comunicação, permitindo que dois periféricos (como câmeras e storages) troquem dados diretamente entre si.
- **Thunderbolt:** Desenvolvido como uma interface de altíssima velocidade que funde os protocolos PCI Express e DisplayPort em um único link serial meta-protocolo de baixa latência, permitindo o tráfego concorrente de dados brutos e streams de vídeo de alta definição através de multiplexação por divisão de tempo.
- **Serial ATA (SATA):** Substituiu o barramento paralelo IDE/PATA. Adota uma arquitetura ponto a ponto pura com sinalização diferencial e cabos seriais finos, eliminando problemas de *skew* (desalinhamento de clock entre linhas paralelas) e otimizando a taxa de transferência de unidades de armazenamento magnético e de estado sólido (SSD) legados.
- **Interfaces de rede (Ethernet e Wi-Fi):** Representam os módulos de E/S de comunicação a longa distância. A interface Ethernet (IEEE 802.3) implementa o controle de acesso ao meio físico cabeado por meio de pacotes estruturados e detecção de colisões/comutação. Já o padrão Wi-Fi (IEEE 802.11) traduz os fluxos digitais do subsistema de E/S em portadoras de radiofrequência, gerenciando o meio compartilhado via mecanismos de prevenção de colisão (CSMA/CA) diretamente na camada física e de enlace do módulo de rede.

---

Interessante acrescentar que a computação de alto desempenho em nuvem e servidores dedicados à inteligência artificial generativa dependem diretamente do InfiniBand. Em clusters de supercomputadores compostos por nós NVIDIA DGX dotados de GPUs H100 ou B200, múltiplas placas de rede ConnectX InfiniBand transferem matrizes de parâmetros matemáticos de pesos de redes neurais diretamente entre as memórias de alta velocidade das GPUs de servidores fisicamente distintos através do barramento de rede InfiniBand sem envolver o sistema operacional, mitigando qualquer latência do host.

## 8. Estrutura de E/S de alto desempenho - IBM zEnterprise EC12

O IBM zEnterprise EC12 é um computador de grande porte (*mainframe*) que emprega uma arquitetura de E/S dedicada de escala alta projetada para eliminar por completo as penalidades de processamento e latência de barramento dos processadores principais.

O zEC12 adota o conceito de subsistema de canais dedicados (CSS - *Channel Subsystem*), descarregando as tarefas para Processadores de Assistência de Sistema (SAP) especializados e isolando as configurações de roteamento de hardware na Área de Sistema de Hardware (HSA) de 32 GB integrada à RAM nativa.

```
                IBM zENTERPRISE EC12 I/O SYSTEM
+-------------------------------------------------------------+
|               Gaiola de Processadores Primários             |
|                                                             |
|  +------------------------+     +------------------------+  |
|  |     Processor Book     |     |     Processor Book     |  |
|  |  +------------------+  |     |  +------------------+  |  |
|  |  |    Active SAP    |  |     |  |    Active SAP    |  |  |
|  |  +--------+---------+  |     |  +--------+---------+  |  |
|  +-----------|------------+     +-----------|------------+  |
+--------------|------------------------------|---------------+
               | InfiniBand                   | PCIe
               | Fanout                       | Fanout
               v                              v
+--------------+------------------------------+---------------+
|                Mecanismo de Fanouts / Comutadores           |
+--------------+------------------------------+---------------+
               |                              |
               v                              v
+--------------+-------------+    +-----------+---------------+
| Gaiola de E/S / I/O Drawer |    | I/O Drawer PCIe           |
|                              |                              |
|  +-----------------------+  |    |  +--------------------+  |
|  | Multiplexador ESCON   |  |    |  | Comutador PCIe     |  |
|  +-----------+-----------+  |    |  +--------+-----------+  |
|              |              |    |           |              |
|              v              |    |           v              |
|  +-----------+-----------+  |    |  +--------+-----------+  |
|  | Fita / Armaz. de Fibra|  |    |  | Canal de Fibra 16G |  |
|  +-----------------------+  |    |  +--------------------+  |
+-----------------------------+    +--------------------------+
```

### Subsistemas de canal, HSA, Fanouts e resiliência física

O subsistema de E/S do zEnterprise EC12 se baseia no isolamento total do fluxo de dados. Dos até 96 núcleos de processadores de alto desempenho executando a 5,5 GHz contidos nos módulos multichip (MCM) dos livros (*books*) de processadores, porções selecionadas são reservadas e configuradas como processadores SAP dedicados à coordenação de E/S. O SAP assume a responsabilidade de executar a varredura e gerenciar a fila de solicitações lógicas de E/S, liberando as CPUs primárias para o processamento exclusivo da lógica de código das aplicações.

A arquitetura lógica de E/S do zEC12 é configurada por meio de quatro componentes principais:

1. **Partições Lógicas (LPARs):** Instâncias de virtualização nativas implementadas diretamente no nível do firmware de hardware de controle, permitindo isolar múltiplos sistemas operacionais independentes sem perda de desempenho.
2. **Área de Sistema de Hardware (HSA):** Uma porção fixa e reservada de 32 GB de memória RAM rápida não volátil do sistema de acesso restrito aos processadores de assistência SAP. A HSA armazena a tabela de configuração física de E/S (IOCDS) do mainframe, assegurando que modificações de caminhos de canal e adição ou remoção de periféricos físicos de hardware ocorram sob o sistema em plena operação (*Dynamic I/O Reconfiguration*) sem exigir reinicializações planejadas.
3. **Subcanais:** Abstração de software que representa cada dispositivo de E/S de forma lógica na partição do sistema operacional, armazenando o estado atual, estatísticas e filas lógicas de acesso (suportando até 196 mil subcanais ativos).
4. **Caminhos de Canal (*Channel Paths*):** Interface de transmissão síncrona exclusiva de alta velocidade que une o subsistema de canais aos controladores externos físicos. Cada CSS suporta até 256 caminhos de canais independentes gerenciados por processadores de canal de menor porte.

No nível físico e estrutural, a integração física das gaiolas de processadores do zEC12 com as gaiolas de E/S instaladas de fábrica e gavetas de E/S (*I/O Drawers*) PCIe intercambiáveis é feita através de cartões controladores dedicados denominados *fanouts*. Cada livro de processadores suporta conectores redundantes contendo até 8 adaptadores de canal do host (HCA) InfiniBand para gaiolas clássicas legadas que utilizam fibra proprietária ESCON, e conexões estruturadas sobre fanouts PCIe Gen 3 acoplados a barramentos de interconexão rápida para cartões de fibra óptica corporativos de alta vazão.

### Elementos lógicos vs. físicos no zEnterprise EC12

| **Componente de E/S** | **Categoria Estrutural** | **Função Primária no Subsistema** | **Tipo de Interface Associada** | **Limite Físico ou Capacidade** |
| --- | --- | --- | --- | --- |
| **SAP (System Assist Processor)** | Unidade de processamento física. | Coordenação, gerenciamento e priorização das filas físicas de canais. | Coprocessador dedicado na pastilha de silício (MCM). | Até 4 chips por subsistema de canal de host. |
| **HSA (Hardware System Area)** | Memória física dedicada. | Armazenamento dinâmico das tabelas lógicas de alocação de dispositivos. | Bloco de 32 GB reservado da memória total do mainframe. | 32 GB fixos e isolados do espaço de endereço dos consumidores. |
| **Subcanal** | Abstração lógica de software. | Fornece aos programas em execução a representação do periférico lógico. | Registro em tabelas de memória virtual mapeado dinamicamente. | Suporte nativo a até 196k subcanais por CSS. |
| **Fanout Adaptador (HCA / PCIe)** | Palca controladora de hardware. | Interconexão síncrona de alta frequência do book com a gaiola de E/S. | Links proprietários InfiniBand ou barramento PCI Express direto. | Suporta até 32 conexões independentes por adaptador. |
| **Gaveta de E/S (I/O Drawer)** | Unidade física estrutural. | Acomoda fisicamente os multiplexadores e canais periféricos adicionais. | Gavetas horizontais compactas e intercambiáveis "a quente". | Alocação modular variável sob demanda do cliente. |

A resiliência de mainframes zEnterprise EC12 é empregada de forma ampla no setor financeiro de processamento de cartões de crédito globais (como a Visa ou Mastercard) e sistemas centrais de bancos corporativos.

Enquanto os processadores de processamento principal lidam com a criptografia e processamento de consultas lógicas de contas, o subsistema de E/S direciona de forma ininterrupta e transparente as buscas de dados necessárias nas matrizes de disco remotas via canais de fibra. Gerenciando, assim, falhas físicas em links ópticos instantaneamente ao comutar o tráfego de dados do barramento por caminhos de canal redundantes mapeados na HSA; mantendo os sistemas funcionando sem interrupção de transações ou degradação na latência.

## Referências Bibliográficas

BEN-YEHUDA, Muli *et al*. The Price of Safety: Evaluating IOMMU Performance. *In*: OTTAWA LINUX SYMPOSIUM, 2007, Ottawa. **Proceedings...** Ottawa: [s.n.], 2007. p. 9-20.

COMPUTE EXPRESS LINK CONSORTIUM. **Compute Express Link (CXL) Specification: Revision 3.1**. Beaverton: CXL Consortium, 2023.

IBM. **IBM zEnterprise EC12 Technical Guide**. Poughkeepsie: IBM Redbooks, 2013. (SG24-8050).

INFINIBAND TRADE ASSOCIATION. **InfiniBand Architecture Specification Volume 1: Release 1.6**. [S. l.]: IBTA, 2023.

INTEL CORPORATION. **Intel Data Direct I/O Technology (Intel DDIO): A Primer**. [S. l.]: Intel Corporation, 2012. (Technology Brief).

PATTERSON, David A.; HENNESSY, John L. **Computer Organization and Design: The Hardware/Software Interface**. 5. ed. Waltham: Morgan Kaufmann, 2013.

PCI-SIG. **PCI Express Base Specification: Revision 6.0**. Beaverton: PCI-SIG, 2022.

STALLINGS, William. **Arquitetura e organização de computadores**. 10. ed. Tradução de Sérgio Nascimento. Revisão técnica de Ricardo Pannain. São Paulo: Pearson Education do Brasil, 2017.

TANENBAUM, Andrew S. **Structured Computer Organization**. 6. ed. Upper Saddle River: Pearson, 2012.
