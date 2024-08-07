from typing import Optional, Dict, Any, List
from numpy import int32

class BuddyLevel:
    def __init__(self, data: Dict[str,Any]):
        self.uuid: Optional[str] = data.get('uuid')
        self.charm_level: Optional[int32] = int32(data.get('charmLevel',0)) if data.get('charmLevel',None) is not None else None
        self.hide_if_not_found: Optional[bool] = data.get('hideIfNotFound')
        self._display_name: Optional[str] = data.get('displayName')
        self.display_icon: Optional[str] = data.get('displayIcon')
        self.asset_path: Optional[str] = data.get('assetPath')
    
    def __str__(self):
        return self._display_name or ''
    
    @property
    def display_name(self):
        """The display name of the Buddy Level. This value changes depending on the language you have set.
        You can also get this value (if not `None`) by using `str(BuddyLevel)`"""
        return self._display_name

class Buddy:
    """
    Represents a Weapon Buddy object

    https://valorantinfo.gg/buddies/

    Attributes
    ----------

    uuid: :class:`Optional[str]`
        The UUID of the Buddy
    display_name: :class:`Optional[str]`
        The display name of the Buddy. This value changes depending on the language you have set
    is_hidden_if__not_owner: :class:`bool`
        Whether the Buddy is hidden if the user is not the owner
    theme_uuid: :class:`Optional[str]`
        The UUID of the Buddy's theme
    display_icon: :class:`Optional[str]`
        The display icon URL of the Buddy
    asset_path: :class:`Optional[str]`
        The asset path of the Buddy
    levels: :class:`List[BuddyLevel]`
        A list of BuddyLevel objects of this Buddy
    
    Operations
    ----------
        **str(Buddy)**
        Returns the display name of the Buddy. If None, returns an empty string
    """
    def __init__(self, data: Dict[str,Any]):
        self.uuid: Optional[str] = data.get('uuid')
        self._display_name: Optional[str] = data.get('displayName')
        self.is_hidden_if__not_owner: Optional[bool] = data.get('isHiddenIfNotOwned')
        self.theme_uuid: Optional[str] = data.get('themeUuid')
        self.display_icon: Optional[str] = data.get('displayIcon')
        self.asset_path: Optional[str] = data.get('assetPath')
        self.levels: List[BuddyLevel] = [BuddyLevel(info) for info in data.get('levels',[])] if data.get('levels') else []
        self._raw = data
    
    def __str__(self):
        return self._display_name or ''
    
    @property
    def display_name(self):
        """The display name of the Buddy. This value changes depending on the language you have set.
        You can also get this value (if not `None`) by using `str(Buddy)`"""
        return self._display_name