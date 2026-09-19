# Mental Health in Tech — Workplace Mental Health Intelligence

![Python](https://img.shields.io/badge/Python-3.10%2B-4C8DFF?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.38%2B-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.22%2B-3F4F75?style=flat-square&logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.2%2B-150458?style=flat-square&logo=pandas&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-A78BFA?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-2DD4BF?style=flat-square)

A glassmorphism analytics dashboard built on the 2014 OSMI "Mental Health in Tech" survey
(1,259 responses). Built with Streamlit + Plotly + custom CSS — dark navy interface, frosted
glass panels, and a 7-page navigation covering treatment patterns, workplace support, and
demographics.

## Contents

- `app.py` — entry point: page config, header, sidebar navigation, filter panel, page routing
- `common.py` — shared design tokens, CSS, and reusable components (KPI cards, chart cards, insight cards)
- `pages_content.py` — the 7 dashboard pages
- `Mental_Health_in_Tech_EDA.ipynb` — the exploratory data analysis notebook
- `survey.csv` — the dataset
- `requirements.txt` — dependencies

## Pages

| Page | Covers |
|---|---|
| 01 — Executive Overview | KPIs, featured chart, quick support/demographic snapshot |
| 02 — Mental Health | Treatment status, family history, work interference |
| 03 — Workplace Environment | Benefits, care options, wellness programs, anonymity, leave |
| 04 — Treatment & Support | Treatment vs. workplace support factors, disclosure comfort |
| 05 — Demographics | Age, gender, country, company size, remote work |
| 06 — Interactive Explorer | Build your own cross-tabulations, download filtered data |
| 07 — Key Findings | Correlation matrix and headline takeaways |

## Running locally

```
pip install -r requirements.txt
streamlit run app.py
```

## Deploying on Streamlit Community Cloud

Upload all files to the **root** of your GitHub repo (not inside a subfolder), then set the
main file path to `app.py` when deploying on [share.streamlit.io](https://share.streamlit.io).

## Data notes

- All KPIs and chart values are calculated live from the dataset — nothing is hardcoded.
- The filter panel applies globally: switching pages keeps your filters active.
- Data cleaning: invalid `Age` values (negatives, absurd outliers) are replaced with the median;
  `Gender` free-text responses are standardized into Male / Female / Other; missing
  `work_interfere` values are treated as "Not applicable" (they mean the respondent has no
  condition, not that data is missing).

## Contributing

Contributions are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on setup,
style, and how to submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
