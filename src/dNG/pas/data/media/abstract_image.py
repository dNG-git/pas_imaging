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

from dNG.pas.runtime.not_implemented_exception import NotImplementedException
from .abstract import Abstract

class AbstractImage(Abstract):
#
	"""
Implementation independent image class.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: imaging
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;gpl
             GNU General Public License 2
	"""

	# pylint: disable=unused-argument

	COLORMAP_CMYK = 3
	"""
CMYK colormap
	"""
	COLORMAP_PALETTE = 4
	"""
Palette based colormap for 256 colors
	"""
	COLORMAP_HIGH_COLOR = 5
	"""
High color colormap
	"""
	COLORMAP_RGB = 1
	"""
RGB colormap
	"""
	COLORMAP_RGBA = 2
	"""
RGBA colormap
	"""
	RESIZE_CROP = 1
	"""
Crop image to fit
	"""
	RESIZE_SCALED_CROP = 2
	"""
Scale image and crop borders to fit
	"""
	RESIZE_SCALED_FIT = 3
	"""
Scale image and add borders to fit
	"""

	def __init__(self):
	#
		"""
Constructor __init__(AbstractImage)

:since: v0.1.00
		"""

		Abstract.__init__(self)

		self.file_path_name = None
		"""
Image file path and name
		"""
		self.image = None
		"""
Underlying image instance
		"""
		self.resize_mode = AbstractImage.RESIZE_CROP
		"""
Resize mode used for "set_size()"
		"""
		self.transformed_image = None
		"""
Underlying image instance of a transformed one
		"""
		self.unsaved_colormap = None
		"""
Unsaved image colormap
		"""
		self.unsaved_height = None
		"""
Unsaved image height
		"""
		self.unsaved_mimetype = None
		"""
Unsaved image mime type
		"""
		self.unsaved_source = None
		"""
Unsaved image source
		"""
		self.unsaved_width = None
		"""
Unsaved image width
		"""
	#

	def _calculate_transformed_size(self):
	#
		"""
Calculates the transformed image size under the defined resize mode.

:return: (tuple) Tuple with width and height in pixel
		"""

		image_metadata = self.get_metadata()

		image_height = image_metadata.get_height()
		image_width = image_metadata.get_width()

		resize_factor = 1
		resize_factor_height = (self.unsaved_height / image_height)
		resize_factor_width = (self.unsaved_width / image_width)

		if (resize_factor_width > 1 or resize_factor_height > 1):
		#
			if (self.resize_mode != AbstractImage.RESIZE_CROP):
			#
				if (resize_factor_width > resize_factor_height):
				#
					resize_factor = (resize_factor_height
					                 if (self.resize_mode == AbstractImage.RESIZE_SCALED_FIT) else
					                 resize_factor_width
					                )
				#
				else:
				#
					resize_factor = (resize_factor_width
					                 if (self.resize_mode == AbstractImage.RESIZE_SCALED_FIT) else
					                 resize_factor_height
					                )
				#
			#
		#
		elif (resize_factor_width < resize_factor_height):
		#
			resize_factor = (resize_factor_width
			                 if (self.resize_mode == AbstractImage.RESIZE_SCALED_FIT) else
			                 resize_factor_height
			                )
		#
		else:
		#
			resize_factor = (resize_factor_height
			                 if (self.resize_mode == AbstractImage.RESIZE_SCALED_FIT) else
			                 resize_factor_width
			                )
		#

		return ( int(image_width * resize_factor), int(image_height * resize_factor) )
	#

	def new(self, file_path_name = None):
	#
		"""
Initializes a new image instance.

:param file_path_name: File path and name or None for a temporary file.

:since: v0.1.02
		"""

		raise NotImplementedException()
	#

	def read(self, n = 0):
	#
		"""
Reads data from the opened image.

:param n: How many bytes to read from the current position (0 means until
          EOF)

:return: (bytes) Data; None if EOF
:since:  v0.1.00
		"""

		raise NotImplementedException()
	#

	def open_url(self, url):
	#
		"""
Initializes an media instance for the given URL.

:param url: URL

:return: (bool) True on success
:since:  v0.1.00
		"""

		return False
	#

	def save(self):
	#
		"""
Saves the image using the defined constraints.

:since: v0.1.02
		"""

		raise NotImplementedException()
	#

	def seek(self, offset):
	#
		"""
python.org: Change the stream position to the given byte offset.

:param offset: Seek to the given offset

:return: (int) Return the new absolute position.
:since:  v0.1.00
		"""

		raise NotImplementedException()
	#

	def set_colormap(self, colormap):
	#
		"""
Sets the image colormap of the unsaved image.

:param colormap: Image colormap

:since: v0.1.02
		"""

		self.unsaved_colormap = colormap
	#

	def set_mimetype(self, mimetype):
	#
		"""
Sets the mime type of the unsaved image.

:param mimetype: Mime type

:since: v0.1.02
		"""

		self.unsaved_mimetype = mimetype
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
Sets the image size of the unsaved image.

:param width: Image width
:param height: Image height

:since: v0.1.00
		"""

		self.unsaved_width = width
		self.unsaved_height = height
	#

	def set_source(self, image):
	#
		"""
Sets the source image.

:param image: Image instance

:since: v0.1.02
		"""

		raise NotImplementedException()
	#

	def tell(self):
	#
		"""
Returns the current offset.

:return: (int) Offset; False on error
:since:  v0.1.02
		"""

		raise NotImplementedException()
	#

	def transform(self):
	#
		"""
Transforms the image using the defined settings.

:return: (bool) True on success
:since:  v0.1.00
		"""

		return False
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

		return None
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

		return False
	#
#

##j## EOF