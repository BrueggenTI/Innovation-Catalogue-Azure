from app import db
from models import Trend

def init_trends():
    """Initialize the database with trend data"""
    
    trends_data = [
        {
            'title': 'Functional Proteins & Adaptogens',
            'category': 'health',
            'report_type': 'produktentwicklung',
            'description': 'Consumers increasingly seek breakfast products that deliver functional benefits beyond basic nutrition. Plant-based proteins, collagen peptides, and adaptogenic herbs like ashwagandha and reishi are driving innovation.',
            'market_data': '73% of consumers actively seek protein-enriched breakfast products. The functional food market is expected to reach €279 billion by 2025.',
            'consumer_insights': 'Millennials and Gen-Z prioritize products that support mental clarity, stress management, and sustained energy throughout the day.',
            'image_url': 'https://images.unsplash.com/photo-1559954860-057f4c0cbfb1?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Probiotic Integration',
            'category': 'health',
            'report_type': 'produktentwicklung',
            'description': 'The gut-brain connection drives demand for breakfast cereals and bars with live probiotics. Stable, shelf-stable probiotic strains are enabling new product formats.',
            'market_data': 'Probiotic food market growing at 7.8% CAGR. 67% of consumers understand the link between gut health and overall wellness.',
            'consumer_insights': 'Parents especially seek probiotic options for children\'s breakfast, viewing it as preventive healthcare.',
            'image_url': 'https://images.unsplash.com/photo-1571115764595-644a1f56a55c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Zero-Waste Ingredient Innovation',
            'category': 'sustainability',
            'report_type': 'produktentwicklung',
            'description': 'Upcycled ingredients from food production waste are becoming premium components. Fruit pomace, spent grains, and vegetable pulps offer unique nutritional profiles.',
            'market_data': 'Upcycled food market projected to reach $46.7 billion by 2024. 60% of consumers willing to pay premium for upcycled products.',
            'consumer_insights': 'Sustainability-conscious consumers view upcycled ingredients as innovative rather than inferior, especially when benefits are clearly communicated.',
            'image_url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Regenerative Agriculture Sourcing',
            'category': 'sustainability',
            'report_type': 'produktentwicklung',
            'description': 'Beyond organic: ingredients sourced from farms that actively restore soil health and biodiversity. Carbon-negative cereals and climate-positive oats.',
            'market_data': 'Regenerative agriculture market growing 14.2% annually. Major retailers committing to regenerative sourcing by 2030.',
            'consumer_insights': 'Consumers increasingly understand that food choices impact climate change, driving preference for regenerative products.',
            'image_url': 'https://images.unsplash.com/photo-1500937386664-56d1dfef3854?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Ultra-Crunchy Texture Innovation',
            'category': 'innovation',
            'report_type': 'produktentwicklung',
            'description': 'New extrusion and puffing technologies create unprecedented texture experiences. Air-puffed ancient grains and freeze-shattered fruits deliver unique mouthfeel.',
            'market_data': 'Texture is the #1 factor in breakfast cereal satisfaction. 45% of consumers actively seek new texture experiences.',
            'consumer_insights': 'Social media drives demand for products with distinctive, shareable texture experiences that photograph well.',
            'image_url': 'https://images.unsplash.com/photo-1558961363-fa8fdf82db35?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Global Fusion Flavors',
            'category': 'innovation',
            'report_type': 'produktentwicklung',
            'description': 'Breakfast products incorporating international flavors: matcha from Japan, turmeric-ginger from India, baobab from Africa, and acai from Brazil.',
            'market_data': 'Ethnic food market growing 11.8% annually. 78% of millennials eager to try international flavors at breakfast.',
            'consumer_insights': 'Travel restrictions increased desire for global experiences through food. Breakfast seen as low-risk way to explore new flavors.',
            'image_url': 'https://images.unsplash.com/photo-1505576391880-b3f9d713dc4f?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        }
    ]
    
    for trend_data in trends_data:
        # Check if trend already exists
        existing = Trend.query.filter_by(title=trend_data['title']).first()
        if not existing:
            trend = Trend(**trend_data)
            db.session.add(trend)
    
    db.session.commit()
    print(f"Initialized {len(trends_data)} trends")
