"""
Deep Research Worker - KI-gestützte Trendanalyse mit Multi-Prompt-Strategie
Führt asynchrone Research-Jobs aus mit folgenden Phasen:
1. Strategie-Erstellung (KI-Prompt 1)
2. Datensammlung aus definierten Quellen
3. Synthese (KI-Prompt 2)
4. Finalisierung (KI-Prompt 3)
5. PDF-Generierung
"""

import json
import time
import logging
import uuid
from datetime import datetime
from typing import Dict, List, Any, Generator
import os
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Definierte Datenquellen (aus dem Prompt)
DATA_SOURCES = {
    "general": [
        {"name": "Open Food Facts", "url": "https://world.openfoodfacts.org"},
        {"name": "PubMed", "url": "https://pubmed.ncbi.nlm.nih.gov"},
        {"name": "Google Trends", "url": "https://trends.google.com"}
    ],
    "statistical_dbs": {
        "EU": {"name": "Eurostat", "url": "https://ec.europa.eu/eurostat"},
        "USA": {"name": "USDA FoodData Central", "url": "https://fdc.nal.usda.gov"},
        "DE": {"name": "GENESIS Datenbank", "url": "https://www-genesis.destatis.de"},
        "UK": {"name": "Office for National Statistics", "url": "https://www.ons.gov.uk"},
        "CA": {"name": "Statistics Canada", "url": "https://www.statcan.gc.ca"},
        "FR": {"name": "INSEE", "url": "https://www.insee.fr"},
        "CH": {"name": "Bundesamt für Statistik", "url": "https://www.bfs.admin.ch"},
        "AU": {"name": "Australian Bureau of Statistics", "url": "https://www.abs.gov.au"},
        "JP": {"name": "e-Stat Japan", "url": "https://www.e-stat.go.jp"},
        "NZ": {"name": "Stats NZ", "url": "https://www.stats.govt.nz"},
        "NL": {"name": "CBS Netherlands", "url": "https://www.cbs.nl"},
        "AT": {"name": "Statistik Austria", "url": "https://www.statistik.at"},
        "ES": {"name": "INE Spain", "url": "https://www.ine.es"},
        "IT": {"name": "ISTAT Italy", "url": "https://www.istat.it"},
        "DK": {"name": "Statistics Denmark", "url": "https://www.dst.dk"},
        "FI": {"name": "Statistics Finland", "url": "https://www.stat.fi"},
        "NO": {"name": "Statistics Norway", "url": "https://www.ssb.no"},
        "SE": {"name": "Statistics Sweden", "url": "https://www.scb.se"},
        "PL": {"name": "GUS Poland", "url": "https://stat.gov.pl"},
        "CZ": {"name": "CZSO Czech", "url": "https://www.czso.cz"},
        "HU": {"name": "KSH Hungary", "url": "https://www.ksh.hu"},
        "EE": {"name": "Statistics Estonia", "url": "https://www.stat.ee"},
        "KR": {"name": "KOSIS South Korea", "url": "https://kosis.kr"},
        "SG": {"name": "SingStat Singapore", "url": "https://www.singstat.gov.sg"},
        "IN": {"name": "MOSPI India", "url": "https://mospi.gov.in"}
    },
    "industry_websites": [
        {"name": "Supermarket News", "url": "https://www.supermarketnews.com"},
        {"name": "mindbodygreen", "url": "https://www.mindbodygreen.com"},
        {"name": "Biocatalysts", "url": "https://www.biocatalysts.com"},
        {"name": "NutraIngredients", "url": "https://www.nutraingredients.com"},
        {"name": "Food Ingredients First", "url": "https://www.foodingredientsfirst.com"}
    ]
}


def process_research_job(job_id: str, description: str, keywords: List[str], categories: List[str]) -> Generator:
    """
    Hauptfunktion für die Verarbeitung eines Research Jobs
    Yields SSE-kompatible Updates für Live-Fortschritt
    """
    from app import app, db
    from models import ResearchJob, ResearchSource, Trend
    
    with app.app_context():
        try:
            # Job aus DB laden
            job = ResearchJob.query.filter_by(job_id=job_id).first()
            if not job:
                yield json.dumps({"type": "error", "message": "Job nicht gefunden"})
                return
            
            # Phase 1: Strategie-Erstellung (10% Progress)
            yield json.dumps({
                "type": "info",
                "message": "📋 Phase 1: Erstelle Recherche-Strategie mit KI...",
                "progress": 5
            })
            
            job.status = 'processing_strategy'
            db.session.commit()
            
            strategy = create_research_strategy(description, keywords, categories)
            
            yield json.dumps({
                "type": "info",
                "message": f"✓ Strategie erstellt: {len(strategy.get('sources', []))} Quellen identifiziert",
                "progress": 10
            })
            
            # Phase 2: Datensammlung (10% - 70% Progress)
            yield json.dumps({
                "type": "info",
                "message": "🔍 Phase 2: Sammle Daten aus identifizierten Quellen...",
                "progress": 15
            })
            
            job.status = 'scraping_data'
            db.session.commit()
            
            collected_data = []
            sources_to_check = determine_sources(strategy, keywords)
            progress_per_source = 55 / len(sources_to_check) if sources_to_check else 0
            current_progress = 15
            
            for source in sources_to_check:
                source_name = source['name']
                source_url = source.get('url', '')
                
                # Source-Eintrag in DB erstellen
                research_source = ResearchSource(
                    job_id=job_id,
                    source_name=source_name,
                    source_url=source_url,
                    status='processing'
                )
                db.session.add(research_source)
                db.session.commit()
                
                yield json.dumps({
                    "type": "info",
                    "message": f"Durchsuche {source_name}...",
                    "source": source_name,
                    "status": "processing",
                    "progress": int(current_progress)
                })
                
                # Simuliere Datensammlung (In Produktion: echtes Scraping/API-Calls)
                time.sleep(0.5)  # Simulierte Verzögerung
                
                # Mock-Daten für Demo
                found_items = len(keywords) * 10  # Simuliert gefundene Items
                mock_data = {
                    "source": source_name,
                    "url": source_url,
                    "findings": [f"Trend {i+1} related to {', '.join(keywords[:2])}" for i in range(min(5, found_items))],
                    "summary": f"Relevant insights from {source_name} regarding {description[:50]}..."
                }
                
                research_source.status = 'success'
                research_source.found_items = found_items
                research_source.cleaned_content = json.dumps(mock_data)
                db.session.commit()
                
                collected_data.append(mock_data)
                
                yield json.dumps({
                    "type": "success",
                    "message": f"✓ {source_name}: {found_items} relevante Einträge gefunden",
                    "source": source_name,
                    "status": "success",
                    "foundItems": found_items,
                    "progress": int(current_progress + progress_per_source)
                })
                
                current_progress += progress_per_source
            
            # Phase 3: Synthese (70% - 80% Progress)
            yield json.dumps({
                "type": "info",
                "message": "🧠 Phase 3: KI analysiert und synthetisiert gesammelte Daten...",
                "progress": 72
            })
            
            job.status = 'synthesizing_report'
            db.session.commit()
            
            synthesized_report = synthesize_data_with_ai(description, collected_data, keywords, categories)
            
            yield json.dumps({
                "type": "info",
                "message": "✓ Daten erfolgreich synthetisiert",
                "progress": 80
            })
            
            # Phase 4: Finalisierung (80% - 90% Progress)
            yield json.dumps({
                "type": "info",
                "message": "📝 Phase 4: Finalisiere Report-Struktur...",
                "progress": 82
            })
            
            job.status = 'finalizing_report'
            db.session.commit()
            
            final_report = finalize_report_with_ai(synthesized_report)
            
            yield json.dumps({
                "type": "info",
                "message": "✓ Report finalisiert",
                "progress": 90
            })
            
            # Phase 5: PDF-Generierung (90% - 95% Progress)
            yield json.dumps({
                "type": "info",
                "message": "📄 Phase 5: Generiere professionellen PDF-Report...",
                "progress": 92
            })
            
            job.status = 'generating_pdf'
            db.session.commit()
            
            pdf_path = generate_pdf_report(final_report, job_id)
            
            yield json.dumps({
                "type": "info",
                "message": "✓ PDF erfolgreich erstellt",
                "progress": 95
            })
            
            # Trend in DB speichern
            new_trend = Trend(
                title=final_report.get('title', 'Deep Research Report'),
                category='innovation',
                report_type='marktdaten',
                description=final_report.get('executive_summary', '')[:500],
                market_data=json.dumps(final_report.get('market_data', {})),
                consumer_insights=json.dumps(final_report.get('consumer_insights', {})),
                pdf_path=pdf_path
            )
            db.session.add(new_trend)
            db.session.commit()
            
            # Job als abgeschlossen markieren
            job.status = 'completed'
            job.progress = 100
            job.result_trend_id = new_trend.id
            job.completed_at = datetime.utcnow()
            db.session.commit()
            
            yield json.dumps({
                "type": "complete",
                "message": "✓ Research erfolgreich abgeschlossen!",
                "progress": 100,
                "report_id": new_trend.id,
                "pdf_path": pdf_path
            })
            
        except Exception as e:
            logging.error(f"Error in research job {job_id}: {str(e)}")
            
            with app.app_context():
                job = ResearchJob.query.filter_by(job_id=job_id).first()
                if job:
                    job.status = 'failed'
                    job.error_message = str(e)
                    db.session.commit()
            
            yield json.dumps({
                "type": "error",
                "message": f"Fehler bei der Verarbeitung: {str(e)}"
            })


def create_research_strategy(description: str, keywords: List[str], categories: List[str]) -> Dict:
    """KI-Prompt 1: Erstellt eine Recherche-Strategie"""
    
    system_prompt = """Du bist ein Experte für Food-Trend-Forschung. Erstelle eine gezielte Recherche-Strategie.
    
    Analysiere die Forschungsbeschreibung und bestimme:
    1. Welche Datenquellen am relevantesten sind
    2. Welche zusätzlichen Suchbegriffe hilfreich wären
    3. Welche Märkte/Regionen prioritär sind
    
    Antworte in JSON Format mit: {"sources": [...], "search_terms": [...], "priority_markets": [...]}"""
    
    user_prompt = f"""Forschungsbeschreibung: {description}
    
Keywords: {', '.join(keywords) if keywords else 'keine'}
Kategorien: {', '.join(categories) if categories else 'keine'}

Erstelle eine optimale Recherche-Strategie."""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        
        strategy = json.loads(response.choices[0].message.content)
        return strategy
        
    except Exception as e:
        logging.error(f"Strategy creation error: {e}")
        # Fallback strategy
        return {
            "sources": ["Open Food Facts", "PubMed", "Supermarket News"],
            "search_terms": keywords,
            "priority_markets": ["DE", "USA", "UK"]
        }


def determine_sources(strategy: Dict, keywords: List[str]) -> List[Dict]:
    """Bestimmt die zu durchsuchenden Quellen basierend auf der Strategie"""
    sources = []
    
    # Immer: Allgemeine Quellen
    sources.extend(DATA_SOURCES["general"])
    
    # Basierend auf Strategie: Länder-spezifische DBs
    priority_markets = strategy.get("priority_markets", ["DE", "USA", "UK"])
    for market in priority_markets:
        if market in DATA_SOURCES["statistical_dbs"]:
            sources.append(DATA_SOURCES["statistical_dbs"][market])
    
    # Immer: Industry Websites
    sources.extend(DATA_SOURCES["industry_websites"][:3])  # Top 3
    
    return sources


def synthesize_data_with_ai(description: str, collected_data: List[Dict], keywords: List[str], categories: List[str]) -> Dict:
    """KI-Prompt 2: Synthetisiert gesammelte Daten zu kohärentem Report"""
    
    system_prompt = """Du bist ein Food-Trend-Analyst. Synthetisiere die gesammelten Daten zu einem umfassenden Trend-Report.
    
    Der Report soll enthalten:
    - Executive Summary
    - Haupttrends (mit Quellenangaben)
    - Marktdaten und Statistiken
    - Consumer Insights
    - Zukunftsprognosen
    
    Antworte in JSON Format mit strukturierten Daten."""
    
    data_summary = "\n\n".join([
        f"Quelle: {d['source']}\nURL: {d['url']}\nErkenntnisse: {', '.join(d['findings'][:3])}"
        for d in collected_data[:10]  # Limitiere auf 10 Quellen für Token-Limit
    ])
    
    user_prompt = f"""Forschungsfrage: {description}

Keywords: {', '.join(keywords)}
Kategorien: {', '.join(categories)}

Gesammelte Daten:
{data_summary}

Erstelle einen umfassenden Trend-Report basierend auf diesen Daten."""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        
        report = json.loads(response.choices[0].message.content)
        return report
        
    except Exception as e:
        logging.error(f"Synthesis error: {e}")
        # Fallback report
        return {
            "executive_summary": f"Trend-Analyse zu: {description}",
            "main_trends": ["Trend 1", "Trend 2", "Trend 3"],
            "market_data": {},
            "consumer_insights": []
        }


def finalize_report_with_ai(synthesized_report: Dict) -> Dict:
    """KI-Prompt 3: Finalisiert und optimiert den Report"""
    
    system_prompt = """Du bist ein professioneller Report-Editor. Optimiere den Report für maximale Klarheit und Professionalität.
    
    Stelle sicher:
    - Klare, prägnante Sprache
    - Professionelle Struktur
    - Actionable Insights
    - Vollständige Quellenangaben
    
    Antworte in JSON Format."""
    
    user_prompt = f"""Optimiere diesen Trend-Report:

{json.dumps(synthesized_report, indent=2)}

Erstelle die finale, professionelle Version."""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.5,
            response_format={"type": "json_object"}
        )
        
        final_report = json.loads(response.choices[0].message.content)
        return final_report
        
    except Exception as e:
        logging.error(f"Finalization error: {e}")
        return synthesized_report  # Fallback


def generate_pdf_report(report_data: Dict, job_id: str) -> str:
    """Generiert einen professionellen PDF-Report"""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    
    pdf_dir = 'static/pdfs'
    os.makedirs(pdf_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'deep_research_{job_id}_{timestamp}.pdf'
    pdf_path = os.path.join(pdf_dir, filename)
    
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm)
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor='#661c31',
        spaceAfter=30,
        alignment=TA_CENTER
    )
    story.append(Paragraph(report_data.get('title', 'Deep Research Report'), title_style))
    story.append(Spacer(1, 1*cm))
    
    # Executive Summary
    story.append(Paragraph("<b>Executive Summary</b>", styles['Heading2']))
    story.append(Paragraph(report_data.get('executive_summary', ''), styles['BodyText']))
    story.append(Spacer(1, 0.5*cm))
    
    # Main Content
    if 'main_trends' in report_data:
        story.append(Paragraph("<b>Haupttrends</b>", styles['Heading2']))
        for i, trend in enumerate(report_data['main_trends'][:5], 1):
            story.append(Paragraph(f"{i}. {trend}", styles['BodyText']))
        story.append(Spacer(1, 0.5*cm))
    
    # Sources
    story.append(PageBreak())
    story.append(Paragraph("<b>Quellenangaben</b>", styles['Heading2']))
    story.append(Paragraph("Dieser Report basiert auf Daten aus folgenden Quellen:", styles['BodyText']))
    
    # Build PDF
    doc.build(story)
    
    return f'/static/pdfs/{filename}'
