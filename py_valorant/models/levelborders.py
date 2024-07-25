from typing import Dict, Any, Optional
from numpy import int32

class LevelBorder:
	"""
	Represents a Valorant Level Border object

	Attributes
	----------
	uuid: :class:`Optional[str]`
		The UUID of the Level Border
	display_name: :class:`Optional[str]`
		The display name of the Level Border. This value changes depending on the language you have set
	starting_level: :class:`Optional[int32]`
		The starting level of the Level Border
	level_number_appearance: :class:`Optional[str]`
		The level number appearance of the Level Border
	small_player_card_appearance: :class:`Optional[str]`
		The small player card appearance of the Level Border
	asset_path: :class:`Optional[str]`
		The asset path of the Level Border
	"""
	def __init__(self, data: Dict[str,Any]):
		self.uuid: Optional[str] = data.get('uuid')
		self._display_name: Optional[str] = data.get('displayName')
		self.starting_level: Optional[int32] = int32(data.get('startingLevel',0)) if data.get('startingLevel',None) is not None else None
		self.level_number_appearance: Optional[str] = data.get('levelNumberAppearance')
		self.small_player_card_appearance: Optional[str] = data.get('smallPlayerCardAppearance')
		self.asset_path: Optional[str] = data.get('assetPath')
		self._raw = data

	def __str__(self):
		return self._display_name or ''
	
	@property
	def display_name(self):
		"""The display name of the Level Border. This value changes depending on the language you have set.
		You can also get this value (if not `None`) by using `str(LevelBorder)`"""
		return self._display_name