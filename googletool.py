from crewai.tools import tool
from typing import Optional

@tool("Google tool")
def google(
    service_type: str, zip_code: int) -> str:
    """
    Generates a Google Maps URL for finding top rated vendors on the specified service.

    :param service_type: The service needed on the home (e.g., Plumbing or Electrical)
    :param zip_code: The zipcode for the home (e.g., 11514)
    :return: The google URL for the vendor search
    """
    print(f"Generating Google URL for {service_type} near {zip_code}")
    # EXAMPLE URL = f"https://www.yelp.com/search?cflt=plumbing&find_loc=Carle+Place,+NY+11514"
    URL = f"https://www.google.com/maps/search/{service_type}+near+{zip_code}"
    #URL = f"https://www.google.com/localservices/prolist?hl=en-US&gl=us&cs=1&ssta=1&src=1&gsas=1&q={service_type}%20near%20{zip_code}"
    return URL


