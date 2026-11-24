import os
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

SWIPL_PATH = r"C:\Users\legio\swipl\bin\swipl.exe"
if not os.path.exists(SWIPL_PATH):
    SWIPL_PATH = "swipl"

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(PROJECT_DIR, "src")
TESTS_DIR = os.path.join(PROJECT_DIR, "tests")

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
        style.configure("Header.TLabel", font=("Segoe UI", 12, "bold"))
        style.configure("SubHeader.TLabel", font=("Segoe UI", 10))
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"))

    def create_widgets(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tab_prop = ttk.Frame(notebook, padding=10)
        self.tab_fol = ttk.Frame(notebook, padding=10)
        self.tab_dp = ttk.Frame(notebook, padding=10)

        notebook.add(self.tab_prop, text="1. Propositional Resolution")
        notebook.add(self.tab_fol, text="2. First-Order Logic Resolution")
        notebook.add(self.tab_dp, text="3. Davis-Putnam SAT Solver")

        self.build_prop_tab()
        self.build_fol_tab()
        self.build_dp_tab()

    def build_prop_tab(self):
        frame = self.tab_prop

        top_frame = ttk.LabelFrame(frame, text=" Select or Enter Propositional CNF Formula ", padding=10)
        top_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(top_frame, text="Preset Example:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.prop_preset_cb = ttk.Combobox(top_frame, state="readonly", width=45)
        self.prop_preset_cb["values"] = [
            "Example 1: (¬a or b) and (c or d) and (¬d or b) ...",
            "Example 2: (¬b or a) and (¬a or b or e) and ...",
            "Example 3: (¬a or b) and (c or f) and ¬c ...",
            "Example 4: (a or b) and (¬a or ¬b) and c",
            "Example 5: (a or ¬b) and (b or ¬c) and ¬c"
        ]
        self.prop_preset_cb.current(0)
        self.prop_preset_cb.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.prop_preset_cb.bind("<<ComboboxSelected>>", self.on_prop_preset_change)

        btn_load = ttk.Button(top_frame, text="Load File...", command=lambda: self.load_file_into(self.prop_input))
        btn_load.grid(row=0, column=2, padx=5, pady=5)

        btn_run = ttk.Button(top_frame, text="Run Resolution", style="Accent.TButton", command=self.run_prop_resolution)
        btn_run.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(top_frame, text="Formula Input (CNF):").grid(row=1, column=0, sticky=tk.NW, padx=5, pady=5)
        self.prop_input = tk.Text(top_frame, height=4, font=("Consolas", 10))
        self.prop_input.grid(row=1, column=1, columnspan=3, sticky="ew", padx=5, pady=5)
        top_frame.columnconfigure(1, weight=1)

        res_frame = ttk.LabelFrame(frame, text=" Resolution Results & Derivation Trace ", padding=10)
        res_frame.pack(fill=tk.BOTH, expand=True)

        info_bar = ttk.Frame(res_frame)
        info_bar.pack(fill=tk.X, pady=(0, 5))
        self.prop_status_lbl = ttk.Label(info_bar, text="Status: Ready", font=("Segoe UI", 10, "bold"))
        self.prop_status_lbl.pack(side=tk.LEFT, padx=5)
        self.prop_ops_lbl = ttk.Label(info_bar, text="Resolution Operations: -", font=("Segoe UI", 10))
        self.prop_ops_lbl.pack(side=tk.LEFT, padx=20)

        self.prop_output = tk.Text(res_frame, wrap=tk.NONE, font=("Consolas", 10))
        self.prop_output.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        scroll_y = ttk.Scrollbar(res_frame, orient=tk.VERTICAL, command=self.prop_output.yview)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.prop_output.config(yscrollcommand=scroll_y.set)

        self.on_prop_preset_change(None)

    def on_prop_preset_change(self, event):
        idx = self.prop_preset_cb.current() + 1
        test_file = os.path.join(TESTS_DIR, f"s1_prop_{idx}.txt")
        if os.path.exists(test_file):
            with open(test_file, "r", encoding="utf-8") as f:
                content = f.read().strip()
            self.prop_input.delete("1.0", tk.END)
            self.prop_input.insert(tk.END, content)

    def run_prop_resolution(self):
        formula = self.prop_input.get("1.0", tk.END).strip()
        if not formula:
            messagebox.showwarning("Empty Formula", "Please enter or select a CNF formula.")
            return

        temp_file = os.path.join(PROJECT_DIR, "temp_prop.txt").replace("\\", "/")
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(formula + "\n")

        pl_script = os.path.join(SRC_DIR, "resolution_prop.pl").replace("\\", "/")
        prolog_query = f"prove_propositional('{temp_file}', Result, Ops, Trace), format('RESULT:~w|OPS:~w|TRACE:~w~n', [Result, Ops, Trace]), halt."
        
        try:
            p = subprocess.run([SWIPL_PATH, "-s", pl_script, "-g", prolog_query], capture_output=True, text=True, encoding="utf-8")
            if os.path.exists(temp_file):
                os.remove(temp_file)

            out = p.stdout.strip()
            if "RESULT:" in out:
                line = [l for l in out.splitlines() if "RESULT:" in l][0]
                parts = line.split("|")
                result_str = parts[0].replace("RESULT:", "")
                ops_str = parts[1].replace("OPS:", "")
                trace_str = parts[2].replace("TRACE:", "")

                if result_str == "refutation_success":
                    self.prop_status_lbl.config(text="Rezultat: NESATISFIABILĂ / CONTRADICȚIE GĂSITĂ (Refutation Succeeded -> Clauza vidă [] derivată)", foreground="#1B5E20")
                else:
                    self.prop_status_lbl.config(text="Rezultat: SATISFIABILĂ / CONSISTENTĂ (Refutation Failed -> Nu există contradicție / Nicio clauză vidă)", foreground="#0D47A1")
                
                self.prop_ops_lbl.config(text=f"Operații de rezoluție: {ops_str}")
                self.prop_output.delete("1.0", tk.END)
                self.prop_output.insert(tk.END, f"===========================================================\n")
                self.prop_output.insert(tk.END, f" RAPORT REZOLUȚIE PROPOZIȚIONALĂ\n")
                self.prop_output.insert(tk.END, f"===========================================================\n")
                if result_str == "refutation_success":
                    self.prop_output.insert(tk.END, f"Status Matematic: NESATISFIABILĂ (UNSAT)\n")
                    self.prop_output.insert(tk.END, f"Semnificație:     Formula conține o contradicție logică. S-a derivat clauza vidă [].\n")
                else:
                    self.prop_output.insert(tk.END, f"Status Matematic: SATISFIABILĂ (SAT)\n")
                    self.prop_output.insert(tk.END, f"Semnificație:     Formula este consistentă logic (există atribuiri de adevăr adevărate).\n")
                    self.prop_output.insert(tk.END, f"                  Metoda refutației se oprește fără a genera clauza vidă.\n")
                self.prop_output.insert(tk.END, f"Total Operații Rezoluție Efectuate: {ops_str}\n\n")
                
                self.prop_output.insert(tk.END, f"=== PAȘII DERIVĂRII / TRACE ===\n")
                if trace_str == "[]" or not trace_str:
                    if ops_str == "0":
                        self.prop_output.insert(tk.END, "Nicio operație de rezoluție necesară.\n")
                        self.prop_output.insert(tk.END, "Motiv: Clauzele redundante au fost eliminate prin optimizarea de subsumare (C5 p.6),\n")
                        self.prop_output.insert(tk.END, "iar clauzele rămase nu conțin literali complementari.\n")
                    else:
                        self.prop_output.insert(tk.END, f"Cele {ops_str} operații de rezoluție efectuate au produs doar tautologii sau clauze subsumate,\n")
                        self.prop_output.insert(tk.END, "care au fost eliminate imediat conform optimizărilor din C5 p.6.\n")
                else:
                    import re
                    steps = re.findall(r"step\((\d+),(\[[^\]]*\]),resolved\((\d+),(\d+),([^)]+)\)\)", trace_str)
                    if steps:
                        for s_num, res_clause, id1, id2, piv in steps:
                            self.prop_output.insert(tk.END, f"Pasul {s_num}: Rezolvare între Clauza {id1} și Clauza {id2} pe pivotul {piv}\n")
                            self.prop_output.insert(tk.END, f"         -> Rezolvent generat: {res_clause}\n\n")
                    else:
                        self.prop_output.insert(tk.END, f"{trace_str}\n")
            else:
                self.prop_output.delete("1.0", tk.END)
                self.prop_output.insert(tk.END, f"Error running SWI-Prolog:\n{p.stderr or p.stdout}")
        except Exception as e:
            messagebox.showerror("Execution Error", str(e))

    def build_fol_tab(self):
        frame = self.tab_fol

        top_frame = ttk.LabelFrame(frame, text=" Select or Enter First-Order Logic (FOL) CNF Formula ", padding=10)
        top_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(top_frame, text="Preset Example:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.fol_preset_cb = ttk.Combobox(top_frame, state="readonly", width=45)
        self.fol_preset_cb["values"] = [
            "Own Example: Alex graduating university (4-6 sentences)",
            "Course Example 1 (C3 p.30): Socrates mortal",
            "Course Example 2 (C3 p.33): Animal lover & killer",
            "Course Example 3 (C4 p.12): Barber paradox"
        ]
        self.fol_preset_cb.current(0)
        self.fol_preset_cb.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.fol_preset_cb.bind("<<ComboboxSelected>>", self.on_fol_preset_change)

        btn_load = ttk.Button(top_frame, text="Load File...", command=lambda: self.load_file_into(self.fol_input))
        btn_load.grid(row=0, column=2, padx=5, pady=5)

        btn_run = ttk.Button(top_frame, text="Run FOL Resolution", style="Accent.TButton", command=self.run_fol_resolution)
        btn_run.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(top_frame, text="Formula Input (FOL CNF):").grid(row=1, column=0, sticky=tk.NW, padx=5, pady=5)
        self.fol_input = tk.Text(top_frame, height=4, font=("Consolas", 10))
        self.fol_input.grid(row=1, column=1, columnspan=3, sticky="ew", padx=5, pady=5)
        top_frame.columnconfigure(1, weight=1)

        res_frame = ttk.LabelFrame(frame, text=" FOL Resolution Results & Derivation Trace ", padding=10)
        res_frame.pack(fill=tk.BOTH, expand=True)

        info_bar = ttk.Frame(res_frame)
        info_bar.pack(fill=tk.X, pady=(0, 5))
        self.fol_status_lbl = ttk.Label(info_bar, text="Status: Ready", font=("Segoe UI", 10, "bold"))
        self.fol_status_lbl.pack(side=tk.LEFT, padx=5)
        self.fol_ops_lbl = ttk.Label(info_bar, text="Resolution Operations: -", font=("Segoe UI", 10))
        self.fol_ops_lbl.pack(side=tk.LEFT, padx=20)

        self.fol_output = tk.Text(res_frame, wrap=tk.NONE, font=("Consolas", 10))
        self.fol_output.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        scroll_y = ttk.Scrollbar(res_frame, orient=tk.VERTICAL, command=self.fol_output.yview)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.fol_output.config(yscrollcommand=scroll_y.set)

        self.on_fol_preset_change(None)

    def on_fol_preset_change(self, event):
        mapping = {
            0: "s1_fol_own.txt",
            1: "s1_fol_c3_p30.txt",
            2: "s1_fol_c3_p33.txt",
            3: "s1_fol_c4_p12.txt"
        }
        idx = self.fol_preset_cb.current()
        test_file = os.path.join(TESTS_DIR, mapping.get(idx, "s1_fol_own.txt"))
        if os.path.exists(test_file):
            with open(test_file, "r", encoding="utf-8") as f:
                content = f.read().strip()
            self.fol_input.delete("1.0", tk.END)
            self.fol_input.insert(tk.END, content)

    def run_fol_resolution(self):
        formula = self.fol_input.get("1.0", tk.END).strip()
        if not formula:
            messagebox.showwarning("Empty Formula", "Please enter or select a FOL CNF formula.")
            return

        temp_file = os.path.join(PROJECT_DIR, "temp_fol.txt").replace("\\", "/")
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(formula + "\n")

        pl_script = os.path.join(SRC_DIR, "resolution_fol.pl").replace("\\", "/")
        prolog_query = f"prove_fol('{temp_file}', Result, Ops, Trace), format('RESULT:~w|OPS:~w|TRACE:~w~n', [Result, Ops, Trace]), halt."
        
        try:
            p = subprocess.run([SWIPL_PATH, "-s", pl_script, "-g", prolog_query], capture_output=True, text=True, encoding="utf-8")
            if os.path.exists(temp_file):
                os.remove(temp_file)

            out = p.stdout.strip()
            if "RESULT:" in out:
                line = [l for l in out.splitlines() if "RESULT:" in l][0]
                parts = line.split("|")
                result_str = parts[0].replace("RESULT:", "")
                ops_str = parts[1].replace("OPS:", "")
                trace_str = parts[2].replace("TRACE:", "")

                if result_str == "refutation_success":
                    self.fol_status_lbl.config(text="Rezultat: DEDUS LOGIC CU SUCCES (Refutation Succeeded -> Clauza vidă [] derivată)", foreground="#1B5E20")
                else:
                    self.fol_status_lbl.config(text="Rezultat: CONSISTENT / NEDEDUS (Refutation Failed)", foreground="#0D47A1")
                
                self.fol_ops_lbl.config(text=f"Operații de rezoluție: {ops_str}")
                self.fol_output.delete("1.0", tk.END)
                self.fol_output.insert(tk.END, f"===========================================================\n")
                self.fol_output.insert(tk.END, f" RAPORT REZOLUȚIE FIRST-ORDER LOGIC (FOL)\n")
                self.fol_output.insert(tk.END, f"===========================================================\n")
                self.fol_output.insert(tk.END, f"Status: {result_str}\n")
                self.fol_output.insert(tk.END, f"Total Operații Rezoluție FOL Efectuate: {ops_str}\n\n")
                self.fol_output.insert(tk.END, f"=== PAȘII DERIVĂRII / TRACE ===\n")
                import re
                steps = re.findall(r"step\((\d+),(\[[^\]]*\]),resolved\((\d+),(\d+)\)\)", trace_str)
                if steps:
                    for s_num, res_clause, id1, id2 in steps:
                        self.fol_output.insert(tk.END, f"Pasul {s_num}: Rezolvare unificată între Clauza {id1} și Clauza {id2}\n")
                        self.fol_output.insert(tk.END, f"         -> Rezolvent instanțiat: {res_clause}\n\n")
                else:
                    self.fol_output.insert(tk.END, f"{trace_str}\n")
            else:
                self.fol_output.delete("1.0", tk.END)
                self.fol_output.insert(tk.END, f"Error running SWI-Prolog:\n{p.stderr or p.stdout}")
        except Exception as e:
            messagebox.showerror("Execution Error", str(e))

    def build_dp_tab(self):
        frame = self.tab_dp

        top_frame = ttk.LabelFrame(frame, text=" Select or Enter CNF Clauses for Davis-Putnam ", padding=10)
        top_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(top_frame, text="Preset Example:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.dp_preset_cb = ttk.Combobox(top_frame, state="readonly", width=45)
        self.dp_preset_cb["values"] = [
            "Example 1: toddler and child and girl (SAT)",
            "Example 2: toddler and child and not girl (UNSAT)",
            "Example 3: (¬a or b) and (c or d) and ¬b ... (UNSAT)",
            "Example 4: (¬b or a) and e and ¬a (UNSAT)",
            "Example 5: (¬a or ¬e or b) ... (SAT)",
            "Example 6: (a or b) and (¬a or ¬b) and ... (UNSAT)"
        ]
        self.dp_preset_cb.current(0)
        self.dp_preset_cb.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.dp_preset_cb.bind("<<ComboboxSelected>>", self.on_dp_preset_change)

        btn_load = ttk.Button(top_frame, text="Load File...", command=lambda: self.load_file_into(self.dp_input))
        btn_load.grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(top_frame, text="Atom Strategy:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.dp_strategy_cb = ttk.Combobox(top_frame, state="readonly", width=45)
        self.dp_strategy_cb["values"] = [
            "Strategy 1: MOMS (Max Occurrences in Minimum Clauses)",
            "Strategy 2: DLIS (Dynamic Largest Individual Sum / Max Frequency)",
            "Compare Both Strategies Side-by-Side"
        ]
        self.dp_strategy_cb.current(0)
        self.dp_strategy_cb.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        btn_run = ttk.Button(top_frame, text="Run Davis-Putnam", style="Accent.TButton", command=self.run_dp_solver)
        btn_run.grid(row=1, column=2, columnspan=2, padx=5, pady=5, sticky="ew")

        ttk.Label(top_frame, text="Formula Input (CNF):").grid(row=2, column=0, sticky=tk.NW, padx=5, pady=5)
        self.dp_input = tk.Text(top_frame, height=4, font=("Consolas", 10))
        self.dp_input.grid(row=2, column=1, columnspan=3, sticky="ew", padx=5, pady=5)
        top_frame.columnconfigure(1, weight=1)

        res_frame = ttk.LabelFrame(frame, text=" Davis-Putnam Satisfiability & Truth Assignment ", padding=10)
        res_frame.pack(fill=tk.BOTH, expand=True)

        info_bar = ttk.Frame(res_frame)
        info_bar.pack(fill=tk.X, pady=(0, 5))
        self.dp_status_lbl = ttk.Label(info_bar, text="Result: Ready", font=("Segoe UI", 11, "bold"))
        self.dp_status_lbl.pack(side=tk.LEFT, padx=5)

        self.dp_output = tk.Text(res_frame, wrap=tk.NONE, font=("Consolas", 10))
        self.dp_output.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        scroll_y = ttk.Scrollbar(res_frame, orient=tk.VERTICAL, command=self.dp_output.yview)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.dp_output.config(yscrollcommand=scroll_y.set)

        self.on_dp_preset_change(None)

    def on_dp_preset_change(self, event):
        idx = self.dp_preset_cb.current() + 1
        test_file = os.path.join(TESTS_DIR, f"s2_dp_{idx}.txt")
        if os.path.exists(test_file):
            with open(test_file, "r", encoding="utf-8") as f:
                content = f.read().strip()
            self.dp_input.delete("1.0", tk.END)
            self.dp_input.insert(tk.END, content)

    def run_dp_solver(self):
        formula = self.dp_input.get("1.0", tk.END).strip()
        if not formula:
            messagebox.showwarning("Empty Formula", "Please enter or select a CNF formula.")
            return

        temp_file = os.path.join(PROJECT_DIR, "temp_dp.txt").replace("\\", "/")
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(formula + "\n")

        pl_script = os.path.join(SRC_DIR, "davis_putnam.pl").replace("\\", "/")
        strat_choice = self.dp_strategy_cb.current()

        try:
            self.dp_output.delete("1.0", tk.END)
            if strat_choice in (0, 1):
                strat_name = "moms" if strat_choice == 0 else "dlis"
                query = f"solve_dp('{temp_file}', {strat_name}, Result, Model), format('RES:~w|MODEL:~w~n', [Result, Model]), halt."
                p = subprocess.run([SWIPL_PATH, "-s", pl_script, "-g", query], capture_output=True, text=True, encoding="utf-8")
                out = p.stdout.strip()
                if "RES:" in out:
                    line = [l for l in out.splitlines() if "RES:" in l][0]
                    res_val = line.split("|")[0].replace("RES:", "")
                    model_val = line.split("|")[1].replace("MODEL:", "")
                    color = "green" if res_val == "YES" else "red"
                    self.dp_status_lbl.config(text=f"Result: {res_val}", foreground=color)
                    self.dp_output.insert(tk.END, f"=== DAVIS-PUTNAM SAT SOLVER ===\n")
                    self.dp_output.insert(tk.END, f"Strategy Used: {strat_name.upper()}\n")
                    self.dp_output.insert(tk.END, f"Satisfiability: {res_val}\n")
                    self.dp_output.insert(tk.END, f"Truth Values Assigned: {model_val}\n")
                else:
                    self.dp_output.insert(tk.END, f"Error:\n{p.stderr or p.stdout}")
            else:
                query_moms = f"solve_dp('{temp_file}', moms, R1, M1), format('MOMS_RES:~w|MOMS_MODEL:~w~n', [R1, M1]), halt."
                p1 = subprocess.run([SWIPL_PATH, "-s", pl_script, "-g", query_moms], capture_output=True, text=True, encoding="utf-8")
                
                query_dlis = f"solve_dp('{temp_file}', dlis, R2, M2), format('DLIS_RES:~w|DLIS_MODEL:~w~n', [R2, M2]), halt."
                p2 = subprocess.run([SWIPL_PATH, "-s", pl_script, "-g", query_dlis], capture_output=True, text=True, encoding="utf-8")

                self.dp_status_lbl.config(text="Result: Comparison Complete", foreground="blue")
                self.dp_output.insert(tk.END, "=== STRATEGY COMPARISON: MOMS vs DLIS ===\n\n")
                self.dp_output.insert(tk.END, "--- 1. Strategy MOMS (Max Occurrences in Minimum Clauses) ---\n")
                for l in p1.stdout.splitlines():
                    if "MOMS_RES:" in l:
                        parts = l.split("|")
                        self.dp_output.insert(tk.END, f"Result: {parts[0].replace('MOMS_RES:', '')}\nModel:  {parts[1].replace('MOMS_MODEL:', '')}\n")
                self.dp_output.insert(tk.END, "\n--- 2. Strategy DLIS (Dynamic Largest Individual Sum) ---\n")
                for l in p2.stdout.splitlines():
                    if "DLIS_RES:" in l:
                        parts = l.split("|")
                        self.dp_output.insert(tk.END, f"Result: {parts[0].replace('DLIS_RES:', '')}\nModel:  {parts[1].replace('DLIS_MODEL:', '')}\n")

            if os.path.exists(temp_file):
                os.remove(temp_file)
        except Exception as e:
            messagebox.showerror("Execution Error", str(e))

    def load_file_into(self, text_widget):
        path = filedialog.askopenfilename(initialdir=TESTS_DIR, title="Select CNF File", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if path:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read().strip()
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, content)

def main():
    root = tk.Tk()
    app = KRRProjectGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
