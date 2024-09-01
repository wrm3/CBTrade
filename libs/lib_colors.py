# lib_colors.py
# https://youtu.be/fYSEsG2FPdU

#<=====>#

import os
import random
import re
# import sys

#<=====>#

class CLR:
	# Dictionary of HTML5 named colors with complete 147 entries
	pallette = {}

	# Reds
	pallette["indianred"]             = "#CD5C5C"      # indianred                             #CD5C5C  205   92   92  389
	pallette["lightcoral"]            = "#F08080"      # lightcoral                            #F08080  240  128  128  496
	pallette["salmon"]                = "#FA8072"      # salmon                                #FA8072  250  128  114  492
	pallette["darksalmon"]            = "#E9967A"      # darksalmon                            #E9967A  233  150  122  505
	pallette["lightsalmon"]           = "#FFA07A"      # lightsalmon                           #FFA07A  255  160  122  537
	pallette["crimson"]               = "#DC143C"      # crimson                               #DC143C  220   20   60  300
	pallette["red"]                   = "#FF0000"      # red                                   #FF0000  255    0    0  255
	pallette["firebrick"]             = "#B22222"      # firebrick                             #B22222  178   34   34  246
	pallette["darkred"]               = "#8B0000"      # darkred                               #8B0000  139    0    0  139

	# Pinks
	pallette["pink"]                  = "#FFC0CB"      # pink                                  #FFC0CB  255  192  203  650
	pallette["lightpink"]             = "#FFB6C1"      # lightpink                             #FFB6C1  255  182  193  630
	pallette["hotpink"]               = "#FF69B4"      # hotpink                               #FF69B4  255  105  180  540
	pallette["deeppink"]              = "#FF1493"      # deeppink                              #FF1493  255   20  147  422
	pallette["mediumvioletred"]       = "#C71585"      # mediumvioletred                       #C71585  199   21  133  353
	pallette["palevioletred"]         = "#DB7093"      # palevioletred                         #DB7093  219  112  147  478

	# Oranges
	pallette["lightsalmon"]           = "#FFA07A"      # lightsalmon                           #FFA07A  255  160  122  537
	pallette["coral"]                 = "#FF7F50"      # coral                                 #FF7F50  255  127   80  462
	pallette["tomato"]                = "#FF6347"      # tomato                                #FF6347  255   99   71  425
	pallette["orangered"]             = "#FF4500"      # orangered                             #FF4500  255   69    0  324
	pallette["darkorange"]            = "#FF8C00"      # darkorange                            #FF8C00  255  140    0  395
	pallette["orange"]                = "#FFA500"      # orange                                #FFA500  255  165    0  420

	# Yellows
	pallette["gold"]                  = "#FFD700"      # gold                                  #FFD700  255  215    0  470
	pallette["yellow"]                = "#FFFF00"      # yellow                                #FFFF00  255  255    0  510
	pallette["lightyellow"]           = "#FFFFE0"      # lightyellow                           #FFFFE0  255  255  224  734
	pallette["lemonchiffon"]          = "#FFFACD"      # lemonchiffon                          #FFFACD  255  250  205  710
	pallette["lightgoldenrodyellow"]  = "#FAFAD2"      # lightgoldenrodyellow                  #FAFAD2  250  250  210  710
	pallette["papayawhip"]            = "#FFEFD5"      # papayawhip                            #FFEFD5  255  239  213  707
	pallette["moccasin"]              = "#FFE4B5"      # moccasin                              #FFE4B5  255  228  181  664
	pallette["peachpuff"]             = "#FFDAB9"      # peachpuff                             #FFDAB9  255  218  185  658
	pallette["palegoldenrod"]         = "#EEE8AA"      # palegoldenrod                         #EEE8AA  238  232  170  640
	pallette["darkkhaki"]             = "#BDB76B"      # darkkhaki                             #BDB76B  189  183  107  479
	pallette["khaki"]                 = "#F0E68C"      # khaki                                 #F0E68C  240  230  140  610

	# Purples
	pallette["lavender"]              = "#E6E6FA"      # lavender                              #E6E6FA  230  230  250  710
	pallette["thistle"]               = "#D8BFD8"      # thistle                               #D8BFD8  216  191  216  623
	pallette["plum"]                  = "#DDA0DD"      # plum                                  #DDA0DD  221  160  221  602
	pallette["violet"]                = "#EE82EE"      # violet                                #EE82EE  238  130  238  606
	pallette["orchid"]                = "#DA70D6"      # orchid                                #DA70D6  218  112  214  544
	pallette["fuchsia"]               = "#FF00FF"      # fuchsia                               #FF00FF  255    0  255  510
	pallette["magenta"]               = "#FF00FF"      # magenta                               #FF00FF  255    0  255  510
	pallette["mediumorchid"]          = "#BA55D3"      # mediumorchid                          #BA55D3  186   85  211  482
	pallette["mediumpurple"]          = "#9370DB"      # mediumpurple                          #9370DB  147  112  219  478
	pallette["rebeccapurple"]         = "#663399"      # rebeccapurple                         #663399  102   51  153  306
	pallette["blueviolet"]            = "#8A2BE2"      # blueviolet                            #8A2BE2  138   43  226  407
	pallette["darkviolet"]            = "#9400D3"      # darkviolet                            #9400D3  148    0  211  359
	pallette["darkorchid"]            = "#9932CC"      # darkorchid                            #9932CC  153   50  204  407
	pallette["darkmagenta"]           = "#8B008B"      # darkmagenta                           #8B008B  139    0  139  278
	pallette["purple"]                = "#800080"      # purple                                #800080  128    0  128  256
	pallette["indigo"]                = "#4B0082"      # indigo                                #4B0082   75    0  130  205
	pallette["slateblue"]             = "#6A5ACD"      # slateblue                             #6A5ACD  106   90  205  401
	pallette["darkslateblue"]         = "#483D8B"      # darkslateblue                         #483D8B   72   61  139  272
	pallette["mediumslateblue"]       = "#7B68EE"      # mediumslateblue                       #7B68EE  123  104  238  465

	# Greens
	pallette["greenyellow"]           = "#ADFF2F"      # greenyellow                           #ADFF2F  173  255   47  475
	pallette["chartreuse"]            = "#7FFF00"      # chartreuse                            #7FFF00  127  255    0  382
	pallette["lawngreen"]             = "#7CFC00"      # lawngreen                             #7CFC00  124  252    0  376
	pallette["lime"]                  = "#00FF00"      # lime                                  #00FF00    0  255    0  255
	pallette["limegreen"]             = "#32CD32"      # limegreen                             #32CD32   50  205   50  305
	pallette["palegreen"]             = "#98FB98"      # palegreen                             #98FB98  152  251  152  555
	pallette["lightgreen"]            = "#90EE90"      # lightgreen                            #90EE90  144  238  144  526
	pallette["mediumspringgreen"]     = "#00FA9A"      # mediumspringgreen                     #00FA9A    0  250  154  404
	pallette["springgreen"]           = "#00FF7F"      # springgreen                           #00FF7F    0  255  127  382
	pallette["mediumseagreen"]        = "#3CB371"      # mediumseagreen                        #3CB371   60  179  113  352
	pallette["seagreen"]              = "#2E8B57"      # seagreen                              #2E8B57   46  139   87  272
	pallette["forestgreen"]           = "#228B22"      # forestgreen                           #228B22   34  139   34  207
	pallette["green"]                 = "#008000"      # green                                 #008000    0  128    0  128
	pallette["darkgreen"]             = "#006400"      # darkgreen                             #006400    0  100    0  100
	pallette["yellowgreen"]           = "#9ACD32"      # yellowgreen                           #9ACD32  154  205   50  409
	pallette["olivedrab"]             = "#6B8E23"      # olivedrab                             #6B8E23  107  142   35  284
	pallette["olive"]                 = "#808000"      # olive                                 #808000  128  128    0  256
	pallette["darkolivegreen"]        = "#556B2F"      # darkolivegreen                        #556B2F   85  107   47  239
	pallette["mediumaquamarine"]      = "#66CDAA"      # mediumaquamarine                      #66CDAA  102  205  170  477
	pallette["darkseagreen"]          = "#8FBC8F"      # darkseagreen                          #8FBC8F  143  188  143  474
	pallette["lightseagreen"]         = "#20B2AA"      # lightseagreen                         #20B2AA   32  178  170  380
	pallette["darkcyan"]              = "#008B8B"      # darkcyan                              #008B8B    0  139  139  278
	pallette["teal"]                  = "#008080"      # teal                                  #008080    0  128  128  256

	# Blues
	pallette["aqua"]                  = "#00FFFF"      # aqua                                  #00FFFF    0  255  255  510
	pallette["cyan"]                  = "#00FFFF"      # cyan                                  #00FFFF    0  255  255  510
	pallette["lightcyan"]             = "#E0FFFF"      # lightcyan                             #E0FFFF  224  255  255  734
	pallette["paleturquoise"]         = "#AFEEEE"      # paleturquoise                         #AFEEEE  175  238  238  651
	pallette["aquamarine"]            = "#7FFFD4"      # aquamarine                            #7FFFD4  127  255  212  594
	pallette["turquoise"]             = "#40E0D0"      # turquoise                             #40E0D0   64  224  208  496
	pallette["mediumturquoise"]       = "#48D1CC"      # mediumturquoise                       #48D1CC   72  209  204  485
	pallette["darkturquoise"]         = "#00CED1"      # darkturquoise                         #00CED1    0  206  209  415
	pallette["cadetblue"]             = "#5F9EA0"      # cadetblue                             #5F9EA0   95  158  160  413
	pallette["steelblue"]             = "#4682B4"      # steelblue                             #4682B4   70  130  180  380
	pallette["lightsteelblue"]        = "#B0C4DE"      # lightsteelblue                        #B0C4DE  176  196  222  594
	pallette["powderblue"]            = "#B0E0E6"      # powderblue                            #B0E0E6  176  224  230  630
	pallette["lightblue"]             = "#ADD8E6"      # lightblue                             #ADD8E6  173  216  230  619
	pallette["skyblue"]               = "#87CEEB"      # skyblue                               #87CEEB  135  206  235  576
	pallette["lightskyblue"]          = "#87CEFA"      # lightskyblue                          #87CEFA  135  206  250  591
	pallette["deepskyblue"]           = "#00BFFF"      # deepskyblue                           #00BFFF    0  191  255  446
	pallette["dodgerblue"]            = "#1E90FF"      # dodgerblue                            #1E90FF   30  144  255  429
	pallette["cornflowerblue"]        = "#6495ED"      # cornflowerblue                        #6495ED  100  149  237  486
	pallette["mediumslateblue"]       = "#7B68EE"      # mediumslateblue                       #7B68EE  123  104  238  465
	pallette["royalblue"]             = "#4169E1"      # royalblue                             #4169E1   65  105  225  395
	pallette["blue"]                  = "#0000FF"      # blue                                  #0000FF    0    0  255  255
	pallette["mediumblue"]            = "#0000CD"      # mediumblue                            #0000CD    0    0  205  205
	pallette["darkblue"]              = "#00008B"      # darkblue                              #00008B    0    0  139  139
	pallette["navy"]                  = "#000080"      # navy                                  #000080    0    0  128  128
	pallette["midnightblue"]          = "#191970"      # midnightblue                          #191970   25   25  112  162

	# Browns
	pallette["cornsilk"]              = "#FFF8DC"      # cornsilk                              #FFF8DC  255  248  220  723
	pallette["blanchedalmond"]        = "#FFEBCD"      # blanchedalmond                        #FFEBCD  255  235  205  695
	pallette["bisque"]                = "#FFE4C4"      # bisque                                #FFE4C4  255  228  196  679
	pallette["navajowhite"]           = "#FFDEAD"      # navajowhite                           #FFDEAD  255  222  173  650
	pallette["wheat"]                 = "#F5DEB3"      # wheat                                 #F5DEB3  245  222  179  646
	pallette["burlywood"]             = "#DEB887"      # burlywood                             #DEB887  222  184  135  541
	pallette["tan"]                   = "#D2B48C"      # tan                                   #D2B48C  210  180  140  530
	pallette["rosybrown"]             = "#BC8F8F"      # rosybrown                             #BC8F8F  188  143  143  474
	pallette["sandybrown"]            = "#F4A460"      # sandybrown                            #F4A460  244  164   96  504
	pallette["goldenrod"]             = "#DAA520"      # goldenrod                             #DAA520  218  165   32  415
	pallette["darkgoldenrod"]         = "#B8860B"      # darkgoldenrod                         #B8860B  184  134   11  329
	pallette["peru"]                  = "#CD853F"      # peru                                  #CD853F  205  133   63  401
	pallette["chocolate"]             = "#D2691E"      # chocolate                             #D2691E  210  105   30  345
	pallette["saddlebrown"]           = "#8B4513"      # saddlebrown                           #8B4513  139   69   19  227
	pallette["sienna"]                = "#A0522D"      # sienna                                #A0522D  160   82   45  287
	pallette["brown"]                 = "#A52A2A"      # brown                                 #A52A2A  165   42   42  249
	pallette["maroon"]                = "#800000"      # maroon                                #800000  128    0    0  128

	# Whites
	pallette["white"]                 = "#FFFFFF"      # white                                 #FFFFFF  255  255  255  765
	pallette["snow"]                  = "#FFFAFA"      # snow                                  #FFFAFA  255  250  250  755
	pallette["honeydew"]              = "#F0FFF0"      # honeydew                              #F0FFF0  240  255  240  735
	pallette["mintcream"]             = "#F5FFFA"      # mintcream                             #F5FFFA  245  255  250  750
	pallette["azure"]                 = "#F0FFFF"      # azure                                 #F0FFFF  240  255  255  750
	pallette["aliceblue"]             = "#F0F8FF"      # aliceblue                             #F0F8FF  240  248  255  743
	pallette["ghostwhite"]            = "#F8F8FF"      # ghostwhite                            #F8F8FF  248  248  255  751
	pallette["whitesmoke"]            = "#F5F5F5"      # whitesmoke                            #F5F5F5  245  245  245  735
	pallette["seashell"]              = "#FFF5EE"      # seashell                              #FFF5EE  255  245  238  738
	pallette["beige"]                 = "#F5F5DC"      # beige                                 #F5F5DC  245  245  220  710
	pallette["oldlace"]               = "#FDF5E6"      # oldlace                               #FDF5E6  253  245  230  728
	pallette["floralwhite"]           = "#FFFAF0"      # floralwhite                           #FFFAF0  255  250  240  745
	pallette["ivory"]                 = "#FFFFF0"      # ivory                                 #FFFFF0  255  255  240  750
	pallette["antiquewhite"]          = "#FAEBD7"      # antiquewhite                          #FAEBD7  250  235  215  700
	pallette["linen"]                 = "#FAF0E6"      # linen                                 #FAF0E6  250  240  230  720
	pallette["lavenderblush"]         = "#FFF0F5"      # lavenderblush                         #FFF0F5  255  240  245  740
	pallette["mistyrose"]             = "#FFE4E1"      # mistyrose                             #FFE4E1  255  228  225  708

	# Grays
	pallette["gainsboro"]             = "#DCDCDC"      # gainsboro                             #DCDCDC  220  220  220  660
	pallette["lightgray"]             = "#D3D3D3"      # lightgray                             #D3D3D3  211  211  211  633
#	pallette["lightgrey"]             = "#D3D3D3"      # lightgrey                             #D3D3D3  211  211  211  633
	pallette["silver"]                = "#C0C0C0"      # silver                                #C0C0C0  192  192  192  576
	pallette["darkgray"]              = "#A9A9A9"      # darkgray                              #A9A9A9  169  169  169  507
#	pallette["darkgrey"]              = "#A9A9A9"      # darkgrey                              #A9A9A9  169  169  169  507
	pallette["gray"]                  = "#808080"      # gray                                  #808080  128  128  128  384
#	pallette["grey"]                  = "#808080"      # grey                                  #808080  128  128  128  384
	pallette["dimgray"]               = "#696969"      # dimgray                               #696969  105  105  105  315
#	pallette["dimgrey"]               = "#696969"      # dimgrey                               #696969  105  105  105  315
	pallette["lightslategray"]        = "#778899"      # lightslategray                        #778899  119  136  153  408
#	pallette["lightslategrey"]        = "#778899"      # lightslategrey                        #778899  119  136  153  408
	pallette["slategray"]             = "#708090"      # slategray                             #708090  112  128  144  384
#	pallette["slategrey"]             = "#708090"      # slategrey                             #708090  112  128  144  384
	pallette["darkslategray"]         = "#2F4F4F"      # darkslategray                         #2F4F4F   47   79   79  205
#	pallette["darkslategrey"]         = "#2F4F4F"      # darkslategrey                         #2F4F4F   47   79   79  205
	pallette["black"]                 = "#000000"      # black                                 #000000    0    0    0    0


	str_close = "\033[0m"

	hex_color_pattern = re.compile(r'#[0-9A-Fa-f]{6}\b')

	#<=====>#

	def __init__(self):

		# Check for a specific environment variable set by Windows Terminal
		# WT_SESSION is a common variable set by Windows Terminal
		self.probably_will_work = False
		if not self.probably_will_work:
			term_check = os.getenv('WT_SESSION')
			if term_check:
				self.probably_will_work = True

		if not self.probably_will_work:
			term_check = os.getenv('TERM_PROGRAM')
			if term_check and term_check == 'vscode':
				self.probably_will_work = True

	#<=====>#

	def rand_hex(self):
		"""
		Generates a random hex color code.
		Returns:
			str: A hex color code.
		"""
		# Randomly generate RGB values
		R = random.randint(0, 255)
		G = random.randint(0, 255)
		B = random.randint(0, 255)
		# Format as a hex color code
		return f"#{R:02X}{G:02X}{B:02X}"

	#<=====>#

	def name2hex(self, color):
#		print('name2hex(color={})'.format(color))
		"""
		Resolves named colors to their hexadecimal values.
		:param color: The named color or hexadecimal value.
		:return: The hexadecimal color code.
		"""
		# Convert color to lowercase for case-insensitive matching
		color = color.lower()
#		print(self.pallette[color])
		# Return the hexadecimal value from the dictionary if available, otherwise assume it's already a hex code
		return self.pallette.get(color, color)

	#<=====>#

	def hex2int(self, x):
		return int(x, 16)

	#<=====>#

	def hex2rgb(self, x):
		r = self.hex2int(x[1:3])
		g = self.hex2int(x[3:5])
		b = self.hex2int(x[5:7])
		return r, g, b

	#<=====>#

	def int2hex(self, x):
		return format(x, '02x')

	#<=====>#

	def lumi_get(self, x):
		r = self.hex2int(x[1:3])
		g = self.hex2int(x[3:5])
		b = self.hex2int(x[5:7])
		l = round(0.2126 * r + 0.7152 * g + 0.0722 * b,2)
		return l

	#<=====>#

	def lumi_inv_hex(self, x):
		lumi = c.lumi_get(x)
		if lumi >= 191:
			inv_color = self.name2hex('black')
		elif lumi >= 127:
			inv_color = self.name2hex('red')
		elif lumi >= 63:
			inv_color = self.name2hex('yellow')
		else:
			inv_color = self.name2hex('white')
		return inv_color

	#<=====>#

	def inv_hex(self, color_cd):
		r = self.hex2int(color_cd[1:3])
		g = self.hex2int(color_cd[3:5])
		b = self.hex2int(color_cd[5:7])
		r_inv = 255 - r
		g_inv = 255 - g
		b_inv = 255 - b
		r_new = self.int2hex(r_inv)
		g_new = self.int2hex(g_inv)
		b_new = self.int2hex(b_inv)
		inv_color = '#{}{}{}'.format(r_new, g_new, b_new)
#		print('color_cd : {}, r : {}, g : {}, b : {}, r_inv : {}, g_inv : {}, b_inv : {}, r_new : {}, g_new : {}, b_new : {}, inv_color : {}'.format(color_cd, r, g, b, r_inv, g_inv, b_inv, r_new, g_new, b_new, inv_color))
		return inv_color

	#<=====>#

	def color_string(self, text, font_color, bg_color='black', bold=False, italic=False, length=0, align='left'):
#		print('color_string(self, text={}, font_color={}, bg_color={}, bold={}, italic={}, length={}, align={})'.format(text, font_color, bg_color, bold, italic, length, align))
#		print('')
#		print('color_string(text={}, font_color={}, bg_color={}, bold={}, italic={}, length={}, align={})'.format(text, font_color, bg_color, bold, italic, length, align))
#		print('length : {} ({})'.format(length, type(length)))
		if length: length = int(length)
		"""
		Returns a colorized string using ANSI escape sequences.
		:param text: The text to be colorized.
		:param font_color: The font color (name or hex).
		:param bg_color: The background color (name or hex).
		:param bold: Boolean to indicate if text should be bold.
		:param italic: Boolean to indicate if text should be italic.
		:return: A string with ANSI escape codes.
		"""

		if align == 'left': align_str = '<'
		elif align == 'center': align_str = '^'
		elif align == 'right': align_str = '>'
		else: align_str = ''

		if length > 0:
			length_str = length
		else:
			length_str = ''

		if align_str == '' and length_str == '':
			m = '{}'
		else:
			m = '{:'
			m += '{}{}'.format(align_str, length_str)
			m += '}'
#		print(m)
		text = m.format(text)

		if not self.probably_will_work:
#			print(term_check)
			return text

		# Resolve named colors or validate hex codes

#		print('font_color : {}, bg_color : {}'.format(font_color, bg_color))
#		print('self.hex_color_pattern.match(font_color) : {}'.format(self.hex_color_pattern.match(font_color)))
		if not self.hex_color_pattern.match(font_color):
			font_color = self.name2hex(font_color)
#			print('font_color : {}'.format(font_color))
#		print('self.hex_color_pattern.match(bg_color) : {}'.format(self.hex_color_pattern.match(bg_color)))
		if not self.hex_color_pattern.match(bg_color):
			bg_color = self.name2hex(bg_color)
#			print('bg_color : {}'.format(bg_color))

#		print('font_color : {}, bg_color : {}'.format(font_color, bg_color))
		font_r, font_g, font_b = int(font_color[1:3], 16), int(font_color[3:5], 16), int(font_color[5:7], 16)
		bg_r, bg_g, bg_b = int(bg_color[1:3], 16), int(bg_color[3:5], 16), int(bg_color[5:7], 16)

		# Build the ANSI escape sequence for styles and colors
		style_code = ''
		if bold:
			style_code += '\x1b[1m'
		if italic:
			style_code += '\x1b[3m'
		r = f"{style_code}\x1b[38;2;{font_r};{font_g};{font_b}m\x1b[48;2;{bg_r};{bg_g};{bg_b}m{text}\x1b[0m"
		r += self.str_close
		return r

	#<=====>#

	def color_print(self, text, font_color, bg_color='black', bold=False, italic=False, length=0, align='left'):
#		print('color_print(self, text={}, font_color={}, bg_color={}, bold={}, italic={}, length={}, align={})'.format(text, font_color, bg_color, bold, italic, length, align))
		"""
		Prints a colorized string to the terminal using ANSI escape sequences.
		:param text: The text to be printed.
		:param font_color: The font color (name or hex).
		:param bg_color: The background color (name or hex).
		:param bold: Boolean to indicate if text should be bold.
		:param italic: Boolean to indicate if text should be italic.
		"""
		colorized_text = self.color_string(text, font_color, bg_color, bold, italic, length, align)
		print(colorized_text)

	#<=====>#

	def demo1(self):
		pass

	#<=====>#

	def demo2(self):
		print()
		print()
		self.color_print('demo 2', 'white', 'purple', length=200, align='center')
		self.color_print('simple tests...', 'gold', 'mediumvioletred', length=200, align='center')
		print(self.color_string('green print cs test', 'green'))
		self.color_print('green print cp test', 'green')
		self.color_print('Hello World', 'black', 'white', italic=True)
		self.color_print('Yellow On OrangeRed', 'yellow', 'orangered', italic=True)
		self.color_print('#CC3300 On #0033CC', '#CC3300', '#0033CC', italic=True)
		for color in self.pallette:
			color_hex = self.pallette[color]
			r, g, b = self.hex2rgb(color_hex)
			lumi = self.lumi_get(color_hex)
			cp('{:<35}  {:>8}  {:>3}  {:>3}  {:>3}  {:>6.2f}  {:>3}'.format(color, color_hex, r, g, b, lumi, r+g+b), self.lumi_inv_hex(color_hex), color_hex)

	#<=====>#

	def demo3(self):
		print()
		print()
		self.color_print('demo 3', 'white', 'purple', length=200, align='center')
		self.color_print('random named font color and background colors...', 'gold', 'mediumvioletred', length=200, align='center')
		for i in range(0,25):
			fc = self.rand_hex()
			bgc = self.rand_hex()
			self.color_print(f'{i+1} Random Font Color ({fc}) On A Random Background Color ({bgc})', fc, bgc)

	#<=====>#

	def demo4(self):
		print()
		print()
		self.color_print('demo 4', 'white', 'purple', length=200, align='center')
		self.color_print('loop through the named background colors and use white, yellow, red or black font colors...', 'gold', 'mediumvioletred', length=200, align='center')
		row_str = ''
		cnt = 0
		for color in self.pallette:
			if cnt % 4 == 0:
				print(row_str)
				row_str = ''
			color_score = self.lumi_get(self.pallette[color])
			if color_score >= 191:
				font_color = 'black'
			elif color_score >= 127:
				font_color = 'red'
			elif color_score >= 63:
				font_color = 'yellow'
			else:
				font_color = 'white'
			desc_str = '{} ({}/{})'.format(color, self.pallette[color], self.pallette[font_color])
			prt_str = self.color_string(desc_str, font_color=font_color, bg_color=color, align='center', length=40, italic=True)
			if row_str != '': row_str += ' | '
			row_str += prt_str
			cnt += 1
		print(row_str)

	#<=====>#

	def demo5(self):
		print()
		print()
		self.color_print('demo 5', 'white', 'purple', length=200, align='center')
		self.color_print('loop through the named background colors and calculate an inverted font colors...', 'gold', 'mediumvioletred', length=200, align='center')
		row_str = ''
		cnt = 0
		for color in self.pallette:
			if cnt % 4 == 0:
				print(row_str)
				row_str = ''
			bg_color = self.pallette[color]
			font_color = self.inv_hex(self.pallette[color])
			desc_str = '{} ({}/{})'.format(color, bg_color, font_color)
			prt_str = self.color_string(desc_str, font_color=font_color, bg_color=color, align='center', length=40, italic=True)
			if row_str != '': row_str += ' | '
			row_str += prt_str
			cnt += 1
		print(row_str)

	#<=====>#

	def demo6(self):
		print()
		print()
		self.color_print('demo 6', 'white', 'purple', length=200, align='center')
		self.color_print('loop through the named background colors and and then all named font colors...', 'gold', 'mediumvioletred', length=200, align='center')
		for bg_color in self.pallette:
			row_str = ''
			cnt = 0
			print()
			bg_color_hex = self.name2hex(bg_color)
			# bg_lumi = self.lumi_get(bg_color_hex)
			style_color_hex = self.inv_hex(bg_color_hex)
#			style_color_hex = self.lumi_inv_hex(bg_color_hex)
			# style_lumi = self.lumi_get(style_color_hex)
#			print('bg_color_hex : {}, color_hex : {}, bg_lumi : {}, style_lumi : {}'.format(bg_color_hex, style_color_hex, bg_lumi, style_lumi))
			cp('{} ({}) Background with {} Font Color'.format(bg_color.upper(), bg_color_hex, style_color_hex), font_color=style_color_hex, bg_color=bg_color_hex, italic=True, length=181, align='center')
			cp('-'*181, font_color=bg_color_hex, bg_color=style_color_hex, length=181)
			for font_color in self.pallette:
				if cnt > 0 and cnt % 8 == 0:
					print(row_str)
					row_str = ''
				desc_str = '{}'.format(font_color)
				if cnt % 2 == 0:
					prt_str = self.color_string(desc_str, font_color, bg_color_hex, align='center', length=20, italic=True)
				else:
					prt_str = self.color_string(desc_str, font_color, bg_color_hex, align='center', length=20)
				div = cs(' | ', font_color=bg_color_hex, bg_color=style_color_hex)
				if row_str != '': row_str += div
				row_str += prt_str
				cnt += 1
			print(row_str)

	#<=====>#

	def demo7(self):
		print()
		print()
		self.color_print('demo 7', 'white', 'purple', length=200, align='center')
		self.color_print('loop through some background colors with white & black font colors...', 'gold', 'mediumvioletred', length=200, align='center')
		color_list = ('00','11','22','33','44','55','66','77','88','99','AA','BB','CC','DD','EE','FF')
#		color_list = ('00','33','66','99','CC','FF')
		# pallette = []
		for red_val in color_list:
			for green_val in color_list:
				row_str = ''
				cnt = 0
				for blue_val in color_list:
					cnt += 1
					hex_color = f'#{red_val}{green_val}{blue_val}'
					w = cs(text=hex_color, font_color='#FFFFFF', bg_color=hex_color)
					b = cs(text=hex_color, font_color='#000000', bg_color=hex_color)
					if cnt < len(color_list):
						wb = '{}{} | '.format(w,b)
					else:
						wb = '{}{}'.format(w,b)
					row_str += wb
				print(row_str)

	#<=====>#

	def demo8(self):
		print()
		print()
		self.color_print('demo 8', 'white', 'purple', length=200, align='center')
		self.color_print('loop through some background colors with calculated inverse font colors...', 'gold', 'mediumvioletred', length=200, align='center')
		color_list = ('00','11','22','33','44','55','66','77','88','99','AA','BB','CC','DD','EE','FF')
		for red_val in color_list:
			for green_val in color_list:
				row_str = ''
				cnt = 0
				for blue_val in color_list:
					cnt += 1
					bg_hex_color = f'#{red_val}{green_val}{blue_val}'
					font_hex_color = self.inv_hex(bg_hex_color)
					font_hex_color = self.lumi_inv_hex(bg_hex_color)
					row_str += cs(text='{} {}'.format(font_hex_color, bg_hex_color), font_color=font_hex_color, bg_color=bg_hex_color)
					if cnt < len(color_list): row_str += ' '
				print(row_str)

	#<=====>#

	def demo9(self):
		print()
		print()
		self.color_print('demo 9', 'white', 'purple', length=200, align='center')
		self.color_print('loop through some background colors with calculated inverse font colors...', 'gold', 'mediumvioletred', length=200, align='center')
#		hex_vals = ('0','3','6','9','C','F')
#		hex_vals = ('0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F')
		hex_vals = ('0','2','4','6','8','A','C','E')
		possible_vals = []
		for d1 in hex_vals:
			for d2 in hex_vals:
				hn = '{}{}'.format(d1,d2)
				possible_vals.append(hn)
		row_str = ''
		cnt = 0
		all_cnt = 0
		for red_val in possible_vals:
			for green_val in possible_vals:
				for blue_val in possible_vals:
					cnt += 1
					all_cnt += 1
					bg_hex_color = f'#{red_val}{green_val}{blue_val}'
					font_hex_color = self.inv_hex(bg_hex_color)
#					font_hex_color = self.lumi_inv_hex(bg_hex_color)
					row_str += cs(text='{} {}'.format(font_hex_color, bg_hex_color), font_color=font_hex_color, bg_color=bg_hex_color)
					if cnt < len(hex_vals):
						row_str += ' '
					else:
						print(row_str)
						row_str = ''
						cnt = 0
		print('all_cnt : {}'.format(all_cnt))

#bbffff #440000 #bbffee #440011 #bbffdd #440022 #bbffcc #440033 #bbffbb #440044 #bbffaa #440055 #bbff99 #440066 #bbff88 #440077 #bbff77 #440088 #bbff66 #440099 #bbff55 #4400AA #bbff44 #4400BB #bbff33 #4400CC #bbff22 #4400DD #bbff11 #4400EE #bbff00 #4400FF
#bbeeff #441100 #bbeeee #441111 #bbeedd #441122 #bbeecc #441133 #bbeebb #441144 #bbeeaa #441155 #bbee99 #441166 #bbee88 #441177 #bbee77 #441188 #bbee66 #441199 #bbee55 #4411AA #bbee44 #4411BB #bbee33 #4411CC #bbee22 #4411DD #bbee11 #4411EE #bbee00 #4411FF
#bbddff #442200 #bbddee #442211 #bbdddd #442222 #bbddcc #442233 #bbddbb #442244 #bbddaa #442255 #bbdd99 #442266 #bbdd88 #442277 #bbdd77 #442288 #bbdd66 #442299 #bbdd55 #4422AA #bbdd44 #4422BB #bbdd33 #4422CC #bbdd22 #4422DD #bbdd11 #4422EE #bbdd00 #4422FF
#bbccff #443300 #bbccee #443311 #bbccdd #443322 #bbcccc #443333 #bbccbb #443344 #bbccaa #443355 #bbcc99 #443366 #bbcc88 #443377 #bbcc77 #443388 #bbcc66 #443399 #bbcc55 #4433AA #bbcc44 #4433BB #bbcc33 #4433CC #bbcc22 #4433DD #bbcc11 #4433EE #bbcc00 #4433FF
#bbbbff #444400 #bbbbee #444411 #bbbbdd #444422 #bbbbcc #444433 #bbbbbb #444444 #bbbbaa #444455 #bbbb99 #444466 #bbbb88 #444477 #bbbb77 #444488 #bbbb66 #444499 #bbbb55 #4444AA #bbbb44 #4444BB #bbbb33 #4444CC #bbbb22 #4444DD #bbbb11 #4444EE #bbbb00 #4444FF
#bbaaff #445500 #bbaaee #445511 #bbaadd #445522 #bbaacc #445533 #bbaabb #445544 #bbaaaa #445555 #bbaa99 #445566 #bbaa88 #445577 #bbaa77 #445588 #bbaa66 #445599 #bbaa55 #4455AA #bbaa44 #4455BB #bbaa33 #4455CC #bbaa22 #4455DD #bbaa11 #4455EE #bbaa00 #4455FF
#bb99ff #446600 #bb99ee #446611 #bb99dd #446622 #bb99cc #446633 #bb99bb #446644 #bb99aa #446655 #bb9999 #446666 #bb9988 #446677 #bb9977 #446688 #bb9966 #446699 #bb9955 #4466AA #bb9944 #4466BB #bb9933 #4466CC #bb9922 #4466DD #bb9911 #4466EE #bb9900 #4466FF
#bb88ff #447700 #bb88ee #447711 #bb88dd #447722 #bb88cc #447733 #bb88bb #447744 #bb88aa #447755 #bb8899 #447766 #bb8888 #447777 #bb8877 #447788 #bb8866 #447799 #bb8855 #4477AA #bb8844 #4477BB #bb8833 #4477CC #bb8822 #4477DD #bb8811 #4477EE #bb8800 #4477FF
#bb77ff #448800 #bb77ee #448811 #bb77dd #448822 #bb77cc #448833 #bb77bb #448844 #bb77aa #448855 #bb7799 #448866 #bb7788 #448877 #bb7777 #448888 #bb7766 #448899 #bb7755 #4488AA #bb7744 #4488BB #bb7733 #4488CC #bb7722 #4488DD #bb7711 #4488EE #bb7700 #4488FF
#bb66ff #449900 #bb66ee #449911 #bb66dd #449922 #bb66cc #449933 #bb66bb #449944 #bb66aa #449955 #bb6699 #449966 #bb6688 #449977 #bb6677 #449988 #bb6666 #449999 #bb6655 #4499AA #bb6644 #4499BB #bb6633 #4499CC #bb6622 #4499DD #bb6611 #4499EE #bb6600 #4499FF
#bb55ff #44AA00 #bb55ee #44AA11 #bb55dd #44AA22 #bb55cc #44AA33 #bb55bb #44AA44 #bb55aa #44AA55 #bb5599 #44AA66 #bb5588 #44AA77 #bb5577 #44AA88 #bb5566 #44AA99 #bb5555 #44AAAA #bb5544 #44AABB #bb5533 #44AACC #bb5522 #44AADD #bb5511 #44AAEE #bb5500 #44AAFF
#bb44ff #44BB00 #bb44ee #44BB11 #bb44dd #44BB22 #bb44cc #44BB33 #bb44bb #44BB44 #bb44aa #44BB55 #bb4499 #44BB66 #bb4488 #44BB77 #bb4477 #44BB88 #bb4466 #44BB99 #bb4455 #44BBAA #bb4444 #44BBBB #bb4433 #44BBCC #bb4422 #44BBDD #bb4411 #44BBEE #bb4400 #44BBFF
#bb33ff #44CC00 #bb33ee #44CC11 #bb33dd #44CC22 #bb33cc #44CC33 #bb33bb #44CC44 #bb33aa #44CC55 #bb3399 #44CC66 #bb3388 #44CC77 #bb3377 #44CC88 #bb3366 #44CC99 #bb3355 #44CCAA #bb3344 #44CCBB #bb3333 #44CCCC #bb3322 #44CCDD #bb3311 #44CCEE #bb3300 #44CCFF
#bb22ff #44DD00 #bb22ee #44DD11 #bb22dd #44DD22 #bb22cc #44DD33 #bb22bb #44DD44 #bb22aa #44DD55 #bb2299 #44DD66 #bb2288 #44DD77 #bb2277 #44DD88 #bb2266 #44DD99 #bb2255 #44DDAA #bb2244 #44DDBB #bb2233 #44DDCC #bb2222 #44DDDD #bb2211 #44DDEE #bb2200 #44DDFF
#bb11ff #44EE00 #bb11ee #44EE11 #bb11dd #44EE22 #bb11cc #44EE33 #bb11bb #44EE44 #bb11aa #44EE55 #bb1199 #44EE66 #bb1188 #44EE77 #bb1177 #44EE88 #bb1166 #44EE99 #bb1155 #44EEAA #bb1144 #44EEBB #bb1133 #44EECC #bb1122 #44EEDD #bb1111 #44EEEE #bb1100 #44EEFF
#bb00ff #44FF00 #bb00ee #44FF11 #bb00dd #44FF22 #bb00cc #44FF33 #bb00bb #44FF44 #bb00aa #44FF55 #bb0099 #44FF66 #bb0088 #44FF77 #bb0077 #44FF88 #bb0066 #44FF99 #bb0055 #44FFAA #bb0044 #44FFBB #bb0033 #44FFCC #bb0022 #44FFDD #bb0011 #44FFEE #bb0000 #44FFFF



#<=====>#

c = CLR()

#<=====>#

def cs(text, font_color, bg_color='black', bold=False, italic=False, length=0, align='left'):
	r = c.color_string(text, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic, length=length, align=align)
	return r

#<=====>#

def cp(text, font_color, bg_color='black', bold=False, italic=False, length=0, align='left'):
	c.color_print(text, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic, length=length, align=align)

#<=====>#

if __name__ == "__main__":
	# Example usage
	cp('demos','white','green')
	c.demo1()
	c.demo2()
	c.demo3()
	c.demo4()
	c.demo5()
	c.demo6()
	c.demo7()
	c.demo8()
	c.demo9()

#	print("WT_SESSION       :", os.getenv('WT_SESSION'))
#	print("TERM_PROGRAM     :", os.getenv('TERM_PROGRAM'))
#	print("TERM_SESSION_TYPE:", os.getenv('TERM_SESSION_TYPE'))

#<=====>#

