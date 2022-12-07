from itertools import zip_longest
from queue import LifoQueue, PriorityQueue, Queue

from rich.align import Align
from rich.columns import Columns
from rich.console import Group
from rich.live import Live
from rich.panel import Panel


class View:
    # define a view that renders the current state of our producers,
    # consumers, and the queue ten times a second
    def __init__(self, buffer, producers, consumers):
        self.buffer = buffer
        self.producers = producers
        self.consumers = consumers

    def animate(self):
        # Renders an auto-updating live display of any given renderable.
        with Live(
            self.render(), screen=True, refresh_per_second=10
        ) as live:
            while True:
                # update the renderable that is displayed
                live.update(self.render())

    def render(self):

        match self.buffer:
            case PriorityQueue():
                title = "Priority Queue"
                products = map(str, reversed(list(self.buffer.queue)))
            case LifoQueue():
                title = "Stack"
                products = list(self.buffer.queue)
            case Queue():
                # here 1st item will be removed first
                title = "Queue"
                products = reversed(list(self.buffer.queue))
            case _:
                title = products = ""

        rows = [
            # A console renderable that draws a border around its contents.
            Panel(f"[bold]{title}:[/] {', '.join(products)}", width=82)
        ]
        pairs = zip_longest(self.producers, self.consumers)
        for i, (producer, consumer) in enumerate(pairs, 1):
            left_panel = self.panel(producer, f"Producer {i}")
            right_panel = self.panel(consumer, f"Consumer {i}")
            rows.append(Columns([left_panel, right_panel], width=40))
        # Takes a group of renderables and
        # returns a renderable object that renders the group.
        return Group(*rows)

    def panel(self, worker, title):
        if worker is None:
            return ""
        padding = " " * int(29 / 100 * worker.progress)
        align = Align(
            padding + worker.state, align="left", vertical="middle"
        )
        return Panel(align, height=5, title=title)
