from typing import Dict, Any, Optional, List
from numpy import int32

class ContractChapterReward:
    def __init__(self, data: Dict[str,Any]):
        self.type: Optional[str] = data.get('type')
        self.uuid: Optional[str] = data.get('uuid')
        self.amount: Optional[int32] = int32(data.get('amount',0)) if data.get('amount',None) is not None else None
        self.is_highlighted: Optional[bool] = data.get('isHighlighted')

class ContractChapterLevel:
    def __init__(self, data: Dict[str,Any]):
        self.reward: Optional[ContractChapterReward] = ContractChapterReward(data.get('reward',{})) if data.get('reward') else None
        self.xp: Optional[int32] = int32(data.get('xp',0)) if data.get('xp',None) is not None else None
        self.vp_cost: Optional[int32] = int32(data.get('vpCost',0)) if data.get('vpCost',None) is not None else None
        self.is_purchasable_with_vp: Optional[bool] = data.get('isPurchasableWithVP')
        self.dough_cost: Optional[int32] = int32(data.get('doughCost',0)) if data.get('doughCost',None) is not None else None
        self.is_purchasable_with_dough: Optional[bool] = data.get('isPurchasableWithDough')

class ContractFreeReward:
    def __init__(self, data: Dict[str,Any]):
        self.type: Optional[str] = data.get('type')
        self.uuid: Optional[str] = data.get('uuid')
        self.amount: Optional[int32] = int32(data.get('amount',0)) if data.get('amount',None) is not None else None
        self.is_highlighted: Optional[bool] = data.get('isHighlighted')

class ContractChapter:
    def __init__(self, data: Dict[str,Any]):
        self.is_epilogue: Optional[bool] = data.get('isEpilogue')
        self.levels: List[ContractChapterLevel] = [ContractChapterLevel(info) for info in data.get('levels',[])]
        self.free_rewards: List[ContractFreeReward] = [ContractFreeReward(info) for info in data.get('freeRewards',[])]

class ContractContent:
    def __init__(self, data: Dict[str,Any]):
        self.relation_type: Optional[str] = data.get('relationType')
        self.relation_uuid: Optional[str] = data.get('relationUuid')
        self.chapters: List[ContractChapter] = [ContractChapter(info) for info in data.get('chapters',[])]
        self.premium_reward_schedule_uuid: Optional[str] = data.get('premiumRewardScheduleUuid')
        self.premium_vp_cost: Optional[int32] = int32(data.get('premiumVPCost',0)) if data.get('premiumVPCost',None) is not None else None

class Contract:
    def __init__(self, data: Dict[str,Any]):
        self.uuid: Optional[str] = data.get('uuid')
        self._display_name: Optional[str] = data.get('displayName')
        self.display_icon: Optional[str] = data.get('displayIcon')
        self.ship_it: Optional[bool] = data.get('shipIt')
        self.use_level_vp_cost_override: Optional[bool] = data.get('useLevelVPCostOverride')
        self.level_vp_cost_overrride: Optional[int32] = int32(data.get('levelVPCostOverride',0)) if data.get('levelVPCostOverride',None) is not None else None
        self.free_reward_scheduled: Optional[bool] = data.get('freeRewardScheduled')
        self.content: Optional[ContractContent] = ContractContent(data.get('content',{})) if data.get('content') else None
        self.asset_path: Optional[str] = data.get('assetPath')
        self._raw = data
    
    def __str__(self):
        return self._display_name or ''

    @property
    def display_name(self):
        """Returns the display name of the contract. This value changes depending on the language you have set."""
        return self._display_name