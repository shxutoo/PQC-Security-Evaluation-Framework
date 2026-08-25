import customtkinter as ctk
import matplotlib

matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from src.gui.components import page_header, panel, section_title
from src.gui.theme import (
    BG,
    PANEL,
    GREEN,
    DARK_GREEN,
    HOVER,
    TEXT,
    MUTED,
)


class BenchmarksPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")

        self.controller = controller
        self.figures = []

        self.pack(fill="both", expand=True)

        page_header(
            self,
            "> BENCHMARKS",
            "Run, inspect and visualize cryptographic benchmark results",
        )

        actions = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )
        actions.pack(fill="x", pady=(0, 12))

        self.run_button = ctk.CTkButton(
            actions,
            text="[ RUN BENCHMARK ]",
            command=self.run_benchmark,
            height=38,
            fg_color=BG,
            hover_color=HOVER,
            border_width=1,
            border_color=GREEN,
            text_color=GREEN,
            font=ctk.CTkFont(size=11, weight="bold"),
        )
        self.run_button.pack(side="left")

        self.status_label = ctk.CTkLabel(
            actions,
            text=controller.last_benchmark_status,
            font=ctk.CTkFont(size=10),
            text_color=MUTED,
        )
        self.status_label.pack(side="left", padx=12)

        self.scroll = ctk.CTkScrollableFrame(
            self,
            fg_color=BG,
            scrollbar_button_color=DARK_GREEN,
            scrollbar_button_hover_color=GREEN,
        )
        self.scroll.pack(fill="both", expand=True)

        if not controller.results:
            self._show_empty()
            return

        self._build_table()
        self._build_charts()

    def _show_empty(self):
        empty = panel(self.scroll)
        empty.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            empty,
            text="NO BENCHMARK RESULTS FOUND",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=MUTED,
        ).pack(padx=20, pady=(25, 5))

        ctk.CTkLabel(
            empty,
            text="Press RUN BENCHMARK to generate fresh results.",
            font=ctk.CTkFont(size=11),
            text_color=MUTED,
        ).pack(padx=20, pady=(0, 25))

    def _build_table(self):
        table = panel(self.scroll)
        table.pack(fill="x")

        columns = [
            "ALGORITHM",
            "KEYGEN",
            "SIGN",
            "VERIFY",
            "PUBLIC KEY",
            "PRIVATE KEY",
            "SIGNATURE",
        ]

        for column in range(len(columns)):
            table.grid_columnconfigure(column, weight=1)

        for column, text in enumerate(columns):
            ctk.CTkLabel(
                table,
                text=text,
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color=GREEN,
            ).grid(
                row=0,
                column=column,
                padx=6,
                pady=10,
                sticky="w",
            )

        for row_number, result in enumerate(
            self.controller.results,
            start=1,
        ):
            values = [
                result["algorithm"],
                self.format_time(result["keygen_time"]),
                self.format_time(result["sign_time"]),
                self.format_time(result["verify_time"]),
                self.format_bytes(result["public_key_size"]),
                self.format_bytes(result["private_key_size"]),
                self.format_bytes(result["signature_size"]),
            ]

            for column, value in enumerate(values):
                ctk.CTkLabel(
                    table,
                    text=value,
                    font=ctk.CTkFont(
                        size=10,
                        weight="bold" if column == 0 else "normal",
                    ),
                    text_color=GREEN if column == 0 else TEXT,
                ).grid(
                    row=row_number,
                    column=column,
                    padx=6,
                    pady=7,
                    sticky="w",
                )

        notes = panel(self.scroll)
        notes.pack(fill="x", pady=(12, 0))
        section_title(notes, "BENCHMARK NOTES", pady=(10, 5))

        ctk.CTkLabel(
            notes,
            text=(
                "> Lower execution time indicates better performance.\n"
                "> Smaller key/signature sizes indicate lower storage overhead.\n"
                "> Charts use the most recently loaded benchmark results."
            ),
            font=ctk.CTkFont(size=11),
            text_color=MUTED,
            justify="left",
        ).pack(anchor="w", padx=15, pady=(0, 12))

    def _build_charts(self):
        charts = ctk.CTkFrame(
            self.scroll,
            fg_color="transparent",
        )
        charts.pack(fill="x", pady=(15, 10))

        charts.grid_columnconfigure((0, 1), weight=1)

        specs = [
            (
                0,
                0,
                "Key Generation Time",
                "keygen_time",
                lambda value: value * 1000,
                "ms",
            ),
            (
                0,
                1,
                "Signing Time",
                "sign_time",
                lambda value: value * 1000,
                "ms",
            ),
            (
                1,
                0,
                "Verification Time",
                "verify_time",
                lambda value: value * 1000,
                "ms",
            ),
            (
                1,
                1,
                "Signature Size",
                "signature_size",
                lambda value: value,
                "bytes",
            ),
        ]

        for row, column, title, key, transform, unit in specs:
            chart_panel = panel(charts)
            chart_panel.grid(
                row=row,
                column=column,
                sticky="nsew",
                padx=5,
                pady=5,
            )

            self._embed_bar_chart(
                chart_panel,
                title,
                key,
                transform,
                unit,
            )

    def _embed_bar_chart(
        self,
        parent,
        title,
        key,
        transform,
        unit,
    ):
        algorithms = [
            item["algorithm"]
            for item in self.controller.results
        ]

        values = [
            transform(item[key])
            for item in self.controller.results
        ]

        figure, axis = plt.subplots(
            figsize=(4.4, 2.4),
            dpi=100,
        )
        self.figures.append(figure)

        figure.patch.set_facecolor(PANEL)
        axis.set_facecolor(PANEL)

        axis.bar(
            algorithms,
            values,
            color=GREEN,
        )

        axis.set_title(
            title,
            color=GREEN,
            fontsize=9,
            fontweight="bold",
        )

        axis.set_ylabel(
            unit,
            color=MUTED,
            fontsize=8,
        )

        axis.tick_params(
            axis="x",
            colors=TEXT,
            labelsize=7,
        )
        axis.tick_params(
            axis="y",
            colors=MUTED,
            labelsize=7,
        )

        for spine in axis.spines.values():
            spine.set_color(DARK_GREEN)

        axis.grid(
            axis="y",
            alpha=0.15,
        )

        figure.tight_layout()

        canvas = FigureCanvasTkAgg(
            figure,
            master=parent,
        )
        canvas.draw()
        canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=6,
            pady=6,
        )

    def run_benchmark(self):
        self.run_button.configure(
            state="disabled",
            text="[ RUNNING... ]",
        )

        self.status_label.configure(
            text="Benchmark in progress...",
            text_color=MUTED,
        )

        self.controller.run_benchmark_async(
            self._benchmark_finished
        )

    def _benchmark_finished(self, success, output):
        if not self.winfo_exists():
            return

        if success:
            # Rebuild the page from the freshly loaded JSON.
            self.controller.show_page(
                BenchmarksPage
            )
            return

        self.run_button.configure(
            state="normal",
            text="[ RUN BENCHMARK ]",
        )

        message = output.splitlines()[-1] if output else "Unknown error."

        self.status_label.configure(
            text=f"Failed: {message}",
            text_color=MUTED,
        )

    def destroy(self):
        for figure in self.figures:
            plt.close(figure)

        super().destroy()

    @staticmethod
    def format_time(value):
        return f"{value * 1000:.3f} ms"

    @staticmethod
    def format_bytes(value):
        if value >= 1024:
            return f"{value / 1024:.2f} KB"

        return f"{value} B"
