from typing import Any, Dict, Optional

class PlayerCardImage:
    def __init__(self, display_icon: Optional[str], small_art: Optional[str], wide_art: Optional[str], large_art: Optional[str]):
        self.display_icon = display_icon
        self.small_art = small_art
        self.wide_art = wide_art
        self.large_art = large_art

class PlayerCard:
    """
    Represents a Player Card object

    Attributes
    ----------
    uuid: :class:`Optional[str]`
        The UUID of the Player Card
    display_name: :class:`Optional[str]`
        The display name of the Player Card. This value changes depending on the language you have set
    is_hidden_if__not_owned: :class:`bool`
        Whether the Player Card is hidden if the user is not the owner
    theme_uuid: :class:`Optional[str]`
        The UUID of the Player Card's theme
    image: :class:`Optional[PlayerCardImage]`
        An Image object of the Player Card
    asset_path: :class:`Optional[str]`
        The asset path of the Player Card
    
    Operations
    ----------
        **str(x)**
        Returns the display name of the Player Card
    """
    def __init__(self, data: Dict[str,Any]):
        self.uuid: Optional[str] = data.get('uuid')
        self._display_name: Optional[str] = data.get('displayName')
        self.is_hidden_if__not_owned: Optional[bool] = data.get('isHiddenIfNotOwned')
        self.theme_uuid: Optional[str] = data.get('themeUuid')
        self.image: Optional[PlayerCardImage] = PlayerCardImage(data.get('displayIcon'),data.get('smallArt'),data.get('wideArt'),data.get('largeArt')) \
        if data.get('displayIcon') is not None else None
        self.asset_path: Optional[str] = data.get('assetPath')
        self._raw = data

    def __str__(self):
        return self._display_name or ''
    
    @property
    def display_name(self):
        """The display name of the Player Card. This value changes depending on the language you have set.
        You can also get this value (if not `None`) by using `str(PlayerCard)`"""
        return self._display_name