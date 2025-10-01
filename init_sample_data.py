#!/usr/bin/env python3
"""
Initialize sample data for the Brüggen Innovation Catalogue
"""

import json
from app import app, db
from models import Product, Trend

def init_sample_data():
    """Initialize sample data for testing"""
    
    with app.app_context():
        # Clear existing data
        Product.query.delete()
        Trend.query.delete()
        
        # Sample products
        products = [
            {
                "name": "Premium Swiss Muesli",
                "category": "Traditional Swiss Muesli",
                "description": "Classic blend of rolled oats, nuts, and dried fruits following authentic Swiss recipe traditions",
                "ingredients": json.dumps([
                    {"name": "Rolled Oats", "percentage": 45.0},
                    {"name": "Hazelnuts", "percentage": 15.0},
                    {"name": "Almonds", "percentage": 12.0},
                    {"name": "Dried Apricots", "percentage": 10.0},
                    {"name": "Raisins", "percentage": 12.0},
                    {"name": "Sunflower Seeds", "percentage": 6.0}
                ]),
                "nutritional_claims": json.dumps(["High Fiber", "Source of Protein", "No Added Sugar"]),
                "certifications": json.dumps(["Organic", "Non-GMO"]),
                "nutritional_info": json.dumps({
                    "energy": "375 kcal",
                    "fat": "12.5g",
                    "saturated_fat": "2.1g",
                    "carbohydrates": "58.2g",
                    "sugars": "18.3g",
                    "fiber": "8.7g",
                    "protein": "12.1g",
                    "salt": "0.02g"
                }),
                "allergens": json.dumps(["Nuts (Hazelnuts, Almonds)", "May contain traces of gluten"]),
                "claims": json.dumps(["Rich in Fiber", "Source of Protein", "No Added Sugar", "Organic"]),
                "image_url": "https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
                "case_study": "Successfully launched in 15 European markets with 23% market share increase",
                "production_tech": "Cold-rolled oats, gentle mixing process, quality-controlled packaging"
            },
            {
                "name": "Protein Power Clusters",
                "category": "Premium Oat Clusters",
                "description": "Crunchy oat clusters enhanced with plant-based protein for active lifestyle consumers",
                "ingredients": json.dumps([
                    {"name": "Oat Clusters", "percentage": 42.0},
                    {"name": "Pea Protein", "percentage": 20.0},
                    {"name": "Chia Seeds", "percentage": 15.0},
                    {"name": "Coconut Oil", "percentage": 8.0},
                    {"name": "Maple Syrup", "percentage": 10.0},
                    {"name": "Natural Vanilla", "percentage": 5.0}
                ]),
                "nutritional_claims": json.dumps(["High Protein", "High Fiber", "Vegan", "Gluten-Free"]),
                "certifications": json.dumps(["Organic", "Vegan Certified"]),
                "nutritional_info": json.dumps({
                    "energy": "425 kcal",
                    "fat": "16.8g",
                    "saturated_fat": "8.2g",
                    "carbohydrates": "35.4g",
                    "sugars": "12.1g",
                    "fiber": "12.3g",
                    "protein": "28.5g",
                    "salt": "0.15g"
                }),
                "allergens": json.dumps(["May contain traces of nuts", "May contain traces of soy"]),
                "claims": json.dumps(["High Protein", "Vegan", "Gluten-Free", "Source of Omega-3"]),
                "image_url": "https://images.unsplash.com/photo-1517686469429-8bdb88b9f907?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
                "case_study": "Developed for leading fitness chain with 40% repeat purchase rate",
                "production_tech": "Cluster formation technology, protein enrichment, controlled baking process"
            },
            {
                "name": "Antioxidant Berry Crunch",
                "category": "Baked Muesli Crunchy",
                "description": "Baked muesli with superfruit blend delivering high antioxidant content",
                "ingredients": json.dumps([
                    {"name": "Baked Oats", "percentage": 50.0},
                    {"name": "Goji Berries", "percentage": 12.0},
                    {"name": "Blueberries", "percentage": 15.0},
                    {"name": "Acai Powder", "percentage": 3.0},
                    {"name": "Quinoa Puffs", "percentage": 12.0},
                    {"name": "Honey", "percentage": 8.0}
                ]),
                "nutritional_claims": json.dumps(["High Antioxidants", "Source of Fiber", "Natural Ingredients"]),
                "certifications": json.dumps(["Organic", "Superfood Certified"]),
                "nutritional_info": json.dumps({
                    "energy": "385 kcal",
                    "fat": "8.9g",
                    "saturated_fat": "1.8g",
                    "carbohydrates": "67.2g",
                    "sugars": "22.5g",
                    "fiber": "9.8g",
                    "protein": "8.7g",
                    "salt": "0.08g"
                }),
                "allergens": json.dumps(["May contain traces of nuts", "May contain traces of gluten"]),
                "claims": json.dumps(["Rich in Antioxidants", "Natural Superfruit Blend", "Source of Fiber", "Organic"]),
                "image_url": "https://images.unsplash.com/photo-1593560708920-61dd98c46a4e?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
                "case_study": "Premium positioning in health food stores with 35% margin improvement",
                "production_tech": "Gentle baking, freeze-dried berries, antioxidant preservation"
            },
            {
                "name": "On-the-Go Energy Bars",
                "category": "Cereal & Fruit Snack Bars",
                "description": "Convenient snack bars combining cereals and fruits for busy professionals",
                "ingredients": json.dumps([
                    {"name": "Oat Flakes", "percentage": 35.0},
                    {"name": "Dates", "percentage": 25.0},
                    {"name": "Almonds", "percentage": 18.0},
                    {"name": "Dark Chocolate", "percentage": 12.0},
                    {"name": "Coconut", "percentage": 10.0}
                ]),
                "nutritional_claims": json.dumps(["Natural Energy", "No Artificial Additives", "Sustained Release"]),
                "certifications": json.dumps(["Organic", "Fair Trade"]),
                "nutritional_info": json.dumps({
                    "energy": "445 kcal",
                    "fat": "18.7g",
                    "saturated_fat": "6.2g",
                    "carbohydrates": "58.9g",
                    "sugars": "35.2g",
                    "fiber": "7.4g",
                    "protein": "11.8g",
                    "salt": "0.12g"
                }),
                "allergens": json.dumps(["Nuts (Almonds)", "May contain traces of other nuts", "May contain traces of gluten"]),
                "claims": json.dumps(["Natural Energy Source", "No Artificial Preservatives", "Fair Trade", "Organic"]),
                "image_url": "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
                "case_study": "Launched in convenience stores with 50% sales growth in 6 months",
                "production_tech": "Cold-press technology, natural binding, extended shelf life"
            },
            {
                "name": "Ancient Grains Blend",
                "category": "Premium Oat Clusters",
                "description": "Unique blend of ancient grains and modern superfoods for health-conscious consumers",
                "ingredients": json.dumps([
                    {"name": "Quinoa", "percentage": 25.0},
                    {"name": "Amaranth", "percentage": 20.0},
                    {"name": "Buckwheat", "percentage": 22.0},
                    {"name": "Chia Seeds", "percentage": 18.0},
                    {"name": "Hemp Hearts", "percentage": 15.0}
                ]),
                "nutritional_claims": json.dumps(["Complete Protein", "High Fiber", "Gluten-Free", "Omega-3"]),
                "certifications": json.dumps(["Organic", "Ancient Grains Certified"]),
                "nutritional_info": json.dumps({
                    "energy": "395 kcal",
                    "fat": "14.2g",
                    "saturated_fat": "2.1g",
                    "carbohydrates": "52.8g",
                    "sugars": "3.2g",
                    "fiber": "11.5g",
                    "protein": "16.8g",
                    "salt": "0.05g"
                }),
                "allergens": json.dumps(["Gluten-Free", "May contain traces of nuts"]),
                "claims": json.dumps(["Complete Protein", "Ancient Grains", "Gluten-Free", "Rich in Omega-3"]),
                "image_url": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
                "case_study": "Premium retail positioning with 28% higher margins than category average",
                "production_tech": "Multi-grain processing, nutrient preservation, quality assurance"
            }
        ]
        
        # Sample trends
        trends = [
            {
                "title": "Plant-Based Protein Revolution",
                "category": "health",
                "description": "Growing consumer demand for plant-based protein sources in breakfast cereals",
                "consumer_insights": json.dumps([
                    "87% of consumers actively seeking plant protein options",
                    "Pea protein preferred over soy by 3:1 ratio",
                    "Premium pricing accepted for quality plant proteins"
                ]),
                "image_url": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
                "market_data": json.dumps({
                    "growth_rate": "35%",
                    "market_size": "€2.8B",
                    "key_demographics": "25-45 health-conscious consumers"
                })
            },
            {
                "title": "Sustainable Packaging Innovation",
                "category": "sustainability",
                "description": "Shift towards eco-friendly packaging solutions in food industry",
                "consumer_insights": json.dumps([
                    "73% willing to pay more for sustainable packaging",
                    "Recyclable materials becoming standard requirement",
                    "Carbon footprint reduction drives innovation"
                ]),
                "image_url": "https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
                "market_data": json.dumps({
                    "growth_rate": "22%",
                    "market_size": "€15.2B",
                    "key_demographics": "Environmentally conscious consumers"
                })
            },
            {
                "title": "Functional Breakfast Foods",
                "category": "innovation",
                "description": "Integration of functional ingredients for health benefits beyond nutrition",
                "consumer_insights": json.dumps([
                    "Probiotics in breakfast foods growing 45% annually",
                    "Adaptogenic ingredients entering mainstream",
                    "Personalized nutrition driving innovation"
                ]),
                "image_url": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
                "market_data": json.dumps({
                    "growth_rate": "28%",
                    "market_size": "€8.7B",
                    "key_demographics": "Health-focused millennials and Gen Z"
                })
            }
        ]
        
        # Add products to database
        for product_data in products:
            product = Product(**product_data)
            db.session.add(product)
        
        # Add trends to database
        for trend_data in trends:
            trend = Trend(**trend_data)
            db.session.add(trend)
        
        # Commit changes
        db.session.commit()
        print("Sample data initialized successfully!")

if __name__ == "__main__":
    init_sample_data()