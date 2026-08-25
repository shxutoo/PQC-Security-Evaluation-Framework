import json
import platform
import subprocess
import sys
import threading
from datetime import datetime
from pathlib import Path

import customtkinter as ctk

from src.analysis.recommendation import generate_recommendation
from src.analysis.summary import generate_summary, load_results
from src.gui.components import Sidebar
from src.gui.pages import (
    BenchmarksPage,
    DashboardPage,
    MigrationPage,
    ReportPage,
)
from src.gui.theme import BG, WINDOW_MIN, WINDOW_SIZE


class PQCApplication(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")

        self.title("PQC Security Evaluation Framework")
        self.geometry(WINDOW_SIZE)
        self.minsize(*WINDOW_MIN)
        self.configure(fg_color=BG)

        self.repo_root = Path(__file__).resolve().parents[2]

        self.results = []
        self.summary = {}
        self.current_algorithm = "ECDSA"

        self.requirement_values = {
            "security": True,
            "signing": True,
            "verification": False,
            "signature_size": False,
            "key_generation": False,
        }

        self.recommendation = {}
        self.current_page = None
        self.last_benchmark_status = ""

        self.reload_data()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        navigation = [
            ("01  DASHBOARD", lambda: self.show_page(DashboardPage)),
            ("02  BENCHMARKS", lambda: self.show_page(BenchmarksPage)),
            ("03  MIGRATION", lambda: self.show_page(MigrationPage)),
            ("04  REPORT", lambda: self.show_page(ReportPage)),
        ]

        self.sidebar = Sidebar(self, navigation)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.content = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color=BG,
        )
        self.content.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=25,
            pady=25,
        )

        self.show_page(DashboardPage)

    def get_selected_requirements(self):
        return [
            key
            for key, enabled in self.requirement_values.items()
            if enabled
        ]

    def reload_data(self):
        try:
            self.results = load_results() or []
        except Exception:
            self.results = []

        try:
            self.summary = (
                generate_summary(self.results)
                if self.results
                else {}
            )
        except Exception:
            self.summary = {}

        if self.results:
            try:
                self.recommendation = generate_recommendation(
                    self.results,
                    self.current_algorithm,
                    self.get_selected_requirements(),
                )
            except Exception as exc:
                self.recommendation = self.error_recommendation(str(exc))
        else:
            self.recommendation = self.error_recommendation(
                "No benchmark data is available. Run the benchmark first."
            )

    def error_recommendation(self, message):
        return {
            "current_algorithm": self.current_algorithm,
            "migration_required": False,
            "decision": "NO BENCHMARK DATA",
            "recommended_algorithm": None,
            "reason": message,
            "score": 0.0,
            "scores": {},
            "weights": {},
            "candidates": [],
        }

    def show_page(self, page_class):
        if self.current_page is not None:
            self.current_page.destroy()

        self.current_page = page_class(
            self.content,
            self,
        )

    def benchmark_metadata(self):
        path = (
            self.repo_root
            / "results"
            / "benchmark_metadata.json"
        )

        if path.exists():
            try:
                return json.loads(
                    path.read_text(encoding="utf-8")
                )
            except Exception:
                pass

        return {
            "timestamp": "Not recorded yet",
            "python_version": platform.python_version(),
            "operating_system": platform.platform(),
            "machine": platform.machine(),
            "processor": platform.processor() or "Unknown",
            "command": "python -m src.main",
        }

    def _write_benchmark_metadata(self):
        metadata = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "python_version": platform.python_version(),
            "operating_system": platform.platform(),
            "machine": platform.machine(),
            "processor": platform.processor() or "Unknown",
            "command": "python -m src.main",
        }

        results_dir = self.repo_root / "results"
        results_dir.mkdir(parents=True, exist_ok=True)

        (
            results_dir
            / "benchmark_metadata.json"
        ).write_text(
            json.dumps(metadata, indent=4),
            encoding="utf-8",
        )

    def run_benchmark_async(self, callback):
        """
        Run the existing benchmark pipeline without freezing the GUI.

        This deliberately calls src.main rather than duplicating benchmark
        logic inside the GUI.
        """

        def worker():
            try:
                completed = subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "src.main",
                    ],
                    cwd=self.repo_root,
                    capture_output=True,
                    text=True,
                    check=False,
                )

                success = completed.returncode == 0

                if success:
                    self._write_benchmark_metadata()

                output = (
                    completed.stdout.strip()
                    or completed.stderr.strip()
                )

                if not output:
                    output = (
                        "Benchmark completed."
                        if success
                        else "Benchmark failed."
                    )

            except Exception as exc:
                success = False
                output = str(exc)

            def finish():
                if success:
                    self.reload_data()
                    self.last_benchmark_status = (
                        "Benchmark completed successfully."
                    )
                else:
                    self.last_benchmark_status = (
                        f"Benchmark failed: {output}"
                    )

                callback(
                    success,
                    output,
                )

            self.after(0, finish)

        threading.Thread(
            target=worker,
            daemon=True,
        ).start()


if __name__ == "__main__":
    app = PQCApplication()
    app.mainloop()
