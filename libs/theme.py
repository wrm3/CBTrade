#<=====>#
# Description
#<=====>#



#<=====>#
# Known To Do List
#<=====>#



#<=====>#
# Imports - Public
#<=====>#
from fstrent_charts import *
from fstrent_colors import *

#<=====>#
# Import - Project
#<=====>#
from libs.common import AttrDict, AttrDictConv, narc
from libs.settings_base import Settings

#<=====>#
# Variables
#<=====>#
lib_name      = 'theme'
log_name      = 'theme'

# <=====>#
# Assignments Pre
# <=====>#

theme_json = {
    "chart": {
        "in_str":"",
        "len_cnt": 260,
        "align":"left",
        "bold":True,
        "italic":False,
        "header_font_color":"white",
        "header_bg_color":"blue",
        "font_color":"#00FF00",
        "bg_color":"#4B0082",
        "border_font_color":"#00FF00",
        "border_bg_color":"#4B0082",
        "style":2,
        "formatted":False
    },
    "chart_top": {
        "in_str": "",
        "len_cnt": 260,
        "align": "left",
        "bold": True,
        "italic": False,
        "header_font_color": "white",
        "header_bg_color": "blue",
        "font_color": "#00FF00",
        "bg_color": "#4B0082",
        "border_font_color": "#00FF00",
        "border_bg_color": "#4B0082",
        "style": 2,
        "formatted": False
    },
    "chart_title": {
        "in_str": "",
        "len_cnt": 260,
        "align": "left",
        "bold": True,
        "italic": False,
        "header_font_color": "white",
        "header_bg_color": "blue",
        "font_color": "#00FF00",
        "bg_color": "#4B0082",
        "border_font_color": "#00FF00",
        "border_bg_color": "#4B0082",
        "style": 2,
        "formatted": False
    },
    "chart_headers": {
        "in_str": "",
        "len_cnt": 260,
        "align": "left",
        "bold": True,
        "italic": False,
        "header_font_color": "white",
        "header_bg_color": "blue",
        "font_color": "gold",
        "bg_color": "blue",
        "border_font_color": "#00FF00",
        "border_bg_color": "#4B0082",
        "style": 2,
        "formatted": False
    },
    "chart_mid": {
        "in_str": "",
        "len_cnt": 260,
        "align": "left",
        "bold": True,
        "italic": False,
        "header_font_color": "white",
        "header_bg_color": "blue",
        "font_color": "#00FF00",
        "bg_color": "#4B0082",
        "border_font_color": "#00FF00",
        "border_bg_color": "#4B0082",
        "style": 2,
        "formatted": False
    },
    "chart_row": {
        "in_str": "",
        "len_cnt": 260,
        "align": "left",
        "bold": False,
        "italic": False,
        "header_font_color": "white",
        "header_bg_color": "blue",
        "font_color": "white",
        "bg_color": "black",
        "border_font_color": "#00FF00",
        "border_bg_color": "#4B0082",
        "style": 2,
        "formatted": False
    },
    "chart_bottom": {
        "in_str": "",
        "len_cnt": 260,
        "align": "left",
        "bold": True,
        "italic": False,
        "header_font_color": "white",
        "header_bg_color": "blue",
        "font_color": "#00FF00",
        "bg_color": "#4B0082",
        "border_font_color": "#00FF00",
        "border_bg_color": "#4B0082",
        "style": 2,
        "formatted": False
    }
}

theme = Settings('settings/theme.json', theme_json)
ts = theme.settings_load()
ts = AttrDict(ts)

chrt = CHRT(
    len_cnt=ts.chart.len_cnt, 
    align=ts.chart.align,
    bold=ts.chart.bold,
    italic=ts.chart.italic,
    font_color=ts.chart.font_color, 
    bg_color=ts.chart.bg_color, 
    header_font_color=ts.chart.header_font_color, 
    header_bg_color=ts.chart.header_bg_color, 
    border_font_color=ts.chart.border_font_color, 
    border_bg_color=ts.chart.border_bg_color, 
    style=2)

#<=====>#
# Classes
#<=====>#



#<=====>#
# Functions
#<=====>#


@narc(1)
def chart_top(in_str=None, len_cnt=None, align=None, bold=None, italic=None, font_color=None, bg_color=None, header_font_color=None, header_bg_color=None, border_font_color=None, border_bg_color=None, style=None, formatted=None):
    part = 'chart_top'
    in_str = in_str or ''
    len_cnt = len_cnt or ts[part].len_cnt
    align = align or ts[part].align
    bold = bold or ts[part].bold
    italic = italic or ts[part].italic
    font_color = font_color or ts[part].font_color
    bg_color = bg_color or ts[part].bg_color
    header_font_color = header_font_color or ts[part].header_font_color
    header_bg_color = header_bg_color or ts[part].header_bg_color
    border_font_color = border_font_color or ts[part].border_font_color
    border_bg_color = border_bg_color or ts[part].border_bg_color
    style = style or ts[part].style
    formatted = formatted or ts[part].formatted
    chrt.chart_top(in_str=in_str, len_cnt=len_cnt, align=align, bold=bold, italic=italic, font_color=font_color, bg_color=bg_color, border_font_color=border_font_color, border_bg_color=border_bg_color, style=style, formatted=formatted)

#<=====>#


@narc(1)
def chart_title(in_str=None, len_cnt=None, align=None, bold=None, italic=None, font_color=None, bg_color=None, header_font_color=None, header_bg_color=None, border_font_color=None, border_bg_color=None, style=None, formatted=None):
    part = 'chart_title'
    in_str = in_str or ''
    len_cnt = len_cnt or ts[part].len_cnt
    align = align or ts[part].align
    bold = bold or ts[part].bold
    italic = italic or ts[part].italic
    font_color = font_color or ts[part].font_color
    bg_color = bg_color or ts[part].bg_color
    header_font_color = header_font_color or ts[part].header_font_color
    header_bg_color = header_bg_color or ts[part].header_bg_color
    border_font_color = border_font_color or ts[part].border_font_color
    border_bg_color = border_bg_color or ts[part].border_bg_color
    style = style or ts[part].style
    formatted = formatted or ts[part].formatted
    chrt.chart_title(in_str=in_str, len_cnt=len_cnt, align=align, bold=bold, italic=italic, font_color=font_color, bg_color=bg_color, border_font_color=border_font_color, border_bg_color=border_bg_color, style=style, formatted=formatted)

#<=====>#


@narc(1)
def chart_headers(in_str=None, len_cnt=None, align=None, bold=None, italic=None, font_color=None, bg_color=None, header_font_color=None, header_bg_color=None, border_font_color=None, border_bg_color=None, style=None, formatted=None):
    part = 'chart_headers'
    in_str = in_str or ''
    len_cnt = len_cnt or ts[part].len_cnt
    align = align or ts[part].align
    bold = bold or ts[part].bold
    italic = italic or ts[part].italic
    font_color = font_color or ts[part].font_color
    bg_color = bg_color or ts[part].bg_color
    header_font_color = header_font_color or ts[part].header_font_color
    header_bg_color = header_bg_color or ts[part].header_bg_color
    border_font_color = border_font_color or ts[part].border_font_color
    border_bg_color = border_bg_color or ts[part].border_bg_color
    style = style or ts[part].style
    formatted = formatted or ts[part].formatted
    chrt.chart_headers(in_str=in_str, len_cnt=len_cnt, align=align, bold=bold, italic=italic, font_color=font_color, bg_color=bg_color, border_font_color=border_font_color, border_bg_color=border_bg_color, style=style, formatted=formatted)

#<=====>#


@narc(1)
def chart_mid(in_str=None, len_cnt=None, align=None, bold=None, italic=None, font_color=None, bg_color=None, header_font_color=None, header_bg_color=None, border_font_color=None, border_bg_color=None, style=None, formatted=None):
    part = 'chart_mid'
    in_str = in_str or ''
    len_cnt = len_cnt or ts[part].len_cnt
    align = align or ts[part].align
    bold = bold or ts[part].bold
    italic = italic or ts[part].italic
    font_color = font_color or ts[part].font_color
    bg_color = bg_color or ts[part].bg_color
    header_font_color = header_font_color or ts[part].header_font_color
    header_bg_color = header_bg_color or ts[part].header_bg_color
    border_font_color = border_font_color or ts[part].border_font_color
    border_bg_color = border_bg_color or ts[part].border_bg_color
    style = style or ts[part].style
    formatted = formatted or ts[part].formatted
    chrt.chart_mid(in_str=in_str, len_cnt=len_cnt, align=align, bold=bold, italic=italic, font_color=font_color, bg_color=bg_color, border_font_color=border_font_color, border_bg_color=border_bg_color, style=style, formatted=formatted)

#<=====>#


@narc(1)
def chart_row(in_str=None, len_cnt=None, align=None, bold=None, italic=None, font_color=None, bg_color=None, header_font_color=None, header_bg_color=None, border_font_color=None, border_bg_color=None, style=None, formatted=None):
    part = 'chart_row'
    in_str = in_str or ''
    len_cnt = len_cnt or ts[part].len_cnt
    align = align or ts[part].align
    bold = bold or ts[part].bold
    italic = italic or ts[part].italic
    font_color = font_color or ts[part].font_color
    bg_color = bg_color or ts[part].bg_color
    header_font_color = header_font_color or ts[part].header_font_color
    header_bg_color = header_bg_color or ts[part].header_bg_color
    border_font_color = border_font_color or ts[part].border_font_color
    border_bg_color = border_bg_color or ts[part].border_bg_color
    style = style or ts[part].style
    formatted = formatted or ts[part].formatted
    chrt.chart_row(in_str=in_str, len_cnt=len_cnt, align=align, bold=bold, italic=italic, font_color=font_color, bg_color=bg_color, border_font_color=border_font_color, border_bg_color=border_bg_color, style=style, formatted=formatted)

#<=====>#


@narc(1)
def chart_bottom(in_str=None, len_cnt=None, align=None, bold=None, italic=None, font_color=None, bg_color=None, header_font_color=None, header_bg_color=None, border_font_color=None, border_bg_color=None, style=None, formatted=None):
    part = 'chart_bottom'
    in_str = in_str or ''
    len_cnt = len_cnt or ts[part].len_cnt
    align = align or ts[part].align
    bold = bold or ts[part].bold
    italic = italic or ts[part].italic
    font_color = font_color or ts[part].font_color
    bg_color = bg_color or ts[part].bg_color
    header_font_color = header_font_color or ts[part].header_font_color
    header_bg_color = header_bg_color or ts[part].header_bg_color
    border_font_color = border_font_color or ts[part].border_font_color
    border_bg_color = border_bg_color or ts[part].border_bg_color
    style = style or ts[part].style
    formatted = formatted or ts[part].formatted
    chrt.chart_bottom(in_str=in_str, len_cnt=len_cnt, align=align, bold=bold, italic=italic, font_color=font_color, bg_color=bg_color, border_font_color=border_font_color, border_bg_color=border_bg_color, style=style, formatted=formatted)


#    pallette = {}
#    
#    # Reds
#    pallette["indianred"]             = "#CD5C5C"      # indianred                             #CD5C5C  205   92   92  389
#    pallette["lightcoral"]            = "#F08080"      # lightcoral                            #F08080  240  128  128  496
#    pallette["salmon"]                = "#FA8072"      # salmon                                #FA8072  250  128  114  492
#    pallette["darksalmon"]            = "#E9967A"      # darksalmon                            #E9967A  233  150  122  505
#    pallette["lightsalmon"]           = "#FFA07A"      # lightsalmon                           #FFA07A  255  160  122  537
#    pallette["crimson"]               = "#DC143C"      # crimson                               #DC143C  220   20   60  300
#    pallette["red"]                   = "#FF0000"      # red                                   #FF0000  255    0    0  255
#    pallette["firebrick"]             = "#B22222"      # firebrick                             #B22222  178   34   34  246
#    pallette["darkred"]               = "#8B0000"      # darkred                               #8B0000  139    0    0  139
#    
#    # Pinks
#    pallette["pink"]                  = "#FFC0CB"      # pink                                  #FFC0CB  255  192  203  650
#    pallette["lightpink"]             = "#FFB6C1"      # lightpink                             #FFB6C1  255  182  193  630
#    pallette["hotpink"]               = "#FF69B4"      # hotpink                               #FF69B4  255  105  180  540
#    pallette["deeppink"]              = "#FF1493"      # deeppink                              #FF1493  255   20  147  422
#    pallette["mediumvioletred"]       = "#C71585"      # mediumvioletred                       #C71585  199   21  133  353
#    pallette["palevioletred"]         = "#DB7093"      # palevioletred                         #DB7093  219  112  147  478
#    
#    # Oranges
#    pallette["lightsalmon"]           = "#FFA07A"      # lightsalmon                           #FFA07A  255  160  122  537
#    pallette["coral"]                 = "#FF7F50"      # coral                                 #FF7F50  255  127   80  462
#    pallette["tomato"]                = "#FF6347"      # tomato                                #FF6347  255   99   71  425
#    pallette["orangered"]             = "#FF4500"      # orangered                             #FF4500  255   69    0  324
#    pallette["darkorange"]            = "#FF8C00"      # darkorange                            #FF8C00  255  140    0  395
#    pallette["orange"]                = "#FFA500"      # orange                                #FFA500  255  165    0  420
#    
#    # Yellows
#    pallette["gold"]                  = "#FFD700"      # gold                                  #FFD700  255  215    0  470
#    pallette["yellow"]                = "#FFFF00"      # yellow                                #FFFF00  255  255    0  510
#    pallette["lightyellow"]           = "#FFFFE0"      # lightyellow                           #FFFFE0  255  255  224  734
#    pallette["lemonchiffon"]          = "#FFFACD"      # lemonchiffon                          #FFFACD  255  250  205  710
#    pallette["lightgoldenrodyellow"]  = "#FAFAD2"      # lightgoldenrodyellow                  #FAFAD2  250  250  210  710
#    pallette["papayawhip"]            = "#FFEFD5"      # papayawhip                            #FFEFD5  255  239  213  707
#    pallette["moccasin"]              = "#FFE4B5"      # moccasin                              #FFE4B5  255  228  181  664
#    pallette["peachpuff"]             = "#FFDAB9"      # peachpuff                             #FFDAB9  255  218  185  658
#    pallette["palegoldenrod"]         = "#EEE8AA"      # palegoldenrod                         #EEE8AA  238  232  170  640
#    pallette["darkkhaki"]             = "#BDB76B"      # darkkhaki                             #BDB76B  189  183  107  479
#    pallette["khaki"]                 = "#F0E68C"      # khaki                                 #F0E68C  240  230  140  610
#    
#    # Purples
#    pallette["lavender"]              = "#E6E6FA"      # lavender                              #E6E6FA  230  230  250  710
#    pallette["thistle"]               = "#D8BFD8"      # thistle                               #D8BFD8  216  191  216  623
#    pallette["plum"]                  = "#DDA0DD"      # plum                                  #DDA0DD  221  160  221  602
#    pallette["violet"]                = "#EE82EE"      # violet                                #EE82EE  238  130  238  606
#    pallette["orchid"]                = "#DA70D6"      # orchid                                #DA70D6  218  112  214  544
#    pallette["fuchsia"]               = "#FF00FF"      # fuchsia                               #FF00FF  255    0  255  510
#    pallette["magenta"]               = "#FF00FF"      # magenta                               #FF00FF  255    0  255  510
#    pallette["mediumorchid"]          = "#BA55D3"      # mediumorchid                          #BA55D3  186   85  211  482
#    pallette["mediumpurple"]          = "#9370DB"      # mediumpurple                          #9370DB  147  112  219  478
#    pallette["rebeccapurple"]         = "#663399"      # rebeccapurple                         #663399  102   51  153  306
#    pallette["blueviolet"]            = "#8A2BE2"      # blueviolet                            #8A2BE2  138   43  226  407
#    pallette["darkviolet"]            = "#9400D3"      # darkviolet                            #9400D3  148    0  211  359
#    pallette["darkorchid"]            = "#9932CC"      # darkorchid                            #9932CC  153   50  204  407
#    pallette["darkmagenta"]           = "#8B008B"      # darkmagenta                           #8B008B  139    0  139  278
#    pallette["purple"]                = "#800080"      # purple                                #800080  128    0  128  256
#    pallette["indigo"]                = "#4B0082"      # indigo                                #4B0082   75    0  130  205
#    pallette["slateblue"]             = "#6A5ACD"      # slateblue                             #6A5ACD  106   90  205  401
#    pallette["darkslateblue"]         = "#483D8B"      # darkslateblue                         #483D8B   72   61  139  272
#    pallette["mediumslateblue"]       = "#7B68EE"      # mediumslateblue                       #7B68EE  123  104  238  465
#    
#    # Greens
#    pallette["greenyellow"]           = "#ADFF2F"      # greenyellow                           #ADFF2F  173  255   47  475
#    pallette["chartreuse"]            = "#7FFF00"      # chartreuse                            #7FFF00  127  255    0  382
#    pallette["lawngreen"]             = "#7CFC00"      # lawngreen                             #7CFC00  124  252    0  376
#    pallette["lime"]                  = "#00FF00"      # lime                                  #00FF00    0  255    0  255
#    pallette["limegreen"]             = "#32CD32"      # limegreen                             #32CD32   50  205   50  305
#    pallette["palegreen"]             = "#98FB98"      # palegreen                             #98FB98  152  251  152  555
#    pallette["lightgreen"]            = "#90EE90"      # lightgreen                            #90EE90  144  238  144  526
#    pallette["mediumspringgreen"]     = "#00FA9A"      # mediumspringgreen                     #00FA9A    0  250  154  404
#    pallette["springgreen"]           = "#00FF7F"      # springgreen                           #00FF7F    0  255  127  382
#    pallette["mediumseagreen"]        = "#3CB371"      # mediumseagreen                        #3CB371   60  179  113  352
#    pallette["seagreen"]              = "#2E8B57"      # seagreen                              #2E8B57   46  139   87  272
#    pallette["forestgreen"]           = "#228B22"      # forestgreen                           #228B22   34  139   34  207
#    pallette["green"]                 = "#008000"      # green                                 #008000    0  128    0  128
#    pallette["darkgreen"]             = "#006400"      # darkgreen                             #006400    0  100    0  100
#    pallette["yellowgreen"]           = "#9ACD32"      # yellowgreen                           #9ACD32  154  205   50  409
#    pallette["olivedrab"]             = "#6B8E23"      # olivedrab                             #6B8E23  107  142   35  284
#    pallette["olive"]                 = "#808000"      # olive                                 #808000  128  128    0  256
#    pallette["darkolivegreen"]        = "#556B2F"      # darkolivegreen                        #556B2F   85  107   47  239
#    pallette["mediumaquamarine"]      = "#66CDAA"      # mediumaquamarine                      #66CDAA  102  205  170  477
#    pallette["darkseagreen"]          = "#8FBC8F"      # darkseagreen                          #8FBC8F  143  188  143  474
#    pallette["lightseagreen"]         = "#20B2AA"      # lightseagreen                         #20B2AA   32  178  170  380
#    pallette["darkcyan"]              = "#008B8B"      # darkcyan                              #008B8B    0  139  139  278
#    pallette["teal"]                  = "#008080"      # teal                                  #008080    0  128  128  256
#    
#    # Blues
#    pallette["aqua"]                  = "#00FFFF"      # aqua                                  #00FFFF    0  255  255  510
#    pallette["cyan"]                  = "#00FFFF"      # cyan                                  #00FFFF    0  255  255  510
#    pallette["lightcyan"]             = "#E0FFFF"      # lightcyan                             #E0FFFF  224  255  255  734
#    pallette["paleturquoise"]         = "#AFEEEE"      # paleturquoise                         #AFEEEE  175  238  238  651
#    pallette["aquamarine"]            = "#7FFFD4"      # aquamarine                            #7FFFD4  127  255  212  594
#    pallette["turquoise"]             = "#40E0D0"      # turquoise                             #40E0D0   64  224  208  496
#    pallette["mediumturquoise"]       = "#48D1CC"      # mediumturquoise                       #48D1CC   72  209  204  485
#    pallette["darkturquoise"]         = "#00CED1"      # darkturquoise                         #00CED1    0  206  209  415
#    pallette["cadetblue"]             = "#5F9EA0"      # cadetblue                             #5F9EA0   95  158  160  413
#    pallette["steelblue"]             = "#4682B4"      # steelblue                             #4682B4   70  130  180  380
#    pallette["lightsteelblue"]        = "#B0C4DE"      # lightsteelblue                        #B0C4DE  176  196  222  594
#    pallette["powderblue"]            = "#B0E0E6"      # powderblue                            #B0E0E6  176  224  230  630
#    pallette["lightblue"]             = "#ADD8E6"      # lightblue                             #ADD8E6  173  216  230  619
#    pallette["skyblue"]               = "#87CEEB"      # skyblue                               #87CEEB  135  206  235  576
#    pallette["lightskyblue"]          = "#87CEFA"      # lightskyblue                          #87CEFA  135  206  250  591
#    pallette["deepskyblue"]           = "#00BFFF"      # deepskyblue                           #00BFFF    0  191  255  446
#    pallette["dodgerblue"]            = "#1E90FF"      # dodgerblue                            #1E90FF   30  144  255  429
#    pallette["cornflowerblue"]        = "#6495ED"      # cornflowerblue                        #6495ED  100  149  237  486
#    pallette["mediumslateblue"]       = "#7B68EE"      # mediumslateblue                       #7B68EE  123  104  238  465
#    pallette["royalblue"]             = "#4169E1"      # royalblue                             #4169E1   65  105  225  395
#    pallette["blue"]                  = "#0000FF"      # blue                                  #0000FF    0    0  255  255
#    pallette["mediumblue"]            = "#0000CD"      # mediumblue                            #0000CD    0    0  205  205
#    pallette["darkblue"]              = "#00008B"      # darkblue                              #00008B    0    0  139  139
#    pallette["navy"]                  = "#000080"      # navy                                  #000080    0    0  128  128
#    pallette["midnightblue"]          = "#191970"      # midnightblue                          #191970   25   25  112  162
#    
#    # Browns
#    pallette["cornsilk"]              = "#FFF8DC"      # cornsilk                              #FFF8DC  255  248  220  723
#    pallette["blanchedalmond"]        = "#FFEBCD"      # blanchedalmond                        #FFEBCD  255  235  205  695
#    pallette["bisque"]                = "#FFE4C4"      # bisque                                #FFE4C4  255  228  196  679
#    pallette["navajowhite"]           = "#FFDEAD"      # navajowhite                           #FFDEAD  255  222  173  650
#    pallette["wheat"]                 = "#F5DEB3"      # wheat                                 #F5DEB3  245  222  179  646
#    pallette["burlywood"]             = "#DEB887"      # burlywood                             #DEB887  222  184  135  541
#    pallette["tan"]                   = "#D2B48C"      # tan                                   #D2B48C  210  180  140  530
#    pallette["rosybrown"]             = "#BC8F8F"      # rosybrown                             #BC8F8F  188  143  143  474
#    pallette["sandybrown"]            = "#F4A460"      # sandybrown                            #F4A460  244  164   96  504
#    pallette["goldenrod"]             = "#DAA520"      # goldenrod                             #DAA520  218  165   32  415
#    pallette["darkgoldenrod"]         = "#B8860B"      # darkgoldenrod                         #B8860B  184  134   11  329
#    pallette["peru"]                  = "#CD853F"      # peru                                  #CD853F  205  133   63  401
#    pallette["chocolate"]             = "#D2691E"      # chocolate                             #D2691E  210  105   30  345
#    pallette["saddlebrown"]           = "#8B4513"      # saddlebrown                           #8B4513  139   69   19  227
#    pallette["sienna"]                = "#A0522D"      # sienna                                #A0522D  160   82   45  287
#    pallette["brown"]                 = "#A52A2A"      # brown                                 #A52A2A  165   42   42  249
#    pallette["maroon"]                = "#800000"      # maroon                                #800000  128    0    0  128
#    
#    # Whites
#    pallette["white"]                 = "#FFFFFF"      # white                                 #FFFFFF  255  255  255  765
#    pallette["snow"]                  = "#FFFAFA"      # snow                                  #FFFAFA  255  250  250  755
#    pallette["honeydew"]              = "#F0FFF0"      # honeydew                              #F0FFF0  240  255  240  735
#    pallette["mintcream"]             = "#F5FFFA"      # mintcream                             #F5FFFA  245  255  250  750
#    pallette["azure"]                 = "#F0FFFF"      # azure                                 #F0FFFF  240  255  255  750
#    pallette["aliceblue"]             = "#F0F8FF"      # aliceblue                             #F0F8FF  240  248  255  743
#    pallette["ghostwhite"]            = "#F8F8FF"      # ghostwhite                            #F8F8FF  248  248  255  751
#    pallette["whitesmoke"]            = "#F5F5F5"      # whitesmoke                            #F5F5F5  245  245  245  735
#    pallette["seashell"]              = "#FFF5EE"      # seashell                              #FFF5EE  255  245  238  738
#    pallette["beige"]                 = "#F5F5DC"      # beige                                 #F5F5DC  245  245  220  710
#    pallette["oldlace"]               = "#FDF5E6"      # oldlace                               #FDF5E6  253  245  230  728
#    pallette["floralwhite"]           = "#FFFAF0"      # floralwhite                           #FFFAF0  255  250  240  745
#    pallette["ivory"]                 = "#FFFFF0"      # ivory                                 #FFFFF0  255  255  240  750
#    pallette["antiquewhite"]          = "#FAEBD7"      # antiquewhite                          #FAEBD7  250  235  215  700
#    pallette["linen"]                 = "#FAF0E6"      # linen                                 #FAF0E6  250  240  230  720
#    pallette["lavenderblush"]         = "#FFF0F5"      # lavenderblush                         #FFF0F5  255  240  245  740
#    pallette["mistyrose"]             = "#FFE4E1"      # mistyrose                             #FFE4E1  255  228  225  708
#    
#    # Grays
#    pallette["gainsboro"]             = "#DCDCDC"      # gainsboro                             #DCDCDC  220  220  220  660
#    pallette["lightgray"]             = "#D3D3D3"      # lightgray                             #D3D3D3  211  211  211  633
#    #pallette["lightgrey"]             = "#D3D3D3"      # lightgrey                             #D3D3D3  211  211  211  633
#    pallette["silver"]                = "#C0C0C0"      # silver                                #C0C0C0  192  192  192  576
#    pallette["darkgray"]              = "#A9A9A9"      # darkgray                              #A9A9A9  169  169  169  507
#    #pallette["darkgrey"]              = "#A9A9A9"      # darkgrey                              #A9A9A9  169  169  169  507
#    pallette["gray"]                  = "#808080"      # gray                                  #808080  128  128  128  384
#    #pallette["grey"]                  = "#808080"      # grey                                  #808080  128  128  128  384
#    pallette["dimgray"]               = "#696969"      # dimgray                               #696969  105  105  105  315
#    #pallette["dimgrey"]               = "#696969"      # dimgrey                               #696969  105  105  105  315
#    pallette["lightslategray"]        = "#778899"      # lightslategray                        #778899  119  136  153  408
#    #pallette["lightslategrey"]        = "#778899"      # lightslategrey                        #778899  119  136  153  408
#    pallette["slategray"]             = "#708090"      # slategray                             #708090  112  128  144  384
#    #pallette["slategrey"]             = "#708090"      # slategrey                             #708090  112  128  144  384
#    pallette["darkslategray"]         = "#2F4F4F"      # darkslategray                         #2F4F4F   47   79   79  205
#    #pallette["darkslategrey"]         = "#2F4F4F"      # darkslategrey                         #2F4F4F   47   79   79  205
#    pallette["black"]                 = "#000000"      # black                                 #000000    0    0    0    0

#<=====>#


@narc(1)
def cp_pct_color(pct, msg):
    print(cs_pct_color(pct,msg))

#<=====>#


@narc(1)
def cs_pct_color(pct, msg):
    if pct >= 25:       # >= 8
        r = WoG6(msg, print_yn='N')
    elif pct >= 20 and  pct < 25:
        r = WoG5(msg, print_yn='N')
    elif pct >= 15 and  pct < 20:
        r = WoG4(msg, print_yn='N')
    elif pct >= 10 and  pct < 15:
        r = WoG3(msg, print_yn='N')
    elif pct >= 5 and  pct < 10:
        r = WoG2(msg, print_yn='N')
    elif pct >= 2 and  pct < 5:
        r = WoG1(msg, print_yn='N')

    elif pct > -2 and pct < 2:
        r = cs(msg, font_color='white', bg_color='black')

    elif pct <= -2 and pct > -5:
        r = WoR1(msg, print_yn='N')
    elif pct <= -5 and pct > -10:
        r = WoR2(msg, print_yn='N')
    elif pct <= -10 and pct > -15:
        r = WoR3(msg, print_yn='N')
    elif pct <= -15 and pct > -20:
        r = WoR4(msg, print_yn='N')
    elif pct <= -20 and pct > -25:
        r = WoR5(msg, print_yn='N')
    elif pct <= -25:
        r = WoR6(msg, print_yn='N')

    return r

#<=====>#


@narc(1)
def cp_pct_color_50(pct, msg):
    print(cs_pct_color_50(pct,msg))

#<=====>#


@narc(1)
def cs_pct_color_50(pct, msg):
    if pct >= 90:
        r = WoG6(msg, print_yn='N')
    elif pct >= 82.5:
        r = WoG5(msg, print_yn='N')
    elif pct >= 75:
        r = WoG4(msg, print_yn='N')
    elif pct >= 67.5:
        r = WoG3(msg, print_yn='N')
    elif pct >= 60:
        r = WoG2(msg, print_yn='N')
    elif pct >= 52.5:
        r = WoG1(msg, print_yn='N')
    elif pct >= 45:
        r = cs(msg, font_color='green', bg_color='black')
    elif pct >= 37.5:
        r = WoR1(msg, print_yn='N')
    elif pct >= 30:
        r = WoR2(msg, print_yn='N')
    elif pct >= 22.5:
        r = WoR3(msg, print_yn='N')
    elif pct >= 15:
        r = WoR4(msg, print_yn='N')
    elif pct >= 7.5:
        r = WoR5(msg, print_yn='N')
    else:
        r = WoR6(msg, print_yn='N')

    return r

#<=====>#


@narc(1)
def cs_pct_color_green_gradient(pct, max_pct, msg):
    incr = max_pct / 7
    if pct >= incr * 7:
        r = WoG6(msg, print_yn='N')
    elif pct >= incr * 6:
        r = WoG5(msg, print_yn='N')
    elif pct >= incr * 5:
        r = WoG4(msg, print_yn='N')
    elif pct >= incr * 4:
        r = WoG3(msg, print_yn='N')
    elif pct >= incr * 3:
        r = WoG2(msg, print_yn='N')
    elif pct >= incr * 2:
        r = WoG1(msg, print_yn='N')
    else:
        r = cs(msg, font_color='green', bg_color='black')
    return r

#<=====>#


@narc(1)
def cp_pct_color_100(pct, msg):
    print(cs_pct_color_100(pct,msg))

#<=====>#


@narc(1)
def cs_pct_color_100(pct, msg):
    if pct >= 90:
        r = WoG6(msg, print_yn='N')
    elif pct >= 82.5:
        r = WoG5(msg, print_yn='N')
    elif pct >= 75:
        r = WoG4(msg, print_yn='N')
    elif pct >= 67.5:
        r = WoG3(msg, print_yn='N')
    elif pct >= 60:
        r = WoG2(msg, print_yn='N')
    elif pct >= 52.5:
        r = WoG1(msg, print_yn='N')
    elif pct >= 45:
        r = msg
    elif pct >= 37.5:
        r = WoR1(msg, print_yn='N')
    elif pct >= 30:
        r = WoR2(msg, print_yn='N')
    elif pct >= 22.5:
        r = WoR3(msg, print_yn='N')
    elif pct >= 15:
        r = WoR4(msg, print_yn='N')
    elif pct >= 7.5:
        r = WoR5(msg, print_yn='N')
    else:
        r = WoR6(msg, print_yn='N')

    return r

#<=====>#


@narc(1)
def prt_cols(l, cols=10, clr='WoG'):
    """🔴 UTILITY - Extracted from cls_bot.py (~20 lines)
    
    Formats lists into columnar display for terminal output.
    
    LOW RISK: Display formatting utility
    - Formats list items into columns with color coding
    - Integrates with chart system for display
    - Used for market pair display and other list formatting
    - FIXED: Uses fstrent_charts display_length for proper ANSI-aware alignment
    """
    # Create a CHRT instance to access display_length function
    chart_helper = CHRT()
    
    col_cnt = 0
    s = ''
    for x in l:
        col_cnt += 1
        
        # Apply color styling first
        if clr == 'WoG':
            colored_text = cs(text=str(x), font_color='white', bg_color='green')
        elif clr == 'GoW':
            colored_text = cs(text=str(x), font_color='green', bg_color='white')
        else:
            colored_text = str(x)
        
        # Calculate the visual length using your fstrent_charts function
        visual_length = chart_helper.display_length(colored_text)
        
        # Pad to exactly 15 visual characters using ANSI-aware padding
        if visual_length < 15:
            # Add spaces to reach 15 visual characters
            padding_needed = 15 - visual_length
            colored_text += ' ' * padding_needed
        elif visual_length > 15:
            # Truncate if too long (shouldn't happen with crypto pairs)
            # This preserves the color codes while truncating content
            plain_text = chart_helper.strip_formatting(colored_text)
            truncated_plain = plain_text[:15]
            if clr == 'WoG':
                colored_text = cs(text=truncated_plain, font_color='white', bg_color='green')
            elif clr == 'GoW':
                colored_text = cs(text=truncated_plain, font_color='green', bg_color='white')
            else:
                colored_text = truncated_plain
        
        s += colored_text
        
        if col_cnt % cols == 0:
            chart_row(s)
            s = ''
            col_cnt = 0
        elif col_cnt == len(l):
            s += ''
        else:
            s += ' | '
    if col_cnt > 0 and col_cnt < cols:
        chart_row(s)

#<=====>#


@narc(1)
def bh1(text, font_color='#FFFFFF', bg_color='#FFFFFF', bold=True, italic=True, length=200, align='center'):
    cp(text, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic, length=length, align=align)


@narc(1)
def bh2(text, font_color='#FFFFFF', bg_color='#FFFFFF', bold=True, italic=True, length=200, align='center'):
    cp(text, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic, length=length, align=align)


@narc(1)
def bh3(text, font_color='#FFFFFF', bg_color='#FFFFFF', bold=True, italic=True, length=200, align='center'):
    cp(text, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic, length=length, align=align)

#<=====>#


@narc(1)
def sh1(text, font_color='#FFFFFF', bg_color='#800080', bold=True, italic=True, length=200, align='center'):
    cp(text, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic, length=length, align=align)


@narc(1)
def sh2(text, font_color='#FFFFFF', bg_color='#FFFFFF', bold=True, italic=True, length=200, align='center'):
    cp(text, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic, length=length, align=align)


@narc(1)
def sh3(text, font_color='#FFFFFF', bg_color='#FFFFFF', bold=True, italic=True, length=200, align='center'):
    cp(text, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic, length=length, align=align)

#<=====>#


@narc(1)
def bad0(text, font_color='#FFFFFF', bg_color='#FF0000', bold=True, italic=True, length=200, align='center'):
    cp(text, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic, length=length, align=align)


@narc(1)
def bad1(text, font_color='#FFFFFF', bg_color='#FF0000', bold=True, italic=True, length=200, align='center'):
    cp(text, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic, length=length, align=align)


@narc(1)
def bad2(text, font_color='#FFFFFF', bg_color='#FF0000', bold=True, italic=True, length=200, align='center'):
    cp(text, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic, length=length, align=align)


@narc(1)
def bad3(text, font_color='#FFFFFF', bg_color='#FF0000', bold=True, italic=True, length=200, align='center'):
    cp(text, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic, length=length, align=align)

#<=====>#


@narc(1)
def good0(text, font_color='#FFFFFF', bg_color='#008000', bold=True, italic=True, length=200, align='center'):
    cp(text, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic, length=length, align=align)


@narc(1)
def good1(text, font_color='#FFFFFF', bg_color='#008000', bold=True, italic=True, length=200, align='center'):
    cp(text, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic, length=length, align=align)


@narc(1)
def good2(text, font_color='#FFFFFF', bg_color='#008000', bold=True, italic=True, length=200, align='center'):
    cp(text, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic, length=length, align=align)


@narc(1)
def good3(text, font_color='#FFFFFF', bg_color='#008000', bold=True, italic=True, length=200, align='center'):
    cp(text, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic, length=length, align=align)

#<=====>#


@narc(1)
def WoR6(text, font_color='#FFFFFF', bg_color='#FF0000', bold=False, italic=False, length=0, align='left', print_yn='Y'):
    if print_yn == 'Y':
        cp(text, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic, length=length, align=align)
    else:
        return cs(text, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic, length=length, align=align)


@narc(1)
def WoR5(text, font_color='#FFFFFF', bg_color='#FF4500', bold=False, italic=False, length=0, align='left', print_yn='Y'):
    if print_yn == 'Y':
        cp(text, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic, length=length, align=align)
    else:
        return cs(text, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic, length=length, align=align)


@narc(1)
def WoR4(text, font_color='#FFFFFF', bg_color='#FFA500', bold=False, italic=False, length=0, align='left', print_yn='Y'):
    if print_yn == 'Y':
        cp(text, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic, length=length, align=align)
    else:
        return cs(text, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic, length=length, align=align)


@narc(1)
def WoR3(text, font_color='#FF0000', bg_color='#000000', bold=False, italic=False, length=0, align='left', print_yn='Y'):
    if print_yn == 'Y':
        cp(text, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic, length=length, align=align)
    else:
        return cs(text, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic, length=length, align=align)


@narc(1)
def WoR2(text, font_color='#FF4500', bg_color='#000000', bold=False, italic=False, length=0, align='left', print_yn='Y'):
    if print_yn == 'Y':
        cp(text, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic, length=length, align=align)
    else:
        return cs(text, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic, length=length, align=align)


@narc(1)
def WoR1(text, font_color='#FFA500', bg_color='#000000', bold=False, italic=False, length=0, align='left', print_yn='Y'):
    if print_yn == 'Y':
        cp(text, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic, length=length, align=align)
    else:
        return cs(text, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic, length=length, align=align)

#    # Reds
#    pallette["indianred"]             = "#CD5C5C"      # indianred                             #CD5C5C  205   92   92  389
#    pallette["lightcoral"]            = "#F08080"      # lightcoral                            #F08080  240  128  128  496
#    pallette["salmon"]                = "#FA8072"      # salmon                                #FA8072  250  128  114  492
#    pallette["darksalmon"]            = "#E9967A"      # darksalmon                            #E9967A  233  150  122  505
#    pallette["lightsalmon"]           = "#FFA07A"      # lightsalmon                           #FFA07A  255  160  122  537
#    pallette["crimson"]               = "#DC143C"      # crimson                               #DC143C  220   20   60  300
#    pallette["red"]                   = "#FF0000"      # red                                   #FF0000  255    0    0  255
#    pallette["firebrick"]             = "#B22222"      # firebrick                             #B22222  178   34   34  246
#    pallette["darkred"]               = "#8B0000"      # darkred                               #8B0000  139    0    0  139

#<=====>#


@narc(1)
def WoG1(text, font_color='#228B22', bg_color='#000000', bold=False, italic=False, length=0, align='left', print_yn='Y'):
    if print_yn == 'Y':
        cp(text, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic, length=length, align=align)
    else:
        return cs(text, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic, length=length, align=align)


@narc(1)
def WoG2(text, font_color='#32CD32', bg_color='#000000', bold=False, italic=False, length=0, align='left', print_yn='Y'):
    if print_yn == 'Y':
        cp(text, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic, length=length, align=align)
    else:
        return cs(text, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic, length=length, align=align)


@narc(1)
def WoG3(text, font_color='#9ACD32', bg_color='#000000', bold=False, italic=False, length=0, align='left', print_yn='Y'):
    if print_yn == 'Y':
        cp(text, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic, length=length, align=align)
    else:
        return cs(text, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic, length=length, align=align)


@narc(1)
def WoG4(text, font_color='#FFFFFF', bg_color='#9ACD32', bold=False, italic=False, length=0, align='left', print_yn='Y'):
    if print_yn == 'Y':
        cp(text, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic, length=length, align=align)
    else:
        return cs(text, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic, length=length, align=align)


@narc(1)
def WoG5(text, font_color='#FFFFFF', bg_color='#32CD32', bold=False, italic=False, length=0, align='left', print_yn='Y'):
    if print_yn == 'Y':
        cp(text, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic, length=length, align=align)
    else:
        return cs(text, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic, length=length, align=align)


@narc(1)
def WoG6(text, font_color='#FFFFFF', bg_color='#228B22', bold=False, italic=False, length=0, align='left', print_yn='Y'):
    if print_yn == 'Y':
        cp(text, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic, length=length, align=align)
    else:
        return cs(text, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic, length=length, align=align)

#<=====>#
# Post Variables
#<=====>#


#<=====>#
# Default Run
#<=====>#

if __name__ == "__main__":
    WoR6('WoR6 - WoR6 - WoR6')
    WoR5('WoR5 - WoR5 - WoR5')
    WoR4('WoR4 - WoR4 - WoR4')
    WoR3('WoR3 - WoR3 - WoR3')
    WoR2('WoR2 - WoR2 - WoR2')
    WoR1('WoR1 - WoR1 - WoR1')
    WoG1('WoG1 - WoG1 - WoG1')
    WoG2('WoG2 - WoG2 - WoG2')
    WoG3('WoG3 - WoG3 - WoG3')
    WoG4('WoG4 - WoG4 - WoG4')
    WoG5('WoG5 - WoG5 - WoG5')
    WoG6('WoG6 - WoG6 - WoG6')

    print()

    cp('lime                  = #00FF00', font_color="#FFFFFF", bg_color="#00FF00")      # lime             
    cp('limegreen             = #32CD32', font_color="#FFFFFF", bg_color="#32CD32")      # limegreen        
    cp('forestgreen           = #228B22', font_color="#FFFFFF", bg_color="#228B22")      # forestgreen      
    cp('green                 = #008000', font_color="#FFFFFF", bg_color="#008000")      # green            
    cp('darkgreen             = #006400', font_color="#FFFFFF", bg_color="#006400")      # darkgreen        

    print()
    cp('greenyellow           = #ADFF2F', font_color="#FFFFFF", bg_color="#ADFF2F")      # greenyellow      
    cp('chartreuse            = #7FFF00', font_color="#FFFFFF", bg_color="#7FFF00")      # chartreuse       
    cp('lawngreen             = #7CFC00', font_color="#FFFFFF", bg_color="#7CFC00")      # lawngreen        
    cp('palegreen             = #98FB98', font_color="#FFFFFF", bg_color="#98FB98")      # palegreen        
    cp('lightgreen            = #90EE90', font_color="#FFFFFF", bg_color="#90EE90")      # lightgreen       
    cp('mediumspringgreen     = #00FA9A', font_color="#FFFFFF", bg_color="#00FA9A")      # mediumspringgreen
    cp('springgreen           = #00FF7F', font_color="#FFFFFF", bg_color="#00FF7F")      # springgreen      

    print()
    cp('yellowgreen           = #9ACD32', font_color="#FFFFFF", bg_color="#9ACD32")      # yellowgreen      
    cp('olivedrab             = #6B8E23', font_color="#FFFFFF", bg_color="#6B8E23")      # olivedrab        
    cp('olive                 = #808000', font_color="#FFFFFF", bg_color="#808000")      # olive            
    cp('darkolivegreen        = #556B2F', font_color="#FFFFFF", bg_color="#556B2F")      # darkolivegreen   
    cp('mediumseagreen        = #3CB371', font_color="#FFFFFF", bg_color="#3CB371")      # mediumseagreen   
    cp('seagreen              = #2E8B57', font_color="#FFFFFF", bg_color="#2E8B57")      # seagreen         

    print()
    cp('mediumaquamarine      = #66CDAA', font_color="#FFFFFF", bg_color="#66CDAA")      # mediumaquamarine 
    cp('darkseagreen          = #8FBC8F', font_color="#FFFFFF", bg_color="#8FBC8F")      # darkseagreen     
    cp('lightseagreen         = #20B2AA', font_color="#FFFFFF", bg_color="#20B2AA")      # lightseagreen    
    cp('darkcyan              = #008B8B', font_color="#FFFFFF", bg_color="#008B8B")      # darkcyan         
    cp('teal                  = #008080', font_color="#FFFFFF", bg_color="#008080")      # teal             

    cp(' * bold italic teal = #008080', font_color="#FFFFFF", bg_color="#008080", bold=True, italic=True, length=69, align='center')      # teal             

#<=====>#
