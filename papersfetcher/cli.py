"""
Command line interface for fetching PubMed papers.
"""

import argparse
from typing import Optional
import csv
from papersfetcher.fetcher import search_pubmed, fetch_pubmed_details

def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch PubMed papers with non-academic authors.")
    parser.add_argument('query', type=str, help='PubMed search query.')
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode.')
    parser.add_argument('-f', '--file', type=str, help='CSV file to save results.')
    args = parser.parse_args()

    pubmed_ids = search_pubmed(args.query, debug=args.debug)
    papers = fetch_pubmed_details(pubmed_ids, debug=args.debug)

    if args.file:
        with open(args.file, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=[
                'PubmedID', 'Title', 'Publication Date',
                'Non-academic Author(s)', 'Company Affiliation(s)',
                'Corresponding Author Email'
            ])
            writer.writeheader()
            writer.writerows(papers)
        print(f"Results saved to {args.file}")
    else:
        for paper in papers:
            print(paper)

if __name__ == "__main__":
    main()
