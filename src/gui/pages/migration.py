import customtkinter as ctk

from src.analysis.recommendation import generate_recommendation
from src.gui.components import (
    AlgorithmSelector,
    divider,
    info_row,
    page_header,
    panel,
)
from src.gui.theme import (
    BG,
    PANEL,
    GREEN,
    DARK_GREEN,
    HOVER,
    TEXT,
    MUTED,
)


REQUIREMENTS = [
    ("security", "SECURITY"),
    ("signing", "SIGNING SPEED"),
    ("verification", "VERIFICATION SPEED"),
    ("signature_size", "SIGNATURE SIZE"),
    ("key_generation", "KEY GENERATION"),
]


class MigrationPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")

        self.controller = controller
        self.requirement_vars = {}

        self.pack(fill="both", expand=True)

        page_header(
            self,
            "> MIGRATION ADVISOR",
            "Select the deployed algorithm and define evaluation requirements",
        )

        workspace = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )
        workspace.pack(fill="both", expand=True)

        workspace.grid_columnconfigure(0, weight=4)
        workspace.grid_columnconfigure(1, weight=5)
        workspace.grid_rowconfigure(0, weight=1)

        self._build_configuration(workspace)
        self._build_result_panel(workspace)
        self.refresh_result()

    def _build_configuration(self, workspace):
        configuration = panel(workspace)
        configuration.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 8),
        )

        ctk.CTkLabel(
            configuration,
            text="CONFIGURATION",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=GREEN,
        ).pack(anchor="w", padx=15, pady=(14, 12))

        ctk.CTkLabel(
            configuration,
            text="CURRENT ALGORITHM",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=MUTED,
        ).pack(anchor="w", padx=15, pady=(0, 5))

        selector = AlgorithmSelector(
            configuration,
            self.controller.current_algorithm,
            self.select_algorithm,
        )
        selector.pack(anchor="w", padx=15, pady=(0, 14))

        divider(configuration, pady=4)

        ctk.CTkLabel(
            configuration,
            text="EVALUATION REQUIREMENTS",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=MUTED,
        ).pack(anchor="w", padx=15, pady=(8, 3))

        ctk.CTkLabel(
            configuration,
            text=(
                "Checked criteria are included with equal weight."
            ),
            font=ctk.CTkFont(size=9),
            text_color=MUTED,
        ).pack(anchor="w", padx=15, pady=(0, 8))

        for key, label in REQUIREMENTS:
            variable = ctk.BooleanVar(
                value=self.controller.requirement_values.get(
                    key,
                    False,
                )
            )

            self.requirement_vars[key] = variable

            ctk.CTkCheckBox(
                configuration,
                text=label,
                variable=variable,
                onvalue=True,
                offvalue=False,
                checkbox_width=18,
                checkbox_height=18,
                border_width=2,
                corner_radius=3,
                fg_color=GREEN,
                hover_color=GREEN,
                border_color=DARK_GREEN,
                checkmark_color=BG,
                text_color=TEXT,
                font=ctk.CTkFont(size=11, weight="bold"),
            ).pack(anchor="w", padx=15, pady=5)

        ctk.CTkLabel(
            configuration,
            text=(
                "Security is also the PQC eligibility condition; "
                "it does not distinguish ML-DSA from SPHINCS."
            ),
            font=ctk.CTkFont(size=9),
            text_color=MUTED,
            wraplength=330,
            justify="left",
        ).pack(anchor="w", padx=15, pady=(6, 2))

        self.validation_label = ctk.CTkLabel(
            configuration,
            text="",
            font=ctk.CTkFont(size=9, weight="bold"),
            text_color=GREEN,
            wraplength=330,
            justify="left",
        )
        self.validation_label.pack(
            anchor="w",
            padx=15,
            pady=(5, 0),
        )

        ctk.CTkButton(
            configuration,
            text="[ ANALYZE MIGRATION ]",
            command=self.analyze,
            height=40,
            fg_color=BG,
            hover_color=HOVER,
            border_width=1,
            border_color=GREEN,
            text_color=GREEN,
            font=ctk.CTkFont(size=11, weight="bold"),
        ).pack(anchor="w", padx=15, pady=(14, 15))

    def _build_result_panel(self, workspace):
        outer = panel(workspace)
        outer.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(8, 0),
        )
        outer.grid_rowconfigure(0, weight=1)
        outer.grid_columnconfigure(0, weight=1)

        self.result_area = ctk.CTkScrollableFrame(
            outer,
            fg_color=PANEL,
            corner_radius=8,
            scrollbar_button_color=DARK_GREEN,
            scrollbar_button_hover_color=GREEN,
        )
        self.result_area.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=2,
            pady=2,
        )

    def select_algorithm(self, algorithm):
        self.controller.current_algorithm = algorithm

    def selected_requirements(self):
        return [
            key
            for key, variable in self.requirement_vars.items()
            if variable.get()
        ]

    def analyze(self):
        selected = self.selected_requirements()

        if not selected:
            self.validation_label.configure(
                text="Select at least one requirement."
            )

            self.controller.recommendation = (
                generate_recommendation(
                    self.controller.results,
                    self.controller.current_algorithm,
                    [],
                )
            )

            self.refresh_result()
            return

        if not self.controller.results:
            self.validation_label.configure(
                text="Run the benchmark first."
            )
            self.controller.recommendation = (
                self.controller.error_recommendation(
                    "No benchmark data is available. "
                    "Open BENCHMARKS and run the benchmark first."
                )
            )
            self.refresh_result()
            return

        self.validation_label.configure(
            text=""
        )

        self.controller.requirement_values = {
            key: variable.get()
            for key, variable in self.requirement_vars.items()
        }

        self.controller.recommendation = generate_recommendation(
            self.controller.results,
            self.controller.current_algorithm,
            selected,
        )

        self.refresh_result()

    def refresh_result(self):
        for widget in self.result_area.winfo_children():
            widget.destroy()

        recommendation = self.controller.recommendation

        ctk.CTkLabel(
            self.result_area,
            text="ANALYSIS RESULT",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=GREEN,
        ).pack(anchor="w", padx=13, pady=(12, 12))

        info_row(
            self.result_area,
            "Current Algorithm",
            recommendation.get("current_algorithm", "N/A"),
        )
        info_row(
            self.result_area,
            "Decision",
            recommendation.get("decision", "N/A"),
        )
        info_row(
            self.result_area,
            "Recommended",
            recommendation.get("recommended_algorithm") or "N/A",
        )
        info_row(
            self.result_area,
            "Weighted Score",
            f'{recommendation.get("score", 0):.2f} / 100',
        )

        candidates = recommendation.get("candidates", [])

        if candidates:
            divider(self.result_area)

            ctk.CTkLabel(
                self.result_area,
                text="PQC CANDIDATE RANKING",
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color=MUTED,
            ).pack(anchor="w", padx=15, pady=(0, 5))

            for index, candidate in enumerate(
                candidates,
                start=1,
            ):
                info_row(
                    self.result_area,
                    f"#{index} {candidate['algorithm']}",
                    f"{candidate['score']:.2f} / 100",
                )

        weights = recommendation.get("weights", {})

        if weights:
            divider(self.result_area)

            ctk.CTkLabel(
                self.result_area,
                text="ACTIVE WEIGHTS",
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color=MUTED,
            ).pack(anchor="w", padx=15, pady=(0, 5))

            for key, weight in weights.items():
                info_row(
                    self.result_area,
                    key.replace("_", " ").upper(),
                    f"{weight * 100:.1f}%",
                )

        divider(self.result_area)

        ctk.CTkLabel(
            self.result_area,
            text="RATIONALE",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=MUTED,
        ).pack(anchor="w", padx=15, pady=(0, 5))

        ctk.CTkLabel(
            self.result_area,
            text=recommendation.get(
                "reason",
                "No analysis available.",
            ),
            font=ctk.CTkFont(size=10),
            text_color=TEXT,
            wraplength=410,
            justify="left",
        ).pack(anchor="w", padx=15, pady=(0, 15))
