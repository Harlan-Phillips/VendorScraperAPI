# VendorScraperAPI 🛠️

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.103%2B-green)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

VendorScraperAPI is a powerful web search API that helps users find top-rated vendors for various home services. Built with modern technologies including FastAPI, CrewAI, and Browserbase for efficient task management and web scraping.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Features ✨
- Find top-rated vendors for home services
- Integrated web scraping with Browserbase
- AI-powered search capabilities
- FastAPI backend for high performance
- Easy-to-use RESTful API endpoints

## Installation 💻

1. **Clone the repository**:
```bash
git clone https://github.com/yourusername/VendorScraperAPI.git
```

2. **Create and activate virtual environment**:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set environment variables**:
```bash
export BROWSERBASE_API_KEY=your_browserbase_api_key
export BROWSERBASE_PROJECT_ID=your_browserbase_project_id
export OPENAI_API_KEY=your_openai_api_key
```

## Usage 🚀

Start the FastAPI server:
```bash
uvicorn main:app --reload
```

Access the API documentation at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Project Structure 📁

```
├── browserbase.py    # Browserbase session management and scraping
├── googletool.py     # Google Maps URL generation
├── main.py           # FastAPI application and endpoints
├── requirements.txt  # Project dependencies
└── README.md         # Project documentation
```

## API Endpoints 🔌

### GET /search
Search for vendors based on service type and filters

**Parameters**:

| Parameter    | Type | Required | Description                     |
|--------------|------|----------|---------------------------------|
| service_type | str  | Yes      | Type of service (e.g., Plumbing)|
| filters      | str  | No       | Additional search filters       |

**Example Request**:
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/search?service_type=Plumbing&filters=24-hour' \
  -H 'accept: application/json'
```

**Example Response**:
```json
{
  "service_type": "Plumbing",
  "filters": "24-hour",
  "results": [
    {
      "name": "QuickFix Plumbers",
      "rating": 4.8,
      "services": ["Emergency", "Drain Cleaning"],
      "contact": "555-1234"
    }
  ]
}
```

## Contributing 🤝
Contributions are welcome! Please follow these steps:

1. Fork the repository  
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)  
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)  
4. Push to the branch (`git push origin feature/AmazingFeature`)  
5. Open a Pull Request  

## License 📄
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
