#<=====>#
# Import All Scope
#<=====>#
import_all_func_list = []

import_all_func_list.append("lpad")
import_all_func_list.append("rpad")
import_all_func_list.append("cpad")

import_all_func_list.append("left")
import_all_func_list.append("right")
import_all_func_list.append("mid")

import_all_func_list.append("IsEnglish")
import_all_func_list.append("format_disp_age")
import_all_func_list.append("format_disp_age2")
import_all_func_list.append("short_link")

import_all_func_list.append("strip_formatting")
import_all_func_list.append("display_length")


__all__ = import_all_func_list

#<=====>#
# Imports - Common Modules
#<=====>#
import re
import sys, os

#<=====>#
# Imports - Download Modules
#<=====>#

#<=====>#
# Imports - Unsure if used/needed
#<=====>#

#<=====>#
# Imports - Recently Removed
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


#<=====>#
# Variables
#<=====>#
lib_name            = 'lib_strings'
log_name            = 'lib_strings'
verbosity           = 1
lib_debug_lvl       = 1
lib_display_lvl     = 1

#<=====>#
# Assignments Pre
#<=====>#


#<=====>#
# Classes
#<=====>#


#<=====>#
# Functions
#<=====>#

def format_disp_age(age_mins, fmt_style=1):
	# func_name = 'format_disp_age'
	# func_str = f'{lib_name}.{func_name}(age_mins={age_mins})'

	age_days    = age_mins // (24 * 60)
	age_hours   = (age_mins // 60) % 24
	age_minutes = age_mins % 60

	if fmt_style == 1:	
		if age_mins < 60:
			disp_age = f"{'':>3} {'':>2} {age_minutes:>2}"
		elif age_mins >= 60 and age_mins < 600:
			disp_age = f"{'':>3} {age_hours:>2}:{age_minutes:>02}"
		elif age_mins >= 600 and age_days < 1:
			disp_age = f"{'':>3} {age_hours:>02}:{age_minutes:>02}"
		else:
			disp_age = f"{age_days:>3} {age_hours:02}:{age_minutes:02}"
	elif fmt_style == 2:
		disp_age = ''
		if age_days > 0:
			disp_age += f"{age_days}:"
		if age_hours > 0:
			disp_age += f"{age_hours}:"
		if age_minutes >= 0:
			disp_age += f"{age_minutes}"

	return disp_age

	#<=====>#

def format_disp_age2(in_age_secs):
	in_age_secs = int(in_age_secs)	
	age_days    = in_age_secs // (24 * 60 * 60)
	age_hours   = (in_age_secs // (60 * 60)) % 24
	age_minutes = (in_age_secs // 60) % 60
	age_secs    = in_age_secs % 60

	disp_age = ''
	if age_days > 0:
		disp_age += f"{age_days} "
	if age_hours > 0:
		disp_age += f"{age_hours}:"
	if age_minutes >= 0:
		disp_age += f"{age_minutes}:"
	if age_secs >= 0:
		disp_age += f"{age_secs}"

	return disp_age

#<=====>#

def IsEnglish(s):
	try:
		s.encode(encoding='utf-8').decode('ascii')
	except UnicodeDecodeError:
		return False
	else:
		return True

#<=====>#

def short_link(url, display_text):
	# Use the OSC 8 escape sequence to start the hyperlink
	# Then use the ST escape to stop it.
	return(f'\033]8;;{url}\033\\{display_text}\033]8;;\033\\')

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

def display_length(in_str):
	strip_str = strip_formatting(in_str)
	display_length = len(strip_str)
	return display_length

#<=====>#
# Assignments Post
#<=====>#


#<=====>#
# Default Run
#<=====>#


#<=====>#


