# Contributing

Thanks for your interest in improving this project. This is a personal/academic
data-analytics project, but contributions and suggestions are welcome.

## How to contribute

1. **Fork** this repository and clone your fork locally.
2. **Create a branch** for your change:
   ```
   git checkout -b fix/short-description
   ```
3. **Make your change.** Keep pull requests focused on one thing at a time —
   easier to review and merge.
4. **Test locally** before opening a pull request:
   ```
   pip install -r requirements.txt
   streamlit run app.py
   ```
   Click through all 7 pages and try a few filter combinations to make sure
   nothing breaks.
5. **Open a pull request** against `main`, with a clear description of what
   changed and why.

## Reporting issues

If you spot a bug (a chart that errors out, a filter that produces wrong
numbers, a broken layout on a certain screen size), please open an issue with:
- What you did (steps to reproduce)
- What you expected to happen
- What actually happened (a screenshot helps)

## Style notes

- Keep the glassmorphism design language consistent — reuse the existing
  helper functions in `common.py` (`kpi_card`, `chart_card`, `insight_card`)
  rather than writing new one-off styled elements.
- All statistics shown on the dashboard should be computed live from the
  data (via pandas), not hardcoded.
- No emojis in the UI, per the project's design brief.

## Code of conduct

Be respectful and constructive in issues and pull requests. Disagreements
about implementation are fine — personal attacks aren't.
