from io import BytesIO
import aiohttp, requests
import threading

#TODO: make this alsoa sync
async def url_to_bytes(url: str, run_async: bool) -> BytesIO:
	"""
	Converts a URL to a BytesIO object

	Parameters
	----------
	url: :class:`str`
		The URL of the resource to convert to BytesIO
	"""
	async with aiohttp.ClientSession() as session:
		async with session.get(url) as response:
			return BytesIO(await response.content.read())