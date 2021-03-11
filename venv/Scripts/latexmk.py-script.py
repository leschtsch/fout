#!C:\Users\ПК\Desktop\проги\проект9.2\fout\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'latexmk.py==0.4','console_scripts','latexmk.py'
__requires__ = 'latexmk.py==0.4'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('latexmk.py==0.4', 'console_scripts', 'latexmk.py')()
    )
