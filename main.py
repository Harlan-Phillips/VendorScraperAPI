import sys
import datetime
from crewai import Crew, Process, Task, Agent
from browserbase import browserbase, phone_number_scraper
from googletool import google
from fastapi import FastAPI, HTTPException, Request
import logging
import asyncio
import multiprocessing
from together import Together

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
    ```json
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
        {
        "vendorName": "Vendor C",
        "rating": 4.5,
        "reviews": 42,
        "description": "Consensus from recent reviews indicates... (50 words max)",
        "247availability": false,
        "contact": "(234) 567-8901",
        "website": "https://vendor-c.com"
        }
    ```
    """

search_task = Task(
    description=(
        "Execute sequential steps:\n"
        "1. Generate Google Search URL for '{service_type} vendors near {zip_code}'\n"
        "2. Use Browserbase to load results\n"
        "3. For up to 10 vendors, apply these filters: {filters}:\n"
        "   a) Click on each business \n"
        "   b) Extract:\n"
        "      - Vendor Name\n"
        "      - Rating\n"
        "      - Number of Reviews\n"
        "      - Description (50-word summary of last 30 reviews, include positive & negative feedback and list the percentage of each)\n"
        "      - Contact Phone\n"
        "      - 24/7 Availability (boolean)\n"
        "      - Website URL\n"
        "4. Return JSON with valid entries (up to 10)\n"
        "DO NOT INCLUDE BRACKETS in your response"
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

    result = crew.kickoff(inputs=inputs)
    return result

# endpoint for deepseek r1
@app.post("/deepseek")
async def deepseek(request: Request):
    try:
        # Parse JSON body
        data = await request.json()
        query = data.get("query")
        instructions = data.get("instructions")

        # Use the query and instructions as needed.
        client = Together()
        messages = [{"role": "user", "content": query}]
        
        if instructions:
            messages.insert(0, {
                "role": "system",
                "content": instructions
            })
            
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1",
            messages=messages
        )
        
        print(response.choices[0].message.content)
        return response.choices[0].message.content
        
        
    except Exception as e:
        logging.error(f"Error calling DeepSeek: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


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