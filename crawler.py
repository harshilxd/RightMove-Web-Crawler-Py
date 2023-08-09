import asyncio
import json
from typing import List, Dict
from httpx import AsyncClient
from parsel import Selector
import jmespath

# TypedDict for the property information structure
class RealEstateInfo(Dict):
    """
    Schema for property dataset
    """
    uid: str
    is_available: bool
    is_archived: bool
    contact_number: str
    rooms: int
    baths: int
    listing_type: str
    estate_type: str
    attributes: List[str]
    details: str
    headline: str
    subheadline: str
    cost: str
    rate_per_sqft: str
    location: Dict[str, str]
    lat: float
    long: float
    key_features: List[str]
    record: Dict[str, str]

# Setup HTTP client with browser-like headers
web_client = AsyncClient(
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
        "Accept": "application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
    },
    follow_redirects=True,
    http2=True,
    timeout=30,
)

def map_property_info(raw_data) -> RealEstateInfo:
    """
    Process property data
    """
    mapping = {
        "uid": "id",
        "is_available": "status.published",
        "is_archived": "status.archived",
        "contact_number": "contactInfo.telephoneNumbers.localNumber",
        "rooms": "bedrooms",
        "baths": "bathrooms",
        "listing_type": "transactionType",
        "estate_type": "propertySubType",
        "attributes": "tags",
        "details": "text.description",
        "headline": "text.pageTitle",
        "subheadline": "text.propertyPhrase",
        "cost": "prices.primaryPrice",
        "rate_per_sqft": "prices.pricePerSqFt",
        "location": "address",
        "lat": "location.latitude",
        "long": "location.longitude",
        "key_features": "keyFeatures",
        "record": "listingHistory",
    }
    processed_data = {}
    for key, path in mapping.items():
        value = jmespath.search(path, raw_data)
        processed_data[key] = value
    return processed_data

def retrieve_data_from_script(response_content) -> Dict:
    """
    Extract property information from a script tag
    """
    sel = Selector(response_content)
    extracted_data = sel.xpath("//script[contains(.,'PAGE_MODEL = ')]/text()").get()
    if not extracted_data:
        print(f"Failed to fetch from {response_content.url}")
        return {}
    extracted_data = extracted_data.split("PAGE_MODEL = ", 1)[1].strip()
    data_as_json = json.loads(extracted_data)
    return data_as_json.get("propertyData", {})

async def collect_property_data(urls: List[str]) -> List[Dict]:
    """
    Gather property data from multiple URLs
    """
    tasks = [web_client.get(link) for link in urls]
    estate_list = []
    for res in asyncio.as_completed(tasks):
        response = await res
        estate_list.append(map_property_info(retrieve_data_from_script(response)))
    return estate_list

async def main():
    fetched_data = await collect_property_data(["https://www.rightmove.co.uk/properties/135498977#/?channel=RES_NEW"])
    with open('estate_data.json', 'w') as out_file:
        json.dump(fetched_data, out_file, indent=2)
    print("Data stored in estate_data.json")

if __name__ == "__main__":
    asyncio.run(main())
