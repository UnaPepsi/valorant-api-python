from typing import Optional, Dict, Any

class BundleIcon:
    def __init__(self, data: Dict[str,Any]):
        self._display_icon: Optional[str] = data.get('displayIcon')
        self._display_icon_2: Optional[str] = data.get('displayIcon2')
        self._logo_icon: Optional[str] = data.get('logoIcon')
    
    def __str__(self):
        return self._display_icon or ''
    
    @property
    def display_icon(self) -> Optional[str]:
        """The URL of the bundle's display icon."""
        return self._display_icon
    
    @property
    def display_icon_2(self) -> Optional[str]:
        """Same as `display_icon`. You shouldn't need to use this."""
        return self._display_icon_2

    @property
    def logo_icon(self) -> Optional[str]:
        """The URL of the bundle's logo icon."""
        return self._logo_icon

class Bundle:
    """
    Represents a Bundle object (multiple skins and other items in a single package purchase)

    Attributes
    ----------
    uuid: :class:`Optional[str]`
        The UUID of the bundle
    display_name: :class:`Optional[str]`
        The display name of the bundle. This value changes depending on the language you have set.
    display_name_subtext: :class:`Optional[str]`
        The display name subtext of the bundle. This value changes depending on the language you have set.
    description: :class:`Optional[str]`
        The description of the bundle. This value changes depending on the language you have set. This value is usually the same as `display_name`
    extra_description: :class:`Optional[str]`
        The extra description of the bundle. This value changes depending on the language you have set.
    promo_description: :class:`Optional[str]`
        The promo description of the bundle. This value changes depending on the language you have set.
    use_additional_context: :class:`Optional[bool]`
        Whether if this bundle has additional context (`extra_descripton` and/or `promo_description`)
    icon: :class:`Optional[BundleIcon]`
        An icon object of the bundle

    Operations
    ----------
        **str(Bundle)**
        Returns the display name or the description of the bundle. If None, returns an empty string
    """
    def __init__(self, data: Dict[str,Any]):
        self.uuid: Optional[str] = data.get('uuid')
        self._display_name: Optional[str] = data.get('displayName')
        self._display_name_subtext: Optional[str] = data.get('displayNameSubText')
        self._description: Optional[str] = data.get('description')
        self._extra_description: Optional[str] = data.get('extraDescription')
        self._promo_description: Optional[str] = data.get('promoDescription')
        self.use_additional_context: Optional[bool] = data.get('useAdditionalContext')
        self.icon: Optional[BundleIcon] = BundleIcon(data) if data.get('displayIcon') else None
        self._raw = data
    
    def __str__(self):
        return self._display_name or self._description or ''
    
    @property
    def display_name(self) -> Optional[str]:
        """The display name of the bundle. This value changes depending on the language you have set.
        You can also get this value (if not `None`) by using `str(Bundle)`"""
        return self._display_name
    
    @property
    def display_name_subtext(self) -> Optional[str]:
        """The display name subtext of the bundle. This value changes depending on the language you have set."""
        return self._display_name_subtext
    
    @property
    def description(self) -> Optional[str]:
        """The description of the bundle. This value changes depending on the language you have set."""
        return self._description
    
    @property
    def extra_description(self) -> Optional[str]:
        """The extra description of the bundle. This value changes depending on the language you have set."""
        return self._extra_description
    
    @property
    def promo_description(self) -> Optional[str]:
        """The promo description of the bundle. This value changes depending on the language you have set."""
        return self._promo_description