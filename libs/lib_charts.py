#<=====>#
# Description
#<=====>#



#<=====>#
# Known To Do List
#<=====>#



#<=====>#
# Imports
#<=====>#
import re
from libs.lib_colors import cs, cp


#<=====>#
# Variables
#<=====>#
lib_name      = 'lib_charts'
log_name      = 'lib_charts'
lib_verbosity = 1
lib_debug_lvl = 1
lib_secs_max  = 2

#<=====>#
# Assignments Pre
#<=====>#


#<=====>#
# Classes
#<=====>#


#<=====>#
# Functions
#<=====>#

def chart_top(in_str='', len_cnt=250, align='left', bold=True, italic=False, font_color='#00FF00', bg_color='#4B0082', border_font_color='#00FF00', border_bg_color='#4B0082', style=2, formatted=False):
	l, s, r = chart_shapes(part='top', style=style)
	disp_str = chart_embed(l, s, r, align, bold, italic, font_color, bg_color, border_font_color, border_bg_color, len_cnt, formatted, in_str=in_str)

#<=====>#

def chart_title(in_str='', len_cnt=250, align='left', bold=True, italic=False, font_color='#00FF00', bg_color='#4B0082', border_font_color='#00FF00', border_bg_color='#4B0082', style=2, formatted=False):
	l, s, r = chart_shapes(part='row', style=style)
	disp_str = chart_embed(l, s, r, align, bold, italic, font_color, bg_color, border_font_color, border_bg_color, len_cnt, formatted, in_str=in_str)

#<=====>#

def chart_headers(in_str='', len_cnt=250, align='left', bold=True, italic=False, font_color='gold', bg_color='blue', border_font_color='#00FF00', border_bg_color='#4B0082', style=2, formatted=False):
	l, s, r = chart_shapes(part='row', style=style)
	disp_str = chart_string(l, s, r, align, bold, italic, font_color, bg_color, border_font_color, border_bg_color, len_cnt, formatted, in_str=in_str)

#<=====>#

def chart_mid(in_str='', len_cnt=250, align='left', bold=True, italic=False, font_color='#00FF00', bg_color='#4B0082', border_font_color='#00FF00', border_bg_color='#4B0082', style=2, formatted=False):
	l, s, r = chart_shapes(part='mid', style=style)
	disp_str = chart_embed(l, s, r, align, bold, italic, font_color, bg_color, border_font_color, border_bg_color, len_cnt, formatted, in_str=in_str)

#<=====>#

def chart_row(in_str='', len_cnt=250, align='left', bold=False, italic=False, font_color='white', bg_color='black', border_font_color='#00FF00', border_bg_color='#4B0082', style=2, formatted=False):
	l, s, r = chart_shapes(part='row', style=style)
	disp_str = chart_string(l, s, r, align, bold, italic, font_color, bg_color, border_font_color, border_bg_color, len_cnt, formatted, in_str=in_str)

#<=====>#

def chart_bottom(in_str='', len_cnt=250, align='left', bold=True, italic=False, font_color='#00FF00', bg_color='#4B0082', border_font_color='#00FF00', border_bg_color='#4B0082', style=2, formatted=False):
	l, s, r = chart_shapes(part='bottom', style=style)
	disp_str = chart_embed(l, s, r, align, bold, italic, font_color, bg_color, border_font_color, border_bg_color, len_cnt, formatted, in_str=in_str)

'''
Single-Line Box Drawing Characters:
┬ (U+252C) — Top T-junction
┴ (U+2534) — Bottom T-junction

Double-Line Box Drawing Characters:
╦ (U+2566) — Top T-junction (double)
╩ (U+2569) — Bottom T-junction (double)

Single-Line Box Drawing Characters:
┼ (U+253C) — Intersection

Double-Line Box Drawing Characters:
╬ (U+256C) — Intersection (double)

╔ ========== ========== ========== ╦ ========== ========== ========== ╗
║                                  ║                                  ║
╠ ========== ========== ========== ╬ ========== ========== ========== ╣
║                                  ║                                  ║
║                                  ║                                  ║
║                                  ║                                  ║
║                                  ║                                  ║
╚ ========== ========== ========== ╩ ========== ========== ========== ╝
'''

#<=====>#

def chart_shapes(part, style):
	func_name = 'chart_embed'

	'''
	Other Vertical and Horizontal Line Variations:
	╶ (U+2576) — Light horizontal line, starting right
	╴ (U+2574) — Light horizontal line, starting left
	╵ (U+2575) — Light vertical line, starting top
	╷ (U+2577) — Light vertical line, starting bottom
	'''

	'''
	Junctions and Intersections
	┬ (U+252C) — Top T-junction
	┼ (U+253C) — Intersection
	┴ (U+2534) — Bottom T-junction
	╦ (U+2566) — Top T-junction (double)
	╬ (U+256C) — Intersection (double)
	╩ (U+2569) — Bottom T-junction (double)
	'''

	if style == 1:
		'''
		Style 1 - Single-Line Box Drawing Characters:
		┌ (U+250C) — Upper left corner
		├ (U+251C) — Left T-junction
		└ (U+2514) — Lower left corner
		┐ (U+2510) — Upper right corner
		┤ (U+2524) — Right T-junction
		┘ (U+2518) — Lower right corner
		│ (U+2502) — Vertical line
		─ (U+2500) — Horizontal line
		┌──────────┐
		├──────────┤
		│          │
		└──────────┘
		'''
		if part == 'top':
			l = '┌'
			s = '─'
			r = '┐'
		elif part == 'mid':
			l = '├'
			s = '─'
			r = '┤'
		elif part == 'row':
			l = '│'
			s = ' '
			r = '│'
		elif part == 'bottom':
			l = '└'
			s = '─'
			r = '┘'

	elif style == 2:
		'''
		Style 2 - Vertical and Horizontal Line Variations:
		╭ (U+256D) — Rounded upper left corner
		├ (U+251C) — Left T-junction
		╰ (U+2570) — Rounded lower left corner
		╮ (U+256E) — Rounded upper right corner
		┤ (U+2524) — Right T-junction
		╯ (U+256F) — Rounded lower right corner
		│ (U+2502) — Vertical line
		─ (U+2500) — Horizontal line
		╭──────────╮
		├──────────┤
		│          │
		╰──────────╯
		'''
		if part == 'top':
			l = '╭'
			s = '─'
			r = '╮'
		elif part == 'mid':
			l = '├'
			s = '─'
			r = '┤'
		elif part == 'row':
			l = '│'
			s = ' '
			r = '│'
		elif part == 'bottom':
			l = '╰'
			s = '─'
			r = '╯'
	elif style == 3:
		'''
		Style 3 - Mixed Single/Double Line Characters:
		╓ (U+2553) — Upper left corner (single horizontal, double vertical)
		╠ (U+2560) — Left T-junction (double)
		╙ (U+2559) — Lower left corner (single horizontal, double vertical)
		╖ (U+2556) — Upper right corner (single horizontal, double vertical)
		╣ (U+2563) — Right T-junction (double)
		╜ (U+255C) — Lower right corner (single horizontal, double vertical)
		║ (U+2551) — Vertical line (double)
		─ (U+2500) — Horizontal line
		╓──────────╖
		╠──────────╣
		║          ║
		╙──────────╜
		'''
		if part == 'top':
			l = '╓'
			s = '─'
			r = '╖'
		elif part == 'mid':
			l = '╠'
			s = '═'
			r = '╣'
		elif part == 'row':
			l = '║'
			s = ' '
			r = '║'
		elif part == 'bottom':
			l = '╙'
			s = '─'
			r = '╜'
	elif style == 4:

		'''
		Style 4 - Mixed Single/Double Line Characters:
		╒ (U+2552) — Upper left corner (double horizontal, single vertical)
		├ (U+251C) — Left T-junction
		╘ (U+2558) — Lower left corner (double horizontal, single vertical)
		╕ (U+2555) — Upper right corner (double horizontal, single vertical)
		┤ (U+2524) — Right T-junction
		╛ (U+255B) — Lower right corner (double horizontal, single vertical)
		│ (U+2502) — Vertical line
		═ (U+2550) — Horizontal line (double)
		╒══════════╕
		├──────────┤
		│          │
		╘══════════╛
		'''
		if part == 'top':
			l = '╒'
			s = '═'
			r = '╗'
		elif part == 'mid':
			l = '├'
			s = '─'
			r = '┤'
		elif part == 'row':
			l = '│'
			s = ' '
			r = '│'
		elif part == 'bottom':
			l = '╘'
			s = '═'
			r = '╛'
		if part == 'top':
			pass
		elif part == 'mid':
			pass
		elif part == 'row':
			pass
		elif part == 'bottom':
			pass
	elif style == 5:
		'''
		Style 5 - Double-Line Box Drawing Characters:
		╔ (U+2554) — Upper left corner (double)
		╠ (U+2560) — Left T-junction (double)
		╚ (U+255A) — Lower left corner (double)
		╗ (U+2557) — Upper right corner (double)
		╣ (U+2563) — Right T-junction (double)
		╝ (U+255D) — Lower right corner (double)
		║ (U+2551) — Vertical line (double)
		═ (U+2550) — Horizontal line (double)
		╔══════════╗
		╠══════════╣
		║          ║
		╚══════════╝
		'''
		if part == 'top':
			l = '╔'
			s = '═'
			r = '╗'
		elif part == 'mid':
			l = '╠'
			s = '═'
			r = '╣'
		elif part == 'row':
			l = '║'
			s = ' '
			r = '║'
		elif part == 'bottom':
			l = '╚'
			s = '═'
			r = '╝'
	return l, s, r

#<=====>#

def chart_rep_str(s, border_font_color, border_bg_color, in_str=''):
	func_name = 'chart_embed'

	front_match = re.match(r'^(' + re.escape(s) + r'+)', in_str)
	rear_match  = re.search(r'(' + re.escape(s) + r'+)$', in_str)

	front_str = front_match.group(1) if front_match else ''
	rear_str  = rear_match.group(1) if rear_match else ''

	return front_str, rear_str

#<=====>#

def chart_embed(l, s, r, align, bold, italic, font_color, bg_color, border_font_color, border_bg_color, len_cnt, formatted, in_str=''):
	func_name = 'chart_embed'

	fore = cs(l, font_color=border_font_color, bg_color=border_bg_color)
	aft  = cs(r, font_color=border_font_color, bg_color=border_bg_color)

	if in_str == '':
		in_str = s * len_cnt
		disp_str = cs(text=in_str, font_color=border_font_color, bg_color=border_bg_color, bold=bold, italic=italic)
		disp_str = f"{fore}{disp_str}{aft}"
	else:
		in_str = f' {in_str} '
		if align == 'left':
			temp_str = f'{s*2}{in_str}'
			temp_str = rpad(temp_str, len_cnt, s)
		if align == 'right':
			temp_str = f'{in_str} {s*2}'
			temp_str = lpad(temp_str, len_cnt, s)
		if align == 'center':
			temp_str = f'{in_str}'
			temp_str = cpad(temp_str, len_cnt, s)

		front_str, rear_str = chart_rep_str(s, border_font_color, border_bg_color, in_str=temp_str)
		front_str = cs(text=front_str, font_color=border_font_color, bg_color=border_bg_color, bold=bold, italic=italic)
		rear_str  = cs(text=rear_str,  font_color=border_font_color, bg_color=border_bg_color, bold=bold, italic=italic)
		disp_str  = cs(text=in_str, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic)

		disp_str = f"{fore}{front_str}{disp_str}{rear_str}{aft}"

	print(disp_str) 

#<=====>#

def chart_string(l, s, r, align, bold, italic, font_color, bg_color, border_font_color, border_bg_color, len_cnt, formatted, in_str=''):
	func_name = 'chart_embed'

	fore = cs(l, font_color=border_font_color, bg_color=border_bg_color, bold=bold, italic=italic)
	aft  = cs(r, font_color=border_font_color, bg_color=border_bg_color, bold=bold, italic=italic)

	if in_str == '':
		in_str = s * len_cnt
		disp_str = cs(text=in_str, font_color=border_font_color, bg_color=border_bg_color, bold=bold, italic=italic)
		disp_str = f"{fore}{disp_str}{aft}"
	else:
		if align == 'left':
			true_len = display_length(in_str)
			in_str = in_str + ' ' * (len_cnt - true_len)
		if align == 'right':
			true_len = display_length(in_str)
			in_str = ' ' * (len_cnt - true_len) + in_str
		if align == 'center':
			true_len = display_length(in_str)
			needed_pad_len = len_cnt - true_len
			lead_pad_len = int(needed_pad_len / 2)
			rear_pad_len = int(needed_pad_len / 2)
			if lead_pad_len + rear_pad_len > needed_pad_len:
				rear_pad_len -= 1
			in_str = ' ' * lead_pad_len + in_str + ' ' * rear_pad_len

		if not formatted:
			disp_str  = cs(text=in_str, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic)

		disp_str = f"{fore}{disp_str}{aft}"

	print(disp_str) 

#<=====>#

def lpad(in_str, length, pad_char):
	out_str = in_str.rjust(length, pad_char)
	return out_str

#<=====>#

def rpad(in_str, length, pad_char):
	out_str = in_str.ljust(length, pad_char)
	return out_str

#<=====>#

def cpad(in_str, length, pad_char):
	out_str = in_str.center(length, pad_char)
	return out_str

#<=====>#

def left(in_str, length):
	out_str = in_str[0:length]
	return out_str

#<=====>#

def right(in_str, length):
	out_str = in_str[length*-1:]
	return out_str

#<=====>#

def mid(in_str, start_position, length):
	out_str = in_str[start_position:length+1]
	return out_str

#<=====>#

def strip_formatting(in_str):
	# Define a regex pattern to match ANSI escape sequences
	ansi_escape = re.compile(r'''
		\x1B     # ESC
		\[       # CSI (Control Sequence Introducer)
		[0-?]*   # Parameter bytes
		[ -/]*   # Intermediate bytes
		[@-~]    # Final byte
		''', re.VERBOSE)
	strip_str = ansi_escape.sub('', in_str)
	return strip_str

#<=====>#

def is_even(number: int) -> bool:
	return number % 2 == 0

#<=====>#

def is_odd(number: int) -> bool:
	return number % 2 != 0

#<=====>#

def display_length(in_str):
	strip_str = strip_formatting(in_str)
	display_length = len(strip_str)
	return display_length

#<=====>#
# Post Variables
#<=====>#


#<=====>#
# Default Run
#<=====>#

if __name__ == "__main__":

	msg_t1   = '* Market Summary * A8-USDC * 2024-09-04 06:56:43 * 2024-09-04 06:55:34 * 1:8 * 8/89'
	msg_h1   = '$     price      |  prc_chg   % | $    buy_prc     | $    sell_prc    |  buy_var   % |  sell_var  % | spread_pct % | $ usdc bal  | $  reserve  | $ available | reserves state |'
	msg_1_01 = '$     0.09140000 |    -7.3961 % | $     0.09140000 | $     0.09130000 |     0.0000 % |     0.1094 % |     0.1094 % | $      1.96 | $      0.00 | $      1.96 |    UNLOCKED    |'
	msg_t2   = '* Market Stats * A8-USDC * 2024-09-04 06:56:45'
	msg_h2   = 'trades   |   wins    |   lose    |  win_pct  % | lose_pct  % | $  win_amt  | $ lose_amt  | $   spent   | $   recv    | $   hold    | $    val    | $ gain_amt  | gain_pct  % |  gain_hr  % | gain_day  % |  elapsed  |'
	msg_2_01 = '34 |      29.0 |       5.0 |     85.29 % |     14.71 % | $    3.5900 | $   -1.9200 | $  137.0000 | $  138.5800 | $   11.9300 | $  138.6700 | $    1.6700 |    1.2200 % |    0.0018 % |    0.0424 % |      9999 |'
	msg_2_02 = 'found no more 4h candles, returning 293 candles...'
	msg_2_03 = 'found no more 1d candles, returning 50 candles...'
	msg_t3   = '* BUY LOGIC * A8-USDC * 2024-09-04 06:56:53'
	msg_h3   = 'mkt             | strat           | freq            | total | open  | close | wins  | lose  |  win   % |  lose  % |  gain_amt  |  gain_pct  % |  gain_hr   % |  gain_day  % | elapsed |    trade_size    |  | pass | fail |  test  % |'
	msg_3_01 = 'A8-USDC         | sha             | 30min           |     5 |     0 |     5 |     5 |     0 | 100.00 % |   0.00 % |       0.73 |       3.18 % |       0.05 % |       1.25 % |    9999 |      10.00000000 |  |    6 |   30 |  16.67 % |'
	msg_3_02 = 'A8-USDC         | sha             | 15min           |     5 |     0 |     5 |     5 |     0 | 100.00 % |   0.00 % |       0.65 |       3.10 % |       0.02 % |       0.44 % |    9999 |      10.00000000 |  |    7 |   21 |  25.00 % |'
	msg_3_03 = 'A8-USDC         | sha             | 4h              |     0 |     0 |     0 |     0 |     0 |   0.00 % |   0.00 % |       0.00 |       0.00 % |       0.00 % |       0.00 % |    9999 |       5.00000000 |  |   13 |   39 |  25.00 % |'
	msg_3_04 = 'A8-USDC         | sha             | 1d              |     0 |     0 |     0 |     0 |     0 |   0.00 % |   0.00 % |       0.00 |       0.00 % |       0.00 % |       0.00 % |    9999 |       5.00000000 |  |   12 |   48 |  20.00 % |'
	msg_3_05 = 'A8-USDC         | imp_macd        | 1d              |     0 |     0 |     0 |     0 |     0 |   0.00 % |   0.00 % |       0.00 |       0.00 % |       0.00 % |       0.00 % |    9999 |       5.00000000 |  |    2 |   20 |   9.09 % |'
	msg_3_06 = 'A8-USDC         | bb_bo           | 1h              |     0 |     0 |     0 |     0 |     0 |   0.00 % |   0.00 % |       0.00 |       0.00 % |       0.00 % |       0.00 % |    9999 |       5.00000000 |  |    1 |   14 |   6.67 % |'
	msg_3_07 = 'A8-USDC         | bb_bo           | 4h              |     0 |     0 |     0 |     0 |     0 |   0.00 % |   0.00 % |       0.00 |       0.00 % |       0.00 % |       0.00 % |    9999 |       5.00000000 |  |    2 |   16 |  11.11 % |'
	msg_3_08 = 'A8-USDC         | bb_bo           | 1d              |     0 |     0 |     0 |     0 |     0 |   0.00 % |   0.00 % |       0.00 |       0.00 % |       0.00 % |       0.00 % |    9999 |       5.00000000 |  |    2 |   19 |   9.52 % |'
	msg_3_09 = 'A8-USDC         | bb              | 15min           |     0 |     0 |     0 |     0 |     0 |   0.00 % |   0.00 % |       0.00 |       0.00 % |       0.00 % |       0.00 % |    9999 |       5.00000000 |  |    1 |    8 |  11.11 % |'
	msg_3_10 = 'A8-USDC         | bb              | 30min           |     0 |     0 |     0 |     0 |     0 |   0.00 % |   0.00 % |       0.00 |       0.00 % |       0.00 % |       0.00 % |    9999 |       5.00000000 |  |    1 |   11 |   8.33 % |'
	msg_3_11 = 'A8-USDC         | bb              | 1h              |     0 |     0 |     0 |     0 |     0 |   0.00 % |   0.00 % |       0.00 |       0.00 % |       0.00 % |       0.00 % |    9999 |       5.00000000 |  |    2 |   13 |  13.33 % |'
	msg_3_12 = 'A8-USDC         | bb              | 4h              |     0 |     0 |     0 |     0 |     0 |   0.00 % |   0.00 % |       0.00 |       0.00 % |       0.00 % |       0.00 % |    9999 |       5.00000000 |  |    3 |   15 |  16.67 % |'
	msg_3_13 = 'A8-USDC         | bb              | 1d              |     0 |     0 |     0 |     0 |     0 |   0.00 % |   0.00 % |       0.00 |       0.00 % |       0.00 % |       0.00 % |    9999 |       5.00000000 |  |    3 |   18 |  14.29 % |'
	msg_3_14 = 'A8-USDC         | sha             | 1h              |     5 |     0 |     5 |     4 |     1 |  80.00 % |  20.00 % |       0.00 |      -0.01 % |      -0.00 % |      -0.00 % |    9999 |       5.00000000 |  |    7 |   37 |  15.91 % |'
	msg_3_15 = 'A8-USDC         | imp_macd        | 4h              |     4 |     0 |     4 |     3 |     1 |  75.00 % |  25.00 % |      -0.04 |      -0.22 % |      -0.00 % |      -0.08 % |    9999 |       5.00000000 |  |    5 |   14 |  26.32 % |'
	msg_3_16 = 'A8-USDC         | imp_macd        | 1h              |     3 |     0 |     3 |     1 |     2 |  33.33 % |  66.67 % |      -0.36 |      -3.99 % |      -0.06 % |      -1.55 % |    9999 |       5.00000000 |  |    1 |   15 |   6.25 % |'
	msg_t4   = '* SELL LOGIC * A8-USDC * 2024-09-04 06:56:53'
	msg_h4   = '    mkt      | T | pos_id |  buy_strat   | freq  |    age     |     buy_val      |    curr_val    |    buy_prc     |    curr_prc    |    high_prc    | prc_pct  % | prc_top  % | prc_low  % | prc_drop % | $    net_est     | $  net_est_high   '
	msg_4_01 = 'A8-USDC has no open positions...'
	msg_4_02 = 'mkt_loop for A8-USDC - took 10.204 seconds...'

	print('')
	print('')
	print('')
	print('')
	print('')

	chart_top(in_str='top')
	chart_top()
	chart_top(in_str=msg_t1)
	chart_headers(in_str=msg_h1)
	chart_row(in_str=msg_1_01)

	chart_mid()

	chart_title(in_str=msg_t2)
	chart_headers(in_str=msg_h2)
	chart_row(in_str=msg_2_01)
	chart_row(in_str=msg_2_02)
	chart_row(in_str=msg_2_03)

	chart_mid()

	chart_title(in_str=msg_t3)
	chart_headers(in_str=msg_h3)
	chart_row(in_str=msg_3_01, align='left',   font_color='white', bg_color='green',    border_font_color='yellow', border_bg_color='#4B0082', style=2)
	chart_row(in_str=msg_3_02)
	chart_row(in_str=msg_3_03)
	chart_row(in_str=msg_3_04, align='left',   font_color='white', bg_color='orangered',    border_font_color='yellow', border_bg_color='#4B0082', style=2)
	chart_row(in_str=msg_3_05)
	chart_row(in_str=msg_3_06)
	chart_row(in_str=msg_3_07)
	chart_row(in_str=msg_3_08, align='left',   font_color='white', bg_color='lightgreen', border_font_color='yellow', border_bg_color='#4B0082', style=2)
	chart_row(in_str=msg_3_09)
	chart_row(in_str=msg_3_10)
	chart_row(in_str=msg_3_11)
	chart_row(in_str=msg_3_12)
	chart_row(in_str=msg_3_13)
	chart_row(in_str=msg_3_14)
	chart_row(in_str=msg_3_15)
	chart_row(in_str=msg_3_16, align='left',   font_color='white', bg_color='red',      border_font_color='yellow', border_bg_color='#4B0082', style=2)

	chart_mid()

	chart_title(in_str=msg_t4)
	chart_headers(in_str=msg_h4)
	chart_row(in_str=msg_4_01)
	chart_row(in_str=msg_4_02)

	chart_bottom()
	chart_bottom(in_str='bottom')

#<=====>#
