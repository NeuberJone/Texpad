from __future__ import annotations

from tkinter import ttk

from listforge_config import save_config
from ui import theme


class ThemeRuntime:
    def __init__(self, controller) -> None:
        self.controller = controller

    def apply_theme(self, theme_name: str, *, persist: bool = True) -> None:
        if theme_name not in theme.THEMES:
            theme_name = theme.DEFAULT_THEME_NAME

        self.controller.theme_name_var.set(theme_name)

        # Troca o tema ativo global imediatamente
        theme.set_active_theme(theme_name)

        # Reaplica o estilo ttk no root atual
        try:
            style = ttk.Style(self.controller.root)
            theme.apply_ttk_theme(style=style, theme_name=theme_name)
        except Exception:
            theme.apply_ttk_theme(theme_name=theme_name)

        # Atualiza a cor base da janela sem resetar geometry/minsize
        try:
            self.controller.root.configure(bg=theme.active_theme().app_bg)
        except Exception:
            pass

        if persist:
            self._persist_theme(theme_name)

        shell = getattr(self.controller, "shell", None)
        if shell is not None:
            shell.rebuild_theme()

    # ------------------------------------------------------------------
    # Internos
    # ------------------------------------------------------------------
    def _persist_theme(self, theme_name: str) -> None:
        cfg = getattr(self.controller, "cfg", None)
        if not isinstance(cfg, dict):
            return

        cfg["theme_name"] = theme_name
        save_config(cfg)