#All functions modified from https://github.com/PyMySQL/PyMySQL/blob/master/pymysql/
#This is all modified to my specific needs, sorry if it gives you any form of sickness.
from pymysql.converters import encoders
from pymysql.converters import _escape_unicode as escape_string
from pymysql.charset import charset_by_name
from functools import partial

encoding = charset_by_name('utf8mb4').encoding

def literal(obj):
	return escape(obj, encoders)

def _ensure_bytes(x, encoding=None):
	if isinstance(x, str):
		x = x.encode(encoding)
	elif isinstance(x, (tuple, list)):
		x = type(x)(_ensure_bytes(v, encoding=encoding) for v in x)
	return x

def _escape_args(args):
	ensure_bytes = partial(_ensure_bytes, encoding=encoding)
	if isinstance(args, (tuple, list)):
		return tuple(literal(arg) for arg in args)
	elif isinstance(args, dict):
		return dict((key, literal(val)) for (key, val) in args.items())
	else:
		return escape(args)

def escape(obj, mapping=None):
	if isinstance(obj, str):
		return "'" + escape_string(obj) + "'"
	return escape_item(obj, self.charset, mapping=mapping)

def escape_item(val, charset, mapping=None):
	if mapping is None:
		mapping = encoders
	encoder = mapping.get(type(val))
	if not encoder:
		try:
			encoder = mapping[text_type]
		except KeyError:
			raise TypeError("no default type converter defined")
	if encoder in (escape_dict, escape_sequence):
		val = encoder(val, charset, mapping)
	else:
		val = encoder(val, mapping)
	return val