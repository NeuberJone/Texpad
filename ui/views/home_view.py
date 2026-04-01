from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from ui import theme
from ui.widgets import (
    build_alert_box,
    build_info_row,
    build_metric_card,
    make_card,
    make_primary_button,
    make_quick_button,
    make_title_label,
)


class HomeView(tk.Frame):
    def __init__(self, parent: tk.Misc, controller) -> None:
        super().__init__(parent, bg=theme.APP_BG)
        self.controller = controller

        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self._build()

    def _build(self) -> None:
        metrics = tk.Frame(self, bg=theme.APP_BG)
        metrics.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 12))
        for i in range(4):
            metrics.grid_columnconfigure(i, weight=1)

        self.metric_input = build_metric_card(
            metrics,
            title="LINHAS NA ENTRADA",
            value_var=self.controller.home_input_lines_var,
            subtitle="linhas preenchidas",
            accent=theme.PRIMARY,
        )
        self.metric_input.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        self.metric_output = build_metric_card(
            metrics,
            title="LINHAS NA SAÍDA",
            value_var=self.controller.home_output_lines_var,
            subtitle="resultado organizado",
            accent=theme.SUCCESS,
        )
        self.metric_output.grid(row=0, column=1, sticky="ew", padx=8)

        self.metric_sizes = build_metric_card(
            metrics,
            title="TAMANHOS VÁLIDOS",
            value_var=self.controller.home_sizes_total_var,
            subtitle="cadastro atual",
            accent=theme.WARNING,
        )
        self.metric_sizes.grid(row=0, column=2, sticky="ew", padx=8)

        self.metric_json = build_metric_card(
            metrics,
            title="JSON",
            value_var=self.controller.home_json_status_var,
            subtitle="visualização e geração",
            accent=theme.DANGER,
        )
        self.metric_json.grid(row=0, column=3, sticky="ew", padx=(8, 0))

        left = tk.Frame(self, bg=theme.APP_BG)
        left.grid(row=1, column=0, sticky="nsew", padx=(0, 8))
        left.grid_columnconfigure(0, weight=1)

        right = tk.Frame(self, bg=theme.APP_BG)
        right.grid(row=1, column=1, rowspan=3, sticky="nsew", padx=(8, 0))
        right.grid_columnconfigure(0, weight=1)
        right.grid_rowconfigure(1, weight=1)

        self._build_actions_card(left)
        self._build_alert_card(left)
        self._build_context_card(left)

        self._build_recent_card(right)
        self._build_hero_card(right)

    def _build_actions_card(self, parent: tk.Misc) -> None:
        card = make_card(parent)
        card.grid(row=0, column=0, sticky="ew", pady=(0, 12))

        make_title_label(card, "Ações rápidas").pack(fill="x", padx=18, pady=(16, 10))

        actions_wrap = tk.Frame(card, bg=theme.PANEL_BG)
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
        card.grid(row=1, column=0, sticky="ew", pady=(0, 12))

        make_title_label(card, "Alertas").pack(fill="x", padx=18, pady=(16, 10))
        build_alert_box(card, textvariable=self.controller.home_alert_var).pack(
            fill="x", padx=18, pady=(0, 16)
        )

    def _build_context_card(self, parent: tk.Misc) -> None:
        card = make_card(parent)
        card.grid(row=2, column=0, sticky="ew")

        make_title_label(card, "Contexto atual").pack(fill="x", padx=18, pady=(16, 10))

        build_info_row(
            card,
            label="Arquivo",
            value_var=self.controller.home_current_file_var,
        )
        build_info_row(
            card,
            label="Modo de texto",
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

        tk.Frame(card, bg=theme.PANEL_BG, height=10).pack(fill="x")

    def _build_recent_card(self, parent: tk.Misc) -> None:
        card = make_card(parent)
        card.grid(row=0, column=0, sticky="ew")

        make_title_label(card, "Resumo recente").pack(fill="x", padx=18, pady=(16, 10))

        self.recent_tree = ttk.Treeview(
            card,
            columns=("item", "valor"),
            show="headings",
            height=5,
        )
        self.recent_tree.heading("item", text="ITEM")
        self.recent_tree.heading("valor", text="VALOR")
        self.recent_tree.column("item", width=190, anchor="w")
        self.recent_tree.column("valor", width=420, anchor="w")
        self.recent_tree.pack(fill="x", padx=18, pady=(0, 18))

    def _build_hero_card(self, parent: tk.Misc) -> None:
        card = make_card(parent)
        card.grid(row=1, column=0, sticky="nsew", pady=(12, 0))

        inner = tk.Frame(card, bg=theme.PANEL_BG)
        inner.pack(fill="both", expand=True, padx=22, pady=22)

        tk.Label(
            inner,
            text="Texpad com shell visual inspirado na UI do Nexor.",
            bg=theme.PANEL_BG,
            fg=theme.TEXT,
            font=(theme.FONT_FAMILY, 15, "bold"),
            justify="left",
            anchor="w",
            wraplength=640,
        ).pack(anchor="w")

        tk.Label(
            inner,
            text=(
                "A Home resume o estado atual do trabalho, enquanto o Editor "
                "continua sendo a área principal para entrada, localizar/substituir, "
                "processamento, saída organizada e JSON."
            ),
            bg=theme.PANEL_BG,
            fg=theme.TEXT_MUTED,
            font=(theme.FONT_FAMILY, 10),
            justify="left",
            anchor="w",
            wraplength=680,
        ).pack(anchor="w", pady=(12, 0))

        make_primary_button(
            inner,
            text="Ir para o Editor",
            command=lambda: self.controller.show_screen("editor"),
        ).pack(anchor="w", pady=(18, 0))

    def refresh(self) -> None:
        self.controller.refresh_home_dashboard()

        self.recent_tree.delete(*self.recent_tree.get_children())
        rows = [
            ("Arquivo atual", self.controller.home_recent_a_var.get()),
            ("Saída", self.controller.home_recent_b_var.get()),
            ("JSON", self.controller.home_recent_c_var.get()),
            ("Backups", self.controller.home_recent_d_var.get()),
        ]
        for row in rows:
            self.recent_tree.insert("", "end", values=row)