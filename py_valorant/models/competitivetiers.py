from typing import Dict, Any, Optional, List
from numpy import int32

class TierIcon:
    def __init__(self, small_icon: Optional[str], large_icon: Optional[str],
                rank_trialgle_down_icon: Optional[str], rank_triangle_up_icon: Optional[str]):
        self._small_icon = small_icon
        self._large_icon = large_icon
        self._rank_triangle_down_icon = rank_trialgle_down_icon
        self._rank_triangle_up_icon = rank_triangle_up_icon
    
    @property
    def small_icon(self) -> Optional[str]:
        """The URL of the small icon of the tier."""
        return self._small_icon
    @property
    def large_icon(self) -> Optional[str]:
        """The URL of the large icon of the tier."""
        return self._large_icon
    @property
    def rank_triangle_down_icon(self) -> Optional[str]:
        """The URL of the rank triangle down icon of the tier."""
        return self._rank_triangle_down_icon
    @property
    def rank_triangle_up_icon(self) -> Optional[str]:
        """The URL of the rank triangle up icon of the tier."""
        return self._rank_triangle_up_icon

class Tier:
    def __init__(self, data: Dict[str,Any]):
        self.tier: Optional[int32] = int32(data.get('tier',0)) if data.get('tier',None) is not None else None
        self._name: Optional[str] = data.get('tierName')
        self.division: Optional[str] = data.get('division')
        self._division_name: Optional[str] = data.get('divisionName')
        self.color: Optional[str] = data.get('color')
        self.background_color: Optional[str] = data.get('backgroundColor')
        self.icon: Optional[TierIcon] = TierIcon(data.get('small_icon'),
                                                data.get('large_icon'),
                                                data.get('rank_triangle_down_icon'),
                                                data.get('rank_triangle_up_icon')) if data.get('small_icon') else None
    
    @property
    def name(self) -> Optional[str]:
        """The name of the tier. This value changes depending on the language you have set.
        You can also get this value (if not `None`) by using `str(Tier)`"""
        return self._name
    
    @property
    def division_name(self) -> Optional[str]:
        """The name of the division. This value changes depending on the language you have set.
        You can also get this value (if not `None`) by using `str(Tier)`"""
        return self._division_name

    def __str__(self):
        return self._name or self._division_name or ''
class CompetitiveTier:
    """
    Represents a competitive tier (rank) object

    Attributes
    ----------
    uuid: :class:`Optional[str]`
        The UUID of the competitive tier
    asset_object_name: :class:`Optional[str]`
        The asset object name of the competitive tier. This is also the name of the episode
    tier: :class:`Optional[List[Tier]]`
        A list of Tier objects of the competitive tier
    asset_path: :class:`Optional[str]`
        The asset path of the competitive tier
    """
    def __init__(self, data: Dict[str,Any]):
        self.uuid: Optional[str] = data.get('uuid')
        self.asset_object_name: Optional[str] = data.get('assetObjectName') #episodes
        self.tiers: List[Tier] = [Tier(info) for info in data.get('tiers',[])]
        self.asset_path: Optional[str] = data.get('assetPath')
        self._filter_unused_tiers: List[Tier] = list(filter(lambda tier: tier.name and 'Unused' not in tier.name, self.tiers))
        self._raw = data