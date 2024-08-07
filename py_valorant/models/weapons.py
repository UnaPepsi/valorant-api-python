from typing import Dict, Any, Optional, List
from numpy import int32, float32

class WeaponAdditionalStats:
	def __init__(self, data: Dict[str,Any]):
		self.zoom_multiplier: Optional[float32] = float32(data.get('zoomMultiplier',0)) if data.get('zoomMultiplier') is not None else None
		self.fire_rate: Optional[float32] = float32(data.get('fireRate',0)) if data.get('fireRate') is not None else None
		self.run_speed_multiplier: Optional[float32] = float32(data.get('runSpeedMultiplier',0)) if data.get('runSpeedMultiplier') is not None else None
		self.burst_count: Optional[int32] = int32(data.get('burstCount',0)) if data.get('burstCount') is not None else None
		self.first_bullet_accuracy: Optional[float32] = float32(data.get('firstBulletAccuracy',0)) if data.get('firstBulletAccuracy') is not None else None

class WeaponAltShotgunStats:
	def __init__(self, data: Dict[str,Any]):
		self.shot_gun_pellet_count: Optional[int32] = int32(data.get('shotgunPelletCount',0)) if data.get('shotgunPelletCount') is not None else None
		self.burst_rate: Optional[float32] = float32(data.get('burstRate',0)) if data.get('burstRate') is not None else None

class WeaponAirBurstStats:
	def __init__(self, data: Dict[str,Any]):
		self.shot_gun_pellet_count: Optional[int32] = int32(data.get('shotgunPelletCount',0)) if data.get('shotgunPelletCount') is not None else None
		self.burst_rate: Optional[float32] = float32(data.get('burstRate',0)) if data.get('burstRate') is not None else None

class WeaponDamageRange:
	def __init__(self, data: Dict[str,Any]):
		self.range_start_meters: Optional[float32] = float32(data.get('rangeStartMeters',0)) if data.get('rangeStartMeters') is not None else None
		self.range_end_meters: Optional[float32] = float32(data.get('rangeEndMeters',0)) if data.get('rangeEndMeters') is not None else None
		self.head_damage: Optional[int32] = int32(data.get('headDamage',0)) if data.get('headDamage') is not None else None
		self.body_damage: Optional[int32] = int32(data.get('bodyDamage',0)) if data.get('bodyDamage') is not None else None
		self.leg_damage: Optional[int32] = int32(data.get('legDamage',0)) if data.get('legDamage') is not None else None

class WeaponStats:
	def __init__(self, data: Dict[str,Any]):
		self.fire_rate: Optional[float32] = float32(data.get('fireRate',0)) if data.get('fireRate') is not None else None
		self.magazine_size: Optional[int32] = int32(data.get('magazineSize',0)) if data.get('magazineSize') is not None else None
		self.run_speed_multiplier: Optional[float32] = float32(data.get('runSpeedMultiplier',0)) if data.get('runSpeedMultiplier') is not None else None
		self.reload_time_seconds: Optional[float32] = float32(data.get('reloadTimeSeconds',0)) if data.get('reloadTimeSeconds') is not None else None
		self.first_bullet_accuracy: Optional[float32] = float32(data.get('firstBulletAccuracy',0)) if data.get('firstBulletAccuracy') is not None else None
		self.shotgun_pellet_count: Optional[int32] = int32(data.get('shotgunPelletCount',0)) if data.get('shotgunPelletCount') is not None else None
		self.wall_penetration: Optional[str] = data.get('wallPenetration')
		self.feature: Optional[str] = data.get('feature')
		self.fire_mode: Optional[str] = data.get('fireMode')
		self.alt_fire_type: Optional[str] = data.get('altFireType')
		self.aditional_stats: Optional[WeaponAdditionalStats] = WeaponAdditionalStats(data.get('adsStats',{})) if data.get('adsStats') else None
		self.alt_shotgun_stats: Optional[WeaponAltShotgunStats] = WeaponAltShotgunStats(data.get('altShotgunStats',{})) if data.get('altShotgunStats') else None
		self.air_burst_stats: Optional[WeaponAirBurstStats] = WeaponAirBurstStats(data.get('airBurstStats',{})) if data.get('airBurstStats') else None
		self.damage_ranges: List[WeaponDamageRange] = [WeaponDamageRange(info) for info in data.get('damageRanges',[])] if data.get('damageRanges') else []

	def __eq__(self, other: object):
		if not isinstance(other, WeaponStats):
			return False
		return (self.fire_rate == other.fire_rate and self.magazine_size == other.magazine_size
		and self.run_speed_multiplier == other.run_speed_multiplier and self.reload_time_seconds == other.reload_time_seconds
		and self.first_bullet_accuracy == other.first_bullet_accuracy and self.shotgun_pellet_count == other.shotgun_pellet_count
		and self.wall_penetration == other.wall_penetration and self.feature == other.feature
		and self.fire_mode == other.fire_mode and self.alt_fire_type == other.alt_fire_type
		and self.aditional_stats == other.aditional_stats and self.alt_shotgun_stats == other.alt_shotgun_stats
		and self.air_burst_stats == other.air_burst_stats and self.damage_ranges == other.damage_ranges)

class WeaponIcon:
	def __init__(self, uuid: Optional[str], display_icon: Optional[str], kill_stream_icon: Optional[str]):
		self.uuid = uuid
		self.display_icon = display_icon
		self.kill_stream_icon = kill_stream_icon

class WeaponShopImage:
	def __init__(self, image: Optional[str], new_image: Optional[str], new_image_2: Optional[str]):
		self.image = image
		self.new_image = new_image
		self.new_image_2 = new_image_2

class WeaponShopData:
	def __init__(self, data: Dict[str,Any]):
		self.cost: Optional[int32] = int32(data.get('cost',0)) if data.get('cost') is not None else None
		self.category: Optional[str] = data.get('category')
		self.shop_order_priority: Optional[int32] = int32(data.get('shopOrderPriority',0)) if data.get('shopOrderPriority') is not None else None
		self._category_text: Optional[str] = data.get('categoryText')
		self.grid_row: Optional[int32] = int32(data.get('gridPosition',{}).get('column',0)) if data.get('gridPosition') is not None else None
		self.grid_column: Optional[int32] = int32(data.get('gridPosition',{}).get('gridColumn',0)) if data.get('gridPosition') is not None else None
		self.can_be_trashed: Optional[bool] = data.get('canBeTrashed')
		self.media: Optional[WeaponShopImage] = WeaponShopImage(data.get('image'), data.get('newImage'), data.get('newImage2')) \
		if data.get('image') or data.get('newImage') or data.get('newImage2') else None
		self.asset_path: Optional[str] = data.get('assetPath')
	
	@property
	def category_text(self):
		"""The category text of the weapon shop data. This value changes depending on the language you have set."""
		return self._category_text

class WeaponSkinChroma:
	def __init__(self, data: Dict[str,Any]):
		self.uuid: Optional[str] = data.get('uuid')
		self._display_name: Optional[str] = data.get('displayName')
		self.display_icon: Optional[str] = data.get('displayIcon')
		self.full_render: Optional[str] = data.get('fullRender')
		self.swatch: Optional[str] = data.get('swatch')
		self.streamed_video: Optional[str] = data.get('streamedVideo')
		self.asset_path: Optional[str] = data.get('assetPath')
	
	def __str__(self):
		return self._display_name or ''
	
	@property
	def display_name(self):
		"""The display name of the chroma. This value changes depending on the language you have set.
		You can also get this value (if not `None`) by using `str(WeaponSkinChroma)`"""
		return self._display_name

class WeaponSkinLevel:
	def __init__(self, data: Dict[str,Any]):
		self.uuid: Optional[str] = data.get('uuid')
		self._display_name: Optional[str] = data.get('displayName')
		self.level_item: Optional[str] = data.get('levelItem')
		self.display_icon: Optional[str] = data.get('displayIcon')
		self.streamed_video: Optional[str] = data.get('streamedVideo')
		self.asset_path: Optional[str] = data.get('assetPath')

	def __str__(self):
		return self._display_name or ''
	
	@property
	def display_name(self):
		"""The display name of the weapon skin level. This value changes depending on the language you have set.
		You can also get this value (if not `None`) by using `str(WeaponSkinLevel)`"""
		return self._display_name

class WeaponSkin:
	def __init__(self, data: Dict[str,Any]):
		self.uuid: Optional[str] = data.get('uuid')
		self._display_name: Optional[str] = data.get('displayName')
		self.theme_uuid: Optional[str] = data.get('themeUuid')
		self.content_tier_uuid: Optional[str] = data.get('contentTierUuid')
		self.display_icon: Optional[str] = data.get('displayIcon')
		self.wallpaper: Optional[str] = data.get('wallpaper')
		self.asset_path: Optional[str] = data.get('assetPath')
		self.chromas: List[WeaponSkinChroma] = [WeaponSkinChroma(info) for info in data.get('chromas',[])] if data.get('chromas') else []
		self.levels: List[WeaponSkinLevel] = [WeaponSkinLevel(info) for info in data.get('levels',[])] if data.get('levels') else []

	def __str__(self):
		return self._display_name or ''
	
	@property
	def display_name(self):
		"""The display name of the weapon skin. This value changes depending on the language you have set.
		You can also get this value (if not `None`) by using `str(WeaponSkin)`"""
		return self._display_name

class Weapon:
	"""
	Represents a Valorant Weapon object

	Attributes
	----------
	uuid: :class:`Optional[str]`
		The UUID of the weapon
	display_name: :class:`Optional[str]`
		The display name of the weapon. This value changes depending on the language you have set.
	category: :class:`Optional[str]`
		The category of the weapon
	icon: :class:`Optional[WeaponIcon]`
		A WeaponIcon object of the weapon containing all the icon URLs
	weapon_stats: :class:`Optional[WeaponStats]`
		A WeaponStats object of the weapon containing all the weapon stats
	asset_path: :class:`Optional[str]`
		The asset path of the weapon
	shop: :class:`Optional[WeaponShopData]`
		A WeaponShopData object of the weapon containing all the shop data
	skins: :class:`List[WeaponSkin]`
		A list of weapon skin objects of the weapon

	Operations
	----------
		**str(x)**
		Returns the display name of the Weapon. If `None`, returns an empty string<br>
		**Weapon == Weapon**
		Returns `True` if both weapons are equal, `False` otherwise
	"""
	def __init__(self, data: Dict[str,Any]):
		self.uuid: Optional[str] = data.get('uuid')
		self._display_name: Optional[str] = data.get('displayName')
		self.category: Optional[str] = data.get('category')
		self.icon: Optional[WeaponIcon] = WeaponIcon(data.get('defaultSkinUuid'), data.get('displayIcon'), data.get('killStreamIcon')) \
		if data.get('defaultSkinUuid') or data.get('displayIcon') or data.get('killStreamIcon') else None
		self.weapon_stats: Optional[WeaponStats] = WeaponStats(data.get('weaponStats',{})) if data.get('weaponStats') else None
		self.asset_path: Optional[str] = data.get('assetPath')
		self.shop: Optional[WeaponShopData] = WeaponShopData(data.get('shopData',{})) if data.get('shopData') else None
		self.skins: List[WeaponSkin] = [WeaponSkin(info) for info in data.get('skins',[])] if data.get('skins') else []
		self._raw = data

	def __str__(self):
		return self._display_name or ''
	
	def __eq__(self, other: object):
		if not isinstance(other, Weapon):
			return False
		return self.uuid == other.uuid and self.weapon_stats == other.weapon_stats and self.asset_path == other.asset_path

	@property
	def display_name(self):
		"""The display name of the weapon. This value changes depending on the language you have set.
		You can also get this value (if not `None`) by using `str(Weapon)`"""
		return self._display_name