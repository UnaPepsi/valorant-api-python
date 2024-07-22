from typing import Any, Dict, Optional
from numpy import int32

class ContentTier:
	"""
	Represents a content tier object
	
	Attributes
	----------
	uuid: :class:`Optional[str]`
		The UUID of the content tier
	display_name: :class:`Optional[str]`
		The display name of the content tier. This value changes depending on the language you have set.
	rank: :class:`Optional[int32]`
		The rank of the content tier
	juice_value: :class:`Optional[int32]`
		The juice value of the content tier
	juice_cost: :class:`Optional[int32]`
		The juice cost of the content tier
	highlight_color: :class:`Optional[str]`
		The highlight color of the content tier in hexadecimal value
	display_icon: :class:`Optional[str]`
		The display icon URL of the content tier
	asset_path: :class:`Optional[str]`
		The asset path of the content tier

	Operations
	----------
		**str(ContentTier)**
		Returns the display name of the content tier. If None, returns an empty string
	"""
	def __init__(self, data: Dict[str,Any]):
		self.uuid: Optional[str] = data.get('uuid')
		self._display_name: Optional[str] = data.get('displayName')
		self.dev_name: Optional[str] = data.get('devName')
		self.rank: Optional[int32] = int32(data.get('rank',0)) if data.get('rank') else None
		self.juice_value: Optional[int32] = data.get('juiceValue')
		self.juice_cost: Optional[int32] = data.get('juiceCost')
		self.highlight_color: Optional[str] = '0x'+data.get('highlightColor','') if data.get('highlightColor') else None
		self.display_icon: Optional[str] = data.get('displayIcon')
		self.asset_path: Optional[str] = data.get('assetPath')
	
	def __str__(self):
		return self._display_name or ''

	@property
	def display_name(self):
		"""The display name of the content tier. This value changes depending on the language you have set.
		You can also get this value by using `str(ContentTier)`"""
		return self._display_name