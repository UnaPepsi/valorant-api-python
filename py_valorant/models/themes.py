from typing import Dict, Any, Optional

class Theme:
	"""
	Represents a Theme object
	
	Attributes
	----------
	uuid: :class:`Optional[str]`
		The UUID of the theme
	display_name: :class:`Optional[str]`
		The display name of the theme. This value changes depending on the language you have set.
	display_icon: :class:`Optional[str]`
		The display icon of the theme
	store_featured_image: :class:`Optional[str]`
		The store featured image of the theme
	asset_path: :class:`Optional[str]`
		The asset path of the theme
		
	Operations
	----------
		**str(x)**
		Returns the display name of the Theme. If `None`, returns an empty string
	"""
	def __init__(self, data: Dict[str,Any]):
		self.uuid: Optional[str] = data.get('uuid')
		self._display_name: Optional[str] = data.get('displayName')
		self.display_icon: Optional[str] = data.get('displayIcon')
		self.store_featured_image: Optional[str] = data.get('storeFeaturedImage')
		self.asset_path: Optional[str] = data.get('assetPath')
		self._raw = data
	
	def __str__(self):
		return self._display_name or ''
	
	@property
	def display_name(self):
		"""
		The display name of the theme. This value changes depending on the language you have set.
		You can also get this value (if not `None`) by using `str(Theme)`"""
		return self._display_name