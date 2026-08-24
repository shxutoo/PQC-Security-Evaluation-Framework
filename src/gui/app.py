import customtkinter as ctk

from src.analysis.summary import (
    load_results,
    generate_summary
)

from src.analysis.recommendation import (
    generate_recommendation
)


class PQCApplication(ctk.CTk):

    def __init__(self):
        super().__init__()

        # ============================================================
        # WINDOW
        # ============================================================

        self.title("PQC Security Evaluation Framework")
        self.geometry("950x600")
        self.minsize(850, 550)

        # ============================================================
        # THEME
        # ============================================================

        ctk.set_appearance_mode("dark")

        self.bg_color = "#000000"
        self.sidebar_color = "#050505"
        self.panel_color = "#0A0A0A"

        self.green = "#00FF41"
        self.dark_green = "#0B5D1E"
        self.hover_color = "#062E12"

        self.text_color = "#E0E0E0"
        self.muted_color = "#6B7280"

        self.configure(
            fg_color=self.bg_color
        )

        # ============================================================
        # DATA
        # ============================================================

        self.results = load_results()

        self.summary = generate_summary(
            self.results
        )

        self.current_algorithm = "ECDSA"

        self.recommendation = generate_recommendation(
            self.results,
            self.current_algorithm
        )

        # ============================================================
        # LAYOUT
        # ============================================================

        self.grid_columnconfigure(
            1,
            weight=1
        )

        self.grid_rowconfigure(
            0,
            weight=1
        )

        self.create_sidebar()
        self.create_main_area()

        self.show_dashboard()

    # ================================================================
    # SIDEBAR
    # ================================================================

    def create_sidebar(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=210,
            corner_radius=0,
            fg_color=self.sidebar_color
        )

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.sidebar.grid_propagate(False)

        # ------------------------------------------------------------
        # TITLE
        # ------------------------------------------------------------

        title = ctk.CTkLabel(
            self.sidebar,
            text="PQC // SEC",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            ),
            text_color=self.green
        )

        title.pack(
            padx=20,
            pady=(25, 5)
        )

        subtitle = ctk.CTkLabel(
            self.sidebar,
            text="SECURITY EVALUATION",
            font=ctk.CTkFont(
                size=10
            ),
            text_color=self.muted_color
        )

        subtitle.pack(
            padx=20,
            pady=(0, 25)
        )

        # ------------------------------------------------------------
        # NAVIGATION
        # ------------------------------------------------------------

        self.create_navigation_button(
            "01  DASHBOARD",
            self.show_dashboard
        )

        self.create_navigation_button(
            "02  BENCHMARKS",
            self.show_benchmarks
        )

        self.create_navigation_button(
            "03  MIGRATION",
            self.show_migration
        )

        self.create_navigation_button(
            "04  REPORT",
            self.show_report
        )

        self.create_status_panel()

    # ================================================================
    # NAVIGATION BUTTON
    # ================================================================

    def create_navigation_button(
        self,
        text,
        command
    ):

        button = ctk.CTkButton(
            self.sidebar,
            text=text,
            height=40,
            corner_radius=6,
            anchor="w",

            fg_color="#000000",
            hover_color=self.hover_color,

            border_width=1,
            border_color=self.dark_green,

            text_color=self.green,

            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),

            command=command
        )

        button.pack(
            fill="x",
            padx=12,
            pady=3
        )

    # ================================================================
    # STATUS PANEL
    # ================================================================

    def create_status_panel(self):

        status_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color=self.panel_color,
            corner_radius=8,
            border_width=1,
            border_color=self.dark_green
        )

        status_frame.pack(
            side="bottom",
            fill="x",
            padx=12,
            pady=15
        )

        status_title = ctk.CTkLabel(
            status_frame,
            text="SYSTEM STATUS",
            font=ctk.CTkFont(
                size=10,
                weight="bold"
            ),
            text_color=self.muted_color
        )

        status_title.pack(
            anchor="w",
            padx=12,
            pady=(10, 2)
        )

        status = ctk.CTkLabel(
            status_frame,
            text="●  ONLINE",
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            text_color=self.green
        )

        status.pack(
            anchor="w",
            padx=12,
            pady=(0, 10)
        )

    # ================================================================
    # MAIN AREA
    # ================================================================

    def create_main_area(self):

        self.main_area = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color=self.bg_color
        )

        self.main_area.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=25,
            pady=25
        )

    def clear_main_area(self):

        for widget in self.main_area.winfo_children():
            widget.destroy()

    # ================================================================
    # DASHBOARD
    # ================================================================

    def show_dashboard(self):

        self.clear_main_area()

        header = ctk.CTkLabel(
            self.main_area,
            text="> DASHBOARD",
            font=ctk.CTkFont(
                size=26,
                weight="bold"
            ),
            text_color=self.green
        )

        header.pack(
            anchor="w"
        )

        subtitle = ctk.CTkLabel(
            self.main_area,
            text="Post-quantum cryptographic security overview",
            font=ctk.CTkFont(
                size=13
            ),
            text_color=self.muted_color
        )

        subtitle.pack(
            anchor="w",
            pady=(0, 18)
        )

        # ------------------------------------------------------------
        # STAT CARDS
        # ------------------------------------------------------------

        cards = ctk.CTkFrame(
            self.main_area,
            fg_color="transparent"
        )

        cards.pack(
            fill="x",
            pady=(0, 15)
        )

        cards.grid_columnconfigure(
            (0, 1, 2),
            weight=1
        )

        algorithm_count = len(
            self.results
        )

        pqc_count = len(
            self.summary["security"][
                "quantum_resistant_algorithms"
            ]
        )

        migration = (
            "REQUIRED"
            if self.recommendation["migration_required"]
            else "NOT REQUIRED"
        )

        self.create_stat_card(
            cards,
            0,
            "ALGORITHMS",
            str(algorithm_count)
        )

        self.create_stat_card(
            cards,
            1,
            "PQC ALGORITHMS",
            str(pqc_count)
        )

        self.create_stat_card(
            cards,
            2,
            "MIGRATION",
            migration
        )

        # ------------------------------------------------------------
        # PERFORMANCE
        # ------------------------------------------------------------

        performance = ctk.CTkFrame(
            self.main_area,
            fg_color=self.panel_color,
            corner_radius=10,
            border_width=1,
            border_color=self.dark_green
        )

        performance.pack(
            fill="x",
            pady=(0, 15)
        )

        performance_title = ctk.CTkLabel(
            performance,
            text="PERFORMANCE",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=self.green
        )

        performance_title.pack(
            anchor="w",
            padx=15,
            pady=(12, 8)
        )

        fastest = self.summary["performance"]

        self.create_info_row(
            performance,
            "Fastest Key Generation",
            fastest["fastest_key_generation"]["algorithm"]
        )

        self.create_info_row(
            performance,
            "Fastest Signing",
            fastest["fastest_signing"]["algorithm"]
        )

        self.create_info_row(
            performance,
            "Fastest Verification",
            fastest["fastest_verification"]["algorithm"]
        )

        # ------------------------------------------------------------
        # RECOMMENDATION
        # ------------------------------------------------------------

        recommendation = ctk.CTkFrame(
            self.main_area,
            fg_color=self.panel_color,
            corner_radius=10,
            border_width=1,
            border_color=self.dark_green
        )

        recommendation.pack(
            fill="x"
        )

        recommendation_title = ctk.CTkLabel(
            recommendation,
            text="PQC MIGRATION RECOMMENDATION",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=self.green
        )

        recommendation_title.pack(
            anchor="w",
            padx=15,
            pady=(12, 8)
        )

        self.create_info_row(
            recommendation,
            "Current Algorithm",
            self.recommendation["current_algorithm"]
        )

        self.create_info_row(
            recommendation,
            "Recommended",
            self.recommendation["recommended_algorithm"]
        )

        self.create_info_row(
            recommendation,
            "Weighted Score",
            f'{self.recommendation["score"]:.2f} / 100'
        )

    # ================================================================
    # STAT CARD
    # ================================================================

    def create_stat_card(
        self,
        parent,
        column,
        title,
        value
    ):

        card = ctk.CTkFrame(
            parent,
            fg_color=self.panel_color,
            corner_radius=10,
            border_width=1,
            border_color=self.dark_green
        )

        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=4
        )

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(
                size=10,
                weight="bold"
            ),
            text_color=self.muted_color
        )

        title_label.pack(
            pady=(12, 2)
        )

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            ),
            text_color=self.green
        )

        value_label.pack(
            pady=(0, 12)
        )

    # ================================================================
    # INFO ROW
    # ================================================================

    def create_info_row(
        self,
        parent,
        label,
        value
    ):

        row = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )

        row.pack(
            fill="x",
            padx=15,
            pady=3
        )

        label_widget = ctk.CTkLabel(
            row,
            text=label,
            font=ctk.CTkFont(
                size=11
            ),
            text_color=self.muted_color
        )

        label_widget.pack(
            side="left"
        )

        value_widget = ctk.CTkLabel(
            row,
            text=value,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            text_color=self.green
        )

        value_widget.pack(
            side="right"
        )

    # ================================================================
    # BENCHMARKS
    # ================================================================

    def show_benchmarks(self):

        self.clear_main_area()

        header = ctk.CTkLabel(
            self.main_area,
            text="> BENCHMARKS",
            font=ctk.CTkFont(
                size=26,
                weight="bold"
            ),
            text_color=self.green
        )

        header.pack(
            anchor="w"
        )

        subtitle = ctk.CTkLabel(
            self.main_area,
            text="Measured performance and resource requirements",
            font=ctk.CTkFont(
                size=13
            ),
            text_color=self.muted_color
        )

        subtitle.pack(
            anchor="w",
            pady=(0, 15)
        )

        table = ctk.CTkFrame(
            self.main_area,
            fg_color=self.panel_color,
            corner_radius=10,
            border_width=1,
            border_color=self.dark_green
        )

        table.pack(
            fill="x"
        )

        columns = [
            "ALGORITHM",
            "KEYGEN",
            "SIGN",
            "VERIFY",
            "PUBLIC KEY",
            "PRIVATE KEY",
            "SIGNATURE"
        ]

        for column, text in enumerate(columns):

            label = ctk.CTkLabel(
                table,
                text=text,
                font=ctk.CTkFont(
                    size=10,
                    weight="bold"
                ),
                text_color=self.green
            )

            label.grid(
                row=0,
                column=column,
                padx=8,
                pady=10,
                sticky="w"
            )

        for row, result in enumerate(
            self.results,
            start=1
        ):

            values = [
                result["algorithm"],
                self.format_time(
                    result["keygen_time"]
                ),
                self.format_time(
                    result["sign_time"]
                ),
                self.format_time(
                    result["verify_time"]
                ),
                self.format_bytes(
                    result["public_key_size"]
                ),
                self.format_bytes(
                    result["private_key_size"]
                ),
                self.format_bytes(
                    result["signature_size"]
                )
            ]

            for column, value in enumerate(values):

                text_color = (
                    self.green
                    if column == 0
                    else self.text_color
                )

                label = ctk.CTkLabel(
                    table,
                    text=value,
                    font=ctk.CTkFont(
                        size=10,
                        weight="bold"
                        if column == 0
                        else "normal"
                    ),
                    text_color=text_color
                )

                label.grid(
                    row=row,
                    column=column,
                    padx=8,
                    pady=7,
                    sticky="w"
                )

        info = ctk.CTkFrame(
            self.main_area,
            fg_color=self.panel_color,
            corner_radius=10,
            border_width=1,
            border_color=self.dark_green
        )

        info.pack(
            fill="x",
            pady=(15, 0)
        )

        title = ctk.CTkLabel(
            info,
            text="BENCHMARK NOTES",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            text_color=self.green
        )

        title.pack(
            anchor="w",
            padx=15,
            pady=(10, 5)
        )

        notes = ctk.CTkLabel(
            info,
            text=(
                "> Lower execution time indicates better performance.\n"
                "> Smaller key/signature sizes indicate lower storage overhead.\n"
                "> Measurements are based on the configured benchmark runs."
            ),
            font=ctk.CTkFont(
                size=11
            ),
            text_color=self.muted_color,
            justify="left"
        )

        notes.pack(
            anchor="w",
            padx=15,
            pady=(0, 12)
        )

    # ================================================================
    # FORMATTING
    # ================================================================

    def format_time(
        self,
        value
    ):

        return f"{value * 1000:.3f} ms"

    def format_bytes(
        self,
        value
    ):

        if value >= 1024:
            return f"{value / 1024:.2f} KB"

        return f"{value} B"

    # ================================================================
    # ALGORITHM DROPDOWN
    # ================================================================

    def create_algorithm_dropdown(
        self,
        parent
    ):

        self.algorithm_dropdown = ctk.CTkComboBox(
            parent,

            width=250,
            height=38,

            values=[
                "RSA",
                "ECDSA"
            ],

            # --------------------------------------------------------
            # READ ONLY
            # --------------------------------------------------------

            state="readonly",

            # --------------------------------------------------------
            # CURRENT VALUE
            # --------------------------------------------------------

            variable=ctk.StringVar(
                value=self.current_algorithm
            ),

            # --------------------------------------------------------
            # MAIN BOX
            # --------------------------------------------------------

            fg_color="#000000",

            border_color=self.green,
            border_width=1,

            text_color=self.green,

            corner_radius=6,

            # --------------------------------------------------------
            # ARROW
            # --------------------------------------------------------

            button_color="#000000",
            button_hover_color=self.hover_color,

            # --------------------------------------------------------
            # DROPDOWN MENU
            # --------------------------------------------------------

            dropdown_fg_color="#000000",
            dropdown_hover_color=self.hover_color,
            dropdown_text_color=self.green,

            # --------------------------------------------------------
            # FONT
            # --------------------------------------------------------

            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),

            dropdown_font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),

            command=self.select_algorithm
        )

        return self.algorithm_dropdown

    # ================================================================
    # SELECT ALGORITHM
    # ================================================================

    def select_algorithm(
        self,
        algorithm
    ):

        self.current_algorithm = algorithm

        self.recommendation = generate_recommendation(
            self.results,
            self.current_algorithm
        )

    # ================================================================
    # MIGRATION ADVISOR
    # ================================================================

    def show_migration(self):

        self.clear_main_area()

        header = ctk.CTkLabel(
            self.main_area,
            text="> MIGRATION ADVISOR",
            font=ctk.CTkFont(
                size=26,
                weight="bold"
            ),
            text_color=self.green
        )

        header.pack(
            anchor="w"
        )

        subtitle = ctk.CTkLabel(
            self.main_area,
            text="Select the currently deployed cryptographic algorithm",
            font=ctk.CTkFont(
                size=13
            ),
            text_color=self.muted_color
        )

        subtitle.pack(
            anchor="w",
            pady=(0, 20)
        )

        # ------------------------------------------------------------
        # SELECTION PANEL
        # ------------------------------------------------------------

        selection = ctk.CTkFrame(
            self.main_area,
            fg_color=self.panel_color,
            corner_radius=10,
            border_width=1,
            border_color=self.dark_green
        )

        selection.pack(
            fill="x",
            pady=(0, 15)
        )

        label = ctk.CTkLabel(
            selection,
            text="CURRENT ALGORITHM",
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            text_color=self.muted_color
        )

        label.pack(
            anchor="w",
            padx=15,
            pady=(12, 5)
        )

        # ------------------------------------------------------------
        # DROPDOWN
        # ------------------------------------------------------------

        dropdown = self.create_algorithm_dropdown(
            selection
        )

        dropdown.pack(
            anchor="w",
            padx=15,
            pady=(0, 12)
        )

        # ------------------------------------------------------------
        # ANALYZE BUTTON
        # ------------------------------------------------------------

        analyze_button = ctk.CTkButton(
            selection,

            text="[ ANALYZE MIGRATION ]",

            height=38,

            fg_color="#000000",
            hover_color=self.hover_color,

            border_width=1,
            border_color=self.green,

            text_color=self.green,

            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),

            command=self.analyze_migration
        )

        analyze_button.pack(
            anchor="w",
            padx=15,
            pady=(0, 15)
        )

        # ------------------------------------------------------------
        # RESULT PANEL
        # ------------------------------------------------------------

        self.migration_result = ctk.CTkFrame(
            self.main_area,
            fg_color=self.panel_color,
            corner_radius=10,
            border_width=1,
            border_color=self.dark_green
        )

        self.migration_result.pack(
            fill="both",
            expand=True
        )

        self.display_migration_result()

    # ================================================================
    # ANALYZE MIGRATION
    # ================================================================

    def analyze_migration(self):

        self.recommendation = generate_recommendation(
            self.results,
            self.current_algorithm
        )

        self.display_migration_result()

    # ================================================================
    # MIGRATION RESULT
    # ================================================================

    def display_migration_result(self):

        for widget in self.migration_result.winfo_children():
            widget.destroy()

        current = self.recommendation[
            "current_algorithm"
        ]

        recommended = self.recommendation[
            "recommended_algorithm"
        ]

        score = self.recommendation[
            "score"
        ]

        migration_required = self.recommendation[
            "migration_required"
        ]

        status = (
            "REQUIRED"
            if migration_required
            else "NOT REQUIRED"
        )

        title = ctk.CTkLabel(
            self.migration_result,
            text="ANALYSIS RESULT",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=self.green
        )

        title.pack(
            anchor="w",
            padx=20,
            pady=(15, 15)
        )

        self.create_info_row(
            self.migration_result,
            "Current Algorithm",
            current
        )

        self.create_info_row(
            self.migration_result,
            "Migration Required",
            status
        )

        self.create_info_row(
            self.migration_result,
            "Recommended Algorithm",
            recommended
        )

        self.create_info_row(
            self.migration_result,
            "Weighted Score",
            f"{score:.2f} / 100"
        )

        separator = ctk.CTkFrame(
            self.migration_result,
            height=1,
            fg_color=self.dark_green
        )

        separator.pack(
            fill="x",
            padx=20,
            pady=15
        )

        reason = ctk.CTkLabel(
            self.migration_result,
            text=self.recommendation["reason"],
            font=ctk.CTkFont(
                size=11
            ),
            text_color=self.muted_color,
            wraplength=650,
            justify="left"
        )

        reason.pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

    # ================================================================
    # REPORT
    # ================================================================

    def show_report(self):

        self.clear_main_area()

        header = ctk.CTkLabel(
            self.main_area,
            text="> REPORT",
            font=ctk.CTkFont(
                size=26,
                weight="bold"
            ),
            text_color=self.green
        )

        header.pack(
            anchor="w"
        )

        subtitle = ctk.CTkLabel(
            self.main_area,
            text="Generated analysis and thesis reporting",
            font=ctk.CTkFont(
                size=13
            ),
            text_color=self.muted_color
        )

        subtitle.pack(
            anchor="w",
            pady=(0, 20)
        )

        panel = ctk.CTkFrame(
            self.main_area,
            fg_color=self.panel_color,
            corner_radius=10,
            border_width=1,
            border_color=self.dark_green
        )

        panel.pack(
            fill="both",
            expand=True
        )

        text = ctk.CTkLabel(
            panel,
            text="[ REPORT MODULE READY ]",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            ),
            text_color=self.green
        )

        text.pack(
            pady=100
        )


# ====================================================================
# ENTRY POINT
# ====================================================================

if __name__ == "__main__":

    app = PQCApplication()

    app.mainloop()
