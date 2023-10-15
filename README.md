# NYC Vehicle Collisions Explorer 🌟 🚗

Explore and analyze motor vehicle collisions in NYC through this interactive Streamlit dashboard.

## Overview 🌐

This Streamlit application allows users to interactively explore motor vehicle collisions data in New York City. It provides insights into the locations and times when most collisions occurred, and allows for deeper exploration based on the number of injured persons and breakdowns of incidents by minute within a selected hour.

## Features 🚀

1. **Map Visualization:** Show where most people are injured in NYC.
2. **Collisions by Time of Day:** Explore collisions occurring at different hours of the day.
3. **Breakdown by Minutes:** Analyze the distribution of collisions throughout an hour.
4. **Dangerous Streets Analysis:** Identify the most dangerous streets based on the type of affected people (Pedestrians, Cyclists, Motorists).
5. **Raw Data View:** Examine the raw collision data used for the visualizations.

## Data Source 📊

The data is sourced from the [NYC Vehicle Collisions GitHub repository](https://github.com/itsmefifa/NYC-Vehicle-Collisions) and is loaded dynamically into the application.

## Prerequisites 🛠️

Ensure you have the following installed:
- Python 3.x
- Pip

## Installation 📥

1. Clone this repository:
   ```
   git clone https://github.com/itsmefifa/NYC-Vehicle-Collisions.git
   ```
2. Navigate to the project directory:
   ```
   cd NYC-Vehicle-Collisions
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
   
   **Note:** `requirements.txt` should contain:
   ```
   streamlit
   pandas
   numpy
   pydeck
   plotly
   requests
   ```
4. Run the Streamlit application:
   ```
   streamlit run app.py
   ```

## Usage 🖥️

- Navigate to `localhost:8501` in your web browser to explore the Streamlit application.
- Use the sliders, selectors, and checkboxes to interact with the visualizations and explore the data.

## Contributing 🤝

Contributions, issues, and feature requests are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for how to set up the project for development.

## License 📄

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
