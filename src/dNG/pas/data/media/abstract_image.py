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

	RESIZE_CROP = 1
	"""
Crop image to fit
	"""
	RESIZE_SCALED = 2
	"""
Scale image to fit
	"""
	RESIZE_SCALED_CROP = 3
	"""
Scale image and crop borders to fit
	"""
	RESIZE_SCALED_FIT = 4
	"""
Scale image and add borders to fit
	"""

	def __init__(self):
	#
		"""
Constructor __init__(AbstractImage)

:since: v0.1.00
		"""

		self.file_pathname = None
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

		return False
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