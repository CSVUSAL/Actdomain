import asyncio
import aiohttp
from colorama import Fore, Style

async def check_subdomain(subdomain, session):
    url = f"http://{subdomain}"
    try:
        async with session.get(url, timeout=5) as response:
            if response.status == 200:
                return subdomain, True
            else:
                return subdomain, False
    except aiohttp.ClientError:
        return subdomain, False

async def main(subdomains):
    async with aiohttp.ClientSession() as session:
        tasks = [check_subdomain(subdomain, session) for subdomain in subdomains]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        active_subdomains = [result[0] for result in results if isinstance(result, tuple) and result[1]]
        inactive_subdomains = [result[0] for result in results if isinstance(result, tuple) and not result[1]]
        return active_subdomains, inactive_subdomains

if __name__ == "__main__":
    print("Subdomainləri daxil edin (Daxil etdikdən sonra sadəcə Enteri basın):")
    subdomains = []
    while True:
        subdomain = input()
        if not subdomain:
            break
        subdomains.append(subdomain.strip())

    active_subdomains, inactive_subdomains = asyncio.run(main(subdomains))

    print(f"{Fore.RED}Aktiv subdomainlər:{Style.RESET_ALL}")
    for sub in active_subdomains:
        print(f"{Fore.GREEN}{sub}{Style.RESET_ALL}")

    print(f"\n{Fore.RED}Aktiv olmayan subdomainlər:{Style.RESET_ALL}")
    for sub in inactive_subdomains:
        print(f"{Fore.GREEN}{sub}{Style.RESET_ALL}")
