from __future__ import annotations

from typing import Dict
from gradio.blocks import Block


class LayoutBase:
    main_layout: Block
    name: str
    global_children_dict: Dict[str, Block]
    renderables: list

    def __init__(self) -> None:
        self.main_layout = None
        self.name = "Layout Base"
        self.global_children_dict = {}
        self.renderables = []

    def add_component(self, name: str, component: Block) -> None:
        self.renderables.append(component)
        self.global_children_dict[name] = component

    def add_layout(self, layout: LayoutBase) -> None:
        self.renderables.append(layout)
        self.global_children_dict.update(layout.global_children_dict)

    def render(self) -> None:
        with self.main_layout:
            for renderable in self.renderables:
                renderable.render()

        self.main_layout.render()

    def attach_event(self, block_dict: Dict[str, Block]) -> None:
        raise NotImplementedError
