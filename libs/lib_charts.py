#<=====>#
# Import All Scope
#<=====>#

import_all_func_list =  []
import_all_func_list.append("chart_top")
import_all_func_list.append("chart_title")
import_all_func_list.append("chart_headers")
import_all_func_list.append("chart_row")
import_all_func_list.append("chart_mid")
import_all_func_list.append("chart_bottom")
__all__ = import_all_func_list

#<=====>#
# Description
#<=====>#


#<=====>#
# Known To Do List
#<=====>#


#<=====>#
# Imports - Common Modules
#<=====>#
import sys
import os
import re

#<=====>#
# Imports - Download Modules
#<=====>#


#<=====>#
# Imports - Shared Library
#<=====>#
# shared_libs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'SHARED_LIBS'))
# if shared_libs_path not in sys.path:
# 	sys.path.append(shared_libs_path)


#<=====>#
# Imports - Local Library
#<=====>#
local_libs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '', 'libs'))
if local_libs_path not in sys.path:
	sys.path.append(local_libs_path)

#from lib_common                    import *
#from lib_common                    import lpad, rpad, cpad
from lib_colors                    import cs, cp

#<=====>#
# Variables
#<=====>#
lib_name      = 'lib_charts'
log_name      = 'lib_charts'
lib_verbosity = 1
lib_debug_lvl = 1
lib_secs_max  = 0.33
lib_secs_max  = 10

#<=====>#
# Assignments Pre
#<=====>#


#<=====>#
# Classes
#<=====>#


#<=====>#
# Functions
#<=====>#

#	pallette = {}
#	
#	# Reds
#	pallette["indianred"]             = "#CD5C5C"      # indianred                             #CD5C5C  205   92   92  389
#	pallette["lightcoral"]            = "#F08080"      # lightcoral                            #F08080  240  128  128  496
#	pallette["salmon"]                = "#FA8072"      # salmon                                #FA8072  250  128  114  492
#	pallette["darksalmon"]            = "#E9967A"      # darksalmon                            #E9967A  233  150  122  505
#	pallette["lightsalmon"]           = "#FFA07A"      # lightsalmon                           #FFA07A  255  160  122  537
#	pallette["crimson"]               = "#DC143C"      # crimson                               #DC143C  220   20   60  300
#	pallette["red"]                   = "#FF0000"      # red                                   #FF0000  255    0    0  255
#	pallette["firebrick"]             = "#B22222"      # firebrick                             #B22222  178   34   34  246
#	pallette["darkred"]               = "#8B0000"      # darkred                               #8B0000  139    0    0  139
#	
#	# Pinks
#	pallette["pink"]                  = "#FFC0CB"      # pink                                  #FFC0CB  255  192  203  650
#	pallette["lightpink"]             = "#FFB6C1"      # lightpink                             #FFB6C1  255  182  193  630
#	pallette["hotpink"]               = "#FF69B4"      # hotpink                               #FF69B4  255  105  180  540
#	pallette["deeppink"]              = "#FF1493"      # deeppink                              #FF1493  255   20  147  422
#	pallette["mediumvioletred"]       = "#C71585"      # mediumvioletred                       #C71585  199   21  133  353
#	pallette["palevioletred"]         = "#DB7093"      # palevioletred                         #DB7093  219  112  147  478
#	
#	# Oranges
#	pallette["lightsalmon"]           = "#FFA07A"      # lightsalmon                           #FFA07A  255  160  122  537
#	pallette["coral"]                 = "#FF7F50"      # coral                                 #FF7F50  255  127   80  462
#	pallette["tomato"]                = "#FF6347"      # tomato                                #FF6347  255   99   71  425
#	pallette["orangered"]             = "#FF4500"      # orangered                             #FF4500  255   69    0  324
#	pallette["darkorange"]            = "#FF8C00"      # darkorange                            #FF8C00  255  140    0  395
#	pallette["orange"]                = "#FFA500"      # orange                                #FFA500  255  165    0  420
#	
#	# Yellows
#	pallette["gold"]                  = "#FFD700"      # gold                                  #FFD700  255  215    0  470
#	pallette["yellow"]                = "#FFFF00"      # yellow                                #FFFF00  255  255    0  510
#	pallette["lightyellow"]           = "#FFFFE0"      # lightyellow                           #FFFFE0  255  255  224  734
#	pallette["lemonchiffon"]          = "#FFFACD"      # lemonchiffon                          #FFFACD  255  250  205  710
#	pallette["lightgoldenrodyellow"]  = "#FAFAD2"      # lightgoldenrodyellow                  #FAFAD2  250  250  210  710
#	pallette["papayawhip"]            = "#FFEFD5"      # papayawhip                            #FFEFD5  255  239  213  707
#	pallette["moccasin"]              = "#FFE4B5"      # moccasin                              #FFE4B5  255  228  181  664
#	pallette["peachpuff"]             = "#FFDAB9"      # peachpuff                             #FFDAB9  255  218  185  658
#	pallette["palegoldenrod"]         = "#EEE8AA"      # palegoldenrod                         #EEE8AA  238  232  170  640
#	pallette["darkkhaki"]             = "#BDB76B"      # darkkhaki                             #BDB76B  189  183  107  479
#	pallette["khaki"]                 = "#F0E68C"      # khaki                                 #F0E68C  240  230  140  610
#	
#	# Purples
#	pallette["lavender"]              = "#E6E6FA"      # lavender                              #E6E6FA  230  230  250  710
#	pallette["thistle"]               = "#D8BFD8"      # thistle                               #D8BFD8  216  191  216  623
#	pallette["plum"]                  = "#DDA0DD"      # plum                                  #DDA0DD  221  160  221  602
#	pallette["violet"]                = "#EE82EE"      # violet                                #EE82EE  238  130  238  606
#	pallette["orchid"]                = "#DA70D6"      # orchid                                #DA70D6  218  112  214  544
#	pallette["fuchsia"]               = "#FF00FF"      # fuchsia                               #FF00FF  255    0  255  510
#	pallette["magenta"]               = "#FF00FF"      # magenta                               #FF00FF  255    0  255  510
#	pallette["mediumorchid"]          = "#BA55D3"      # mediumorchid                          #BA55D3  186   85  211  482
#	pallette["mediumpurple"]          = "#9370DB"      # mediumpurple                          #9370DB  147  112  219  478
#	pallette["rebeccapurple"]         = "#663399"      # rebeccapurple                         #663399  102   51  153  306
#	pallette["blueviolet"]            = "#8A2BE2"      # blueviolet                            #8A2BE2  138   43  226  407
#	pallette["darkviolet"]            = "#9400D3"      # darkviolet                            #9400D3  148    0  211  359
#	pallette["darkorchid"]            = "#9932CC"      # darkorchid                            #9932CC  153   50  204  407
#	pallette["darkmagenta"]           = "#8B008B"      # darkmagenta                           #8B008B  139    0  139  278
#	pallette["purple"]                = "#800080"      # purple                                #800080  128    0  128  256
#	pallette["indigo"]                = "#4B0082"      # indigo                                #4B0082   75    0  130  205
#	pallette["slateblue"]             = "#6A5ACD"      # slateblue                             #6A5ACD  106   90  205  401
#	pallette["darkslateblue"]         = "#483D8B"      # darkslateblue                         #483D8B   72   61  139  272
#	pallette["mediumslateblue"]       = "#7B68EE"      # mediumslateblue                       #7B68EE  123  104  238  465
#	
#	# Greens
#	pallette["greenyellow"]           = "#ADFF2F"      # greenyellow                           #ADFF2F  173  255   47  475
#	pallette["chartreuse"]            = "#7FFF00"      # chartreuse                            #7FFF00  127  255    0  382
#	pallette["lawngreen"]             = "#7CFC00"      # lawngreen                             #7CFC00  124  252    0  376
#	pallette["lime"]                  = "#00FF00"      # lime                                  #00FF00    0  255    0  255
#	pallette["limegreen"]             = "#32CD32"      # limegreen                             #32CD32   50  205   50  305
#	pallette["palegreen"]             = "#98FB98"      # palegreen                             #98FB98  152  251  152  555
#	pallette["lightgreen"]            = "#90EE90"      # lightgreen                            #90EE90  144  238  144  526
#	pallette["mediumspringgreen"]     = "#00FA9A"      # mediumspringgreen                     #00FA9A    0  250  154  404
#	pallette["springgreen"]           = "#00FF7F"      # springgreen                           #00FF7F    0  255  127  382
#	pallette["mediumseagreen"]        = "#3CB371"      # mediumseagreen                        #3CB371   60  179  113  352
#	pallette["seagreen"]              = "#2E8B57"      # seagreen                              #2E8B57   46  139   87  272
#	pallette["forestgreen"]           = "#228B22"      # forestgreen                           #228B22   34  139   34  207
#	pallette["green"]                 = "#008000"      # green                                 #008000    0  128    0  128
#	pallette["darkgreen"]             = "#006400"      # darkgreen                             #006400    0  100    0  100
#	pallette["yellowgreen"]           = "#9ACD32"      # yellowgreen                           #9ACD32  154  205   50  409
#	pallette["olivedrab"]             = "#6B8E23"      # olivedrab                             #6B8E23  107  142   35  284
#	pallette["olive"]                 = "#808000"      # olive                                 #808000  128  128    0  256
#	pallette["darkolivegreen"]        = "#556B2F"      # darkolivegreen                        #556B2F   85  107   47  239
#	pallette["mediumaquamarine"]      = "#66CDAA"      # mediumaquamarine                      #66CDAA  102  205  170  477
#	pallette["darkseagreen"]          = "#8FBC8F"      # darkseagreen                          #8FBC8F  143  188  143  474
#	pallette["lightseagreen"]         = "#20B2AA"      # lightseagreen                         #20B2AA   32  178  170  380
#	pallette["darkcyan"]              = "#008B8B"      # darkcyan                              #008B8B    0  139  139  278
#	pallette["teal"]                  = "#008080"      # teal                                  #008080    0  128  128  256
#	
#	# Blues
#	pallette["aqua"]                  = "#00FFFF"      # aqua                                  #00FFFF    0  255  255  510
#	pallette["cyan"]                  = "#00FFFF"      # cyan                                  #00FFFF    0  255  255  510
#	pallette["lightcyan"]             = "#E0FFFF"      # lightcyan                             #E0FFFF  224  255  255  734
#	pallette["paleturquoise"]         = "#AFEEEE"      # paleturquoise                         #AFEEEE  175  238  238  651
#	pallette["aquamarine"]            = "#7FFFD4"      # aquamarine                            #7FFFD4  127  255  212  594
#	pallette["turquoise"]             = "#40E0D0"      # turquoise                             #40E0D0   64  224  208  496
#	pallette["mediumturquoise"]       = "#48D1CC"      # mediumturquoise                       #48D1CC   72  209  204  485
#	pallette["darkturquoise"]         = "#00CED1"      # darkturquoise                         #00CED1    0  206  209  415
#	pallette["cadetblue"]             = "#5F9EA0"      # cadetblue                             #5F9EA0   95  158  160  413
#	pallette["steelblue"]             = "#4682B4"      # steelblue                             #4682B4   70  130  180  380
#	pallette["lightsteelblue"]        = "#B0C4DE"      # lightsteelblue                        #B0C4DE  176  196  222  594
#	pallette["powderblue"]            = "#B0E0E6"      # powderblue                            #B0E0E6  176  224  230  630
#	pallette["lightblue"]             = "#ADD8E6"      # lightblue                             #ADD8E6  173  216  230  619
#	pallette["skyblue"]               = "#87CEEB"      # skyblue                               #87CEEB  135  206  235  576
#	pallette["lightskyblue"]          = "#87CEFA"      # lightskyblue                          #87CEFA  135  206  250  591
#	pallette["deepskyblue"]           = "#00BFFF"      # deepskyblue                           #00BFFF    0  191  255  446
#	pallette["dodgerblue"]            = "#1E90FF"      # dodgerblue                            #1E90FF   30  144  255  429
#	pallette["cornflowerblue"]        = "#6495ED"      # cornflowerblue                        #6495ED  100  149  237  486
#	pallette["mediumslateblue"]       = "#7B68EE"      # mediumslateblue                       #7B68EE  123  104  238  465
#	pallette["royalblue"]             = "#4169E1"      # royalblue                             #4169E1   65  105  225  395
#	pallette["blue"]                  = "#0000FF"      # blue                                  #0000FF    0    0  255  255
#	pallette["mediumblue"]            = "#0000CD"      # mediumblue                            #0000CD    0    0  205  205
#	pallette["darkblue"]              = "#00008B"      # darkblue                              #00008B    0    0  139  139
#	pallette["navy"]                  = "#000080"      # navy                                  #000080    0    0  128  128
#	pallette["midnightblue"]          = "#191970"      # midnightblue                          #191970   25   25  112  162
#	
#	# Browns
#	pallette["cornsilk"]              = "#FFF8DC"      # cornsilk                              #FFF8DC  255  248  220  723
#	pallette["blanchedalmond"]        = "#FFEBCD"      # blanchedalmond                        #FFEBCD  255  235  205  695
#	pallette["bisque"]                = "#FFE4C4"      # bisque                                #FFE4C4  255  228  196  679
#	pallette["navajowhite"]           = "#FFDEAD"      # navajowhite                           #FFDEAD  255  222  173  650
#	pallette["wheat"]                 = "#F5DEB3"      # wheat                                 #F5DEB3  245  222  179  646
#	pallette["burlywood"]             = "#DEB887"      # burlywood                             #DEB887  222  184  135  541
#	pallette["tan"]                   = "#D2B48C"      # tan                                   #D2B48C  210  180  140  530
#	pallette["rosybrown"]             = "#BC8F8F"      # rosybrown                             #BC8F8F  188  143  143  474
#	pallette["sandybrown"]            = "#F4A460"      # sandybrown                            #F4A460  244  164   96  504
#	pallette["goldenrod"]             = "#DAA520"      # goldenrod                             #DAA520  218  165   32  415
#	pallette["darkgoldenrod"]         = "#B8860B"      # darkgoldenrod                         #B8860B  184  134   11  329
#	pallette["peru"]                  = "#CD853F"      # peru                                  #CD853F  205  133   63  401
#	pallette["chocolate"]             = "#D2691E"      # chocolate                             #D2691E  210  105   30  345
#	pallette["saddlebrown"]           = "#8B4513"      # saddlebrown                           #8B4513  139   69   19  227
#	pallette["sienna"]                = "#A0522D"      # sienna                                #A0522D  160   82   45  287
#	pallette["brown"]                 = "#A52A2A"      # brown                                 #A52A2A  165   42   42  249
#	pallette["maroon"]                = "#800000"      # maroon                                #800000  128    0    0  128
#	
#	# Whites
#	pallette["white"]                 = "#FFFFFF"      # white                                 #FFFFFF  255  255  255  765
#	pallette["snow"]                  = "#FFFAFA"      # snow                                  #FFFAFA  255  250  250  755
#	pallette["honeydew"]              = "#F0FFF0"      # honeydew                              #F0FFF0  240  255  240  735
#	pallette["mintcream"]             = "#F5FFFA"      # mintcream                             #F5FFFA  245  255  250  750
#	pallette["azure"]                 = "#F0FFFF"      # azure                                 #F0FFFF  240  255  255  750
#	pallette["aliceblue"]             = "#F0F8FF"      # aliceblue                             #F0F8FF  240  248  255  743
#	pallette["ghostwhite"]            = "#F8F8FF"      # ghostwhite                            #F8F8FF  248  248  255  751
#	pallette["whitesmoke"]            = "#F5F5F5"      # whitesmoke                            #F5F5F5  245  245  245  735
#	pallette["seashell"]              = "#FFF5EE"      # seashell                              #FFF5EE  255  245  238  738
#	pallette["beige"]                 = "#F5F5DC"      # beige                                 #F5F5DC  245  245  220  710
#	pallette["oldlace"]               = "#FDF5E6"      # oldlace                               #FDF5E6  253  245  230  728
#	pallette["floralwhite"]           = "#FFFAF0"      # floralwhite                           #FFFAF0  255  250  240  745
#	pallette["ivory"]                 = "#FFFFF0"      # ivory                                 #FFFFF0  255  255  240  750
#	pallette["antiquewhite"]          = "#FAEBD7"      # antiquewhite                          #FAEBD7  250  235  215  700
#	pallette["linen"]                 = "#FAF0E6"      # linen                                 #FAF0E6  250  240  230  720
#	pallette["lavenderblush"]         = "#FFF0F5"      # lavenderblush                         #FFF0F5  255  240  245  740
#	pallette["mistyrose"]             = "#FFE4E1"      # mistyrose                             #FFE4E1  255  228  225  708
#	
#	# Grays
#	pallette["gainsboro"]             = "#DCDCDC"      # gainsboro                             #DCDCDC  220  220  220  660
#	pallette["lightgray"]             = "#D3D3D3"      # lightgray                             #D3D3D3  211  211  211  633
#	#pallette["lightgrey"]             = "#D3D3D3"      # lightgrey                             #D3D3D3  211  211  211  633
#	pallette["silver"]                = "#C0C0C0"      # silver                                #C0C0C0  192  192  192  576
#	pallette["darkgray"]              = "#A9A9A9"      # darkgray                              #A9A9A9  169  169  169  507
#	#pallette["darkgrey"]              = "#A9A9A9"      # darkgrey                              #A9A9A9  169  169  169  507
#	pallette["gray"]                  = "#808080"      # gray                                  #808080  128  128  128  384
#	#pallette["grey"]                  = "#808080"      # grey                                  #808080  128  128  128  384
#	pallette["dimgray"]               = "#696969"      # dimgray                               #696969  105  105  105  315
#	#pallette["dimgrey"]               = "#696969"      # dimgrey                               #696969  105  105  105  315
#	pallette["lightslategray"]        = "#778899"      # lightslategray                        #778899  119  136  153  408
#	#pallette["lightslategrey"]        = "#778899"      # lightslategrey                        #778899  119  136  153  408
#	pallette["slategray"]             = "#708090"      # slategray                             #708090  112  128  144  384
#	#pallette["slategrey"]             = "#708090"      # slategrey                             #708090  112  128  144  384
#	pallette["darkslategray"]         = "#2F4F4F"      # darkslategray                         #2F4F4F   47   79   79  205
#	#pallette["darkslategrey"]         = "#2F4F4F"      # darkslategrey                         #2F4F4F   47   79   79  205
#	pallette["black"]                 = "#000000"      # black                                 #000000    0    0    0    0

#<=====>#

def chart_top(in_str='', len_cnt=250, align='left', font_color='white', bg_color='darkblue', border_font_color='lightblue', border_bg_color='darkblue', style=2, formatted=False):
	l, s, r = chart_shapes(part='top', style=style)
	disp_str = chart_embed(l, s, r, align, font_color, bg_color, border_font_color, border_bg_color, len_cnt, formatted, in_str=in_str)

#<=====>#

def chart_title(in_str='', len_cnt=250, align='left', font_color='white', bg_color='darkblue', border_font_color='lightblue', border_bg_color='darkblue', style=2, formatted=False):
	l, s, r = chart_shapes(part='row', style=style)
	disp_str = chart_embed(l, s, r, align, font_color, bg_color, border_font_color, border_bg_color, len_cnt, formatted, in_str=in_str)

#<=====>#

def chart_headers(in_str='', len_cnt=250, align='left', font_color='white', bg_color='blue', border_font_color='lightblue', border_bg_color='darkblue', style=2, formatted=False):
	l, s, r = chart_shapes(part='row', style=style)
	disp_str = chart_string(l, s, r, align, font_color, bg_color, border_font_color, border_bg_color, len_cnt, formatted, in_str=in_str)

#<=====>#

def chart_mid(in_str='', len_cnt=250, align='left', font_color='white', bg_color='darkblue', border_font_color='lightblue', border_bg_color='darkblue', style=2, formatted=False):
	l, s, r = chart_shapes(part='mid', style=style)
	disp_str = chart_embed(l, s, r, align, font_color, bg_color, border_font_color, border_bg_color, len_cnt, formatted, in_str=in_str)

#<=====>#

def chart_row(in_str='', len_cnt=250, align='left', font_color='white', bg_color='black', border_font_color='lightblue', border_bg_color='darkblue', style=2, formatted=False):
	l, s, r = chart_shapes(part='row', style=style)
	disp_str = chart_string(l, s, r, align, font_color, bg_color, border_font_color, border_bg_color, len_cnt, formatted, in_str=in_str)

#<=====>#

def chart_bottom(in_str='', len_cnt=250, align='left', font_color='white', bg_color='darkblue', border_font_color='lightblue', border_bg_color='darkblue', style=2, formatted=False):
	l, s, r = chart_shapes(part='bottom', style=style)
	disp_str = chart_embed(l, s, r, align, font_color, bg_color, border_font_color, border_bg_color, len_cnt, formatted, in_str=in_str)

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

def chart_embed(l, s, r, align, font_color, bg_color, border_font_color, border_bg_color, len_cnt, formatted, in_str=''):
	func_name = 'chart_embed'

	fore = cs(l, font_color=border_font_color, bg_color=border_bg_color)
	aft  = cs(r, font_color=border_font_color, bg_color=border_bg_color)

	if in_str == '':
		in_str = s * len_cnt
		disp_str = cs(text=in_str, font_color=border_font_color, bg_color=border_bg_color)
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
		front_str = cs(text=front_str, font_color=border_font_color, bg_color=border_bg_color)
		rear_str  = cs(text=rear_str,  font_color=border_font_color, bg_color=border_bg_color)
		disp_str  = cs(text=in_str, font_color=font_color, bg_color=bg_color)

		disp_str = f"{fore}{front_str}{disp_str}{rear_str}{aft}"

	print(disp_str) 

#<=====>#

def chart_string(l, s, r, align, font_color, bg_color, border_font_color, border_bg_color, len_cnt, formatted, in_str=''):
	func_name = 'chart_embed'

	fore = cs(l, font_color=border_font_color, bg_color=border_bg_color)
	aft  = cs(r, font_color=border_font_color, bg_color=border_bg_color)

	if in_str == '':
		in_str = s * len_cnt
		disp_str = cs(text=in_str, font_color=border_font_color, bg_color=border_bg_color)
		disp_str = f"{fore}{disp_str}{aft}"
	else:
		if align == 'left':
#			in_str = rpad(in_str, len_cnt, s)
			true_len = display_length(in_str)
			in_str = in_str + ' ' * (len_cnt - true_len)
		if align == 'right':
#			in_str = lpad(in_str, len_cnt, s)
			true_len = display_length(in_str)
			in_str = ' ' * (len_cnt - true_len) + in_str
		if align == 'center':
#			in_str = cpad(in_str, len_cnt, s)
			true_len = display_length(in_str)
			needed_pad_len = len_cnt - true_len
			lead_pad_len = int(needed_pad_len / 2)
			rear_pad_len = int(needed_pad_len / 2)
			if lead_pad_len + rear_pad_len > needed_pad_len:
				rear_pad_len -= 1
			in_str = ' ' * lead_pad_len + in_str + ' ' * rear_pad_len

		if not formatted:
			disp_str  = cs(text=in_str, font_color=font_color, bg_color=bg_color)

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
	chart_row(in_str=msg_3_01, align='left',   font_color='white', bg_color='green',    border_font_color='yellow', border_bg_color='darkblue', style=2)
	chart_row(in_str=msg_3_02)
	chart_row(in_str=msg_3_03)
	chart_row(in_str=msg_3_04, align='left',   font_color='white', bg_color='orangered',    border_font_color='yellow', border_bg_color='darkblue', style=2)
	chart_row(in_str=msg_3_05)
	chart_row(in_str=msg_3_06)
	chart_row(in_str=msg_3_07)
	chart_row(in_str=msg_3_08, align='left',   font_color='white', bg_color='lightgreen', border_font_color='yellow', border_bg_color='darkblue', style=2)
	chart_row(in_str=msg_3_09)
	chart_row(in_str=msg_3_10)
	chart_row(in_str=msg_3_11)
	chart_row(in_str=msg_3_12)
	chart_row(in_str=msg_3_13)
	chart_row(in_str=msg_3_14)
	chart_row(in_str=msg_3_15)
	chart_row(in_str=msg_3_16, align='left',   font_color='white', bg_color='red',      border_font_color='yellow', border_bg_color='darkblue', style=2)

	chart_mid()

	chart_title(in_str=msg_t4)
	chart_headers(in_str=msg_h4)
	chart_row(in_str=msg_4_01)
	chart_row(in_str=msg_4_02)

	chart_bottom()
	chart_bottom(in_str='bottom')

#<=====>#
