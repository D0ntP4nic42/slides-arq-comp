---
title: "Sistemas de Entrada/Saída"
sub_title: "Cap. 7 — Organização de Computadores"
authors:
  - Karoline Costa
  - Leonardo Brito
  - Luiz Gustavo
theme:
  path: themes/solarized-light.yaml
---

Glossário
=========

- **Barramento** → Canal físico passivo que transporta dados, endereços e sinais de controle entre CPU, memória e módulos de E/S. Não armazena nada.

- **Buffer** → Registrador temporário no módulo de E/S que resolve o descasamento de velocidades entre periféricos lentos e barramento rápido.

- **Módulo de E/S** → Intermediário lógico entre CPU e periféricos. Controla temporização, comunicação, buffering e detecção de erros.

- **Transdutor** → Componente que converte dados entre forma elétrica e outras formas de energia (ex: elétrico → luz no monitor).

- **Polling** → CPU verifica repetidamente um bit de estado (*READY/BUSY*) até o periférico estar pronto. Consome ciclos ociosamente.

- **Cycle Stealing** → DMA "rouba" um ciclo de barramento por vez, suspendendo a CPU momentaneamente sem salvar contexto.

<!-- end_slide -->

Evolução da Função de E/S
=========================

Módulos de E/S formam o **terceiro pilar da arquitetura de computadores**, ao lado da CPU e da memória. Conectar periféricos diretamente ao barramento é inviável: velocidades, formatos e métodos operacionais são incompatíveis.

A taxonomia de Stallings descreve como a responsabilidade foi progressivamente transferida da CPU para módulos especializados:

1. **Controle direto pela CPU** — processador gerencia toda lógica de temporização e amostragem de dados

2. **Módulo de E/S sem interrupções** — hardware gerencia o periférico, mas CPU faz *polling* do estado

3. **E/S por interrupção** — módulo sinaliza a CPU apenas quando dados estão prontos, eliminando espera ociosa

4. **DMA (Direct Memory Access)** — módulo transfere blocos entre periférico e memória; CPU só intervém no início e no fim

5. **Canais de E/S** — processador de propósito específico com conjunto de instruções próprio

6. **Processadores de E/S autônomos** — memória local dedicada, opera como sistema independente

<!-- end_slide -->

Arquitetura de um Módulo de E/S
==============================

```
+-------------------------------------------------------------------------+
|                          BARRAMENTO DO SISTEMA                          |
+---+------------------------------+------------------------------+-------+
    |                              |                              |
    Dados                       Endereços                       Controle
    |                              |                              |
+---+------------------------------+------------------------------+-------+
|                              MÓDULO DE E/S                              |
|                                                                         |
|  +--------------------+  +--------------------+  +--------------------+ |
|  | Reg. Dados Interno |  | Reg. Estado/Contr. |  | Lógica de Interface| |
|  +--------------------+  +--------------------+  +--------------------+ |
|           ^                         ^                         ^         |
|           |                         |                         |         |
|           +----------+--------------+                         |         |
|                      |                                        |         |
+----------------------+----------------------------------------+---------+
                       |
            +----------+----------+
            |  Sinais de E/S:     |
            |  Dados, Estado      |
            |  e Controle         |
            +----------+----------+
                       |
+----------------------v----------------------------------------------------+
|                          DISPOSITIVO PERIFÉRICO                           |
|                                                                           |
|  +--------------------+  +--------------------+  +--------------------+   |
|  | Lógica de Controle |  |  Buffer de Dados   |  |     Transdutor     |   |
|  +--------------------+  +--------------------+  +--------------------+   |
+---------------------------------------------------------------------------+
```

<!-- end_slide -->

Cinco Funções Nucleares do Módulo de E/S
========================================

De acordo com a taxonomia de Stallings, todo módulo de E/S deve desempenhar cinco funções obrigatórias:

1. **Controle e temporização**

2. **Comunicação com a CPU**

3. **Comunicação com o dispositivo externo**

4. **Buffering de dados**

5. **Detecção de erros**

<!-- end_slide -->

Dispositivos Externos: Tipos e Características
==============================================

Os periféricos são classificados pelo **alvo da informação** e pela **natureza da transdução**:

| Tipo | Alvo | Taxa de Dados | Latência | Exemplos |
| --- | --- | --- | --- | --- |
| **Inteligível ao humano** | Usuário final | Baixa (Bps a KBps) | Alta (percepção humana) | Teclado, monitor, display |
| **Inteligível à máquina** | Controladores | Alta (MBps a GBps) | Crítica (física do meio) | HDD, SSD NVMe, sensores |
| **Comunicação** | Redes/sistemas remotos | Ultra-alta (Gbps+) | Baixa e crítica | Ethernet, Wi-Fi 7, óptica |

**Dois padrões de operação:**

- **Fluxo de caracteres:** usado por dispositivos humanos (ex: teclado envia códigos ASCII por pressionamento de tecla).
- **Transdução em blocos:** usada por dispositivos de máquina (ex: disco lê/egrava setores inteiros, exigindo buffers e ECC).

<!-- end_slide -->

Por que Buffering é Necessário?
===============================

A **CPU e a memória principal operam em velocidades muito superiores** à maioria dos periféricos.

Sem buffer, a CPU ficaria presa esperando o dispositivo liberar ou entregar cada byte, desperdiçando ciclos.

```
Periférico lento          Buffer no módulo de E/S          Barramento rápido
    ||                              ||                              ||
    ||  dados em pequenas doses     ||  dados acumulados em blocos  ||
    ||  --------------------------> ||  --------------------------> ||
    ||        KBps a MBps           ||         MBps a GBps          ||
```

**Função do buffer:**

- **Acumular dados** vindos do periférico antes de enviá-los ao barramento.
- **Absorver diferenças de velocidade** entre dispositivos lentos e o sistema rápido.
- **Liberar a CPU** para outras tarefas enquanto o buffer é preenchido.

Em sistemas modernos, o buffering evoluiu para **filas FIFO em silício** e **controle de fluxo por créditos**, evitando que grandes blocos de dados do barramento saturem o transdutor do dispositivo.

<!-- end_slide -->

E/S Programada e Mapeamento de Endereços
========================================

Na **E/S programada**, a CPU transfere dados diretamente para o módulo de E/S e fica em um laço verificando o bit **READY/BUSY** até que o dispositivo esteja pronto.

Existem duas formas de acessar os registradores do módulo de E/S:

| Característica | MMIO (*Memory-Mapped I/O*) | Isolated I/O |
| --- | --- | --- |
| Endereço | Mesmo espaço da RAM | Espaço de E/S separado |
| Instruções | Normais (`MOV`, `LDR`) | Especiais (`IN`, `OUT` no x86) |
| Uso comum | ARM, RISC-V | x86 legado |

No **MMIO**, os registradores de E/S são tratados como posições de memória, mas devem ser marcados como **não-cacheáveis** para evitar leituras de valores desatualizados.

<!-- end_slide -->

Por que MMIO Precisa Ser Não-Cacheável?
========================================

A CPU pode cachear registradores de E/S, mas eles mudam o tempo todo. Se forem cacheáveis:

- **Leitura desatualizada:** a CPU lê o valor antigo da cache, ignorando a atualização do dispositivo.
- **Escrita atrasada:** a escrita fica presa na cache (*write-back*) e não chega ao hardware.

**Solução:** marcar MMIO como **Uncacheable** e **Strongly Ordered**, forçando a CPU a acessar o registrador real diretamente.

<!-- end_slide -->
