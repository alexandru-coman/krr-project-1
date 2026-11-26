import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Preformatted, KeepTogether, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

DOC_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(DOC_DIR, ".."))
SRC_DIR = os.path.join(PROJECT_DIR, "src")
OUTPUT_PDF = os.path.join(DOC_DIR, "Coman_Ioan_Alexandru_project1.pdf")

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setStrokeColor(colors.HexColor("#CCCCCC"))
        self.setFillColor(colors.HexColor("#555555"))
        
        # Header (on pages after the first)
        if self._pageNumber > 1:
            self.drawString(54, 755, "KRR Project 1 - Resolution & Davis-Putnam | Coman Ioan Alexandru")
            self.line(54, 748, 558, 748)

        # Footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 38, page_str)
        self.drawString(54, 38, "Faculty of Mathematics and Computer Science, University of Bucharest (UniBuc)")
        self.line(54, 48, 558, 48)
        self.restoreState()

def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    base_style = getSampleStyleSheet()['Normal']

    def make_style(name, font_name='Helvetica', font_size=9, leading=12, color='#212121', **kwargs):
        return ParagraphStyle(
            name,
            parent=base_style,
            fontName=font_name,
            fontSize=font_size,
            leading=leading,
            textColor=colors.HexColor(color),
            **kwargs,
        )

    title_style = make_style('DocTitle', font_name='Helvetica-Bold', font_size=20, leading=24, color='#1A237E', spaceAfter=6)
    subtitle_style = make_style('DocSubTitle', font_size=12, leading=16, color='#283593', spaceAfter=15)
    meta_style = make_style('DocMeta', font_size=9.5, leading=14, color='#333333', spaceAfter=15)
    h1_style = make_style('Heading1_Custom', font_name='Helvetica-Bold', font_size=13, leading=17, color='#0D47A1', spaceBefore=14, spaceAfter=6, keepWithNext=True)
    h2_style = make_style('Heading2_Custom', font_name='Helvetica-Bold', font_size=10.5, leading=14, color='#1565C0', spaceBefore=10, spaceAfter=4, keepWithNext=True)
    body_style = make_style('Body_Custom', font_size=9, leading=12.5, spaceAfter=6)
    bullet_style = make_style('Bullet_Custom', font_size=8.5, leading=12, leftIndent=15, spaceAfter=3)
    code_style = make_style('Code_Custom', font_name='Courier', font_size=7, leading=8.5, color='#1B5E20')

    def make_table(data, col_widths, font_size, align_rules):
        table = Table(data, colWidths=col_widths)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E8EAF6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1A237E')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), font_size),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BDBDBD')),
            *align_rules,
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
        ]))
        return table

    story = []

    # Title & Metadata Header
    story.append(Paragraph("Project 1: Knowledge Representation and Reasoning", title_style))
    story.append(Paragraph("Automated Theorem Proving via Resolution and the Davis-Putnam SAT Solver", subtitle_style))
    
    meta_text = """
    <b>Author:</b> Coman Ioan Alexandru &nbsp;&nbsp;|&nbsp;&nbsp; <b>Institution:</b> Faculty of Mathematics and Computer Science, University of Bucharest<br/>
    <b>Course:</b> Knowledge Representation and Reasoning (KRR) &nbsp;&nbsp;|&nbsp;&nbsp; <b>Instructor:</b> Conf. dr. Marina Anca Cidota<br/>
    <b>Submission Deadline:</b> December 12th, 2026
    """
    story.append(Paragraph(meta_text, meta_style))
    story.append(Spacer(1, 4))

    # SECTION 1
    story.append(Paragraph("1. Subject 1: First-Order and Propositional Resolution", h1_style))
    
    story.append(Paragraph("1.a) Knowledge Base in Natural Language and First-Order Representation", h2_style))
    p1 = """
    The chosen original domain represents the academic standing and graduation eligibility of university students. The knowledge base consists of four sentences formulated with universal quantifiers and existential constants:
    """
    story.append(Paragraph(p1, body_style))
    story.append(Paragraph("1. Every student who submits all required assignments and passes the final exam qualifies for graduation.", bullet_style))
    story.append(Paragraph("2. Any student who is diligent submits all required assignments.", bullet_style))
    story.append(Paragraph("3. Every student who attends all lectures passes the final exam.", bullet_style))
    story.append(Paragraph("4. Alex is an enrolled student who is diligent and attends all lectures.", bullet_style))
    story.append(Paragraph("<b>Question:</b> Does Alex qualify for graduation? (Goal: <i>graduates(alex)</i>).", bullet_style))
    
    story.append(Paragraph("<b>Formal Vocabulary:</b> Constants: <i>alex</i>. Predicates: <i>student(X)</i>, <i>submits(X)</i>, <i>passes(X)</i>, <i>diligent(X)</i>, <i>attends(X)</i>, <i>graduates(X)</i>.", body_style))
    story.append(Paragraph("<b>FOL Formalization:</b><br/>"
                           "1. &forall;X ((student(X) &and; submits(X) &and; passes(X)) &rarr; graduates(X))<br/>"
                           "2. &forall;Y ((student(Y) &and; diligent(Y)) &rarr; submits(Y))<br/>"
                           "3. &forall;Z ((student(Z) &and; attends(Z)) &rarr; passes(Z))<br/>"
                           "4. student(alex) &and; diligent(alex) &and; attends(alex)<br/>"
                           "<b>Query:</b> graduates(alex)", body_style))

    story.append(Paragraph("1.b) Transformation to CNF and Manual Resolution Proof", h2_style))
    p_cnf = """
    By eliminating implications (&alpha; &rarr; &beta; &equiv; &not;&alpha; &or; &beta;), applying De Morgan's laws, dropping universal quantifiers, and adding the negated query (&not;graduates(alex)), we obtain the refutation clause set:
    <br/>
    &bull; C1: {&not;student(X), &not;submits(X), &not;passes(X), graduates(X)} &nbsp;&nbsp;&nbsp;&nbsp; &bull; C4: {student(alex)}<br/>
    &bull; C2: {&not;student(Y), &not;diligent(Y), submits(Y)} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&bull; C5: {diligent(alex)}<br/>
    &bull; C3: {&not;student(Z), &not;attends(Z), passes(Z)} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&bull; C6: {attends(alex)}<br/>
    &bull; C7: {&not;graduates(alex)} (Negated Goal)
    """
    story.append(Paragraph(p_cnf, body_style))

    tree_img_path = os.path.join(DOC_DIR, "resolution_tree.png")
    story.append(KeepTogether([
        Image(tree_img_path, width=470, height=520),
        Spacer(1, 4),
        Paragraph("<b>Figure 1:</b> Refutation Resolution Tree in First-Order Logic. The derivation of the empty clause [] completes the proof, verifying that <i>KB |= graduates(alex)</i>.", body_style)
    ]))

    story.append(Paragraph("1.c) Automatic FOL Resolution Evaluation", h2_style))
    story.append(Paragraph("The First-Order Logic resolution algorithm was implemented in Prolog (<i>resolution_fol.pl</i>), featuring standardizing apart, Robinson unification (MGU), factoring, and subsumption. The execution results on the test instances are summarized below:", body_style))

    fol_table_data = [
        ["Test Instance", "Formula Description", "Result", "Ops Done"],
        ["Own Example", "Academic graduation entitlement", "refutation_success", "10"],
        ["C3 p.30", "Socrates mortality (¬man(X) or mortal(X))...", "refutation_success", "2"],
        ["C3 p.33", "Animal lover & killer contradiction...", "refutation_success", "3"],
        ["C4 p.12", "Barber paradox (¬person(X) or shaves...)", "refutation_success", "3"]
    ]
    t_fol = make_table(fol_table_data, [80, 230, 110, 60], 8, [('ALIGN', (2, 0), (-1, -1), 'CENTER')])
    story.append(t_fol)
    story.append(Spacer(1, 4))

    story.append(Paragraph("1.d) Propositional Resolution & Optimizations", h2_style))
    story.append(Paragraph("The propositional resolution prover (<i>resolution_prop.pl</i>) implements three critical optimizations from course slide C5 p.6: (1) <b>Tautology Elimination</b> ({L, &not;L} discarded), (2) <b>Subsumption Elimination</b> (if C1 &sube; C2, C2 dropped), and (3) <b>Repeated Resolution Prevention</b> (clause index pairs and pivot are tracked to avoid redundant operations).", body_style))

    prop_table_data = [
        ["No.", "Propositional CNF Formula", "Result", "Ops", "Status"],
        ["i", "(¬a or b) and (c or d) and (¬d or b) and ¬b and (¬c or b) and e and (f or a or b or ¬f)", "refutation_success", "5", "UNSAT"],
        ["ii", "(¬b or a) and (¬a or b or e) and (a or ¬e) and ¬a and e", "refutation_success", "3", "UNSAT"],
        ["iii", "(¬a or b) and (c or f) and ¬c and (¬f or b) and (¬c or b)", "refutation_failure", "2", "SAT"],
        ["iv", "(a or b) and (¬a or ¬b) and c", "refutation_failure", "2", "SAT"],
        ["v", "(a or ¬b) and (b or ¬c) and ¬c", "refutation_failure", "0", "SAT"]
    ]
    t_prop = make_table(prop_table_data, [20, 275, 105, 35, 45], 7.5, [('ALIGN', (0, 0), (0, -1), 'CENTER'), ('ALIGN', (2, 0), (-1, -1), 'CENTER')])
    story.append(t_prop)
    story.append(Spacer(1, 6))

    # SECTION 2
    story.append(Paragraph("2. Subject 2: Davis-Putnam SAT Solver", h1_style))
    story.append(Paragraph("2.a) The Davis-Putnam Procedure (Brachman & Levesque 2004)", h2_style))
    p_dp = """
    The classic Davis-Putnam algorithm (1960) determines satisfiability via four systematic rules:
    <br/>
    1. <b>Base Cases:</b> If &empty; &in; S, return <b>NOT</b> (unsatisfiable). If S = &empty;, return <b>YES</b> (satisfiable).<br/>
    2. <b>Unit Clause Rule:</b> If a unit clause {L} exists, assign L = true, remove all clauses containing L, and remove &not;L from remaining clauses.<br/>
    3. <b>Pure Literal Rule:</b> If an atom occurs with only one polarity, assign it to satisfy its clauses and remove them.<br/>
    4. <b>Resolution Elimination Rule (The &bull; Operation):</b> Choose atom p. Partition S into Sp (containing p), S&not;p (containing &not;p), and S0 (containing neither). Form resolvents Res(Sp, S&not;p) on p, define S &bull; p = S0 &cup; Res(Sp, S&not;p) after removing tautologies and subsumed clauses, and recurse. If S &bull; p is satisfiable, reconstruct the truth assignment for p by checking consistency with S&not;p.
    """
    story.append(Paragraph(p_dp, body_style))

    story.append(Paragraph("2.b) Atom Selection Strategies & Comparative Analysis", h2_style))
    p_strat = """
    Two distinct selection heuristics were implemented for the &bull; operation:
    <br/>
    &bull; <b>Strategy 1: MOMS (Maximum Occurrences in Minimum Size Clauses):</b> Computes atom frequencies exclusively within clauses of minimal length (>1). Prioritizes producing shorter resolvents and immediate unit clauses in subsequent iterations.<br/>
    &bull; <b>Strategy 2: DLIS (Dynamic Largest Individual Sum / Max Frequency):</b> Selects the atom maximizing total positive and negative occurrences across all active clauses. Maximizes the number of clauses eliminated in the initial partition.<br/>
    <b>Comparison:</b> On problems with strong local structure (such as the Toddler ontology in Example 1), MOMS rapidly triggers cascades of unit propagations. DLIS provides robust performance across uniformly distributed clause sets.
    """
    story.append(Paragraph(p_strat, body_style))

    story.append(Paragraph("2.c) Davis-Putnam Benchmark Results", h2_style))
    dp_table_data = [
        ["Set", "Formula Summary", "MOMS Result", "DLIS Result", "Model (Truth Values Assigned)"],
        ["i", "Toddler ontology with girl", "YES", "YES", "{boy/true; child/true; female/true; girl/true; infant/true; male/false; toddler/true}"],
        ["ii", "Toddler ontology with ¬girl", "NOT", "NOT", "{}"],
        ["iii", "Propositional set 3", "NOT", "NOT", "{}"],
        ["iv", "Propositional set 4", "NOT", "NOT", "{}"],
        ["v", "Propositional set 5", "YES", "YES", "{a/false; b/false; d/true; e/true; f/true}"],
        ["vi", "Propositional set 6", "NOT", "NOT", "{}"]
    ]
    t_dp = make_table(dp_table_data, [20, 120, 50, 50, 240], 7, [('ALIGN', (0, 0), (0, -1), 'CENTER'), ('ALIGN', (2, 0), (3, -1), 'CENTER')])
    story.append(t_dp)
    story.append(Spacer(1, 6))

    # SECTION 3
    story.append(Paragraph("3. Theoretical Questions: Herbrand's Theorem", h1_style))
    p_herb = """
    <b>Herbrand's Theorem (Jacques Herbrand, 1930)</b> is the cornerstone of automated deduction and computational logic:
    <br/>
    &bull; <b>Herbrand Universe (H):</b> The set of all ground terms formed from constants and function symbols in formula S.<br/>
    &bull; <b>Herbrand Base (B):</b> The set of all ground atomic formulas formed by applying predicates in S to terms from H.<br/>
    &bull; <b>Statement:</b> <i>A set of first-order clauses S is unsatisfiable if and only if there exists a finite set of ground instances S' of clauses from S that is propositionally unsatisfiable.</i><br/>
    &bull; <b>Significance:</b> It reduces the undecidable problem of first-order validity over arbitrary domains to testing finite propositional unsatisfiability. Robinson's Resolution Principle (1965) directly operationalized Herbrand's theorem through unification, allowing provers to instantiate variables dynamically only when needed.
    """
    story.append(Paragraph(p_herb, body_style))

    # SECTION 4
    story.append(Paragraph("4. References & Bibliography", h1_style))
    p_ref = """
    1. Ronald J. Brachman and Hector J. Levesque. <i>Knowledge Representation and Reasoning</i>. Morgan Kaufmann / Elsevier, 2004.<br/>
    2. Martin Davis and Hilary Putnam. <i>A Computing Procedure for Quantification Theory</i>. Journal of the ACM (JACM), 7(3):201-215, 1960.<br/>
    3. J. Alan Robinson. <i>A Machine-Oriented Logic Based on the Resolution Principle</i>. Journal of the ACM (JACM), 12(1):23-41, 1965.<br/>
    4. Jacques Herbrand. <i>Recherches sur la th&#233;orie de la d&#233;monstration</i>. PhD thesis, University of Paris, 1930.<br/>
    5. Conf. dr. Marina Anca Cidota. Lecture slides on <i>Knowledge Representation and Reasoning</i> (C1-C5), FMI UniBuc, 2026.
    """
    story.append(Paragraph(p_ref, body_style))

    # SECTION 5: CODE APPENDIX
    story.append(PageBreak())
    story.append(Paragraph("5. Source Code Appendix (Algorithms Only - Without Explanatory Comments)", h1_style))
    story.append(Paragraph("<i>Note: In strict compliance with evaluation rules, all Prolog source code is provided without explanatory comments.</i>", body_style))

    files_to_include = [
        ("5.1. src/parser.pl (DCG Grammar Parser)", os.path.join(SRC_DIR, "parser.pl")),
        ("5.2. src/resolution_prop.pl (Optimized Propositional Resolution)", os.path.join(SRC_DIR, "resolution_prop.pl")),
        ("5.3. src/resolution_fol.pl (First-Order Logic Resolution)", os.path.join(SRC_DIR, "resolution_fol.pl")),
        ("5.4. src/davis_putnam.pl (Davis-Putnam SAT Solver)", os.path.join(SRC_DIR, "davis_putnam.pl"))
    ]

    for title, fpath in files_to_include:
        story.append(Paragraph(title, h2_style))
        with open(fpath, "r", encoding="utf-8") as f:
            code_text = f.read()
        story.append(Preformatted(code_text, code_style))
        story.append(Spacer(1, 8))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF: {OUTPUT_PDF}")

if __name__ == "__main__":
    build_pdf()
