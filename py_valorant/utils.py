from io import BytesIO
import requests
import threading
from typing import Optional

def url_to_bytes(url: str, run_thread: Optional[bool] = False) -> BytesIO:
		"""
		Converts a URL to a BytesIO object

		Parameters
		----------
		url: :class:`str`
			The URL of the resource to convert to BytesIO
		run_thread: :class:`bool`
			Whether to run the function in a new Thread
		"""
		container = []
		if run_thread:
			def _run_loop():
				result = url_to_bytes(url,False)
				container.append(result)
			thread = threading.Thread(target=_run_loop,daemon=True)
			thread.start()
			thread.join()
			return container[0]
		resp = requests.get(url)
		return BytesIO(resp.content)
