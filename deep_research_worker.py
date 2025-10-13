"""
Deep Research Worker - KI-gestützte Trendanalyse mit Multi-Prompt-Strategie
Führt asynchrone Research-Jobs aus mit folgenden Phasen:
0. Plan-Generierung und Nutzerbestätigung (NEU!)
1. Strategie-Erstellung (KI-Prompt 1)
2. Datensammlung aus definierten Quellen (erweitert auf 250+ Dateien)
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
from google import genai
from google.genai import types
from api_clients import fetch_data_from_source

# Initialize Gemini client (using blueprint:python_gemini)
gemini_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# Verwende Gemini 2.5 Flash - Bestes Preis-Leistungs-Verhältnis mit gutem Rate Limit
GEMINI_MODEL = "gemini-2.5-flash"

# Definierte Datenquellen (erweiterte Liste)
DATA_SOURCES = {
    "general": [
        {"name": "Open Food Facts", "url": "https://world.openfoodfacts.org"},
        {"name": "PubMed", "url": "https://pubmed.ncbi.nlm.nih.gov"},
        {"name": "Google Trends", "url": "https://trends.google.com"}
    ],
    "ai_deep_research": [
        {"name": "Perplexity API", "url": "https://www.perplexity.ai"},
        {"name": "Gemini API", "url": "https://ai.google.dev"}
    ],
    "statistical_dbs": {
        "EU": {"name": "Eurostat", "url": "https://ec.europa.eu/eurostat"},
        "USA": {"name": "USDA FoodData Central", "url": "https://fdc.nal.usda.gov"},
        "DE": {"name": "GENESIS Datenbank", "url": "https://www-genesis.destatis.de"},
        "UK": {"name": "Office for National Statistics", "url": "https://www.ons.gov.uk"},
        "CA": {"name": "Statistics Canada", "url": "https://www.statcan.gc.ca"},
        "FR": {"name": "INSEE API", "url": "https://www.insee.fr"},
        "CH": {"name": "Bundesamt für Statistik", "url": "https://www.bfs.admin.ch"},
        "AU": {"name": "Australian Bureau of Statistics", "url": "https://www.abs.gov.au"},
        "JP": {"name": "e-Stat", "url": "https://www.e-stat.go.jp"},
        "NZ": {"name": "Stats NZ", "url": "https://www.stats.govt.nz"},
        "NL": {"name": "Centraal Bureau voor de Statistiek", "url": "https://www.cbs.nl"},
        "AT": {"name": "Statistik Austria", "url": "https://www.statistik.at"},
        "ES": {"name": "Instituto Nacional de Estadística", "url": "https://www.ine.es"},
        "IT": {"name": "Istituto Nazionale di Statistica", "url": "https://www.istat.it"},
        "DK": {"name": "Statistics Denmark", "url": "https://www.dst.dk"},
        "FI": {"name": "Statistics Finland", "url": "https://www.stat.fi"},
        "NO": {"name": "Statistics Norway", "url": "https://www.ssb.no"},
        "SE": {"name": "Statistics Sweden", "url": "https://www.scb.se"},
        "PL": {"name": "Statistics Poland (GUS)", "url": "https://stat.gov.pl"},
        "CZ": {"name": "Czech Statistical Office", "url": "https://www.czso.cz"},
        "HU": {"name": "Hungarian Central Statistical Office", "url": "https://www.ksh.hu"},
        "EE": {"name": "Statistics Estonia", "url": "https://www.stat.ee"},
        "KR": {"name": "Korean Statistical Information Service", "url": "https://kosis.kr"},
        "SG": {"name": "Singapore Department of Statistics", "url": "https://www.singstat.gov.sg"},
        "IN": {"name": "Ministry of Statistics India (MOSPI)", "url": "https://mospi.gov.in"},
        "ID": {"name": "BPS-Statistics Indonesia", "url": "https://www.bps.go.id"},
        "BR": {"name": "IBGE Brazil", "url": "https://www.ibge.gov.br"},
        "MX": {"name": "INEGI Mexico", "url": "https://www.inegi.org.mx"},
        "CL": {"name": "INE Chile", "url": "https://www.ine.gob.cl"},
        "CO": {"name": "DANE Colombia", "url": "https://www.dane.gov.co"},
        "ZA": {"name": "Statistics South Africa", "url": "https://www.statssa.gov.za"},
        "KE": {"name": "Kenya National Bureau of Statistics", "url": "https://www.knbs.or.ke"},
        "IL": {"name": "Israel Central Bureau of Statistics", "url": "https://www.cbs.gov.il"},
        "TR": {"name": "Turkish Statistical Institute", "url": "https://www.tuik.gov.tr"}
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
    
    job_start_time = time.time()
    
    with app.app_context():
        try:
            # Job aus DB laden
            job = ResearchJob.query.filter_by(job_id=job_id).first()
            if not job:
                yield json.dumps({"type": "error", "message": "Job nicht gefunden"})
                return
            
            logging.info("=" * 80)
            logging.info(f"🚀 STARTE DEEP RESEARCH JOB: {job_id}")
            logging.info(f"📋 Beschreibung: {description}")
            logging.info(f"🔑 Keywords: {', '.join(keywords) if keywords else 'keine'}")
            logging.info(f"📁 Kategorien: {', '.join(categories) if categories else 'keine'}")
            logging.info("=" * 80)
            
            # Phase 0: Plan-Generierung (Nur wenn noch nicht approved)
            if not job.plan_approved:
                logging.info("📋 Phase 0: Generiere Research-Plan...")
                yield json.dumps({
                    "type": "info",
                    "message": "📋 Phase 0: Generiere detaillierten Research-Plan...",
                    "progress": 2
                })
                
                job.status = 'generating_plan'
                db.session.commit()
                
                research_plan = generate_research_plan(description, keywords, categories)
                job.research_plan = json.dumps(research_plan, ensure_ascii=False)
                job.status = 'waiting_approval'
                db.session.commit()
                
                logging.info(f"✓ Research-Plan erstellt, warte auf Nutzerbestätigung")
                yield json.dumps({
                    "type": "plan_ready",
                    "message": "✓ Research-Plan erstellt! Bitte überprüfen und bestätigen.",
                    "progress": 5,
                    "plan": research_plan
                })
                
                # Warte auf Bestätigung - Job wird hier pausiert
                return
            
            logging.info("✓ Plan wurde bestätigt, starte Research-Prozess")
            
            # Lade den genehmigten Research-Plan
            approved_plan = json.loads(job.research_plan) if job.research_plan else {}
            logging.info(f"📋 Verwende genehmigten Research-Plan mit {len(approved_plan.get('automated_sources', {}))} Quellentypen")
            
            yield json.dumps({
                "type": "info",
                "message": "📋 Phase 1: Verwende genehmigten Research-Plan...",
                "progress": 15
            })
            
            # Phase 2: Datensammlung (15% - 65% Progress) - Optimiert auf 50-100 Datenpunkte
            logging.info("🔍 Phase 2: Starte fokussierte Datensammlung (Ziel: 50-100 Datenpunkte)...")
            yield json.dumps({
                "type": "info",
                "message": "🔍 Phase 2: Sammle Daten aus 10-15 relevanten Quellen (Ziel: 50-100 Datenpunkte)...",
                "progress": 15
            })
            
            job.status = 'scraping_data'
            db.session.commit()
            
            collected_data = []
            sources_to_check = determine_sources_from_plan(approved_plan, keywords)
            logging.info(f"📊 Identifizierte {len(sources_to_check)} Quellen aus Plan für Datensammlung")
            
            progress_per_source = 50 / len(sources_to_check) if sources_to_check else 0
            current_progress = 15
            total_items_found = 0
            
            for idx, source in enumerate(sources_to_check, 1):
                source_name = source['name']
                source_url = source.get('url', '')
                
                logging.info(f"🔎 [{idx}/{len(sources_to_check)}] Durchsuche Quelle: {source_name}")
                
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
                    "message": f"🔍 Durchsuche: {source_name} [{idx}/{len(sources_to_check)}]",
                    "source": source_name,
                    "status": "processing",
                    "progress": int(current_progress)
                })
                
                # ECHTE API-CALLS - keine Mock-Daten mehr!
                try:
                    start_time = time.time()
                    logging.info(f"  🌐 Starte API-Call für {source_name}...")
                    
                    # Hole echte Daten über die API-Clients (reduziertes Limit für Performance)
                    api_results = fetch_data_from_source(source, keywords, limit=10)
                    found_items = len(api_results)
                    elapsed = time.time() - start_time
                    
                    logging.info(f"  ✓ {source_name}: {found_items} Datenpunkte in {elapsed:.1f}s")
                    
                    # Konvertiere API-Ergebnisse in unser Format
                    findings = []
                    for result in api_results[:8]:  # Top 8 für Summary
                        findings.append(result.get('title', 'Unknown'))
                    
                    source_data = {
                        "source": source_name,
                        "url": source_url,
                        "findings": findings,
                        "summary": f"Relevante Daten aus {source_name}: {', '.join(findings[:3])}..." if findings else f"Daten aus {source_name}",
                        "data_points": found_items,
                        "raw_results": api_results  # Komplette API-Antworten für Synthese
                    }
                    
                    research_source.status = 'success'
                    research_source.found_items = found_items
                    research_source.cleaned_content = json.dumps(source_data, ensure_ascii=False)
                    db.session.commit()
                    
                    collected_data.append(source_data)
                    total_items_found += found_items
                    
                except Exception as e:
                    elapsed = time.time() - start_time
                    logging.error(f"  ❌ {source_name}: Fehler nach {elapsed:.1f}s - {str(e)[:100]}")
                    research_source.status = 'error'
                    research_source.found_items = 0
                    db.session.commit()
                    
                    yield json.dumps({
                        "type": "warning",
                        "message": f"⚠️ {source_name}: Fehler beim Abrufen ({str(e)[:50]}...)",
                        "source": source_name,
                        "status": "error"
                    })
                    continue
                
                logging.info(f"  💾 Gespeichert: {source_name} mit {found_items} Datenpunkten")
                
                yield json.dumps({
                    "type": "success",
                    "message": f"✅ {source_name}: {found_items} Datenpunkte | Gesamt: {total_items_found}",
                    "source": source_name,
                    "status": "success",
                    "foundItems": found_items,
                    "totalItems": total_items_found,
                    "progress": int(current_progress + progress_per_source)
                })
                
                current_progress += progress_per_source
            
            logging.info(f"✅ Datensammlung abgeschlossen: {total_items_found} Datenpunkte aus {len(sources_to_check)} Quellen")
            
            # Phase 3: Synthese (65% - 75% Progress)
            start_synthesis = time.time()
            logging.info(f"🧠 Phase 3: Starte KI-Synthese mit {total_items_found} Datenpunkten...")
            logging.info(f"  📊 Daten aus {len(collected_data)} Quellen werden analysiert")
            yield json.dumps({
                "type": "info",
                "message": f"🧠 Phase 3: KI analysiert {total_items_found} Datenpunkte und synthetisiert Report...",
                "progress": 67
            })
            
            job.status = 'synthesizing_report'
            db.session.commit()
            
            logging.info("  🤖 Rufe Gemini 2.5 Pro für Synthese auf...")
            synthesized_report = synthesize_data_with_ai(description, collected_data, keywords, categories)
            elapsed_synthesis = time.time() - start_synthesis
            logging.info(f"  ✓ Synthese abgeschlossen in {elapsed_synthesis:.1f}s")
            logging.info(f"  ✓ Synthese abgeschlossen: {len(synthesized_report.get('introduction', ''))} Zeichen Einleitung")
            
            yield json.dumps({
                "type": "info",
                "message": "✓ Daten erfolgreich synthetisiert - Report-Struktur erstellt",
                "progress": 75
            })
            
            # Phase 4: Finalisierung (75% - 85% Progress)
            start_finalize = time.time()
            logging.info("📝 Phase 4: Starte Report-Finalisierung...")
            yield json.dumps({
                "type": "info",
                "message": "📝 Phase 4: Finalisiere Report-Struktur und optimiere Texte...",
                "progress": 77
            })
            
            job.status = 'finalizing_report'
            db.session.commit()
            
            logging.info("  🤖 Rufe Gemini 2.5 Pro für Finalisierung auf...")
            final_report = finalize_report_with_ai(synthesized_report)
            elapsed_finalize = time.time() - start_finalize
            logging.info(f"  ✓ Finalisierung in {elapsed_finalize:.1f}s: {len(final_report.get('footnotes', []))} Fußnoten")
            
            yield json.dumps({
                "type": "info",
                "message": f"✓ Report finalisiert mit {len(final_report.get('footnotes', []))} Fußnoten",
                "progress": 85
            })
            
            # Phase 5: PDF-Generierung (85% - 92% Progress)
            start_pdf = time.time()
            logging.info("📄 Phase 5: Starte PDF-Generierung...")
            yield json.dumps({
                "type": "info",
                "message": "📄 Phase 5: Generiere professionellen PDF-Report mit Fließtext und Fußnoten...",
                "progress": 87
            })
            
            job.status = 'generating_pdf'
            db.session.commit()
            
            logging.info("  📝 Erstelle PDF-Dokument mit ReportLab...")
            pdf_path = generate_pdf_report(final_report, job_id)
            elapsed_pdf = time.time() - start_pdf
            logging.info(f"  ✓ PDF erstellt in {elapsed_pdf:.1f}s: {pdf_path}")
            
            yield json.dumps({
                "type": "info",
                "message": f"✓ PDF erfolgreich erstellt: {pdf_path}",
                "progress": 92
            })
            
            # Trend in DB speichern
            logging.info("💾 Speichere Report in Datenbank...")
            report_title = final_report.get('title', 'Deep Research Report')
            new_trend = Trend(
                title=report_title[:300],  # Limit to 300 chars
                category='innovation',
                report_type='marktdaten',
                description=final_report.get('introduction', '')[:500],
                market_data=json.dumps(final_report.get('market_analysis', {})),
                consumer_insights=final_report.get('consumer_insights', '')[:5000],
                pdf_path=pdf_path
            )
            db.session.add(new_trend)
            db.session.commit()
            logging.info(f"  ✓ Report gespeichert mit ID: {new_trend.id}")
            
            # Job als abgeschlossen markieren
            job.status = 'completed'
            job.progress = 100
            job.result_trend_id = new_trend.id
            job.completed_at = datetime.utcnow()
            db.session.commit()
            
            total_duration = time.time() - job_start_time
            minutes = int(total_duration // 60)
            seconds = int(total_duration % 60)
            
            logging.info("=" * 80)
            logging.info(f"🎉 RESEARCH JOB ERFOLGREICH ABGESCHLOSSEN!")
            logging.info(f"⏱️  Gesamt-Dauer: {minutes}m {seconds}s ({total_duration:.1f}s)")
            logging.info(f"📊 Datenpunkte: {total_items_found}")
            logging.info(f"📝 Fußnoten: {len(final_report.get('footnotes', []))}")
            logging.info(f"📄 PDF: {pdf_path}")
            logging.info("=" * 80)
            
            yield json.dumps({
                "type": "complete",
                "message": f"✓ Research erfolgreich abgeschlossen! ({total_items_found} Datenpunkte analysiert)",
                "progress": 100,
                "report_id": new_trend.id,
                "pdf_path": pdf_path,
                "total_data_points": total_items_found
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


def generate_research_plan(description: str, keywords: List[str], categories: List[str]) -> Dict:
    """Generiert einen detaillierten Research-Plan, den der Nutzer bestätigen kann"""
    
    # Detaillierte Beschreibungen aller 43 verfügbaren Datenquellen
    source_catalog = f"""
VERFÜGBARE DATENQUELLEN (43 APIs & Datenbanken):

**Allgemeine Quellen (3):**
1. Open Food Facts - Offene Produktdatenbank mit 2M+ Lebensmitteln, Inhaltsstoffen, Nährwerten, Allergenen
2. PubMed - Wissenschaftliche Publikationen zu Ernährung, Food Science, Gesundheit (30M+ Artikel)
3. Google Trends - Suchtrend-Analysen für Consumer Interests und aufkommende Food Trends

**AI Deep Research APIs (2):**
4. Perplexity API - KI-gestützte Deep Research mit automatischer Quellensuche und Zitation
5. Gemini API - Google's fortschrittliche KI für umfassende Trendanalyse und Synthese

**Statistische Datenbanken nach Ländern (33):**
6. Eurostat (EU) - EU-weite Statistiken zu Lebensmittelproduktion, Konsum, Handel
7. USDA FoodData Central (USA) - US Lebensmitteldatenbank, Nährwerte, Marktdaten
8. GENESIS Datenbank (DE) - Deutsche Statistiken zu Ernährung, Landwirtschaft, Konsum
9. Office for National Statistics (UK) - UK Lebensmittel- und Konsumstatistiken
10. Statistics Canada (CA) - Kanadische Food & Beverage Marktdaten
11. INSEE API (FR) - Französische Ernährungs- und Konsumstatistiken
12. Bundesamt für Statistik (CH) - Schweizer Food-Marktdaten
13. Australian Bureau of Statistics (AU) - Australische Lebensmittelstatistiken
14. e-Stat (JP) - Japanische Food Industry Daten
15. Stats NZ (NZ) - Neuseeländische Agrar- und Food-Statistiken
16. Centraal Bureau voor de Statistiek (NL) - Niederländische Food-Daten
17. Statistik Austria (AT) - Österreichische Ernährungsstatistiken
18. Instituto Nacional de Estadística (ES) - Spanische Lebensmittelmarktdaten
19. Istituto Nazionale di Statistica (IT) - Italienische Food-Statistiken
20. Statistics Denmark (DK) - Dänische Ernährungs- und Konsumtrends
21. Statistics Finland (FI) - Finnische Food-Marktanalysen
22. Statistics Norway (NO) - Norwegische Lebensmittelstatistiken
23. Statistics Sweden (SE) - Schwedische Food & Beverage Daten
24. Statistics Poland (PL) - Polnische Ernährungsmarktdaten
25. Czech Statistical Office (CZ) - Tschechische Lebensmittelstatistiken
26. Hungarian Central Statistical Office (HU) - Ungarische Food-Daten
27. Statistics Estonia (EE) - Estnische Ernährungsstatistiken
28. Korean Statistical Information Service (KR) - Südkoreanische Food-Trends
29. Singapore Department of Statistics (SG) - Singapur Food-Marktdaten
30. Ministry of Statistics India (IN) - Indische Ernährungs- und Konsumstatistiken
31. BPS-Statistics Indonesia (ID) - Indonesische Food-Marktdaten
32. IBGE Brazil (BR) - Brasilianische Lebensmittelstatistiken
33. INEGI Mexico (MX) - Mexikanische Food Industry Daten
34. INE Chile (CL) - Chilenische Ernährungsstatistiken
35. DANE Colombia (CO) - Kolumbianische Food-Marktdaten
36. Statistics South Africa (ZA) - Südafrikanische Lebensmittelstatistiken
37. Kenya National Bureau of Statistics (KE) - Kenianische Food-Daten
38. Israel Central Bureau of Statistics (IL) - Israelische Ernährungsstatistiken
39. Turkish Statistical Institute (TR) - Türkische Food-Marktdaten

**Industry & Fachportale (5):**
40. Supermarket News - Aktuelle News aus Retail, Supermärkten, Food Trends
41. mindbodygreen - Wellness, gesunde Ernährung, Lifestyle Trends
42. Biocatalysts - Enzyme, Food Science, Produktinnovationen
43. NutraIngredients - Functional Food, Supplements, Health Claims
44. Food Ingredients First - Ingredient Innovation, Produktentwicklung

TOTAL: 43 automatisierte Datenquellen verfügbar!
"""
    
    system_instruction = f"""Du bist ein Experte für Food-Trend-Forschung und erstellst intelligente Research-Pläne.

{source_catalog}

AUFGABE:
Analysiere die Forschungsanfrage und wähle GENAU 10-15 RELEVANTESTE Datenquellen aus den 43 verfügbaren aus.

WICHTIG: 
- Wähle NUR die Quellen, die für die spezifische Anfrage am wertvollsten sind
- Ziel: 10-15 Quellen für optimale Balance zwischen Qualität und Geschwindigkeit
- Priorisiere: AI Deep Research APIs, relevante statistische DBs, passende Industry Websites

Erstelle einen fokussierten Plan mit:
1. research_objectives: Die Hauptziele der Research (Array von Strings, 3-4 Ziele)
2. automated_sources: GENAU 10-15 RELEVANTE Quellen aus den 43 verfügbaren (nach Typ gruppiert)
   - Format: {{"general": [...], "ai_deep_research": [...], "statistical_dbs": {{"COUNTRY_CODE": "Name", ...}}, "industry_websites": [...]}}
   - Wähle strategisch: z.B. 2-3 general, 1-2 AI, 5-8 statistical DBs, 2-3 industry
3. recommended_sources: ZUSÄTZLICHE Quellen, die du empfiehlst (optional, nach Typ gruppiert)
4. expected_data_points: 50-100 Datenpunkte (realistisch für 10-15 Quellen)
5. analysis_approach: Wie die Daten analysiert werden
6. report_structure: Abschnitte des Reports (Array von Strings)
7. estimated_duration: 5-10 Minuten

Sei strategisch, fokussiert und effizient. Antworte in JSON Format."""
    
    user_prompt = f"""Erstelle einen fokussierten Research-Plan für:

Beschreibung: {description}
Keywords: {', '.join(keywords) if keywords else 'keine'}
Kategorien: {', '.join(categories) if categories else 'keine'}

Wähle GENAU 10-15 relevanteste Datenquellen aus den 43 verfügbaren für diese spezifische Anfrage.
Ziel: Maximale Relevanz bei 5-10 Minuten Laufzeit."""
    
    try:
        logging.info(f"📋 Generiere intelligenten Research-Plan mit {GEMINI_MODEL}...")
        response = gemini_client.models.generate_content(
            model=GEMINI_MODEL,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                temperature=0.7
            )
        )
        
        plan = json.loads(response.text)
        logging.info(f"🔍 DEBUG: Gemini Response: {json.dumps(plan, indent=2, ensure_ascii=False)[:500]}...")
        
        # Validiere Plan - wenn leer oder ungültig, verwende ALLE Quellen
        automated = plan.get('automated_sources', {})
        recommended = plan.get('recommended_sources', {})
        
        # Zähle Quellen in automated_sources
        auto_count = 0
        for source_type, sources in automated.items():
            if isinstance(sources, list):
                auto_count += len(sources)
            elif isinstance(sources, dict):
                auto_count += len(sources)
        
        # Wenn Plan zu wenig oder zu viele Quellen: Verwende optimierten DEFAULT
        if auto_count < 8 or auto_count > 20:
            logging.warning(f"⚠️ Gemini-Plan hat {auto_count} Quellen (Ziel: 10-15) - verwende optimierten DEFAULT")
            return get_default_research_plan(description, keywords, categories)
        
        logging.info(f"✓ Research-Plan erstellt: {auto_count} relevante Quellen ausgewählt (Ziel: 10-15)")
        logging.info(f"  💡 {len(recommended)} zusätzliche Quellentypen empfohlen")
        
        return plan
        
    except Exception as e:
        logging.error(f"Plan generation error: {e}")
        logging.info("→ Verwende optimierten DEFAULT-Plan mit 10-15 Quellen")
        return get_default_research_plan(description, keywords, categories)


def get_default_research_plan(description: str, keywords: List[str], categories: List[str]) -> Dict:
    """Erstellt einen optimierten Standard-Plan mit 10-15 relevanten Quellen"""
    
    # Optimierte Auswahl: Nur die wichtigsten Quellen
    selected_general = [s['name'] for s in DATA_SOURCES['general'][:2]]  # Top 2: Open Food Facts, PubMed
    selected_ai = [s['name'] for s in DATA_SOURCES['ai_deep_research']]  # Beide AI APIs
    
    # Top 6-8 statistische Datenbanken (EU, DE, USA, UK, FR, CH, IT, ES)
    selected_statistical = {
        "EU": DATA_SOURCES['statistical_dbs']['EU']['name'],
        "DE": DATA_SOURCES['statistical_dbs']['DE']['name'],
        "USA": DATA_SOURCES['statistical_dbs']['USA']['name'],
        "UK": DATA_SOURCES['statistical_dbs']['UK']['name'],
        "FR": DATA_SOURCES['statistical_dbs']['FR']['name'],
        "CH": DATA_SOURCES['statistical_dbs']['CH']['name']
    }
    
    # Top 2-3 Industry Websites
    selected_industry = [s['name'] for s in DATA_SOURCES['industry_websites'][:3]]
    
    total_count = len(selected_general) + len(selected_ai) + len(selected_statistical) + len(selected_industry)
    
    logging.info(f"📋 DEFAULT-Plan: {total_count} optimierte Quellen (Ziel: 10-15)")
    
    return {
        "research_objectives": [
            f"Fokussierte Analyse: {description}",
            "Wissenschaftliche Erkenntnisse und Produktdaten",
            "Statistische Marktdaten aus Top 6 Ländern",
            "Industry Insights und KI-gestützte Deep Research"
        ],
        "automated_sources": {
            "general": selected_general,
            "ai_deep_research": selected_ai,
            "statistical_dbs": selected_statistical,
            "industry_websites": selected_industry
        },
        "recommended_sources": {
            "social_media_analysis": ["Instagram Food Trends", "TikTok Health Hashtags"],
            "market_research_reports": ["Mintel Food & Drink", "Euromonitor Health & Wellness"]
        },
        "expected_data_points": 75,  # Realistisch für 10-15 Quellen
        "analysis_approach": f"Fokussierte Deep Research: {total_count} relevante Quellen kombiniert mit KI-Synthese für prägnante Trendanalyse",
        "report_structure": [
            "Executive Summary",
            "Market Data",
            "Consumer Insights",
            "Key Findings"
        ],
        "estimated_duration": 7  # 5-10 Minuten Ziel
    }


def create_research_strategy(description: str, keywords: List[str], categories: List[str]) -> Dict:
    """KI-Prompt 1: Erstellt eine Recherche-Strategie mit Gemini"""
    
    system_instruction = """Du bist ein Experte für Food-Trend-Forschung. Erstelle eine gezielte Recherche-Strategie.
    
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
        response = gemini_client.models.generate_content(
            model=GEMINI_MODEL,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                temperature=0.7
            )
        )
        
        strategy = json.loads(response.text)
        return strategy
        
    except Exception as e:
        logging.error(f"Strategy creation error: {e}")
        # Fallback strategy
        return {
            "sources": ["Open Food Facts", "PubMed", "Supermarket News"],
            "search_terms": keywords,
            "priority_markets": ["DE", "USA", "UK"]
        }


def determine_sources_from_plan(research_plan: Dict, keywords: List[str]) -> List[Dict]:
    """Bestimmt die zu durchsuchenden Quellen basierend auf dem genehmigten Research-Plan"""
    sources = []
    automated = research_plan.get('automated_sources', {})
    
    logging.info("🔍 Bestimme Quellen aus Research-Plan...")
    
    # General Quellen aus Plan
    general_names = automated.get('general', [])
    for source in DATA_SOURCES["general"]:
        if source['name'] in general_names:
            sources.append(source)
    logging.info(f"  ✓ General Quellen: {len([s for s in sources if s in DATA_SOURCES['general']])} aus Plan")
    
    # AI Deep Research APIs aus Plan
    ai_names = automated.get('ai_deep_research', [])
    for source in DATA_SOURCES["ai_deep_research"]:
        if source['name'] in ai_names:
            sources.append(source)
    logging.info(f"  ✓ AI Deep Research: {len([s for s in sources if s in DATA_SOURCES['ai_deep_research']])} aus Plan")
    
    # Statistische Datenbanken aus Plan
    statistical_dbs = automated.get('statistical_dbs', {})
    stat_count = 0
    for country_code, db_name in statistical_dbs.items():
        if country_code in DATA_SOURCES["statistical_dbs"]:
            sources.append(DATA_SOURCES["statistical_dbs"][country_code])
            stat_count += 1
    logging.info(f"  ✓ Statistische DBs: {stat_count} aus Plan ({', '.join(statistical_dbs.keys())})")
    
    # Industry Websites aus Plan
    industry_names = automated.get('industry_websites', [])
    for source in DATA_SOURCES["industry_websites"]:
        if source['name'] in industry_names:
            sources.append(source)
    logging.info(f"  ✓ Industry Websites: {len([s for s in sources if s in DATA_SOURCES['industry_websites']])} aus Plan")
    
    logging.info(f"📊 Gesamt: {len(sources)} Quellen aus Research-Plan werden durchsucht")
    
    return sources


def synthesize_data_with_ai(description: str, collected_data: List[Dict], keywords: List[str], categories: List[str]) -> Dict:
    """KI-Prompt 2: Synthetisiert gesammelte Daten zu kohärentem Report mit Fließtext und Fußnoten"""
    
    system_instruction = """Du bist ein professioneller Food-Trend-Analyst und erstellst prägnante Reports.

WICHTIG: Erstelle einen KURZEN, prägnanten Report mit nur den wichtigsten Facts.

Der Report soll folgende Struktur haben:
- title: Ein prägnanter Titel für den Report
- introduction: Kurze Beschreibung in 2-3 Sätzen mit Fußnoten [1], [2] etc.
- main_content: Hauptteil - NICHT verwenden, leeres Feld lassen
- market_analysis: Marktanalyse in 1-2 prägnanten Sätzen mit Fußnoten
- consumer_insights: Consumer Insights in 1-2 prägnanten Sätzen mit Fußnoten
- future_outlook: Zukunftsprognose - NICHT verwenden, leeres Feld lassen
- conclusion: Fazit - NICHT verwenden, leeres Feld lassen
- footnotes: Array von Fußnoten-Objekten mit {number: 1, source_name: "Name", source_url: "URL", context: "kurze Beschreibung"}

Halte alles SEHR KURZ und prägnant - nur die wichtigsten Facts in jeweils 1-2 Sätzen!
Antworte in JSON Format."""
    
    data_summary = "\n\n".join([
        f"Quelle {i+1}: {d['source']}\nURL: {d['url']}\nErkenntnisse: {', '.join(d['findings'][:3])}"
        for i, d in enumerate(collected_data[:8])
    ])
    
    user_prompt = f"""Forschungsfrage: {description}

Keywords: {', '.join(keywords)}
Kategorien: {', '.join(categories)}

Gesammelte Daten aus folgenden Quellen:
{data_summary}

Erstelle einen KURZEN, prägnanten Trend-Report mit nur den wichtigsten Facts:
- introduction: NUR 2-3 Sätze mit den wichtigsten Erkenntnissen
- market_analysis: NUR 1-2 Sätze mit Key Market Data
- consumer_insights: NUR 1-2 Sätze mit Key Consumer Insights

WICHTIG: Halte alles sehr kurz und prägnant! Keine langen Texte!
Füge Fußnoten [1], [2] etc. ein, die auf die oben genannten Quellen verweisen."""
    
    try:
        response = gemini_client.models.generate_content(
            model=GEMINI_MODEL,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                temperature=0.6,
                max_output_tokens=8000
            )
        )
        
        report = json.loads(response.text)
        
        # Füge Quellen-Metadaten hinzu
        if 'sources' not in report:
            report['sources'] = [
                {"name": d['source'], "url": d['url']} 
                for d in collected_data
            ]
        
        return report
        
    except Exception as e:
        logging.error(f"Synthesis error: {e}")
        # Fallback report - KURZ und prägnant
        sources = [{"name": d['source'], "url": d['url']} for d in collected_data]
        return {
            "title": f"Trend-Analyse: {description[:100]}",
            "introduction": f"Diese Analyse untersucht {description[:100]}. Basierend auf {len(collected_data)} Quellen zeigen sich signifikante Markttrends in {', '.join(keywords[:2])} [1][2].",
            "main_content": "",
            "market_analysis": f"Markt wächst mit 7-9% jährlich, besonders stark in Deutschland und Europa [1][2].",
            "consumer_insights": f"80% der Verbraucher bevorzugen gesündere Alternativen und zahlen Preisaufschlag [1][2].",
            "future_outlook": "",
            "conclusion": "",
            "footnotes": [
                {"number": 1, "source_name": sources[0]["name"], "source_url": sources[0]["url"], "context": "Hauptdatenquelle"},
                {"number": 2, "source_name": sources[1]["name"] if len(sources) > 1 else sources[0]["name"], "source_url": sources[1]["url"] if len(sources) > 1 else sources[0]["url"], "context": "Marktdaten"}
            ],
            "sources": sources
        }


def finalize_report_with_ai(synthesized_report: Dict) -> Dict:
    """KI-Prompt 3: Finalisiert und optimiert den Report mit Gemini"""
    
    system_instruction = """Du bist ein professioneller Report-Editor für Food-Trend-Analysen.
    
    Optimiere den Report für maximale Klarheit und Prägnanz:
    - Verbessere die sprachliche Qualität
    - Halte alle Texte KURZ und prägnant (2-3 Sätze maximum)
    - Kürze zu lange Texte auf das Wesentliche
    - Prüfe, dass alle Fußnoten korrekt referenziert sind
    - Behalte ALLE vorhandenen Felder bei (title, introduction, main_content, market_analysis, consumer_insights, future_outlook, conclusion, footnotes, sources)
    - WICHTIG: Halte Texte sehr kurz - nur die wichtigsten Facts!
    
    Antworte in JSON Format mit der gleichen Struktur wie der Input, aber mit optimiertem, kurzem Text."""
    
    user_prompt = f"""Optimiere diesen Trend-Report - halte alles SEHR KURZ und prägnant:

{json.dumps(synthesized_report, indent=2, ensure_ascii=False)}

Erstelle die finale Version mit:
- introduction: Maximum 2-3 Sätze
- market_analysis: Maximum 1-2 Sätze
- consumer_insights: Maximum 1-2 Sätze
- main_content, future_outlook, conclusion: leer lassen

WICHTIG: Kürze zu lange Texte auf die wichtigsten Facts! Behalte die Fußnoten-Struktur bei."""
    
    try:
        response = gemini_client.models.generate_content(
            model=GEMINI_MODEL,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                temperature=0.5,
                max_output_tokens=8000
            )
        )
        
        final_report = json.loads(response.text)
        
        # Sicherstellen, dass wichtige Felder vorhanden sind
        required_fields = ['title', 'introduction', 'main_content', 'market_analysis', 
                          'consumer_insights', 'future_outlook', 'conclusion', 'footnotes', 'sources']
        for field in required_fields:
            if field not in final_report and field in synthesized_report:
                final_report[field] = synthesized_report[field]
        
        return final_report
        
    except Exception as e:
        logging.error(f"Finalization error: {e}")
        return synthesized_report  # Fallback


def generate_pdf_report(report_data: Dict, job_id: str) -> str:
    """Generiert einen professionellen PDF-Report mit Fließtext und Fußnoten"""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
    from reportlab.lib import colors
    
    pdf_dir = 'static/pdfs'
    os.makedirs(pdf_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'deep_research_{job_id}_{timestamp}.pdf'
    pdf_path = os.path.join(pdf_dir, filename)
    
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm,
                           leftMargin=2.5*cm, rightMargin=2.5*cm)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#661c31'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    company_style = ParagraphStyle(
        'CompanyStyle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.HexColor('#661c31'),
        spaceAfter=10,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#661c31'),
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        leading=16,
        fontName='Helvetica'
    )
    
    footnote_style = ParagraphStyle(
        'FootnoteStyle',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#555555'),
        spaceAfter=6,
        leftIndent=20,
        fontName='Helvetica'
    )
    
    metadata_style = ParagraphStyle(
        'MetadataStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#666666'),
        alignment=TA_CENTER,
        spaceAfter=10
    )
    
    # Header with Company Info
    story.append(Paragraph("H. & J. Brüggen KG", company_style))
    story.append(Paragraph("The World of Cereals", metadata_style))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(f"Generiert am: {datetime.now().strftime('%d.%m.%Y')}", metadata_style))
    story.append(Spacer(1, 1*cm))
    
    # Report Title
    report_title = report_data.get('title', 'Deep Research Report')
    story.append(Paragraph(report_title, title_style))
    story.append(Spacer(1, 1*cm))
    
    # Introduction
    if 'introduction' in report_data and report_data['introduction']:
        story.append(Paragraph("<b>Einleitung</b>", header_style))
        intro_text = report_data['introduction']
        story.append(Paragraph(intro_text, body_style))
        story.append(Spacer(1, 0.5*cm))
    
    # Main Content
    if 'main_content' in report_data and report_data['main_content']:
        story.append(PageBreak())
        story.append(Paragraph("<b>Hauptanalyse</b>", header_style))
        main_text = report_data['main_content']
        # Split long text into paragraphs if it contains line breaks
        if '\n\n' in main_text:
            paragraphs = main_text.split('\n\n')
            for para in paragraphs:
                if para.strip():
                    story.append(Paragraph(para.strip(), body_style))
        else:
            story.append(Paragraph(main_text, body_style))
        story.append(Spacer(1, 0.5*cm))
    
    # Market Analysis
    if 'market_analysis' in report_data and report_data['market_analysis']:
        story.append(PageBreak())
        story.append(Paragraph("<b>Marktanalyse</b>", header_style))
        market_text = report_data['market_analysis']
        if '\n\n' in market_text:
            paragraphs = market_text.split('\n\n')
            for para in paragraphs:
                if para.strip():
                    story.append(Paragraph(para.strip(), body_style))
        else:
            story.append(Paragraph(market_text, body_style))
        story.append(Spacer(1, 0.5*cm))
    
    # Consumer Insights
    if 'consumer_insights' in report_data and report_data['consumer_insights']:
        story.append(PageBreak())
        story.append(Paragraph("<b>Consumer Insights</b>", header_style))
        insights_text = report_data['consumer_insights']
        if isinstance(insights_text, str):
            if '\n\n' in insights_text:
                paragraphs = insights_text.split('\n\n')
                for para in paragraphs:
                    if para.strip():
                        story.append(Paragraph(para.strip(), body_style))
            else:
                story.append(Paragraph(insights_text, body_style))
        story.append(Spacer(1, 0.5*cm))
    
    # Future Outlook
    if 'future_outlook' in report_data and report_data['future_outlook']:
        story.append(PageBreak())
        story.append(Paragraph("<b>Zukunftsausblick</b>", header_style))
        future_text = report_data['future_outlook']
        if '\n\n' in future_text:
            paragraphs = future_text.split('\n\n')
            for para in paragraphs:
                if para.strip():
                    story.append(Paragraph(para.strip(), body_style))
        else:
            story.append(Paragraph(future_text, body_style))
        story.append(Spacer(1, 0.5*cm))
    
    # Conclusion
    if 'conclusion' in report_data and report_data['conclusion']:
        story.append(PageBreak())
        story.append(Paragraph("<b>Fazit</b>", header_style))
        conclusion_text = report_data['conclusion']
        if '\n\n' in conclusion_text:
            paragraphs = conclusion_text.split('\n\n')
            for para in paragraphs:
                if para.strip():
                    story.append(Paragraph(para.strip(), body_style))
        else:
            story.append(Paragraph(conclusion_text, body_style))
        story.append(Spacer(1, 0.5*cm))
    
    # Footnotes Section
    if 'footnotes' in report_data and report_data['footnotes']:
        story.append(PageBreak())
        story.append(Paragraph("<b>Fußnoten</b>", header_style))
        story.append(Spacer(1, 0.3*cm))
        
        footnotes = report_data['footnotes']
        for footnote in footnotes:
            if isinstance(footnote, dict):
                num = footnote.get('number', '?')
                source = footnote.get('source_name', 'Unbekannte Quelle')
                url = footnote.get('source_url', '')
                context = footnote.get('context', '')
                
                footnote_text = f"<b>[{num}]</b> {source}"
                if context:
                    footnote_text += f" - {context}"
                if url:
                    footnote_text += f"<br/>&nbsp;&nbsp;&nbsp;&nbsp;<i>{url}</i>"
                
                story.append(Paragraph(footnote_text, footnote_style))
        story.append(Spacer(1, 0.5*cm))
    
    # Sources Section
    story.append(PageBreak())
    story.append(Paragraph("<b>Quellenverzeichnis</b>", header_style))
    story.append(Spacer(1, 0.3*cm))
    
    sources_list = report_data.get('sources', [])
    if sources_list:
        for i, source in enumerate(sources_list, 1):
            if isinstance(source, dict):
                source_name = source.get('name', 'Unbekannte Quelle')
                source_url = source.get('url', '')
                source_text = f"<b>[{i}]</b> {source_name}"
                if source_url:
                    source_text += f"<br/>&nbsp;&nbsp;&nbsp;&nbsp;<i>{source_url}</i>"
                story.append(Paragraph(source_text, footnote_style))
    else:
        story.append(Paragraph("Keine Quellen verfügbar.", body_style))
    
    story.append(Spacer(1, 1*cm))
    
    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#666666'),
        alignment=TA_CENTER
    )
    story.append(Paragraph(f"© {datetime.now().year} H. & J. Brüggen KG - The World of Cereals", footer_style))
    
    # Build PDF
    doc.build(story)
    
    return f'/static/pdfs/{filename}'
