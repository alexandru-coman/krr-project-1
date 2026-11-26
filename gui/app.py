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

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=[12, 6])
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"))

        notebook = ttk.Notebook(root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tab_prop = ttk.Frame(notebook, padding=10)
        tab_fol = ttk.Frame(notebook, padding=10)
        tab_dp = ttk.Frame(notebook, padding=10)

        notebook.add(tab_prop, text="1. Propositional Resolution")
        notebook.add(tab_fol, text="2. First-Order Logic Resolution")
        notebook.add(tab_dp, text="3. Davis-Putnam SAT Solver")

        self.prop_input, self.prop_status_lbl, self.prop_ops_lbl, self.prop_output, _ = self.build_tab(
            tab_prop, "Select or Enter Propositional CNF Formula", "Resolution Results & Derivation Trace",
            PROP_PRESETS, "Run Resolution", self.run_prop_resolution,
        )
        self.fol_input, self.fol_status_lbl, self.fol_ops_lbl, self.fol_output, _ = self.build_tab(
            tab_fol, "Select or Enter First-Order Logic (FOL) CNF Formula", "FOL Resolution Results & Derivation Trace",
            FOL_PRESETS, "Run FOL Resolution", self.run_fol_resolution, input_label="Formula Input (FOL CNF):",
        )
        self.dp_input, self.dp_status_lbl, _, self.dp_output, self.dp_strategy_cb = self.build_tab(
            tab_dp, "Select or Enter CNF Clauses for Davis-Putnam", "Davis-Putnam Satisfiability & Truth Assignment",
            DP_PRESETS, "Run Davis-Putnam", self.run_dp_solver, status_text="Result: Ready", strategies=DP_STRATEGIES,
        )

    def build_tab(
        self, parent, top_title, res_title, presets, run_text, run_cmd,
        input_label="Formula Input (CNF):", status_text="Status: Ready", strategies=None,
    ):
        top_frame = ttk.LabelFrame(parent, text=f" {top_title} ", padding=10)
        top_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(top_frame, text="Preset Example:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        preset_cb = ttk.Combobox(top_frame, state="readonly", width=45, values=[label for label, _ in presets])
        preset_cb.current(0)
        preset_cb.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        input_text = tk.Text(top_frame, height=4, font=("Consolas", 10))
        load_preset = lambda _e=None: self.set_text_from_file(input_text, os.path.join(TESTS_DIR, presets[preset_cb.current()][1]))
        preset_cb.bind("<<ComboboxSelected>>", load_preset)

        ttk.Button(top_frame, text="Load File...", command=lambda: self.load_file_into(input_text)).grid(row=0, column=2, padx=5, pady=5)

        strategy_cb = None
        if strategies:
            ttk.Label(top_frame, text="Atom Strategy:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
            strategy_cb = ttk.Combobox(top_frame, state="readonly", width=45, values=strategies)
            strategy_cb.current(0)
            strategy_cb.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
            ttk.Button(top_frame, text=run_text, style="Accent.TButton", command=run_cmd).grid(row=1, column=2, columnspan=2, padx=5, pady=5, sticky="ew")
            input_row = 2
        else:
            ttk.Button(top_frame, text=run_text, style="Accent.TButton", command=run_cmd).grid(row=0, column=3, padx=5, pady=5)
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
        if not strategies:
            ops_lbl = ttk.Label(info_bar, text="Resolution Operations: -", font=("Segoe UI", 10))
            ops_lbl.pack(side=tk.LEFT, padx=20)

        output_text = tk.Text(res_frame, wrap=tk.NONE, font=("Consolas", 10))
        output_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        scroll_y = ttk.Scrollbar(res_frame, orient=tk.VERTICAL, command=output_text.yview)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        output_text.config(yscrollcommand=scroll_y.set)

        load_preset()
        return input_text, status_lbl, ops_lbl, output_text, strategy_cb

    def set_text_from_file(self, text_widget, path):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, content)

    def load_file_into(self, text_widget):
        path = filedialog.askopenfilename(initialdir=TESTS_DIR, title="Select CNF File", filetypes=[("Text files", "*.txt")])
        if path:
            self.set_text_from_file(text_widget, path)

    def eval_prolog(self, script, formula, query_fmt, marker):
        temp_file = os.path.join(PROJECT_DIR, "temp_input.txt").replace("\\", "/")
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(formula + "\n")
        pl_script = os.path.join(SRC_DIR, script).replace("\\", "/")
        p = subprocess.run(
            [SWIPL_PATH, "-s", pl_script, "-g", query_fmt.format(f=temp_file)],
            capture_output=True, text=True, encoding="utf-8",
        )
        os.remove(temp_file)
        line = next(l for l in p.stdout.splitlines() if l.startswith(marker))
        return dict(part.split(":", 1) for part in line.split("|"))

    def run_prop_resolution(self):
        formula = self.prop_input.get("1.0", tk.END).strip()
        res = self.eval_prolog(
            "resolution_prop.pl", formula,
            "prove_propositional('{f}', R, O, T), format('RESULT:~w|OPS:~w|TRACE:~w~n', [R, O, T]), halt.", "RESULT:",
        )
        result_str, ops_str, trace_str = res["RESULT"], res["OPS"], res["TRACE"]
        is_unsat = result_str == "refutation_success"
        status_text = (
            "Rezultat: NESATISFIABILĂ / CONTRADICȚIE GĂSITĂ (Refutation Succeeded -> Clauza vidă [] derivată)"
            if is_unsat
            else "Rezultat: SATISFIABILĂ / CONSISTENTĂ (Refutation Failed -> Nu există contradicție / Nicio clauză vidă)"
        )
        self.prop_status_lbl.config(text=status_text, foreground="#1B5E20" if is_unsat else "#0D47A1")
        self.prop_ops_lbl.config(text=f"Operații de rezoluție: {ops_str}")

        self.prop_output.delete("1.0", tk.END)
        self.prop_output.insert(tk.END, "===========================================================\n RAPORT REZOLUȚIE PROPOZIȚIONALĂ\n===========================================================\n")
        if is_unsat:
            self.prop_output.insert(tk.END, "Status Matematic: NESATISFIABILĂ (UNSAT)\nSemnificație:     Formula conține o contradicție logică. S-a derivat clauza vidă [].\n")
        else:
            self.prop_output.insert(tk.END, "Status Matematic: SATISFIABILĂ (SAT)\nSemnificație:     Formula este consistentă logic (există atribuiri de adevăr adevărate).\n                  Metoda refutației se oprește fără a genera clauza vidă.\n")
        self.prop_output.insert(tk.END, f"Total Operații Rezoluție Efectuate: {ops_str}\n\n=== PAȘII DERIVĂRII / TRACE ===\n")

        if trace_str == "[]":
            self.prop_output.insert(tk.END, f"Trace vid (Operații efectuate: {ops_str}).\n")
            return
        for s_num, res_clause, id1, id2, piv in re.findall(r"step\((\d+),(\[[^\]]*\]),resolved\((\d+),(\d+),((?:pos|neg)\([^)]+\))\)\)", trace_str):
            self.prop_output.insert(tk.END, f"Pasul {s_num}: Rezolvare între Clauza {id1} și Clauza {id2} pe pivotul {piv}\n         -> Rezolvent generat: {res_clause}\n\n")

    def run_fol_resolution(self):
        formula = self.fol_input.get("1.0", tk.END).strip()
        res = self.eval_prolog(
            "resolution_fol.pl", formula,
            "prove_fol('{f}', R, O, T), format('RESULT:~w|OPS:~w|TRACE:~w~n', [R, O, T]), halt.", "RESULT:",
        )
        result_str, ops_str, trace_str = res["RESULT"], res["OPS"], res["TRACE"]
        is_unsat = result_str == "refutation_success"
        status_text = (
            "Rezultat: DEDUS LOGIC CU SUCCES (Refutation Succeeded -> Clauza vidă [] derivată)"
            if is_unsat else "Rezultat: CONSISTENT / NEDEDUS (Refutation Failed)"
        )
        self.fol_status_lbl.config(text=status_text, foreground="#1B5E20" if is_unsat else "#0D47A1")
        self.fol_ops_lbl.config(text=f"Operații de rezoluție: {ops_str}")

        self.fol_output.delete("1.0", tk.END)
        self.fol_output.insert(tk.END, f"===========================================================\n RAPORT REZOLUȚIE FIRST-ORDER LOGIC (FOL)\n===========================================================\nStatus: {result_str}\nTotal Operații Rezoluție FOL Efectuate: {ops_str}\n\n=== PAȘII DERIVĂRII / TRACE ===\n")
        for s_num, res_clause, id1, id2 in re.findall(r"step\((\d+),(\[[^\]]*\]),resolved\((\d+),(\d+)\)\)", trace_str):
            self.fol_output.insert(tk.END, f"Pasul {s_num}: Rezolvare unificată între Clauza {id1} și Clauza {id2}\n         -> Rezolvent instanțiat: {res_clause}\n\n")

    def run_dp_solver(self):
        formula = self.dp_input.get("1.0", tk.END).strip()
        strat_choice = self.dp_strategy_cb.current()
        self.dp_output.delete("1.0", tk.END)

        if strat_choice in (0, 1):
            strat_name = "moms" if strat_choice == 0 else "dlis"
            res = self.eval_prolog("davis_putnam.pl", formula, f"solve_dp('{{f}}', {strat_name}, R, M), format('RES:~w|MODEL:~w~n', [R, M]), halt.", "RES:")
            res_val, model_val = res["RES"], res["MODEL"]
            self.dp_status_lbl.config(text=f"Result: {res_val}", foreground="green" if res_val == "YES" else "red")
            self.dp_output.insert(tk.END, f"=== DAVIS-PUTNAM SAT SOLVER ===\nStrategy Used: {strat_name.upper()}\nSatisfiability: {res_val}\nTruth Values Assigned: {model_val}\n")
        else:
            res = self.eval_prolog(
                "davis_putnam.pl", formula,
                "solve_dp('{f}', moms, R1, M1), solve_dp('{f}', dlis, R2, M2), format('R1:~w|M1:~w|R2:~w|M2:~w~n', [R1, M1, R2, M2]), halt.", "R1:",
            )
            self.dp_status_lbl.config(text="Result: Comparison Complete", foreground="blue")
            self.dp_output.insert(
                tk.END,
                f"=== STRATEGY COMPARISON: MOMS vs DLIS ===\n\n"
                f"--- 1. Strategy MOMS (Max Occurrences in Minimum Clauses) ---\nResult: {res['R1']}\nModel:  {res['M1']}\n\n"
                f"--- 2. Strategy DLIS (Dynamic Largest Individual Sum) ---\nResult: {res['R2']}\nModel:  {res['M2']}\n",
            )


def main():
    root = tk.Tk()
    KRRProjectGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
