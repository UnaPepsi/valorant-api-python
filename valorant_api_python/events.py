from typing import Any, Dict, Optional
from datetime import datetime

class Event:
    """
    Represents a Valorant Event object

    Attributes
    ----------
    uuid: :class:`Optional[str]`
        The UUID of the event
    display_name: :class:`Optional[str]`
        The display name of the event. This value changes depending on the language you have set.
    short_display_name: :class:`Optional[str]`
        The short display name of the event. This value changes depending on the language you have set.
    start_time: :class:`Optional[datetime]`
        The start time of the event
    end_time: :class:`Optional[datetime]`
        The end time of the event
    asset_path: :class:`Optional[str]`
        The asset path of the event

    Operations
    ----------
        **str(Event)**
        Returns the display name or the short display name of the event. If None, returns an empty string
    """
    def __init__(self, data: Dict[str,Any]):
        self.uuid: Optional[str] = data.get('uuid')
        self._display_name: Optional[str] = data.get('displayName')
        self._short_display_name: Optional[str] = data.get('shortDisplayName')
        self.start_time: Optional[datetime] = datetime.strptime(data.get('startTime',''),'%Y-%m-%dT%H:%M:%SZ') if data.get('startTime') else None
        self.end_time: Optional[datetime] = datetime.strptime(data.get('endTime',''),'%Y-%m-%dT%H:%M:%SZ') if data.get('endTime') else None
        self.asset_path: Optional[str] = data.get('assetPath')
        self._raw = data
    
    def __str__(self):
        return self._display_name or self._short_display_name or ''
    
    @property
    def display_name(self) -> Optional[str]:
        """The display name of the event. This value changes depending on the language you have set."""
        return self._display_name
    
    @property
    def short_display_name(self) -> Optional[str]:
        """The short display name of the event. This value changes depending on the language you have set."""
        return self._short_display_name