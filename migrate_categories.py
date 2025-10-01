
import json
from app import app, db
from models import Product

def migrate_categories():
    """Migrate existing product categories to new classification system"""
    
    # Category mapping from old to new
    category_mapping = {
        "Traditional Swiss Muesli": "Traditional Muesli",
        "Crunchy Granola": "Crunchy Muesli", 
        "Multi-grain Cereal": "Multigrain & Branflakes",
        "Breakfast Cereal": "Puffed Cereals",
        "Porridge & Hot Cereals": "Oat Flakes"
    }
    
    with app.app_context():
        products = Product.query.all()
        
        # First, migrate existing products
        for product in products:
            if product.category in category_mapping:
                old_category = product.category
                product.category = category_mapping[old_category]
                print(f"Updated {product.name}: {old_category} -> {product.category}")
        
        # Remove products with unmapped old categories
        old_categories_to_remove = [
            "Premium Breakfast Solutions",
            "Health & Wellness Cereals",
            "Artisanal Muesli Collection",
            "Baked Crunchy Muesli",
            "Cereal & Fruit Snack Bars",
            "Premium Oat Clusters",
            "Baked Muesli Crunchy"
        ]
        
        for old_category in old_categories_to_remove:
            products_to_remove = Product.query.filter_by(category=old_category).all()
            for product in products_to_remove:
                print(f"Removing product with old category: {product.name} ({old_category})")
                db.session.delete(product)
        
        # Add products for all 10 new categories
        new_products = [
            # 1. Flakes
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
                "image_url": "/static/images/cornflakes.jpg"
            },
            
            # 2. Multigrain & Branflakes
            {
                "name": "Multigrain Breakfast Flakes",
                "category": "Multigrain & Branflakes",
                "description": "Nutritious blend of multiple grains including wheat, rice, and corn. Rich in fiber and essential nutrients for a healthy start.",
                "ingredients": json.dumps([
                    {"name": "Wheat flakes", "percentage": 40},
                    {"name": "Rice flakes", "percentage": 25},
                    {"name": "Corn flakes", "percentage": 20},
                    {"name": "Bran", "percentage": 10},
                    {"name": "Vitamins & minerals", "percentage": 5}
                ]),
                "nutritional_claims": json.dumps([
                    "High in fiber",
                    "Multiple grain benefits",
                    "Fortified with vitamins",
                    "Wholesome nutrition"
                ]),
                "allergens": json.dumps([
                    "Contains gluten",
                    "May contain traces of nuts"
                ]),
                "certifications": json.dumps([
                    "Whole grain certified",
                    "Quality assured"
                ]),
                "image_url": "/static/images/multigrain-flakes.jpg"
            },
            
            # 3. Puffed Cereals
            {
                "name": "Chocolate Puffed Rice",
                "category": "Puffed Cereals",
                "description": "Light and airy chocolate-flavored puffed rice cereal. Perfect for kids and adults who love a sweet crunch.",
                "ingredients": json.dumps([
                    {"name": "Puffed rice", "percentage": 70},
                    {"name": "Cocoa powder", "percentage": 15},
                    {"name": "Sugar", "percentage": 10},
                    {"name": "Vitamin mix", "percentage": 3},
                    {"name": "Salt", "percentage": 2}
                ]),
                "nutritional_claims": json.dumps([
                    "Light and crunchy texture",
                    "Fortified with vitamins",
                    "Fun chocolate flavor",
                    "Low in fat"
                ]),
                "allergens": json.dumps([
                    "May contain traces of milk",
                    "May contain traces of nuts"
                ]),
                "certifications": json.dumps([
                    "Child-friendly approved",
                    "Quality certified"
                ]),
                "image_url": "/static/images/puffed-chocolate.jpg"
            },
            
            # 4. Extrudates & Co-Extrudates
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
                "image_url": "/static/images/honey-extrudates.jpg"
            },
            
            # 5. Traditional Muesli (already exists)
            
            # 6. Crunchy Muesli
            {
                "name": "Alpine Crunchy Granola",
                "category": "Crunchy Muesli",
                "description": "Premium crunchy granola with alpine herbs and mountain honey. A sophisticated twist on traditional granola.",
                "ingredients": json.dumps([
                    {"name": "Oat flakes", "percentage": 40},
                    {"name": "Almonds", "percentage": 20},
                    {"name": "Mountain honey", "percentage": 15},
                    {"name": "Hazelnuts", "percentage": 10},
                    {"name": "Alpine herbs", "percentage": 10},
                    {"name": "Coconut oil", "percentage": 5}
                ]),
                "nutritional_claims": json.dumps([
                    "Premium alpine ingredients",
                    "Natural mountain honey",
                    "High in healthy fats",
                    "Artisanal recipe"
                ]),
                "allergens": json.dumps([
                    "Contains nuts (almonds, hazelnuts)",
                    "May contain traces of other nuts",
                    "Contains gluten"
                ]),
                "certifications": json.dumps([
                    "Alpine quality certified",
                    "Natural ingredients"
                ]),
                "image_url": "/static/images/alpine-granola.jpg"
            },
            
            # 7. Bio & Fair-Trade muesli
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
                "image_url": "/static/images/fairtrade-muesli.jpg"
            },
            
            # 8. Oat Flakes
            {
                "name": "Premium Rolled Oats",
                "category": "Oat Flakes",
                "description": "High-quality rolled oats perfect for porridge, baking, or muesli. Rich in beta-glucan and heart-healthy fiber.",
                "ingredients": json.dumps([
                    {"name": "Rolled oats", "percentage": 100}
                ]),
                "nutritional_claims": json.dumps([
                    "100% pure oats",
                    "High in beta-glucan",
                    "Heart-healthy fiber",
                    "Versatile ingredient"
                ]),
                "allergens": json.dumps([
                    "Contains gluten",
                    "May contain traces of nuts"
                ]),
                "certifications": json.dumps([
                    "Premium quality",
                    "Sustainably sourced"
                ]),
                "image_url": "/static/images/rolled-oats.jpg"
            },
            
            # 9. Wheat, Rye & Barley Flakes
            {
                "name": "Ancient Grain Flakes Mix",
                "category": "Wheat, Rye & Barley Flakes",
                "description": "Traditional blend of wheat, rye, and barley flakes. Rich in complex carbohydrates and traditional grain nutrition.",
                "ingredients": json.dumps([
                    {"name": "Wheat flakes", "percentage": 40},
                    {"name": "Rye flakes", "percentage": 30},
                    {"name": "Barley flakes", "percentage": 25},
                    {"name": "Sea salt", "percentage": 5}
                ]),
                "nutritional_claims": json.dumps([
                    "Traditional grain blend",
                    "High in complex carbohydrates",
                    "Rich in B vitamins",
                    "Hearty texture"
                ]),
                "allergens": json.dumps([
                    "Contains gluten (wheat, rye, barley)",
                    "May contain traces of nuts"
                ]),
                "certifications": json.dumps([
                    "Traditional grain certified",
                    "Heritage quality"
                ]),
                "image_url": "/static/images/ancient-grain-flakes.jpg"
            },
            
            # 10. Bars
            {
                "name": "Energy Power Bars",
                "category": "Bars",
                "description": "High-energy bars packed with nuts, seeds, and dried fruits. Perfect for active lifestyles and on-the-go nutrition.",
                "ingredients": json.dumps([
                    {"name": "Dates", "percentage": 30},
                    {"name": "Almonds", "percentage": 25},
                    {"name": "Oats", "percentage": 20},
                    {"name": "Protein powder", "percentage": 15},
                    {"name": "Chia seeds", "percentage": 5},
                    {"name": "Honey", "percentage": 5}
                ]),
                "nutritional_claims": json.dumps([
                    "High in protein",
                    "Natural energy boost",
                    "Portable nutrition",
                    "No artificial additives"
                ]),
                "allergens": json.dumps([
                    "Contains nuts (almonds)",
                    "May contain milk",
                    "May contain traces of other allergens"
                ]),
                "certifications": json.dumps([
                    "Sports nutrition approved",
                    "Natural ingredients"
                ]),
                "image_url": "/static/images/energy-bars.jpg"
            }
        ]
        
        # Check if these products already exist before adding
        existing_names = {p.name for p in Product.query.all()}
        
        for product_data in new_products:
            if product_data["name"] not in existing_names:
                new_product = Product(**product_data)
                db.session.add(new_product)
                print(f"Added new product: {product_data['name']} in category {product_data['category']}")
        
        db.session.commit()
        print("Complete category migration with all 10 categories completed successfully!")
        
        # Print summary of all categories
        print("\nFinal category summary:")
        categories = db.session.query(Product.category).distinct().all()
        for i, (category,) in enumerate(categories, 1):
            count = Product.query.filter_by(category=category).count()
            print(f"{i}. {category} ({count} products)")

if __name__ == "__main__":
    migrate_categories()
