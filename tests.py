name = win32print.GetDefaultPrinter() # verify that it matches with the name of your printer
printdefaults = {"DesiredAccess": win32print.PRINTER_ALL_ACCESS} # Doesn't work with PRINTER_ACCESS_USE
handle = win32print.OpenPrinter(name, printdefaults)
level = 2
attributes = win32print.GetPrinter(handle, level)
attributes['pDevMode'].Duplex = 1  #no flip
win32print.SetPrinter(handle, level, attributes, 0)
win32print.GetPrinter(handle, level)['pDevMode'].Duplex
win32api.ShellExecute(0,'print','C:\\aaa.txt','.','/manualstoprint',0)