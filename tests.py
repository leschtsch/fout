# -*- coding: utf-8 -*-
"""
This demo is tex_demo.py modified to have unicode. See that file for
more information.
"""

import matplotlib

matplotlib.rcParams['text.usetex'] = True
import matplotlib.pyplot as plt

plt.figure(1, figsize=(10, 10))
ax = plt.axes([0.0, 0.0, 1, 1])

# plt.rc('text.latex', preamble=r'\usepackage{amsmath}')
matplotlib.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'

s = r'''
$\left[ \begin{gathered} x \\ b \end{gathered} \right.$
'''

ax.text(0.5, 0.5, s,
        horizontalalignment='center',
        verticalalignment='center',
        fontsize=20, color='black')

plt.xlabel(r'\textbf{time (s)}')
plt.ylabel('\\textit{Velocity (m/sec)}', fontsize=16)
plt.title(s, fontsize=16, color='r')
plt.show()

