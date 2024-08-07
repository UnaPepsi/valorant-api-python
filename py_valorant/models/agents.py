from typing import Dict, Any, Optional, List
from datetime import datetime
from numpy import float32, int32

class AgentDisplayIcon:
	def __init__(self, display_icon: Optional[str], display_icon_small: Optional[str]):
		self._display_icon = display_icon
		self._display_icon_small = display_icon_small
	
	def __str__(self):
		return self._display_icon or ''

	@property
	def display_icon(self) -> Optional[str]:
		"""The URL of the agent's display icon. You can also get this value (if not `None`) by using `str(AgentDisplayIcon)`"""
		return self._display_icon
	@property
	def display_icon_small(self) -> Optional[str]:
		"""The URL of the agent's display icon but with a smaller size."""
		return self._display_icon_small

class AgentPortrait:
	def __init__(self, full_portrait: Optional[str], full_portrait_v2: Optional[str],kill_feed_portrait: Optional[str], is_full_portrait_facing_right: Optional[bool] = False):
		self._full_portrait: Optional[str] = full_portrait
		self._full_portrait_v2: Optional[str] = full_portrait_v2
		self._kill_feed_portrait: Optional[str] = kill_feed_portrait   
		self._is_full_portrait_facing_right: Optional[bool] = is_full_portrait_facing_right 

	@property
	def full_portrait(self) -> Optional[str]:
		"""The URL of the agent's portrait."""
		return self._full_portrait
	@property
	def full_portrait_v2(self) -> Optional[str]:
		"""Same as `full_portrait`. You shouldn't need to use this"""
		return self._full_portrait_v2
	@property
	def kill_feed_portrait(self) -> Optional[str]:
		"""The URL of the agent's kill feed portrait."""
		return self._kill_feed_portrait
	@property
	def is_full_portrait_facing_right(self) -> Optional[bool]:
		"""Whether the agent's full portrait is facing right."""
		return self._is_full_portrait_facing_right

class AgentRole:
	def __init__(self, data: Optional[Dict[str,Any]]):
		if data is None: data = {}
		self._uuid: Optional[str] = data.get('uuid')
		self._display_name: Optional[str] = data.get('displayName')
		self._description: Optional[str] = data.get('description')
		self._display_icon: Optional[str] = data.get('displayIcon')
		self._asset_path: Optional[str] = data.get('assetPath')
	
	def __str__(self):
		return self._display_name or ''

	@property
	def uuid(self) -> Optional[str]:
		"""The UUID of the role."""
		return self._uuid
	@property
	def display_name(self) -> Optional[str]:
		"""The display name of the role. This value changes depending on the language you have set.
  		You can also get this value (if not `None`) by using `str(BuddyLevel)`"""
		return self._display_name
	@property
	def description(self) -> Optional[str]:
		"""The description of the role. This value changes depending on the language you have set."""
		return self._description
	@property
	def display_icon(self) -> Optional[str]:
		"""The URL of the role's display icon."""
		return self._display_icon
	@property
	def asset_path(self) -> Optional[str]:
		"""The asset path of the role."""
		return self._asset_path

class AgentRecruitmentData:
	# TODO: make properties for this
	def __init__(self, data: Optional[Dict[str,Any]]):
		if data is None: data = {}
		self.counter_id: Optional[str] = data.get('counterId')
		self.milestone_id: Optional[str] = data.get('milestoneId')
		self.milestone_threshold: Optional[int32] = int32(data.get('milestoneThreshold',0)) if data.get('milestoneThreshold',None) is not None else None
		self.use_level_vp_cost_override: Optional[bool] = data.get('useLevelVpCostOverride')
		self.level_vp_cost_override: Optional[int32] = int32(data.get('levelVpCostOverride',0)) if data.get('levelVpCostOverride',None) is not None else None
		self.start_date: Optional[datetime] = datetime.strptime(data.get('startDate',''),'%Y-%m-%dT%H:%M:%SZ') if data.get('startDate') else None
		self.end_date: Optional[datetime] = datetime.strptime(data.get('endDate',''),'%Y-%m-%dT%H:%M:%SZ') if data.get('startDate') else None

class AgentAbility:
	def __init__(self, data: Optional[Dict[str,Any]]):
		if data is None: data = {}
		self._slot: Optional[str] = data.get('slot')
		self._display_name: Optional[str] = data.get('displayName')
		self._description: Optional[str] = data.get('description')
		self._display_icon: Optional[str] = data.get('displayIcon')
	
	def __str__(self):
		return self._display_name or ''
 
	@property
	def slot(self) -> Optional[str]:
		"""The slot of the ability."""
		return self._slot
	@property
	def display_name(self) -> Optional[str]:
		"""The display name of the ability. This value changes depending on the language you have set.
  		You can also get this value (if not `None`) by using `str(AgentAbility)`"""
		return self._display_name
	@property
	def description(self) -> Optional[str]:
		"""The description of the ability. This value changes depending on the language you have set."""
		return self._description
	@property
	def display_icon(self) -> Optional[str]:
		"""The display icon of the ability."""
		return self._display_icon

class VoiceLineMediaList:
	# TODO: make properties for this
	def __init__(self, data: Optional[Dict[str,Any]]):
		if data is None: data = {}
		self.id: Optional[int32] = int32(data.get('id',0)) if data.get('id',None) is not None else None
		self.wwise: Optional[str] = data.get('wwise')
		self.wave: Optional[str] = data.get('wave')

class VoiceLine:
	def __init__(self, data: Optional[Dict[str,Any]]):
		if data is None: data = {}
		self._min_duration: Optional[float32] = float32(data.get('minDuration',0.0)) if data.get('minDuration') else None
		self._max_duration: Optional[float32] = float32(data.get('maxDuration',0.0)) if data.get('maxDuration') else None
		self.media_list: Optional[VoiceLineMediaList] = VoiceLineMediaList(data.get('mediaList')) if data.get('mediaList') else None
	
	@property
	def min_duration(self) -> Optional[float32]:
		"""The minimum duration of the voice line for a single play."""
		return self._min_duration
	
	@property
	def max_duration(self) -> Optional[float32]:
		"""The maximum duration of the voice line for a single play."""
		return self._max_duration

class Agent:
	"""
	Represents an Agent object (a character in the game)

	https://valorantinfo.gg/agents/

	Attributes
	----------
	uuid: :class:`Optional[str]`
		The UUID of the agent
	display_name: :class:`Optional[str]`
		The display name of the agent. This value changes depending on the language you have set
	description: :class:`Optional[str]`
		The description of the agent. This value changes depending on the language you have set
	developer_name: :class:`Optional[str]`
		The developer name of the agent
	character_tags: :class:`List[str]`
		A List containing the tags of the agent. The values change depending on the language you have set
	icon: :class:`Optional[AgentDisplayIcon]`
		The display icon of the agent
	bust_portrait: :class:`Optional[str]`
		The bust portrait of the agent
	portrait: :class:`AgentPortrait`
		An object representing all portraits data from the agent
	background: :class:`Optional[str]`
		The background URL of the agent
	background_gradient_colors: :class:`List[str]`
		A List containing the background gradient colors of the agent
	is_playable_character: :class:`Optional[bool]`
		Whether the agent is a playable character. If this is `False` this is probably a duplicate
	is_available_for_test: :class:`Optional[bool]`
		Whether the agent is available for testing
	is_base_content: :class:`Optional[str]`
		Whether the agent is base content
	role: :class:`Optional[AgentRole]`
		An object representing the role of the agent
	recruitment_data: :class:`Optional[AgentRecruitmentData]`
		An object representing the recruitment data of the agent
	abilities: :class:`List[AgentAbility]`
		A List containing ability objects of the agent
	voice_line: :class:`Optional[VoiceLine]`
		An object representing the voice line object of the agent

	Operations
	----------
		**str(Agent)**
		Returns the display name of the agent. If None, returns an empty string
	"""
	def __init__(self, data: Dict[str,Any]):
		self.uuid: Optional[str] = data.get('uuid')
		self._display_name: Optional[str] = data.get('displayName')
		self._description: Optional[str] = data.get('description')
		self.developer_name: Optional[str] = data.get('developerName')
		self._character_tags: List[str] = data.get('characterTags',[])
		self.icon: Optional[AgentDisplayIcon] = AgentDisplayIcon(data.get('displayIcon'),data.get('displayIconSmall')) if data.get('displayIcon') or data.get('displayIconSmall') else None
		self.bust_portrait: Optional[str] = data.get('bustPortrait')
		self.portrait: Optional[AgentPortrait] = AgentPortrait(data.get('fullPortrait'),data.get('fullPortraitV2'),data.get('killfeedPortrait'),data.get('isFullPortraitRightFacing')) \
		if data.get('fullPortrait') or data.get('fullPortraitV2') or data.get('killfeedPortrait') or data.get('isFullPortraitRightFacing') else None
		self.background: Optional[str] = data.get('background')
		self.background_gradient_colors: List[str] = data.get('backgroundGradientColors',[])
		self.is_playable_character: Optional[bool] = data.get('isPlayableCharacter')
		self.is_available_for_test: Optional[bool] = data.get('isAvailableForTest')
		self.is_base_content: Optional[str] = data.get('isBaseContent')
		self.role: Optional[AgentRole] = AgentRole(data.get('role',{})) if data.get('role') else None
		self.recruitment_data: Optional[AgentRecruitmentData] = AgentRecruitmentData(data.get('recruitmentData')) if data.get('recruitmentData') else None
		self.abilities: List[AgentAbility] = [AgentAbility(info) for info in data.get('abilities',[])]
		self.voice_line: Optional[VoiceLine] = VoiceLine(data.get('voiceLine')) if data.get('voiceLine') else None
		self._raw = data

	def __str__(self):
		return self._display_name or ''

	@property
	def display_name(self):
		"""The display name of the Agent. This value changes depending on the language you have set.
  		You can also get this value (if not `None`) by using `str(Agent)`"""
		return self._display_name
	
	@property
	def description(self):
		"""The description of the Agent. This value changes depending on the language you have set."""        
		return self._description
	
	@property
	def character_tags(self):
		"""A List containing the tags of the Agent. This value changes depending on the language you have set."""        
		return self._character_tags