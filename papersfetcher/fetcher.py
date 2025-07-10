"""
Module to fetch PubMed papers and extract those with non-academic authors.
"""

from typing import List, Dict
import requests
import re

PUBMED_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

def is_non_academic(affiliation: str) -> bool:
    academic_keywords = ['university', 'college', 'hospital', 'institute', 'school', 'center', 'centre']
    return not any(kw.lower() in affiliation.lower() for kw in academic_keywords)

def search_pubmed(query: str, debug: bool = False) -> List[str]:
    params = {'db': 'pubmed', 'retmode': 'json', 'term': query, 'retmax': '50'}
    response = requests.get(PUBMED_SEARCH_URL, params=params)
    response.raise_for_status()
    ids = response.json()['esearchresult']['idlist']
    if debug:
        print(f"[DEBUG] Found {len(ids)} papers for query: {query}")
    return ids

def fetch_pubmed_details(pubmed_ids: List[str], debug: bool = False) -> List[Dict]:
    if not pubmed_ids:
        return []
    params = {'db': 'pubmed', 'retmode': 'xml', 'id': ','.join(pubmed_ids)}
    response = requests.get(PUBMED_FETCH_URL, params=params)
    response.raise_for_status()
    from xml.etree import ElementTree as ET
    root = ET.fromstring(response.content)

    papers = []
    for article in root.findall(".//PubmedArticle"):
        pmid = article.findtext(".//PMID")
        title = article.findtext(".//ArticleTitle")
        pubdate = article.findtext(".//PubDate/Year") or "Unknown"
        authors_info = []

        for author in article.findall(".//Author"):
            name = ' '.join(filter(None, [
                author.findtext("ForeName"), author.findtext("LastName")
            ])).strip()
            affiliation = author.findtext(".//Affiliation") or ""
            if is_non_academic(affiliation):
                authors_info.append((name, affiliation))

        corresponding_email = None
        for aff in article.findall(".//Affiliation"):
            emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", aff.text or "")
            if emails:
                corresponding_email = emails[0]
                break

        if authors_info:
            papers.append({
                "PubmedID": pmid,
                "Title": title,
                "Publication Date": pubdate,
                "Non-academic Author(s)": "; ".join(name for name, _ in authors_info),
                "Company Affiliation(s)": "; ".join(aff for _, aff in authors_info),
                "Corresponding Author Email": corresponding_email or ""
            })
    if debug:
        print(f"[DEBUG] Filtered {len(papers)} papers with non-academic authors.")
    return papers
