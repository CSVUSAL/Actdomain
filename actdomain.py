import asyncio
import aiohttp
from colorama import Fore, Style
import re

async def check_subdomain(subdomain, session):
    url = f"http://{subdomain}"
    try:
        async with session.get(url, timeout=5) as response:
            if 200 <= response.status < 300:
                return subdomain, "active"
            elif 300 <= response.status < 400:
                return subdomain, "redirect"
            else:
                return subdomain, "inactive"
    except aiohttp.ClientError:
        return subdomain, "inactive"

async def main(subdomains):
    async with aiohttp.ClientSession() as session:
        tasks = [check_subdomain(subdomain, session) for subdomain in subdomains]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        active_subdomains = [result[0] for result in results if isinstance(result, tuple) and result[1] == "active"]
        redirect_subdomains = [result[0] for result in results if isinstance(result, tuple) and result[1] == "redirect"]
        inactive_subdomains = [result[0] for result in results if isinstance(result, tuple) and result[1] == "inactive"]
        return list(set(active_subdomains)), list(set(redirect_subdomains)), list(set(inactive_subdomains))

if __name__ == "__main__":
    print("Subdomainləri daxil edin (Daxil etdikdən sonra Enteri vurun):")
    subdomains = []
    while True:
        subdomain = input()
        if not subdomain:
            break
        # Remove 'http://' and 'https://' from the input
        subdomain = re.sub(r'^https?://', '', subdomain.strip())
        subdomains.append(subdomain)

    active_subdomains, redirect_subdomains, inactive_subdomains = asyncio.run(main(subdomains))

    if active_subdomains:
        print(f"{Fore.RED}Aktiv Domainlər:{Style.RESET_ALL}")
        for sub in active_subdomains:
            print(f"{Fore.GREEN}{sub}{Style.RESET_ALL}")

    if redirect_subdomains:
        print(f"\n{Fore.RED}Redireksiya olunmuş Domainlər:{Style.RESET_ALL}")
        for sub in redirect_subdomains:
            print(f"{Fore.GREEN}{sub}{Style.RESET_ALL}")

    if inactive_subdomains:
        print(f"\n{Fore.RED}Aktiv olmayan Domainlər:{Style.RESET_ALL}")
        for sub in inactive_subdomains:
            print(f"{Fore.GREEN}{sub}{Style.RESET_ALL}")
