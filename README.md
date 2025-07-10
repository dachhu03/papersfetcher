# PapersFetcher

Fetch PubMed papers with at least one author from a pharmaceutical or biotech company.



##  Usage

```bash
poetry run get-papers-list "cancer AND drug"
poetry run get-papers-list "covid vaccine" -f results.csv
poetry run get-papers-list "diabetes treatment" -d
```

##  How it works
* Uses PubMed API (`esearch` + `efetch`)
* Filters non-academic authors based on heuristic
* Returns CSV with required fields

##  Tools used
* Python + Types
* Poetry: https://python-poetry.org
* Requests: https://docs.python-requests.org
* tqdm: https://tqdm.github.io

##  Publish (Bonus)
To publish to TestPyPI:
```bash
poetry build
poetry publish -r testpypi
```

##  Code structure
* `fetcher.py`: Logic to fetch and filter papers
* `cli.py`: Command line tool
