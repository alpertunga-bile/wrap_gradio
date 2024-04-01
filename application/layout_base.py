from __future__ import annotations

from typing import Dict
from gradio.blocks import Block


class LayoutBase:
    main_layout: Block
    name: str
    global_children_dict: Dict[str, Block]
    local_children: list[Block]
    layout_list: list[LayoutBase]

    def __init__(self) -> None:
        self.main_layout = None
        self.name = "Layout Base"
        self.global_children_dict = {}
        self.local_children = []
        self.layout_list = []

    def add_component(self, name: str, component: Block) -> None:
        self.local_children.append(component)
        self.global_children_dict[name] = component

    def add_layout(self, layout: LayoutBase) -> None:
        self.layout_list.append(layout)
        self.global_children_dict.update(layout.global_children_dict)

    def render(self) -> None:
        with self.main_layout:
            for layout in self.layout_list:
                layout.render()

            for local_child in self.local_children:
                local_child.render()

        self.main_layout.render()

    def attach_event(self, block_dict: Dict[str, Block]) -> None:
        raise NotImplementedError
