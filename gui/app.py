from contextlib import contextmanager
import os
import re
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog

SWIPL_PATH = r"C:\Users\legio\swipl\bin\swipl.exe"
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(PROJECT_DIR, "src")
TESTS_DIR = os.path.join(PROJECT_DIR, "tests")

PROP_PRESETS = [
    ("Example 1: (not a or b) and (c or d) and (not d or b) ...", "s1_prop_1.txt"),
    ("Example 2: (not b or a) and (not a or b or e) and ...", "s1_prop_2.txt"),
    ("Example 3: (not a or b) and (c or f) and not c ...", "s1_prop_3.txt"),
    ("Example 4: (a or b) and (not a or not b) and c", "s1_prop_4.txt"),
    ("Example 5: (a or not b) and (b or not c) and not c", "s1_prop_5.txt"),
]

FOL_PRESETS = [
    ("Own Example: Alex graduating university (4-6 sentences)", "s1_fol_own.txt"),
    ("Course Example 1 (C3 p.30): Socrates mortal", "s1_fol_c3_p30.txt"),
    ("Course Example 2 (C3 p.33): Animal lover & killer", "s1_fol_c3_p33.txt"),
    ("Course Example 3 (C4 p.12): Barber paradox", "s1_fol_c4_p12.txt"),
]

DP_PRESETS = [
    ("Example 1: toddler and child and girl (SAT)", "s2_dp_1.txt"),
    ("Example 2: toddler and child and not girl (UNSAT)", "s2_dp_2.txt"),
    ("Example 3: (not a or b) and (c or d) and not b ... (UNSAT)", "s2_dp_3.txt"),
    ("Example 4: (not b or a) and e and not a (UNSAT)", "s2_dp_4.txt"),
    ("Example 5: (not a or not e or b) ... (SAT)", "s2_dp_5.txt"),
    ("Example 6: (a or b) and (not a or not b) and ... (UNSAT)", "s2_dp_6.txt"),
]

DP_STRATEGIES = [
    "Strategy 1: MOMS (Max Occurrences in Minimum Clauses)",
    "Strategy 2: DLIS (Dynamic Largest Individual Sum / Max Frequency)",
    "Compare Both Strategies Side-by-Side",
]


class KRRProjectGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("KRR Project 1 - Resolution & Davis-Putnam SAT Solver")
        self.root.geometry("980x740")
        self.root.minsize(860, 620)

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=[12, 6])
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"))

    def create_widgets(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tab_prop = ttk.Frame(notebook, padding=10)
        tab_fol = ttk.Frame(notebook, padding=10)
        tab_dp = ttk.Frame(notebook, padding=10)

        notebook.add(tab_prop, text="1. Propositional Resolution")
        notebook.add(tab_fol, text="2. First-Order Logic Resolution")
        notebook.add(tab_dp, text="3. Davis-Putnam SAT Solver")

        self.prop_input, self.prop_status_lbl, self.prop_ops_lbl, self.prop_output, _ = self.build_tab(
            tab_prop,
            top_title="Select or Enter Propositional CNF Formula",
            res_title="Resolution Results & Derivation Trace",
            presets=PROP_PRESETS,
            run_text="Run Resolution",
            run_cmd=self.run_prop_resolution,
        )
        self.fol_input, self.fol_status_lbl, self.fol_ops_lbl, self.fol_output, _ = self.build_tab(
            tab_fol,
            top_title="Select or Enter First-Order Logic (FOL) CNF Formula",
            res_title="FOL Resolution Results & Derivation Trace",
            presets=FOL_PRESETS,
            run_text="Run FOL Resolution",
            run_cmd=self.run_fol_resolution,
            input_label="Formula Input (FOL CNF):",
        )
        self.dp_input, self.dp_status_lbl, _, self.dp_output, self.dp_strategy_cb = self.build_tab(
            tab_dp,
            top_title="Select or Enter CNF Clauses for Davis-Putnam",
            res_title="Davis-Putnam Satisfiability & Truth Assignment",
            presets=DP_PRESETS,
            run_text="Run Davis-Putnam",
            run_cmd=self.run_dp_solver,
            status_text="Result: Ready",
            with_ops=False,
            strategies=DP_STRATEGIES,
        )

    def build_tab(
        self,
        parent,
        top_title,
        res_title,
        presets,
        run_text,
        run_cmd,
        input_label="Formula Input (CNF):",
        status_text="Status: Ready",
        with_ops=True,
        strategies=None,
    ):
        top_frame = ttk.LabelFrame(parent, text=f" {top_title} ", padding=10)
        top_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(top_frame, text="Preset Example:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        preset_cb = ttk.Combobox(top_frame, state="readonly", width=45)
        preset_cb["values"] = [label for label, _ in presets]
        preset_cb.current(0)
        preset_cb.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        input_text = tk.Text(top_frame, height=4, font=("Consolas", 10))

        def load_selected_preset(_event=None):
            _, filename = presets[preset_cb.current()]
            self.set_text_from_file(input_text, os.path.join(TESTS_DIR, filename))

        preset_cb.bind("<<ComboboxSelected>>", load_selected_preset)

        btn_load = ttk.Button(top_frame, text="Load File...", command=lambda: self.load_file_into(input_text))
        btn_load.grid(row=0, column=2, padx=5, pady=5)

        strategy_cb = None
        if strategies:
            ttk.Label(top_frame, text="Atom Strategy:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
            strategy_cb = ttk.Combobox(top_frame, state="readonly", width=45)
            strategy_cb["values"] = strategies
            strategy_cb.current(0)
            strategy_cb.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
            btn_run = ttk.Button(top_frame, text=run_text, style="Accent.TButton", command=run_cmd)
            btn_run.grid(row=1, column=2, columnspan=2, padx=5, pady=5, sticky="ew")
            input_row = 2
        else:
            btn_run = ttk.Button(top_frame, text=run_text, style="Accent.TButton", command=run_cmd)
            btn_run.grid(row=0, column=3, padx=5, pady=5)
            input_row = 1

        ttk.Label(top_frame, text=input_label).grid(row=input_row, column=0, sticky=tk.NW, padx=5, pady=5)
        input_text.grid(row=input_row, column=1, columnspan=3, sticky="ew", padx=5, pady=5)
        top_frame.columnconfigure(1, weight=1)

        res_frame = ttk.LabelFrame(parent, text=f" {res_title} ", padding=10)
        res_frame.pack(fill=tk.BOTH, expand=True)

        info_bar = ttk.Frame(res_frame)
        info_bar.pack(fill=tk.X, pady=(0, 5))
        status_lbl = ttk.Label(info_bar, text=status_text, font=("Segoe UI", 10, "bold"))
        status_lbl.pack(side=tk.LEFT, padx=5)

        ops_lbl = None
        if with_ops:
            ops_lbl = ttk.Label(info_bar, text="Resolution Operations: -", font=("Segoe UI", 10))
            ops_lbl.pack(side=tk.LEFT, padx=20)

        out_frame = ttk.Frame(res_frame)
        out_frame.pack(fill=tk.BOTH, expand=True)
        out_frame.rowconfigure(0, weight=1)
        out_frame.columnconfigure(0, weight=1)

        output_text = tk.Text(out_frame, wrap=tk.NONE, font=("Consolas", 10))
        output_text.grid(row=0, column=0, sticky="nsew")
        scroll_y = ttk.Scrollbar(out_frame, orient=tk.VERTICAL, command=output_text.yview)
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x = ttk.Scrollbar(out_frame, orient=tk.HORIZONTAL, command=output_text.xview)
        scroll_x.grid(row=1, column=0, sticky="ew")
        output_text.config(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        load_selected_preset()
        return input_text, status_lbl, ops_lbl, output_text, strategy_cb

    def set_text_from_file(self, text_widget, path):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, content)

    def load_file_into(self, text_widget):
        path = filedialog.askopenfilename(
            initialdir=TESTS_DIR,
            title="Select CNF File",
            filetypes=[("Text files", "*.txt")],
        )
        if path:
            self.set_text_from_file(text_widget, path)

    @contextmanager
    def temp_formula_file(self, filename, formula):
        temp_file = os.path.join(PROJECT_DIR, filename).replace("\\", "/")
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(formula + "\n")
        try:
            yield temp_file
        finally:
            os.remove(temp_file)

    def run_swipl(self, script_name, query):
        pl_script = os.path.join(SRC_DIR, script_name).replace("\\", "/")
        return subprocess.run(
            [SWIPL_PATH, "-s", pl_script, "-g", query],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

    def parse_line(self, stdout, marker):
        line = next(l for l in stdout.splitlines() if l.startswith(marker))
        return dict(part.split(":", 1) for part in line.split("|"))

    def run_resolution_query(self, temp_name, formula, script_name, predicate):
        with self.temp_formula_file(temp_name, formula) as temp_file:
            query = (
                f"{predicate}('{temp_file}', Result, Ops, Trace), "
                "format('RESULT:~w|OPS:~w|TRACE:~w~n', [Result, Ops, Trace]), halt."
            )
            p = self.run_swipl(script_name, query)
        parsed = self.parse_line(p.stdout, "RESULT:")
        return parsed["RESULT"], parsed["OPS"], parsed["TRACE"]

    def run_prop_resolution(self):
        formula = self.prop_input.get("1.0", tk.END).strip()
        result_str, ops_str, trace_str = self.run_resolution_query(
            "temp_prop.txt", formula, "resolution_prop.pl", "prove_propositional"
        )
        is_unsat = result_str == "refutation_success"
        status_text = (
            "Rezultat: NESATISFIABILĂ / CONTRADICȚIE GĂSITĂ (Refutation Succeeded -> Clauza vidă [] derivată)"
            if is_unsat
            else "Rezultat: SATISFIABILĂ / CONSISTENTĂ (Refutation Failed -> Nu există contradicție / Nicio clauză vidă)"
        )
        self.prop_status_lbl.config(text=status_text, foreground="#1B5E20" if is_unsat else "#0D47A1")
        self.prop_ops_lbl.config(text=f"Operații de rezoluție: {ops_str}")

        self.prop_output.delete("1.0", tk.END)
        self.prop_output.insert(tk.END, "===========================================================\n")
        self.prop_output.insert(tk.END, " RAPORT REZOLUȚIE PROPOZIȚIONALĂ\n")
        self.prop_output.insert(tk.END, "===========================================================\n")
        if is_unsat:
            self.prop_output.insert(tk.END, "Status Matematic: NESATISFIABILĂ (UNSAT)\n")
            self.prop_output.insert(tk.END, "Semnificație:     Formula conține o contradicție logică. S-a derivat clauza vidă [].\n")
        else:
            self.prop_output.insert(tk.END, "Status Matematic: SATISFIABILĂ (SAT)\n")
            self.prop_output.insert(tk.END, "Semnificație:     Formula este consistentă logic (există atribuiri de adevăr adevărate).\n")
            self.prop_output.insert(tk.END, "                  Metoda refutației se oprește fără a genera clauza vidă.\n")
        self.prop_output.insert(tk.END, f"Total Operații Rezoluție Efectuate: {ops_str}\n\n")
        self.prop_output.insert(tk.END, "=== PAȘII DERIVĂRII / TRACE ===\n")

        if trace_str == "[step(0,[],initial_empty_clause)]":
            self.prop_output.insert(tk.END, "Pasul 0: Clauza vidă [] este prezentă inițial.\n")
            return
        if trace_str == "[]":
            self.prop_output.insert(tk.END, f"Trace vid (Operații efectuate: {ops_str}).\n")
            return

        steps = re.findall(r"step\((\d+),(\[[^\]]*\]),resolved\((\d+),(\d+),((?:pos|neg)\([^)]+\))\)\)", trace_str)
        for s_num, res_clause, id1, id2, piv in steps:
            self.prop_output.insert(tk.END, f"Pasul {s_num}: Rezolvare între Clauza {id1} și Clauza {id2} pe pivotul {piv}\n")
            self.prop_output.insert(tk.END, f"         -> Rezolvent generat: {res_clause}\n\n")

    def run_fol_resolution(self):
        formula = self.fol_input.get("1.0", tk.END).strip()
        result_str, ops_str, trace_str = self.run_resolution_query(
            "temp_fol.txt", formula, "resolution_fol.pl", "prove_fol"
        )
        is_unsat = result_str == "refutation_success"
        status_text = (
            "Rezultat: DEDUS LOGIC CU SUCCES (Refutation Succeeded -> Clauza vidă [] derivată)"
            if is_unsat
            else "Rezultat: CONSISTENT / NEDEDUS (Refutation Failed)"
        )
        self.fol_status_lbl.config(text=status_text, foreground="#1B5E20" if is_unsat else "#0D47A1")
        self.fol_ops_lbl.config(text=f"Operații de rezoluție: {ops_str}")

        self.fol_output.delete("1.0", tk.END)
        self.fol_output.insert(tk.END, "===========================================================\n")
        self.fol_output.insert(tk.END, " RAPORT REZOLUȚIE FIRST-ORDER LOGIC (FOL)\n")
        self.fol_output.insert(tk.END, "===========================================================\n")
        self.fol_output.insert(tk.END, f"Status: {result_str}\n")
        self.fol_output.insert(tk.END, f"Total Operații Rezoluție FOL Efectuate: {ops_str}\n\n")
        self.fol_output.insert(tk.END, "=== PAȘII DERIVĂRII / TRACE ===\n")

        if trace_str == "[step(0,[],initial_empty_clause)]":
            self.fol_output.insert(tk.END, "Pasul 0: Clauza vidă [] este prezentă inițial.\n")
            return
        if trace_str == "[]":
            self.fol_output.insert(tk.END, f"Trace vid (Operații efectuate: {ops_str}).\n")
            return

        steps = re.findall(r"step\((\d+),(\[[^\]]*\]),resolved\((\d+),(\d+)\)\)", trace_str)
        for s_num, res_clause, id1, id2 in steps:
            self.fol_output.insert(tk.END, f"Pasul {s_num}: Rezolvare unificată între Clauza {id1} și Clauza {id2}\n")
            self.fol_output.insert(tk.END, f"         -> Rezolvent instanțiat: {res_clause}\n\n")

    def query_dp_strategy(self, temp_file, strategy):
        query = f"solve_dp('{temp_file}', {strategy}, Result, Model), format('RES:~w|MODEL:~w~n', [Result, Model]), halt."
        p = self.run_swipl("davis_putnam.pl", query)
        parsed = self.parse_line(p.stdout, "RES:")
        return parsed["RES"], parsed["MODEL"]

    def run_dp_solver(self):
        formula = self.dp_input.get("1.0", tk.END).strip()
        strat_choice = self.dp_strategy_cb.current()
        self.dp_output.delete("1.0", tk.END)

        with self.temp_formula_file("temp_dp.txt", formula) as temp_file:
            if strat_choice in (0, 1):
                strat_name = "moms" if strat_choice == 0 else "dlis"
                res_val, model_val = self.query_dp_strategy(temp_file, strat_name)
                color = "green" if res_val == "YES" else "red"
                self.dp_status_lbl.config(text=f"Result: {res_val}", foreground=color)
                self.dp_output.insert(tk.END, "=== DAVIS-PUTNAM SAT SOLVER ===\n")
                self.dp_output.insert(tk.END, f"Strategy Used: {strat_name.upper()}\n")
                self.dp_output.insert(tk.END, f"Satisfiability: {res_val}\n")
                self.dp_output.insert(tk.END, f"Truth Values Assigned: {model_val}\n")
            else:
                moms_res, moms_model = self.query_dp_strategy(temp_file, "moms")
                dlis_res, dlis_model = self.query_dp_strategy(temp_file, "dlis")
                self.dp_status_lbl.config(text="Result: Comparison Complete", foreground="blue")
                self.dp_output.insert(tk.END, "=== STRATEGY COMPARISON: MOMS vs DLIS ===\n\n")
                self.dp_output.insert(tk.END, "--- 1. Strategy MOMS (Max Occurrences in Minimum Clauses) ---\n")
                self.dp_output.insert(tk.END, f"Result: {moms_res}\nModel:  {moms_model}\n")
                self.dp_output.insert(tk.END, "\n--- 2. Strategy DLIS (Dynamic Largest Individual Sum) ---\n")
                self.dp_output.insert(tk.END, f"Result: {dlis_res}\nModel:  {dlis_model}\n")


def main():
    root = tk.Tk()
    KRRProjectGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
