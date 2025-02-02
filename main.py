import aiohttp
import asyncio

async def fetch_data(session, url):
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.json()
    except asyncio.TimeoutError:
        print(f"Timeout error for URL: {url}")
    except aiohttp.ClientError as e:
        print(f"Client error for URL {url}: {e}")
    except Exception as e:
        print(f"Unexpected error for URL {url}: {e}")

async def fetch_all_data(urls, timeout=10):
    timeout = aiohttp.ClientTimeout(total=timeout)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = [fetch_data(session, url) for url in urls]
        return await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":
    urls = [
        "https://jsonplaceholder.typicode.com/todos/1",
        "https://jsonplaceholder.typicode.com/todos/2", 
        "https://jsonplaceholder.typicode.com/todos/3",
    ]
    
    results = asyncio.run(fetch_all_data(urls))
    
    for url, result in zip(urls, results):
        if isinstance(result, Exception):
            print(f"Error occurred while fetching {url}: {result}")
        else:
            print(f"Data from {url}: {result}\n")
