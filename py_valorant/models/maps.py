from typing import Any, Dict, Optional, List
from numpy import float32

class MapIcon:
	def __init__(self, display_icon: Optional[str], list_view_icon: Optional[str], list_view_icon_tall: Optional[str]):
		self.display_icon = display_icon
		self.list_view_icon = list_view_icon
		self.list_view_icon_tall = list_view_icon_tall

class MapBackground:
	def __init__(self, stylized_background: Optional[str], premier_background: Optional[str], splash: Optional[str]):
		self.stylized_background = stylized_background
		self.premier_background = premier_background
		self.splash = splash

class MapLocation:
	def __init__(self, data: Dict[str,Any]):
		self.x: Optional[float32] = float32(data.get('x',0)) if data.get('x',None) is not None else None
		self.y: Optional[float32] = float32(data.get('y',0)) if data.get('y',None) is not None else None
	
	def __eq__(self, other):
		if isinstance(other,MapLocation):
			return self.x == other.x and self.y == other.y
		return False

class MapCallout:
	def __init__(self, data: Dict[str,Any]):
		self._region_name: Optional[str] = data.get('regionName')
		self._super_region_name: Optional[str] = data.get('superRegionName')
		self.location: Optional[MapLocation] = MapLocation(data.get('location',{})) if data.get('location') is not None else None
	
	def __eq__(self, other):
		if isinstance(other,MapCallout):
			return self.location == other.location
		return False

class Map:
	"""
	Represents a Valorant Map object

	Attributes
	----------
	uuid: :class:`Optional[str]`
		The UUID of the Map
	display_name: :class:`Optional[str]`
		The display name of the Map. This value changes depending on the language you have set
	narrative_description: :class:`Optional[str]`
		The narrative description of the Map. This value changes depending on the language you have set
	tactical_description: :class:`Optional[str]`
		The tactical description of the Map. This value changes depending on the language you have set
	coordinates: :class:`Optional[str]`
		The coordinates of the Map. This value changes depending on the language you have set
	icon: :class:`Optional[MapIcon]`
		An Icon object of the Map
	background: :class:`Optional[MapBackground]`
		A Background object of the Map
	asset_path: :class:`Optional[str]`
		The asset path of the Map
	map_url: :class:`Optional[str]`
		The URL of the Map
	x_multiplier: :class:`Optional[float32]`
		The X multiplier of the Map
	y_muiltiplier: :class:`Optional[float32]`
		The Y multiplier of the Map
	y_scalar_to_add: :class:`Optional[float32]`
		The Y scalar to add of the Map
	callouts: :class:`List[MapCallout]`
		A list of MapCallout objects of the Map

	Operations
	----------
		**str(Map)**
		Returns the display name of the Map. If None, returns an empty string<br>
		**Map == Map**
		Returns True if both Maps are equal
	"""
	def __init__(self, data: Dict[str,Any]):
		self.uuid: Optional[str] = data.get('uuid')
		self._display_name: Optional[str] = data.get('displayName')
		self._narrative_description: Optional[str] = data.get('narrativeDescription')
		self._tactical_description: Optional[str] = data.get('tacticalDescription')
		self._coordinates: Optional[str] = data.get('coordinates')
		self.icon: Optional[MapIcon] = MapIcon(data.get('displayIcon'),data.get('listViewIcon'),
											   data.get('listViewIconTall')) \
		if data.get('displayIcon') is not None or data.get('listViewIcon') is not None or data.get('listViewIconTall') is not None else None
		self.background: Optional[MapBackground] = MapBackground(data.get('stylizedBackgroundImage'),data.get('premierBackgroundImage'),
																 data.get('splash')) \
		if data.get('stylizedBackgroundImage') is not None or data.get('premierBackgroundImage') is not None or data.get('splash') is not None else None
		self.asset_path: Optional[str] = data.get('assetPath')
		self.map_url: Optional[str] = data.get('mapUrl')
		self.x_multiplier: Optional[float32] = float32(data.get('xMultiplier',0)) if data.get('xMultiplier',None) is not None else None
		self.y_muiltiplier: Optional[float32] = float32(data.get('yMultiplier',0)) if data.get('yMultiplier',None) is not None else None
		self.y_scalar_to_add: Optional[float32] = float32(data.get('yScalarToAdd',0)) if data.get('yScalarToAdd',None) is not None else None
		self.callouts: List[MapCallout] = [MapCallout(callout) for callout in data.get('callouts',[])] if data.get('callouts') else []
		self._raw = data

	def __str__(self):
		return self._display_name or ''
	
	def __eq__(self,other):
		if isinstance(other,Map):
			return self.uuid == other.uuid and self.callouts == other.callouts
		
	@property
	def display_name(self):
		"""The display name of the Map. This value changes depending on the language you have set.
		You can also get this value (if not `None`) by using `str(Map)`"""
		return self._display_name
	
	@property
	def narrative_description(self):
		"""The narrative description of the Map. This value changes depending on the language you have set."""
		return self._narrative_description
	
	@property
	def tactical_description(self):
		"""The tactical description of the Map. This value changes depending on the language you have set."""
		return self._tactical_description
	
	@property
	def coordinates(self):
		"""The coordinates of the Map. This value changes depending on the language you have set."""
		return self._coordinates