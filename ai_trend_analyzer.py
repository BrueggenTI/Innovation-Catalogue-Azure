import json
import os
from openai import OpenAI

# the newest OpenAI model is "gpt-5" which was released August 7, 2025.
# do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai = OpenAI(api_key=OPENAI_API_KEY)

def analyze_document_for_trend(text_content):
    """
    Analyze document content and extract trend information using OpenAI
    Returns structured JSON with trend suggestions
    """
    try:
        prompt = """
        Analyze the following document content and extract information for a food industry trend report.
        
        Please provide a JSON response with the following structure:
        {
            "title": "suggested title for the trend (max 100 characters)",
            "description": "detailed description of the trend (max 300 characters)", 
            "category": "one of: Health, Sustainability, Innovation",
            "report_type": "one of: produktentwicklung, marktdaten",
            "market_data": "one concise fact about market data, statistics, growth rates, market size, or financial information (max 150 characters)",
            "consumer_insights": "one concise fact about consumer behavior, preferences, trends, or demographic insights (max 150 characters)",
            "confidence": "confidence score from 0.0 to 1.0"
        }
        
        Generate two specific key facts:
        1. Market Data: Focus on statistics, growth rates, market size, revenue data, or financial metrics
        2. Consumer Insights: Focus on consumer behavior, preferences, demographic trends, or purchasing patterns
        
        Focus on:
        - Food industry trends and innovations
        - Health and wellness aspects
        - Sustainability factors
        - Market developments
        - Product development insights
        
        Document content:
        """ + text_content
        
        response = openai.chat.completions.create(
            model="gpt-5",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert food industry analyst specializing in trend identification and market insights. Analyze documents and extract relevant trend information for the food industry."
                },
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        if content is None:
            raise Exception("No content received from OpenAI")
        result = json.loads(content)
        return result
        
    except Exception as e:
        raise Exception(f"Failed to analyze document: {e}")

def improve_trend_description(title, description, category):
    """
    Use AI to improve and enhance trend descriptions
    """
    try:
        prompt = f"""
        Improve the following food trend description to make it more engaging and informative:
        
        Title: {title}
        Current Description: {description}
        Category: {category}
        
        Please provide an improved description that:
        - Is concise but informative (max 300 characters)
        - Uses industry-appropriate language
        - Highlights key benefits or innovations
        - Is engaging for food industry professionals
        
        Return only the improved description text, no additional formatting.
        """
        
        response = openai.chat.completions.create(
            model="gpt-5",
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = response.choices[0].message.content
        if content is None:
            return description  # Fallback to original description
        return content.strip()
        
    except Exception as e:
        return description  # Fallback to original description

def extract_key_topics(text_content):
    """
    Extract key topics and keywords from document content
    """
    try:
        prompt = f"""
        Extract the main topics and keywords from this food industry document.
        
        Return a JSON object with:
        {{
            "main_topics": ["list of 5-8 main topics"],
            "keywords": ["list of 10-15 relevant keywords"],
            "industry_segments": ["list of relevant food industry segments mentioned"]
        }}
        
        Document content:
        {text_content[:2000]}...
        """
        
        response = openai.chat.completions.create(
            model="gpt-5",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        if content is None:
            return {"main_topics": [], "keywords": [], "industry_segments": []}
        return json.loads(content)
        
    except Exception as e:
        return {
            "main_topics": [],
            "keywords": [],
            "industry_segments": []
        }