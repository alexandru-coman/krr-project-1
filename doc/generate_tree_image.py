import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

DOC_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_PATH = os.path.join(DOC_DIR, "resolution_tree.png")

def create_tree():
    _, ax = plt.subplots(figsize=(10, 11), dpi=250)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 110)
    ax.axis("off")

    def draw_box(x, y, w, h, text, bg="#E8EAF6", border="#1A237E", fontsize=8.5, bold=False):
        rect = patches.FancyBboxPatch(
            (x - w / 2, y - h / 2), w, h,
            boxstyle="round,pad=0.5,rounding_size=1.5",
            facecolor=bg, edgecolor=border, linewidth=1.2
        )
        ax.add_patch(rect)
        weight = "bold" if bold else "normal"
        ax.text(x, y, text, ha="center", va="center", fontsize=fontsize, fontweight=weight, color="#1A237E")

    def draw_line(x1, y1, x2, y2, label=None):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color="#37474F", lw=1.1, shrinkA=3, shrinkB=3))
        if label:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(mx + 2, my, label, fontsize=7.5, color="#D84315", fontweight="bold", va="center")

    # Level 0 (Roots)
    draw_box(30, 104, 52, 4.2, "C1: {¬student(X), ¬submits(X), ¬passes(X), graduates(X)}", bg="#FFF3E0", border="#E65100")
    draw_box(80, 104, 32, 4.2, "C7: {¬graduates(alex)} [Negated Goal]", bg="#FFEBEE", border="#C62828", bold=True)

    # Resolvent 8
    draw_box(45, 93, 48, 4.2, "C8: {¬student(alex), ¬submits(alex), ¬passes(alex)}")
    draw_line(30, 101.9, 45, 95.1, label="[X = alex]")
    draw_line(80, 101.9, 45, 95.1)

    # C4
    draw_box(82, 93, 26, 4.2, "C4: {student(alex)}", bg="#E8F5E9", border="#2E7D32")

    # Resolvent 9
    draw_box(55, 82, 38, 4.2, "C9: {¬submits(alex), ¬passes(alex)}")
    draw_line(45, 90.9, 55, 84.1)
    draw_line(82, 90.9, 55, 84.1)

    # C2
    draw_box(18, 82, 34, 4.2, "C2: {¬student(Y), ¬diligent(Y), submits(Y)}", bg="#FFF3E0", border="#E65100")

    # Resolvent 10
    draw_box(40, 71, 48, 4.2, "C10: {¬passes(alex), ¬student(alex), ¬diligent(alex)}")
    draw_line(18, 79.9, 40, 73.1, label="[Y = alex]")
    draw_line(55, 79.9, 40, 73.1)

    # C4
    draw_box(80, 71, 26, 4.2, "C4: {student(alex)}", bg="#E8F5E9", border="#2E7D32")

    # Resolvent 11
    draw_box(50, 60, 38, 4.2, "C11: {¬passes(alex), ¬diligent(alex)}")
    draw_line(40, 68.9, 50, 62.1)
    draw_line(80, 68.9, 50, 62.1)

    # C5
    draw_box(80, 60, 24, 4.2, "C5: {diligent(alex)}", bg="#E8F5E9", border="#2E7D32")

    # Resolvent 12
    draw_box(55, 49, 28, 4.2, "C12: {¬passes(alex)}")
    draw_line(50, 57.9, 55, 51.1)
    draw_line(80, 57.9, 55, 51.1)

    # C3
    draw_box(20, 49, 36, 4.2, "C3: {¬student(Z), ¬attends(Z), passes(Z)}", bg="#FFF3E0", border="#E65100")

    # Resolvent 13
    draw_box(42, 38, 38, 4.2, "C13: {¬student(alex), ¬attends(alex)}")
    draw_line(20, 46.9, 42, 40.1, label="[Z = alex]")
    draw_line(55, 46.9, 42, 40.1)

    # C4
    draw_box(78, 38, 26, 4.2, "C4: {student(alex)}", bg="#E8F5E9", border="#2E7D32")

    # Resolvent 14
    draw_box(50, 27, 28, 4.2, "C14: {¬attends(alex)}")
    draw_line(42, 35.9, 50, 29.1)
    draw_line(78, 35.9, 50, 29.1)

    # C6
    draw_box(78, 27, 24, 4.2, "C6: {attends(alex)}", bg="#E8F5E9", border="#2E7D32")

    # Resolvent 15 (Empty clause)
    draw_box(55, 15, 34, 5.0, "C15: [ ] (EMPTY CLAUSE)", bg="#FFCDD2", border="#B71C1C", fontsize=9.5, bold=True)
    draw_line(50, 24.9, 55, 17.5)
    draw_line(78, 24.9, 55, 17.5)

    # Legend / Title
    ax.text(50, 5, "Refutation Proof Tree by Resolution in First-Order Logic\nDerivation of empty clause [] confirms KB |= graduates(alex)",
            ha="center", fontsize=9, fontstyle="italic", color="#37474F")

    plt.tight_layout()
    plt.savefig(IMG_PATH, bbox_inches="tight", dpi=250)
    plt.close()
    print(f"Tree diagram saved to: {IMG_PATH}")

if __name__ == "__main__":
    create_tree()
