from typing import Any, Dict, Optional

class Ceremony:
    """
    Represents a Ceremony object (the message that appears in a big bar)

    https://i.imgur.com/KwzV2U6.png (example)

    Attributes
    ----------
    uuid: :class:`Optional[str]`
        The UUID of the ceremony
    display_name: :class:`Optional[str]`
        The display name of the ceremony. This value changes depending on the language you have set
    asset_path: :class:`Optional[str]`
        The asset path of the ceremony
    
    Operations
    ----------
        **str(Ceremony)**
        Returns the display name of the ceremony. If None, returns an empty string
    """
    def __init__(self, data: Dict[str,Any]):
        self.uuid: Optional[str] = data.get('uuid')
        self._display_name: Optional[str] = data.get('displayName')
        self.asset_path: Optional[str] = data.get('assetPath')
        self._raw = data
    
    @property
    def display_name(self):
        """The display name of the Ceremony. This value changes depending on the language you have set.
        You can also get this value (if not `None`) by using `str(Ceremony)`"""
        return self._display_name

    def __str__(self):
        return self._display_name or ''