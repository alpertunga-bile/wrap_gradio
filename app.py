from __future__ import annotations

from gradio.blocks import Block, Blocks
from typing import Dict
from fastapi import FastAPI

"""
---------------------------------------------------------------------------------------------------------
-- Base Classes
"""


# Base class for the RowLayout, ColumnLayout and TabLayout classes
class LayoutBase:
    main_layout: Block  # Stores the main layout from the gradio package of this class.
    name: str  # Name of the class. Used to differentiate from other layouts and for debug purposes.
    global_children_dict: Dict[
        str, Block
    ]  # Stores the children components with given name.
    renderables: list  # Stores the renderable elements such as components and layouts.

    def __init__(self) -> None:
        self.main_layout = None
        self.name = "Layout Base"
        self.global_children_dict = {}
        self.renderables = []

    """
        components are coming from the gradio package
        these components are inherited from the Block class eventually
    """

    def add_component(self, name: str, component: Block) -> None:
        self.renderables.append(component)
        self.global_children_dict[name] = component

    """
        layout has to be from RowLayout, ColumnLayout or TabLayout classes
        the parent class includes all the components that children layouts have
    """

    def add_layout(self, layout: LayoutBase) -> None:
        self.renderables.append(layout)
        self.global_children_dict.update(layout.global_children_dict)

    def render(self) -> None:
        with self.main_layout:
            for renderable in self.renderables:
                renderable.render()

        self.main_layout.render()

    def clear(self) -> None:
        self.global_children_dict.clear()

        # we can be sure that all objects are cleaned
        for renderable in self.renderables:
            if isinstance(renderable, LayoutBase):
                renderable.clear()

        self.renderables.clear()

    """
        the inherited class has to implement this function.
        block_dict is coming from Application class's _attach_event function or parent class's attach_event function
    """

    def attach_event(self, block_dict: Dict[str, Block]) -> None:
        raise NotImplementedError


# Responsible for rendering, attaching events and launching
class Application:
    app: Blocks  # Base application component from the gradio package.
    children: list[LayoutBase]  # Stores the layouts

    # Blocks constructor parameters are omitted for brevity
    def __init__(self, title: str) -> None:
        self.app = Blocks(title=title)
        self.children = []

    """
        adding given RowLayout, ColumnLayout or TabLayout classes to children variable
    """

    def add(self, child: LayoutBase):
        self.children.append(child)

    def _render(self):
        with self.app:
            for child in self.children:
                child.render()

        self.app.render()

    def _attach_event(self):
        block_dict: Dict[str, Block] = {}

        for child in self.children:
            block_dict.update(child.global_children_dict)

        with self.app:
            for child in self.children:
                try:
                    child.attach_event(block_dict=block_dict)
                except NotImplementedError:
                    print(f"{child.name}'s attach_event is not implemented")

    """
        clearing the children
        we don't need them because they are going to live in the app.blocks and app.fns functions
    """

    def _clear(self):
        from gc import collect

        for child in self.children:
            child.clear()

        self.children.clear()

        collect()

    # launch function parameters are omitted for the brevity
    def launch(self) -> tuple[FastAPI, str, str]:
        self._render()
        self._attach_event()
        self._clear()

        return self.app.launch()


from gradio import Row, Column, Tab, Textbox


class RowLayout(LayoutBase):
    def __init__(self, name: str) -> None:
        super().__init__()

        self.main_layout = Row()

        self.global_children_dict[name] = self.main_layout


class ColumnLayout(LayoutBase):
    def __init__(self, name: str) -> None:
        super().__init__()

        self.main_layout = Column()

        self.global_children_dict[name] = self.main_layout


class TabLayout(LayoutBase):
    def __init__(self, name: str) -> None:
        super().__init__()

        self.main_layout = Tab(label=name)

        self.global_children_dict[name] = self.main_layout


"""
---------------------------------------------------------------------------------------------------------
-- Example
"""


def change_text(new_str: str):
    return Textbox(value=new_str)


class RowExample(RowLayout):
    def __init__(self, name: str) -> None:
        super().__init__(name=name)

        self.left_textbox = Textbox(
            value="Left Textbox", interactive=True, render=False
        )
        self.right_textbox = Textbox(value="Right Textbox", render=False)

        self.add_component("left_textbox", self.left_textbox)
        self.add_component("right_textbox", self.right_textbox)

    def attach_event(self, block_dict: Dict[str, Block]) -> None:
        self.left_textbox.change(
            change_text,
            inputs=self.left_textbox,
            outputs=self.right_textbox,
        )


class FirstTab(TabLayout):
    def __init__(self, name: str) -> None:
        super().__init__(name)

        self.row = RowExample(name="first tab row layout")

        self.add_layout(self.row)

    def attach_event(self, block_dict: Dict[str, Block]) -> None:
        self.row.attach_event(block_dict)


class SecondTab(TabLayout):
    def __init__(self, name: str) -> None:
        super().__init__(name)

        self.column = ColumnLayout(name="second tab column layout")

        self.top_textbox = Textbox(value="Top Textbox", interactive=True, render=False)
        self.bottom_textbox = Textbox(value="Bottom Textbox", render=False)

        self.column.add_component("top_textbox", self.top_textbox)
        self.column.add_component("bottom_textbox", self.bottom_textbox)

        self.add_layout(self.column)

    def attach_event(self, block_dict: Dict[str, Block]) -> None:
        block_dict["left_textbox"].change(
            change_text,
            inputs=block_dict["left_textbox"],
            outputs=self.bottom_textbox,
        )


"""
---------------------------------------------------------------------------------------------------------
-- Main
"""

gui = Application(title="Wrap Gradio")

first_tab = FirstTab(name="First Tab")
second_tab = SecondTab(name="Second Tab")

gui.add(first_tab)
gui.add(second_tab)

gui.launch()
