from gradio import Blocks
from gradio.themes import ThemeClass as Theme
from gradio.blocks import Block
from typing import Dict

from .layout_base import LayoutBase


class Application:
    app: Blocks
    children: list[LayoutBase]
    block_dict: Dict[str, Block]

    def __init__(
        self,
        theme: Theme | str | None = None,
        analytics_enabled: bool | None = None,
        mode: str = "blocks",
        title: str = "Gradio",
        css: str | None = None,
        js: str | None = None,
        head: str | None = None,
        fill_height: bool = False,
        delete_cache: tuple[int, int] | None = None,
        **kwargs,
    ) -> None:
        self.app = Blocks(
            theme=theme,
            analytics_enabled=analytics_enabled,
            mode=mode,
            title=title,
            css=css,
            js=js,
            head=head,
            fill_height=fill_height,
            delete_cache=delete_cache,
            **kwargs,
        )

        self.children = []
        self.block_dict = {}

    def add(self, child: LayoutBase):
        self.children.append(child)

    def _render(self):
        with self.app:
            for child in self.children:
                child.render()

        self.app.render()

    def _attach_event(self):
        for child in self.children:
            self.block_dict.update(child.global_children_dict)

        with self.app:
            for child in self.children:
                try:
                    child.attach_event(block_dict=self.block_dict)
                except NotImplementedError:
                    print(f"{child.name}'s attach_event is not implemented")

    def _clear(self):
        for child in self.children:
            child.clear()

        self.children.clear()

    def launch(self, **args):
        self._render()
        self._attach_event()
        self._clear()

        self.app.launch(args)
