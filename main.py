from application.application import Application
from application.layouts import RowLayout, TabLayout, ColumnLayout

from gradio import Textbox

from typing import Dict
from gradio.blocks import Block


class FirstTab(TabLayout):
    def __init__(
        self,
        label: str | None = None,
        visible: bool = True,
        interactive: bool = True,
        id: int | str | None = None,
        elem_id: str | None = None,
        elem_classes: list[str] | str | None = None,
    ) -> None:
        super().__init__(label, visible, interactive, id, elem_id, elem_classes)

        self.row = RowLayout()

        self.left_textbox = Textbox(
            value="Left Textbox", interactive=True, render=False
        )
        self.right_textbox = Textbox(value="Right Textbox", render=False)

        self.row.add_component("left_textbox", self.left_textbox)
        self.row.add_component("right_textbox", self.right_textbox)

        self.add_layout(self.row)

    def attach_event(self, block_dict: Dict[str, Block]) -> None:
        def change_text(new_str: str):
            return Textbox(value=new_str)

        self.left_textbox.change(
            change_text,
            inputs=block_dict["left_textbox"],
            outputs=block_dict["right_textbox"],
        )


class SecondTab(TabLayout):
    def __init__(
        self,
        label: str | None = None,
        visible: bool = True,
        interactive: bool = True,
        id: int | str | None = None,
        elem_id: str | None = None,
        elem_classes: list[str] | str | None = None,
    ) -> None:
        super().__init__(label, visible, interactive, id, elem_id, elem_classes)

        self.column = ColumnLayout()

        self.upper_textbox = Textbox(value="Upper Textbox", interactive=True)
        self.bottom_textbox = Textbox(value="Bottom Textbox")

        self.column.add_component("upper_textbox", self.upper_textbox)
        self.column.add_component("bottom_textbox", self.bottom_textbox)

        self.add_layout(self.column)


if __name__ == "__main__":
    gui = Application(title="Wrap Gradio")

    first_tab = FirstTab(label="First Tab")
    second_tab = SecondTab(label="Second Tab")

    gui.add(first_tab)
    gui.add(second_tab)

    gui.launch()