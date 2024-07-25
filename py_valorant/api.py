import aiohttp
import requests
from .errors import *
from typing import Literal, List, Dict, Any, Union, get_args, Optional
from .models.agents import Agent
from .models.buddies import Buddy, BuddyLevel
from .models.bundles import Bundle
from .models.ceremonies import Ceremony
from .models.competitivetiers import CompetitiveTier
from .models.contenttiers import ContentTier
from .models.contracts import Contract
from .models.currencies import Currency
from .models.events import Event
from .models.gamemodes import Gamemode, GamemodeEquipable
from .models.gears import Gear
from .models.levelborders import LevelBorder
from .models.maps import Map
from .models.playercards import PlayerCard
from .models.playertitles import PlayerTitle
from .models.sprays import Spray, SprayLevel
from .cache import *

BASE = "https://valorant-api.com/v1"
LANGUAGE = Literal['ar-AE','de-DE','en-US','es-ES','es-MX','fr-FR','id-ID','it-IT','ja-JP','ko-KR','pl-PL','pt-BR','ru-RU','th-TH','tr-TR','vi-VN','zh-CN','zh-TW']

class ValorantAPI:

	def __init__(self, language: LANGUAGE = 'en-US'):
		assert language in get_args(LANGUAGE), "Invalid language type. Valid languages: %s"%(get_args(LANGUAGE),)
		self._language = language
		self._session = SyncClient()
		self.agent = SyncAgentEndpoint(self)
		self.buddy = SyncBuddyEndpoint(self)
		self.bundle = SyncBundleEndpoint(self)
		self.competitive_tier = SyncCompetitiveTierEndpoint(self)
		self.content_tier = SyncContentTierEndpoint(self)
		self.contract = SyncContractEndpoint(self)
		self.currency = SyncCurrencyEndpoint(self)
		self.event = SyncEventEndpoint(self)
		self.gamemode = SyncGamemodeEndpoint(self)
		self.gamemode_equipable = SyncGamemodeEquipableEndpoint(self)
		self.gear = SyncGearEndpoint(self)
		self.level_border = SyncLevelBorderEndpoint(self)
		self.map = SyncMapEndpoint(self)
		self.player_card = SyncPlayerCardEndpoint(self)
		self.player_title = SyncPlayerTitleEndpoint(self)
		self.spray = SyncSprayEndpoint(self)

	@property
	def language(self):
		return self._language
	@language.setter
	def language(self,language: LANGUAGE):
		assert language in get_args(LANGUAGE), "Invalid language type. Valid languages: %s"%(get_args(LANGUAGE),)
		self._language = language

class ValorantAPIAsync(ValorantAPI): #This is probably just repeating but if I do in ValorantAPI type checker yells because comparing coroutines with functions
	def __init__(self, language: LANGUAGE = 'en-US'):
		super().__init__(language=language)
		self._session = AsyncClient()
		self.agent = AsyncAgentEndpoint(self)
		self.buddy = AsyncBuddyEndpoint(self)
		self.bundle = AsyncBundleEndpoint(self)
		self.competitive_tier = AsyncCompetitiveTierEndpoint(self)
		self.content_tier = AsyncContentTierEndpoint(self)
		self.contract = AsyncContractEndpoint(self)
		self.currency = AsyncCurrencyEndpoint(self)
		self.event = AsyncEventEndpoint(self)
		self.gamemode = AsyncGamemodeEndpoint(self)
		self.gamemode_equipable = AsyncGamemodeEquipableEndpoint(self)
		self.gear = AsyncGearEndpoint(self)
		self.level_border = AsyncLevelBorderEndpoint(self)
		self.map = AsyncMapEndpoint(self)
		self.player_card = AsyncPlayerCardEndpoint(self)
		self.player_title = AsyncPlayerTitleEndpoint(self)
		self.spray = AsyncSprayEndpoint(self)
		
class SyncClient:
	def get(self, endpoint: str, **params) -> Dict[str,Any]:
		resp = requests.request('GET',BASE + endpoint, params=params)
		data: Dict[str,Any] = resp.json()
		if resp.status_code == 200:
			return data
		if resp.status_code == 400:
			raise InvalidOrMissingParameters(data['status'],'Invalid or missing parameters')
		elif resp.status_code == 404:
			raise UUIDNotFound(data['status'],'UUID not valid')
		raise BaseException(data['status'],data['error'])
	
class AsyncClient:
	async def get(self, endpoint: str, **params) -> Dict[str,Any]:
		if params.get('isPlayableCharacter') is not None:
			# https://github.com/aio-libs/yarl#why-isnt-boolean-supported-by-the-url-query-api
			params['isPlayableCharacter'] = str(params['isPlayableCharacter']).lower()
		else:
			params.pop('isPlayableCharacter',None)
		async with aiohttp.ClientSession() as sess:
			async with sess.request('GET', BASE + endpoint, params=params) as resp:
				data: Dict[str,Any] = await resp.json()
				if resp.status == 200:
					return data
				if resp.status == 400:
					raise InvalidOrMissingParameters(data['status'],'Invalid or missing parameters')
				elif resp.status == 404:
					raise UUIDNotFound(data['status'],'UUID not valid')
				raise BaseException(data['status'],data['error'])

#Endpoints
class BaseEndpoint:
	def __init__(self, client: Union[ValorantAPI,ValorantAPIAsync]):
		self._client = client
	
	@property
	def client(self):
		"""The client of this endpoint"""
		return self._client

class SyncAgentEndpoint(BaseEndpoint):
	@sync_caching
	def fetch_all(self, is_playable_character: Optional[bool] = None, *, cache: Optional[bool] = False) -> List[Agent]:
		"""Fetches all agents' data from the API.
		
		Parameters
		----------
		is_playable_character : `Optional[bool]`
			According to https://dash.valorant-api.com/endpoints/agents set this to `True` to remove possible duplicates
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,AsyncClient):
			raise ValueError('Invalid session type')
		data = self._client._session.get('/agents',language=self._client.language,isPlayableCharacter=is_playable_character)
		return [Agent(info) for info in data.get('data',[])]
	
	@sync_caching
	def fetch_from_uuid(self,uuid: str, *, cache: Optional[bool] = False) -> Agent:
		"""Fetches an agent's data
		
		Parameters
		----------
		uuid : `str`
			The UUID of the Agent
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,AsyncClient):
			raise ValueError('Invalid session type')
		data = self._client._session.get('/agents/%s'%uuid,language=self._client.language)
		return Agent(data.get('data',{}))
	
class AsyncAgentEndpoint(BaseEndpoint):
	@async_caching
	async def fetch_all(self, is_playable_character: Optional[bool] = None, *, cache: Optional[bool] = False) -> List[Agent]:
		"""Fetches all agents' data from the API.
		
		Parameters
		----------
		is_playable_character : `Optional[bool]`
			According to https://dash.valorant-api.com/endpoints/agents set this to `True` to remove possible duplicates
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,SyncClient):
			raise ValueError('Invalid session type')
		data = await self._client._session.get('/agents',language=self._client.language,isPlayableCharacter=is_playable_character)
		return [Agent(info) for info in data.get('data',[])]
			
	@async_caching
	async def fetch_from_uuid(self,uuid: str, *, cache: Optional[bool] = False) -> Agent:
		"""Fetches an agent's data
		
		Parameters
		----------
		uuid : `str`
			The UUID of the Agent
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,SyncClient):
			raise ValueError('Invalid session type')
		data = await self._client._session.get('/agents/%s'%uuid,language=self._client.language)
		return Agent(data.get('data',{}))

class SyncBuddyEndpoint(BaseEndpoint):
	@sync_caching
	def fetch_all(self, *, cache: Optional[bool] = False) -> List[Buddy]:
		"""Fetches all weapon buddies' data
		
		Parameters
		----------
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,AsyncClient):
			raise ValueError('Invalid session type')
		data = self._client._session.get('/buddies',language=self._client._language)
		return [Buddy(info) for info in data.get('data',[])]
	
	@sync_caching
	def fetch_from_uuid(self, uuid: str, *, cache: Optional[bool] = False) -> Buddy:
		"""
		Fetches a weapon buddy's data
		
		Parameters
		----------
		uuid : `str`
			The UUID of the Buddy
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,AsyncClient):
			raise ValueError('Invalid session type')
		data = self._client._session.get('/buddies/%s'%uuid,language=self.client._language)
		return Buddy(data.get('data',{}))
	
	@sync_caching
	def fetch_all_levels(self, *, cache: Optional[bool] = False) -> List[BuddyLevel]:
		"""Fetches all weapon buddy levels' data
		
		Parameters
		----------
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,AsyncClient):
			raise ValueError('Invalid session type')
		data = self._client._session.get('/buddies/levels',language=self._client._language)
		return [BuddyLevel(info) for info in data.get('data',[])]
	
	@sync_caching
	def fetch_level_from_uuid(self,uuid: str, *, cache: Optional[bool] = False) -> BuddyLevel:
		"""Fetches a weapon buddy level's data
		
		Parameters
		----------
		uuid : `str`
			The UUID of the Buddy Level
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,AsyncClient):
			raise ValueError('Invalid session type')
		data = self._client._session.get('/buddies/levels/%s'%uuid,language=self._client._language)
		return BuddyLevel(data.get('data',{}))

class AsyncBuddyEndpoint(BaseEndpoint):
	@async_caching
	async def fetch_all(self, *, cache: Optional[bool] = False) -> List[Buddy]:
		"""Fetches all weapon buddies' data
		
		Parameters
		----------
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,SyncClient):
			raise ValueError('Invalid session type')
		data = await self._client._session.get('/buddies',language=self._client._language)
		return [Buddy(info) for info in data.get('data',[])]
	
	@async_caching
	async def fetch_from_uuid(self, uuid: str, *, cache: Optional[bool] = False) -> Buddy:
		"""
		Fetches a weapon buddy's data
		
		Parameters
		----------
		uuid : `str`
			The UUID of the Buddy
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,SyncClient):
			raise ValueError('Invalid session type')
		data = await self._client._session.get('/buddies/%s'%uuid,language=self.client._language)
		return Buddy(data.get('data',{}))
	
	@async_caching
	async def fetch_all_levels(self, *, cache: Optional[bool] = False) -> List[BuddyLevel]:
		"""Fetches all weapon buddy levels' data
		
		Parameters
		----------
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,SyncClient):
			raise ValueError('Invalid session type')
		data = await self._client._session.get('/buddies/levels',language=self._client._language)
		return [BuddyLevel(info) for info in data.get('data',[])]
	
	@async_caching
	async def fetch_level_from_uuid(self,uuid: str, *, cache: Optional[bool] = False) -> BuddyLevel:
		"""Fetches a weapon buddy level's data
		
		Parameters
		----------
		uuid : `str`
			The UUID of the Buddy Level
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,SyncClient):
			raise ValueError('Invalid session type')
		data = await self._client._session.get('/buddies/levels/%s'%uuid,language=self._client._language)
		return BuddyLevel(data.get('data',{}))

class SyncBundleEndpoint(BaseEndpoint):
	@sync_caching
	def fetch_all(self, *, cache: Optional[bool] = False) -> List[Bundle]:
		"""Fetches all bundles' data
		
		Parameters
		----------
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,AsyncClient):
			raise ValueError('Invalid session type')
		data = self._client._session.get('/bundles',language=self._client._language)
		return [Bundle(info) for info in data.get('data',[])]
	
	@sync_caching
	def fetch_from_uuid(self, uuid: str, *, cache: Optional[bool] = False) -> Bundle:
		"""
		Fetches a bundles's data
		
		Parameters
		----------
		uuid : `str`
			The UUID of the Bundle
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,AsyncClient):
			raise ValueError('Invalid session type')
		data = self._client._session.get('/bundles/%s'%uuid,language=self.client._language)
		return Bundle(data.get('data',{}))
	
class AsyncBundleEndpoint(BaseEndpoint):
	@sync_caching
	async def fetch_all(self, *, cache: Optional[bool] = False) -> List[Bundle]:
		"""Fetches all bundles' data
		
		Parameters
		----------
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,SyncClient):
			raise ValueError('Invalid session type')
		data = await self._client._session.get('/bundles',language=self._client._language)
		return [Bundle(info) for info in data.get('data',[])]
	
	@sync_caching
	async def fetch_from_uuid(self, uuid: str, *, cache: Optional[bool] = False) -> Bundle:
		"""
		Fetches a bundles's data
		
		Parameters
		----------
		uuid : `str`
			The UUID of the Bundle
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,SyncClient):
			raise ValueError('Invalid session type')
		data = await self._client._session.get('/bundles/%s'%uuid,language=self._client._language)
		return Bundle(data.get('data',{}))

class SyncCeremonyEndpoint(BaseEndpoint):
	@sync_caching
	def fetch_all(self, *, cache: Optional[bool] = False) -> List[Ceremony]:
		"""Fetches all ceremonies' data
		
		Parameters
		----------
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,AsyncClient):
			raise ValueError('Invalid session type')
		data = self._client._session.get('/ceremonies',language=self._client._language)
		return [Ceremony(info) for info in data.get('data',[])]
	
	@sync_caching
	def fetch_from_uuid(self, uuid: str, *, cache: Optional[bool] = False) -> Ceremony:
		"""
		Fetches a ceremony's data
		
		Parameters
		----------
		uuid : `str`
			The UUID of the Ceremony
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,AsyncClient):
			raise ValueError('Invalid session type')
		data = self._client._session.get('/ceremonies/%s'%uuid,language=self.client._language)
		return Ceremony(data.get('data',{}))
	
class AsyncCeremonyEndpoint(BaseEndpoint):
	@sync_caching
	async def fetch_all(self, *, cache: Optional[bool] = False) -> List[Ceremony]:
		"""Fetches all ceremonies' data
		
		Parameters
		----------
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,SyncClient):
			raise ValueError('Invalid session type')
		data = await self._client._session.get('/ceremonies',language=self._client._language)
		return [Ceremony(info) for info in data.get('data',[])]
	
	@sync_caching
	async def fetch_from_uuid(self, uuid: str, *, cache: Optional[bool] = False) -> Ceremony:
		"""
		Fetches a ceremony's data
		
		Parameters
		----------
		uuid : `str`
			The UUID of the Ceremony
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,SyncClient):
			raise ValueError('Invalid session type')
		data = await self._client._session.get('/ceremonies/%s'%uuid,language=self._client._language)
		return Ceremony(data.get('data',{}))
	
class SyncCompetitiveTierEndpoint(BaseEndpoint):
	@sync_caching
	def fetch_all(self, remove_unused: Optional[bool] = False, *, cache: Optional[bool] = False) -> List[CompetitiveTier]:
		"""Fetches all competitive tiers' data
		
		Parameters
		----------
		remove_unused : `Optional[bool]`
			Filter out tiers with name 'Unused'
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,AsyncClient):
			raise ValueError('Invalid session type')
		data = self._client._session.get('/competitivetiers',language=self._client._language)
		comp_tiers =  [CompetitiveTier(info) for info in data.get('data',[])]
		if remove_unused:
			for comp in comp_tiers:
				for tier in list(comp.tiers):
					if tier.name and 'Unused' in tier.name:
						comp_tiers[comp_tiers.index(comp)].tiers.remove(tier)
		return comp_tiers

	
	@sync_caching
	def fetch_from_uuid(self, uuid: str, *, cache: Optional[bool] = False) -> CompetitiveTier:
		"""
		Fetches a competitive tier's data
		
		Parameters
		----------
		uuid : `str`
			The UUID of the Competitive Tier
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,AsyncClient):
			raise ValueError('Invalid session type')
		data = self._client._session.get('/competitivetiers/%s'%uuid,language=self.client._language)
		return CompetitiveTier(data.get('data',{}))
	
class AsyncCompetitiveTierEndpoint(BaseEndpoint):
	@async_caching
	async def fetch_all(self, remove_unused: Optional[bool] = False, *, cache: Optional[bool] = False) -> List[CompetitiveTier]:
		"""Fetches all competitive tiers' data
		
		Parameters
		----------
		remove_unused : `Optional[bool]`
			Filter out tiers with name 'Unused'
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,SyncClient):
			raise ValueError('Invalid session type')
		data = await self._client._session.get('/competitivetiers',language=self._client._language)
		comp_tiers = [CompetitiveTier(info) for info in data.get('data',[])]
		if remove_unused:
			for comp in comp_tiers:
				for tier in list(comp.tiers):
					if tier.name and 'Unused' in tier.name:
						comp_tiers[comp_tiers.index(comp)].tiers.remove(tier)
		return comp_tiers
	
	@async_caching
	async def fetch_from_uuid(self, uuid: str, *, cache: Optional[bool] = False) -> CompetitiveTier:
		"""
		Fetches a competitive tier's data
		
		Parameters
		----------
		uuid : `str`
			The UUID of the Competitive Tier
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,SyncClient):
			raise ValueError('Invalid session type')
		data = await self._client._session.get('/competitivetiers/%s'%uuid,language=self._client._language)
		return CompetitiveTier(data.get('data',{}))

class SyncContentTierEndpoint(BaseEndpoint):
	@sync_caching
	def fetch_all(self, *, cache: Optional[bool] = False) -> List[ContentTier]:
		"""Fetches all content tiers' data
		
		Parameters
		----------
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,AsyncClient):
			raise ValueError('Invalid session type')
		data = self._client._session.get('/contenttiers',language=self._client._language)
		return [ContentTier(info) for info in data.get('data',[])]

	
	@sync_caching
	def fetch_from_uuid(self, uuid: str, *, cache: Optional[bool] = False) -> ContentTier:
		"""
		Fetches a content tier's data
		
		Parameters
		----------
		uuid : `str`
			The UUID of the Competitive Tier
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,AsyncClient):
			raise ValueError('Invalid session type')
		data = self._client._session.get('/contenttiers/%s'%uuid,language=self.client._language)
		return ContentTier(data.get('data',{}))

class AsyncContentTierEndpoint(BaseEndpoint):
	@async_caching
	async def fetch_all(self, *, cache: Optional[bool] = False) -> List[ContentTier]:
		"""Fetches all content tiers' data
		
		Parameters
		----------
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,SyncClient):
			raise ValueError('Invalid session type')
		data = await self._client._session.get('/contenttiers',language=self._client._language)
		return [ContentTier(info) for info in data.get('data',[])]
	
	@async_caching
	async def fetch_from_uuid(self, uuid: str, *, cache: Optional[bool] = False) -> ContentTier:
		"""
		Fetches a content tier's data
		
		Parameters
		----------
		uuid : `str`
			The UUID of the Competitive Tier
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,SyncClient):
			raise ValueError('Invalid session type')
		data = await self._client._session.get('/contenttiers/%s'%uuid,language=self._client._language)
		return ContentTier(data.get('data',{}))

class SyncContractEndpoint(BaseEndpoint):
	@sync_caching
	def fetch_all(self, *, cache: Optional[bool] = False) -> List[Contract]:
		"""Fetches all contracts' data
		
		Parameters
		----------
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,AsyncClient):
			raise ValueError('Invalid session type')
		data = self._client._session.get('/contracts',language=self._client._language)
		return [Contract(info) for info in data.get('data',[])]

	
	@sync_caching
	def fetch_from_uuid(self, uuid: str, *, cache: Optional[bool] = False) -> Contract:
		"""
		Fetches a contract's data
		
		Parameters
		----------
		uuid : `str`
			The UUID of the Contract
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,AsyncClient):
			raise ValueError('Invalid session type')
		data = self._client._session.get('/contracts/%s'%uuid,language=self.client._language)
		return Contract(data.get('data',{}))

class AsyncContractEndpoint(BaseEndpoint):
	@async_caching
	async def fetch_all(self, *, cache: Optional[bool] = False) -> List[Contract]:
		"""Fetches all contracts' data
		
		Parameters
		----------
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,SyncClient):
			raise ValueError('Invalid session type')
		data = await self._client._session.get('/contracts',language=self._client._language)
		return [Contract(info) for info in data.get('data',[])]
	
	@async_caching
	async def fetch_from_uuid(self, uuid: str, *, cache: Optional[bool] = False) -> Contract:
		"""
		Fetches a contract's data
		
		Parameters
		----------
		uuid : `str`
			The UUID of the Contract
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,SyncClient):
			raise ValueError('Invalid session type')
		data = await self._client._session.get('/contracts/%s'%uuid,language=self._client._language)
		return Contract(data.get('data',{}))

class SyncCurrencyEndpoint(BaseEndpoint):
	@sync_caching
	def fetch_all(self, *, cache: Optional[bool] = False) -> List[Currency]:
		"""Fetches all currencies' data
		
		Parameters
		----------
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,AsyncClient):
			raise ValueError('Invalid session type')
		data = self._client._session.get('/currencies',language=self._client._language)
		return [Currency(info) for info in data.get('data',[])]

	
	@sync_caching
	def fetch_from_uuid(self, uuid: str, *, cache: Optional[bool] = False) -> Currency:
		"""
		Fetches a currency's data
		
		Parameters
		----------
		uuid : `str`
			The UUID of the Currency
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,AsyncClient):
			raise ValueError('Invalid session type')
		data = self._client._session.get('/currencies/%s'%uuid,language=self.client._language)
		return Currency(data.get('data',{}))

class AsyncCurrencyEndpoint(BaseEndpoint):
	@async_caching
	async def fetch_all(self, *, cache: Optional[bool] = False) -> List[Currency]:
		"""Fetches all currencies' data
		
		Parameters
		----------
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,SyncClient):
			raise ValueError('Invalid session type')
		data = await self._client._session.get('/currencies',language=self._client._language)
		return [Currency(info) for info in data.get('data',[])]
	
	@async_caching
	async def fetch_from_uuid(self, uuid: str, *, cache: Optional[bool] = False) -> Currency:
		"""
		Fetches a currency's data
		
		Parameters
		----------
		uuid : `str`
			The UUID of the Currency
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,SyncClient):
			raise ValueError('Invalid session type')
		data = await self._client._session.get('/currencies/%s'%uuid,language=self._client._language)
		return Currency(data.get('data',{}))

class SyncEventEndpoint(BaseEndpoint):
	@sync_caching
	def fetch_all(self, *, cache: Optional[bool] = False) -> List[Event]:
		"""Fetches all events' data
		
		Parameters
		----------
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,AsyncClient):
			raise ValueError('Invalid session type')
		data = self._client._session.get('/events',language=self._client._language)
		return [Event(info) for info in data.get('data',[])]
	
	@sync_caching
	def fetch_from_uuid(self, uuid: str, *, cache: Optional[bool] = False) -> Event:
		"""
		Fetches an event's data
		
		Parameters
		----------
		uuid : `str`
			The UUID of the Event
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,AsyncClient):
			raise ValueError('Invalid session type')
		data = self._client._session.get('/events/%s'%uuid,language=self.client._language)
		return Event(data.get('data',{}))

class AsyncEventEndpoint(BaseEndpoint):
	@async_caching
	async def fetch_all(self, *, cache: Optional[bool] = False) -> List[Event]:
		"""Fetches all events' data
		
		Parameters
		----------
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,SyncClient):
			raise ValueError('Invalid session type')
		data = await self._client._session.get('/events',language=self._client._language)
		return [Event(info) for info in data.get('data',[])]
	
	@async_caching
	async def fetch_from_uuid(self, uuid: str, *, cache: Optional[bool] = False) -> Event:
		"""
		Fetches an event's data
		
		Parameters
		----------
		uuid : `str`
			The UUID of the Event
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,SyncClient):
			raise ValueError('Invalid session type')
		data = await self._client._session.get('/events/%s'%uuid,language=self._client._language)
		return Event(data.get('data',{}))

class SyncGamemodeEndpoint(BaseEndpoint):
	@sync_caching
	def fetch_all(self, *, cache: Optional[bool] = False) -> List[Gamemode]:
		"""Fetches all gamemodes' data
		
		Parameters
		----------
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,AsyncClient):
			raise ValueError('Invalid session type')
		data = self._client._session.get('/gamemodes',language=self._client._language)
		return [Gamemode(info) for info in data.get('data',[])]
	
	@sync_caching
	def fetch_from_uuid(self, uuid: str, *, cache: Optional[bool] = False) -> Gamemode:
		"""
		Fetches a gamemode's data
		
		Parameters
		----------
		uuid : `str`
			The UUID of the Gamemode
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,AsyncClient):
			raise ValueError('Invalid session type')
		data = self._client._session.get('/gamemodes/%s'%uuid,language=self.client._language)
		return Gamemode(data.get('data',{}))

class AsyncGamemodeEndpoint(BaseEndpoint):
	@async_caching
	async def fetch_all(self, *, cache: Optional[bool] = False) -> List[Gamemode]:
		"""Fetches all gamemodes' data
		
		Parameters
		----------
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,SyncClient):
			raise ValueError('Invalid session type')
		data = await self._client._session.get('/gamemodes',language=self._client._language)
		return [Gamemode(info) for info in data.get('data',[])]
	
	@async_caching
	async def fetch_from_uuid(self, uuid: str, *, cache: Optional[bool] = False) -> Gamemode:
		"""
		Fetches a gamemode's data
		
		Parameters
		----------
		uuid : `str`
			The UUID of the Gamemode
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,SyncClient):
			raise ValueError('Invalid session type')
		data = await self._client._session.get('/gamemodes/%s'%uuid,language=self._client._language)
		return Gamemode(data.get('data',{}))

class SyncGamemodeEquipableEndpoint(BaseEndpoint):
	@sync_caching
	def fetch_all(self, *, cache: Optional[bool] = False) -> List[GamemodeEquipable]:
		"""Fetches all gamemode equipables' data
		
		Parameters
		----------
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,AsyncClient):
			raise ValueError('Invalid session type')
		data = self._client._session.get('/gamemodes/equippables',language=self._client._language)
		return [GamemodeEquipable(info) for info in data.get('data',[])]
	
	@sync_caching
	def fetch_from_uuid(self, uuid: str, *, cache: Optional[bool] = False) -> GamemodeEquipable:
		"""
		Fetches a gamemode equipable's data
		
		Parameters
		----------
		uuid : `str`
			The UUID of the Gamemode Equipable
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,AsyncClient):
			raise ValueError('Invalid session type')
		data = self._client._session.get('/gamemodes/equippables/%s'%uuid,language=self.client._language)
		return GamemodeEquipable(data.get('data',{}))

class AsyncGamemodeEquipableEndpoint(BaseEndpoint):
	@async_caching
	async def fetch_all(self, *, cache: Optional[bool] = False) -> List[GamemodeEquipable]:
		"""Fetches all gamemode equipables' data
		
		Parameters
		----------
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,SyncClient):
			raise ValueError('Invalid session type')
		data = await self._client._session.get('/gamemodes/equippables',language=self._client._language)
		return [GamemodeEquipable(info) for info in data.get('data',[])]
	
	@async_caching
	async def fetch_from_uuid(self, uuid: str, *, cache: Optional[bool] = False) -> GamemodeEquipable:
		"""
		Fetches a gamemode equipable's data
		
		Parameters
		----------
		uuid : `str`
			The UUID of the Gamemode Equipable
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,SyncClient):
			raise ValueError('Invalid session type')
		data = await self._client._session.get('/gamemodes/equippables/%s'%uuid,language=self._client._language)
		return GamemodeEquipable(data.get('data',{}))

class SyncGearEndpoint(BaseEndpoint):
	@sync_caching
	def fetch_all(self, *, cache: Optional[bool] = False) -> List[Gear]:
		"""Fetches all gears' data
		
		Parameters
		----------
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,AsyncClient):
			raise ValueError('Invalid session type')
		data = self._client._session.get('/gear',language=self._client._language)
		return [Gear(info) for info in data.get('data',[])]
	
	@sync_caching
	def fetch_from_uuid(self, uuid: str, *, cache: Optional[bool] = False) -> Gear:
		"""
		Fetches a gear's data
		
		Parameters
		----------
		uuid : `str`
			The UUID of the Gear
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,AsyncClient):
			raise ValueError('Invalid session type')
		data = self._client._session.get('/gear/%s'%uuid,language=self.client._language)
		return Gear(data.get('data',{}))

class AsyncGearEndpoint(BaseEndpoint):
	@async_caching
	async def fetch_all(self, *, cache: Optional[bool] = False) -> List[Gear]:
		"""Fetches all gears' data
		
		Parameters
		----------
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,SyncClient):
			raise ValueError('Invalid session type')
		data = await self._client._session.get('/gear',language=self._client._language)
		return [Gear(info) for info in data.get('data',[])]
	
	@async_caching
	async def fetch_from_uuid(self, uuid: str, *, cache: Optional[bool] = False) -> Gear:
		"""
		Fetches a gear's data
		
		Parameters
		----------
		uuid : `str`
			The UUID of the Gear
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,SyncClient):
			raise ValueError('Invalid session type')
		data = await self._client._session.get('/gear/%s'%uuid,language=self._client._language)
		return Gear(data.get('data',{}))

class SyncLevelBorderEndpoint(BaseEndpoint):
	@sync_caching
	def fetch_all(self, *, cache: Optional[bool] = False) -> List[LevelBorder]:
		"""Fetches all level borders' data
		
		Parameters
		----------
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,AsyncClient):
			raise ValueError('Invalid session type')
		data = self._client._session.get('/levelborders',language=self._client._language)
		return [LevelBorder(info) for info in data.get('data',[])]

	@sync_caching
	def fetch_from_uuid(self, uuid: str, *, cache: Optional[bool] = False) -> LevelBorder:
		"""
		Fetches a level border's data
		
		Parameters
		----------
		uuid : `str`
			The UUID of the Level Border
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,AsyncClient):
			raise ValueError('Invalid session type')
		data = self._client._session.get('/levelborders/%s'%uuid,language=self.client._language)
		return LevelBorder(data.get('data',{}))

class AsyncLevelBorderEndpoint(BaseEndpoint):
	@async_caching
	async def fetch_all(self, *, cache: Optional[bool] = False) -> List[LevelBorder]:
		"""Fetches all level borders' data
		
		Parameters
		----------
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,SyncClient):
			raise ValueError('Invalid session type')
		data = await self._client._session.get('/levelborders',language=self._client._language)
		return [LevelBorder(info) for info in data.get('data',[])]
	
	@async_caching
	async def fetch_from_uuid(self, uuid: str, *, cache: Optional[bool] = False) -> LevelBorder:
		"""
		Fetches a level border's data
		
		Parameters
		----------
		uuid : `str`
			The UUID of the Level Border
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,SyncClient):
			raise ValueError('Invalid session type')
		data = await self._client._session.get('/levelborders/%s'%uuid,language=self._client._language)
		return LevelBorder(data.get('data',{}))

class SyncMapEndpoint(BaseEndpoint):
	@sync_caching
	def fetch_all(self, *, cache: Optional[bool] = False) -> List[Map]:
		"""Fetches all Valorant maps' data
		
		Parameters
		----------
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,AsyncClient):
			raise ValueError('Invalid session type')
		data = self._client._session.get('/maps',language=self._client._language)
		return [Map(info) for info in data.get('data',[])]

	@sync_caching
	def fetch_from_uuid(self, uuid: str, *, cache: Optional[bool] = False) -> Map:
		"""
		Fetches a Valorant map's data
		
		Parameters
		----------
		uuid : `str`
			The UUID of the Map
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,AsyncClient):
			raise ValueError('Invalid session type')
		data = self._client._session.get('/maps/%s'%uuid,language=self.client._language)
		return Map(data.get('data',{}))

class AsyncMapEndpoint(BaseEndpoint):
	@async_caching
	async def fetch_all(self, *, cache: Optional[bool] = False) -> List[Map]:
		"""Fetches all Valorant maps' data
		
		Parameters
		----------
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,SyncClient):
			raise ValueError('Invalid session type')
		data = await self._client._session.get('/maps',language=self._client._language)
		return [Map(info) for info in data.get('data',[])]
	
	@async_caching
	async def fetch_from_uuid(self, uuid: str, *, cache: Optional[bool] = False) -> Map:
		"""
		Fetches a Valorant map's data
		
		Parameters
		----------
		uuid : `str`
			The UUID of the Map
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,SyncClient):
			raise ValueError('Invalid session type')
		data = await self._client._session.get('/maps/%s'%uuid,language=self._client._language)
		return Map(data.get('data',{}))
	
class SyncPlayerCardEndpoint(BaseEndpoint):
	@sync_caching
	def fetch_all(self, *, cache: Optional[bool] = False) -> List[PlayerCard]:
		"""Fetches all player cards' data
		
		Parameters
		----------
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,AsyncClient):
			raise ValueError('Invalid session type')
		data = self._client._session.get('/playercards',language=self._client._language)
		return [PlayerCard(info) for info in data.get('data',[])]
	
	@sync_caching
	def fetch_from_uuid(self, uuid: str, *, cache: Optional[bool] = False) -> PlayerCard:
		"""
		Fetches a player card's data
		
		Parameters
		----------
		uuid : `str`
			The UUID of the Player Card
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,AsyncClient):
			raise ValueError('Invalid session type')
		data = self._client._session.get('/playercards/%s'%uuid,language=self.client._language)
		return PlayerCard(data.get('data',{}))

class AsyncPlayerCardEndpoint(BaseEndpoint):
	@async_caching
	async def fetch_all(self, *, cache: Optional[bool] = False) -> List[PlayerCard]:
		"""Fetches all player cards' data
		
		Parameters
		----------
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,SyncClient):
			raise ValueError('Invalid session type')
		data = await self._client._session.get('/playercards',language=self._client._language)
		return [PlayerCard(info) for info in data.get('data',[])]
	
	@async_caching
	async def fetch_from_uuid(self, uuid: str, *, cache: Optional[bool] = False) -> PlayerCard:
		"""
		Fetches a player card's data
		
		Parameters
		----------
		uuid : `str`
			The UUID of the Player Card
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,SyncClient):
			raise ValueError('Invalid session type')
		data = await self._client._session.get('/playercards/%s'%uuid,language=self._client._language)
		return PlayerCard(data.get('data',{}))
	
class SyncPlayerTitleEndpoint(BaseEndpoint):
	@sync_caching
	def fetch_all(self, *, cache: Optional[bool] = False) -> List[PlayerTitle]:
		"""Fetches all player titles' data
		
		Parameters
		----------
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,AsyncClient):
			raise ValueError('Invalid session type')
		data = self._client._session.get('/playertitles',language=self._client._language)
		return [PlayerTitle(info) for info in data.get('data',[])]
	
	@sync_caching
	def fetch_from_uuid(self, uuid: str, *, cache: Optional[bool] = False) -> PlayerTitle:
		"""
		Fetches a player title's data
		
		Parameters
		----------
		uuid : `str`
			The UUID of the Player Title
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,AsyncClient):
			raise ValueError('Invalid session type')
		data = self._client._session.get('/playertitles/%s'%uuid,language=self.client._language)
		return PlayerTitle(data.get('data',{}))

class AsyncPlayerTitleEndpoint(BaseEndpoint):
	@async_caching
	async def fetch_all(self, *, cache: Optional[bool] = False) -> List[PlayerTitle]:
		"""Fetches all player titles' data
		
		Parameters
		----------
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,SyncClient):
			raise ValueError('Invalid session type')
		data = await self._client._session.get('/playertitles',language=self._client._language)
		return [PlayerTitle(info) for info in data.get('data',[])]
	
	@async_caching
	async def fetch_from_uuid(self, uuid: str, *, cache: Optional[bool] = False) -> PlayerTitle:
		"""
		Fetches a player title's data
		
		Parameters
		----------
		uuid : `str`
			The UUID of the Player Title
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,SyncClient):
			raise ValueError('Invalid session type')
		data = await self._client._session.get('/playertitles/%s'%uuid,language=self._client._language)
		return PlayerTitle(data.get('data',{}))
	
class SyncSprayEndpoint(BaseEndpoint):
	@sync_caching
	def fetch_all(self, *, cache: Optional[bool] = False) -> List[Spray]:
		"""Fetches all sprays' data
		
		Parameters
		----------
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,AsyncClient):
			raise ValueError('Invalid session type')
		data = self._client._session.get('/Sprays',language=self._client._language)
		return [Spray(info) for info in data.get('data',[])]
	
	@sync_caching
	def fetch_from_uuid(self, uuid: str, *, cache: Optional[bool] = False) -> Spray:
		"""
		Fetches a spray's data
		
		Parameters
		----------
		uuid : `str`
			The UUID of the Spray
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,AsyncClient):
			raise ValueError('Invalid session type')
		data = self._client._session.get('/sprays/%s'%uuid,language=self.client._language)
		return Spray(data.get('data',{}))

	@sync_caching
	def fetch_all_levels(self, *, cache: Optional[bool] = False) -> List[SprayLevel]:
		"""Fetches all spray levels' data
		
		Parameters
		----------
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,AsyncClient):
			raise ValueError('Invalid session type')
		data = self._client._session.get('/sprays/levels',language=self._client._language)
		return [SprayLevel(info) for info in data.get('data',[])]
	
	@sync_caching
	def fetch_level_from_uuid(self, uuid: str, *, cache: Optional[bool] = False) -> SprayLevel:
		"""
		Fetches a spray level's data
		
		Parameters
		----------
		uuid : `str`
			The UUID of the Spray Level
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,AsyncClient):
			raise ValueError('Invalid session type')
		data = self._client._session.get('/sprays/levels/%s'%uuid,language=self.client._language)
		return SprayLevel(data.get('data',{}))

class AsyncSprayEndpoint(BaseEndpoint):
	@async_caching
	async def fetch_all(self, *, cache: Optional[bool] = False) -> List[Spray]:
		"""Fetches all sprays' data
		
		Parameters
		----------
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,SyncClient):
			raise ValueError('Invalid session type')
		data = await self._client._session.get('/sprays',language=self._client._language)
		return [Spray(info) for info in data.get('data',[])]
	
	@async_caching
	async def fetch_from_uuid(self, uuid: str, *, cache: Optional[bool] = False) -> Spray:
		"""
		Fetches a spray's data
		
		Parameters
		----------
		uuid : `str`
			The UUID of the Spray
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,SyncClient):
			raise ValueError('Invalid session type')
		data = await self._client._session.get('/Sprays/%s'%uuid,language=self._client._language)
		return Spray(data.get('data',{}))

	@async_caching
	async def fetch_all_levels(self, *, cache: Optional[bool] = False) -> List[SprayLevel]:
		"""Fetches all spray levels' data
		
		Parameters
		----------
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,SyncClient):
			raise ValueError('Invalid session type')
		data = await self._client._session.get('/sprays/levels',language=self._client._language)
		return [SprayLevel(info) for info in data.get('data',[])]
	
	@async_caching
	async def fetch_level_from_uuid(self, uuid: str, *, cache: Optional[bool] = False) -> SprayLevel:
		"""
		Fetches a spray level's data
		
		Parameters
		----------
		uuid : `str`
			The UUID of the Spray Level
		cache : `Optional[bool]`
			If `True` returns values saved in cache and if not found it fetches normally and saves to cache.
			If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
		"""
		if isinstance(self._client._session,SyncClient):
			raise ValueError('Invalid session type')
		data = await self._client._session.get('/sprays/levels/%s'%uuid,language=self.client._language)
		return SprayLevel(data.get('data',{}))