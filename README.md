# Real Estate Tools

This project provides a suite of tools designed to assist real estate agents in their daily activities. The tools leverage generative AI agents to automate and enhance various tasks, such as generating property listings and retrieving information about nearby points of interest.

## Features

- **AI-powered Listing Generation:** Automatically generate property listings with information about interesting places nearby.
- **Integration with External APIs:** Retrieve data from external sources to enrich listings and provide valuable insights.

## Agent AI Tools

Currently, the following AI tool is available:

- **Google Places API Tool:**  
    Retrieves information about nearby places of interest.  
    - **Configuration:**  
        1. Obtain an API key from [Google Cloud Console](https://developers.google.com/maps/documentation/places/web-service/get-api-key).
        2. Set the API key in your environment or configuration file as required by the tool.

## Running the Project

This project uses [Streamlit](https://streamlit.io/) for its user interface.

### Prerequisites

- Python 3.8+
- Streamlit

### Installation

```bash
pip install -r requirements.txt
```

### Running the App

```bash
streamlit run app.py
```

## Future Tools

Additional generative AI agents will be added to support more real estate tasks.
