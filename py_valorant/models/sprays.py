from typing import Dict, Any, Optional, List
from numpy import int32

class SprayMedia:
	def __init__(self, display_icon: Optional[str], full_icon: Optional[str], full_transparent_icon: Optional[str],
			  animation_png: Optional[str], animation_gif: Optional[str]):
		self.display_icon = display_icon
		self.full_icon = full_icon
		self.full_transparent_icon = full_transparent_icon
		self.animation_png = animation_png
		self.animation_gif = animation_gif

class SprayLevel:
	def __init__(self, data: Dict[str,Any]):
		self.uuid: Optional[str] = data.get('uuid')
		self.spray_level: Optional[int32] = int32(data.get('sprayLevel',0)) if data.get('sprayLevel') is not None else None
		self._display_name: Optional[str] = data.get('displayName')
		self.display_icon: Optional[str] = data.get('displayIcon')
		self.asset_path: Optional[str] = data.get('assetPath')

	@property
	def display_name(self):
		"""The display name of the spray level. This value changes depending on the language you have set.
        You can also get this value (if not `None`) by using `str(SprayLevel)`"""
		return self._display_name

	def __str__(self):
		return self._display_name or ''

class Spray:
	"""
	Represents a Spray object

	Attributes
	----------
	uuid: :class:`Optional[str]`
		The UUID of the spray
	display_name: :class:`Optional[str]`
		The display name of the spray. This value changes depending on the language you have set.
	category: :class:`Optional[str]`
		The category of the spray
	theme_uuid: :class:`Optional[str]`
		The UUID of the theme of the spray
	is_none_spray: :class:`Optional[bool]`
		Whether the spray is a none spray
	hide_if_not_owned: :class:`Optional[bool]`
		Whether the spray is hidden if the user is not the owner
	media: :class:`Optional[SprayMedia]`
		A media object of the spray containing all the media URLs
	asset_path: :class:`Optional[str]`
		The asset path of the spray
	levels: :class:`List[SprayLevel]`
		A list of spray levels objects of the spray

	Operations
    ----------
        **str(x)**
        Returns the display name of the Spray
	"""
	def __init__(self, data: Dict[str,Any]):
		self.uuid: Optional[str] = data.get('uuid')
		self._display_name: Optional[str] = data.get('displayName')
		self.category: Optional[str] = data.get('category')
		self.theme_uuid: Optional[str] = data.get('themeUuid')
		self.is_none_spray: Optional[bool] = data.get('isNullSpray')
		self.hide_if_not_owned: Optional[bool] = data.get('hideIfNotOwned')
		self.media: Optional[SprayMedia] = SprayMedia(data.get('displayIcon'),data.get('fullIcon'),data.get('fullTransparentIcon'),
												data.get('animationPng'),data.get('animationGif')) \
		if data.get('displayIcon') or data.get('fullIcon') or data.get('fullTransparentIcon') or data.get('animationPng') or data.get('animationGif') else None
		self.asset_path: Optional[str] = data.get('assetPath')
		self.levels: List[SprayLevel] = [SprayLevel(level) for level in data.get('levels',[])]
		self._raw = data
	
	def __str__(self):
		return self._display_name or ''
	
	@property
	def display_name(self):
		"""The display name of the spray. This value changes depending on the language you have set.
		You can also get this value (if not `None`) by using `str(Spray)`"""
		return self._display_name