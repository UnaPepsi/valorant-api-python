from typing import Dict, Any, Optional, List
from datetime import datetime

class AgentDisplayIcon:
	def __init__(self, display_icon: Optional[str], display_icon_small: Optional[str]):
		self._display_icon: Optional[str] = display_icon
		self._display_icon_small: Optional[str] = display_icon_small
	
	def __str__(self):
		return self._display_icon or ''

	@property
	def display_icon(self) -> Optional[str]:
		"""The URL of the agent's display icon."""
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
  		You can also get this value by using `str(BuddyLevel)`"""
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
		self.milestone_threshold: Optional[int] = data.get('milestoneThreshold')
		self.use_level_vp_cost_override: Optional[bool] = data.get('useLevelVpCostOverride')
		self.level_vp_cost_override: Optional[int] = data.get('levelVpCostOverride')
		self.start_date: Optional[datetime] = datetime.strptime(data.get('startDate'),'%Y-%m-%dT%H:%M:%SZ') if data.get('startDate') else None #type: ignore
		self.end_date: Optional[datetime] = datetime.strptime(data.get('endDate'),'%Y-%m-%dT%H:%M:%SZ') if data.get('startDate') else None #type: ignore

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
  		You can also get this value by using `str(AgentAbility)`"""
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
		self.id: Optional[int] = data.get('id')
		self.wwise: Optional[str] = data.get('wwise')
		self.wave: Optional[str] = data.get('wave')

class VoiceLine:
	def __init__(self, data: Optional[Dict[str,Any]]):
		if data is None: data = {}
		self._min_duration_single: Optional[int] = data.get('minDuration')
		self._max_duration_single: Optional[int] = data.get('maxDuration')
		self.media_list: Optional[VoiceLineMediaList] = VoiceLineMediaList(data.get('mediaList')) if data.get('mediaList') else None
	
	@property
	def min_duration_single(self) -> Optional[int]:
		"""The minimum duration of the voice line for a single play."""
		return self._min_duration_single
	
	@property
	def max_duration_single(self) -> Optional[int]:
		"""The maximum duration of the voice line for a single play."""
		return self._max_duration_single

class Agent:
	def __init__(self, data: Dict[str,Any]):
		self.uuid: Optional[str] = data.get('uuid')
		self._display_name: Optional[str] = data.get('displayName')
		self._description: Optional[str] = data.get('description')
		self.developer_name: Optional[str] = data.get('developerName')
		self._character_tags: List[str] = data.get('characterTags',[])
		self.icon: Optional[AgentDisplayIcon] = AgentDisplayIcon(data.get('displayIcon'),data.get('displayIconSmall')) if data.get('displayIcon') else None
		self.bust_portrait: Optional[str] = data.get('bustPortrait')
		self.portrait: AgentPortrait = AgentPortrait(data.get('fullPortrait'),data.get('fullPortraitV2'),data.get('killFeedPortrait'),data.get('isFullPortraitFacingRight'))
		self.background: Optional[str] = data.get('background')
		self.background_gradient_colors: List[str] = data.get('backgroundGradientColors',[])
		self.is_playable_character: Optional[bool] = data.get('isPlayableCharacter')
		self.is_available_for_test: Optional[bool] = data.get('isAvailableForTest')
		self.is_base_content: Optional[str] = data.get('isBaseContent')
		self.role: Optional[AgentRole] = AgentRole(data.get('role')) if data.get('role') else None
		self.recruitment_data: Optional[AgentRecruitmentData] = AgentRecruitmentData(data.get('recruitmentData')) if data.get('recruitmentData') else None
		self.abilities: List[AgentAbility] = [AgentAbility(info) for info in data.get('abilities',[])]
		self.voice_line: Optional[VoiceLine] = VoiceLine(data.get('voiceLine')) if data.get('voiceLine') else None

	def __str__(self):
		return self._display_name or ''

	@property
	def display_name(self):
		"""The display name of the Agent. This value changes depending on the language you have set.
  		You can also get this value by using `str(Agent)`"""
		return self._display_name
	
	@property
	def description(self):
		"""The description of the Agent. This value changes depending on the language you have set."""        
		return self._description
	
	@property
	def character_tags(self):
		"""A List containing the tags of the Agent. This value changes depending on the language you have set."""        
		return self._character_tags
