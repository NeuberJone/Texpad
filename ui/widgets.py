from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from ui import theme


def make_card(parent: tk.Misc) -> tk.Frame:
    t = theme.active_theme()
    return tk.Frame(
        parent,
        bg=t.panel_bg,
        highlightbackground=t.border,
        highlightthickness=1,
        bd=0,
    )


def make_inner(parent: tk.Misc, *, bg: str | None = None) -> tk.Frame:
    t = theme.active_theme()
    return tk.Frame(parent, bg=bg or t.panel_bg, bd=0, highlightthickness=0)


def make_sidebar_button(
    parent: tk.Misc,
    *,
    text: str,
    command,
) -> tk.Button:
    t = theme.active_theme()
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=t.sidebar_bg,
        fg=t.text_muted,
        activebackground=t.sidebar_hover,
        activeforeground=t.text,
        relief="flat",
        bd=0,
        highlightthickness=0,
        anchor="w",
        cursor="hand2",
        font=(theme.FONT_FAMILY, 10),
        padx=12,
        pady=10,
    )


def set_sidebar_button_active(button: tk.Button, active: bool) -> None:
    t = theme.active_theme()
    button.configure(
        bg=(t.sidebar_active if active else t.sidebar_bg),
        fg=(t.text if active else t.text_muted),
        activebackground=(t.sidebar_active if active else t.sidebar_hover),
        activeforeground=t.text,
    )


def make_primary_button(parent: tk.Misc, *, text: str, command) -> tk.Button:
    t = theme.active_theme()
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=t.primary,
        fg="#FFFFFF",
        activebackground=t.primary_hover,
        activeforeground="#FFFFFF",
        relief="flat",
        bd=0,
        cursor="hand2",
        font=(theme.FONT_FAMILY, 10, "bold"),
        padx=14,
        pady=7,
    )


def make_secondary_button(parent: tk.Misc, *, text: str, command) -> tk.Button:
    t = theme.active_theme()
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=t.panel_alt,
        fg=t.text,
        activebackground=t.panel_hover,
        activeforeground=t.text,
        relief="flat",
        bd=0,
        cursor="hand2",
        font=(theme.FONT_FAMILY, 10),
        padx=12,
        pady=7,
    )


def make_quick_button(parent: tk.Misc, *, text: str, command) -> tk.Button:
    t = theme.active_theme()
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=t.panel_alt,
        fg=t.text,
        activebackground=t.panel_hover,
        activeforeground=t.text,
        relief="flat",
        bd=0,
        cursor="hand2",
        font=(theme.FONT_FAMILY, 10),
        padx=12,
        pady=18,
    )


def make_title_label(parent: tk.Misc, text: str) -> tk.Label:
    t = theme.active_theme()
    return tk.Label(
        parent,
        text=text,
        bg=t.panel_bg,
        fg=t.text,
        font=(theme.FONT_FAMILY, 12, "bold"),
        anchor="w",
    )


def make_section_label(parent: tk.Misc, text: str) -> tk.Label:
    t = theme.active_theme()
    return tk.Label(
        parent,
        text=text,
        bg=t.panel_bg,
        fg=t.text_muted,
        font=(theme.FONT_FAMILY, 9, "bold"),
        anchor="w",
    )


def make_muted_label(
    parent: tk.Misc,
    text: str = "",
    *,
    bg: str | None = None,
    wraplength: int | None = None,
    justify: str = "left",
) -> tk.Label:
    t = theme.active_theme()
    kwargs = {}
    if wraplength is not None:
        kwargs["wraplength"] = wraplength

    return tk.Label(
        parent,
        text=text,
        bg=bg or t.panel_bg,
        fg=t.text_muted,
        font=(theme.FONT_FAMILY, 10),
        justify=justify,
        anchor="w",
        **kwargs,
    )


def build_metric_card(
    parent: tk.Misc,
    *,
    title: str,
    value_var: tk.StringVar,
    subtitle: str,
    accent: str,
) -> tk.Frame:
    t = theme.active_theme()
    card = make_card(parent)

    tk.Label(
        card,
        text=title,
        bg=t.panel_bg,
        fg=t.text_muted,
        font=(theme.FONT_FAMILY, 9, "bold"),
        anchor="w",
    ).pack(fill="x", padx=18, pady=(16, 6))

    tk.Label(
        card,
        textvariable=value_var,
        bg=t.panel_bg,
        fg=accent,
        font=(theme.FONT_FAMILY, 22, "bold"),
        anchor="w",
    ).pack(fill="x", padx=18)

    tk.Label(
        card,
        text=subtitle,
        bg=t.panel_bg,
        fg=t.text_muted,
        font=(theme.FONT_FAMILY, 10),
        anchor="w",
    ).pack(fill="x", padx=18, pady=(4, 16))

    return card


def build_info_row(parent: tk.Misc, *, label: str, value_var: tk.StringVar) -> tk.Frame:
    t = theme.active_theme()
    row = tk.Frame(parent, bg=t.panel_bg)
    row.pack(fill="x", padx=18, pady=4)

    tk.Label(
        row,
        text=label,
        bg=t.panel_bg,
        fg=t.text_muted,
        font=(theme.FONT_FAMILY, 10),
        width=14,
        anchor="w",
    ).pack(side="left")

    tk.Label(
        row,
        textvariable=value_var,
        bg=t.panel_bg,
        fg=t.text,
        font=(theme.FONT_FAMILY, 10),
        anchor="w",
    ).pack(side="left", fill="x", expand=True)

    return row


def build_alert_box(parent: tk.Misc, *, textvariable: tk.StringVar) -> tk.Frame:
    t = theme.active_theme()
    alert_box = tk.Frame(
        parent,
        bg=t.alert_bg,
        highlightbackground=t.alert_border,
        highlightthickness=1,
        bd=0,
    )

    tk.Label(
        alert_box,
        textvariable=textvariable,
        bg=t.alert_bg,
        fg=t.alert_text,
        justify="left",
        wraplength=520,
        anchor="w",
        font=(theme.FONT_FAMILY, 10, "bold"),
    ).pack(fill="x", padx=12, pady=12)

    return alert_box


def create_text_area(parent: tk.Misc, *, background: str | None = None) -> tuple[tk.Frame, tk.Text]:
    t = theme.active_theme()
    bg = background or t.editor_bg

    holder = tk.Frame(parent, bg=bg, bd=0, highlightthickness=0)

    text = tk.Text(
        holder,
        wrap="none",
        font=(theme.FONT_MONO, 10),
        undo=True,
        maxundo=-1,
        autoseparators=True,
        bg=bg,
        fg=t.text,
        insertbackground=t.text,
        selectbackground=t.selection,
        selectforeground="#FFFFFF",
        relief="flat",
        bd=0,
        padx=8,
        pady=8,
    )

    yscroll = ttk.Scrollbar(holder, orient="vertical", command=text.yview)
    xscroll = ttk.Scrollbar(holder, orient="horizontal", command=text.xview)

    text.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)

    holder.rowconfigure(0, weight=1)
    holder.columnconfigure(0, weight=1)

    text.grid(row=0, column=0, sticky="nsew")
    yscroll.grid(row=0, column=1, sticky="ns")
    xscroll.grid(row=1, column=0, sticky="ew")

    return holder, text