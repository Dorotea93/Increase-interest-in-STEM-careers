import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch
from matplotlib import font_manager

# ============================================================
# 1. Datos
# ============================================================

scores = [1, 2, 3, 4, 5]

counts = [5, 3, 291, 146, 139]

percentages = [0.9, 0.5, 49.8, 25.0, 23.8]

labels = [
    "1\nDisminuyó\nsignificativamente",
    "2\nDisminuyó\nlevemente",
    "3\nSe mantuvo\nigual",
    "4\nAumentó levemente\no moderadamente",
    "5\nAumentó\nconsiderablemente"
]

# ============================================================
# 2. Configuración de la fuente
# ============================================================

available_fonts = {
    font.name for font in font_manager.fontManager.ttflist
}

if "Palatino Linotype" in available_fonts:
    font_name = "Palatino Linotype"
else:
    # Alternativa habitual en sistemas Linux/macOS
    font_name = "DejaVu Serif"
    print(
        "Aviso: Palatino Linotype no está instalada. "
        "Se utilizará DejaVu Serif como alternativa."
    )

plt.rcParams.update({
    "font.family": font_name,
    "font.size": 11,
    "axes.titlesize": 15,
    "axes.labelsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.dpi": 150,
    "savefig.dpi": 600
})

# ============================================================
# 3. Colores
# ============================================================

gray = "#A6A6A6"
fuchsia = "#C218B8"

# Gris: disminuyó o se mantuvo
# Fucsia: aumentó
colors = [
    gray,
    gray,
    gray,
    fuchsia,
    fuchsia
]

# ============================================================
# 4. Crear figura
# ============================================================

fig, ax = plt.subplots(figsize=(11, 7))

# Reservar espacio inferior para la leyenda (aumentado a 0.35)
fig.subplots_adjust(
    left=0.11,
    right=0.96,
    bottom=0.35, 
    top=0.87
)

x = np.arange(len(scores))

bars = ax.bar(
    x,
    percentages,
    width=0.62,
    color=colors,
    edgecolor="white",
    linewidth=0.9,
    zorder=3
)

# ============================================================
# 5. Etiquetas de las barras
# ============================================================

for bar, percentage, count in zip(
    bars,
    percentages,
    counts
):
    ax.annotate(
        f"{percentage:.1f}%\n(n={count})",
        xy=(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height()
        ),
        xytext=(0, 7),
        textcoords="offset points",
        ha="center",
        va="bottom",
        fontsize=10,
        clip_on=False
    )

# ============================================================
# 6. Título y ejes
# ============================================================

ax.set_title(
    "Distribución global del cambio de interés tras la intervención",
    pad=18
)

ax.set_xlabel(
    "Puntuación de cambio de interés "
    "(escala Likert de 1 a 5)",
    labelpad=12
)

ax.set_ylabel(
    "Porcentaje de estudiantes (%)",
    labelpad=10
)

ax.set_xticks(x)
ax.set_xticklabels(
    labels,
    ha="center"
)

ax.set_ylim(0, 62)
ax.set_yticks(np.arange(0, 61, 10))

# ============================================================
# 7. Rejilla y estilo
# ============================================================

ax.grid(
    axis="y",
    linestyle="--",
    linewidth=0.7,
    alpha=0.35,
    zorder=0
)

ax.set_axisbelow(True)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.spines["left"].set_color("#777777")
ax.spines["bottom"].set_color("#777777")

# ============================================================
# 8. Leyenda fuera del área de las barras
# ============================================================

legend_elements = [
    Patch(
        facecolor=gray,
        edgecolor="white",
        label="Disminuyó o se mantuvo igual"
    ),
    Patch(
        facecolor=fuchsia,
        edgecolor="white",
        label="Aumentó"
    )
]

ax.legend(
    handles=legend_elements,
    loc="upper center",
    bbox_to_anchor=(0.5, -0.35), # Bajado de -0.17 a -0.35 para quedar bajo el texto del eje X
    ncol=2,
    frameon=False,
    handlelength=1.5,
    columnspacing=2.5,
    borderaxespad=0
)

# ============================================================
# 9. Guardar y mostrar
# ============================================================

plt.savefig(
    "figure_table4_interest_change_palatino.png",
    dpi=600,
    bbox_inches="tight",
    facecolor="white"
)

plt.show()