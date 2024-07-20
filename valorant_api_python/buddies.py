from typing import Optional, Dict, Any, List

class BuddyLevel:
    def __init__(self, data: Dict[str,Any]):
        self.uuid: Optional[str] = data.get('uuid')
        self.charm_level: Optional[int] = data.get('charmLevel')
        self.hide_if_not_found: Optional[bool] = data.get('hideIfNotFound')
        self._display_name: Optional[str] = data.get('displayName')
        self.display_icon: Optional[str] = data.get('displayIcon')
        self.asset_path: Optional[str] = data.get('asset_path')
    
    def __str__(self):
        return self._display_name or ''
    
    @property
    def display_name(self):
        """The display name of the Buddy Level. This value changes depending on the language you have set.
        You can also get this value by using `str(BuddyLevel)`"""
        return self._display_name

class Buddy:
    def __init__(self, data: Dict[str,Any]):
        self.uuid: Optional[str] = data.get('uuid')
        self._display_name: Optional[str] = data.get('displayName')
        self.is_hidden_if__not_owner: Optional[bool] = data.get('isHiddenIfNotOwner')
        self.theme_uuid: Optional[str] = data.get('themeUuid')
        self.display_icon: Optional[str] = data.get('displayIcon')
        self.asset_path: Optional[str] = data.get('assetPath')
        self.levels: List[BuddyLevel] = data.get('levels',[])
    
    def __str__(self):
        return self._display_name or ''
    
    @property
    def display_name(self):
        """The display name of the Buddy. This value changes depending on the language you have set.
        You can also get this value by using `str(Buddy)`"""
        return self._display_name