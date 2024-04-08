from wrap_gradio.application import Application
from wrap_gradio.layouts import RowLayout, TabLayout, ColumnLayout

from gradio import Textbox

from typing import Dict, Literal
from gradio.blocks import Block


def change_text(new_str: str):
    return Textbox(value=new_str)


class RowExample(RowLayout):
    def __init__(
        self,
        *,
        name: str,
        variant: Literal["default", "panel", "compact"] = "default",
        visible: bool = True,
        elem_id: str | None = None,
        elem_classes: list[str] | str | None = None,
        equal_height: bool = True
    ) -> None:
        super().__init__(
            name=name,
            variant=variant,
            visible=visible,
            elem_id=elem_id,
            elem_classes=elem_classes,
            equal_height=equal_height,
        )

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
    def __init__(
        self,
        name: str,
        visible: bool = True,
        interactive: bool = True,
        id: int | str | None = None,
        elem_id: str | None = None,
        elem_classes: list[str] | str | None = None,
    ) -> None:
        super().__init__(name, visible, interactive, id, elem_id, elem_classes)

        self.row = RowExample(name="first tab row layout")

        self.add_layout(self.row)

    def attach_event(self, block_dict: Dict[str, Block]) -> None:
        self.row.attach_event(block_dict)


class SecondTab(TabLayout):
    def __init__(
        self,
        name: str,
        visible: bool = True,
        interactive: bool = True,
        id: int | str | None = None,
        elem_id: str | None = None,
        elem_classes: list[str] | str | None = None,
    ) -> None:
        super().__init__(name, visible, interactive, id, elem_id, elem_classes)

        self.column = ColumnLayout(name="second tab column layout")

        self.top_textbox = Textbox(value="Top Textbox", interactive=True)
        self.bottom_textbox = Textbox(value="Bottom Textbox")

        self.column.add_component("top_textbox", self.top_textbox)
        self.column.add_component("bottom_textbox", self.bottom_textbox)

        self.add_layout(self.column)

    def attach_event(self, block_dict: Dict[str, Block]) -> None:
        block_dict["left_textbox"].change(
            change_text,
            inputs=block_dict["left_textbox"],
            outputs=self.bottom_textbox,
        )


if __name__ == "__main__":
    gui = Application(title="Wrap Gradio")

    first_tab = FirstTab(name="First Tab")
    second_tab = SecondTab(name="Second Tab")

    gui.add(first_tab)
    gui.add(second_tab)

    gui.launch()
