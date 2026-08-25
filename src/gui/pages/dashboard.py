import customtkinter as ctk

from src.gui.components import (
    info_row,
    page_header,
    panel,
    section_title,
    stat_card,
)
from src.gui.theme import MUTED


class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.pack(fill="both", expand=True)

        page_header(
            self,
            "> DASHBOARD",
            "Post-quantum cryptographic security overview",
        )

        if not controller.results:
            empty = panel(self)
            empty.pack(fill="x")

            ctk.CTkLabel(
                empty,
                text="NO BENCHMARK DATA",
                font=ctk.CTkFont(size=15, weight="bold"),
                text_color=MUTED,
            ).pack(padx=20, pady=(25, 5))

            ctk.CTkLabel(
                empty,
                text=(
                    "Open BENCHMARKS and run the benchmark "
                    "to populate the framework."
                ),
                font=ctk.CTkFont(size=11),
                text_color=MUTED,
            ).pack(padx=20, pady=(0, 25))
            return

        cards = ctk.CTkFrame(self, fg_color="transparent")
        cards.pack(fill="x", pady=(0, 15))
        cards.grid_columnconfigure((0, 1, 2), weight=1)

        pqc_count = len(
            controller.summary
            .get("security", {})
            .get("quantum_resistant_algorithms", [])
        )

        migration = (
            "REQUIRED"
            if controller.recommendation.get("migration_required", False)
            else "NOT REQUIRED"
        )

        stat_card(cards, 0, "ALGORITHMS", str(len(controller.results)))
        stat_card(cards, 1, "PQC ALGORITHMS", str(pqc_count))
        stat_card(cards, 2, "MIGRATION", migration)

        performance = panel(self)
        performance.pack(fill="x", pady=(0, 15))
        section_title(performance, "PERFORMANCE")

        fastest = controller.summary.get("performance", {})

        info_row(
            performance,
            "Fastest Key Generation",
            fastest.get("fastest_key_generation", {}).get("algorithm", "N/A"),
        )
        info_row(
            performance,
            "Fastest Signing",
            fastest.get("fastest_signing", {}).get("algorithm", "N/A"),
        )
        info_row(
            performance,
            "Fastest Verification",
            fastest.get("fastest_verification", {}).get("algorithm", "N/A"),
        )

        recommendation = panel(self)
        recommendation.pack(fill="x")
        section_title(recommendation, "PQC MIGRATION RECOMMENDATION")

        info_row(
            recommendation,
            "Current Algorithm",
            controller.recommendation.get("current_algorithm", "N/A"),
        )
        info_row(
            recommendation,
            "Decision",
            controller.recommendation.get("decision", "N/A"),
        )
        info_row(
            recommendation,
            "Recommended",
            controller.recommendation.get("recommended_algorithm") or "N/A",
        )
        info_row(
            recommendation,
            "Weighted Score",
            f'{controller.recommendation.get("score", 0):.2f} / 100',
        )
