# kersyms: prepare your linux kernel image analysis

kersyms is to prepare your linux kernel image analysis with extracting symbols and rename them, and finally add the common entry point `0xffffffff81000000` to your binary ninja.

# Usage

Install this plugin, you can do this by git clone this to your binary ninja plugin folder.

Then, open binary ninja, `Tools -> kersyms`, and wait for it to finish.
