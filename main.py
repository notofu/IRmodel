#coding: utf-8
from ir_analyzer  import ir
#確認用
ir_model = ir.IR_main(maximum_sumbol_num = 1, num_of_symbols = 8)
symbols, symbol_startnotes, onset, pitch, duration, beat, closure_index = ir_model.ir_main("data/sample.musicxml")
#ir_model.plot_ir(0, 50, symbols, pitch)
#ir_model.plot_ir(0, 50, symbol_startnotes, pitch)