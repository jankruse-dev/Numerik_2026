import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import ticker
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

runtime = pd.read_csv(BASE_DIR / 'runtime.csv', sep=';', encoding='utf-8')

fig, ax = plt.subplots()

#ax.plot(runtime['sizes'], runtime['Matrix'], ls='', marker='o', label='Matrixschreibweise')
ax.plot(runtime['sizes'], runtime['Index'], ls='', marker='o', label='Indexschreibweise')
#ax.set_yscale('log')
#ax.set_xscale('log')
ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:g}'))
ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:g}'))
ax.grid(which='both', alpha=0.5)
ax.set_xlabel('Anzahl der Gleichungen im System')
ax.set_ylabel('Lösungszeit in s')
ax.legend()


fig.tight_layout
fig.savefig(BASE_DIR / 'Abgabe_Beamer' / 'Bilder' / 'runtime_index.pdf', 
            bbox_inches='tight')

