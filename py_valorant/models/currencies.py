from typing import Any, Dict, Optional

class CurrencyIcon:
    def __init__(self, display_icon: Optional[str], large_icon: Optional[str]):
        self._display_icon = display_icon
        self._large_icon = large_icon
        
    @property
    def display_icon(self) -> Optional[str]:
        """The URL of the currency's display icon."""
        return self._display_icon
    @property
    def large_icon(self) -> Optional[str]:
        """The URL of the currency's display icon but bigger."""
        return self._large_icon

class Currency:
    """
    Represents a currency (in-game money) object

    Attributes
    ----------
    uuid: :class:`Optional[str]`
        The UUID of the currency
    display_name: :class:`Optional[str]`
        The display name of the currency. This value changes depending on the language you have set.
    display_name_singular: :class:`Optional[str]`
        Same as `display_name` but with singular instead of plural
    display_icon: :class:`Optional[CurrencyIcon]`
        An icon object of the currency
    asset_path: :class:`Optional[str]`
        The asset path of the currency

    Operations
    ----------
        **str(Currency)**
        Returns the display name or display name singular of the currency. If None, returns an empty string
    """
    def __init__(self, data: Dict[str,Any]):
        self.uuid: Optional[str] = data.get('uuid')
        self._display_name: Optional[str] = data.get('displayName')
        self._display_name_singular: Optional[str] = data.get('displayNameSingular')
        self.display_icon: Optional[CurrencyIcon] = CurrencyIcon(data.get('displayIcon'),data.get('largeIcon')) \
        if data.get('displayIcon') or data.get('largeIcon') else None
        self.asset_path: Optional[str] = data.get('assetPath')
        self._raw = data
    
    def __str__(self):
        return self._display_name or self._display_name_singular or ''

    @property
    def display_name(self) -> Optional[str]:
        """The display name of the currency. This value changes depending on the language you have set.
        You can also get this value (if not `None`) by using `str(Currency)`"""
        return self._display_name
    @property
    def display_name_singular(self) -> Optional[str]:
        """Same as `display_name` but with singular instead of plural."""
        return self._display_name_singular