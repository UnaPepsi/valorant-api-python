from typing import Any, Dict, List, Optional
from numpy import int32

class GameFeatureOverrides:
	def __init__(self, feature_name: Optional[str], state: Optional[bool]):
		self.feature_name = feature_name
		self.state = state

class GameRuleOverrides:
	def __init__(self, rule_name: Optional[str], state: Optional[bool]):
		self.rule_name = rule_name
		self.state = state

class Gamemode:
	"""
	Represents a Valorant Gamemode object

	Atributes
	----------
	uuid: :class:`Optional[str]`
		The UUID of the gamemode
	display_name: :class:`Optional[str]`
		The display name of the gamemode. This value changes depending on the language you have set.
	description: :class:`Optional[str]`

	duration: :class:`Optional[str]`
		The duration of the gamemode. This value changes depending on the language you have set.
	economy_type: :class:`Optional[str]`
		The economy type of the gamemode
	allow_match_timeouts: :class:`Optional[bool]`
		Whether match timeouts are allowed in the gamemode
	is_team_voice_allowed: :class:`Optional[bool]`
		Whether team voice is allowed in the gamemode
	is_minimap_hidden: :class:`Optional[bool]`
		Whether the minimap is hidden in the gamemode
	orb_count: :class:`Optional[int32]`
		The orb count of the gamemode
	round_per_half: :class:`Optional[int32]`
		Amount of rounds per half
	team_roles: :class:`List[str]`
		A list of the team roles of the gamemdoe
	game_feature_overrides: :class:`List[GameFeatureOverrides]`
		A list of the game feature overrides of the gamemode
	game_rule_overrides: :class:`List[GameRuleOverrides]`
		A list of the game rule overrides of the gamemode
	display_icon: :class:`Optional[str]`
		The display icon URL of the gamemode
	list_view_icon_tall: :class:`Optional[str]`
		The list view icon tall URL of the gamemode
	asset_path: :class:`Optional[str]`
		The asset path of the gamemode

	Operations
	----------
		**str(Gamemode)**
		Returns the display name of the gamemode. If None, returns an empty string
	"""
	def __init__(self, data: Dict[str,Any]):
		self.uuid: Optional[str] = data.get('uuid')
		self._display_name: Optional[str] = data.get('displayName')
		self._description: Optional[str] = data.get('description')
		self._duration: Optional[str] = data.get('duration')
		self.economy_type: Optional[str] = data.get('economyType')
		self.allow_match_timeouts: Optional[bool] = data.get('allowMatchTimeouts')
		self.is_team_voice_allowed: Optional[bool] = data.get('isTeamVoiceAllowed')
		self.is_minimap_hidden: Optional[bool] = data.get('isMinimapHidden')
		self.orb_count: Optional[int32] = int32(data.get('orbCount',0)) if data.get('orbCount',None) is not None else None
		self.round_per_half: Optional[int32] = int32(data.get('roundPerHalf',0)) if data.get('roundPerHalf',None) is not None else None
		self.team_roles: List[str] = data.get('teamRoles',[]) if data.get('teamRoles') else []
		self.game_feature_overrides: List[GameFeatureOverrides] = [GameFeatureOverrides(info.get('featureName'),info.get('state')) for info in data.get('gameFeatureOverrides',[])] \
		if data.get('gameFeatureOverrides') else []
		self.game_rule_overrides: List[GameRuleOverrides] = [GameRuleOverrides(info.get('ruleName'),info.get('state')) for info in data.get('gameRuleBoolOverrides',[])] \
		if data.get('gameRuleBoolOverrides') else []
		self.display_icon: Optional[str] = data.get('displayIcon')
		self.list_view_icon_tall: Optional[str] = data.get('listViewIconTall')
		self.asset_path: Optional[str] = data.get('assetPath')
	
	def __str__(self):
		return self._display_name or ''

	@property
	def display_name(self):
		"""
		Returns the display name of the gamemode.
		This value canges depending on the language you have set. You can also get this value (if not `None`) using `str(Gamemode)`
		"""
		return self._display_name
	@property
	def description(self):
		"""
		Returns the description of the gamemode.
		This value changes depending on the language you have set.
		"""
		return self._description
	@property
	def duration(self):
		"""
		Returns the raw string of the duration of the gamemode. Example: `'10-30 MINS'`.
		This value changes depending on the language you have set.
		"""
		return self._duration
	@property
	def duration_range(self):
		"""
		Tries to format `duration` into a range object. Example: `10-30 MINS` -> `range(10,30)`. Returns `None` if it fails.
		"""
		temp = self.duration_list
		if temp:
			return range(temp[0],temp[1])
		return None
	@property
	def duration_list(self):
		"""
		Tries to format `duration` into a list object. Example: `10-30 MINS` -> `[10,30]`. Returns `None` if it fails.
		"""
		if isinstance(self._duration,str):
			try:
				splitted = self._duration.replace(' MIN','').replace('S','').split('-')
				return [int(splitted[0]),int(splitted[1])]
			except IndexError:
				return None
		return None

class GamemodeEquipableIcon:
	def __init__(self, display_icon: Optional[str], kill_stream_icon: Optional[str]):
		self.display_icon = display_icon
		self.kill_stream_icon = kill_stream_icon

class GamemodeEquipable:
	"""
	Represents a Valorant Gamemode Equipable object

	Attributes
	----------
	uuid: :class:`Optional[str]`
		The UUID of the gamemode equipable
	display_name: :class:`Optional[str]`
		The display name of the gamemode equipable. This value changes depending on the language you have set.
	category: :class:`Optional[str]`
		The category of the gamemode equipable
	icon: :class:`Optional[GamemodeEquipableIcon]`
		The icon object of the gamemode equipable
	asset_path: :class:`Optional[str]`
		The asset path of the gamemode equipable

	Operations
	----------
		**str(GamemodeEquipable)**
		Returns the display name of the gamemode equipable. If None, returns an empty string
	"""
	def __init__(self, data: Dict[str,Any]):
		self.uuid: Optional[str] = data.get('uuid')
		self._display_name: Optional[str] = data.get('displayName')
		self.category: Optional[str] = data.get('category')
		self.icon: Optional[GamemodeEquipableIcon] = GamemodeEquipableIcon(data.get('displayIcon'),data.get('killStreamIcon')) \
		if data.get('displayIcon') or data.get('killStreamIcon') else None
		self.asset_path: Optional[str] = data.get('assetPath')
	
	def __str__(self):
		return self._display_name or ''

	@property
	def display_name(self):
		"""
		Returns the display name. This value changes depending on the language you have set."""
		return self._display_name