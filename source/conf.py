# -*- coding: utf-8 -*-
import glob
import os
import sys

sys.path.insert(0,os.path.abspath('..'))

from rtdpy import __version__

project = 'rtdpy'
copyright = 'Copyright 2019-2020 Merck Sharp & Dohme Corp. a subsidiary of Merck & Co., Inc., Kenilworth, NJ, USA'
author = 'Matthew Flamm'

release = __version__

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'IPython.sphinxext.ipython_directive',
    'IPython.sphinxext.ipython_console_highlighting',
    'numpydoc',
    'matplotlib.sphinxext.plot_directive',
   ]

source_suffix = '.rst'
master_doc = 'index'

language = None

exclude_patterns = []
pygments_style = None

html_theme = 'alabaster'
html_theme_options = {'font_size': '1.1em',
                      'code_font_size': '0.7em',
                      'fixed_sidebar': True,
                      'sidebar_width': '300px'}

htmlhelp_basename = 'rtdpydoc'

numpydoc_use_plots = True
numpydoc_show_class_members = False

todo_include_todos = True

plot_include_source = True
plot_formats = [('png', 96), 'pdf']
plot_html_show_formats = False
plot_html_show_source_link = False

autosummary_generate = glob.glob("*.rst")

import matplotlib.pyplot as plt
plt.ioff()

plot_pre_code = """
import numpy as np
import matplotlib.pyplot as plt
import rtdpy
np.random.seed(123)
"""

ipython_execlines = ['import numpy as np',
                     'import matplotlib.pyplot as plt',
                     'import rtdpy']
