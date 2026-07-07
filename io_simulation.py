#!/usr/bin/env python3
"""
Simulação visual dos modos de Entrada/Saída (Cap. 7 — Stallings)
Usa Textual (TUI sem flicker, tema solarized-light) para mostrar 6 cenários:

  1. E/S Programada (Polling)   — CPU bloqueia em laço READY/BUSY
  2. E/S com Threads            — CPU faz outra tarefa; thread sinaliza ao fim
  3. E/S Assíncrona (asyncio)   — task com callback (interrupção simulada)
  4. Buffering                   — dispositivo envia em doses; buffer acumula
  5. Multiprocessing            — múltiplos dispositivos em paralelo (GIL-free)
  6. DMA simulado               — cópia direta memória↔periférico; CPU livre

Controles:
  ← / →   navegar entre cenários
  espaço  reiniciar cenário atual
  p       pausar/continuar
  q       sair
"""

import time
from collections import defaultdict

from rich.text import Text
from rich.style import Style
from rich.table import Table

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.widgets import Header, Footer, Static, RichLog

# Solarized light palette (cores explícitas para o Gantt)
SOL = {
    "bg":     "#fdf6e3",   # base3
    "bg2":    "#eee8d5",   # base2
    "fg":     "#586e75",
    "green":  "#859900",
    "red":    "#dc322f",
    "yellow": "#b58900",
    "blue":   "#268bd2",
    "magenta": "#d33682",
    "orange": "#cb4b16",
}

# ---------------------------------------------------------------------------
# Estados
# ---------------------------------------------------------------------------
C_WORK = "WORK"; C_WAIT = "WAIT"; C_OTHER = "OTHER"; C_IDLE = "IDLE"
D_TRANSFER = "TRANSFER"; D_IDLE = "IDLE"

CPU_BG = {C_WORK: SOL["green"], C_WAIT: SOL["red"],
           C_OTHER: SOL["yellow"], C_IDLE: SOL["bg2"]}
CPU_FG = {C_WORK: SOL["green"], C_WAIT: SOL["red"],
           C_OTHER: SOL["yellow"], C_IDLE: SOL["fg"]}
DEV_BG = {D_TRANSFER: SOL["blue"], D_IDLE: SOL["bg2"]}
CPU_DESC = {C_WORK: "processando", C_WAIT: "bloqueada (polling)",
             C_OTHER: "outra tarefa", C_IDLE: "ociosa"}
BUF_MAX = 8
BLOCK = " ▁▂▃▄▅▆▇█"

# Velocidade: ms virtual por tick
TICK_MS = 20

# ---------------------------------------------------------------------------
# Cenários
# ---------------------------------------------------------------------------

def scenario_polling():
    ev = [(0, "cpu", C_WAIT, "READ"), (0, "dev", D_TRANSFER, "transferindo")]
    for i in range(1, 19):
        ev.append((i * 50, "cpu", C_WAIT, f"poll {i}"))
    ev += [(900, "dev", D_IDLE, "done"), (900, "cpu", C_WORK, "processa"),
           (1200, "cpu", C_IDLE, "fim")]
    return ev, 1300

def scenario_threaded():
    ev = [(0, "cpu", C_OTHER, "dispara thread"), (0, "dev", D_TRANSFER, "thread: I/O"),
          (300, "cpu", C_OTHER, "computando"), (600, "cpu", C_OTHER, "processando"),
          (900, "dev", D_IDLE, "Event.set"), (900, "cpu", C_WORK, "processa"),
          (1100, "cpu", C_IDLE, "fim")]
    return ev, 1300

def scenario_async():
    ev = [(0, "cpu", C_OTHER, "await io_task()"), (0, "dev", D_TRANSFER, "task: I/O"),
          (300, "cpu", C_OTHER, "outras corrotinas"), (600, "cpu", C_OTHER, "await..."),
          (900, "dev", D_IDLE, "callback"), (900, "cpu", C_WORK, "processa"),
          (1100, "cpu", C_IDLE, "fim")]
    return ev, 1300

def scenario_buffering():
    ev = [(0, "cpu", C_OTHER, "configura buffer")]
    for i in range(1, 6):
        ev.append((i * 200, "dev", D_TRANSFER, f"dose {i}"))
        ev.append((i * 200, "buf", i, f"buffer={i}/5"))
        ev.append((i * 200 + 1, "dev", D_IDLE, ""))
    ev += [(1000, "cpu", C_WORK, "buffer cheio — processa"),
           (1000, "buf", 0, "esvaziado"), (1300, "cpu", C_IDLE, "fim")]
    return ev, 1500

def scenario_multiprocessing():
    ev = [(0, "cpu", C_OTHER, "3 processos paralelos")]
    for i in range(1, 4):
        ev.append((0, f"dev{i}", D_TRANSFER, f"proc{i}"))
    ev += [(900, "dev1", D_IDLE, "proc1 done"), (1100, "dev2", D_IDLE, "proc2 done"),
           (1300, "dev3", D_IDLE, "proc3 done"),
           (1300, "cpu", C_WORK, "agrega"), (1500, "cpu", C_IDLE, "fim")]
    return ev, 1700

def scenario_dma():
    ev = [(0, "cpu", C_OTHER, "configura DMA"), (0, "dev", D_TRANSFER, "DMA ativo"),
          (300, "buf", 2, "bloco..."), (600, "buf", 4, "parcial"),
          (800, "buf", 6, "final"), (900, "dev", D_IDLE, "TC + IRQ"),
          (900, "cpu", C_WORK, "processa"), (1100, "cpu", C_IDLE, "fim")]
    return ev, 1300

SCENARIOS = [
    ("1. E/S Programada (Polling)", scenario_polling,
     "CPU emite comando e fica presa em laço testando READY/BUSY. Ineficiente: desperdiça ciclos."),
    ("2. E/S com Threads", scenario_threaded,
     "CPU dispara thread de E/S e faz outra tarefa. Thread sinaliza (interrupção) ao terminar."),
    ("3. E/S Assíncrona (asyncio)", scenario_async,
     "asyncio: task de E/S roda assíncrona; CPU continua em outras corrotinas até callback."),
    ("4. Buffering", scenario_buffering,
     "Dispositivo lento envia doses; buffer acumula. CPU só processa quando o bloco está cheio."),
    ("5. Multiprocessing", scenario_multiprocessing,
     "3 dispositivos em paralelo, cada um num processo próprio (GIL-free). CPU agrega ao fim."),
    ("6. DMA simulado", scenario_dma,
     "Controlador transfere direto memória↔periférico. CPU fica livre até receber IRQ final."),
]

# ---------------------------------------------------------------------------
# Mundo
# ---------------------------------------------------------------------------

class World:
    def __init__(self, events, duration_ms):
        self.events = sorted(events, key=lambda e: e[0])
        self.duration_ms = duration_ms
        self.idx = 0; self.t_now = 0
        self.cpu = C_IDLE; self.dev = {}; self.buf = 0
        self.last_label = ""
        self.history = defaultdict(list)
        self.event_log = []

    def reset(self):
        self.idx = 0; self.t_now = 0; self.cpu = C_IDLE
        self.dev.clear(); self.buf = 0; self.last_label = ""
        self.history.clear(); self.event_log.clear()

    def advance(self, dt):
        end = self.t_now + dt
        while self.idx < len(self.events) and self.events[self.idx][0] <= end:
            t, e, s, lbl = self.events[self.idx]
            if e == "cpu": self.cpu = s
            elif e.startswith("dev"): self.dev[e] = s
            elif e == "buf": self.buf = s
            self.history[e].append((t, s))
            if lbl:
                self.last_label = lbl
                self.event_log.append((t, lbl))
            self.idx += 1
        self.t_now = min(end, self.duration_ms)


def _state_at(hist, t, default=None):
    s = default
    for (tt, st) in hist:
        if tt <= t: s = st
        else: break
    return s


# ---------------------------------------------------------------------------
# Barras Gantt (rich Text)
# ---------------------------------------------------------------------------

def make_bar(history, t_now, dur, width, bg_map, default_state, is_buf=False):
    bar = Text()
    hist = history
    for i in range(width):
        t = (i + 0.5) / width * dur
        if t > t_now:
            bar.append(" ", Style(bgcolor=SOL["bg"]))
        elif is_buf:
            lvl = _state_at(hist, t, 0) or 0
            ci = min(lvl, BUF_MAX) * (len(BLOCK) - 1) // BUF_MAX
            bar.append(BLOCK[ci], Style(color=SOL["magenta"], bgcolor=SOL["bg2"]))
        else:
            s = _state_at(hist, t, default_state)
            bar.append(" ", Style(bgcolor=bg_map.get(s, SOL["bg2"])))
    return bar


def dev_bar_combined(world, t_now, dur, width):
    hists = [h for k, h in world.history.items() if k.startswith("dev")]
    bar = Text()
    for i in range(width):
        t = (i + 0.5) / width * dur
        if t > t_now:
            bar.append(" ", Style(bgcolor=SOL["bg"]))
        else:
            active = any(_state_at(h, t, D_IDLE) == D_TRANSFER for h in hists)
            col = DEV_BG[D_TRANSFER] if active else DEV_BG[D_IDLE]
            bar.append(" ", Style(bgcolor=col))
    return bar


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

LEGEND = Text.assemble(
    ("■ ", Style(color=SOL["green"])),  ("CPU processando    ", {}),
    ("■ ", Style(color=SOL["red"])),    ("CPU bloqueada      ", {}),
    ("■ ", Style(color=SOL["yellow"])), ("CPU outra tarefa   ", {}),
    ("■ ", Style(color=SOL["blue"])),   ("DES transferindo   ", {}),
    ("■ ", Style(color=SOL["magenta"])),("BUF nível", {}),
)


class IOSim(App):
    TITLE = "Simulação de E/S — Cap. 7"
    theme = "solarized-light"

    BINDINGS = [
        Binding("left", "prev", "Anterior"),
        Binding("right", "next", "Próximo"),
        Binding("space", "restart", "Reiniciar"),
        Binding("p", "pause", "Pausar"),
        Binding("q", "quit", "Sair"),
    ]

    def __init__(self):
        super().__init__()
        self.scenario_idx = 0
        self.world = None
        self.paused = False

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical():
            yield Static("", id="title")
            yield Static("", id="summary")
            yield Static("", id="timeline")
            yield Static("", id="status")
            yield Static(LEGEND, id="legend")
            yield RichLog(id="log", markup=False, highlight=False, wrap=True, max_lines=200)
        yield Footer()

    def on_mount(self) -> None:
        self._load()
        self.set_interval(0.1, self._tick)   # 100ms real por tick

    def _load(self):
        _name, fn, _sum = SCENARIOS[self.scenario_idx]
        ev, dur = fn()
        self.world = World(ev, dur)
        self._logged = 0
        try:
            self.query_one("#log", RichLog).clear()
        except Exception:
            pass

    def _tick(self):
        if not self.paused and self.world.t_now < self.world.duration_ms:
            self.world.advance(TICK_MS)
        self._render()

    def _render(self):
        w = self.size.width
        bar_w = max(20, min(70, w - 10))
        dur = self.world.duration_ms
        t_now = self.world.t_now
        prog = t_now / dur if dur else 0

        name, _fn, summary = SCENARIOS[self.scenario_idx]
        flag = " [PAUSADO]" if self.paused else ""
        if t_now >= dur:
            flag += " [CONCLUIDO]"
        filled = int(prog * 20)
        pbar = "#" * filled + "-" * (20 - filled)
        header = Text.assemble(
            (name + "\n", Style(color=SOL["orange"], bold=True)),
            (f"t = {t_now:4d} / {dur} ms  [{pbar}] {int(prog*100):3d}%{flag}",
             Style(color=SOL["fg"])),
        )
        self.query_one("#title", Static).update(header)
        self.query_one("#summary", Static).update(
            Text(summary, Style(color=SOL["fg"], italic=True))
        )

        # barras
        cpu = make_bar(self.world.history.get("cpu", []), t_now, dur, bar_w,
                       CPU_BG, C_IDLE)
        dev = dev_bar_combined(self.world, t_now, dur, bar_w)
        buf = make_bar(self.world.history.get("buf", []), t_now, dur, bar_w,
                       {}, 0, is_buf=True)

        grid = Table.grid(padding=(0, 1))
        grid.add_column(justify="right", width=4, no_wrap=True)
        grid.add_column(no_wrap=True)
        grid.add_row(Text("CPU", style=Style(color=SOL["fg"], bold=True)), cpu)
        grid.add_row(Text("DES", style=Style(color=SOL["fg"], bold=True)), dev)
        grid.add_row(Text("BUF", style=Style(color=SOL["fg"], bold=True)), buf)
        cur = int(prog * bar_w)
        marker = Text.assemble((" " * (5 + cur), {}), ("▼", Style(color=SOL["orange"], bold=True)))
        grid.add_row(Text(""), marker)
        self.query_one("#timeline", Static).update(grid)

        # status compacto (uma linha)
        n = len(self.world.dev) or 1
        act = sum(1 for s in self.world.dev.values() if s == D_TRANSFER) if self.world.dev else 0
        st = Text.assemble(
            ("CPU: ", {}), (CPU_DESC[self.world.cpu], Style(color=CPU_FG[self.world.cpu], bold=True)),
            ("   DES: ", {}), (f"{act}/{n} ativo(s)", Style(color=SOL["blue"])),
            ("   BUF: ", {}), (f"{self.world.buf}/{BUF_MAX}", Style(color=SOL["magenta"])),
        )
        if self.world.last_label:
            st.append(f"   → {self.world.last_label}", Style(color=SOL["fg"], italic=True))
        self.query_one("#status", Static).update(st)

        # log de eventos
        log = self.query_one("#log", RichLog)
        while self._logged < len(self.world.event_log):
            t_ms, label = self.world.event_log[self._logged]
            line = Text(f"{t_ms:4d}ms  {label}",
                        style=Style(color=SOL["fg"]))
            log.write(line)
            self._logged += 1

    def action_prev(self):
        self.scenario_idx = (self.scenario_idx - 1) % len(SCENARIOS)
        self.paused = False; self._load()

    def action_next(self):
        self.scenario_idx = (self.scenario_idx + 1) % len(SCENARIOS)
        self.paused = False; self._load()

    def action_restart(self):
        self.paused = False; self._load()

    def action_pause(self):
        self.paused = not self.paused


def run():
    IOSim().run()


if __name__ == "__main__":
    run()