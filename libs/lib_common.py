<<<<<<< Updated upstream
#<=====>#
# Description
#<=====>#



#<=====>#
# Known To Do List
#<=====>#



#<=====>#
# Imports
#<=====>#
from datetime import datetime as dt
from libs.cls_settings import AttrDict
from libs.cls_settings import Settings
from pprint import pformat
from pprint import pprint
from termcolor import cprint
# import beepy
import concurrent.futures
import datetime
import decimal
import errno
import json
import os
import pyttsx3
import pytz
import sys
import time
import traceback
import winsound


#<=====>#
# Variables
#<=====>#
lib_name            = 'lib_common'
log_name            = 'lib_common'


#<=====>#
# Assignments Pre
#<=====>#



#<=====>#
# Classes
#<=====>#

class AttrDict(dict):
	def __getattr__(self, item):
		return self[item]
	def __setattr__(self, key, value):
		self[key] = value

#<=====>#

class EmptyObject:
	pass

#<=====>#
class AttrDict(dict):
	def __getattr__(self, item):
		return self[item]
	def __setattr__(self, key, value):
		self[key] = value

#<=====>#
# Functions
#<=====>#

# helpful regexp replace for converting sections of code 
# find: tkn\['(\w+)'\]
# repl: tkn.\1
def AttrDictConv(in_dict=None):
	func_name = 'AttrDictConv'
	out_attr_dict = AttrDict()
	'''
	Returns AttrDict from dict
	If No Dict is provided returns AttrDict
	'''
	try:
		if in_dict:
			if isinstance(in_dict, dict):
				for k in in_dict:
					v = in_dict[k]
					if isinstance(v, dict):
						v = AttrDictConv(v)
					out_attr_dict[k] = v
	except Exception as e:
		print('{} ==> errored... {}'.format(func_name, e))
		traceback.print_exc()
		traceback.print_stack()
		print(type(e))
		print(e)
		print('k : {} ({})'.format(k, type(k)))
		print('v : {} ({})'.format(v, type(v)))
		print('in_dict : ({})'.format(type(in_dict)))
		pprint(in_dict)
		sys.exit()
	return out_attr_dict

#<=====>#

def AttrDictUpd(in_attr_dict=None, in_dict=None):
	func_name = 'AttrDictUpd'
	if in_attr_dict and isinstance(in_attr_dict, AttrDict):
		out_attr_dict = in_attr_dict
	else:
		out_attr_dict = AttrDict()
	'''
	Returns in AttrDict with new keys added from in_dict
	If No Dict is provided returns AttrDict with keys added from in_dict
	'''
	try:
		if in_dict:
			if isinstance(in_dict, dict):
				for k in in_dict:
					v = in_dict[k]
					if isinstance(v, dict):
						v = AttrDictConv(v)
					out_attr_dict[k] = v
	except Exception as e:
		print('{} ==> errored... {}'.format(func_name, e))
		traceback.print_exc()
		traceback.print_stack()
		print(type(e))
		print(e)
		print('k : {} ({})'.format(k, type(k)))
		print('v : {} ({})'.format(v, type(v)))
		print('in_dict : ({})'.format(type(in_dict)))
		pprint(in_dict)
		sys.exit()
	return out_attr_dict

#<=====>#

def dict_of_dicts_sort(d:dict, k:str, typ='float', rev=False):
	sorted_d  = {}
	vals_list = []
	pks_list  = []
	for pk in d:
		val = str(d[pk][k])
		vals_list.append(val)
	sorted_vals_list = sorted(vals_list, reverse=rev)
	for val_tgt in sorted_vals_list:
		if typ == 'float': val_tgt = float(val_tgt)
		if typ == 'str': val_tgt = str(val_tgt)
		if typ == 'int': val_tgt = int(val_tgt)
		for pk in d:
			val = d[pk][k]
			if val == val_tgt:
				pks_list.append(pk)
	for pk in pks_list:
		sorted_d[pk] = d[pk]
	return sorted_d

#<=====>#

def is_even(number: int) -> bool:
	return number % 2 == 0

#<=====>#

def is_odd(number: int) -> bool:
	return number % 2 != 0

#<=====>#

def dec_2_float(in_data):
	func_name = 'dec_2_float'
	'''
	Cycles Through Dict Keys And Converts decimal.Decimal to float
	'''
	try:
		if isinstance(in_data, decimal.Decimal):
			return float(in_data)
		elif isinstance(in_data, list):
			return [dec_2_float(item) for item in in_data]
		elif isinstance(in_data, dict):
			return {key: dec_2_float(value) for key, value in in_data.items()}
		else:
			return in_data
	except Exception as e:
		print('{} ==> errored... {}'.format(func_name, e))
		traceback.print_exc()
		traceback.print_stack()
		print(type(e))
		print(e)
		print('in_data : ({})'.format(type(in_data)))
		pprint(in_data)
		sys.exit()

#<=====>#

def DictKeyValIfElse(in_dict, k, d):
	func_name = 'DictKeyValIfElse'
	'''
	Returns Value If Key Is Present
	Else Returns Default
	'''
	try:
		if k in in_dict:
			v = in_dict[k]
		else:
			v = d
		if not v:
			v = d
	except Exception as e:
		print('{} ==> errored... {}'.format(func_name, e))
		traceback.print_exc()
		traceback.print_stack()
		print(type(e))
		print(e)
		print('k : {} ({})'.format(k, type(k)))
		print('v : {} ({})'.format(v, type(v)))
		print('in_dict : ({})'.format(type(in_dict)))
		pprint(in_dict)
		sys.exit()
	return v

#<=====>#

def DictKeyValFill(in_dict, k, v):
	func_name = 'DictKeyValFill'
	'''
	Builds Key If Absent
	Checks Value of Key
	If No Value, populates with default
	'''
	try:
		if k not in in_dict:
			in_dict[k] = v
		if not DictKeyVal(in_dict, k):
			in_dict[k] = v
	except Exception as e:
		print('{} ==> errored... {}'.format(func_name, e))
		traceback.print_exc()
		traceback.print_stack()
		print(type(e))
		print(e)
		print('k : {} ({})'.format(k, type(k)))
		print('v : {} ({})'.format(v, type(v)))
		print('in_dict : ({})'.format(type(in_dict)))
		pprint(in_dict)
		sys.exit()
	return in_dict[k]

#<=====>#

def DictKeyVal(in_dict, k):
	func_name = 'DictKeyVal'
	'''
	Returns Boolean if key in in_dict and has value using HaveValue function
	'''
	try:
		resp = False
		if k in in_dict:
			if HasVal(in_dict[k]):
				resp = True
	except Exception as e:
		print('{} ==> errored... {}'.format(func_name, e))
		traceback.print_exc()
		traceback.print_stack()
		print(type(e))
		print(e)
		print('k : {} ({})'.format(k, type(k)))
		print('in_dict : ({})'.format(type(in_dict)))
		pprint(in_dict)
		sys.exit()
	return resp

#<=====>#

def DictKeyDel(in_dict, k):
	func_name = 'DictKeyDel'
	'''
	Deletes key if in in_dict
	'''
	try:
		if k in in_dict:
			del in_dict[k]
	except Exception as e:
		print('{} ==> errored... {}'.format(func_name, e))
		traceback.print_exc()
		traceback.print_stack()
		print(type(e))
		print(e)
		print('k : {} ({})'.format(k, type(k)))
		print('in_dict : ({})'.format(type(in_dict)))
		pprint(in_dict)
		sys.exit()
	return in_dict

#<=====>#

def DictKeyValMult(in_dict, ks):
	'''
	Returns Boolean if all key in ks return True using DictKeyVal function
	'''
	resp = True
	for k in ks:
		if k not in in_dict:
			resp = False
			break
		elif not DictKeyVal(in_dict, k):
			resp = False
			break
	return resp

#<=====>#

def DictContainsKeys(in_dict={}, ks=[]):
	'''
	Returns Boolean if all keys in ks are keys in in_dict.
	ks - either a single key or list of keys
	DOES NOT check values of those keys, just if keys are present
	'''
	s = set(ks)
	resp = s.issubset(in_dict.keys())
	return resp

#<=====>#

def DictValCheck(in_dict={}, ks=[], show_yn='N'):
	'''
	Returns Boolean to verify all values in dict have value using HaveValue function
	ks - allows specified keys to be returned
	'''
	if HasVal(ks):
		resp = True
		if isinstance(ks, list):
			for k in ks:
				if k in in_dict:
					v = in_dict[k]
					if not HasVal(v):
						if show_yn == 'Y':
							print('{} : {}'.format(k,v))
						resp=False
				else:
					resp = False
					return resp
		elif isinstance(ks, str):
			if ks in in_dict:
				v = in_dict[ks]
				if not HasVal(v):
					if show_yn == 'Y':
						print('{} : {}'.format(ks,v))
					resp=False
			else:
				resp = False
				return resp
	return resp

#<=====>#

def AllHaveVal(vals=None, itemize_yn='N'):
	'''
	Returns Boolean if all vals have value using HaveValue function
	itemize_yn - prints while validating
	'''
	resp = True
	if isinstance(vals, list):
		for x in vals:
			r = HasVal(x)
			if itemize_yn == 'Y':
				print('r : {}, x : {}'.format(r, x))
			if r is False:
				resp = False
	else:
		resp = HasVal(vals)
	return resp

#<=====>#

def HasVal(val=None):
	'''
	Returns Boolean if val has value (is not null or empty)
	I created this after finding a situation where "if val:" was not working as I had thought
	Now I have forgotten which scenario this was needed for and I over use this in this project
	It was definitely something unique like the response to a function from a web3 contract, post data cleanup...
	'''
	if val is None:
		return False
	elif isinstance(val, str) and len(val) > 0:
		return True
	elif isinstance(val, dict) and len(val) > 0:
		return True
	elif isinstance(val, list) and len(val) > 0:
		return True
	elif isinstance(val, tuple) and len(val) > 0:
		return True
	elif val is not None and val != '':
		return True
	else:
		return False

#<=====>#

def int2tf(val):
	if val == 1:
		val = True
	else:
		val = 0
	return val

#<=====>#

def tf2int(val):
	if val:
		val = int(1)
	else:
		val = int(0)
	return val

#<=====>#

def dec(val):
	if val is None:
		val = decimal.Decimal(0)
	else:
		val = decimal.Decimal(str(val))
	return val

#<=====>#

def dec_prec(number, prec=28):
	with decimal.localcontext() as ctx:
		ctx.prec = prec
		d = decimal.Decimal(number)
		pprint(d)
		return d

#<=====>#

def tf(val):
	if val == 1:
		tf = True
	else:
		tf = False
	return tf

#<=====>#

def dir_val(directory_string):
	"""
	Check if a directory exists. If it doesn't, then create it.
	:param directory_string: The relative directory string (ex: settings/secrets.json)
	:type directory_string: str
	"""
	if not os.path.exists(os.path.dirname(directory_string)):
		try:
			os.makedirs(os.path.dirname(directory_string))
			print("Successfully created '{}' file directory".format(directory_string))
		except OSError as exception:
			if exception.errno != errno.EEXIST:
				raise

#<=====>#

def file_write(fullfilename, msg):
	dir_val(fullfilename)
	with open(fullfilename, 'a') as FileWriter:
		if isinstance(msg, str):
			if msg == '':
				FileWriter.writelines('\n')
			else:
				FileWriter.writelines(dt.now().strftime('%Y-%m-%d %H:%M:%S') + ' ==> ' + msg)
		else:
			FileWriter.writelines(str(dt.now()) + ' ')
			FileWriter.writelines('\n')
			FileWriter.write(pformat(msg))
		FileWriter.writelines('\n')
		FileWriter.close()
	return

#<=====>#

def logit(logname, msg):
	dttm_now = dt.now().strftime('%Y_%m_%d')
	logfile = 'logs/' + dttm_now+ '_' + logname + '.log'

	dir_val(logfile)
	with open(logfile, 'a') as LogWriter:
		if isinstance(msg, str):
			if msg == '':
				LogWriter.writelines('\n')
			else:
				LogWriter.writelines(dt.now().strftime('%Y-%m-%d %H:%M:%S') + ' ==> ' + msg)
		else:
			LogWriter.write(pformat(msg))
		LogWriter.writelines('\n')
		LogWriter.close()

	return

#<=====>#

def json_safe(in_data, depth=0):
	depth += 1
	out_data = in_data

	if isinstance(in_data, list):
		for x in in_data:
			x = json_safe(x, depth)

	elif isinstance(in_data, dict):
		for x in in_data:
			in_data[x] = json_safe(in_data[x], depth)

	elif isinstance(in_data, decimal.Decimal):
		out_data = float(in_data)

	else:
		out_data = in_data

	return out_data

#<=====>#

def json_file_read(directory_string, default_json_content=None):
	"""
	Get the contents of a JSON file. If it doesn't exist,
	create and populate it with specified or default JSON content.
	:param directory_string: The relative directory string (ex: settings/secrets.json)
	:type directory_string: str
	:param default_json_content: The content to populate a non-existing JSON file with
	:type default_json_content: dict, list
	"""
	dir_val(directory_string)
	try:
		with open(directory_string) as file:
			file_content = json.load(file)
			file.close()
			return file_content
	except (IOError, json.decoder.JSONDecodeError):
		with open(directory_string, "w") as file:
			if default_json_content is None:
				default_json_content = {}
			json.dump(default_json_content, file, indent=4)
			file.close()
			return default_json_content

#<=====>#

def json_file_write(directory_string, json_content):
	"""
	Get the contents of a JSON file. If it doesn't exist,
	create and populate it with specified or default JSON content.
	:param directory_string: The relative directory string (ex: settings/secrets.json)
	:type directory_string: str
	:param json_content: The content to populate a non-existing JSON file with
	:type json_content: dict
	"""
	dir_val(directory_string)
	with open(directory_string, "w") as file:
		json.dump(json_content, file, indent=4)
		file.close()

#<=====>#

def dict_2_obj(in_dict, i=0):
	out_obj = EmptyObject()
	for k in in_dict:
		v = in_dict[k]
		print('{} => k : {}, v : ({}) {}'.format('    '*i, k, type(v), v))
		if isinstance(v, dict):
			i += 1
			v = dict_2_obj(v)
		setattr(out_obj, k, v)
	return out_obj

#<=====>#

def ObjAttrGet(in_obj={}, attr='', default=None):
	'''
	Returns an attribute value from object if it HasVal else default
	'''
	resp = default
	if hasattr(in_obj, attr):
		v = getattr(in_obj, attr)
		if HasVal(v):
			resp = v
	return resp

#<=====>#

def temp_timing_begin(func_name, logname='', log_yn='Y', min_yn='N'):
	f = {}
	t0              = time.perf_counter()
	strt_dttm       = dt.now().strftime('%Y-%m-%d %H:%M:%S')
	f['func_name']  = func_name
	f['logname']    = logname
	f['log_yn']     = log_yn
	f['min_yn']     = min_yn
	f['t0']         = t0
	f['strt_dttm']  = strt_dttm
	msg = "{:<50} begins at {}".format(func_name, strt_dttm)
	if log_yn == 'Y': logit(logname, msg)
	if min_yn == 'N': print(msg)
	return f

#<=====>#

def temp_timing_end(f):
	t1 = time.perf_counter()
	end_dttm        = dt.now().strftime('%Y-%m-%d %H:%M:%S')
	t0              = f['t0']
	func_name       = f['func_name']
	logname         = f['logname']
	log_yn          = f['log_yn']
	min_yn          = f['min_yn']
	f['t1']         = t1
	f['end_dttm']   = end_dttm
	secs = round(t1 - t0, 3)
	f['secs']       = secs
	m = "{:<50} completed at {}, taking {:>7.3f} seconds..."
	msg = m.format(func_name, end_dttm, secs)
	if log_yn == 'Y': logit(logname, msg)
	if min_yn != 'Y': print(msg)
	return f

#<=====>#

def temp_timer_begin(nm):
	t = {}
	t['name']  = nm
	t0              = time.perf_counter()
	t['t0']         = t0
	strt_dttm       = dt.now().strftime('%Y-%m-%d %H:%M:%S')
	t['strt_dttm']  = strt_dttm
	msg = "{} begins at {}".format(nm, strt_dttm)
	print(msg)
	return t

#<=====>#

def temp_timer_end(t):

	t1 = time.perf_counter()
	t['t1']         = t1

	end_dttm        = dt.now().strftime('%Y-%m-%d %H:%M:%S')
	t['end_dttm']   = end_dttm

	t0              = t['t0']
	nm              = t['name']

	secs = round(t1 - t0, 3)
	t['secs']       = secs

	m = "{} completed at {}, taking {} seconds..."
	msg = m.format(nm, end_dttm, secs)
	print(msg)

	return t

#<=====>#

def utc_now():
	import datetime
	utc_now = datetime.datetime.now(datetime.UTC)
	return utc_now

#<=====>#

def dttm_get():
	dttm_str = dt.now().strftime('%Y-%m-%d %H:%M:%S')
	return dttm_str

#<=====>#

def dttm_get():
	dttm_str = dt.now().strftime('%Y-%m-%d %H:%M:%S')
	return dttm_str

#<=====>#

def now_utc_get():
	now_utc = dt.now(datetime.timezone.utc)
	return now_utc

#<=====>#

def now_utc_ts_get():
	now_utc_ts = dt.now(datetime.timezone.utc).timestamp()
	return now_utc_ts

#<=====>#

def calc_elapsed(dttm_new, dttm_old, interval='seconds'):
	if interval == 'seconds':
		elapsed = (dttm_new - dttm_old).total_seconds()
	elif interval == 'minutes':
		elapsed = (dttm_new - dttm_old).total_seconds() / 60
	elif interval == 'hours':
		elapsed = (dttm_new - dttm_old).total_seconds() / (60 * 60)
	elif interval == 'days':
		elapsed = (dttm_new - dttm_old).total_seconds() / (60 * 60 * 24)
	return elapsed

#<=====>#

def getRaw(nbr, dec):
	r = int(nbr * 10 ** dec)
	return r

#<=====>#

def get_now():
	now = dt.now().replace(microsecond=0)

	return now

#<=====>#

def dict_upd(d, e, k, v):
	func_name = 'dict_upd'
	func_str = ' * {}.{}(d, e={}, k={}, v={})'.format(lib_name, func_name, e, k, v)
	print(func_str)

	if not e in d: d[e] = {}
	d[e][k] = v

	return d

#<=====>#

def prt_dttm_get():
	prt_dttm    = dt.now().strftime('%Y-%m-%d %H:%M:%S')
	return prt_dttm

#<=====>#

def plogit(logname, epoch, msg=None, printyn='Y', logyn='Y'):
	dttm_now = dt.now().strftime('%Y_%m_%d')
	prt_dttm_now = dt.now().strftime('%Y-%m-%d %H:%M:%S')

	logfile = 'logs/' + dttm_now + '_' + logname + '.log'

	dir_val(logfile)
	with open(logfile, 'a') as LogWriter:
		if isinstance(msg, str):
			if msg == '':
				if printyn == 'Y': print('')
				if logyn == 'Y': LogWriter.writelines('\n')
			else:
				m = '{} ({}) ==> {}'
				fmsg = m.format(prt_dttm_now, epoch, msg)
				if printyn == 'Y': print(fmsg)
				if logyn == 'Y': LogWriter.writelines(fmsg)
		else:
			if printyn == 'Y': print(pformat(msg))
			if logyn == 'Y': LogWriter.write(pformat(msg))
		LogWriter.writelines('\n')
		LogWriter.close()
	return

#<=====>#

def file_write(fullfilename, msg):
	dir_val(fullfilename)
	with open(fullfilename, 'a') as FileWriter:
		if isinstance(msg, str):
			if msg == '':
				FileWriter.writelines('\n')
			else:
				FileWriter.writelines(msg)
		else:
			FileWriter.writelines(str(dt.now()) + ' ')
			FileWriter.writelines('\n')
			FileWriter.write(pformat(msg))
		FileWriter.writelines('\n')
		FileWriter.close()
	return

#<=====>#

def sleep_until(dttm):
	func_name = 'sleep_until'
	func_str = ' * {}.{}(dttm={})'.format(lib_name, func_name, dttm)
	print(func_str)

	cnt = 0

	now = get_now()
	while now <= dttm:
		now = get_now()
		cnt += 1
		time.sleep(1)
#		print(cnt)

#<=====>#

def sleep(sec):
	func_name = 'sleep_until'
	func_str = ' * {}.{}(dttm={})'.format(lib_name, func_name, sec)
	print(func_str)

	time.sleep(sec)

#<=====>#

def print_dict(d):
	func_name = 'print_dict'
	func_str = ' * {}.{}(d)'.format(lib_name, func_name)

	print('')
	print('')
	print(json.dumps(d, indent=4))
	print(d)
	print('')
	print('')

	return


#<=====>#

def print_obj(obj):
	obj_list = {}
	for attr, value in obj.__dict__.items():
		obj_list[attr] = value
	print(obj_list)

#<=====>#

def beep_old():
	frequency = 2500  # Set Frequency To 2500 Hertz
	duration = 1000  # Set Duration To 1000 ms == 1 second
	winsound.Beep(frequency, duration)

#<=====>#

def beep(reps=1):
	for _ in range(0, reps, 1):
		cprint('beep()!!!', 'white', 'on_red')
	play_beep(frequency=2500,duration=1000, reps=reps)

#<=====>#

# def beep_error():
# 	beepy.beep(sound='error')

#<=====>#

def play_beep(frequency=1000, duration=1000, reps=1):
	"""
	Used to play a beep sound
	:param frequency: The frequency of the beep
	:type frequency: int
	:param duration: The duration of the beep
	:type duration: int
	"""
	if winsound is None:
		print(f'play_beep(frequnecy={frequency}, duration={duration}, reps={reps}')
		return
	for _ in range(0, reps, 1):
		winsound.Beep(frequency, duration)

#<=====>#

def play_sw_theme():
	"""
	Used to play the Star Wars theme song
	"""
	if winsound is None:
		print('Sound is off, you are missing SW Theme')
		return
	play_beep(1046, 880)
	play_beep(1567, 880)
	play_beep(1396, 55)
	play_beep(1318, 55)
	play_beep(1174, 55)
	play_beep(2093, 880)
	time.sleep(0.3)
	play_beep(1567, 600)
	play_beep(1396, 55)
	play_beep(1318, 55)
	play_beep(1174, 55)
	play_beep(2093, 880)
	time.sleep(0.3)
	play_beep(1567, 600)
	play_beep(1396, 55)
	play_beep(1318, 55)
	play_beep(1396, 55)
	play_beep(1174, 880)

#<=====>#

def play_sw_imperial_march():
	"""
	Used to play the Star Wars Imperial March song
	"""
	if winsound is None:
		print('Sound is off, you are missing SW Imperial March')
		return
	play_beep(440, 500)
	play_beep(440, 500)
	play_beep(440, 500)
	play_beep(349, 375)
	play_beep(523, 150)
	play_beep(440, 600)
	play_beep(349, 375)
	play_beep(523, 150)
	play_beep(440, 1000)
	time.sleep(0.2)
	play_beep(659, 500)
	play_beep(659, 500)
	play_beep(659, 500)
	play_beep(698, 375)
	play_beep(523, 150)
	play_beep(415, 600)
	play_beep(349, 375)
	play_beep(523, 150)
	play_beep(440, 1000)

#<=====>#

def play_file(f):
	winsound.PlaySound(f, winsound.SND_FILENAME)

#<=====>#

def play_cash():
	print('play_cash()')
	play_file('sounds/cashreg.wav')

#<=====>#

def play_doh():
	print('play_doh()')
	play_file('sounds/DOH!.WAV')

#<=====>#

def play_thunder():
	print('play_thunder()')
	play_file('sounds/thunder.wav')

#<=====>#

def speak(tempmessage):
	print(f'speaking : {tempmessage}...')
	engine = pyttsx3.init()
	voices = engine.getProperty('voices')
	engine.setProperty('voice', voices[0].id)  # changing index changes voices but only 0 and 1 are working here
	engine.setProperty('rate', 120)  # 120 words per minute
	engine.setProperty('volume', 0.9)
	engine.say(tempmessage)
	engine.runAndWait()

#<=====>#

def speak_async(tempmessage):
	with concurrent.futures.ThreadPoolExecutor() as executor:
		future = executor.submit(speak, tempmessage)
		return future

#<=====>#

def func_begin(func_name, func_str, logname, secs_max=0.33):
	fnc = {}
	t0                = time.perf_counter()
	strt_dttm         = dt.now().strftime('%Y-%m-%d %H:%M:%S')
	fnc['func_name']  = func_name
	fnc['func_str']   = func_str
	fnc['logname']    = logname
	fnc['strt_dttm']  = strt_dttm
	fnc['end_dttm']   = None
	fnc['t0']         = t0
	fnc['t1']         = None
	fnc['secs']       = 0
	fnc['secs_max']   = secs_max

	return fnc

#<=====>#

def func_end(fnc):
	t0              = fnc['t0']
	func_name       = fnc['func_name']
	func_str        = fnc['func_str']
	# logname         = fnc['logname']
	secs_max        = fnc['secs_max']
	strt_dttm       = fnc['strt_dttm']
	end_dttm        = dt.now().strftime('%Y-%m-%d %H:%M:%S')
	t1              = time.perf_counter()
	secs            = round(t1 - t0, 3)
	fnc['t1']       = t1
	fnc['end_dttm'] = end_dttm
	fnc['secs']     = secs

	if secs_max >= 0:
		if secs > secs_max:
			msg = f"{func_name:<35} began at {strt_dttm} completed at {end_dttm}, taking {secs} seconds... max : {secs_max} * {func_str}"
			cprint(msg, 'white', 'on_red')

	return fnc

#<=====>#

def print_clickable_link(url, display_text):
	# Use the OSC 8 escape sequence to start the hyperlink
	# Then use the ST escape to stop it.
	print(f'\033]8;;{url}\033\\{display_text}\033]8;;\033\\')

#<=====>#

def print_adv(adv=1):
	while adv > 0:
		adv -= 1
		print('')

#<=====>#

def print_func_name(func_name, adv=0, clr='white', bgclr='on_blue'):
	dttm_str = dttm_get()
	if adv > 0: print_adv(adv)
	s = '{}  ===>  {}'.format(dttm_str, func_name)
	cprint(s, clr, bgclr)

#<=====>#

def print_line(char='-', cnt=10, clr='white', bgclr='on_black'):
	s = char * cnt
	cprint(s, clr, bgclr)

#<=====>#

def print_obj(in_obj):
	#https://pythonexamples.org/convert-python-class-object-to-json/
	jsonStr = json.dumps(in_obj.__dict__)
	print(jsonStr)

#<=====>#

def debug_display_func_name(func_name, debug_show_lvl=0):

	prt_dttm_now = dt.now().strftime('%Y-%m-%d %H:%M:%S')
	m = '{} ==> {}'
	msg = m.format(prt_dttm_now, func_name)
	print(msg)

	return

#<=====>#

def banner_display(e, msg):

	plogit('pcp', e, '')
	plogit('pcp', e, '')
	m = '#<==|===||====|||=== ({}) - {:<20} ===|||====||===|==>#'
	msg = m.format(e, msg)
	plogit('pcp', e, msg)

	return

#<=====>#

def clear_screen():
	if os.name == 'nt':
		os.system('cls')
#	if os.name == 'posix':
#		os.system('clear')

#<=====>#

def section_header(
	txt
	, l=100
	, clr=''
	, bgclr=''
	, before_ln_adv = 2
	, after_ln_adv = 0
	, show_dttm_yn = 'Y'
	, center_yn = 'N'
	):
	func_name = 'section_header(display_text=' + str(txt) +', clr=' + str(clr) +', bgclr=' + str(bgclr) + ')'

	if center_yn == 'Y': txt = txt.center(l)

	if before_ln_adv > 0: pa(before_ln_adv)

	dttm_str = ''
	if show_dttm_yn == 'Y':
		dttm_str = dt.now().strftime('%Y-%m-%d %H:%M:%S') + ' '

	if clr not in ('grey','red','green','yellow','blue','magenta','cyan','white'): clr = ''

	if bgclr not in ('on_grey','on_red','on_green','on_yellow','on_blue','on_magenta','on_cyan','on_white'): bgclr = ''

	if clr != '' and bgclr != '':
		cprint(dttm_str + txt, clr, bgclr)
	elif clr != '':
		cprint(dttm_str + txt, clr)
	else:
		print(dttm_str + txt)

	if after_ln_adv > 0: pa(after_ln_adv)

	return

#<=====>#

def pa(r=1):
	cnt = 0
	while cnt < r:
		print('')
		cnt += 1
	return

#<=====>#

def pb(c='*', l=235, fgclr='', bgclr=''):
	txt = c*l
	if fgclr not in ('grey','red','green','yellow','blue','magenta','cyan','white'): fgclr = ''
	if bgclr not in ('on_grey','on_red','on_green','on_yellow','on_blue','on_magenta','on_cyan','on_white'): bgclr = ''
	if fgclr != '' and bgclr != '':
		cprint(txt, fgclr, bgclr)
	elif fgclr != '':
		cprint(txt, fgclr)
	else:
		print(txt)
	return

#<=====>#
# Assignments Post
#<=====>#



#<=====>#
# Default Run
#<=====>#



#<=====>#
=======
#<=====>#
# Description
#<=====>#



#<=====>#
# Known To Do List
#<=====>#



#<=====>#
# Imports
#<=====>#
from datetime import datetime as dt
from libs.cls_settings import AttrDict
from libs.cls_settings import Settings
from pprint import pformat
from pprint import pprint
from termcolor import cprint
# import beepy
import concurrent.futures
import datetime
import decimal
import errno
import json
import os
import pyttsx3
import pytz
import sys
import time
import traceback
import winsound


#<=====>#
# Variables
#<=====>#
lib_name            = 'lib_common'
log_name            = 'lib_common'


#<=====>#
# Assignments Pre
#<=====>#



#<=====>#
# Classes
#<=====>#

class AttrDict(dict):
	def __getattr__(self, item):
		return self[item]
	def __setattr__(self, key, value):
		self[key] = value

#<=====>#

class EmptyObject:
	pass

#<=====>#
class AttrDict(dict):
	def __getattr__(self, item):
		return self[item]
	def __setattr__(self, key, value):
		self[key] = value

#<=====>#
# Functions
#<=====>#

# helpful regexp replace for converting sections of code 
# find: tkn\['(\w+)'\]
# repl: tkn.\1
def AttrDictConv(in_dict=None):
	func_name = 'AttrDictConv'
	out_attr_dict = AttrDict()
	'''
	Returns AttrDict from dict
	If No Dict is provided returns AttrDict
	'''
	try:
		if in_dict:
			if isinstance(in_dict, dict):
				for k in in_dict:
					v = in_dict[k]
					if isinstance(v, dict):
						v = AttrDictConv(v)
					out_attr_dict[k] = v
	except Exception as e:
		print('{} ==> errored... {}'.format(func_name, e))
		traceback.print_exc()
		traceback.print_stack()
		print(type(e))
		print(e)
		print('k : {} ({})'.format(k, type(k)))
		print('v : {} ({})'.format(v, type(v)))
		print('in_dict : ({})'.format(type(in_dict)))
		pprint(in_dict)
		sys.exit()
	return out_attr_dict

#<=====>#

def AttrDictUpd(in_attr_dict=None, in_dict=None):
	func_name = 'AttrDictUpd'
	if in_attr_dict and isinstance(in_attr_dict, AttrDict):
		out_attr_dict = in_attr_dict
	else:
		out_attr_dict = AttrDict()
	'''
	Returns in AttrDict with new keys added from in_dict
	If No Dict is provided returns AttrDict with keys added from in_dict
	'''
	try:
		if in_dict:
			if isinstance(in_dict, dict):
				for k in in_dict:
					v = in_dict[k]
					if isinstance(v, dict):
						v = AttrDictConv(v)
					out_attr_dict[k] = v
	except Exception as e:
		print('{} ==> errored... {}'.format(func_name, e))
		traceback.print_exc()
		traceback.print_stack()
		print(type(e))
		print(e)
		print('k : {} ({})'.format(k, type(k)))
		print('v : {} ({})'.format(v, type(v)))
		print('in_dict : ({})'.format(type(in_dict)))
		pprint(in_dict)
		sys.exit()
	return out_attr_dict

#<=====>#

def dict_of_dicts_sort(d:dict, k:str, typ='float', rev=False):
	sorted_d  = {}
	vals_list = []
	pks_list  = []
	for pk in d:
		val = str(d[pk][k])
		vals_list.append(val)
	sorted_vals_list = sorted(vals_list, reverse=rev)
	for val_tgt in sorted_vals_list:
		if typ == 'float': val_tgt = float(val_tgt)
		if typ == 'str': val_tgt = str(val_tgt)
		if typ == 'int': val_tgt = int(val_tgt)
		for pk in d:
			val = d[pk][k]
			if val == val_tgt:
				pks_list.append(pk)
	for pk in pks_list:
		sorted_d[pk] = d[pk]
	return sorted_d

#<=====>#

def is_even(number: int) -> bool:
	return number % 2 == 0

#<=====>#

def is_odd(number: int) -> bool:
	return number % 2 != 0

#<=====>#

def dec_2_float(in_data):
	func_name = 'dec_2_float'
	'''
	Cycles Through Dict Keys And Converts decimal.Decimal to float
	'''
	try:
		if isinstance(in_data, decimal.Decimal):
			return float(in_data)
		elif isinstance(in_data, list):
			return [dec_2_float(item) for item in in_data]
		elif isinstance(in_data, dict):
			return {key: dec_2_float(value) for key, value in in_data.items()}
		else:
			return in_data
	except Exception as e:
		print('{} ==> errored... {}'.format(func_name, e))
		traceback.print_exc()
		traceback.print_stack()
		print(type(e))
		print(e)
		print('in_data : ({})'.format(type(in_data)))
		pprint(in_data)
		sys.exit()

#<=====>#

def DictKeyValIfElse(in_dict, k, d):
	func_name = 'DictKeyValIfElse'
	'''
	Returns Value If Key Is Present
	Else Returns Default
	'''
	try:
		if k in in_dict:
			v = in_dict[k]
		else:
			v = d
		if not v:
			v = d
	except Exception as e:
		print('{} ==> errored... {}'.format(func_name, e))
		traceback.print_exc()
		traceback.print_stack()
		print(type(e))
		print(e)
		print('k : {} ({})'.format(k, type(k)))
		print('v : {} ({})'.format(v, type(v)))
		print('in_dict : ({})'.format(type(in_dict)))
		pprint(in_dict)
		sys.exit()
	return v

#<=====>#

def DictKeyValFill(in_dict, k, v):
	func_name = 'DictKeyValFill'
	'''
	Builds Key If Absent
	Checks Value of Key
	If No Value, populates with default
	'''
	try:
		if k not in in_dict:
			in_dict[k] = v
		if not DictKeyVal(in_dict, k):
			in_dict[k] = v
	except Exception as e:
		print('{} ==> errored... {}'.format(func_name, e))
		traceback.print_exc()
		traceback.print_stack()
		print(type(e))
		print(e)
		print('k : {} ({})'.format(k, type(k)))
		print('v : {} ({})'.format(v, type(v)))
		print('in_dict : ({})'.format(type(in_dict)))
		pprint(in_dict)
		sys.exit()
	return in_dict[k]

#<=====>#

def DictKeyVal(in_dict, k):
	func_name = 'DictKeyVal'
	'''
	Returns Boolean if key in in_dict and has value using HaveValue function
	'''
	try:
		resp = False
		if k in in_dict:
			if HasVal(in_dict[k]):
				resp = True
	except Exception as e:
		print('{} ==> errored... {}'.format(func_name, e))
		traceback.print_exc()
		traceback.print_stack()
		print(type(e))
		print(e)
		print('k : {} ({})'.format(k, type(k)))
		print('in_dict : ({})'.format(type(in_dict)))
		pprint(in_dict)
		sys.exit()
	return resp

#<=====>#

def DictKeyDel(in_dict, k):
	func_name = 'DictKeyDel'
	'''
	Deletes key if in in_dict
	'''
	try:
		if k in in_dict:
			del in_dict[k]
	except Exception as e:
		print('{} ==> errored... {}'.format(func_name, e))
		traceback.print_exc()
		traceback.print_stack()
		print(type(e))
		print(e)
		print('k : {} ({})'.format(k, type(k)))
		print('in_dict : ({})'.format(type(in_dict)))
		pprint(in_dict)
		sys.exit()
	return in_dict

#<=====>#

def DictKeyValMult(in_dict, ks):
	'''
	Returns Boolean if all key in ks return True using DictKeyVal function
	'''
	resp = True
	for k in ks:
		if k not in in_dict:
			resp = False
			break
		elif not DictKeyVal(in_dict, k):
			resp = False
			break
	return resp

#<=====>#

def DictContainsKeys(in_dict={}, ks=[]):
	'''
	Returns Boolean if all keys in ks are keys in in_dict.
	ks - either a single key or list of keys
	DOES NOT check values of those keys, just if keys are present
	'''
	s = set(ks)
	resp = s.issubset(in_dict.keys())
	return resp

#<=====>#

def DictValCheck(in_dict={}, ks=[], show_yn='N'):
	'''
	Returns Boolean to verify all values in dict have value using HaveValue function
	ks - allows specified keys to be returned
	'''
	if HasVal(ks):
		resp = True
		if isinstance(ks, list):
			for k in ks:
				if k in in_dict:
					v = in_dict[k]
					if not HasVal(v):
						if show_yn == 'Y':
							print('{} : {}'.format(k,v))
						resp=False
				else:
					resp = False
					return resp
		elif isinstance(ks, str):
			if ks in in_dict:
				v = in_dict[ks]
				if not HasVal(v):
					if show_yn == 'Y':
						print('{} : {}'.format(ks,v))
					resp=False
			else:
				resp = False
				return resp
	return resp

#<=====>#

def AllHaveVal(vals=None, itemize_yn='N'):
	'''
	Returns Boolean if all vals have value using HaveValue function
	itemize_yn - prints while validating
	'''
	resp = True
	if isinstance(vals, list):
		for x in vals:
			r = HasVal(x)
			if itemize_yn == 'Y':
				print('r : {}, x : {}'.format(r, x))
			if r is False:
				resp = False
	else:
		resp = HasVal(vals)
	return resp

#<=====>#

def HasVal(val=None):
	'''
	Returns Boolean if val has value (is not null or empty)
	I created this after finding a situation where "if val:" was not working as I had thought
	Now I have forgotten which scenario this was needed for and I over use this in this project
	It was definitely something unique like the response to a function from a web3 contract, post data cleanup...
	'''
	if val is None:
		return False
	elif isinstance(val, str) and len(val) > 0:
		return True
	elif isinstance(val, dict) and len(val) > 0:
		return True
	elif isinstance(val, list) and len(val) > 0:
		return True
	elif isinstance(val, tuple) and len(val) > 0:
		return True
	elif val is not None and val != '':
		return True
	else:
		return False

#<=====>#

def int2tf(val):
	if val == 1:
		val = True
	else:
		val = 0
	return val

#<=====>#

def tf2int(val):
	if val:
		val = int(1)
	else:
		val = int(0)
	return val

#<=====>#

def dec(val):
	if val is None:
		val = decimal.Decimal(0)
	else:
		val = decimal.Decimal(str(val))
	return val

#<=====>#

def dec_prec(number, prec=28):
	with decimal.localcontext() as ctx:
		ctx.prec = prec
		d = decimal.Decimal(number)
		pprint(d)
		return d

#<=====>#

def tf(val):
	if val == 1:
		tf = True
	else:
		tf = False
	return tf

#<=====>#

def dir_val(directory_string):
	"""
	Check if a directory exists. If it doesn't, then create it.
	:param directory_string: The relative directory string (ex: settings/secrets.json)
	:type directory_string: str
	"""
	if not os.path.exists(os.path.dirname(directory_string)):
		try:
			os.makedirs(os.path.dirname(directory_string))
			print("Successfully created '{}' file directory".format(directory_string))
		except OSError as exception:
			if exception.errno != errno.EEXIST:
				raise

#<=====>#

def file_write(fullfilename, msg):
	dir_val(fullfilename)
	with open(fullfilename, 'a') as FileWriter:
		if isinstance(msg, str):
			if msg == '':
				FileWriter.writelines('\n')
			else:
				FileWriter.writelines(dt.now().strftime('%Y-%m-%d %H:%M:%S') + ' ==> ' + msg)
		else:
			FileWriter.writelines(str(dt.now()) + ' ')
			FileWriter.writelines('\n')
			FileWriter.write(pformat(msg))
		FileWriter.writelines('\n')
		FileWriter.close()
	return

#<=====>#

def logit(logname, msg):
	dttm_now = dt.now().strftime('%Y_%m_%d')
	logfile = 'logs/' + dttm_now+ '_' + logname + '.log'

	dir_val(logfile)
	with open(logfile, 'a') as LogWriter:
		if isinstance(msg, str):
			if msg == '':
				LogWriter.writelines('\n')
			else:
				LogWriter.writelines(dt.now().strftime('%Y-%m-%d %H:%M:%S') + ' ==> ' + msg)
		else:
			LogWriter.write(pformat(msg))
		LogWriter.writelines('\n')
		LogWriter.close()

	return

#<=====>#

def json_safe(in_data, depth=0):
	depth += 1
	out_data = in_data

	if isinstance(in_data, list):
		for x in in_data:
			x = json_safe(x, depth)

	elif isinstance(in_data, dict):
		for x in in_data:
			in_data[x] = json_safe(in_data[x], depth)

	elif isinstance(in_data, decimal.Decimal):
		out_data = float(in_data)

	else:
		out_data = in_data

	return out_data

#<=====>#

def json_file_read(directory_string, default_json_content=None):
	"""
	Get the contents of a JSON file. If it doesn't exist,
	create and populate it with specified or default JSON content.
	:param directory_string: The relative directory string (ex: settings/secrets.json)
	:type directory_string: str
	:param default_json_content: The content to populate a non-existing JSON file with
	:type default_json_content: dict, list
	"""
	dir_val(directory_string)
	try:
		with open(directory_string) as file:
			file_content = json.load(file)
			file.close()
			return file_content
	except (IOError, json.decoder.JSONDecodeError):
		with open(directory_string, "w") as file:
			if default_json_content is None:
				default_json_content = {}
			json.dump(default_json_content, file, indent=4)
			file.close()
			return default_json_content

#<=====>#

def json_file_write(directory_string, json_content):
	"""
	Get the contents of a JSON file. If it doesn't exist,
	create and populate it with specified or default JSON content.
	:param directory_string: The relative directory string (ex: settings/secrets.json)
	:type directory_string: str
	:param json_content: The content to populate a non-existing JSON file with
	:type json_content: dict
	"""
	dir_val(directory_string)
	with open(directory_string, "w") as file:
		json.dump(json_content, file, indent=4)
		file.close()

#<=====>#

def dict_2_obj(in_dict, i=0):
	out_obj = EmptyObject()
	for k in in_dict:
		v = in_dict[k]
		print('{} => k : {}, v : ({}) {}'.format('    '*i, k, type(v), v))
		if isinstance(v, dict):
			i += 1
			v = dict_2_obj(v)
		setattr(out_obj, k, v)
	return out_obj

#<=====>#

def ObjAttrGet(in_obj={}, attr='', default=None):
	'''
	Returns an attribute value from object if it HasVal else default
	'''
	resp = default
	if hasattr(in_obj, attr):
		v = getattr(in_obj, attr)
		if HasVal(v):
			resp = v
	return resp

#<=====>#

def temp_timing_begin(func_name, logname='', log_yn='Y', min_yn='N'):
	f = {}
	t0              = time.perf_counter()
	strt_dttm       = dt.now().strftime('%Y-%m-%d %H:%M:%S')
	f['func_name']  = func_name
	f['logname']    = logname
	f['log_yn']     = log_yn
	f['min_yn']     = min_yn
	f['t0']         = t0
	f['strt_dttm']  = strt_dttm
	msg = "{:<50} begins at {}".format(func_name, strt_dttm)
	if log_yn == 'Y': logit(logname, msg)
	if min_yn == 'N': print(msg)
	return f

#<=====>#

def temp_timing_end(f):
	t1 = time.perf_counter()
	end_dttm        = dt.now().strftime('%Y-%m-%d %H:%M:%S')
	t0              = f['t0']
	func_name       = f['func_name']
	logname         = f['logname']
	log_yn          = f['log_yn']
	min_yn          = f['min_yn']
	f['t1']         = t1
	f['end_dttm']   = end_dttm
	secs = round(t1 - t0, 3)
	f['secs']       = secs
	m = "{:<50} completed at {}, taking {:>7.3f} seconds..."
	msg = m.format(func_name, end_dttm, secs)
	if log_yn == 'Y': logit(logname, msg)
	if min_yn != 'Y': print(msg)
	return f

#<=====>#

def temp_timer_begin(nm):
	t = {}
	t['name']  = nm
	t0              = time.perf_counter()
	t['t0']         = t0
	strt_dttm       = dt.now().strftime('%Y-%m-%d %H:%M:%S')
	t['strt_dttm']  = strt_dttm
	msg = "{} begins at {}".format(nm, strt_dttm)
	print(msg)
	return t

#<=====>#

def temp_timer_end(t):

	t1 = time.perf_counter()
	t['t1']         = t1

	end_dttm        = dt.now().strftime('%Y-%m-%d %H:%M:%S')
	t['end_dttm']   = end_dttm

	t0              = t['t0']
	nm              = t['name']

	secs = round(t1 - t0, 3)
	t['secs']       = secs

	m = "{} completed at {}, taking {} seconds..."
	msg = m.format(nm, end_dttm, secs)
	print(msg)

	return t

#<=====>#

def utc_now():
	import datetime
	utc_now = datetime.datetime.now(datetime.UTC)
	return utc_now

#<=====>#

def dttm_get():
	dttm_str = dt.now().strftime('%Y-%m-%d %H:%M:%S')
	return dttm_str

#<=====>#

def dttm_get():
	dttm_str = dt.now().strftime('%Y-%m-%d %H:%M:%S')
	return dttm_str

#<=====>#

def now_utc_get():
	now_utc = dt.now(datetime.timezone.utc)
	return now_utc

#<=====>#

def now_utc_ts_get():
	now_utc_ts = dt.now(datetime.timezone.utc).timestamp()
	return now_utc_ts

#<=====>#

def calc_elapsed(dttm_new, dttm_old, interval='seconds'):
	if interval == 'seconds':
		elapsed = (dttm_new - dttm_old).total_seconds()
	elif interval == 'minutes':
		elapsed = (dttm_new - dttm_old).total_seconds() / 60
	elif interval == 'hours':
		elapsed = (dttm_new - dttm_old).total_seconds() / (60 * 60)
	elif interval == 'days':
		elapsed = (dttm_new - dttm_old).total_seconds() / (60 * 60 * 24)
	return elapsed

#<=====>#

def getRaw(nbr, dec):
	r = int(nbr * 10 ** dec)
	return r

#<=====>#

def get_now():
	now = dt.now().replace(microsecond=0)

	return now

#<=====>#

def dict_upd(d, e, k, v):
	func_name = 'dict_upd'
	func_str = ' * {}.{}(d, e={}, k={}, v={})'.format(lib_name, func_name, e, k, v)
	print(func_str)

	if not e in d: d[e] = {}
	d[e][k] = v

	return d

#<=====>#

def prt_dttm_get():
	prt_dttm    = dt.now().strftime('%Y-%m-%d %H:%M:%S')
	return prt_dttm

#<=====>#

def plogit(logname, epoch, msg=None, printyn='Y', logyn='Y'):
	dttm_now = dt.now().strftime('%Y_%m_%d')
	prt_dttm_now = dt.now().strftime('%Y-%m-%d %H:%M:%S')

	logfile = 'logs/' + dttm_now + '_' + logname + '.log'

	dir_val(logfile)
	with open(logfile, 'a') as LogWriter:
		if isinstance(msg, str):
			if msg == '':
				if printyn == 'Y': print('')
				if logyn == 'Y': LogWriter.writelines('\n')
			else:
				m = '{} ({}) ==> {}'
				fmsg = m.format(prt_dttm_now, epoch, msg)
				if printyn == 'Y': print(fmsg)
				if logyn == 'Y': LogWriter.writelines(fmsg)
		else:
			if printyn == 'Y': print(pformat(msg))
			if logyn == 'Y': LogWriter.write(pformat(msg))
		LogWriter.writelines('\n')
		LogWriter.close()
	return

#<=====>#

def file_write(fullfilename, msg):
	dir_val(fullfilename)
	with open(fullfilename, 'a') as FileWriter:
		if isinstance(msg, str):
			if msg == '':
				FileWriter.writelines('\n')
			else:
				FileWriter.writelines(msg)
		else:
			FileWriter.writelines(str(dt.now()) + ' ')
			FileWriter.writelines('\n')
			FileWriter.write(pformat(msg))
		FileWriter.writelines('\n')
		FileWriter.close()
	return

#<=====>#

def sleep_until(dttm):
	func_name = 'sleep_until'
	func_str = ' * {}.{}(dttm={})'.format(lib_name, func_name, dttm)
	print(func_str)

	cnt = 0

	now = get_now()
	while now <= dttm:
		now = get_now()
		cnt += 1
		time.sleep(1)
#		print(cnt)

#<=====>#

def sleep(sec):
	func_name = 'sleep_until'
	func_str = ' * {}.{}(dttm={})'.format(lib_name, func_name, sec)
	print(func_str)

	time.sleep(sec)

#<=====>#

def print_dict(d):
	func_name = 'print_dict'
	func_str = ' * {}.{}(d)'.format(lib_name, func_name)

	print('')
	print('')
	print(json.dumps(d, indent=4))
	print(d)
	print('')
	print('')

	return


#<=====>#

def print_obj(obj):
	obj_list = {}
	for attr, value in obj.__dict__.items():
		obj_list[attr] = value
	print(obj_list)

#<=====>#

def beep_old():
	frequency = 2500  # Set Frequency To 2500 Hertz
	duration = 1000  # Set Duration To 1000 ms == 1 second
	winsound.Beep(frequency, duration)

#<=====>#

def beep(reps=1):
	for _ in range(0, reps, 1):
		cprint('beep()!!!', 'white', 'on_red')
	play_beep(frequency=2500,duration=1000, reps=reps)

#<=====>#

# def beep_error():
# 	beepy.beep(sound='error')

#<=====>#

def play_beep(frequency=1000, duration=1000, reps=1):
	"""
	Used to play a beep sound
	:param frequency: The frequency of the beep
	:type frequency: int
	:param duration: The duration of the beep
	:type duration: int
	"""
	if winsound is None:
		print(f'play_beep(frequnecy={frequency}, duration={duration}, reps={reps}')
		return
	for _ in range(0, reps, 1):
		winsound.Beep(frequency, duration)

#<=====>#

def play_sw_theme():
	"""
	Used to play the Star Wars theme song
	"""
	if winsound is None:
		print('Sound is off, you are missing SW Theme')
		return
	play_beep(1046, 880)
	play_beep(1567, 880)
	play_beep(1396, 55)
	play_beep(1318, 55)
	play_beep(1174, 55)
	play_beep(2093, 880)
	time.sleep(0.3)
	play_beep(1567, 600)
	play_beep(1396, 55)
	play_beep(1318, 55)
	play_beep(1174, 55)
	play_beep(2093, 880)
	time.sleep(0.3)
	play_beep(1567, 600)
	play_beep(1396, 55)
	play_beep(1318, 55)
	play_beep(1396, 55)
	play_beep(1174, 880)

#<=====>#

def play_sw_imperial_march():
	"""
	Used to play the Star Wars Imperial March song
	"""
	if winsound is None:
		print('Sound is off, you are missing SW Imperial March')
		return
	play_beep(440, 500)
	play_beep(440, 500)
	play_beep(440, 500)
	play_beep(349, 375)
	play_beep(523, 150)
	play_beep(440, 600)
	play_beep(349, 375)
	play_beep(523, 150)
	play_beep(440, 1000)
	time.sleep(0.2)
	play_beep(659, 500)
	play_beep(659, 500)
	play_beep(659, 500)
	play_beep(698, 375)
	play_beep(523, 150)
	play_beep(415, 600)
	play_beep(349, 375)
	play_beep(523, 150)
	play_beep(440, 1000)

#<=====>#

def play_file(f):
	winsound.PlaySound(f, winsound.SND_FILENAME)

#<=====>#

def play_cash():
	print('play_cash()')
	play_file('sounds/cashreg.wav')

#<=====>#

def play_doh():
	print('play_doh()')
	play_file('sounds/DOH!.WAV')

#<=====>#

def play_thunder():
	print('play_thunder()')
	play_file('sounds/thunder.wav')

#<=====>#

def speak(tempmessage):
	print(f'speaking : {tempmessage}...')
	engine = pyttsx3.init()
	voices = engine.getProperty('voices')
	engine.setProperty('voice', voices[0].id)  # changing index changes voices but only 0 and 1 are working here
	engine.setProperty('rate', 120)  # 120 words per minute
	engine.setProperty('volume', 0.9)
	engine.say(tempmessage)
	engine.runAndWait()

#<=====>#

def speak_async(tempmessage):
	with concurrent.futures.ThreadPoolExecutor() as executor:
		future = executor.submit(speak, tempmessage)
		return future

#<=====>#

def func_begin(func_name, func_str, logname, secs_max=0.33):
	fnc = {}
	t0                = time.perf_counter()
	strt_dttm         = dt.now().strftime('%Y-%m-%d %H:%M:%S')
	fnc['func_name']  = func_name
	fnc['func_str']   = func_str
	fnc['logname']    = logname
	fnc['strt_dttm']  = strt_dttm
	fnc['end_dttm']   = None
	fnc['t0']         = t0
	fnc['t1']         = None
	fnc['secs']       = 0
	fnc['secs_max']   = secs_max

	return fnc

#<=====>#

def func_end(fnc):
	t0              = fnc['t0']
	func_name       = fnc['func_name']
	func_str        = fnc['func_str']
	# logname         = fnc['logname']
	secs_max        = fnc['secs_max']
	strt_dttm       = fnc['strt_dttm']
	end_dttm        = dt.now().strftime('%Y-%m-%d %H:%M:%S')
	t1              = time.perf_counter()
	secs            = round(t1 - t0, 3)
	fnc['t1']       = t1
	fnc['end_dttm'] = end_dttm
	fnc['secs']     = secs

	if secs_max >= 0:
		if secs > secs_max:
			msg = f"{func_name:<35} began at {strt_dttm} completed at {end_dttm}, taking {secs} seconds... max : {secs_max} * {func_str}"
			cprint(msg, 'white', 'on_red')

	return fnc

#<=====>#

def print_clickable_link(url, display_text):
	# Use the OSC 8 escape sequence to start the hyperlink
	# Then use the ST escape to stop it.
	print(f'\033]8;;{url}\033\\{display_text}\033]8;;\033\\')

#<=====>#

def print_adv(adv=1):
	while adv > 0:
		adv -= 1
		print('')

#<=====>#

def print_func_name(func_name, adv=0, clr='white', bgclr='on_blue'):
	dttm_str = dttm_get()
	if adv > 0: print_adv(adv)
	s = '{}  ===>  {}'.format(dttm_str, func_name)
	cprint(s, clr, bgclr)

#<=====>#

def print_line(char='-', cnt=10, clr='white', bgclr='on_black'):
	s = char * cnt
	cprint(s, clr, bgclr)

#<=====>#

def print_obj(in_obj):
	#https://pythonexamples.org/convert-python-class-object-to-json/
	jsonStr = json.dumps(in_obj.__dict__)
	print(jsonStr)

#<=====>#

def debug_display_func_name(func_name, debug_show_lvl=0):

	prt_dttm_now = dt.now().strftime('%Y-%m-%d %H:%M:%S')
	m = '{} ==> {}'
	msg = m.format(prt_dttm_now, func_name)
	print(msg)

	return

#<=====>#

def banner_display(e, msg):

	plogit('pcp', e, '')
	plogit('pcp', e, '')
	m = '#<==|===||====|||=== ({}) - {:<20} ===|||====||===|==>#'
	msg = m.format(e, msg)
	plogit('pcp', e, msg)

	return

#<=====>#

def clear_screen():
	if os.name == 'nt':
		os.system('cls')
#	if os.name == 'posix':
#		os.system('clear')

#<=====>#

def section_header(
	txt
	, l=100
	, clr=''
	, bgclr=''
	, before_ln_adv = 2
	, after_ln_adv = 0
	, show_dttm_yn = 'Y'
	, center_yn = 'N'
	):
	func_name = 'section_header(display_text=' + str(txt) +', clr=' + str(clr) +', bgclr=' + str(bgclr) + ')'

	if center_yn == 'Y': txt = txt.center(l)

	if before_ln_adv > 0: pa(before_ln_adv)

	dttm_str = ''
	if show_dttm_yn == 'Y':
		dttm_str = dt.now().strftime('%Y-%m-%d %H:%M:%S') + ' '

	if clr not in ('grey','red','green','yellow','blue','magenta','cyan','white'): clr = ''

	if bgclr not in ('on_grey','on_red','on_green','on_yellow','on_blue','on_magenta','on_cyan','on_white'): bgclr = ''

	if clr != '' and bgclr != '':
		cprint(dttm_str + txt, clr, bgclr)
	elif clr != '':
		cprint(dttm_str + txt, clr)
	else:
		print(dttm_str + txt)

	if after_ln_adv > 0: pa(after_ln_adv)

	return

#<=====>#

def pa(r=1):
	cnt = 0
	while cnt < r:
		print('')
		cnt += 1
	return

#<=====>#

def pb(c='*', l=235, fgclr='', bgclr=''):
	txt = c*l
	if fgclr not in ('grey','red','green','yellow','blue','magenta','cyan','white'): fgclr = ''
	if bgclr not in ('on_grey','on_red','on_green','on_yellow','on_blue','on_magenta','on_cyan','on_white'): bgclr = ''
	if fgclr != '' and bgclr != '':
		cprint(txt, fgclr, bgclr)
	elif fgclr != '':
		cprint(txt, fgclr)
	else:
		print(txt)
	return

#<=====>#
# Assignments Post
#<=====>#



#<=====>#
# Default Run
#<=====>#



#<=====>#
>>>>>>> Stashed changes
