---

### utils.py

```python
# utils.py
from typing import Dict

def generate_tracking_link(affiliate_data: Dict[str, str], user_id: str) -> str:
    """
    Generate a tracking link based on affiliate data and the unique user identifier.

    Parameters:
        affiliate_data (Dict[str, str]): Dictionary containing:
            - 'trackingLink': The base tracking URL.
            - 'sourcePlatform': The affiliate source platform.
            - 'id': A unique offer identifier.
        user_id (str): The unique identifier for the user.

    Returns:
        str: The complete tracking link.
    """
    tracking_link = affiliate_data['trackingLink']
    source_platform = affiliate_data['sourcePlatform']

    if "{USER_ID}" in tracking_link:
        return tracking_link.replace("{USER_ID}", user_id).replace("{OFFER_UUID}", affiliate_data['id'])

    platform_links = {
        "IMPACT": f"{tracking_link}?subid1={user_id}",
        "INVOLVE_ASIA": f"{tracking_link}?aff_sub={user_id}",
        "COMMISSION_FACTORY": f"{tracking_link}&UniqueId={user_id}",
        "OPTIMISE": f"{tracking_link}&UID={user_id}",
        "CJ": f"{tracking_link}?sid={user_id}",
        "RAKUTEN": f"{tracking_link}&u1={user_id}",
        "PARTNERIZE": f"{tracking_link}/pubref:{user_id}",
        "AWIN": f"{tracking_link}&clickref={user_id}"
    }

    return platform_links.get(source_platform, tracking_link)