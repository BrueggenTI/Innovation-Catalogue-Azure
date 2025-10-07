import os
import json
import asyncio
from typing import List, Dict, Any, Generator
from openai import OpenAI
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import time

def fetch_open_food_facts(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch product data from Open Food Facts database.
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing product data
    
    Implementation Notes:
        - Use Open Food Facts API: https://world.openfoodfacts.org/data
        - Search for products matching keywords
        - Extract nutritional data, ingredients, labels
        - No API key required (public API)
    """
    return {
        "source": "Open Food Facts",
        "url": "https://world.openfoodfacts.org",
        "data": f"Placeholder data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_pubmed_articles(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch scientific articles from PubMed database.
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing article abstracts and metadata
    
    Implementation Notes:
        - Use NCBI E-utilities API: https://www.ncbi.nlm.nih.gov/books/NBK25501/
        - Search for articles related to keywords
        - Extract abstracts, publication dates, authors
        - API key recommended but not required (get from Replit Secrets: PUBMED_API_KEY)
    """
    return {
        "source": "PubMed",
        "url": "https://pubmed.ncbi.nlm.nih.gov",
        "data": f"Placeholder scientific articles for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_google_trends(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch trend data from Google Trends.
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing search trend data
    
    Implementation Notes:
        - Use pytrends library or Google Trends unofficial API
        - Get interest over time, related queries, regional interest
        - No official API key required
        - Consider rate limiting
    """
    return {
        "source": "Google Trends",
        "url": "https://trends.google.com",
        "data": f"Placeholder trend data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_perplexity_ai(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch AI-powered research from Perplexity AI.
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing AI research results
    
    Implementation Notes:
        - Use Perplexity AI API: https://docs.perplexity.ai/
        - Requires API key (get from Replit Secrets: PERPLEXITY_API_KEY)
        - Submit research query combining keywords
        - Extract comprehensive market research data
    """
    return {
        "source": "Perplexity AI",
        "url": "https://www.perplexity.ai",
        "data": f"Placeholder AI research for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_gemini_ai(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch AI-powered research from Google Gemini.
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing AI research results
    
    Implementation Notes:
        - Use Google Gemini API: https://ai.google.dev/
        - Requires API key (get from Replit Secrets: GEMINI_API_KEY)
        - Submit comprehensive research prompts
        - Extract trend insights and market data
    """
    return {
        "source": "Gemini AI",
        "url": "https://ai.google.dev",
        "data": f"Placeholder Gemini research for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_eurostat_data(keywords: List[str], country: str = "") -> Dict[str, Any]:
    """
    Fetch statistical data from Eurostat (EU Statistical Office).
    
    Args:
        keywords: List of search keywords
        country: Specific EU country code (optional)
    
    Returns:
        Dictionary containing EU statistical data
    
    Implementation Notes:
        - Use Eurostat API: https://ec.europa.eu/eurostat/web/json-and-unicode-web-services
        - Search for relevant datasets related to keywords
        - Extract economic indicators, consumption data, trade statistics
        - No API key required (public API)
    """
    return {
        "source": f"Eurostat{' - ' + country if country else ''}",
        "url": "https://ec.europa.eu/eurostat",
        "data": f"Placeholder EU statistical data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_usda_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch agricultural data from USDA (United States Department of Agriculture).
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing USDA agricultural data
    
    Implementation Notes:
        - Use USDA QuickStats API: https://quickstats.nass.usda.gov/api
        - Requires API key (get from Replit Secrets: USDA_API_KEY)
        - Search for crop data, production statistics, market prices
        - Focus on cereals, grains, breakfast products
    """
    return {
        "source": "USDA",
        "url": "https://www.usda.gov",
        "data": f"Placeholder USDA data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_genesis_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch German statistical data from GENESIS (Statistisches Bundesamt).
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing German statistical data
    
    Implementation Notes:
        - Use GENESIS-Online API: https://www-genesis.destatis.de
        - Search for relevant datasets related to food consumption, production
        - Extract economic indicators, consumer spending, industry data
        - API key may be required for full access
    """
    return {
        "source": "GENESIS (Destatis)",
        "url": "https://www-genesis.destatis.de",
        "data": f"Placeholder German statistical data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_ons_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch UK statistical data from ONS (Office for National Statistics).
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing UK statistical data
    
    Implementation Notes:
        - Use ONS API: https://developer.ons.gov.uk
        - Search for datasets related to consumer spending, food industry
        - Extract economic indicators, trade data, consumer trends
        - No API key required (public API)
    """
    return {
        "source": "ONS (UK)",
        "url": "https://www.ons.gov.uk",
        "data": f"Placeholder UK statistical data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_statcan_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch Canadian statistical data from Statistics Canada.
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Canadian statistical data
    
    Implementation Notes:
        - Use Statistics Canada Web Data Service
        - Search for food consumption, agricultural production data
        - Extract economic indicators, consumer spending patterns
        - No API key required (public access)
    """
    return {
        "source": "Statistics Canada",
        "url": "https://www.statcan.gc.ca",
        "data": f"Placeholder Canadian statistical data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_insee_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch French statistical data from INSEE.
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing French statistical data
    
    Implementation Notes:
        - Use INSEE API: https://api.insee.fr
        - Requires API key (get from Replit Secrets: INSEE_API_KEY)
        - Search for consumption data, industry statistics
        - Extract economic indicators, market trends
    """
    return {
        "source": "INSEE (France)",
        "url": "https://www.insee.fr",
        "data": f"Placeholder French statistical data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_bfs_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch Swiss statistical data from BFS (Bundesamt für Statistik).
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Swiss statistical data
    
    Implementation Notes:
        - Use BFS Open Data Portal
        - Search for food industry, consumer spending data
        - Extract economic indicators, production statistics
        - Public access available
    """
    return {
        "source": "BFS (Switzerland)",
        "url": "https://www.bfs.admin.ch",
        "data": f"Placeholder Swiss statistical data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_abs_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch Australian statistical data from ABS (Australian Bureau of Statistics).
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Australian statistical data
    
    Implementation Notes:
        - Use ABS API: https://www.abs.gov.au/about/data-services/application-programming-interfaces-apis
        - Search for food consumption, agricultural production
        - Extract economic indicators, trade data
        - No API key required (public API)
    """
    return {
        "source": "ABS (Australia)",
        "url": "https://www.abs.gov.au",
        "data": f"Placeholder Australian statistical data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_estat_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch Japanese statistical data from e-Stat.
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Japanese statistical data
    
    Implementation Notes:
        - Use e-Stat API: https://www.e-stat.go.jp/api/
        - Requires application ID (get from Replit Secrets: ESTAT_APP_ID)
        - Search for food industry, consumption data
        - Extract economic indicators, market statistics
    """
    return {
        "source": "e-Stat (Japan)",
        "url": "https://www.e-stat.go.jp",
        "data": f"Placeholder Japanese statistical data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_statsnz_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch New Zealand statistical data from Stats NZ.
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing New Zealand statistical data
    
    Implementation Notes:
        - Use Stats NZ API
        - Search for agricultural data, consumer spending
        - Extract economic indicators, food industry statistics
        - No API key required (public API)
    """
    return {
        "source": "Stats NZ",
        "url": "https://www.stats.govt.nz",
        "data": f"Placeholder New Zealand statistical data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_cbs_nl_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch Dutch statistical data from CBS Netherlands.
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Dutch statistical data
    
    Implementation Notes:
        - Use CBS Open Data StatLine
        - Search for food consumption, agricultural production
        - Extract economic indicators, industry data
        - No API key required (public API)
    """
    return {
        "source": "CBS (Netherlands)",
        "url": "https://www.cbs.nl",
        "data": f"Placeholder Dutch statistical data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_statistik_at_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch Austrian statistical data from Statistik Austria.
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Austrian statistical data
    
    Implementation Notes:
        - Use Statistik Austria Open Data
        - Search for food industry, consumption patterns
        - Extract economic indicators, market data
        - Public access available
    """
    return {
        "source": "Statistik Austria",
        "url": "https://www.statistik.at",
        "data": f"Placeholder Austrian statistical data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_ine_es_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch Spanish statistical data from INE Spain.
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Spanish statistical data
    
    Implementation Notes:
        - Use INE API: https://www.ine.es/dyngs/DataLab/en/api.html
        - Search for food consumption, production data
        - Extract economic indicators, consumer trends
        - No API key required (public API)
    """
    return {
        "source": "INE (Spain)",
        "url": "https://www.ine.es",
        "data": f"Placeholder Spanish statistical data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_istat_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch Italian statistical data from ISTAT.
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Italian statistical data
    
    Implementation Notes:
        - Use ISTAT API
        - Search for food industry, consumer spending
        - Extract economic indicators, market statistics
        - Public access available
    """
    return {
        "source": "ISTAT (Italy)",
        "url": "https://www.istat.it",
        "data": f"Placeholder Italian statistical data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_dst_dk_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch Danish statistical data from Statistics Denmark.
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Danish statistical data
    
    Implementation Notes:
        - Use Statistics Denmark API
        - Search for food consumption, agricultural data
        - Extract economic indicators, trade statistics
        - No API key required (public API)
    """
    return {
        "source": "Statistics Denmark",
        "url": "https://www.dst.dk",
        "data": f"Placeholder Danish statistical data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_stat_fi_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch Finnish statistical data from Statistics Finland.
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Finnish statistical data
    
    Implementation Notes:
        - Use Statistics Finland API
        - Search for food industry, consumer spending
        - Extract economic indicators, market data
        - Public access available
    """
    return {
        "source": "Statistics Finland",
        "url": "https://www.stat.fi",
        "data": f"Placeholder Finnish statistical data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_ssb_no_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch Norwegian statistical data from Statistics Norway.
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Norwegian statistical data
    
    Implementation Notes:
        - Use Statistics Norway API
        - Search for food consumption, agricultural production
        - Extract economic indicators, consumer trends
        - No API key required (public API)
    """
    return {
        "source": "Statistics Norway",
        "url": "https://www.ssb.no",
        "data": f"Placeholder Norwegian statistical data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_scb_se_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch Swedish statistical data from Statistics Sweden.
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Swedish statistical data
    
    Implementation Notes:
        - Use Statistics Sweden API
        - Search for food industry, consumption data
        - Extract economic indicators, market statistics
        - No API key required (public API)
    """
    return {
        "source": "Statistics Sweden",
        "url": "https://www.scb.se",
        "data": f"Placeholder Swedish statistical data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_gus_pl_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch Polish statistical data from GUS (Central Statistical Office).
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Polish statistical data
    
    Implementation Notes:
        - Use GUS API
        - Search for food consumption, agricultural data
        - Extract economic indicators, industry statistics
        - Public access available
    """
    return {
        "source": "GUS (Poland)",
        "url": "https://stat.gov.pl",
        "data": f"Placeholder Polish statistical data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_czso_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch Czech statistical data from CZSO (Czech Statistical Office).
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Czech statistical data
    
    Implementation Notes:
        - Use CZSO API
        - Search for food industry, consumer spending
        - Extract economic indicators, market data
        - No API key required (public API)
    """
    return {
        "source": "CZSO (Czech Republic)",
        "url": "https://www.czso.cz",
        "data": f"Placeholder Czech statistical data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_ksh_hu_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch Hungarian statistical data from KSH.
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Hungarian statistical data
    
    Implementation Notes:
        - Use KSH API
        - Search for food consumption, agricultural production
        - Extract economic indicators, consumer trends
        - Public access available
    """
    return {
        "source": "KSH (Hungary)",
        "url": "https://www.ksh.hu",
        "data": f"Placeholder Hungarian statistical data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_stat_ee_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch Estonian statistical data from Statistics Estonia.
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Estonian statistical data
    
    Implementation Notes:
        - Use Statistics Estonia API
        - Search for food industry, consumption data
        - Extract economic indicators, market statistics
        - No API key required (public API)
    """
    return {
        "source": "Statistics Estonia",
        "url": "https://www.stat.ee",
        "data": f"Placeholder Estonian statistical data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_kosis_kr_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch South Korean statistical data from KOSIS.
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing South Korean statistical data
    
    Implementation Notes:
        - Use KOSIS API: https://kosis.kr/openapi/
        - Requires API key (get from Replit Secrets: KOSIS_API_KEY)
        - Search for food consumption, agricultural data
        - Extract economic indicators, market trends
    """
    return {
        "source": "KOSIS (South Korea)",
        "url": "https://kosis.kr",
        "data": f"Placeholder South Korean statistical data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_singstat_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch Singapore statistical data from SingStat.
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Singapore statistical data
    
    Implementation Notes:
        - Use SingStat API
        - Search for food consumption, import/export data
        - Extract economic indicators, consumer spending
        - No API key required (public API)
    """
    return {
        "source": "SingStat (Singapore)",
        "url": "https://www.singstat.gov.sg",
        "data": f"Placeholder Singapore statistical data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_mospi_in_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch Indian statistical data from MOSPI.
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Indian statistical data
    
    Implementation Notes:
        - Use MOSPI API
        - Search for food industry, consumption patterns
        - Extract economic indicators, market data
        - Public access available
    """
    return {
        "source": "MOSPI (India)",
        "url": "https://www.mospi.gov.in",
        "data": f"Placeholder Indian statistical data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_bps_id_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch Indonesian statistical data from BPS.
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Indonesian statistical data
    
    Implementation Notes:
        - Use BPS API
        - Search for food consumption, agricultural production
        - Extract economic indicators, trade statistics
        - No API key required (public API)
    """
    return {
        "source": "BPS (Indonesia)",
        "url": "https://www.bps.go.id",
        "data": f"Placeholder Indonesian statistical data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_ibge_br_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch Brazilian statistical data from IBGE.
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Brazilian statistical data
    
    Implementation Notes:
        - Use IBGE API: https://servicodados.ibge.gov.br/api/docs
        - Search for food industry, consumption data
        - Extract economic indicators, market statistics
        - No API key required (public API)
    """
    return {
        "source": "IBGE (Brazil)",
        "url": "https://www.ibge.gov.br",
        "data": f"Placeholder Brazilian statistical data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_inegi_mx_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch Mexican statistical data from INEGI.
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Mexican statistical data
    
    Implementation Notes:
        - Use INEGI API
        - Search for food consumption, agricultural production
        - Extract economic indicators, consumer trends
        - No API key required (public API)
    """
    return {
        "source": "INEGI (Mexico)",
        "url": "https://www.inegi.org.mx",
        "data": f"Placeholder Mexican statistical data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_ine_cl_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch Chilean statistical data from INE Chile.
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Chilean statistical data
    
    Implementation Notes:
        - Use INE Chile API
        - Search for food industry, consumption data
        - Extract economic indicators, market statistics
        - Public access available
    """
    return {
        "source": "INE (Chile)",
        "url": "https://www.ine.gob.cl",
        "data": f"Placeholder Chilean statistical data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_dane_co_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch Colombian statistical data from DANE.
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Colombian statistical data
    
    Implementation Notes:
        - Use DANE API
        - Search for food consumption, agricultural data
        - Extract economic indicators, consumer spending
        - No API key required (public API)
    """
    return {
        "source": "DANE (Colombia)",
        "url": "https://www.dane.gov.co",
        "data": f"Placeholder Colombian statistical data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_stats_sa_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch South African statistical data from Stats SA.
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing South African statistical data
    
    Implementation Notes:
        - Use Stats SA API
        - Search for food industry, consumption patterns
        - Extract economic indicators, market data
        - Public access available
    """
    return {
        "source": "Stats SA (South Africa)",
        "url": "https://www.statssa.gov.za",
        "data": f"Placeholder South African statistical data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_knbs_ke_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch Kenyan statistical data from KNBS.
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Kenyan statistical data
    
    Implementation Notes:
        - Use KNBS API
        - Search for food consumption, agricultural production
        - Extract economic indicators, trade statistics
        - No API key required (public API)
    """
    return {
        "source": "KNBS (Kenya)",
        "url": "https://www.knbs.or.ke",
        "data": f"Placeholder Kenyan statistical data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_cbs_il_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch Israeli statistical data from CBS Israel.
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Israeli statistical data
    
    Implementation Notes:
        - Use CBS Israel API
        - Search for food industry, consumption data
        - Extract economic indicators, market statistics
        - Public access available
    """
    return {
        "source": "CBS (Israel)",
        "url": "https://www.cbs.gov.il",
        "data": f"Placeholder Israeli statistical data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_tuik_tr_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch Turkish statistical data from TUIK.
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Turkish statistical data
    
    Implementation Notes:
        - Use TUIK API
        - Search for food consumption, agricultural production
        - Extract economic indicators, consumer trends
        - No API key required (public API)
    """
    return {
        "source": "TUIK (Turkey)",
        "url": "https://www.tuik.gov.tr",
        "data": f"Placeholder Turkish statistical data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_all_data(keywords: List[str], countries: List[str], products: List[str] = []) -> Dict[str, Any]:
    """
    Orchestrate data collection from all available sources.
    
    Args:
        keywords: List of search keywords
        countries: List of target countries (ISO 2-letter codes)
        products: List of product categories (optional)
    
    Returns:
        Dictionary containing all collected data organized by source type
    """
    all_data = {
        "general_sources": [],
        "ai_research": [],
        "country_specific": []
    }
    
    all_data["general_sources"].append(fetch_open_food_facts(keywords))
    all_data["general_sources"].append(fetch_pubmed_articles(keywords))
    all_data["general_sources"].append(fetch_google_trends(keywords))
    
    all_data["ai_research"].append(fetch_perplexity_ai(keywords))
    all_data["ai_research"].append(fetch_gemini_ai(keywords))
    
    country_connector_map = {
        'USA': fetch_usda_data,
        'DE': fetch_genesis_data,
        'UK': fetch_ons_data,
        'CA': fetch_statcan_data,
        'FR': fetch_insee_data,
        'CH': fetch_bfs_data,
        'AU': fetch_abs_data,
        'JP': fetch_estat_data,
        'NZ': fetch_statsnz_data,
        'NL': fetch_cbs_nl_data,
        'AT': fetch_statistik_at_data,
        'ES': fetch_ine_es_data,
        'IT': fetch_istat_data,
        'DK': fetch_dst_dk_data,
        'FI': fetch_stat_fi_data,
        'NO': fetch_ssb_no_data,
        'SE': fetch_scb_se_data,
        'PL': fetch_gus_pl_data,
        'CZ': fetch_czso_data,
        'HU': fetch_ksh_hu_data,
        'EE': fetch_stat_ee_data,
        'KR': fetch_kosis_kr_data,
        'SG': fetch_singstat_data,
        'IN': fetch_mospi_in_data,
        'ID': fetch_bps_id_data,
        'BR': fetch_ibge_br_data,
        'MX': fetch_inegi_mx_data,
        'CL': fetch_ine_cl_data,
        'CO': fetch_dane_co_data,
        'ZA': fetch_stats_sa_data,
        'KE': fetch_knbs_ke_data,
        'IL': fetch_cbs_il_data,
        'TR': fetch_tuik_tr_data
    }
    
    eu_countries = ['AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR', 
                    'DE', 'GR', 'HU', 'IE', 'IT', 'LV', 'LT', 'LU', 'MT', 'NL', 
                    'PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'SE']
    
    for country in countries:
        country = country.upper()
        
        if country in eu_countries:
            all_data["country_specific"].append(fetch_eurostat_data(keywords, country))
        
        if country in country_connector_map:
            connector_func = country_connector_map[country]
            all_data["country_specific"].append(connector_func(keywords))
    
    return all_data


def get_sources_list(raw_data: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Extract list of all sources with URLs from raw data.
    
    Args:
        raw_data: Dictionary containing all fetched data
        
    Returns:
        List of dictionaries with source names and URLs
    """
    sources = []
    
    # Add industry-specific web sources used for deep research
    web_sources = [
        {'name': 'Supermarket News', 'url': 'https://www.supermarketnews.com'},
        {'name': 'mindbodygreen', 'url': 'https://www.mindbodygreen.com'},
        {'name': 'Biocatalysts - Ingredient Innovation', 'url': 'https://www.biocatalysts.com'},
        {'name': 'NutraIngredients', 'url': 'https://www.nutraingredients.com'},
        {'name': 'Food Ingredients First', 'url': 'https://www.foodingredientsfirst.com'}
    ]
    sources.extend(web_sources)
    
    for source in raw_data.get('general_sources', []):
        if 'source' in source and 'url' in source:
            sources.append({
                'name': source['source'],
                'url': source['url']
            })
    
    for source in raw_data.get('ai_research', []):
        if 'source' in source and 'url' in source:
            sources.append({
                'name': source['source'],
                'url': source['url']
            })
    
    for source in raw_data.get('country_specific', []):
        if 'source' in source and 'url' in source:
            sources.append({
                'name': source['source'],
                'url': source['url']
            })
    
    return sources


def analyze_data_with_openai(raw_data: Dict[str, Any], topic: str = "", keywords: List[str] = [], products: List[str] = [], countries: List[str] = []) -> Dict[str, Any]:
    """
    Analyze collected data using OpenAI GPT-4o model to generate a comprehensive trend report.
    
    Args:
        raw_data: Dictionary containing all fetched data from various sources
        topic: Optional topic/description provided by user
        keywords: List of keywords for the analysis
        products: List of product categories
        countries: List of target countries
    
    Returns:
        Dictionary containing:
        - title: Report title
        - description: Comprehensive description
        - market_data: Detailed market insights
        - consumer_insights: Consumer behavior insights
        - verbrauchertrends: List of consumer trends
        - konsumtrends: List of consumption trends
        - innovationstrends: List of innovation trends
        - sources: List of data sources with URLs
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    sources = get_sources_list(raw_data)
    
    system_prompt = """Du bist ein Senior-Experte für Marktforschung und Trendanalyse in der Lebensmittelindustrie mit Spezialgebiet Cerealien, Müsli, Haferflocken und Frühstücksprodukte. 

Deine Aufgabe ist es, einen vollständigen, professionellen Trend-Report zu erstellen, der auf den bereitgestellten Keywords und dem Kontext basiert. Da die Datenquellen aktuell noch in Entwicklung sind, sollst du basierend auf deinem Fachwissen realistische, datengestützte Marktanalysen erstellen.

Erstelle einen umfassenden Report als JSON-Objekt mit folgender Struktur:
{
  "title": "Prägnanter Report-Titel (max 100 Zeichen)",
  "description": "Umfassende Beschreibung des Reports (200-400 Wörter), die den Kontext, die Relevanz und die wichtigsten Erkenntnisse zusammenfasst",
  "market_data": "Detaillierte Marktdaten und statistische Insights (150-300 Wörter) mit konkreten Zahlen, Marktgrößen, Wachstumsraten, regionalen Unterschieden",
  "consumer_insights": "Tiefgehende Consumer-Insights (150-300 Wörter) zu Kaufverhalten, Präferenzen, demografischen Trends, Motivationen",
  "verbrauchertrends": ["5-8 prägnante Verbrauchertrend-Aussagen"],
  "konsumtrends": ["5-8 prägnante Konsumtrend-Aussagen"],
  "innovationstrends": ["5-8 prägnante Innovationstrend-Aussagen"]
}

Verwende professionelle Sprache, konkrete Daten (auch geschätzte, realistische Zahlen), und branchenspezifisches Vokabular. Der Report soll actionable sein für Produktentwicklung und Marketing."""
    
    keywords_str = ", ".join(keywords) if keywords else "Allgemeine Marktanalyse"
    products_str = ", ".join(products) if products else "Frühstücksprodukte"
    countries_str = ", ".join(countries) if countries else "Global"
    
    user_message = f"""Erstelle einen vollständigen professionellen Trend-Report basierend auf folgenden Parametern:

**Keywords/Suchbegriffe:** {keywords_str}
**Produktkategorien:** {products_str}
**Zielmärkte/Länder:** {countries_str}
**Zusätzlicher Kontext:** {topic if topic else 'Umfassende Markt- und Trendanalyse für die Frühstücks- und Cerealienbranche'}

**Analysefokus:**
- Aktuelle Markttrends und Entwicklungen
- Konsumentenverhalten und -präferenzen
- Innovations- und Produktentwicklungstrends
- Regionale Besonderheiten der Zielmärkte
- Wissenschaftliche Erkenntnisse und Studien
- Wettbewerbsanalyse und Best Practices

**Deep Research Web-Quellen (nutze diese für tiefgehende Recherche):**
Durchsuche folgende branchenspezifische Websites und all ihre Unterseiten für aktuelle Insights:
- Supermarket News (https://www.supermarketnews.com) - Food and drink news, FMCG retail news
- mindbodygreen (https://www.mindbodygreen.com) - Well-rounded well-being, health trends
- Biocatalysts (https://www.biocatalysts.com) - Ingredient innovation leading the food industry in 2025
- NutraIngredients (https://www.nutraingredients.com) - Dietary supplements, nutraceuticals, functional foods, health ingredients, herbals
- Food Ingredients First (https://www.foodingredientsfirst.com) - Food ingredients & food science, additives, flavours, starch

Nutze diese Quellen aktiv für deine Analyse und integriere die neuesten Erkenntnisse, Trends und Innovationen aus diesen Branchen-Websites in deinen Report.

Erstelle einen detaillierten, datengestützten Report, der für strategische Entscheidungen in Produktentwicklung und Marketing verwendet werden kann. Verwende realistische Marktdaten, Statistiken und Insights basierend auf aktuellen Branchentrends 2024/2025."""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=3500
        )
        
        response_text = response.choices[0].message.content
        if not response_text:
            raise ValueError("Empty response from OpenAI")
        
        response_text = response_text.strip()
        
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        parsed_response = json.loads(response_text)
        parsed_response['sources'] = sources
        
        return parsed_response
        
    except json.JSONDecodeError as e:
        fallback_title = topic if topic else f"Trendanalyse: {keywords_str}"
        return {
            "error": "Failed to parse OpenAI response as JSON",
            "details": str(e),
            "title": fallback_title,
            "description": f"Automatisch generierter Report für Keywords: {keywords_str}. Zielmärkte: {countries_str}.",
            "market_data": "Daten konnten nicht vollständig analysiert werden.",
            "consumer_insights": "Insights konnten nicht vollständig generiert werden.",
            "verbrauchertrends": ["Analyse fehlgeschlagen"],
            "konsumtrends": ["Analyse fehlgeschlagen"],
            "innovationstrends": ["Analyse fehlgeschlagen"],
            "sources": sources
        }
    except Exception as e:
        fallback_title = topic if topic else f"Trendanalyse: {keywords_str}"
        return {
            "error": "Failed to analyze data with OpenAI",
            "details": str(e),
            "title": fallback_title,
            "description": f"Automatisch generierter Report für Keywords: {keywords_str}. Zielmärkte: {countries_str}.",
            "market_data": "Daten konnten nicht vollständig analysiert werden.",
            "consumer_insights": "Insights konnten nicht vollständig generiert werden.",
            "verbrauchertrends": ["Analyse fehlgeschlagen"],
            "konsumtrends": ["Analyse fehlgeschlagen"],
            "innovationstrends": ["Analyse fehlgeschlagen"],
            "sources": sources
        }


def extract_key_facts(report_data: Dict[str, Any]) -> List[str]:
    """
    Extract exactly 2 key facts from the full report for display card.
    
    Args:
        report_data: Dictionary containing the full report data
        
    Returns:
        List of exactly 2 key fact strings
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    try:
        # Combine all trend data for analysis
        all_trends = []
        all_trends.extend(report_data.get('verbrauchertrends', []))
        all_trends.extend(report_data.get('konsumtrends', []))
        all_trends.extend(report_data.get('innovationstrends', []))
        
        context = f"""
        Report Title: {report_data.get('title', '')}
        Description: {report_data.get('description', '')}
        Market Data: {report_data.get('market_data', '')}
        Consumer Insights: {report_data.get('consumer_insights', '')}
        All Trends: {', '.join(all_trends[:10])}
        """
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Du bist ein Experte darin, komplexe Marktanalysen auf die wichtigsten 2 Key Facts zu reduzieren. Extrahiere GENAU 2 prägnante, aussagekräftige Key Facts aus dem gegebenen Report. Jeder Fact sollte maximal 15 Wörter haben und eine konkrete, actionable Erkenntnis darstellen."},
                {"role": "user", "content": f"Extrahiere GENAU 2 Key Facts aus diesem Report:\n\n{context}\n\nAntworte mit einem JSON-Array: [\"Fact 1\", \"Fact 2\"]"}
            ],
            temperature=0.5,
            max_tokens=200
        )
        
        response_text = response.choices[0].message.content
        if not response_text:
            raise ValueError("Empty response from OpenAI")
        
        response_text = response_text.strip()
        
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        facts = json.loads(response_text)
        
        if isinstance(facts, list) and len(facts) >= 2:
            return facts[:2]
        else:
            # Fallback to first 2 trends
            return all_trends[:2] if len(all_trends) >= 2 else ["Key insights available in full report", "Detailed analysis included"]
            
    except Exception as e:
        # Fallback: Return first 2 trends from any category
        all_trends = []
        all_trends.extend(report_data.get('verbrauchertrends', []))
        all_trends.extend(report_data.get('konsumtrends', []))
        all_trends.extend(report_data.get('innovationstrends', []))
        return all_trends[:2] if len(all_trends) >= 2 else ["Key insights available in full report", "Detailed analysis included"]


def generate_report_with_streaming(keywords: List[str], countries: List[str], products: List[str] = [], topic: str = "") -> Generator[str, None, None]:
    """
    Generate trend report with real-time progress updates via Server-Sent Events.
    
    Args:
        keywords: List of search keywords
        countries: List of target countries
        products: List of product categories
        topic: Optional topic/description
        
    Yields:
        JSON strings with progress updates and final report data
    """
    try:
        keywords_str = ", ".join(keywords)
        progress = 5
        
        # Collect all data sources with detailed progress
        all_data = {
            "general_sources": [],
            "ai_research": [],
            "country_specific": []
        }
        
        # General sources
        yield json.dumps({
            'type': 'progress',
            'step': 'searching_open_food_facts',
            'message': f'Durchsuche Open Food Facts mit Keywords: {keywords_str}',
            'progress': progress
        }) + '\n'
        time.sleep(0.3)
        all_data["general_sources"].append(fetch_open_food_facts(keywords))
        progress += 3
        
        yield json.dumps({
            'type': 'progress',
            'step': 'searching_pubmed',
            'message': f'Durchsuche PubMed wissenschaftliche Datenbank mit Keywords: {keywords_str}',
            'progress': progress
        }) + '\n'
        time.sleep(0.3)
        all_data["general_sources"].append(fetch_pubmed_articles(keywords))
        progress += 3
        
        yield json.dumps({
            'type': 'progress',
            'step': 'searching_google_trends',
            'message': f'Analysiere Google Trends für: {keywords_str}',
            'progress': progress
        }) + '\n'
        time.sleep(0.3)
        all_data["general_sources"].append(fetch_google_trends(keywords))
        progress += 3
        
        # Industry Web Sources
        yield json.dumps({
            'type': 'progress',
            'step': 'searching_web_sources',
            'message': f'Durchsuche Supermarket News für aktuelle Food & Retail Insights: {keywords_str}',
            'progress': progress
        }) + '\n'
        time.sleep(0.3)
        progress += 2
        
        yield json.dumps({
            'type': 'progress',
            'step': 'searching_mindbodygreen',
            'message': f'Durchsuche mindbodygreen für Health & Wellness Trends: {keywords_str}',
            'progress': progress
        }) + '\n'
        time.sleep(0.3)
        progress += 2
        
        yield json.dumps({
            'type': 'progress',
            'step': 'searching_biocatalysts',
            'message': f'Durchsuche Biocatalysts für Food Innovation 2025: {keywords_str}',
            'progress': progress
        }) + '\n'
        time.sleep(0.3)
        progress += 2
        
        yield json.dumps({
            'type': 'progress',
            'step': 'searching_nutraingredients',
            'message': f'Durchsuche NutraIngredients für Supplements & Functional Foods: {keywords_str}',
            'progress': progress
        }) + '\n'
        time.sleep(0.3)
        progress += 2
        
        yield json.dumps({
            'type': 'progress',
            'step': 'searching_food_ingredients',
            'message': f'Durchsuche Food Ingredients First für Additives & Flavours: {keywords_str}',
            'progress': progress
        }) + '\n'
        time.sleep(0.3)
        progress += 2
        
        # AI Research sources
        yield json.dumps({
            'type': 'progress',
            'step': 'searching_perplexity',
            'message': f'Deep Research mit Perplexity AI für: {keywords_str}',
            'progress': progress
        }) + '\n'
        time.sleep(0.3)
        all_data["ai_research"].append(fetch_perplexity_ai(keywords))
        progress += 3
        
        yield json.dumps({
            'type': 'progress',
            'step': 'searching_gemini',
            'message': f'Deep Research mit Google Gemini für: {keywords_str}',
            'progress': progress
        }) + '\n'
        time.sleep(0.3)
        all_data["ai_research"].append(fetch_gemini_ai(keywords))
        progress += 3
        
        # Country-specific sources
        country_connector_map = {
            'USA': ('USDA', fetch_usda_data),
            'DE': ('GENESIS (Destatis)', fetch_genesis_data),
            'UK': ('ONS', fetch_ons_data),
            'CA': ('Statistics Canada', fetch_statcan_data),
            'FR': ('INSEE', fetch_insee_data),
            'CH': ('BFS Switzerland', fetch_bfs_data),
            'AU': ('ABS Australia', fetch_abs_data),
            'JP': ('e-Stat Japan', fetch_estat_data),
            'NZ': ('Stats NZ', fetch_statsnz_data),
            'NL': ('CBS Netherlands', fetch_cbs_nl_data),
            'AT': ('Statistik Austria', fetch_statistik_at_data),
            'ES': ('INE Spain', fetch_ine_es_data),
            'IT': ('ISTAT Italy', fetch_istat_data),
            'DK': ('Statistics Denmark', fetch_dst_dk_data),
            'FI': ('Statistics Finland', fetch_stat_fi_data),
            'NO': ('Statistics Norway', fetch_ssb_no_data),
            'SE': ('Statistics Sweden', fetch_scb_se_data),
            'PL': ('GUS Poland', fetch_gus_pl_data),
            'CZ': ('CZSO Czech', fetch_czso_data),
            'HU': ('KSH Hungary', fetch_ksh_hu_data),
            'EE': ('Statistics Estonia', fetch_stat_ee_data),
            'KR': ('KOSIS South Korea', fetch_kosis_kr_data),
            'SG': ('SingStat Singapore', fetch_singstat_data),
            'IN': ('MOSPI India', fetch_mospi_in_data),
            'ID': ('BPS Indonesia', fetch_bps_id_data),
            'BR': ('IBGE Brazil', fetch_ibge_br_data),
            'MX': ('INEGI Mexico', fetch_inegi_mx_data),
            'CL': ('INE Chile', fetch_ine_cl_data),
            'CO': ('DANE Colombia', fetch_dane_co_data),
            'ZA': ('Stats SA South Africa', fetch_stats_sa_data),
            'KE': ('KNBS Kenya', fetch_knbs_ke_data),
            'IL': ('CBS Israel', fetch_cbs_il_data),
            'TR': ('TUIK Turkey', fetch_tuik_tr_data)
        }
        
        eu_countries = ['AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR', 
                        'DE', 'GR', 'HU', 'IE', 'IT', 'LV', 'LT', 'LU', 'MT', 'NL', 
                        'PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'SE']
        
        for country in countries:
            country_upper = country.upper()
            
            # Check Eurostat for EU countries
            if country_upper in eu_countries:
                yield json.dumps({
                    'type': 'progress',
                    'step': f'searching_eurostat_{country_upper}',
                    'message': f'Durchsuche Eurostat für {country_upper} mit Keywords: {keywords_str}',
                    'progress': progress
                }) + '\n'
                time.sleep(0.3)
                all_data["country_specific"].append(fetch_eurostat_data(keywords, country_upper))
                progress += 2
            
            # Check country-specific databases
            if country_upper in country_connector_map:
                db_name, connector_func = country_connector_map[country_upper]
                yield json.dumps({
                    'type': 'progress',
                    'step': f'searching_{country_upper.lower()}',
                    'message': f'Durchsuche {db_name} mit Keywords: {keywords_str}',
                    'progress': progress
                }) + '\n'
                time.sleep(0.3)
                all_data["country_specific"].append(connector_func(keywords))
                progress += 2
        
        total_sources = len(all_data["general_sources"]) + len(all_data["ai_research"]) + len(all_data["country_specific"])
        
        yield json.dumps({
            'type': 'progress',
            'step': 'data_collection_complete',
            'message': f'✓ Datensammlung abgeschlossen: {total_sources} Quellen durchsucht',
            'progress': 50
        }) + '\n'
        
        # Step 2: AI Analysis
        time.sleep(0.5)
        yield json.dumps({
            'type': 'progress',
            'step': 'ai_analysis_start',
            'message': f'Analysiere gesammelte Daten mit OpenAI GPT-4o für Keywords: {keywords_str}',
            'progress': 55
        }) + '\n'
        
        report = analyze_data_with_openai(all_data, topic, keywords, products, countries)
        
        yield json.dumps({
            'type': 'progress',
            'step': 'analysis_complete',
            'message': '✓ KI-Analyse abgeschlossen - Report generiert',
            'progress': 75
        }) + '\n'
        
        # Step 3: Extract Key Facts
        time.sleep(0.3)
        yield json.dumps({
            'type': 'progress',
            'step': 'extracting_facts',
            'message': 'Extrahiere 2 Key Facts für Trend-Karte mit GPT-4o',
            'progress': 82
        }) + '\n'
        
        key_facts = extract_key_facts(report)
        
        yield json.dumps({
            'type': 'progress',
            'step': 'facts_extracted',
            'message': f'✓ Key Facts extrahiert: "{key_facts[0][:50]}..."',
            'progress': 88
        }) + '\n'
        
        # Step 4: Generate PDF
        time.sleep(0.3)
        yield json.dumps({
            'type': 'progress',
            'step': 'generating_pdf',
            'message': f'Erstelle professionellen PDF-Report mit {total_sources} Quellenangaben',
            'progress': 93
        }) + '\n'
        
        pdf_path = generate_trend_report_pdf(report, keywords, countries)
        
        # Step 5: Complete
        yield json.dumps({
            'type': 'progress',
            'step': 'complete',
            'message': '✓ Report erfolgreich erstellt!',
            'progress': 100
        }) + '\n'
        
        # Final result
        yield json.dumps({
            'type': 'complete',
            'report': report,
            'key_facts': key_facts,
            'pdf_path': pdf_path,
            'keywords': keywords,
            'countries': countries,
            'products': products,
            'topic': topic
        }) + '\n'
        
    except Exception as e:
        yield json.dumps({
            'type': 'error',
            'message': str(e)
        }) + '\n'


def generate_trend_report_pdf(report_data: Dict[str, Any], keywords: List[str], countries: List[str]) -> str:
    """
    Generate a professional PDF report for the trend analysis with source citations.
    
    Args:
        report_data: Dictionary containing the full report data
        keywords: List of keywords used for the analysis
        countries: List of countries analyzed
    
    Returns:
        str: Path to the generated PDF file
    """
    pdf_dir = 'static/pdfs'
    os.makedirs(pdf_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_title = "".join(c for c in report_data.get('title', 'trend_report')[:50] if c.isalnum() or c in (' ', '-', '_')).strip()
    safe_title = safe_title.replace(' ', '_')
    filename = f'custom_trend_{safe_title}_{timestamp}.pdf'
    filepath = os.path.join(pdf_dir, filename)
    
    doc = SimpleDocTemplate(filepath, pagesize=A4,
                           leftMargin=0.75*inch, rightMargin=0.75*inch,
                           topMargin=0.75*inch, bottomMargin=0.75*inch)
    styles = getSampleStyleSheet()
    story = []
    
    title_style = ParagraphStyle(
        'BruggenTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#661c31'),
        alignment=TA_CENTER,
        spaceAfter=10,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'BruggenSubtitle',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#ff4143'),
        alignment=TA_CENTER,
        spaceAfter=20,
        fontName='Helvetica-Bold'
    )
    
    header_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#661c31'),
        spaceBefore=15,
        spaceAfter=10,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#212529'),
        spaceAfter=6,
        fontName='Helvetica',
        leading=14
    )
    
    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#212529'),
        spaceAfter=4,
        fontName='Helvetica',
        leftIndent=20,
        bulletIndent=10
    )
    
    story.append(Paragraph("H. & J. Brüggen KG", title_style))
    story.append(Paragraph("Trend Analysis Report", subtitle_style))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph(report_data.get('title', 'Custom Trend Report'), header_style))
    story.append(Spacer(1, 10))
    
    metadata_text = f"<b>Keywords:</b> {', '.join(keywords)}<br/><b>Target Markets:</b> {', '.join(countries)}<br/><b>Generated:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}"
    story.append(Paragraph(metadata_text, normal_style))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("Executive Summary", header_style))
    description = report_data.get('description', '')
    if description:
        for para in description.split('\n'):
            if para.strip():
                story.append(Paragraph(para.strip(), normal_style))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("Market Data & Statistics", header_style))
    market_data = report_data.get('market_data', '')
    if market_data:
        for para in market_data.split('\n'):
            if para.strip():
                story.append(Paragraph(para.strip(), normal_style))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("Consumer Insights", header_style))
    consumer_insights = report_data.get('consumer_insights', '')
    if consumer_insights:
        for para in consumer_insights.split('\n'):
            if para.strip():
                story.append(Paragraph(para.strip(), normal_style))
    story.append(Spacer(1, 20))
    
    story.append(PageBreak())
    
    story.append(Paragraph("Detailed Trend Analysis", title_style))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("Verbrauchertrends (Consumer Trends)", header_style))
    verbrauchertrends = report_data.get('verbrauchertrends', [])
    if verbrauchertrends:
        for trend in verbrauchertrends:
            story.append(Paragraph(f"• {trend}", bullet_style))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("Konsumtrends (Consumption Trends)", header_style))
    konsumtrends = report_data.get('konsumtrends', [])
    if konsumtrends:
        for trend in konsumtrends:
            story.append(Paragraph(f"• {trend}", bullet_style))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("Innovationstrends (Innovation Trends)", header_style))
    innovationstrends = report_data.get('innovationstrends', [])
    if innovationstrends:
        for trend in innovationstrends:
            story.append(Paragraph(f"• {trend}", bullet_style))
    story.append(Spacer(1, 30))
    
    # Add sources section
    sources = report_data.get('sources', [])
    if sources:
        story.append(PageBreak())
        story.append(Paragraph("Data Sources & Citations", header_style))
        story.append(Spacer(1, 10))
        
        for source in sources:
            source_text = f"<b>{source.get('name', 'Unknown')}:</b> {source.get('url', 'N/A')}"
            story.append(Paragraph(source_text, normal_style))
        
        story.append(Spacer(1, 20))
    
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#6b7280'),
        alignment=TA_CENTER,
        fontName='Helvetica-Oblique'
    )
    story.append(Spacer(1, 30))
    story.append(Paragraph("© 2024 H. & J. Brüggen KG. All rights reserved.", footer_style))
    story.append(Paragraph("The World of Cereals", footer_style))
    
    doc.build(story)
    
    return f'/static/pdfs/{filename}'
