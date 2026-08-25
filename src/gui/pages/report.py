import json
from datetime import datetime
from pathlib import Path

import customtkinter as ctk

from src.gui.components import page_header, panel
from src.gui.theme import (
    BG,
    GREEN,
    DARK_GREEN,
    HOVER,
    TEXT,
    MUTED,
)


class ReportPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(
            parent,
            fg_color="transparent",
        )

        self.controller = controller
        self.pack(fill="both", expand=True)

        page_header(
            self,
            "> REPORT",
            "Review and export the current benchmark and migration analysis",
        )

        actions = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )
        actions.pack(fill="x", pady=(0, 12))

        self._action_button(
            actions,
            "[ REFRESH ]",
            self.refresh,
        ).pack(side="left")

        self._action_button(
            actions,
            "[ EXPORT TXT ]",
            self.export_txt,
        ).pack(side="left", padx=(8, 0))

        self._action_button(
            actions,
            "[ EXPORT JSON ]",
            self.export_json,
        ).pack(side="left", padx=(8, 0))

        self.status_label = ctk.CTkLabel(
            actions,
            text="",
            font=ctk.CTkFont(size=10),
            text_color=MUTED,
        )
        self.status_label.pack(side="left", padx=12)

        report_panel = panel(self)
        report_panel.pack(fill="both", expand=True)

        self.textbox = ctk.CTkTextbox(
            report_panel,
            fg_color=BG,
            border_width=0,
            text_color=TEXT,
            font=("Courier", 11),
            wrap="word",
        )
        self.textbox.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=8,
        )

        self.refresh()

    def _action_button(self, parent, text, command):
        return ctk.CTkButton(
            parent,
            text=text,
            command=command,
            height=36,
            fg_color=BG,
            hover_color=HOVER,
            border_width=1,
            border_color=GREEN,
            text_color=GREEN,
            font=ctk.CTkFont(size=10, weight="bold"),
        )

    def build_report_text(self):
        metadata = self.controller.benchmark_metadata()
        recommendation = self.controller.recommendation

        selected = [
            key.replace("_", " ").upper()
            for key, enabled
            in self.controller.requirement_values.items()
            if enabled
        ]

        lines = [
            "PQC SECURITY EVALUATION FRAMEWORK",
            "=" * 72,
            "",
            "BENCHMARK ENVIRONMENT",
            "-" * 72,
            f"Timestamp:        {metadata.get('timestamp', 'N/A')}",
            f"Python:           {metadata.get('python_version', 'N/A')}",
            f"Operating system: {metadata.get('operating_system', 'N/A')}",
            f"Machine:          {metadata.get('machine', 'N/A')}",
            f"Processor:        {metadata.get('processor', 'N/A')}",
            f"Benchmark command:{metadata.get('command', 'N/A')}",
            "",
            "ALGORITHMS",
            "-" * 72,
        ]

        if self.controller.results:
            for result in self.controller.results:
                lines.extend(
                    [
                        f"{result['algorithm']}:",
                        f"  Key generation: {result['keygen_time'] * 1000:.6f} ms",
                        f"  Signing:        {result['sign_time'] * 1000:.6f} ms",
                        f"  Verification:   {result['verify_time'] * 1000:.6f} ms",
                        f"  Public key:     {result['public_key_size']} bytes",
                        f"  Private key:    {result['private_key_size']} bytes",
                        f"  Signature:      {result['signature_size']} bytes",
                        "",
                    ]
                )
        else:
            lines.extend(
                [
                    "No benchmark data available.",
                    "",
                ]
            )

        lines.extend(
            [
                "MIGRATION ANALYSIS",
                "-" * 72,
                f"Current algorithm: {recommendation.get('current_algorithm', 'N/A')}",
                f"Decision:          {recommendation.get('decision', 'N/A')}",
                f"Recommended:       {recommendation.get('recommended_algorithm') or 'N/A'}",
                f"Score:             {recommendation.get('score', 0):.2f} / 100",
                "",
                "Selected requirements:",
                (
                    "  " + ", ".join(selected)
                    if selected
                    else "  None"
                ),
                "",
                "Candidate ranking:",
            ]
        )

        candidates = recommendation.get(
            "candidates",
            [],
        )

        if candidates:
            for index, candidate in enumerate(
                candidates,
                start=1,
            ):
                lines.append(
                    f"  {index}. {candidate['algorithm']}: "
                    f"{candidate['score']:.2f} / 100"
                )
        else:
            lines.append("  No ranking available.")

        lines.extend(
            [
                "",
                "Rationale:",
                recommendation.get(
                    "reason",
                    "No analysis available.",
                ),
                "",
                "METHODOLOGY NOTE",
                "-" * 72,
                (
                    "Selected checkbox criteria are included with equal weight. "
                    "Only quantum-resistant algorithms are ranked as migration "
                    "candidates. Security therefore acts as a PQC eligibility "
                    "condition and does not differentiate ML-DSA from SPHINCS."
                ),
                "",
            ]
        )

        return "\n".join(lines)

    def refresh(self):
        report = self.build_report_text()

        self.textbox.configure(
            state="normal"
        )
        self.textbox.delete(
            "1.0",
            "end",
        )
        self.textbox.insert(
            "1.0",
            report,
        )
        self.textbox.configure(
            state="disabled"
        )

        self.status_label.configure(
            text="Report refreshed."
        )

    def _report_directory(self):
        directory = (
            self.controller.repo_root
            / "results"
            / "reports"
        )

        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        return directory

    def export_txt(self):
        stamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        path = (
            self._report_directory()
            / f"pqc_report_{stamp}.txt"
        )

        path.write_text(
            self.build_report_text(),
            encoding="utf-8",
        )

        self.status_label.configure(
            text=f"Saved: {path.name}"
        )

    def export_json(self):
        stamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        path = (
            self._report_directory()
            / f"pqc_report_{stamp}.json"
        )

        payload = {
            "metadata": self.controller.benchmark_metadata(),
            "benchmark_results": self.controller.results,
            "selected_requirements": [
                key
                for key, enabled
                in self.controller.requirement_values.items()
                if enabled
            ],
            "recommendation": self.controller.recommendation,
        }

        path.write_text(
            json.dumps(
                payload,
                indent=4,
            ),
            encoding="utf-8",
        )

        self.status_label.configure(
            text=f"Saved: {path.name}"
        )
