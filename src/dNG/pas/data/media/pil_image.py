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
from PIL import Image, ImageOps
from tempfile import TemporaryFile

try: from urllib.parse import unquote, urlsplit
except ImportError:
#
	from urllib import unquote
	from urlparse import urlsplit
#

from dNG.data.file import File
from dNG.pas.data.text.input_filter import InputFilter
from dNG.pas.runtime.exception_log_trap import ExceptionLogTrap
from dNG.pas.runtime.io_exception import IOException
from dNG.pas.runtime.type_exception import TypeException
from dNG.pas.runtime.value_exception import ValueException
from .abstract_image import AbstractImage
from .exif import Exif
from .pil_image_metadata import PilImageMetadata

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

	PIL_COLORMAPS = { "image/bmp": ( { "constant": AbstractImage.COLORMAP_PALETTE,
	                                   "depth": 8,
	                                   "pil_mode": "P"
	                                 },
	                                 { "constant": AbstractImage.COLORMAP_RGB,
	                                   "depth": 24,
	                                   "pil_mode": "RGB"
	                                 }
	                               ),
	                  "image/jpeg": ( { "constant": AbstractImage.COLORMAP_CMYK,
	                                    "depth": 32,
	                                    "pil_mode": "CMYK"
	                                  },
	                                  { "constant": AbstractImage.COLORMAP_RGB,
	                                    "depth": 24,
	                                    "pil_mode": "RGB"
	                                  }
	                               ),
	                  "image/png": ( { "constant": AbstractImage.COLORMAP_PALETTE,
	                                   "depth": 8,
	                                   "pil_mode": "P"
	                                 },
	                                 { "constant": AbstractImage.COLORMAP_RGB,
	                                   "depth": 24,
	                                   "pil_mode": "RGB"
	                                 },
	                                 { "constant": AbstractImage.COLORMAP_RGBA,
	                                   "depth": 32,
	                                   "pil_mode": "RGBA"
	                                 }
	                               )
	                }
	"""
PIL colormap constant mapping
	"""
	PIL_FORMATS = { "image/bmp": "BMP",
	                "image/jpeg": "JPEG",
	                "image/png": "PNG"
	              }
	"""
Dictionary with PIL format mappings
	"""

	# See PIL libImaging/unpack.c 2013/10/01
	PIL_MODES = { "1": 1, # bilevel
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
	              "I;16L": 16
	            }

	def __init__(self):
	#
		"""
Constructor __init__(PilImage)

:since: v0.1.00
		"""

		AbstractImage.__init__(self)

		self.image_file = None
		"""
Underlying image file instance
		"""
		self.metadata = None
		"""
Cached metadata instance
		"""

		self.supported_features['transformation'] = True
	#

	def __del__(self):
	#
		"""
Destructor __del__(File)

:since: v0.1.00
		"""

		if (self.image_file is not None): self.image_file.close()
	#

	def get_image_file(self):
	#
		"""
Returns the original or transformed image file instance.
		"""

		return (self.image_file
		        if (self.transformed_image is None) else
		        self.transformed_image.get_image_file()
		       )
	#

	def get_metadata(self):
	#
		"""
Return the metadata for this URL.

:return: (object) Metadata object
:since:  v0.1.00
		"""

		# pylint: disable=protected-access

		if (self.image is None and self.unsaved_source is not None):
		#
			pil_mode = self.unsaved_source.mode
			if (pil_mode not in PilImage.PIL_MODES): raise ValueException("Unknown PIL image mode returned")

			_return = PilImageMetadata("file-unsaved:///{0:d}".format(id(self.unsaved_source)),
			                           None,
			                           width = self.unsaved_source.size[0],
			                           height = self.unsaved_source.size[1],
			                           bpp = PilImage.PIL_MODES[pil_mode]
			                          )
		#
		else:
		#
			if (self.metadata is None):
			#
				if (self.image.mode not in PilImage.PIL_MODES): raise ValueException("Unknown PIL image mode returned")

				exif_data = (self.image._getexif() if (hasattr(self.image, "_getexif")) else None)

				self.metadata = PilImageMetadata("file:///{0}".format(self.file_path_name),
				                                 exif_data,
				                                 width = self.image.size[0],
				                                 height = self.image.size[1],
				                                 bpp = PilImage.PIL_MODES[self.image.mode]
				                                )
			#

			_return = self.metadata
		#

		return _return
	#

	def new(self, file_path_name = None):
	#
		"""
Initializes a new image instance.

:param file_path_name: File path and name or None for a temporary file.

:since: v0.1.02
		"""

		if (file_path_name is None): self.image_file = TemporaryFile("w+b")
		else:
		#
			self.image_file = File()

			if (not self.image_file.open(file_path_name, file_mode = "w+b")):
			#
				self.image_file = None
				raise IOException("Failed to create image file for path '{0}'".format(file_path_name))
			#

			self.file_path_name = file_path_name
		#
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
		file_path_name = path.normpath(unquote(url_elements.path[1:]))

		with ExceptionLogTrap("pas_media"):
		#
			self.image_file = File()
			self.image_file.open(file_path_name, True, "rb")

			self.image = Image.open(file_path_name)

			self.file_path_name = file_path_name

			_return = True
		#

		return _return
	#

	def read(self, n = 0):
	#
		"""
Reads data from the opened image.

:param n: How many bytes to read from the current position (0 means until
          EOF)

:return: (bytes) Data; None if EOF
:since:  v0.1.02
		"""

		if (self.image is None): raise IOException("Invalid image state")

		image_file = self.get_image_file()
		return (image_file.read() if (n < 1) else image_file.read(n))
	#

	def save(self):
	#
		"""
Saves the media instance using the defined constraints.

:since: v0.1.02
		"""

		if (self.unsaved_source is None): raise ValueException("Source image is not defined")

		pil_format = PilImage.get_pil_format(self.unsaved_mimetype)
		pil_mode = PilImage.get_pil_colormap_definition(self.unsaved_mimetype, self.unsaved_colormap)['pil_mode']

		image = self.unsaved_source
		is_size_rotated = False
		unsaved_size = ( self.unsaved_width, self.unsaved_height )

		exif_data = (image._getexif() if (hasattr(image, "_getexif")) else None)

		if (exif_data is not None and Exif.IMAGE_ORIENTATION in exif_data):
		#
			image_orientation = InputFilter.filter_int(exif_data[Exif.IMAGE_ORIENTATION])

			if (image_orientation == Exif.IMAGE_ORIENTATION_90):
			#
				image = image.rotate(90)
				is_size_rotated = True
			#
			elif (image_orientation == Exif.IMAGE_ORIENTATION_180): image = image.rotate(180)
			elif (image_orientation == Exif.IMAGE_ORIENTATION_270):
			#
				image = image.rotate(270)
				is_size_rotated = True
			#

			if (is_size_rotated):
			#
				unsaved_size = ( self.unsaved_height, self.unsaved_width )

				self.unsaved_width = unsaved_size[0]
				self.unsaved_height = unsaved_size[1]
			#
		#

		if (self.unsaved_source.size != unsaved_size):
		#
			if (is_size_rotated): ( resize_height, resize_width ) = self._calculate_transformed_size()
			else: ( resize_width, resize_height ) = self._calculate_transformed_size()

			image = image.resize(( resize_width, resize_height ), Image.ANTIALIAS)

			if (resize_width != self.unsaved_width or resize_height != self.unsaved_height):
			#
				if (self.resize_mode == PilImage.RESIZE_SCALED_FIT):
				#
					sized_image = Image.new(self.unsaved_source.mode, unsaved_size)
					base_x = round((self.unsaved_width - resize_width) / 2)
					base_y = round((self.unsaved_height - resize_height) / 2)

					sized_image.paste(image, (base_x, base_y ))
					image = sized_image
				#
				else: image = ImageOps.fit(image, unsaved_size)
			#
		#

		if (self.unsaved_source.mode != pil_mode): image = image.convert(pil_mode, palette = Image.ADAPTIVE)

		self.image = image

		self.image_file.truncate(0)
		self.image.save(self.image_file, pil_format)
		self.image_file.seek(0)
	#

	def seek(self, offset):
	#
		"""
python.org: Change the stream position to the given byte offset.

:param offset: Seek to the given offset

:return: (int) Return the new absolute position.
:since:  v0.1.02
		"""

		if (self.image is None): raise IOException("Invalid image state")

		image_file = self.get_image_file()
		return image_file.seek(offset)
	#

	def set_colormap(self, colormap):
	#
		"""
Sets the image colormap of the unsaved image.

:param colormap: Image colormap

:since: v0.1.02
		"""

		if (not PilImage.is_colormap_supported(self.unsaved_mimetype, colormap)): raise ValueException("Colormap given is not supported by PilImage for the mime type '{0}'".format(self.unsaved_mimetype))
		self.unsaved_colormap = colormap
	#

	def set_mimetype(self, mimetype):
	#
		"""
Sets the mime type of the unsaved image.

:param mimetype: Mime type

:since: v0.1.02
		"""

		if (not PilImage.is_mimetype_supported(mimetype)): raise ValueException("Unsupported unsaved image mime type '{0}'".format(mimetype))
		self.unsaved_mimetype = mimetype
	#

	def set_source(self, image):
	#
		"""
Sets the source image.

:param image: Image instance

:since: v0.1.02
		"""

		if (not isinstance(image, Image.Image)): raise TypeException("Given image source is invalid")
		self.unsaved_source = image
	#

	def tell(self):
	#
		"""
python.org: Return the current stream position as an opaque number.

:return: (int) Stream position
:since:  v0.1.02
		"""

		if (self.image is None): raise IOException("Invalid image state")

		image_file = self.get_image_file()
		return image_file.tell()
	#

	def transform(self):
	#
		"""
Transforms the image using the defined settings.

:return: (bool) True on success
:since:  v0.1.00
		"""

		pil_format = PilImage.get_pil_format(self.unsaved_mimetype)
		pil_mode = PilImage.get_pil_colormap_definition(self.unsaved_mimetype, self.unsaved_colormap)['pil_mode']

		if (self.image.mode != pil_mode
		    or self.image.format != pil_format
		    or self.image.size != ( self.unsaved_width, self.unsaved_height )
		   ):
		#
			self.transformed_image = PilImage()

			self.transformed_image.new()
			self.transformed_image.set_source(self.image)

			self.transformed_image.set_mimetype(self.unsaved_mimetype)
			self.transformed_image.set_colormap(self.unsaved_colormap)

			self.transformed_image.set_resize_mode(self.resize_mode)
			self.transformed_image.set_size(self.unsaved_width, self.unsaved_height)

			self.transformed_image.save()
		#
	#

	@staticmethod
	def get_colormap_for_depth(mimetype, depth):
	#
		"""
Returns the colormap (constant) for the requested depth and mime type. If it
is not supported None is returned.

:param mimetype: Mime type
:param depth: Image depth

:return: (int) Colormap constant; None if not supported
:since:  v0.1.02
		"""

		_return = None

		if (mimetype in PilImage.PIL_COLORMAPS):
		#
			for pil_colormap_definition in PilImage.PIL_COLORMAPS[mimetype]:
			#
				if (pil_colormap_definition['depth'] == depth):
				#
					_return = pil_colormap_definition['constant']
					break
				#
			#
		#

		return _return
	#

	@staticmethod
	def get_pil_format(mimetype):
	#
		"""
Returns the PIL colormap definition for the given mime type and colormap.

:param mimetype: Mime type
:param colormap: Colormap constant

:return: (dict) PIL colormap definition
:since:  v0.1.02
		"""

		_return = PilImage.PIL_FORMATS.get(mimetype)

		if (_return is None): raise ValueException("Unsupported unsaved image mime type '{0}'".format(mimetype))
		return _return
	#

	@staticmethod
	def get_pil_colormap_definition(mimetype, colormap):
	#
		"""
Returns the PIL colormap definition for the given mime type and colormap.

:param mimetype: Mime type
:param colormap: Colormap constant

:return: (dict) PIL colormap definition
:since:  v0.1.02
		"""

		if (not PilImage.is_mimetype_supported(mimetype)): raise ValueException("Mime type '{0}' given is not supported by PilImage".format(mimetype))
		_return = None

		for pil_colormap_definition in PilImage.PIL_COLORMAPS[mimetype]:
		#
			if (pil_colormap_definition['constant'] == colormap):
			#
				_return = pil_colormap_definition
				break
			#
		#

		if (_return is None): raise ValueException("Colormap given is not supported by PilImage for the mime type '{0}'".format(mimetype))
		return _return
	#

	@staticmethod
	def is_colormap_supported(mimetype, colormap):
	#
		"""
Returns true if the given colormap is supported for the mime type.

:param mimetype: Mime type to check
:param colormap: Colormap constant to check

:return: (bool) True if supported
:since:  v0.1.02
		"""

		_return = True

		try: PilImage.get_pil_colormap_definition(mimetype, colormap)
		except ValueException: _return = False

		return _return
	#

	@staticmethod
	def is_mimetype_supported(mimetype):
	#
		"""
Returns true if the given mime type is supported.

:param mimetype: Mime type to check

:return: (bool) True if supported
:since:  v0.1.02
		"""

		return (mimetype in PilImage.PIL_FORMATS)
	#
#

##j## EOF