from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from ui import theme
from ui.widgets import create_text_area, make_card


class EditorView(tk.Frame):
    def __init__(self, parent: tk.Misc, controller) -> None:
        super().__init__(parent, bg=theme.APP_BG)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self._build()

    def _build(self) -> None:
        self._build_file_bar()
        self._build_prepare_box()
        self._build_search_box()
        self._build_editor_body()
        self._build_footer_actions()

    # ------------------------------------------------------------------
    # Top bars
    # ------------------------------------------------------------------
    def _build_file_bar(self) -> None:
        row_files = make_card(self)
        row_files.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        files_inner = tk.Frame(row_files, bg=theme.PANEL_BG)
        files_inner.pack(fill="x", padx=16, pady=12)

        self.btn_open_input = tk.Button(
            files_inner,
            text="Abrir Lista",
            command=self.controller.open_input_file,
            bg=theme.PANEL_ALT,
            fg=theme.TEXT,
            activebackground=theme.PANEL_HOVER,
            activeforeground=theme.TEXT,
            relief="flat",
            bd=0,
            cursor="hand2",
            font=(theme.FONT_FAMILY, 10),
            padx=12,
            pady=7,
        )
        self.btn_open_input.pack(side="left")

        self.btn_save_input = tk.Button(
            files_inner,
            text="Salvar Entrada",
            command=self.controller.save_input_file,
            bg=theme.PANEL_ALT,
            fg=theme.TEXT,
            activebackground=theme.PANEL_HOVER,
            activeforeground=theme.TEXT,
            relief="flat",
            bd=0,
            cursor="hand2",
            font=(theme.FONT_FAMILY, 10),
            padx=12,
            pady=7,
        )
        self.btn_save_input.pack(side="left", padx=(6, 0))

        self.btn_save_input_as = tk.Button(
            files_inner,
            text="Salvar Entrada Como",
            command=self.controller.save_input_as_file,
            bg=theme.PANEL_ALT,
            fg=theme.TEXT,
            activebackground=theme.PANEL_HOVER,
            activeforeground=theme.TEXT,
            relief="flat",
            bd=0,
            cursor="hand2",
            font=(theme.FONT_FAMILY, 10),
            padx=12,
            pady=7,
        )
        self.btn_save_input_as.pack(side="left", padx=(6, 0))

        self.btn_undo = tk.Button(
            files_inner,
            text="Desfazer",
            command=self.controller.undo_last_change,
            bg=theme.PANEL_ALT,
            fg=theme.TEXT,
            activebackground=theme.PANEL_HOVER,
            activeforeground=theme.TEXT,
            relief="flat",
            bd=0,
            cursor="hand2",
            font=(theme.FONT_FAMILY, 10),
            padx=12,
            pady=7,
        )
        self.btn_undo.pack(side="left", padx=(14, 0))

        self.btn_open_backups = tk.Button(
            files_inner,
            text="Abrir pasta de backups",
            command=self.controller.open_backups_folder,
            bg=theme.PANEL_ALT,
            fg=theme.TEXT,
            activebackground=theme.PANEL_HOVER,
            activeforeground=theme.TEXT,
            relief="flat",
            bd=0,
            cursor="hand2",
            font=(theme.FONT_FAMILY, 10),
            padx=12,
            pady=7,
        )
        self.btn_open_backups.pack(side="left", padx=(6, 0))

        tk.Label(
            files_inner,
            textvariable=self.controller.current_file_var,
            bg=theme.PANEL_BG,
            fg=theme.TEXT_MUTED,
            font=(theme.FONT_FAMILY, 9),
            anchor="e",
        ).pack(side="right")

    def _build_prepare_box(self) -> None:
        prep_box = ttk.LabelFrame(self, text="Preparação da lista", style="Card.TLabelframe")
        prep_box.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        prep_inner = tk.Frame(prep_box, bg=theme.PANEL_BG)
        prep_inner.pack(fill="x", padx=12, pady=12)

        ttk.Label(prep_inner, text="Separador da entrada").grid(row=0, column=0, sticky="w", padx=(0, 6))
        self.ent_separator = ttk.Entry(prep_inner, textvariable=self.controller.editor_separator_var, width=8)
        self.ent_separator.grid(row=0, column=1, sticky="w")

        ttk.Label(prep_inner, text='Use "\\t" para tab').grid(row=0, column=2, sticky="w", padx=(8, 18))

        self.btn_reset_separator = ttk.Button(
            prep_inner,
            text="Padrão (,)",
            command=self.controller.set_default_separator,
        )
        self.btn_reset_separator.grid(row=0, column=3, sticky="w", padx=(0, 8))

        self.btn_clean_spaces = ttk.Button(
            prep_inner,
            text="Remover espaços desnecessários",
            command=self.controller.clean_unnecessary_spaces,
        )
        self.btn_clean_spaces.grid(row=0, column=4, sticky="w", padx=(0, 18))

        ttk.Label(prep_inner, text="Maiúsculas / minúsculas").grid(row=0, column=5, sticky="w", padx=(0, 6))
        self.cmb_case_mode = ttk.Combobox(
            prep_inner,
            textvariable=self.controller.editor_case_label_var,
            values=self.controller.case_labels,
            width=18,
            state="readonly",
        )
        self.cmb_case_mode.grid(row=0, column=6, sticky="w")

    def _build_search_box(self) -> None:
        search_box = ttk.LabelFrame(self, text="Localizar / Localizar e substituir", style="Card.TLabelframe")
        search_box.grid(row=2, column=0, sticky="ew", pady=(0, 10))

        search_inner = tk.Frame(search_box, bg=theme.PANEL_BG)
        search_inner.pack(fill="x", padx=12, pady=12)

        ttk.Label(search_inner, text="Localizar").grid(row=0, column=0, sticky="w", padx=(0, 6))
        self.ent_find = ttk.Entry(search_inner, textvariable=self.controller.find_var, width=28)
        self.ent_find.grid(row=0, column=1, sticky="w")

        ttk.Label(search_inner, text="Substituir por").grid(row=0, column=2, sticky="w", padx=(16, 6))
        self.ent_replace = ttk.Entry(search_inner, textvariable=self.controller.replace_var, width=28)
        self.ent_replace.grid(row=0, column=3, sticky="w")

        ttk.Checkbutton(
            search_inner,
            text="Diferenciar maiúsculas/minúsculas",
            variable=self.controller.search_match_case_var,
        ).grid(row=0, column=4, sticky="w", padx=(16, 10))

        btns_search = tk.Frame(search_inner, bg=theme.PANEL_BG)
        btns_search.grid(row=0, column=5, sticky="e")

        ttk.Button(btns_search, text="Localizar", command=self.controller.find_next_from_cursor).pack(side="left")
        ttk.Button(btns_search, text="Anterior", command=self.controller.find_previous).pack(side="left", padx=(6, 0))
        ttk.Button(btns_search, text="Próximo", command=self.controller.find_next).pack(side="left", padx=(6, 0))
        ttk.Button(btns_search, text="Substituir", command=self.controller.replace_current).pack(side="left", padx=(12, 0))
        ttk.Button(btns_search, text="Substituir tudo", command=self.controller.replace_all).pack(side="left", padx=(6, 0))
        ttk.Button(btns_search, text="Limpar destaque", command=self.controller.clear_search_highlight).pack(
            side="left", padx=(12, 0)
        )

    # ------------------------------------------------------------------
    # Main editor body
    # ------------------------------------------------------------------
    def _build_editor_body(self) -> None:
        body = tk.Frame(self, bg=theme.APP_BG)
        body.grid(row=3, column=0, sticky="nsew")
        body.grid_rowconfigure(0, weight=1)
        body.grid_columnconfigure(0, weight=1)
        body.grid_columnconfigure(1, weight=1)

        left = make_card(body)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        left.grid_rowconfigure(1, weight=1)
        left.grid_columnconfigure(0, weight=1)

        right = make_card(body)
        right.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        right.grid_rowconfigure(1, weight=1)
        right.grid_columnconfigure(0, weight=1)

        tk.Label(
            left,
            text="Entrada / edição",
            bg=theme.PANEL_BG,
            fg=theme.TEXT,
            font=(theme.FONT_FAMILY, 11, "bold"),
            anchor="w",
        ).grid(row=0, column=0, sticky="ew", padx=14, pady=(14, 8))

        input_holder, self.txt_in = create_text_area(left, background=theme.EDITOR_BG)
        input_holder.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0, 14))

        tk.Label(
            right,
            text="Saída",
            bg=theme.PANEL_BG,
            fg=theme.TEXT,
            font=(theme.FONT_FAMILY, 11, "bold"),
            anchor="w",
        ).grid(row=0, column=0, sticky="ew", padx=14, pady=(14, 8))

        self.outputs_nb = ttk.Notebook(right)
        self.outputs_nb.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0, 14))

        self.tab_list = tk.Frame(self.outputs_nb, bg=theme.PANEL_BG)
        self.tab_json = tk.Frame(self.outputs_nb, bg=theme.PANEL_BG)

        self.outputs_nb.add(self.tab_list, text="Lista organizada")
        self.outputs_nb.add(self.tab_json, text="Prévia JSON")

        output_holder, self.txt_out = create_text_area(self.tab_list, background=theme.EDITOR_ALT)
        output_holder.pack(fill="both", expand=True)

        json_holder, self.txt_json = create_text_area(self.tab_json, background=theme.EDITOR_ALT)
        json_holder.pack(fill="both", expand=True)

        self.controller.bind_editor_widgets(
            txt_in=self.txt_in,
            txt_out=self.txt_out,
            txt_json=self.txt_json,
            notebook=self.outputs_nb,
            tab_list=self.tab_list,
            tab_json=self.tab_json,
            ent_find=self.ent_find,
            ent_replace=self.ent_replace,
        )

    # ------------------------------------------------------------------
    # Bottom actions
    # ------------------------------------------------------------------
    def _build_footer_actions(self) -> None:
        footer = tk.Frame(self, bg=theme.APP_BG)
        footer.grid(row=4, column=0, sticky="ew", pady=(10, 0))

        left_actions = tk.Frame(footer, bg=theme.APP_BG)
        left_actions.pack(side="left")

        right_actions = tk.Frame(footer, bg=theme.APP_BG)
        right_actions.pack(side="right")

        self.btn_clear_all = ttk.Button(left_actions, text="Limpar tudo", command=self.controller.clear_all)
        self.btn_clear_all.pack(side="left")

        self.btn_copy_output = ttk.Button(left_actions, text="Copiar saída", command=self.controller.copy_output)
        self.btn_copy_output.pack(side="left", padx=(6, 0))

        self.btn_save_output = ttk.Button(left_actions, text="Salvar saída", command=self.controller.save_output)
        self.btn_save_output.pack(side="left", padx=(6, 0))

        self.btn_copy_json = ttk.Button(left_actions, text="Copiar JSON", command=self.controller.copy_json)
        self.btn_copy_json.pack(side="left", padx=(6, 0))

        self.btn_generate_json = ttk.Button(right_actions, text="Gerar JSON", command=self.controller.generate_json)
        self.btn_generate_json.pack(side="right")

        self.btn_process = ttk.Button(
            right_actions,
            text="Processar",
            style="Accent.TButton",
            command=self.controller.process_and_preview,
        )
        self.btn_process.pack(side="right", padx=(0, 6))

    # ------------------------------------------------------------------
    # Runtime toggles
    # ------------------------------------------------------------------
    def apply_runtime_preferences(self) -> None:
        json_widget = str(self.tab_json)
        current_tabs = self.outputs_nb.tabs()

        if self.controller.show_json_tab_var.get():
            if json_widget not in current_tabs:
                self.outputs_nb.add(self.tab_json, text="Prévia JSON")
        else:
            if json_widget in current_tabs:
                if self.outputs_nb.select() == json_widget:
                    self.outputs_nb.select(self.tab_list)
                self.outputs_nb.forget(self.tab_json)

        if self.controller.show_copy_json_button_var.get():
            if not self.btn_copy_json.winfo_manager():
                self.btn_copy_json.pack(side="left", padx=(6, 0))
        else:
            if self.btn_copy_json.winfo_manager():
                self.btn_copy_json.pack_forget()

        if self.controller.show_generate_json_button_var.get():
            if not self.btn_generate_json.winfo_manager():
                self.btn_generate_json.pack(side="right")
        else:
            if self.btn_generate_json.winfo_manager():
                self.btn_generate_json.pack_forget()