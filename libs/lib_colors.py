#<=====>#
# Description
#<=====>#



#<=====>#
# Known To Do List
#<=====>#



#<=====>#
# Imports
#<=====>#
import os
import random
import re


#<=====>#
# Variables
#<=====>#
lib_name            = 'lib_colors'
log_name            = 'lib_colors'


#<=====>#
# Assignments Pre
#<=====>#



#<=====>#
# Classes
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
		"""
		Resolves named colors to their hexadecimal values.
		:param color: The named color or hexadecimal value.
		:return: The hexadecimal color code.
		"""
		# Convert color to lowercase for case-insensitive matching
		color = color.lower()
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
		return inv_color

	#<=====>#

	def color_string(self, text, font_color, bg_color='black', bold=False, italic=False, length=0, align='left'):
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

		length_str = max(length, len(text))

		if align == 'left': align_str = '<'
		elif align == 'center': align_str = '^'
		elif align == 'right': align_str = '>'
		else: align_str = ''

		text = f'{text:{align_str}{length_str}}'

		if not self.probably_will_work:
#			print(term_check)
			return text

		# Resolve named colors or validate hex codes

		if not self.hex_color_pattern.match(font_color):
			font_color = self.name2hex(font_color)
		if not self.hex_color_pattern.match(bg_color):
			bg_color = self.name2hex(bg_color)

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
			# style_lumi = self.lumi_get(style_color_hex)
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
					row_str += cs(text='{} {}'.format(font_hex_color, bg_hex_color), font_color=font_hex_color, bg_color=bg_hex_color)
					if cnt < len(hex_vals):
						row_str += ' '
					else:
						print(row_str)
						row_str = ''
						cnt = 0
		print('all_cnt : {}'.format(all_cnt))

# helpful regexp replace for converting sections of code 
# find: tkn\['(\w+)'\]
# repl: tkn.\1

#<=====>#
# Functions
#<=====>#

def K(in_str, print_tf=True, *args, **kwargs):
	if print_tf:
		cp(in_str, font_color='black', *args, **kwargs)
	else:
		return cs(text=in_str, font_color='black', *args, **kwargs)

#<=====>#

def R(in_str, print_tf=True, *args, **kwargs):
	if print_tf:
		cp(in_str, font_color='red', *args, **kwargs)
	else:
		return cs(text=in_str, font_color='red', *args, **kwargs)

#<=====>#

def G(in_str, print_tf=True, *args, **kwargs):
	if print_tf:
		cp(in_str, font_color='green', *args, **kwargs)
	else:
		return cs(text=in_str, font_color='green', *args, **kwargs)

#<=====>#

def Y(in_str, print_tf=True, *args, **kwargs):
	if print_tf:
		cp(in_str, font_color='yellow', *args, **kwargs)
	else:
		return cs(text=in_str, font_color='yellow', *args, **kwargs)

#<=====>#

def B(in_str, print_tf=True, *args, **kwargs):
	if print_tf:
		cp(in_str, font_color='blue', *args, **kwargs)
	else:
		return cs(text=in_str, font_color='blue', *args, **kwargs)

#<=====>#

def M(in_str, print_tf=True, *args, **kwargs):
	if print_tf:
		cp(in_str, font_color='magenta', *args, **kwargs)
	else:
		return cs(text=in_str, font_color='magenta', *args, **kwargs)

#<=====>#

def C(in_str, print_tf=True, *args, **kwargs):
	if print_tf:
		cp(in_str, font_color='cyan', *args, **kwargs)
	else:
		return cs(text=in_str, font_color='cyan', *args, **kwargs)

#<=====>#

def W(in_str, print_tf=True, *args, **kwargs):
	if print_tf:
		cp(in_str, font_color='white', *args, **kwargs)
	else:
		return cs(text=in_str, font_color='white', *args, **kwargs)

#<=====>#

def LGy(in_str, print_tf=True, *args, **kwargs):
	if print_tf:
		cp(in_str, font_color='light_grey', *args, **kwargs)
	else:
		return cs(text=in_str, font_color='light_grey', *args, **kwargs)

#<=====>#

def DGy(in_str, print_tf=True, *args, **kwargs):
	if print_tf:
		cp(in_str, font_color='dark_grey', *args, **kwargs)
	else:
		return cs(text=in_str, font_color='dark_grey', *args, **kwargs)

#<=====>#

def LR(in_str, print_tf=True, *args, **kwargs):
	if print_tf:
		cp(in_str, font_color='light_red', *args, **kwargs)
	else:
		return cs(text=in_str, font_color='light_red', *args, **kwargs)

#<=====>#

def LG(in_str, print_tf=True, *args, **kwargs):
	if print_tf:
		cp(in_str, font_color='light_green', *args, **kwargs)
	else:
		return cs(text=in_str, font_color='light_green', *args, **kwargs)

#<=====>#

def LY(in_str, print_tf=True, *args, **kwargs):
	if print_tf:
		cp(in_str, font_color='light_yellow', *args, **kwargs)
	else:
		return cs(text=in_str, font_color='light_yellow', *args, **kwargs)

#<=====>#

def LB(in_str, print_tf=True, *args, **kwargs):
	if print_tf:
		cp(in_str, font_color='light_blue', *args, **kwargs)
	else:
		return cs(text=in_str, font_color='light_blue', *args, **kwargs)

#<=====>#

def LM(in_str, print_tf=True, *args, **kwargs):
	if print_tf:
		cp(in_str, font_color='light_magenta', *args, **kwargs)
	else:
		return cs(text=in_str, font_color='light_magenta', *args, **kwargs)

#<=====>#

def LC(in_str, print_tf=True, *args, **kwargs):
	if print_tf:
		cp(in_str, font_color='light_cyan', *args, **kwargs)
	else:
		return cs(text=in_str, font_color='light_cyan', *args, **kwargs)

#<=====>#

def KoK(in_str, print_tf=True, *args, **kwargs):
	if print_tf:
		cp(in_str, font_color='black', bg_color='black', *args, **kwargs)
	else:
		return cs(text=in_str, font_color='black', bg_color='black', *args, **kwargs)

#<=====>#
		
def RoK(in_str, print_tf=True, *args, **kwargs):
	if print_tf:
		cp(in_str, font_color='red', bg_color='black', *args, **kwargs)
	else:
		return cs(text=in_str, font_color='red', bg_color='black', *args, **kwargs)

#<=====>#

def GoK(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='green', bg_color='black', *args, **kwargs)
	else: return cs(text=in_str, font_color='green', bg_color='black', *args, **kwargs)

#<=====>#

def YoK(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='yellow', bg_color='black', *args, **kwargs)
	else: return cs(text=in_str, font_color='yellow', bg_color='black', *args, **kwargs)

#<=====>#

def BoK(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='blue', bg_color='black', *args, **kwargs)
	else: return cs(text=in_str, font_color='blue', bg_color='black', *args, **kwargs)

#<=====>#

def MoK(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='magenta', bg_color='black', *args, **kwargs)
	else: return cs(text=in_str, font_color='magenta', bg_color='black', *args, **kwargs)

#<=====>#

def CoK(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='cyan', bg_color='black', *args, **kwargs)
	else: return cs(text=in_str, font_color='cyan', bg_color='black', *args, **kwargs)

#<=====>#

def WoK(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='white', bg_color='black', *args, **kwargs)
	else: return cs(text=in_str, font_color='white', bg_color='black', *args, **kwargs)

#<=====>#

def LGyoK(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_grey', bg_color='black', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_grey', bg_color='black', *args, **kwargs)

#<=====>#

def DGyoK(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='dark_grey', bg_color='black', *args, **kwargs)
	else: return cs(text=in_str, font_color='dark_grey', bg_color='black', *args, **kwargs)

#<=====>#

def LRoK(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_red', bg_color='black', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_red', bg_color='black', *args, **kwargs)

#<=====>#

def LGoK(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_green', bg_color='black', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_green', bg_color='black', *args, **kwargs)

#<=====>#

def LYoK(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_yellow', bg_color='black', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_yellow', bg_color='black', *args, **kwargs)

#<=====>#

def LBoK(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_blue', bg_color='black', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_blue', bg_color='black', *args, **kwargs)

#<=====>#

def LMoK(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_magenta', bg_color='black', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_magenta', bg_color='black', *args, **kwargs)

#<=====>#

def LCoK(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_cyan', bg_color='black', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_cyan', bg_color='black', *args, **kwargs)

#<=====>#

def KoR(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='black', bg_color='red', *args, **kwargs)
	else: return cs(text=in_str, font_color='black', bg_color='red', *args, **kwargs)

#<=====>#

def RoR(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='red', bg_color='red', *args, **kwargs)
	else: return cs(text=in_str, font_color='red', bg_color='red', *args, **kwargs)

#<=====>#

def GoR(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='green', bg_color='red', *args, **kwargs)
	else: return cs(text=in_str, font_color='green', bg_color='red', *args, **kwargs)

#<=====>#

def YoR(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='yellow', bg_color='red', *args, **kwargs)
	else: return cs(text=in_str, font_color='yellow', bg_color='red', *args, **kwargs)

#<=====>#

def BoR(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='blue', bg_color='red', *args, **kwargs)
	else: return cs(text=in_str, font_color='blue', bg_color='red', *args, **kwargs)

#<=====>#

def MoR(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='magenta', bg_color='red', *args, **kwargs)
	else: return cs(text=in_str, font_color='magenta', bg_color='red', *args, **kwargs)

#<=====>#

def CoR(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='cyan', bg_color='red', *args, **kwargs)
	else: return cs(text=in_str, font_color='cyan', bg_color='red', *args, **kwargs)

#<=====>#

def WoR(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='white', bg_color='red', *args, **kwargs)
	else: return cs(text=in_str, font_color='white', bg_color='red', *args, **kwargs)

#<=====>#

def LGyoR(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_grey', bg_color='red', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_grey', bg_color='red', *args, **kwargs)

#<=====>#

def DGyoR(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='dark_grey', bg_color='red', *args, **kwargs)
	else: return cs(text=in_str, font_color='dark_grey', bg_color='red', *args, **kwargs)

#<=====>#

def LRoR(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_red', bg_color='red', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_red', bg_color='red', *args, **kwargs)

#<=====>#

def LGoR(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_green', bg_color='red', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_green', bg_color='red', *args, **kwargs)

#<=====>#

def LYoR(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_yellow', bg_color='red', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_yellow', bg_color='red', *args, **kwargs)

#<=====>#

def LBoR(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_blue', bg_color='red', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_blue', bg_color='red', *args, **kwargs)

#<=====>#

def LMoR(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_magenta', bg_color='red', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_magenta', bg_color='red', *args, **kwargs)

#<=====>#

def LCoR(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_cyan', bg_color='red', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_cyan', bg_color='red', *args, **kwargs)

#<=====>#

def KoG(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='black', bg_color='green', *args, **kwargs)
	else: return cs(text=in_str, font_color='black', bg_color='green', *args, **kwargs)

#<=====>#

def RoG(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='red', bg_color='green', *args, **kwargs)
	else: return cs(text=in_str, font_color='red', bg_color='green', *args, **kwargs)

#<=====>#

def GoG(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='green', bg_color='green', *args, **kwargs)
	else: return cs(text=in_str, font_color='green', bg_color='green', *args, **kwargs)

#<=====>#

def YoG(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='yellow', bg_color='green', *args, **kwargs)
	else: return cs(text=in_str, font_color='yellow', bg_color='green', *args, **kwargs)

#<=====>#

def BoG(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='blue', bg_color='green', *args, **kwargs)
	else: return cs(text=in_str, font_color='blue', bg_color='green', *args, **kwargs)

#<=====>#

def MoG(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='magenta', bg_color='green', *args, **kwargs)
	else: return cs(text=in_str, font_color='magenta', bg_color='green', *args, **kwargs)

#<=====>#

def CoG(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='cyan', bg_color='green', *args, **kwargs)
	else: return cs(text=in_str, font_color='cyan', bg_color='green', *args, **kwargs)

#<=====>#

def WoG(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='white', bg_color='green', *args, **kwargs)
	else: return cs(text=in_str, font_color='white', bg_color='green', *args, **kwargs)

#<=====>#

def LGyoG(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_grey', bg_color='green', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_grey', bg_color='green', *args, **kwargs)

#<=====>#

def DGyoG(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='dark_grey', bg_color='green', *args, **kwargs)
	else: return cs(text=in_str, font_color='dark_grey', bg_color='green', *args, **kwargs)

#<=====>#

def LRoG(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_red', bg_color='green', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_red', bg_color='green', *args, **kwargs)

#<=====>#

def LGoG(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_green', bg_color='green', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_green', bg_color='green', *args, **kwargs)

#<=====>#

def LYoG(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_yellow', bg_color='green', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_yellow', bg_color='green', *args, **kwargs)

#<=====>#

def LBoG(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_blue', bg_color='green', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_blue', bg_color='green', *args, **kwargs)

#<=====>#

def LMoG(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_magenta', bg_color='green', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_magenta', bg_color='green', *args, **kwargs)

#<=====>#

def LCoG(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_cyan', bg_color='green', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_cyan', bg_color='green', *args, **kwargs)

#<=====>#

def KoY(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='black', bg_color='yellow', *args, **kwargs)
	else: return cs(text=in_str, font_color='black', bg_color='yellow', *args, **kwargs)

#<=====>#

def RoY(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='red', bg_color='yellow', *args, **kwargs)
	else: return cs(text=in_str, font_color='red', bg_color='yellow', *args, **kwargs)

#<=====>#

def GoY(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='green', bg_color='yellow', *args, **kwargs)
	else: return cs(text=in_str, font_color='green', bg_color='yellow', *args, **kwargs)

#<=====>#

def YoY(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='yellow', bg_color='yellow', *args, **kwargs)
	else: return cs(text=in_str, font_color='yellow', bg_color='yellow', *args, **kwargs)

#<=====>#

def BoY(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='blue', bg_color='yellow', *args, **kwargs)
	else: return cs(text=in_str, font_color='blue', bg_color='yellow', *args, **kwargs)

#<=====>#

def MoY(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='magenta', bg_color='yellow', *args, **kwargs)
	else: return cs(text=in_str, font_color='magenta', bg_color='yellow', *args, **kwargs)

#<=====>#

def CoY(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='cyan', bg_color='yellow', *args, **kwargs)
	else: return cs(text=in_str, font_color='cyan', bg_color='yellow', *args, **kwargs)

#<=====>#

def WoY(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='white', bg_color='yellow', *args, **kwargs)
	else: return cs(text=in_str, font_color='white', bg_color='yellow', *args, **kwargs)

#<=====>#

def LGyoY(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_grey', bg_color='yellow', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_grey', bg_color='yellow', *args, **kwargs)

#<=====>#

def DGyoY(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='dark_grey', bg_color='yellow', *args, **kwargs)
	else: return cs(text=in_str, font_color='dark_grey', bg_color='yellow', *args, **kwargs)

#<=====>#

def LRoY(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_red', bg_color='yellow', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_red', bg_color='yellow', *args, **kwargs)

#<=====>#

def LGoY(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_green', bg_color='yellow', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_green', bg_color='yellow', *args, **kwargs)

#<=====>#

def LYoY(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_yellow', bg_color='yellow', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_yellow', bg_color='yellow', *args, **kwargs)

#<=====>#

def LBoY(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_blue', bg_color='yellow', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_blue', bg_color='yellow', *args, **kwargs)

#<=====>#

def LMoY(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_magenta', bg_color='yellow', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_magenta', bg_color='yellow', *args, **kwargs)

#<=====>#

def LCoY(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_cyan', bg_color='yellow', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_cyan', bg_color='yellow', *args, **kwargs)

#<=====>#

def KoB(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='black', bg_color='blue', *args, **kwargs)
	else: return cs(text=in_str, font_color='black', bg_color='blue', *args, **kwargs)

#<=====>#

def RoB(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='red', bg_color='blue', *args, **kwargs)
	else: return cs(text=in_str, font_color='red', bg_color='blue', *args, **kwargs)

#<=====>#

def GoB(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='green', bg_color='blue', *args, **kwargs)
	else: return cs(text=in_str, font_color='green', bg_color='blue', *args, **kwargs)

#<=====>#

def YoB(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='yellow', bg_color='blue', *args, **kwargs)
	else: return cs(text=in_str, font_color='yellow', bg_color='blue', *args, **kwargs)

#<=====>#

def BoB(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='blue', bg_color='blue', *args, **kwargs)
	else: return cs(text=in_str, font_color='blue', bg_color='blue', *args, **kwargs)

#<=====>#

def MoB(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='magenta', bg_color='blue', *args, **kwargs)
	else: return cs(text=in_str, font_color='magenta', bg_color='blue', *args, **kwargs)

#<=====>#

def CoB(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='cyan', bg_color='blue', *args, **kwargs)
	else: return cs(text=in_str, font_color='cyan', bg_color='blue', *args, **kwargs)

#<=====>#

def WoB(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='white', bg_color='blue', *args, **kwargs)
	else: return cs(text=in_str, font_color='white', bg_color='blue', *args, **kwargs)

#<=====>#

def LGyoB(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_grey', bg_color='blue', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_grey', bg_color='blue', *args, **kwargs)

#<=====>#

def DGyoB(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='dark_grey', bg_color='blue', *args, **kwargs)
	else: return cs(text=in_str, font_color='dark_grey', bg_color='blue', *args, **kwargs)

#<=====>#

def LRoB(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_red', bg_color='blue', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_red', bg_color='blue', *args, **kwargs)

#<=====>#

def LGoB(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_green', bg_color='blue', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_green', bg_color='blue', *args, **kwargs)

#<=====>#

def LYoB(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_yellow', bg_color='blue', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_yellow', bg_color='blue', *args, **kwargs)

#<=====>#

def LBoB(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_blue', bg_color='blue', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_blue', bg_color='blue', *args, **kwargs)

#<=====>#

def LMoB(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_magenta', bg_color='blue', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_magenta', bg_color='blue', *args, **kwargs)

#<=====>#

def LCoB(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_cyan', bg_color='blue', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_cyan', bg_color='blue', *args, **kwargs)

#<=====>#

def KoM(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='black', bg_color='magenta', *args, **kwargs)
	else: return cs(text=in_str, font_color='black', bg_color='magenta', *args, **kwargs)

#<=====>#

def RoM(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='red', bg_color='magenta', *args, **kwargs)
	else: return cs(text=in_str, font_color='red', bg_color='magenta', *args, **kwargs)

#<=====>#

def GoM(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='green', bg_color='magenta', *args, **kwargs)
	else: return cs(text=in_str, font_color='green', bg_color='magenta', *args, **kwargs)

#<=====>#

def YoM(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='yellow', bg_color='magenta', *args, **kwargs)
	else: return cs(text=in_str, font_color='yellow', bg_color='magenta', *args, **kwargs)

#<=====>#

def BoM(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='blue', bg_color='magenta', *args, **kwargs)
	else: return cs(text=in_str, font_color='blue', bg_color='magenta', *args, **kwargs)

#<=====>#

def MoM(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='magenta', bg_color='magenta', *args, **kwargs)
	else: return cs(text=in_str, font_color='magenta', bg_color='magenta', *args, **kwargs)

#<=====>#

def CoM(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='cyan', bg_color='magenta', *args, **kwargs)
	else: return cs(text=in_str, font_color='cyan', bg_color='magenta', *args, **kwargs)

#<=====>#

def WoM(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='white', bg_color='magenta', *args, **kwargs)
	else: return cs(text=in_str, font_color='white', bg_color='magenta', *args, **kwargs)

#<=====>#

def LGyoM(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_grey', bg_color='magenta', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_grey', bg_color='magenta', *args, **kwargs)

#<=====>#

def DGyoM(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='dark_grey', bg_color='magenta', *args, **kwargs)
	else: return cs(text=in_str, font_color='dark_grey', bg_color='magenta', *args, **kwargs)

#<=====>#

def LRoM(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_red', bg_color='magenta', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_red', bg_color='magenta', *args, **kwargs)

#<=====>#

def LGoM(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_green', bg_color='magenta', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_green', bg_color='magenta', *args, **kwargs)

#<=====>#

def LYoM(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_yellow', bg_color='magenta', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_yellow', bg_color='magenta', *args, **kwargs)

#<=====>#

def LBoM(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_blue', bg_color='magenta', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_blue', bg_color='magenta', *args, **kwargs)

#<=====>#

def LMoM(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_magenta', bg_color='magenta', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_magenta', bg_color='magenta', *args, **kwargs)

#<=====>#

def LCoM(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_cyan', bg_color='magenta', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_cyan', bg_color='magenta', *args, **kwargs)

#<=====>#

def KoC(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='black', bg_color='cyan', *args, **kwargs)
	else: return cs(text=in_str, font_color='black', bg_color='cyan', *args, **kwargs)

#<=====>#

def RoC(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='red', bg_color='cyan', *args, **kwargs)
	else: return cs(text=in_str, font_color='red', bg_color='cyan', *args, **kwargs)

#<=====>#

def GoC(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='green', bg_color='cyan', *args, **kwargs)
	else: return cs(text=in_str, font_color='green', bg_color='cyan', *args, **kwargs)

#<=====>#

def YoC(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='yellow', bg_color='cyan', *args, **kwargs)
	else: return cs(text=in_str, font_color='yellow', bg_color='cyan', *args, **kwargs)

#<=====>#

def BoC(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='blue', bg_color='cyan', *args, **kwargs)
	else: return cs(text=in_str, font_color='blue', bg_color='cyan', *args, **kwargs)

#<=====>#

def MoC(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='magenta', bg_color='cyan', *args, **kwargs)
	else: return cs(text=in_str, font_color='magenta', bg_color='cyan', *args, **kwargs)

#<=====>#

def CoC(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='cyan', bg_color='cyan', *args, **kwargs)
	else: return cs(text=in_str, font_color='cyan', bg_color='cyan', *args, **kwargs)

#<=====>#

def WoC(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='white', bg_color='cyan', *args, **kwargs)
	else: return cs(text=in_str, font_color='white', bg_color='cyan', *args, **kwargs)

#<=====>#

def LGyoC(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_grey', bg_color='cyan', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_grey', bg_color='cyan', *args, **kwargs)

#<=====>#

def DGyoC(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='dark_grey', bg_color='cyan', *args, **kwargs)
	else: return cs(text=in_str, font_color='dark_grey', bg_color='cyan', *args, **kwargs)

#<=====>#

def LRoC(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_red', bg_color='cyan', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_red', bg_color='cyan', *args, **kwargs)

#<=====>#

def LGoC(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_green', bg_color='cyan', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_green', bg_color='cyan', *args, **kwargs)

#<=====>#

def LYoC(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_yellow', bg_color='cyan', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_yellow', bg_color='cyan', *args, **kwargs)

#<=====>#

def LBoC(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_blue', bg_color='cyan', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_blue', bg_color='cyan', *args, **kwargs)

#<=====>#

def LMoC(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_magenta', bg_color='cyan', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_magenta', bg_color='cyan', *args, **kwargs)

#<=====>#

def LCoC(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_cyan', bg_color='cyan', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_cyan', bg_color='cyan', *args, **kwargs)

#<=====>#

def KoW(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='black', bg_color='white', *args, **kwargs)
	else: return cs(text=in_str, font_color='black', bg_color='white', *args, **kwargs)

#<=====>#

def RoW(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='red', bg_color='white', *args, **kwargs)
	else: return cs(text=in_str, font_color='red', bg_color='white', *args, **kwargs)

#<=====>#

def GoW(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='green', bg_color='white', *args, **kwargs)
	else: return cs(text=in_str, font_color='green', bg_color='white', *args, **kwargs)

#<=====>#

def YoW(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='yellow', bg_color='white', *args, **kwargs)
	else: return cs(text=in_str, font_color='yellow', bg_color='white', *args, **kwargs)

#<=====>#

def BoW(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='blue', bg_color='white', *args, **kwargs)
	else: return cs(text=in_str, font_color='blue', bg_color='white', *args, **kwargs)

#<=====>#

def MoW(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='magenta', bg_color='white', *args, **kwargs)
	else: return cs(text=in_str, font_color='magenta', bg_color='white', *args, **kwargs)

#<=====>#

def CoW(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='cyan', bg_color='white', *args, **kwargs)
	else: return cs(text=in_str, font_color='cyan', bg_color='white', *args, **kwargs)

#<=====>#

def WoW(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='white', bg_color='white', *args, **kwargs)
	else: return cs(text=in_str, font_color='white', bg_color='white', *args, **kwargs)

#<=====>#

def LGyoW(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_grey', bg_color='white', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_grey', bg_color='white', *args, **kwargs)

#<=====>#

def DGyoW(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='dark_grey', bg_color='white', *args, **kwargs)
	else: return cs(text=in_str, font_color='dark_grey', bg_color='white', *args, **kwargs)

#<=====>#

def LRoW(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_red', bg_color='white', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_red', bg_color='white', *args, **kwargs)

#<=====>#

def LGoW(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_green', bg_color='white', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_green', bg_color='white', *args, **kwargs)

#<=====>#

def LYoW(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_yellow', bg_color='white', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_yellow', bg_color='white', *args, **kwargs)

#<=====>#

def LBoW(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_blue', bg_color='white', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_blue', bg_color='white', *args, **kwargs)

#<=====>#

def LMoW(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_magenta', bg_color='white', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_magenta', bg_color='white', *args, **kwargs)

#<=====>#

def LCoW(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_cyan', bg_color='white', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_cyan', bg_color='white', *args, **kwargs)

#<=====>#

def KoLGy(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='black', bg_color='light_grey', *args, **kwargs)
	else: return cs(text=in_str, font_color='black', bg_color='light_grey', *args, **kwargs)

#<=====>#

def RoLGy(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='red', bg_color='light_grey', *args, **kwargs)
	else: return cs(text=in_str, font_color='red', bg_color='light_grey', *args, **kwargs)

#<=====>#

def GoLGy(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='green', bg_color='light_grey', *args, **kwargs)
	else: return cs(text=in_str, font_color='green', bg_color='light_grey', *args, **kwargs)

#<=====>#

def YoLGy(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='yellow', bg_color='light_grey', *args, **kwargs)
	else: return cs(text=in_str, font_color='yellow', bg_color='light_grey', *args, **kwargs)

#<=====>#

def BoLGy(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='blue', bg_color='light_grey', *args, **kwargs)
	else: return cs(text=in_str, font_color='blue', bg_color='light_grey', *args, **kwargs)

#<=====>#

def MoLGy(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='magenta', bg_color='light_grey', *args, **kwargs)
	else: return cs(text=in_str, font_color='magenta', bg_color='light_grey', *args, **kwargs)

#<=====>#

def CoLGy(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='cyan', bg_color='light_grey', *args, **kwargs)
	else: return cs(text=in_str, font_color='cyan', bg_color='light_grey', *args, **kwargs)

#<=====>#

def WoLGy(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='white', bg_color='light_grey', *args, **kwargs)
	else: return cs(text=in_str, font_color='white', bg_color='light_grey', *args, **kwargs)

#<=====>#

def LGyoLGy(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_grey', bg_color='light_grey', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_grey', bg_color='light_grey', *args, **kwargs)

#<=====>#

def DGyoLGy(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='dark_grey', bg_color='light_grey', *args, **kwargs)
	else: return cs(text=in_str, font_color='dark_grey', bg_color='light_grey', *args, **kwargs)

#<=====>#

def LRoLGy(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_red', bg_color='light_grey', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_red', bg_color='light_grey', *args, **kwargs)

#<=====>#

def LGoLGy(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_green', bg_color='light_grey', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_green', bg_color='light_grey', *args, **kwargs)

#<=====>#

def LYoLGy(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_yellow', bg_color='light_grey', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_yellow', bg_color='light_grey', *args, **kwargs)

#<=====>#

def LBoLGy(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_blue', bg_color='light_grey', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_blue', bg_color='light_grey', *args, **kwargs)

#<=====>#

def LMoLGy(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_magenta', bg_color='light_grey', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_magenta', bg_color='light_grey', *args, **kwargs)

#<=====>#

def LCoLGy(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_cyan', bg_color='light_grey', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_cyan', bg_color='light_grey', *args, **kwargs)

#<=====>#

def KoDGy(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='black', bg_color='dark_grey', *args, **kwargs)
	else: return cs(text=in_str, font_color='black', bg_color='dark_grey', *args, **kwargs)

#<=====>#

def RoDGy(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='red', bg_color='dark_grey', *args, **kwargs)
	else: return cs(text=in_str, font_color='red', bg_color='dark_grey', *args, **kwargs)

#<=====>#

def GoDGy(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='green', bg_color='dark_grey', *args, **kwargs)
	else: return cs(text=in_str, font_color='green', bg_color='dark_grey', *args, **kwargs)

#<=====>#

def YoDGy(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='yellow', bg_color='dark_grey', *args, **kwargs)
	else: return cs(text=in_str, font_color='yellow', bg_color='dark_grey', *args, **kwargs)

#<=====>#

def BoDGy(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='blue', bg_color='dark_grey', *args, **kwargs)
	else: return cs(text=in_str, font_color='blue', bg_color='dark_grey', *args, **kwargs)

#<=====>#

def MoDGy(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='magenta', bg_color='dark_grey', *args, **kwargs)
	else: return cs(text=in_str, font_color='magenta', bg_color='dark_grey', *args, **kwargs)

#<=====>#

def CoDGy(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='cyan', bg_color='dark_grey', *args, **kwargs)
	else: return cs(text=in_str, font_color='cyan', bg_color='dark_grey', *args, **kwargs)

#<=====>#

def WoDGy(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='white', bg_color='dark_grey', *args, **kwargs)
	else: return cs(text=in_str, font_color='white', bg_color='dark_grey', *args, **kwargs)

#<=====>#

def LGyoDGy(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_grey', bg_color='dark_grey', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_grey', bg_color='dark_grey', *args, **kwargs)

#<=====>#

def DGyoDGy(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='dark_grey', bg_color='dark_grey', *args, **kwargs)
	else: return cs(text=in_str, font_color='dark_grey', bg_color='dark_grey', *args, **kwargs)

#<=====>#

def LRoDGy(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_red', bg_color='dark_grey', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_red', bg_color='dark_grey', *args, **kwargs)

#<=====>#

def LGoDGy(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_green', bg_color='dark_grey', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_green', bg_color='dark_grey', *args, **kwargs)

#<=====>#

def LYoDGy(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_yellow', bg_color='dark_grey', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_yellow', bg_color='dark_grey', *args, **kwargs)

#<=====>#

def LBoDGy(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_blue', bg_color='dark_grey', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_blue', bg_color='dark_grey', *args, **kwargs)

#<=====>#

def LMoDGy(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_magenta', bg_color='dark_grey', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_magenta', bg_color='dark_grey', *args, **kwargs)

#<=====>#

def LCoDGy(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_cyan', bg_color='dark_grey', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_cyan', bg_color='dark_grey', *args, **kwargs)

#<=====>#

def KoLR(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='black', bg_color='light_red', *args, **kwargs)
	else: return cs(text=in_str, font_color='black', bg_color='light_red', *args, **kwargs)

#<=====>#

def RoLR(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='red', bg_color='light_red', *args, **kwargs)
	else: return cs(text=in_str, font_color='red', bg_color='light_red', *args, **kwargs)

#<=====>#

def GoLR(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='green', bg_color='light_red', *args, **kwargs)
	else: return cs(text=in_str, font_color='green', bg_color='light_red', *args, **kwargs)

#<=====>#

def YoLR(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='yellow', bg_color='light_red', *args, **kwargs)
	else: return cs(text=in_str, font_color='yellow', bg_color='light_red', *args, **kwargs)

#<=====>#

def BoLR(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='blue', bg_color='light_red', *args, **kwargs)
	else: return cs(text=in_str, font_color='blue', bg_color='light_red', *args, **kwargs)

#<=====>#

def MoLR(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='magenta', bg_color='light_red', *args, **kwargs)
	else: return cs(text=in_str, font_color='magenta', bg_color='light_red', *args, **kwargs)

#<=====>#

def CoLR(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='cyan', bg_color='light_red', *args, **kwargs)
	else: return cs(text=in_str, font_color='cyan', bg_color='light_red', *args, **kwargs)

#<=====>#

def WoLR(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='white', bg_color='light_red', *args, **kwargs)
	else: return cs(text=in_str, font_color='white', bg_color='light_red', *args, **kwargs)

#<=====>#

def LGyoLR(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_grey', bg_color='light_red', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_grey', bg_color='light_red', *args, **kwargs)

#<=====>#

def DGyoLR(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='dark_grey', bg_color='light_red', *args, **kwargs)
	else: return cs(text=in_str, font_color='dark_grey', bg_color='light_red', *args, **kwargs)

#<=====>#

def LRoLR(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_red', bg_color='light_red', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_red', bg_color='light_red', *args, **kwargs)

#<=====>#

def LGoLR(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_green', bg_color='light_red', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_green', bg_color='light_red', *args, **kwargs)

#<=====>#

def LYoLR(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_yellow', bg_color='light_red', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_yellow', bg_color='light_red', *args, **kwargs)

#<=====>#

def LBoLR(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_blue', bg_color='light_red', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_blue', bg_color='light_red', *args, **kwargs)

#<=====>#

def LMoLR(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_magenta', bg_color='light_red', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_magenta', bg_color='light_red', *args, **kwargs)

#<=====>#

def LCoLR(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_cyan', bg_color='light_red', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_cyan', bg_color='light_red', *args, **kwargs)

#<=====>#

def KoLG(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='black', bg_color='light_green', *args, **kwargs)
	else: return cs(text=in_str, font_color='black', bg_color='light_green', *args, **kwargs)

#<=====>#

def RoLG(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='red', bg_color='light_green', *args, **kwargs)
	else: return cs(text=in_str, font_color='red', bg_color='light_green', *args, **kwargs)

#<=====>#

def GoLG(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='green', bg_color='light_green', *args, **kwargs)
	else: return cs(text=in_str, font_color='green', bg_color='light_green', *args, **kwargs)

#<=====>#

def YoLG(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='yellow', bg_color='light_green', *args, **kwargs)
	else: return cs(text=in_str, font_color='yellow', bg_color='light_green', *args, **kwargs)

#<=====>#

def BoLG(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='blue', bg_color='light_green', *args, **kwargs)
	else: return cs(text=in_str, font_color='blue', bg_color='light_green', *args, **kwargs)

#<=====>#

def MoLG(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='magenta', bg_color='light_green', *args, **kwargs)
	else: return cs(text=in_str, font_color='magenta', bg_color='light_green', *args, **kwargs)

#<=====>#

def CoLG(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='cyan', bg_color='light_green', *args, **kwargs)
	else: return cs(text=in_str, font_color='cyan', bg_color='light_green', *args, **kwargs)

#<=====>#

def WoLG(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='white', bg_color='light_green', *args, **kwargs)
	else: return cs(text=in_str, font_color='white', bg_color='light_green', *args, **kwargs)

#<=====>#

def LGyoLG(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_grey', bg_color='light_green', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_grey', bg_color='light_green', *args, **kwargs)

#<=====>#

def DGyoLG(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='dark_grey', bg_color='light_green', *args, **kwargs)
	else: return cs(text=in_str, font_color='dark_grey', bg_color='light_green', *args, **kwargs)

#<=====>#

def LRoLG(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_red', bg_color='light_green', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_red', bg_color='light_green', *args, **kwargs)

#<=====>#

def LGoLG(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_green', bg_color='light_green', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_green', bg_color='light_green', *args, **kwargs)

#<=====>#

def LYoLG(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_yellow', bg_color='light_green', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_yellow', bg_color='light_green', *args, **kwargs)

#<=====>#

def LBoLG(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_blue', bg_color='light_green', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_blue', bg_color='light_green', *args, **kwargs)

#<=====>#

def LMoLG(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_magenta', bg_color='light_green', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_magenta', bg_color='light_green', *args, **kwargs)

#<=====>#

def LCoLG(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_cyan', bg_color='light_green', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_cyan', bg_color='light_green', *args, **kwargs)

#<=====>#

def KoLY(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='black', bg_color='light_yellow', *args, **kwargs)
	else: return cs(text=in_str, font_color='black', bg_color='light_yellow', *args, **kwargs)

#<=====>#

def RoLY(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='red', bg_color='light_yellow', *args, **kwargs)
	else: return cs(text=in_str, font_color='red', bg_color='light_yellow', *args, **kwargs)

#<=====>#

def GoLY(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='green', bg_color='light_yellow', *args, **kwargs)
	else: return cs(text=in_str, font_color='green', bg_color='light_yellow', *args, **kwargs)

#<=====>#

def YoLY(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='yellow', bg_color='light_yellow', *args, **kwargs)
	else: return cs(text=in_str, font_color='yellow', bg_color='light_yellow', *args, **kwargs)

#<=====>#

def BoLY(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='blue', bg_color='light_yellow', *args, **kwargs)
	else: return cs(text=in_str, font_color='blue', bg_color='light_yellow', *args, **kwargs)

#<=====>#

def MoLY(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='magenta', bg_color='light_yellow', *args, **kwargs)
	else: return cs(text=in_str, font_color='magenta', bg_color='light_yellow', *args, **kwargs)

#<=====>#

def CoLY(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='cyan', bg_color='light_yellow', *args, **kwargs)
	else: return cs(text=in_str, font_color='cyan', bg_color='light_yellow', *args, **kwargs)

#<=====>#

def WoLY(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='white', bg_color='light_yellow', *args, **kwargs)
	else: return cs(text=in_str, font_color='white', bg_color='light_yellow', *args, **kwargs)

#<=====>#

def LGyoLY(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_grey', bg_color='light_yellow', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_grey', bg_color='light_yellow', *args, **kwargs)

#<=====>#

def DGyoLY(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='dark_grey', bg_color='light_yellow', *args, **kwargs)
	else: return cs(text=in_str, font_color='dark_grey', bg_color='light_yellow', *args, **kwargs)

#<=====>#

def LRoLY(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_red', bg_color='light_yellow', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_red', bg_color='light_yellow', *args, **kwargs)

#<=====>#

def LGoLY(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_green', bg_color='light_yellow', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_green', bg_color='light_yellow', *args, **kwargs)

#<=====>#

def LYoLY(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_yellow', bg_color='light_yellow', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_yellow', bg_color='light_yellow', *args, **kwargs)

#<=====>#

def LBoLY(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_blue', bg_color='light_yellow', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_blue', bg_color='light_yellow', *args, **kwargs)

#<=====>#

def LMoLY(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_magenta', bg_color='light_yellow', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_magenta', bg_color='light_yellow', *args, **kwargs)

#<=====>#

def LCoLY(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_cyan', bg_color='light_yellow', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_cyan', bg_color='light_yellow', *args, **kwargs)

#<=====>#

def KoLB(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='black', bg_color='light_blue', *args, **kwargs)
	else: return cs(text=in_str, font_color='black', bg_color='light_blue', *args, **kwargs)

#<=====>#

def RoLB(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='red', bg_color='light_blue', *args, **kwargs)
	else: return cs(text=in_str, font_color='red', bg_color='light_blue', *args, **kwargs)

#<=====>#

def GoLB(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='green', bg_color='light_blue', *args, **kwargs)
	else: return cs(text=in_str, font_color='green', bg_color='light_blue', *args, **kwargs)

#<=====>#

def YoLB(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='yellow', bg_color='light_blue', *args, **kwargs)
	else: return cs(text=in_str, font_color='yellow', bg_color='light_blue', *args, **kwargs)

#<=====>#

def BoLB(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='blue', bg_color='light_blue', *args, **kwargs)
	else: return cs(text=in_str, font_color='blue', bg_color='light_blue', *args, **kwargs)

#<=====>#

def MoLB(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='magenta', bg_color='light_blue', *args, **kwargs)
	else: return cs(text=in_str, font_color='magenta', bg_color='light_blue', *args, **kwargs)

#<=====>#

def CoLB(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='cyan', bg_color='light_blue', *args, **kwargs)
	else: return cs(text=in_str, font_color='cyan', bg_color='light_blue', *args, **kwargs)

#<=====>#

def WoLB(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='white', bg_color='light_blue', *args, **kwargs)
	else: return cs(text=in_str, font_color='white', bg_color='light_blue', *args, **kwargs)

#<=====>#

def LGyoLB(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_grey', bg_color='light_blue', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_grey', bg_color='light_blue', *args, **kwargs)

#<=====>#

def DGyoLB(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='dark_grey', bg_color='light_blue', *args, **kwargs)
	else: return cs(text=in_str, font_color='dark_grey', bg_color='light_blue', *args, **kwargs)

#<=====>#

def LRoLB(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_red', bg_color='light_blue', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_red', bg_color='light_blue', *args, **kwargs)

#<=====>#

def LGoLB(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_green', bg_color='light_blue', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_green', bg_color='light_blue', *args, **kwargs)

#<=====>#

def LYoLB(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_yellow', bg_color='light_blue', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_yellow', bg_color='light_blue', *args, **kwargs)

#<=====>#

def LBoLB(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_blue', bg_color='light_blue', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_blue', bg_color='light_blue', *args, **kwargs)

#<=====>#

def LMoLB(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_magenta', bg_color='light_blue', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_magenta', bg_color='light_blue', *args, **kwargs)

#<=====>#

def LCoLB(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_cyan', bg_color='light_blue', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_cyan', bg_color='light_blue', *args, **kwargs)

#<=====>#

def KoLM(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='black', bg_color='light_magenta', *args, **kwargs)
	else: return cs(text=in_str, font_color='black', bg_color='light_magenta', *args, **kwargs)

#<=====>#

def RoLM(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='red', bg_color='light_magenta', *args, **kwargs)
	else: return cs(text=in_str, font_color='red', bg_color='light_magenta', *args, **kwargs)

#<=====>#

def GoLM(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='green', bg_color='light_magenta', *args, **kwargs)
	else: return cs(text=in_str, font_color='green', bg_color='light_magenta', *args, **kwargs)

#<=====>#

def YoLM(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='yellow', bg_color='light_magenta', *args, **kwargs)
	else: return cs(text=in_str, font_color='yellow', bg_color='light_magenta', *args, **kwargs)

#<=====>#

def BoLM(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='blue', bg_color='light_magenta', *args, **kwargs)
	else: return cs(text=in_str, font_color='blue', bg_color='light_magenta', *args, **kwargs)

#<=====>#

def MoLM(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='magenta', bg_color='light_magenta', *args, **kwargs)
	else: return cs(text=in_str, font_color='magenta', bg_color='light_magenta', *args, **kwargs)

#<=====>#

def CoLM(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='cyan', bg_color='light_magenta', *args, **kwargs)
	else: return cs(text=in_str, font_color='cyan', bg_color='light_magenta', *args, **kwargs)

#<=====>#

def WoLM(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='white', bg_color='light_magenta', *args, **kwargs)
	else: return cs(text=in_str, font_color='white', bg_color='light_magenta', *args, **kwargs)

#<=====>#

def LGyoLM(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_grey', bg_color='light_magenta', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_grey', bg_color='light_magenta', *args, **kwargs)

#<=====>#

def DGyoLM(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='dark_grey', bg_color='light_magenta', *args, **kwargs)
	else: return cs(text=in_str, font_color='dark_grey', bg_color='light_magenta', *args, **kwargs)

#<=====>#

def LRoLM(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_red', bg_color='light_magenta', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_red', bg_color='light_magenta', *args, **kwargs)

#<=====>#

def LGoLM(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_green', bg_color='light_magenta', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_green', bg_color='light_magenta', *args, **kwargs)

#<=====>#

def LYoLM(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_yellow', bg_color='light_magenta', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_yellow', bg_color='light_magenta', *args, **kwargs)

#<=====>#

def LBoLM(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_blue', bg_color='light_magenta', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_blue', bg_color='light_magenta', *args, **kwargs)

#<=====>#

def LMoLM(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_magenta', bg_color='light_magenta', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_magenta', bg_color='light_magenta', *args, **kwargs)

#<=====>#

def LCoLM(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_cyan', bg_color='light_magenta', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_cyan', bg_color='light_magenta', *args, **kwargs)

#<=====>#

def KoLC(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='black', bg_color='light_cyan', *args, **kwargs)
	else: return cs(text=in_str, font_color='black', bg_color='light_cyan', *args, **kwargs)

#<=====>#

def RoLC(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='red', bg_color='light_cyan', *args, **kwargs)
	else: return cs(text=in_str, font_color='red', bg_color='light_cyan', *args, **kwargs)

#<=====>#

def GoLC(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='green', bg_color='light_cyan', *args, **kwargs)
	else: return cs(text=in_str, font_color='green', bg_color='light_cyan', *args, **kwargs)

#<=====>#

def YoLC(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='yellow', bg_color='light_cyan', *args, **kwargs)
	else: return cs(text=in_str, font_color='yellow', bg_color='light_cyan', *args, **kwargs)

#<=====>#

def BoLC(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='blue', bg_color='light_cyan', *args, **kwargs)
	else: return cs(text=in_str, font_color='blue', bg_color='light_cyan', *args, **kwargs)

#<=====>#

def MoLC(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='magenta', bg_color='light_cyan', *args, **kwargs)
	else: return cs(text=in_str, font_color='magenta', bg_color='light_cyan', *args, **kwargs)

#<=====>#

def CoLC(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='cyan', bg_color='light_cyan', *args, **kwargs)
	else: return cs(text=in_str, font_color='cyan', bg_color='light_cyan', *args, **kwargs)

#<=====>#

def WoLC(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='white', bg_color='light_cyan', *args, **kwargs)
	else: return cs(text=in_str, font_color='white', bg_color='light_cyan', *args, **kwargs)

#<=====>#

def LGyoLC(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_grey', bg_color='light_cyan', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_grey', bg_color='light_cyan', *args, **kwargs)

#<=====>#

def DGyoLC(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='dark_grey', bg_color='light_cyan', *args, **kwargs)
	else: return cs(text=in_str, font_color='dark_grey', bg_color='light_cyan', *args, **kwargs)

#<=====>#

def LRoLC(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_red', bg_color='light_cyan', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_red', bg_color='light_cyan', *args, **kwargs)

#<=====>#

def LGoLC(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_green', bg_color='light_cyan', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_green', bg_color='light_cyan', *args, **kwargs)

#<=====>#

def LYoLC(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_yellow', bg_color='light_cyan', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_yellow', bg_color='light_cyan', *args, **kwargs)

#<=====>#

def LBoLC(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_blue', bg_color='light_cyan', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_blue', bg_color='light_cyan', *args, **kwargs)

#<=====>#

def LMoLC(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_magenta', bg_color='light_cyan', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_magenta', bg_color='light_cyan', *args, **kwargs)

#<=====>#

def LCoLC(in_str, print_tf=True, *args, **kwargs):
	if print_tf: cp(in_str, font_color='light_cyan', bg_color='light_cyan', *args, **kwargs)
	else: return cs(text=in_str, font_color='light_cyan', bg_color='light_cyan', *args, **kwargs)

#<=====>#

def cs(text, font_color, bg_color='black', bold=False, italic=False, length=0, align='left'):
	r = c.color_string(text, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic, length=length, align=align)
	return r

#<=====>#

def cp(text, font_color, bg_color='black', bold=False, italic=False, length=0, align='left'):
	c.color_print(text, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic, length=length, align=align)

#<=====>#
# Assignments Post
#<=====>#

c = CLR()

#<=====>#
# Default Run
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

