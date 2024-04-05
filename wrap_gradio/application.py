from gradio import Blocks
from gradio.themes import ThemeClass as Theme
from gradio.blocks import Block
from typing import Dict, Callable, Any, Literal

from .layout_base import LayoutBase

from fastapi import Request, FastAPI


class Application:
    app: Blocks
    children: list[LayoutBase]

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

    def _clear(self):
        from gc import collect

        for child in self.children:
            child.clear()

        self.children.clear()

        collect()

    def launch(
        self,
        inline: bool | None = None,
        inbrowser: bool = False,
        share: bool | None = None,
        debug: bool = False,
        max_threads: int = 40,
        auth: Callable | tuple[str, str] | list[tuple[str, str]] | None = None,
        auth_message: str | None = None,
        prevent_thread_lock: bool = False,
        show_error: bool = False,
        server_name: str | None = None,
        server_port: int | None = None,
        *,
        height: int = 500,
        width: int | str = "100%",
        favicon_path: str | None = None,
        ssl_keyfile: str | None = None,
        ssl_certfile: str | None = None,
        ssl_keyfile_password: str | None = None,
        ssl_verify: bool = True,
        quiet: bool = False,
        show_api: bool = True,
        allowed_paths: list[str] | None = None,
        blocked_paths: list[str] | None = None,
        root_path: str | None = None,
        app_kwargs: dict[str, Any] | None = None,
        state_session_capacity: int = 10000,
        share_server_address: str | None = None,
        share_server_protocol: Literal["http", "https"] | None = None,
        auth_dependency: Callable[[Request], str | None] | None = None,
        _frontend: bool = True,
    ) -> tuple[FastAPI, str, str]:
        self._render()
        self._attach_event()
        self._clear()

        return self.app.launch(
            inline=inline,
            inbrowser=inbrowser,
            share=share,
            debug=debug,
            max_threads=max_threads,
            auth=auth,
            auth_message=auth_message,
            prevent_thread_lock=prevent_thread_lock,
            show_error=show_error,
            server_name=server_name,
            server_port=server_port,
            height=height,
            width=width,
            favicon_path=favicon_path,
            ssl_keyfile=ssl_keyfile,
            ssl_certfile=ssl_certfile,
            ssl_keyfile_password=ssl_keyfile_password,
            ssl_verify=ssl_verify,
            quiet=quiet,
            show_api=show_api,
            allowed_paths=allowed_paths,
            blocked_paths=blocked_paths,
            root_path=root_path,
            app_kwargs=app_kwargs,
            state_session_capacity=state_session_capacity,
            share_server_address=share_server_address,
            share_server_protocol=share_server_protocol,
            auth_dependency=auth_dependency,
            _frontend=_frontend,
        )
