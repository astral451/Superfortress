"""Superfortress: a tiny e-ink-friendly simulation, built to prove out
sideloading a Python/Kivy app onto a Supernote A5X.

Design notes for e-ink:
  - No continuous animation. maxfps is capped low.
  - The canvas only redraws when the simulation actually changes state
    (see sim.World.tick() returning a "changed" flag).
  - Ticks are spaced out (every TICK_INTERVAL seconds) rather than
    running every frame, both to keep the pace watchable and to avoid
    hammering the e-ink panel with refreshes.
"""
from kivy.config import Config

Config.set("graphics", "maxfps", "4")

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from sim import GRASS, STONE, TREE, WATER, World

TICK_INTERVAL = 1.5

TILE_COLORS = {
    GRASS: (0.85, 0.85, 0.85, 1),
    TREE: (0.25, 0.25, 0.25, 1),
    STONE: (0.55, 0.55, 0.55, 1),
    WATER: (0.05, 0.05, 0.05, 1),
}


class MapView(Widget):
    def __init__(self, world, **kwargs):
        super().__init__(**kwargs)
        self.world = world
        self.bind(size=self._redraw, pos=self._redraw)

    def cell_size(self):
        return (
            self.width / self.world.width,
            self.height / self.world.height,
        )

    def _redraw(self, *_args):
        self.canvas.clear()
        cw, ch = self.cell_size()
        with self.canvas:
            for y in range(self.world.height):
                for x in range(self.world.width):
                    Color(*TILE_COLORS[self.world.tile_at(x, y)])
                    Rectangle(
                        pos=(self.x + x * cw, self.y + (self.world.height - 1 - y) * ch),
                        size=(cw, ch),
                    )
            Color(1, 1, 1, 1)
            wx = self.x + self.world.worker_x * cw
            wy = self.y + (self.world.height - 1 - self.world.worker_y) * ch
            Ellipse(pos=(wx + cw * 0.2, wy + ch * 0.2), size=(cw * 0.6, ch * 0.6))


class SuperfortressRoot(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.world = World(width=16, height=20)
        self.paused = False

        self.status_label = Label(
            text=self._status_text(),
            size_hint_y=None,
            height="40dp",
        )

        self.pause_button = Button(text="Pause", size_hint_y=None, height="48dp")
        self.pause_button.bind(on_release=self._toggle_pause)

        top_bar = BoxLayout(size_hint_y=None, height="48dp")
        top_bar.add_widget(self.status_label)
        top_bar.add_widget(self.pause_button)

        self.map_view = MapView(self.world)

        self.add_widget(top_bar)
        self.add_widget(self.map_view)

        Clock.schedule_interval(self._on_tick, TICK_INTERVAL)

    def _status_text(self):
        return (
            f"Wood: {self.world.wood}  "
            f"Trees: {self.world.trees_remaining()}  "
            f"Tick: {self.world.tick_count}"
        )

    def _toggle_pause(self, *_args):
        self.paused = not self.paused
        self.pause_button.text = "Resume" if self.paused else "Pause"

    def _on_tick(self, _dt):
        if self.paused:
            return
        changed = self.world.tick()
        self.status_label.text = self._status_text()
        if changed:
            self.map_view._redraw()


class SuperfortressApp(App):
    def build(self):
        self.title = "Superfortress"
        return SuperfortressRoot()


if __name__ == "__main__":
    SuperfortressApp().run()
