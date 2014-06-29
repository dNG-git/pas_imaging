# -*- coding: utf-8 -*-
##j## BOF

"""
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
http://www.direct-netware.de/redirect.py?pas;imaging

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
http://www.direct-netware.de/redirect.py?licenses;gpl
----------------------------------------------------------------------------
#echo(pasImagingVersion)#
#echo(__FILEPATH__)#
"""

from dNG.pas.data.media.abstract_image import AbstractImage
from dNG.pas.data.media.image_metadata import ImageMetadata
from dNG.pas.runtime.io_exception import IOException
from dNG.pas.runtime.not_implemented_exception import NotImplementedException
from dNG.pas.runtime.value_exception import ValueException
from .gstreamer import Gstreamer

class GstImage(Gstreamer, AbstractImage):
#
	"""
GStreamer implementation of the image class.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: imaging
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;gpl
             GNU General Public License 2
	"""

	def __init__(self):
	#
		"""
Constructor __init__(GstImage)

:since: v0.1.00
		"""

		AbstractImage.__init__(self)
		Gstreamer.__init__(self)
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

		_return = Gstreamer.get_metadata(self)
		if (not isinstance(_return, ImageMetadata)): raise ValueException("Metadata do not correspond to an image")
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