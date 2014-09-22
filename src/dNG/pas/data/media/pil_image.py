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

# pylint: disable=duplicate-key,import-error,no-name-in-module

from os import path
from PIL import Image

try: from urllib.parse import unquote, urlsplit
except ImportError:
#
	from urllib import unquote
	from urlparse import urlsplit
#

from dNG.pas.runtime.exception_log_trap import ExceptionLogTrap
from dNG.pas.runtime.io_exception import IOException
from dNG.pas.runtime.not_implemented_exception import NotImplementedException
from dNG.pas.runtime.value_exception import ValueException
from .abstract_image import AbstractImage
from .pil_image_metadata import PilImageMetadata

# See PIL libImaging/unpack.c 2013/10/01
_PIL_MODES = { "1": 1, # bilevel
               "1;I": 1,
               "1;R": 1,
               "1;IR": 1,

               # greyscale
               "L;2": 2,
               "L;4": 4,
               "L": 8,
               "L;I": 8,
               "L;R": 8,
               "L;16": 16,
               "L;16B": 16,

               # greyscale w. alpha
               "LA": 16,
               "LA;L": 16,

               # palette
               "P;1": 1,
               "P;2": 2,
               "P;2L": 2,
               "P;4": 4,
               "P;4L": 4,
               "P": 8,
               "P;R": 8,

               # palette w. alpha
               "PA": 16,
               "PA;L": 16,

               # true colour
               "RGB": 24,
               "RGB;L": 24,
               "RGB;R": 24,
               "RGB;16B": 48,
               "BGR": 24,
               "BGR;15": 16,
               "BGR;16": 16,
               "BGR;5": 16,
               "RGBX": 32,
               "RGBX;L": 32,
               "BGRX": 32,
               "XRGB": 24,
               "XBGR": 32,
               "YCC;P": 24,
               "R": 8,
               "G": 8,
               "B": 8,

               # true colour w. alpha
               "LA": 16,
               "LA;16B": 32,
               "RGBA": 32,
               "RGBa": 32,
               "RGBA;I": 32,
               "RGBA;L": 32,
               "RGBA;16B": 64,
               "BGRA": 32,
               "ARGB": 32,
               "ABGR": 32,
               "YCCA;P": 32,
               "R": 8,
               "G": 8,
               "B": 8,
               "A": 8,

               # true colour w. padding
               "RGB": 24,
               "RGB;L": 24,
               "RGB;16B": 48,
               "BGR": 24,
               "BGR;15": 16,
               "BGR;16": 16,
               "BGR;5": 16,
               "RGBX": 32,
               "RGBX;L": 32,
               "BGRX": 32,
               "XRGB": 24,
               "XBGR": 32,
               "YCC;P": 24,
               "R": 8,
               "G": 8,
               "B": 8,
               "X": 8,

               # colour separation
               "CMYK": 32,
               "CMYK;I": 32,
               "CMYK;L": 32,
               "C": 8,
               "M": 8,
               "Y": 8,
               "K": 8,
               "C;I": 8,
               "M;I": 8,
               "Y;I": 8,
               "K;I": 8,

               # video (YCbCr)
               "YCbCr": 24,
               "YCbCr;L": 24,
               "YCbCrX": 32,
               "YCbCrK": 32,

               # integer variations
               "I": 32,
               "I;8": 8,
               "I;8S": 8,
               "I;16": 16,
               "I;16S": 16,
               "I;16B": 16,
               "I;16BS": 16,
               "I;16N": 16,
               "I;16NS": 16,
               "I;32": 32,
               "I;32S": 32,
               "I;32B": 32,
               "I;32BS": 32,
               "I;32N": 32,
               "I;32NS": 32,

               # floating point variations
               "F": 32,
               "F;8": 8,
               "F;8S": 8,
               "F;16": 16,
               "F;16S": 16,
               "F;16B": 16,
               "F;16BS": 16,
               "F;16N": 16,
               "F;16NS": 16,
               "F;32": 32,
               "F;32S": 32,
               "F;32B": 32,
               "F;32BS": 32,
               "F;32N": 32,
               "F;32NS": 32,
               "F;32F": 32,
               "F;32BF": 32,
               "F;32NF": 32,
               "F;64F": 64,
               "F;64BF": 64,
               "F;64NF": 64,

               # storage modes
               "I;16": 16,
               "I;16B": 16,
               "I;16L": 16
             }

class PilImage(AbstractImage):
#
	"""
PIL implementation of the image class.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: imaging
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;gpl
             GNU General Public License 2
	"""

	def __init__(self):
	#
		"""
Constructor __init__(PilImage)

:since: v0.1.00
		"""

		AbstractImage.__init__(self)

		self.metadata = None
		"""
Cached metadata instance
		"""
	#

	def copy(self, file_pathname):
	#
		"""
Creates a copy of the image converting it to match the file extension if
needed.

:param file_pathname: Image file path and name

:return: (bool) True on success
:since:  v0.1.00
		"""

		if (self.image == None): raise IOException("Invalid image state")

		raise NotImplementedException()
	#

	def get_metadata(self):
	#
		"""
Return the metadata for this URL.

:return: (object) Metadata object
:since:  v0.1.00
		"""

		# pylint: disable=protected-access

		if (self.metadata == None):
		#
			if (self.image.mode not in _PIL_MODES): raise ValueException("Unknown PIL image mode returned")

			exif_data = (self.image._getexif() if (hasattr(self.image, "_getexif")) else None)

			self.metadata = PilImageMetadata("file:///{0}".format(self.file_pathname),
			                                 exif_data,
			                                 width = self.image.size[0],
			                                 height = self.image.size[1],
			                                 bpp = _PIL_MODES[self.image.mode]
			                                )
		#

		return self.metadata
	#

	def open_url(self, url):
	#
		"""
Initializes an media instance for the given URL.

:param url: URL

:return: (bool) True on success
:since:  v0.1.00
		"""

		_return = False

		self.image = None
		self.metadata = None

		url_elements = urlsplit(url)
		file_pathname = path.normpath(unquote(url_elements.path[1:]))

		with ExceptionLogTrap("pas_media"):
		#
			self.image = Image.open(file_pathname, "r")
			self.file_pathname = file_pathname

			_return = True
		#

		return _return
	#

	def save(self):
	#
		"""
Saves the image if changed.

:return: (bool) True on success
:since:  v0.1.00
		"""

		return False
	#

	def set_resize_mode(self, mode):
	#
		"""
Sets the resize mode.

:param mode: Resize mode

:since: v0.1.00
		"""

		self.resize_mode = mode
	#

	def set_size(self, width, height):
	#
		"""
Sets the image size (and resizes it).

:param width: Image width
:param height: Image height

:since: v0.1.00
		"""

		raise NotImplementedException()
	#
#

##j## EOF