# Border Crossing Entry Dashboard

This Streamlit dashboard provides interactive visualizations and insights into U.S. border crossing entry data, powered by data from [data.gov](https://catalog.data.gov/dataset/border-crossing-entry-data-683ae). It includes KPIs, charts, filters, and a map — all styled similarly to the official Streamlit blog demo.

---

## Features

- Summary KPIs (total crossings, ports, states, border types)
- Top 10 ports by crossing volume
- Monthly time series of border entries
- Interactive filters for Border, State, and Measure
- Dynamic bubble map showing port-level entry volume
- Clean layout and dark theme

---

## Dataset

- **Source:** [U.S. Customs and Border Protection – Border Crossing Entry Data](https://catalog.data.gov/dataset/border-crossing-entry-data-683ae)
- **Columns:**
  - `Port Name`: U.S. port of entry
  - `State`: U.S. state where the port is located
  - `Border`: North / South / Other
  - `Date`: Monthly timestamp
  - `Measure`: Type of crossing (e.g., Vehicles, Pedestrians)
  - `Value`: Number of crossings
  - `Latitude` and `Longitude`: Coordinates for mapping

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip
- Streamlit installed

### Installation

Clone this repo:

```bash
git clone https://github.com/SyamGopalGuttula/border-crossing-dashboard.git
cd border-crossing-dashboard
```

Create a virtual environment and install dependencies:

```bash
python -m venv venv
.env\Scriptsctivate
pip install -r requirements.txt
```

Download the dataset:

1. Visit: [data.gov dataset page](https://catalog.data.gov/dataset/border-crossing-entry-data-683ae)
2. Download `Border_Crossing_Entry_Data.csv`
3. Place it in the project root folder (next to `app.py`)

---

### Run the Dashboard

```bash
streamlit run app.py
```

Open your browser to `http://localhost:8501`


## License

This project is for educational and demonstration purposes. The dataset is public domain via data.gov.

---

## Acknowledgments

- Streamlit Team
- U.S. Customs and Border Protection
- Inspired by: [Streamlit Blog Demo](https://blog.streamlit.io/crafting-a-dashboard-app-in-python-using-streamlit/)
