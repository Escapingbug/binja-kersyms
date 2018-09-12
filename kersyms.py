from binaryninja import *

class KerSyms(BackgroundTaskThread):
    def __init__(self, view):
        BackgroundTaskThread.__init__(self, '', True)
        self.view = view
        self.symtab_sections = []
        self.progress = ''
        self.reader = BinaryReader(self.view)
        self.rename_count = 0

    def rename(self, addr, name):
        # checkout types
        text = self.view.sections['.text']
        if text.start <= addr <= text.end:
            # function type
            symbol_type = enums.SymbolType.FunctionSymbol
            self.view.add_function(addr)
        else:
            # data
            symbol_type = enums.SymbolType.DataSymbol
        symbol = Symbol(symbol_type, addr, name)
        self.view.define_auto_symbol(symbol)
        self.rename_count += 1

    def extract_section(self, addr, addr_end):
        for addr in range(addr, addr_end, 0x10):
            self.reader.seek(addr)
            data_addr = self.reader.read64()
            string_addr = self.reader.read64()

            # find out string length
            reader = BinaryReader(self.view)
            string = ''
            length = 0
            reader.seek(string_addr)
            while True:
                cur = reader.read8()
                if cur == 0:
                    break
                string += chr(cur)
                length += 1

            c_string_type = self.view.parse_type_string('char str[%d]' % length)[0];
            self.view.define_data_var(string_addr, c_string_type)

            self.rename(data_addr, string)

    def run(self):
        self.progress = 'kersyms: extracting kernel symtable addresses'
        for sec_name, sec in self.view.sections.items():
            if 'ksymtab' in sec_name and 'string' not in sec_name:
                self.progress = 'renaming section %s (%x ~ %x)' % (sec_name, sec.start, sec.end)
                self.extract_section(sec.start, sec.end)
        self.progress = 'kersyms: renaming complete. Re-analyze..'
        prompt = 'kersyms: renamed %d data item' % self.rename_count
        show_message_box('kersyms', prompt)

        # finally, since binary ninja doesn't get correct entry point by itself, we add it
        self.view.add_entry_point(0xffffffff81000000)

        self.view.update_analysis_and_wait()
