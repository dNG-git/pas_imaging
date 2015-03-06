# -*- coding: utf-8 -*-
##j## BOF

"""
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?pas;imaging

The following license agreement remains valid unless any additions or
changes are being made by direct Netware Group in a written form.

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 2 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc.,
59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;gpl
----------------------------------------------------------------------------
#echo(pasImagingVersion)#
#echo(__FILEPATH__)#
"""

from codecs import getdecoder
import re

from dNG.pas.data.binary import Binary
from dNG.pas.data.text.input_filter import InputFilter

class Exif(object):
#
	"""
This class contains static Exif parsing helper functions.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: imaging
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;gpl
             GNU General Public License 2
	"""


	ARTIST = 0x013b
	"""
Exif artist tag
	"""
	COPYRIGHT = 0x8298
	"""
Exif copyright tag
	"""
	DESCRIPTION = 0x010e
	"""
Exif description tag
	"""
	DEVICE_VENDOR = 0x010f
	"""
Exif device vendor tag
	"""
	DEVICE_MODEL = 0x0110
	"""
Exif device model tag
	"""
	IMAGE_ORIENTATION = 0x0112
	"""
Exif image orientation tag
	"""
	IMAGE_ORIENTATION_90 = 0x8
	"""
Exif image orientation rotated 90°
	"""
	IMAGE_ORIENTATION_180 = 0x3
	"""
Exif image orientation rotated 180°
	"""
	IMAGE_ORIENTATION_270 = 0x6
	"""
Exif image orientation rotated 270°
	"""
	SOFTWARE = 0x0131
	"""
Exif software tag
	"""
	USER_COMMENT = 0x9286
	"""
Exif user comment tag
	"""

	@staticmethod
	def filter_ascii(data):
	#
		"""
Filter a Exif ASCII string and strip whitespace characters from the
beginning and end of the string.

:param data: Raw data

:return: (str) Filtered data
:since:  v0.1.00
		"""

		return InputFilter.filter_control_chars(data).strip()
	#

	@staticmethod
	def filter_typed_string(data):
	#
		"""
Filter a typed Exif string and strip whitespace characters from the
beginning and end of the string.

:param data: Raw data

:return: (str) Filtered data
:since:  v0.1.00
		"""

		if (data is not None and len(data) >= 8):
		#
			if (Binary.str(data[:8]) == "ASCII\x00\x00\x00"): stripped_ascii = data[8:]
			elif (re.match("ASCII\\w", Binary.str(data[:6]))): stripped_ascii = data[5:]
			else: stripped_ascii = None

			if (stripped_ascii is not None):
			#
				if (stripped_ascii.isalnum()): data = stripped_ascii
				else:
				#
					py_decode = getdecoder("latin_1")
					data = py_decode(stripped_ascii)[0]
				#
			#
			elif (data[:8] == "UNICODE\x00"): data = data[8:]
			elif (re.match("UNICODE\\w", Binary.str(data[:8]))): data = data[7:]
		#

		return InputFilter.filter_control_chars(data).strip()
	#
#

##j## EOF