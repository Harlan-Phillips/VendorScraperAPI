import sys
import datetime
from crewai import Crew, Process, Task, Agent
from browserbase import browserbase, phone_number_scraper
from yelp import yelp
from googletool import google
from fastapi import FastAPI
import logging
import asyncio
import multiprocessing


logging.basicConfig(level=logging.INFO)



google_agent = Agent(
    role="Google Expert",
    goal="Extract and Format Data from Google Page",
    backstory="I am an agent that can go to any google page and know where to look for data and format it to json.",
    llm="chatgpt-4o-latest",
    tools=[google, browserbase],
    allow_delegation=False,
)

expected_output = """
    {
      "vendorName": "Vendor A",
      "rating": 4.9,
      "reviews": 56,
      "description": "Summary of last 30 reviews highlighting... (50 words max)",
      "247availability": true,
      "contact": "(123) 456-7890",
      "website": "https://vendor-a.com"
    },
    {
      "vendorName": "Vendor B",
      "rating": 4.5,
      "reviews": 42,
      "description": "Consensus from recent reviews indicates... (50 words max)",
      "247availability": false,
      "contact": "(234) 567-8901",
      "website": "https://vendor-b.com"
    }
    """

search_task = Task(
    description=(
        "Execute sequential steps:\n"
        "1. Generate Google Search URL for '{service_type} vendors near {zip_code}'\n"
        "2. Use Browserbase to load results ONCE\n"
        "3. For the first 3 vendors returned:\n"
        "   - Apply filters: {filters}\n"
        "   - If a vendor does not meet the filters, skip it.\n"
        "4. For all subsequent vendors (beyond the first 3), ignore filters and include them automatically. (Up to 10)\n"
        "5. For each included vendor:\n"
        "   a) Visit the business page (single load)\n"
        "   b) Extract:\n"
        "      - Vendor Name\n"
        "      - Rating\n"
        "      - Number of Reviews\n"
        "      - Description (50-word summary of last 30 reviews, include positive & negative feedback)\n"
        "      - Contact Phone\n"
        "      - 24/7 Availability (boolean)\n"
        "      - Website URL\n"
        "6. Return JSON array with valid entries (any number)\n"
        "7. Empty array if no matches\n\n"
        "- No duplicate tool calls\n"
        "- 30s/page timeout\n"
        "- Validate filters before inclusion\n"
        "- Pure JSON output only"
    ),
    expected_output=expected_output,
    agent=google_agent,
)



# Assemble the crew
crew = Crew(
    agents=[google_agent],
    tasks=[search_task],
    max_rpm=100,
    verbose=True,
    planning=True,
)

app = FastAPI()

def run_task(inputs):
    return crew.kickoff(inputs=inputs)

@app.get("/search")
def search(service_type: str, filters: str = None):
    """Endpoint to perform a web search."""
    logging.info(f"Received search request for service_type: {service_type}")
    logging.info(f"Filters: {filters}")

    inputs = {
        "service_type": service_type,
        "filters": filters,
        "city": "Carle Place",
        "state": "NY",
        "zip_code": "11514",
    }

    with multiprocessing.Pool(processes=4) as pool:
        result = pool.map(run_task, [inputs])

    logging.info("Search completed")
    return result


if __name__ == "__main__":
    import uvicorn
    import signal

    def cleanup(*args):
        logging.info("Shutting down gracefully...")
        # Perform any necessary cleanup here
        sys.exit(0)

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    logging.info("Starting FastAPI server")
    uvicorn.run(app, host="0.0.0.0", port=8000)

# # Kick off the crew with inputs
# if __name__ == "__main__":
#     result = crew.kickoff(
#         inputs={
#             "service_type": "carpenter",
#             "city": "Las Vegas",
#             "state": "NV",
#             "zip_code": "89121",
#         }
#     )
#     print(result)