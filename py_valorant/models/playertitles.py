from typing import Any, Dict, Optional

class PlayerTitle:
    """
    Represents a Player Title object

    Attributes
    ----------
    uuid: :class:`Optional[str]`
        The UUID of the Player Title
    display_name: :class:`Optional[str]`
        The display name of the Player Title. This value changes depending on the language you have set
    title_text: :class:`Optional[str]`
        The title text of the Player Title. This value changes depending on the language you have set
    is_hidden_if_not_owned: :class:`bool`
        Whether the Player Title is hidden if the user is not the owner
    asset_path: :class:`Optional[str]`
        The asset path of the Player Title

    Operations
    ----------
        **str(x)**
        Returns the display name of the Player Title
    """
    def __init__(self, data: Dict[str,Any]):
        self.uuid: Optional[str] = data.get('uuid')
        self._display_name: Optional[str] = data.get('displayName')
        self._title_text: Optional[str] = data.get('titleText')
        self.is_hidden_if_not_owned: Optional[bool] = data.get('isHiddenIfNotOwned')
        self.asset_path: Optional[str] = data.get('assetPath')
        self._raw = data

    def __str__(self):
        return self._display_name or ''
    
    @property
    def display_name(self):
        """The display name of the Player Title. This value changes depending on the language you have set.
        You can also get this value (if not `None`) by using `str(PlayerTitle)`"""
        return self._display_name

    @property
    def title_text(self):
        """The title text of the Player Title. This value changes depending on the language you have set.
        You can also get this value (if not `None`) by using `str(PlayerTitle)`"""
        return self._title_text