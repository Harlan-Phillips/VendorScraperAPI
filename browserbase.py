import os
import requests
from crewai.tools import tool
from playwright.sync_api import sync_playwright
from html2text import html2text
from time import sleep

API_KEY = os.environ["BROWSERBASE_API_KEY"]
PROJECT_ID = os.environ["BROWSERBASE_PROJECT_ID"]

def create_session_with_proxy() -> str:
    """
    Create a Browserbase session with proxy configuration.

    :returns: The new session's ID.
    """
    sessions_url = "https://api.browserbase.com/v1/sessions"
    headers = {
        "Content-Type": "application/json",
        "x-bb-api-key": API_KEY,
    }
    json = {
        "projectId": PROJECT_ID,
        "browserSettings": {
            "proxies": True,  # Use default proxy configuration
        },
    }

    response = requests.post(sessions_url, json=json, headers=headers)
    response.raise_for_status()
    return response.json()["id"]

@tool("Browserbase tool")
def browserbase(url: str):
    """
    Loads a URL using a headless webbrowser

    :param url: The URL to load
    :return: The text content of the page
    """
    with sync_playwright() as playwright:
        session_id = create_session_with_proxy()
        browser = playwright.chromium.connect_over_cdp(
            f"wss://connect.browserbase.com?apiKey={API_KEY}&sessionId={session_id}"
        )
        context = browser.contexts[0]
        page = context.pages[0]
        page.goto(url)

        # if phonenumber:
        #     # Wait for the parent div containing the phone number to appear
        #     page.wait_for_selector("div.y-css-8x4us")
        #     parent_div = page.query_selector("div.y-css-8x4us")

        #     # Extract the phone number from the second <p> element within the parent div
        #     phone_number = parent_div.query_selector_all("p")[1].inner_text()
        #     return phone_number
        # Wait for results list to load
        #page.wait_for_selector("ul.list__09f24__ynIEd", timeout=10000)
        #page.wait_for_selector('div[class="DyM7H"]')
        #page.wait_for_selector('div[class="Nv2PK tH5CWc THOPZb"]') 
        sleep(2)
        content = html2text(page.content())
        browser.close()
        return content

@tool("PhoneNumberScraper tool")
def phone_number_scraper(url: str):
    """
    Extracts phone number from a Yelp business page

    :param url: The URL of the Yelp business page
    :return: The phone number of the business
    """
    with sync_playwright() as playwright:
        session_id = create_session_with_proxy()
        browser = playwright.chromium.connect_over_cdp(
            f"wss://connect.browserbase.com?apiKey={API_KEY}&sessionId={session_id}"
        )

        context = browser.contexts[0]
        page = context.pages[0]
        page.goto(url)

        # Wait for the parent div containing the phone number to appear
        page.wait_for_selector("div.y-css-8x4us")
        parent_div = page.query_selector("div.y-css-8x4us")

        # Extract the phone number from the second <p> element within the parent div
        phone_number = parent_div.query_selector_all("p")[1].inner_text()

        browser.close()
        return phone_number