from binaryninja import *
from .kersyms import *

def kersyms_start(view):
    kersyms = KerSyms(view)
    kersyms.start()

PluginCommand.register(
    'kersyms: rename kernel symbols',
    'Extract kernel symbols and rename them',
    kersyms_start
)
