# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.media.PilImageMetadata
"""
"""n// NOTE
----------------------------------------------------------------------------
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
----------------------------------------------------------------------------
NOTE_END //n"""

from .exif import Exif
from .image_metadata import ImageMetadata

class PilImageMetadata(ImageMetadata):
#
	"""
This class provides access to PIL metadata.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: imaging
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;gpl
             GNU General Public License 2
	"""

	def __init__(self, url, exif_data, **kwargs):
	#
		"""
Constructor __init__(PilImageMetadata)

:param url: Metadata source URL
:param exif_data: Image Exif data as dict

:since: v0.1.00
		"""

		if (exif_data != None):
		#
			if (Exif.ARTIST in exif_data):
			#
				exif_value = Exif.filter_ascii(exif_data[Exif.ARTIST])
				if (exif_value != None and len(exif_value) > 0): kwargs['artist'] = exif_value
			#

			if (Exif.COPYRIGHT in exif_data):
			#
				exif_value = Exif.filter_ascii(exif_data[Exif.COPYRIGHT])
				if (exif_value != None and len(exif_value) > 0): kwargs['copyright'] = exif_value
			#

			"""
Select description from Exif.DESCRIPTION or Exif.USER_COMMENT tags.
			"""

			exif_value = None

			if (Exif.DESCRIPTION in exif_data):
			#
				exif_value = Exif.filter_ascii(exif_data[Exif.DESCRIPTION])
				if (exif_value != None and len(exif_value) == 0): exif_value = None
			#

			if (exif_value == None and Exif.USER_COMMENT in exif_data): exif_value = Exif.filter_typed_string(exif_data[Exif.USER_COMMENT])
			if (exif_value != None and len(exif_value) > 0): kwargs['description'] = exif_value

			"""
Select producer from Exif.DEVICE_* or Exif.SOFTWARE tags.
			"""

			if (Exif.DEVICE_VENDOR in exif_data or Exif.DEVICE_MODEL in exif_data):
			#
				exif_value = (Exif.filter_ascii(exif_data[Exif.DEVICE_VENDOR]) if (Exif.DEVICE_VENDOR in exif_data) else "")
				exif_model_value = (Exif.filter_ascii(exif_data[Exif.DEVICE_MODEL]) if (Exif.DEVICE_MODEL in exif_data) else "")

				if (len(exif_model_value) > 0):
				#
					exif_model_value = Exif.filter_ascii(exif_data[Exif.DEVICE_MODEL])

					if (len(exif_value) > 0): exif_value += " - {0}".format(exif_model_value)
					else: exif_value = exif_model_value
				#

				if (exif_value != None and len(exif_value) == 0): exif_value = None
			#

			if (exif_value == None and Exif.SOFTWARE in exif_data): exif_value = Exif.filter_ascii(exif_data[Exif.SOFTWARE])
			if (exif_value != None and len(exif_value) > 0): kwargs['producer'] = exif_value
		#

		ImageMetadata.__init__(self, url, **kwargs)
	#
#

##j## EOF