from app import db
from models import Product
import json

def init_products():
    """Initialize products with sample data"""

    # Clear existing products first
    Product.query.delete()

    products_data = [
        {
            "name": "Traditional Swiss Muesli",
            "category": "Traditional Muesli",
            "description": "A classic blend of rolled oats, nuts, and dried fruits, inspired by traditional Swiss recipes. Perfect balance of taste and nutrition for health-conscious consumers.",
            "ingredients": json.dumps([
                {"name": "Rolled oats", "percentage": 45},
                {"name": "Hazelnuts", "percentage": 15},
                {"name": "Almonds", "percentage": 10},
                {"name": "Raisins", "percentage": 15},
                {"name": "Dried apples", "percentage": 10},
                {"name": "Sunflower seeds", "percentage": 5}
            ]),
            "nutritional_claims": json.dumps([
                "High in fiber",
                "Source of protein",
                "Rich in magnesium",
                "No added sugar"
            ]),
            "allergens": json.dumps([
                "Contains nuts (hazelnuts, almonds)",
                "May contain traces of other nuts",
                "Contains gluten"
            ]),
            "certifications": json.dumps([
                "Non-GMO verified",
                "Rainforest Alliance certified nuts"
            ]),
            "nutritional_info": json.dumps({
                "energy": 390,
                "fat": 12.5,
                "saturated_fat": 2.1,
                "carbohydrates": 58.2,
                "sugars": 18.5,
                "fiber": 8.7,
                "protein": 11.3,
                "salt": 0.02
            }),
            "claims": json.dumps([
                "Authentic Swiss recipe",
                "Perfect breakfast balance",
                "Natural energy boost",
                "Traditional taste"
            ]),
            "image_url": "/static/images/recipes/product_1753113378_Bild1.png"
        },
        {
            "name": "Protein Power Granola",
            "category": "Crunchy Muesli",
            "description": "High-protein crunchy granola with roasted nuts and seeds. Ideal for active lifestyles and post-workout nutrition.",
            "ingredients": json.dumps([
                {"name": "Oat flakes", "percentage": 35},
                {"name": "Protein flakes (soy)", "percentage": 20},
                {"name": "Almonds", "percentage": 15},
                {"name": "Pumpkin seeds", "percentage": 10},
                {"name": "Honey", "percentage": 10},
                {"name": "Coconut oil", "percentage": 5},
                {"name": "Cinnamon", "percentage": 5}
            ]),
            "nutritional_claims": json.dumps([
                "High in protein (>20g per 100g)",
                "Source of fiber",
                "Rich in healthy fats",
                "Natural sweeteners only"
            ]),
            "allergens": json.dumps([
                "Contains soy",
                "Contains nuts (almonds)",
                "May contain traces of other allergens",
                "Contains gluten"
            ]),
            "certifications": json.dumps([
                "Organic certified",
                "Non-GMO verified"
            ]),
            "nutritional_info": json.dumps({
                "energy": 445,
                "fat": 18.7,
                "saturated_fat": 4.2,
                "carbohydrates": 52.3,
                "sugars": 12.8,
                "fiber": 7.5,
                "protein": 22.1,
                "salt": 0.05
            }),
            "claims": json.dumps([
                "Perfect for active lifestyles",
                "Post-workout nutrition",
                "Sustained energy release",
                "Premium protein source"
            ]),
            "image_url": "/static/images/recipes/product_1753113814_Bild3.png"
        },
        {
            "name": "Ancient Grains Mix",
            "category": "Multigrain & Branflakes",
            "description": "A nutritious blend of ancient grains including quinoa, amaranth, and spelt. Tapping into the ancient grains trend.",
            "ingredients": json.dumps([
                {"name": "Quinoa flakes", "percentage": 25},
                {"name": "Amaranth pops", "percentage": 20},
                {"name": "Spelt flakes", "percentage": 20},
                {"name": "Buckwheat", "percentage": 15},
                {"name": "Chia seeds", "percentage": 10},
                {"name": "Dried goji berries", "percentage": 10}
            ]),
            "nutritional_claims": json.dumps([
                "Complete protein source",
                "High in fiber",
                "Rich in antioxidants",
                "Gluten-free options available"
            ]),
            "allergens": json.dumps([
                "May contain traces of nuts",
                "Spelt contains gluten"
            ]),
            "certifications": json.dumps([
                "Organic certified",
                "Fair Trade certified",
                "Non-GMO verified"
            ]),
            "nutritional_info": json.dumps({
                "energy": 365,
                "fat": 6.2,
                "saturated_fat": 1.1,
                "carbohydrates": 62.5,
                "sugars": 8.3,
                "fiber": 11.2,
                "protein": 14.8,
                "salt": 0.01
            }),
            "claims": json.dumps([
                "Ancient superfood blend",
                "Nutrient-dense formula",
                "Naturally wholesome",
                "Complete amino acids"
            ]),
            "image_url": "/static/images/recipes/product_1753114029_Bild1.png"
        },
        {
            "name": "Kids Choco Crunch",
            "category": "Puffed Cereals",
            "description": "Fun and nutritious chocolate-flavored cereal designed for children. Fortified with essential vitamins and minerals.",
            "ingredients": json.dumps([
                {"name": "Whole grain wheat", "percentage": 40},
                {"name": "Rice flour", "percentage": 25},
                {"name": "Cocoa powder", "percentage": 15},
                {"name": "Sugar", "percentage": 10},
                {"name": "Vitamin mix", "percentage": 5},
                {"name": "Salt", "percentage": 5}
            ]),
            "nutritional_claims": json.dumps([
                "Fortified with vitamins",
                "Source of iron",
                "Whole grain",
                "Fun shapes for kids"
            ]),
            "allergens": json.dumps([
                "Contains gluten",
                "May contain traces of milk",
                "May contain traces of nuts"
            ]),
            "certifications": json.dumps([
                "EU organic certification",
                "Child-friendly approved"
            ]),
            "nutritional_info": json.dumps({
                "energy": 380,
                "fat": 4.2,
                "saturated_fat": 1.8,
                "carbohydrates": 76.5,
                "sugars": 22.1,
                "fiber": 3.2,
                "protein": 8.9,
                "salt": 0.35
            }),
            "claims": json.dumps([
                "Kids love the taste",
                "Fun breakfast time",
                "Essential vitamins added",
                "Perfect for growing minds"
            ]),
            "image_url": "/static/images/recipes/product_1753114220_Bild1.jpg"
        },
        {
            "name": "Gluten-Free Oat Porridge",
            "category": "Oat Flakes",
            "description": "Creamy gluten-free oat porridge perfect for a warming breakfast. Made from certified gluten-free oats.",
            "ingredients": json.dumps([
                {"name": "Gluten-free oats", "percentage": 85},
                {"name": "Rice flour", "percentage": 10},
                {"name": "Salt", "percentage": 3},
                {"name": "Natural vanilla", "percentage": 2}
            ]),
            "nutritional_claims": json.dumps([
                "Gluten-free certified",
                "High in beta-glucan",
                "Source of fiber",
                "Heart-healthy"
            ]),
            "allergens": json.dumps([
                "Gluten-free",
                "May contain traces of nuts"
            ]),
            "certifications": json.dumps([
                "Gluten-free certified",
                "Organic certified"
            ]),
            "nutritional_info": json.dumps({
                "energy": 350,
                "fat": 6.8,
                "saturated_fat": 1.2,
                "carbohydrates": 62.1,
                "sugars": 1.8,
                "fiber": 10.5,
                "protein": 13.2,
                "salt": 0.02
            }),
            "claims": json.dumps([
                "Gluten-free certified",
                "Warming comfort food",
                "Heart-healthy choice",
                "Creamy texture"
            ]),
            "image_url": "/static/images/recipes/product_1753114310_Bild3.jpg"
        },
        {
            "name": "Cornflakes Classic",
            "category": "Flakes",
            "description": "Crispy golden cornflakes made from the finest corn. A timeless breakfast classic loved by families worldwide.",
            "ingredients": json.dumps([
                {"name": "Corn grits", "percentage": 85},
                {"name": "Sugar", "percentage": 8},
                {"name": "Salt", "percentage": 4},
                {"name": "Malt extract", "percentage": 3}
            ]),
            "nutritional_claims": json.dumps([
                "Fortified with vitamins and minerals",
                "Source of B vitamins",
                "Low in fat",
                "Crispy texture"
            ]),
            "allergens": json.dumps([
                "Gluten-free",
                "May contain traces of nuts"
            ]),
            "certifications": json.dumps([
                "Non-GMO corn",
                "Quality certified"
            ]),
            "nutritional_info": json.dumps({
                "energy": 375,
                "fat": 0.9,
                "saturated_fat": 0.2,
                "carbohydrates": 84.2,
                "sugars": 8.5,
                "fiber": 3.1,
                "protein": 7.8,
                "salt": 1.25
            }),
            "claims": json.dumps([
                "Classic breakfast choice",
                "Crispy golden texture",
                "Family favorite",
                "Quick energy source"
            ]),
            "image_url": "/static/images/recipes/product_1753114575_Bild5.png"
        },
        {
            "name": "Organic Fair-Trade Muesli",
            "category": "Bio & Fair-Trade muesli",
            "description": "Premium organic muesli with fair-trade ingredients. Supporting sustainable farming and ethical trade practices.",
            "ingredients": json.dumps([
                {"name": "Organic oat flakes", "percentage": 40},
                {"name": "Fair-trade raisins", "percentage": 20},
                {"name": "Fair-trade almonds", "percentage": 15},
                {"name": "Organic dried bananas", "percentage": 10},
                {"name": "Fair-trade coconut flakes", "percentage": 10},
                {"name": "Organic sunflower seeds", "percentage": 5}
            ]),
            "nutritional_claims": json.dumps([
                "100% organic",
                "Fair-trade certified",
                "High in fiber",
                "Natural ingredients only"
            ]),
            "allergens": json.dumps([
                "Contains nuts (almonds)",
                "May contain traces of other nuts",
                "Contains gluten"
            ]),
            "certifications": json.dumps([
                "EU Organic certification",
                "Fair Trade certified",
                "Rainforest Alliance"
            ]),
            "nutritional_info": json.dumps({
                "energy": 405,
                "fat": 14.8,
                "saturated_fat": 3.2,
                "carbohydrates": 55.7,
                "sugars": 16.2,
                "fiber": 9.1,
                "protein": 12.5,
                "salt": 0.01
            }),
            "claims": json.dumps([
                "Ethically sourced ingredients",
                "Supporting farming communities",
                "Premium organic quality",
                "Sustainable choice"
            ]),
            "image_url": "/static/images/recipes/product_1753171328_Bild1.png"
        },
        {
            "name": "Wheat Breakfast Flakes",
            "category": "Wheat, Rye & Barley Flakes",
            "description": "Nutritious wheat flakes with a hearty texture. Rich in fiber and perfect for a substantial breakfast.",
            "ingredients": json.dumps([
                {"name": "Whole wheat flakes", "percentage": 90},
                {"name": "Sugar", "percentage": 5},
                {"name": "Salt", "percentage": 3},
                {"name": "Vitamin mix", "percentage": 2}
            ]),
            "nutritional_claims": json.dumps([
                "Whole grain",
                "High in fiber",
                "Source of B vitamins",
                "Fortified with iron"
            ]),
            "allergens": json.dumps([
                "Contains gluten (wheat)",
                "May contain traces of nuts"
            ]),
            "certifications": json.dumps([
                "Whole grain certified",
                "Quality assured"
            ]),
            "nutritional_info": json.dumps({
                "energy": 348,
                "fat": 2.1,
                "saturated_fat": 0.4,
                "carbohydrates": 69.8,
                "sugars": 5.2,
                "fiber": 12.4,
                "protein": 11.7,
                "salt": 0.08
            }),
            "claims": json.dumps([
                "Hearty whole grain goodness",
                "Substantial breakfast",
                "Long-lasting satisfaction",
                "Traditional nutrition"
            ]),
            "image_url": "/static/images/recipes/product_1753171545_Bild3.jpg"
        },
        {
            "name": "Protein Energy Bars",
            "category": "Bars",
            "description": "High-protein energy bars with nuts and seeds. Perfect for on-the-go nutrition and post-workout recovery.",
            "ingredients": json.dumps([
                {"name": "Protein powder (whey)", "percentage": 30},
                {"name": "Oats", "percentage": 25},
                {"name": "Almonds", "percentage": 15},
                {"name": "Dates", "percentage": 15},
                {"name": "Honey", "percentage": 10},
                {"name": "Chia seeds", "percentage": 5}
            ]),
            "nutritional_claims": json.dumps([
                "High in protein (>20g per bar)",
                "Natural energy source",
                "No artificial additives",
                "Convenient format"
            ]),
            "allergens": json.dumps([
                "Contains milk (whey)",
                "Contains nuts (almonds)",
                "May contain traces of other allergens"
            ]),
            "certifications": json.dumps([
                "Sports nutrition approved",
                "Non-GMO verified"
            ]),
            "nutritional_info": json.dumps({
                "energy": 420,
                "fat": 16.8,
                "saturated_fat": 3.2,
                "carbohydrates": 32.5,
                "sugars": 18.7,
                "fiber": 6.8,
                "protein": 25.3,
                "salt": 0.12
            }),
            "claims": json.dumps([
                "On-the-go convenience",
                "Athletic performance fuel",
                "Recovery nutrition",
                "Portable energy solution"
            ]),
            "image_url": "/static/images/recipes/product_1753171862_Bild2.jpg"
        },
        {
            "name": "Honey Crunch Extrudates",
            "category": "Extrudates & Co-Extrudates",
            "description": "Crunchy honey-flavored extruded cereals with a satisfying texture. Perfect for mixing into mueslis or enjoying alone.",
            "ingredients": json.dumps([
                {"name": "Corn meal", "percentage": 50},
                {"name": "Wheat flour", "percentage": 25},
                {"name": "Honey", "percentage": 15},
                {"name": "Sugar", "percentage": 8},
                {"name": "Salt", "percentage": 2}
            ]),
            "nutritional_claims": json.dumps([
                "Natural honey flavor",
                "Crunchy texture",
                "Source of energy",
                "Versatile ingredient"
            ]),
            "allergens": json.dumps([
                "Contains gluten (wheat)",
                "May contain traces of nuts"
            ]),
            "certifications": json.dumps([
                "Quality certified",
                "Natural honey used"
            ]),
            "nutritional_info": json.dumps({
                "energy": 395,
                "fat": 1.8,
                "saturated_fat": 0.3,
                "carbohydrates": 85.2,
                "sugars": 15.5,
                "fiber": 2.8,
                "protein": 6.5,
                "salt": 0.42
            }),
            "claims": json.dumps([
                "Natural honey sweetness",
                "Perfect texture crunch",
                "Versatile mix-in ingredient",
                "Golden breakfast delight"
            ]),
            "image_url": "/static/images/recipes/product_1753172346_Bild2.jpg"
        }
    ]

    for product_data in products_data:
        # Check if product already exists
        existing = Product.query.filter_by(name=product_data['name']).first()
        if not existing:
            product = Product(**product_data)
            db.session.add(product)

    db.session.commit()
    print(f"Initialized {len(products_data)} products")