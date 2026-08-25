import customtkinter as ctk

from src.gui.theme import (
    BG,
    SIDEBAR,
    PANEL,
    GREEN,
    DARK_GREEN,
    HOVER,
    TEXT,
    MUTED,
)


class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, navigation):
        super().__init__(
            parent,
            width=210,
            corner_radius=0,
            fg_color=SIDEBAR,
        )
        self.grid_propagate(False)

        ctk.CTkLabel(
            self,
            text="PQC // SEC",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=GREEN,
        ).pack(padx=20, pady=(25, 5))

        ctk.CTkLabel(
            self,
            text="SECURITY EVALUATION",
            font=ctk.CTkFont(size=10),
            text_color=MUTED,
        ).pack(padx=20, pady=(0, 25))

        for text, command in navigation:
            ctk.CTkButton(
                self,
                text=text,
                command=command,
                height=40,
                corner_radius=6,
                anchor="w",
                fg_color=BG,
                hover_color=HOVER,
                border_width=1,
                border_color=DARK_GREEN,
                text_color=GREEN,
                font=ctk.CTkFont(size=12, weight="bold"),
            ).pack(fill="x", padx=12, pady=3)

        status = ctk.CTkFrame(
            self,
            fg_color=PANEL,
            corner_radius=8,
            border_width=1,
            border_color=DARK_GREEN,
        )
        status.pack(side="bottom", fill="x", padx=12, pady=15)

        ctk.CTkLabel(
            status,
            text="SYSTEM STATUS",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=MUTED,
        ).pack(anchor="w", padx=12, pady=(10, 2))

        ctk.CTkLabel(
            status,
            text="●  ONLINE",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=GREEN,
        ).pack(anchor="w", padx=12, pady=(0, 10))


class AlgorithmSelector(ctk.CTkFrame):
    def __init__(self, parent, value, command):
        # The outer frame owns the green outline. The menu itself has no border,
        # which prevents the broken/partial-border look from the older selector.
        super().__init__(
            parent,
            width=280,
            height=42,
            fg_color=GREEN,
            corner_radius=7,
        )
        self.pack_propagate(False)

        self.menu = ctk.CTkOptionMenu(
            self,
            values=["RSA", "ECDSA", "MLDSA", "SPHINCS"],
            command=command,
            width=278,
            height=40,
            fg_color=BG,
            button_color=BG,
            button_hover_color=HOVER,
            dropdown_fg_color=BG,
            dropdown_hover_color=HOVER,
            dropdown_text_color=GREEN,
            text_color=GREEN,
            corner_radius=6,
            font=ctk.CTkFont(size=11, weight="bold"),
            dropdown_font=ctk.CTkFont(size=11, weight="bold"),
        )
        self.menu.set(value)
        self.menu.pack(fill="both", expand=True, padx=1, pady=1)

    def set(self, value):
        self.menu.set(value)


def page_header(parent, title, subtitle):
    ctk.CTkLabel(
        parent,
        text=title,
        font=ctk.CTkFont(size=26, weight="bold"),
        text_color=GREEN,
    ).pack(anchor="w")

    ctk.CTkLabel(
        parent,
        text=subtitle,
        font=ctk.CTkFont(size=13),
        text_color=MUTED,
    ).pack(anchor="w", pady=(0, 18))


def panel(parent, **kwargs):
    options = {
        "fg_color": PANEL,
        "corner_radius": 10,
        "border_width": 1,
        "border_color": DARK_GREEN,
    }
    options.update(kwargs)
    return ctk.CTkFrame(parent, **options)


def info_row(parent, label, value):
    row = ctk.CTkFrame(parent, fg_color="transparent")
    row.pack(fill="x", padx=15, pady=3)

    ctk.CTkLabel(
        row,
        text=label,
        font=ctk.CTkFont(size=11),
        text_color=MUTED,
    ).pack(side="left")

    ctk.CTkLabel(
        row,
        text=str(value),
        font=ctk.CTkFont(size=11, weight="bold"),
        text_color=GREEN,
    ).pack(side="right")


def section_title(parent, text, pady=(14, 8)):
    ctk.CTkLabel(
        parent,
        text=text,
        font=ctk.CTkFont(size=12, weight="bold"),
        text_color=GREEN,
    ).pack(anchor="w", padx=15, pady=pady)


def divider(parent, pady=12):
    ctk.CTkFrame(
        parent,
        height=1,
        fg_color=DARK_GREEN,
    ).pack(fill="x", padx=15, pady=pady)


def stat_card(parent, column, title, value):
    card = panel(parent)
    card.grid(row=0, column=column, sticky="nsew", padx=4)

    ctk.CTkLabel(
        card,
        text=title,
        font=ctk.CTkFont(size=10, weight="bold"),
        text_color=MUTED,
    ).pack(pady=(12, 2))

    ctk.CTkLabel(
        card,
        text=value,
        font=ctk.CTkFont(size=18, weight="bold"),
        text_color=GREEN,
    ).pack(pady=(0, 12))
