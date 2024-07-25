from typing import Any, Dict, Optional
from numpy import int32

class GearImage:
	def __init__(self, data: Dict[str,Any]):
		self.image: Optional[str] = data.get('image')
		self.new_image: Optional[str] = data.get('newImage')
		self.new_image2: Optional[str] = data.get('newImage2')

class GearShopGridPosition:
	def __init__(self, data: Dict[str,Any]):
		self.row: Optional[int32] = int32(data.get('row',0)) if data.get('row',None) is not None else None
		self.column: Optional[int32] = int32(data.get('column',0)) if data.get('column',None) is not None else None
	
	def __eq__(self, other):
		if isinstance(other, GearShopGridPosition):
			return self.row == other.row and self.column == other.column
		return False

class GearShopData:
	def __init__(self, data: Dict[str,Any]):
		self.cost: Optional[int32] = int32(data.get('cost',0)) if data.get('cost',None) is not None else None
		self.category: Optional[str] = data.get('category')
		self.shop_order_priority: Optional[int32] = int32(data.get('shopOrderPriority',0)) if data.get('shopOrderPriority',None) is not None else None
		self._category_text: Optional[str] = data.get('categoryText')
		self.grid_position: Optional[GearShopGridPosition] = GearShopGridPosition(data.get('gridPosition',{})) if data.get('gridPosition',None) is not None else None
		self.can_be_trashed: Optional[bool] = data.get('canBeTrashed')
		self.image: Optional[GearImage] = GearImage(data.get('image',{})) if data.get('image',None) is not None else None
		self.asset_path: Optional[str] = data.get('assetPath')
	
	@property
	def category_text(self):
		"""The category text of the Gear Shop Data. This value changes depending on the language you have set."""
		return self._category_text

class Gear:
	"""
	Represents a Valorant Gear object

	Attributes
	----------
	uuid: :class:`Optional[str]`
		The UUID of the Gear
	display_name: :class:`Optional[str]`
		The display name of the Gear. This value changes depending on the language you have set
	description: :class:`Optional[str]`
		The description of the Gear
	display_icon: :class:`Optional[str]`
		The display icon URL of the Gear
	asset_path: :class:`Optional[str]`
		The asset path of the Gear
	shop_data: :class:`Optional[GearShopData]`
		The shop data of the Gear

	Operations
	----------
		**str(Gear)**
		Returns the display name of the Gear. If None, returns an empty string
	"""
	def __init__(self, data: Dict[str,Any]):
		self.uuid: Optional[str] = data.get('uuid')
		self._display_name: Optional[str] = data.get('displayName')
		self.description: Optional[str] = data.get('description')
		self.display_icon: Optional[str] = data.get('displayIcon')
		self.asset_path: Optional[str] = data.get('assetPath')
		self.shop_data: Optional[GearShopData] = GearShopData(data.get('shopData',{})) if data.get('shopData',None) is not None else None
		self._raw = data

	def __str__(self):
		return self._display_name or ''
	
	@property
	def display_name(self):
		"""The display name of the Gear. This value changes depending on the language you have set.
		You can also get this value (if not `None`) by using `str(Gear)`"""
		return self._display_name