import os
import json
import asyncio
from typing import List, Dict, Any
from openai import OpenAI

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
        "data": f"Placeholder Gemini research for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_eurostat_data(keywords: List[str], country_code: str) -> Dict[str, Any]:
    """
    Fetch statistical data from Eurostat (EU statistical office).
    
    Args:
        keywords: List of search keywords
        country_code: EU country code (e.g., 'DE', 'FR', 'IT')
    
    Returns:
        Dictionary containing statistical data
    
    Implementation Notes:
        - Use Eurostat API: https://ec.europa.eu/eurostat/web/main/data/web-services
        - Search for relevant datasets based on keywords and country
        - Extract consumption patterns, production statistics
        - No API key required
    """
    return {
        "source": f"Eurostat ({country_code})",
        "data": f"Placeholder Eurostat data for {country_code}: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_usda_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch agricultural and food data from USDA (United States).
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing USDA data
    
    Implementation Notes:
        - Use USDA APIs: https://www.usda.gov/developer
        - Requires API key (get from Replit Secrets: USDA_API_KEY)
        - Access FoodData Central, NASS QuickStats
        - Extract nutrition data, production statistics
    """
    return {
        "source": "USDA (USA)",
        "data": f"Placeholder USDA data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_genesis_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch statistical data from GENESIS-Online (Germany).
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing German statistical data
    
    Implementation Notes:
        - Use GENESIS-Online API: https://www-genesis.destatis.de/
        - Requires registration and credentials (get from Replit Secrets: GENESIS_USER, GENESIS_PASSWORD)
        - Search for food consumption, production statistics
        - Extract relevant German market data
    """
    return {
        "source": "GENESIS-Online (DE)",
        "data": f"Placeholder GENESIS data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_ons_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch statistical data from ONS (Office for National Statistics, UK).
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing UK statistical data
    
    Implementation Notes:
        - Use ONS API: https://developer.ons.gov.uk/
        - No API key required
        - Search for food consumption, household spending
        - Extract UK market trends
    """
    return {
        "source": "ONS (UK)",
        "data": f"Placeholder ONS data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_statcan_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch statistical data from Statistics Canada.
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Canadian statistical data
    
    Implementation Notes:
        - Use Statistics Canada API: https://www.statcan.gc.ca/eng/developers
        - No API key required
        - Access food consumption, production data
        - Extract Canadian market trends
    """
    return {
        "source": "Statistics Canada (CA)",
        "data": f"Placeholder Statistics Canada data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_insee_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch statistical data from INSEE (France).
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing French statistical data
    
    Implementation Notes:
        - Use INSEE API: https://api.insee.fr/
        - Requires API key (get from Replit Secrets: INSEE_API_KEY)
        - Access consumption patterns, production statistics
        - Extract French market data
    """
    return {
        "source": "INSEE (FR)",
        "data": f"Placeholder INSEE data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_bfs_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch statistical data from BFS (Switzerland).
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Swiss statistical data
    
    Implementation Notes:
        - Use BFS/OFS API: https://www.bfs.admin.ch/
        - Access available datasets
        - Extract Swiss consumption and production data
        - May require specific data portal credentials
    """
    return {
        "source": "BFS (CH)",
        "data": f"Placeholder BFS data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_abs_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch statistical data from ABS (Australian Bureau of Statistics).
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Australian statistical data
    
    Implementation Notes:
        - Use ABS API: https://www.abs.gov.au/about/data-services/application-programming-interfaces-apis
        - No API key required for basic access
        - Access food consumption, production statistics
        - Extract Australian market trends
    """
    return {
        "source": "ABS (AU)",
        "data": f"Placeholder ABS data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_estat_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch statistical data from e-Stat (Japan).
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Japanese statistical data
    
    Implementation Notes:
        - Use e-Stat API: https://www.e-stat.go.jp/
        - Requires API key (get from Replit Secrets: ESTAT_API_KEY)
        - Access food consumption, production data
        - Extract Japanese market trends
    """
    return {
        "source": "e-Stat (JP)",
        "data": f"Placeholder e-Stat data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_statsnz_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch statistical data from Stats NZ (New Zealand).
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing New Zealand statistical data
    
    Implementation Notes:
        - Use Stats NZ API: https://www.stats.govt.nz/
        - Access available datasets
        - Extract consumption and production statistics
        - No API key required for public data
    """
    return {
        "source": "Stats NZ (NZ)",
        "data": f"Placeholder Stats NZ data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_cbs_nl_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch statistical data from CBS (Netherlands).
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Dutch statistical data
    
    Implementation Notes:
        - Use CBS Open Data API: https://www.cbs.nl/en-gb/onze-diensten/open-data
        - No API key required
        - Access consumption patterns, production data
        - Extract Dutch market trends
    """
    return {
        "source": "CBS (NL)",
        "data": f"Placeholder CBS data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_statistik_at_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch statistical data from Statistik Austria.
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Austrian statistical data
    
    Implementation Notes:
        - Use Statistik Austria API or data portal
        - Access consumption and production statistics
        - Extract Austrian market data
        - Check for API access requirements
    """
    return {
        "source": "Statistik Austria (AT)",
        "data": f"Placeholder Statistik Austria data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_ine_es_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch statistical data from INE (Spain).
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Spanish statistical data
    
    Implementation Notes:
        - Use INE API: https://www.ine.es/
        - Access available datasets
        - Extract Spanish consumption and production data
        - Check for API documentation and requirements
    """
    return {
        "source": "INE (ES)",
        "data": f"Placeholder INE data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_istat_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch statistical data from ISTAT (Italy).
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Italian statistical data
    
    Implementation Notes:
        - Use ISTAT API: http://www.istat.it/
        - Access consumption patterns, production statistics
        - Extract Italian market data
        - Check API documentation for access requirements
    """
    return {
        "source": "ISTAT (IT)",
        "data": f"Placeholder ISTAT data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_dst_dk_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch statistical data from DST (Denmark).
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Danish statistical data
    
    Implementation Notes:
        - Use Statistics Denmark API: https://www.dst.dk/
        - Access food consumption, production data
        - Extract Danish market trends
        - Check for API access requirements
    """
    return {
        "source": "DST (DK)",
        "data": f"Placeholder DST data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_stat_fi_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch statistical data from Statistics Finland.
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Finnish statistical data
    
    Implementation Notes:
        - Use Statistics Finland API: https://www.stat.fi/
        - Access consumption and production statistics
        - Extract Finnish market data
        - No API key required for public data
    """
    return {
        "source": "Statistics Finland (FI)",
        "data": f"Placeholder Statistics Finland data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_ssb_no_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch statistical data from SSB (Norway).
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Norwegian statistical data
    
    Implementation Notes:
        - Use Statistics Norway API: https://www.ssb.no/
        - Access food consumption, production data
        - Extract Norwegian market trends
        - Check API documentation for requirements
    """
    return {
        "source": "SSB (NO)",
        "data": f"Placeholder SSB data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_scb_se_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch statistical data from SCB (Statistics Sweden).
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Swedish statistical data
    
    Implementation Notes:
        - Use SCB API: https://www.scb.se/
        - Access consumption patterns, production statistics
        - Extract Swedish market data
        - No API key required for public data
    """
    return {
        "source": "SCB (SE)",
        "data": f"Placeholder SCB data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_gus_pl_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch statistical data from GUS (Poland).
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Polish statistical data
    
    Implementation Notes:
        - Use Statistics Poland API: https://stat.gov.pl/
        - Access food consumption, production data
        - Extract Polish market trends
        - Check for API documentation and requirements
    """
    return {
        "source": "GUS (PL)",
        "data": f"Placeholder GUS data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_czso_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch statistical data from CZSO (Czech Republic).
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Czech statistical data
    
    Implementation Notes:
        - Use Czech Statistical Office API: https://www.czso.cz/
        - Access consumption and production statistics
        - Extract Czech market data
        - Check API access requirements
    """
    return {
        "source": "CZSO (CZ)",
        "data": f"Placeholder CZSO data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_ksh_hu_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch statistical data from KSH (Hungary).
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Hungarian statistical data
    
    Implementation Notes:
        - Use Hungarian Central Statistical Office API
        - Access food consumption, production data
        - Extract Hungarian market trends
        - Check for API documentation
    """
    return {
        "source": "KSH (HU)",
        "data": f"Placeholder KSH data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_stat_ee_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch statistical data from Statistics Estonia.
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Estonian statistical data
    
    Implementation Notes:
        - Use Statistics Estonia API: https://www.stat.ee/
        - Access consumption patterns, production statistics
        - Extract Estonian market data
        - No API key required for public data
    """
    return {
        "source": "Statistics Estonia (EE)",
        "data": f"Placeholder Statistics Estonia data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_kosis_kr_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch statistical data from KOSIS (South Korea).
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing South Korean statistical data
    
    Implementation Notes:
        - Use KOSIS API: https://kosis.kr/
        - Requires API key (get from Replit Secrets: KOSIS_API_KEY)
        - Access food consumption, production data
        - Extract South Korean market trends
    """
    return {
        "source": "KOSIS (KR)",
        "data": f"Placeholder KOSIS data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_singstat_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch statistical data from SingStat (Singapore).
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Singapore statistical data
    
    Implementation Notes:
        - Use SingStat API: https://www.singstat.gov.sg/
        - Requires API key (get from Replit Secrets: SINGSTAT_API_KEY)
        - Access consumption patterns, import/export data
        - Extract Singapore market trends
    """
    return {
        "source": "SingStat (SG)",
        "data": f"Placeholder SingStat data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_mospi_in_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch statistical data from MOSPI (India).
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Indian statistical data
    
    Implementation Notes:
        - Use Ministry of Statistics API (India)
        - Access food consumption, production data
        - Extract Indian market trends
        - Check for data portal and API requirements
    """
    return {
        "source": "MOSPI (IN)",
        "data": f"Placeholder MOSPI data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_bps_id_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch statistical data from BPS (Indonesia).
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Indonesian statistical data
    
    Implementation Notes:
        - Use Statistics Indonesia API: https://www.bps.go.id/
        - Access consumption and production statistics
        - Extract Indonesian market data
        - Check for API access requirements
    """
    return {
        "source": "BPS (ID)",
        "data": f"Placeholder BPS data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_ibge_br_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch statistical data from IBGE (Brazil).
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Brazilian statistical data
    
    Implementation Notes:
        - Use IBGE API: https://www.ibge.gov.br/
        - Access food consumption, production data
        - Extract Brazilian market trends
        - No API key required for public data
    """
    return {
        "source": "IBGE (BR)",
        "data": f"Placeholder IBGE data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_inegi_mx_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch statistical data from INEGI (Mexico).
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Mexican statistical data
    
    Implementation Notes:
        - Use INEGI API: https://www.inegi.org.mx/
        - Access consumption patterns, production statistics
        - Extract Mexican market data
        - Check for API token requirements
    """
    return {
        "source": "INEGI (MX)",
        "data": f"Placeholder INEGI data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_ine_cl_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch statistical data from INE (Chile).
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Chilean statistical data
    
    Implementation Notes:
        - Use INE Chile API: https://www.ine.cl/
        - Access food consumption, production data
        - Extract Chilean market trends
        - Check for API documentation
    """
    return {
        "source": "INE (CL)",
        "data": f"Placeholder INE Chile data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_dane_co_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch statistical data from DANE (Colombia).
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Colombian statistical data
    
    Implementation Notes:
        - Use DANE API: https://www.dane.gov.co/
        - Access consumption and production statistics
        - Extract Colombian market data
        - Check for API access requirements
    """
    return {
        "source": "DANE (CO)",
        "data": f"Placeholder DANE data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_stats_sa_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch statistical data from Stats SA (South Africa).
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing South African statistical data
    
    Implementation Notes:
        - Use Statistics South Africa: http://www.statssa.gov.za/
        - Access food consumption, production data
        - Extract South African market trends
        - Check for data portal access
    """
    return {
        "source": "Stats SA (ZA)",
        "data": f"Placeholder Stats SA data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_knbs_ke_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch statistical data from KNBS (Kenya).
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Kenyan statistical data
    
    Implementation Notes:
        - Use Kenya National Bureau of Statistics
        - Access consumption patterns, production statistics
        - Extract Kenyan market data
        - Check for available datasets and API
    """
    return {
        "source": "KNBS (KE)",
        "data": f"Placeholder KNBS data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_cbs_il_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch statistical data from CBS (Israel).
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Israeli statistical data
    
    Implementation Notes:
        - Use Central Bureau of Statistics Israel
        - Access food consumption, production data
        - Extract Israeli market trends
        - Check for API access and documentation
    """
    return {
        "source": "CBS (IL)",
        "data": f"Placeholder CBS Israel data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_tuik_tr_data(keywords: List[str]) -> Dict[str, Any]:
    """
    Fetch statistical data from TÜİK (Turkey).
    
    Args:
        keywords: List of search keywords
    
    Returns:
        Dictionary containing Turkish statistical data
    
    Implementation Notes:
        - Use Turkish Statistical Institute (TÜİK)
        - Access consumption and production statistics
        - Extract Turkish market data
        - Check for API documentation and requirements
    """
    return {
        "source": "TÜİK (TR)",
        "data": f"Placeholder TÜİK data for keywords: {', '.join(keywords)}",
        "status": "stub"
    }


def fetch_all_data(keywords: List[str], countries: List[str], products: List[str] = None) -> Dict[str, Any]:
    """
    Main orchestration function to fetch data from all relevant sources.
    
    Args:
        keywords: List of search keywords
        countries: List of country codes to fetch data for
        products: Optional list of product categories
    
    Returns:
        Dictionary containing all fetched data organized by source
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


def analyze_data_with_openai(raw_data: Dict[str, Any], topic: str = "") -> Dict[str, Any]:
    """
    Analyze collected data using OpenAI GPT-4o model.
    
    Args:
        raw_data: Dictionary containing all fetched data from various sources
        topic: Optional topic/description provided by user
    
    Returns:
        Dictionary containing structured trend analysis with three main categories:
        - verbrauchertrends (consumer trends)
        - konsumtrends (consumption trends)
        - innovationstrends (innovation trends)
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    system_prompt = """Du bist ein Experte für Marktforschung und Trendanalyse in der Lebensmittelindustrie mit dem Spezialgebiet Cerealien und Frühstücksprodukte. Deine Aufgabe ist es, die folgenden Rohdaten (wissenschaftliche Abstracts, Suchtrends, Produktdaten, statistische Erhebungen aus verschiedenen Ländern) zu analysieren. Identifiziere und synthetisiere daraus die wichtigsten globalen und regionalen Trends. Strukturiere deine Ausgabe ausschließlich als JSON-Objekt mit den folgenden drei Hauptschlüsseln: 'verbrauchertrends', 'konsumtrends', 'innovationstrends'. Jeder Schlüssel soll eine Liste von prägnant formulierten Trendaussagen (Strings) enthalten. Gib nur das JSON-Objekt zurück, ohne einleitenden oder abschließenden Text."""
    
    data_summary = json.dumps(raw_data, indent=2)
    
    user_message = f"""Analysiere die folgenden Rohdaten und erstelle einen strukturierten Trend-Report.

Topic/Kontext: {topic if topic else 'Allgemeine Trendanalyse'}

Rohdaten:
{data_summary}

Erstelle einen umfassenden Trend-Report als JSON-Objekt mit den Schlüsseln 'verbrauchertrends', 'konsumtrends', und 'innovationstrends'."""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        response_text = response.choices[0].message.content.strip()
        
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        parsed_response = json.loads(response_text)
        
        return parsed_response
        
    except json.JSONDecodeError as e:
        return {
            "error": "Failed to parse OpenAI response as JSON",
            "details": str(e),
            "verbrauchertrends": ["Fehler bei der Analyse"],
            "konsumtrends": ["Fehler bei der Analyse"],
            "innovationstrends": ["Fehler bei der Analyse"]
        }
    except Exception as e:
        return {
            "error": "Failed to analyze data with OpenAI",
            "details": str(e),
            "verbrauchertrends": ["Fehler bei der Analyse"],
            "konsumtrends": ["Fehler bei der Analyse"],
            "innovationstrends": ["Fehler bei der Analyse"]
        }
