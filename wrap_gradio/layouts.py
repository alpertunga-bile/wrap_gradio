from gradio import Row, Column, Tab

from .layout_base import LayoutBase

from typing import Literal


class RowLayout(LayoutBase):
    def __init__(
        self,
        *,
        name: str,
        variant: Literal["default", "panel", "compact"] = "default",
        visible: bool = True,
        elem_id: str | None = None,
        elem_classes: list[str] | str | None = None,
        equal_height: bool = True,
    ) -> None:
        super().__init__()

        self.main_layout = Row(
            variant=variant,
            visible=visible,
            elem_id=elem_id,
            elem_classes=elem_classes,
            render=False,
            equal_height=equal_height,
        )

        self.global_children_dict[name] = self.main_layout


class ColumnLayout(LayoutBase):
    def __init__(
        self,
        *,
        name: str,
        scale: int = 1,
        min_width: int = 320,
        variant: Literal["default", "panel", "compact"] = "default",
        visible: bool = True,
        elem_id: str | None = None,
        elem_classes: list[str] | str | None = None,
    ) -> None:
        super().__init__()

        self.main_layout = Column(
            scale=scale,
            min_width=min_width,
            variant=variant,
            visible=visible,
            elem_id=elem_id,
            elem_classes=elem_classes,
            render=False,
        )

        self.global_children_dict[name] = self.main_layout


class TabLayout(LayoutBase):
    def __init__(
        self,
        name: str,
        visible: bool = True,
        interactive: bool = True,
        id: int | str | None = None,
        elem_id: str | None = None,
        elem_classes: list[str] | str | None = None,
    ) -> None:
        super().__init__()

        self.main_layout = Tab(
            label=name,
            visible=visible,
            interactive=interactive,
            id=id,
            elem_id=elem_id,
            elem_classes=elem_classes,
            render=False,
        )

        self.global_children_dict[name] = self.main_layout
