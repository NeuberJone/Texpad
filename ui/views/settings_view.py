from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from ui import theme


class SettingsView(tk.Frame):
    def __init__(self, parent: tk.Misc, controller) -> None:
        super().__init__(parent, bg=theme.active_theme().app_bg)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.nb = None
        self.sizes_nb = None

        self.main_selector_buttons: dict[str, tk.Label] = {}
        self.main_selector_panels: dict[str, tk.Frame] = {}
        self.current_main_section: str = "general"

        self.size_selector_buttons: dict[str, tk.Label] = {}
        self.size_selector_panels: dict[str, tk.Frame] = {}
        self.current_size_group: str = "male"

        self._build()

    def _build(self) -> None:
        t = theme.active_theme()

        wrap = tk.Frame(self, bg=t.app_bg)
        wrap.grid(row=0, column=0, sticky="nsew")
        wrap.grid_rowconfigure(1, weight=1)
        wrap.grid_columnconfigure(0, weight=1)

        selector_wrap = tk.Frame(wrap, bg=t.app_bg)
        selector_wrap.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        for col in range(5):
            selector_wrap.grid_columnconfigure(col, weight=1)

        sections = [
            ("general", "Geral"),
            ("output", "Saída"),
            ("json", "JSON"),
            ("sizes", "Tamanhos"),
            ("appearance", "Aparência"),
        ]

        for col, (section_key, title) in enumerate(sections):
            self._create_main_selector_button(selector_wrap, section_key, title, col)

        content_wrap = tk.Frame(wrap, bg=t.app_bg)
        content_wrap.grid(row=1, column=0, sticky="nsew")
        content_wrap.grid_rowconfigure(0, weight=1)
        content_wrap.grid_columnconfigure(0, weight=1)

        self.tab_general = tk.Frame(content_wrap, bg=t.app_bg)
        self.tab_output = tk.Frame(content_wrap, bg=t.app_bg)
        self.tab_json = tk.Frame(content_wrap, bg=t.app_bg)
        self.tab_sizes = tk.Frame(content_wrap, bg=t.app_bg)
        self.tab_appearance = tk.Frame(content_wrap, bg=t.app_bg)

        self.main_selector_panels = {
            "general": self.tab_general,
            "output": self.tab_output,
            "json": self.tab_json,
            "sizes": self.tab_sizes,
            "appearance": self.tab_appearance,
        }

        self._build_general_tab()
        self._build_output_tab()
        self._build_json_tab()
        self._build_sizes_tab()
        self._build_appearance_tab()

        actions = tk.Frame(wrap, bg=t.app_bg)
        actions.grid(row=2, column=0, sticky="ew", pady=(10, 6))

        ttk.Button(
            actions,
            text="Restaurar padrões gerais",
            command=self.controller.restore_default_settings,
        ).pack(side="left")

        ttk.Button(
            actions,
            text="Restaurar tamanhos padrão",
            command=self.controller.restore_default_size_settings,
        ).pack(side="left", padx=(6, 0))

        ttk.Button(
            actions,
            text="Salvar configurações",
            style="Accent.TButton",
            command=self.controller.save_settings_from_ui,
        ).pack(side="right")

        self._select_main_section("general")

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _make_section(self, parent: tk.Misc, title: str) -> tuple[ttk.LabelFrame, tk.Frame]:
        box = ttk.LabelFrame(parent, text=title, style="Card.TLabelframe")
        box.pack(fill="both", expand=True, pady=(0, 10))

        inner = tk.Frame(box, bg=theme.active_theme().panel_bg)
        inner.pack(fill="both", expand=True, padx=12, pady=12)
        return box, inner

    def _create_main_selector_button(
        self,
        parent: tk.Misc,
        section_key: str,
        title: str,
        column: int,
    ) -> None:
        t = theme.active_theme()

        btn = tk.Label(
            parent,
            text=title,
            bg=t.panel_alt,
            fg=t.text_muted,
            bd=1,
            relief="solid",
            cursor="hand2",
            font=(theme.FONT_FAMILY, 10),
            padx=12,
            pady=8,
        )
        btn.grid(row=0, column=column, sticky="ew", padx=(0 if column == 0 else 6, 0))

        btn.bind("<Button-1>", lambda _e, key=section_key: self._select_main_section(key))
        btn.bind("<Enter>", lambda _e, key=section_key: self._hover_main_section(key, True))
        btn.bind("<Leave>", lambda _e, key=section_key: self._hover_main_section(key, False))

        self.main_selector_buttons[section_key] = btn

    def _select_main_section(self, section_key: str) -> None:
        t = theme.active_theme()
        self.current_main_section = section_key

        for key, btn in self.main_selector_buttons.items():
            selected = key == section_key
            btn.configure(
                bg=t.primary if selected else t.panel_alt,
                fg="#FFFFFF" if selected else t.text_muted,
                relief="solid",
                bd=1,
            )

        for key, panel in self.main_selector_panels.items():
            panel.grid_forget()
            if key == section_key:
                panel.grid(row=0, column=0, sticky="nsew")

    def _hover_main_section(self, section_key: str, hovering: bool) -> None:
        t = theme.active_theme()

        if section_key == self.current_main_section:
            return

        btn = self.main_selector_buttons[section_key]
        btn.configure(
            bg=t.panel_hover if hovering else t.panel_alt,
            fg=t.text if hovering else t.text_muted,
        )

    def _create_size_selector_button(
        self,
        parent: tk.Misc,
        group_key: str,
        title: str,
        column: int,
    ) -> None:
        t = theme.active_theme()

        btn = tk.Label(
            parent,
            text=title,
            bg=t.panel_alt,
            fg=t.text_muted,
            bd=1,
            relief="solid",
            cursor="hand2",
            font=(theme.FONT_FAMILY, 10),
            padx=12,
            pady=8,
        )
        btn.grid(row=0, column=column, sticky="ew", padx=(0 if column == 0 else 6, 0))

        btn.bind("<Button-1>", lambda _e, key=group_key: self._select_size_group(key))
        btn.bind("<Enter>", lambda _e, key=group_key: self._hover_size_group(key, True))
        btn.bind("<Leave>", lambda _e, key=group_key: self._hover_size_group(key, False))

        self.size_selector_buttons[group_key] = btn

    def _select_size_group(self, group_key: str) -> None:
        t = theme.active_theme()
        self.current_size_group = group_key

        for key, btn in self.size_selector_buttons.items():
            selected = key == group_key
            btn.configure(
                bg=t.primary if selected else t.panel_alt,
                fg="#FFFFFF" if selected else t.text_muted,
                relief="solid",
                bd=1,
            )

        for key, panel in self.size_selector_panels.items():
            panel.pack_forget()
            if key == group_key:
                panel.pack(fill="both", expand=True)

    def _hover_size_group(self, group_key: str, hovering: bool) -> None:
        t = theme.active_theme()

        if group_key == self.current_size_group:
            return

        btn = self.size_selector_buttons[group_key]
        btn.configure(
            bg=t.panel_hover if hovering else t.panel_alt,
            fg=t.text if hovering else t.text_muted,
        )

    # ------------------------------------------------------------------
    # Tabs / Sections
    # ------------------------------------------------------------------
    def _build_general_tab(self) -> None:
        t = theme.active_theme()
        container = tk.Frame(self.tab_general, bg=t.app_bg)
        container.pack(fill="both", expand=True)

        _, inner_text = self._make_section(container, "Padrões de texto")

        ttk.Label(inner_text, text="Modo padrão de maiúsculas/minúsculas").grid(
            row=0, column=0, sticky="w", padx=(0, 6)
        )
        self.cmb_default_case = ttk.Combobox(
            inner_text,
            textvariable=self.controller.default_case_label_var,
            values=self.controller.case_labels,
            width=18,
            state="readonly",
        )
        self.cmb_default_case.grid(row=0, column=1, sticky="w")

        ttk.Label(inner_text, text="Separador padrão da entrada").grid(
            row=1, column=0, sticky="w", padx=(0, 6), pady=(10, 0)
        )
        self.ent_default_separator = ttk.Entry(
            inner_text,
            textvariable=self.controller.default_input_separator_var,
            width=8,
        )
        self.ent_default_separator.grid(row=1, column=1, sticky="w", pady=(10, 0))

        ttk.Label(inner_text, text='Use "\\t" para tab').grid(
            row=1, column=2, sticky="w", padx=(8, 0), pady=(10, 0)
        )

        _, inner_notes = self._make_section(container, "Observações")

        tk.Label(
            inner_notes,
            text=(
                "• O modo de maiúsculas/minúsculas afeta apenas strings comuns.\n"
                "• Campos de tamanho continuam sempre em maiúsculas.\n"
                "• O separador padrão afeta a leitura da entrada."
            ),
            bg=theme.active_theme().panel_bg,
            fg=theme.active_theme().text_muted,
            justify="left",
            anchor="w",
            font=(theme.FONT_FAMILY, 10),
        ).pack(anchor="w")

    def _build_output_tab(self) -> None:
        t = theme.active_theme()
        container = tk.Frame(self.tab_output, bg=t.app_bg)
        container.pack(fill="both", expand=True)

        _, inner_output = self._make_section(container, "Saída")
        inner_output.grid_columnconfigure(1, weight=1)

        ttk.Checkbutton(
            inner_output,
            text="Usar pasta padrão para salvar a saída",
            variable=self.controller.use_default_output_dir_var,
            command=self.controller.update_settings_field_states,
        ).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 8))

        ttk.Label(inner_output, text="Pasta padrão").grid(row=1, column=0, sticky="w", padx=(0, 6))
        self.ent_output_dir = ttk.Entry(
            inner_output,
            textvariable=self.controller.output_dir_var,
            width=60,
        )
        self.ent_output_dir.grid(row=1, column=1, sticky="ew")

        self.btn_pick_output_dir = ttk.Button(
            inner_output,
            text="Escolher...",
            command=self.controller.pick_default_output_folder,
        )
        self.btn_pick_output_dir.grid(row=1, column=2, sticky="w", padx=(6, 0))

        ttk.Checkbutton(
            inner_output,
            text="Usar nome padrão da lista",
            variable=self.controller.use_default_list_name_var,
            command=self.controller.update_settings_field_states,
        ).grid(row=2, column=0, columnspan=3, sticky="w", pady=(12, 8))

        ttk.Label(inner_output, text="Nome padrão").grid(row=3, column=0, sticky="w", padx=(0, 6))
        self.ent_default_name = ttk.Entry(
            inner_output,
            textvariable=self.controller.default_list_name_var,
            width=30,
        )
        self.ent_default_name.grid(row=3, column=1, sticky="w")

    def _build_json_tab(self) -> None:
        t = theme.active_theme()
        container = tk.Frame(self.tab_json, bg=t.app_bg)
        container.pack(fill="both", expand=True)

        _, inner_json = self._make_section(container, "JSON")

        ttk.Checkbutton(
            inner_json,
            text="Mostrar aba de JSON",
            variable=self.controller.show_json_tab_var,
        ).pack(anchor="w", pady=(0, 4))

        ttk.Checkbutton(
            inner_json,
            text="Mostrar botão Gerar JSON",
            variable=self.controller.show_generate_json_button_var,
        ).pack(anchor="w", pady=4)

        ttk.Checkbutton(
            inner_json,
            text="Mostrar botão Copiar JSON",
            variable=self.controller.show_copy_json_button_var,
        ).pack(anchor="w", pady=(4, 0))

    def _build_sizes_tab(self) -> None:
        t = theme.active_theme()

        container = tk.Frame(self.tab_sizes, bg=t.app_bg)
        container.pack(fill="both", expand=True)

        outer, outer_inner = self._make_section(container, "Cadastro de tamanhos")
        outer_inner.pack_forget()

        selector_wrap = tk.Frame(outer, bg=t.panel_bg)
        selector_wrap.pack(fill="x", padx=12, pady=(12, 0))

        selector_wrap.grid_columnconfigure(0, weight=1)
        selector_wrap.grid_columnconfigure(1, weight=1)
        selector_wrap.grid_columnconfigure(2, weight=1)

        self.size_selector_buttons = {}
        self.size_selector_panels = {}

        options = [
            ("male", "Masculino"),
            ("female", "Feminino"),
            ("child", "Infantil"),
        ]

        for col, (group_key, title) in enumerate(options):
            self._create_size_selector_button(selector_wrap, group_key, title, col)

        content_wrap = tk.Frame(outer, bg=t.panel_bg)
        content_wrap.pack(fill="both", expand=True, padx=12, pady=12)

        for group_key, title in options:
            panel = tk.Frame(content_wrap, bg=t.panel_bg)
            self.size_selector_panels[group_key] = panel
            self._build_single_size_tab(panel, group_key)

        self._select_size_group("male")

        notes = tk.Frame(container, bg=t.app_bg)
        notes.pack(fill="both", expand=True, pady=(10, 0))

        _, inner_notes = self._make_section(notes, "Observações")

        tk.Label(
            inner_notes,
            text=(
                "Base sizes = tamanhos-base\n"
                "Prefixes = prefixos\n"
                "Suffixes = sufixos\n"
                "Os campos de tamanho permanecem sempre em maiúsculas."
            ),
            bg=theme.active_theme().panel_bg,
            fg=theme.active_theme().text_muted,
            justify="left",
            anchor="w",
            font=(theme.FONT_FAMILY, 10),
        ).pack(anchor="w")

        tk.Label(
            inner_notes,
            textvariable=self.controller.size_summary_var,
            bg=theme.active_theme().panel_bg,
            fg=theme.active_theme().text,
            justify="left",
            anchor="w",
            font=(theme.FONT_FAMILY, 9),
        ).pack(anchor="w", pady=(10, 0))

    def _build_single_size_tab(self, parent: tk.Misc, group_key: str) -> None:
        vars_map = self.controller.size_group_vars[group_key]

        wrap = tk.Frame(parent, bg=theme.active_theme().panel_bg)
        wrap.pack(fill="both", expand=True, padx=16, pady=16)
        wrap.grid_columnconfigure(1, weight=1)

        ttk.Label(wrap, text="Tamanhos-base").grid(row=0, column=0, sticky="w", padx=(0, 8), pady=(0, 8))
        ttk.Entry(
            wrap,
            textvariable=vars_map["base_sizes"],
            width=60,
        ).grid(row=0, column=1, sticky="ew", pady=(0, 8))

        ttk.Label(wrap, text="Prefixos").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=(0, 8))
        ttk.Entry(
            wrap,
            textvariable=vars_map["prefixes"],
            width=60,
        ).grid(row=1, column=1, sticky="ew", pady=(0, 8))

        ttk.Label(wrap, text="Sufixos").grid(row=2, column=0, sticky="w", padx=(0, 8))
        ttk.Entry(
            wrap,
            textvariable=vars_map["suffixes"],
            width=60,
        ).grid(row=2, column=1, sticky="ew")

    def _build_appearance_tab(self) -> None:
        t = theme.active_theme()
        container = tk.Frame(self.tab_appearance, bg=t.app_bg)
        container.pack(fill="both", expand=True)

        _, inner_appearance = self._make_section(container, "Tema da interface")

        ttk.Label(inner_appearance, text="Tema").grid(row=0, column=0, sticky="w", padx=(0, 8))
        self.cmb_theme = ttk.Combobox(
            inner_appearance,
            textvariable=self.controller.theme_name_var,
            values=self.controller.theme_names,
            width=24,
            state="readonly",
        )
        self.cmb_theme.grid(row=0, column=1, sticky="w")
        self.cmb_theme.bind(
            "<<ComboboxSelected>>",
            lambda _e: self.controller.apply_theme(self.cmb_theme.get(), persist=True),
        )

        tk.Label(
            inner_appearance,
            text=(
                "Você pode manter o tema atual do Texpad ou usar um tema inspirado "
                "na interface do SisBolt."
            ),
            bg=theme.active_theme().panel_bg,
            fg=theme.active_theme().text_muted,
            justify="left",
            anchor="w",
            font=(theme.FONT_FAMILY, 10),
            wraplength=700,
        ).grid(row=1, column=0, columnspan=2, sticky="w", pady=(12, 0))

    # ------------------------------------------------------------------
    # Runtime bindings / refresh
    # ------------------------------------------------------------------
    def bind_runtime_widgets(self) -> None:
        self.controller.bind_settings_widgets(
            ent_output_dir=self.ent_output_dir,
            btn_pick_output_dir=self.btn_pick_output_dir,
            ent_default_name=self.ent_default_name,
        )

    def refresh(self) -> None:
        self.controller.refresh_home_dashboard()