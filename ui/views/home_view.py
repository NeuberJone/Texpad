from __future__ import annotations

import tkinter as tk

from ui import theme
from ui.widgets import build_alert_box, build_info_row, make_card, make_quick_button, make_title_label


class HomeView(tk.Frame):
    def __init__(self, parent: tk.Misc, controller) -> None:
        super().__init__(parent, bg=theme.active_theme().app_bg)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self._build()

    def _build(self) -> None:
        t = theme.active_theme()

        left = tk.Frame(self, bg=t.app_bg)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        left.grid_columnconfigure(0, weight=1)

        right = tk.Frame(self, bg=t.app_bg)
        right.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        right.grid_columnconfigure(0, weight=1)

        self._build_actions_card(left)
        self._build_alert_card(left)
        self._build_summary_card(right)

    # ------------------------------------------------------------------
    # Cards
    # ------------------------------------------------------------------
    def _build_actions_card(self, parent: tk.Misc) -> None:
        card = make_card(parent)
        card.grid(row=0, column=0, sticky="ew", pady=(0, 12))

        make_title_label(card, "Ações rápidas").pack(fill="x", padx=18, pady=(16, 10))

        actions_wrap = tk.Frame(card, bg=theme.active_theme().panel_bg)
        actions_wrap.pack(fill="x", padx=18, pady=(0, 16))
        for i in range(4):
            actions_wrap.grid_columnconfigure(i, weight=1)

        btn_open = make_quick_button(
            actions_wrap,
            text="Abrir Lista",
            command=self.controller.open_input_file,
        )
        btn_open.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        btn_editor = make_quick_button(
            actions_wrap,
            text="Editor",
            command=lambda: self.controller.show_screen("editor"),
        )
        btn_editor.grid(row=0, column=1, sticky="ew", padx=10)

        btn_process = make_quick_button(
            actions_wrap,
            text="Processar",
            command=self.controller.process_and_preview,
        )
        btn_process.grid(row=0, column=2, sticky="ew", padx=10)

        btn_settings = make_quick_button(
            actions_wrap,
            text="Configurações",
            command=lambda: self.controller.show_screen("settings"),
        )
        btn_settings.grid(row=0, column=3, sticky="ew", padx=(10, 0))

    def _build_alert_card(self, parent: tk.Misc) -> None:
        card = make_card(parent)
        card.grid(row=1, column=0, sticky="ew")

        make_title_label(card, "Alertas").pack(fill="x", padx=18, pady=(16, 10))
        build_alert_box(card, textvariable=self.controller.home_alert_var).pack(
            fill="x", padx=18, pady=(0, 16)
        )

    def _build_summary_card(self, parent: tk.Misc) -> None:
        card = make_card(parent)
        card.grid(row=0, column=0, sticky="nsew")
        card.grid_columnconfigure(0, weight=1)

        make_title_label(card, "Resumo atual").pack(fill="x", padx=18, pady=(16, 10))

        build_info_row(
            card,
            label="Arquivo",
            value_var=self.controller.home_current_file_var,
        )
        build_info_row(
            card,
            label="Modo",
            value_var=self.controller.home_mode_var,
        )
        build_info_row(
            card,
            label="Separador",
            value_var=self.controller.home_separator_var,
        )
        build_info_row(
            card,
            label="Salvar saída",
            value_var=self.controller.home_output_policy_var,
        )
        build_info_row(
            card,
            label="JSON",
            value_var=self.controller.home_json_status_var,
        )
        build_info_row(
            card,
            label="Tema",
            value_var=self.controller.theme_name_var,
        )

        spacer = tk.Frame(card, bg=theme.active_theme().panel_bg, height=8)
        spacer.pack(fill="x")

        tk.Label(
            card,
            text="Tamanhos cadastrados",
            bg=theme.active_theme().panel_bg,
            fg=theme.active_theme().text_muted,
            font=(theme.FONT_FAMILY, 9, "bold"),
            anchor="w",
        ).pack(fill="x", padx=18, pady=(8, 4))

        tk.Label(
            card,
            textvariable=self.controller.size_summary_var,
            bg=theme.active_theme().panel_bg,
            fg=theme.active_theme().text,
            justify="left",
            anchor="w",
            font=(theme.FONT_FAMILY, 9),
        ).pack(fill="x", padx=18, pady=(0, 16))

    # ------------------------------------------------------------------
    # Runtime
    # ------------------------------------------------------------------
    def refresh(self) -> None:
        self.controller.refresh_home_dashboard()