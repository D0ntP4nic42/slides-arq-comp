#!/usr/bin/env python3
"""
Corrida: Async vs Sync — Cap. 7 (E/S controlada)

Analogia: dois carros 🏎️ correm numa pista de 5000m.
Cada um precisa processar 5000 dados para chegar ao fim.
A cada IO_INTERVAL dados, ambos fazem uma operação de E/S.

  · Async: dispara I/O e CONTINUA processando enquanto espera
  · Sync:  BLOQUEIA tudo até o I/O terminar (não processa nada)

Controles:
  espaço  reiniciar
  p       pausar/continuar
  q       sair
"""

from rich.text import Text
from rich.style import Style

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.widgets import Header, Footer, Static, RichLog

# Solarized light palette
SOL = {
    "bg":    "#fdf6e3",
    "bg2":   "#eee8d5",
    "fg":    "#586e75",
    "fg2":   "#93a1a1",
    "green": "#859900",
    "red":   "#dc322f",
    "yellow": "#b58900",
    "blue":  "#268bd2",
    "magenta": "#d33682",
    "orange": "#cb4b16",
    "cyan":  "#2aa198",
    "violet": "#6c71c4",
}

TOTAL_DADOS = 5000
TRACK_LEN_PX = 70          # largura visual da pista em células

IO_INTERVAL = 500          # a cada 500 dados processados -> dispara I/O
IO_DURATION = 100          # duração do I/O em ticks (operação lenta)
PROCESS_PER_TICK = 10      # dados processados por tick quando livre


class Carro:
    def __init__(self, nome, estilo, cor):
        self.nome = nome
        self.estilo = estilo      # "async" ou "sync"
        self.cor = cor
        self.reset()

    def reset(self):
        self.dados = 0            # dados processados (= distância em m)
        self.io_ticks_restantes = 0   # ticks até I/O completar
        self.io_count = 0         # quantos I/Os já concluiu
        self.bloqueado = False
        self.ticks_parado = 0
        self.io_inflight = False  # Async: I/O está em andamento mas não bloqueia

    def tick(self):
        # dispara I/O quando atinge o intervalo
        if self.dados > 0 and self.dados % IO_INTERVAL == 0 and not self.io_inflight and self.io_ticks_restantes == 0:
            self.io_ticks_restantes = IO_DURATION
            self.io_inflight = True
            if self.estilo == "sync":
                self.bloqueado = True

        # atualiza I/O em andamento
        if self.io_ticks_restantes > 0:
            self.io_ticks_restantes -= 1
            if self.io_ticks_restantes == 0:
                self.io_inflight = False
                self.io_count += 1
                self.bloqueado = False

        if self.estilo == "async":
            # async: processa sempre (I/O não bloqueia)
            if self.bloqueado:
                self.bloqueado = False
            if self.dados < TOTAL_DADOS:
                n = min(PROCESS_PER_TICK, TOTAL_DADOS - self.dados)
                self.dados += n
        else:  # sync
            # sync: só processa se não estiver bloqueado esperando I/O
            if self.bloqueado:
                self.ticks_parado += 1
            elif self.dados < TOTAL_DADOS:
                n = min(PROCESS_PER_TICK, TOTAL_DADOS - self.dados)
                self.dados += n

    @property
    def concluido(self):
        return self.dados >= TOTAL_DADOS


def _pct(v):
    return v / TOTAL_DADOS


def _barra_pista(pct, width, carro_char="🏎️", bloqueado=False, io_ativo=False, tick=0):
    """Retorna Text com a pista e o carro na posição pct.
    io_ativo: se True, mostra ⚡ piscando ao lado do carro (async com I/O em andamento).
    """
    pos = int(pct * (width - 2))
    t = Text()
    t.append("|", Style(color=SOL["fg2"]))
    for i in range(width - 2):
        if i in ((width - 2) // 4, (width - 2) // 2, 3 * (width - 2) // 4):
            t.append("+", Style(color=SOL["fg2"]))
        else:
            t.append("-", Style(color=SOL["fg2"]))
    t.append("|", Style(color=SOL["fg2"]))
    t.append("\n")
    t.append(" " * (pos + 1))
    if bloqueado:
        t.append("⛽", Style(color=SOL["red"]))
    else:
        t.append(carro_char)
        if io_ativo:
            # ⚡ pisca a cada 5 ticks ao lado do carro
            if tick % 10 < 5:
                t.append("⚡", Style(color=SOL["yellow"], bold=True))
    return t


class CorridaApp(App):
    TITLE = "Corrida: Async vs Sync"
    theme = "solarized-light"

    BINDINGS = [
        Binding("space", "restart", "Reiniciar"),
        Binding("p", "pause", "Pausar"),
        Binding("q", "quit", "Sair"),
    ]

    def __init__(self):
        super().__init__()
        self.async_car = Carro("Async", "async", SOL["green"])
        self.sync_car = Carro("Sync", "sync", SOL["orange"])
        self.paused = False
        self.t = 0
        self.winner = None
        self._last_async_io = 0
        self._last_sync_io = 0

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical():
            yield Static("", id="title")
            yield Static("", id="track")
            yield Static("", id="status")
            yield Static("", id="summary")
            yield RichLog(id="log", markup=False, highlight=False, wrap=True, max_lines=200)
        yield Footer()

    def on_mount(self) -> None:
        self._load()
        self.set_interval(0.04, self._tick)   # ~25fps

    def _load(self):
        self.async_car.reset()
        self.sync_car.reset()
        self.t = 0
        self.winner = None
        self._last_async_io = 0
        self._last_sync_io = 0
        try:
            self.query_one("#log", RichLog).clear()
        except Exception:
            pass

    def _tick(self):
        if not self.paused and self.winner is None:
            self.async_car.tick()
            self.sync_car.tick()
            self.t += 1
            if self.async_car.concluido and self.sync_car.concluido:
                self.winner = "empate"
            elif self.async_car.concluido:
                self.winner = "async"
            elif self.sync_car.concluido:
                self.winner = "sync"
        self._render()

    def _render(self):
        w = self.size.width
        track_w = max(40, min(TRACK_LEN_PX, w - 4))

        # header
        flag = " [PAUSADO]" if self.paused else ""
        if self.winner:
            flag += f" [VENCEDOR: {self.winner.upper()}]"
        header = Text.assemble(
            ("🏁 Corrida: Async vs Sync 🏁\n", Style(color=SOL["orange"], bold=True)),
            (f"tick = {self.t:4d}  dados = 5000  I/O a cada {IO_INTERVAL} dados\n",
             Style(color=SOL["fg"])),
            ("Async dispara I/O e continua; Sync trava esperando I/O completar",
             Style(color=SOL["fg2"], italic=True)),
        )
        self.query_one("#title", Static).update(header)

        # pista
        line_a = Text.assemble(("Async  ", Style(color=SOL["green"], bold=True)),
                               _barra_pista(_pct(self.async_car.dados), track_w, "🏎️",
                                            io_ativo=self.async_car.io_inflight, tick=self.t))
        line_s = Text.assemble(("Sync   ", Style(color=SOL["orange"], bold=True)),
                               _barra_pista(_pct(self.sync_car.dados), track_w, "🚙",
                                            bloqueado=self.sync_car.bloqueado))
        finish_pos = (track_w - 2) + 0
        finish_line = Text.assemble(("       ", {}),
                                    (" " * finish_pos, {}),
                                    ("🏁", {}))
        track = Text.assemble(line_a, Text("\n"), line_s, Text("\n"), finish_line)
        self.query_one("#track", Static).update(track)

        # status
        a_state = ("PROCESSANDO" if not self.async_car.io_inflight
                   else f"PROCESSANDO + I/O ({self.async_car.io_ticks_restantes}t)")
        s_state = ("BLOQUEADO (I/O)" if self.sync_car.bloqueado
                   else "PROCESSANDO")
        s_color = SOL["red"] if self.sync_car.bloqueado else SOL["orange"]
        st = Text.assemble(
            ("Async: ", Style(color=SOL["green"], bold=True)),
            (f"{self.async_car.dados:4d}/5000 m  ", {}),
            (f"{a_state}  ", Style(color=SOL["green"])),
            (f"I/Os concluídos: {self.async_car.io_count}\n", {}),
            ("Sync:  ", Style(color=SOL["orange"], bold=True)),
            (f"{self.sync_car.dados:4d}/5000 m  ", {}),
            (f"{s_state}  ", Style(color=s_color)),
            (f"I/Os concluídos: {self.sync_car.io_count}   ", {}),
            (f"(parado: {self.sync_car.ticks_parado}t)", Style(color=SOL["red"])),
        )
        self.query_one("#status", Static).update(st)

        # resumo dinâmico
        delta = self.async_car.dados - self.sync_car.dados
        if delta > 0:
            summ = Text.assemble(
                ("⚡ Async está ", {}),
                (f"{delta}m", Style(color=SOL["green"], bold=True)),
                (" à frente — continuou processando durante a espera de I/O.",
                 Style(color=SOL["fg"], italic=True)),
            )
        elif delta < 0:
            summ = Text.assemble(
                ("Sync está ", {}),
                (f"{-delta}m", Style(color=SOL["orange"], bold=True)),
                (" à frente.", Style(color=SOL["fg"], italic=True)),
            )
        else:
            summ = Text.assemble(("Empatados.", Style(color=SOL["fg"], italic=True)))
        self.query_one("#summary", Static).update(summ)

        # log
        log = self.query_one("#log", RichLog)
        msgs = []
        if self.async_car.io_count > self._last_async_io:
            msgs.append(("Async", f"I/O #{self.async_car.io_count} concluído", SOL["green"]))
            self._last_async_io = self.async_car.io_count
        if self.sync_car.io_count > self._last_sync_io:
            msgs.append(("Sync", f"I/O #{self.sync_car.io_count} concluído", SOL["orange"]))
            self._last_sync_io = self.sync_car.io_count
        for who, msg, cor in msgs:
            line = Text.assemble(
                (f"t={self.t:4d} ", Style(color=SOL["fg2"])),
                (f"{who}: ", Style(color=cor, bold=True)),
                (msg, Style(color=SOL["fg"])),
            )
            log.write(line)

    def action_restart(self):
        self._load()
        self.paused = False

    def action_pause(self):
        self.paused = not self.paused


def run():
    CorridaApp().run()


if __name__ == "__main__":
    run()