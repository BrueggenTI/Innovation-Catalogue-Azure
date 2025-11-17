SHELF_LIFE_DATA = {
    "Product in toppers": {"months": 6, "days": 180},
    "Products with probiotic bacteria (Lactobacillus)": {"months": 8, "days": 240},
    "Cornflakes": {"months": 14, "days": 425},
    "Snowies (coated cornflakes)": {"months": 12, "days": 365},
    "Cornflakes with cacao": {"months": 14, "days": 425},
    "Crunchy flakes (Peanut honey flakes)": {"months": 14, "days": 425},
    "Spelt flakes (toasted)": {"months": 14, "days": 425},
    "Barley flakes (toasted)": {"months": 14, "days": 425},
    "Oat flakes (toasted)": {"months": 10, "days": 300},
    "Rice flakes (toasted)": {"months": 12, "days": 365},
    "Rice cooked": {"months": 12, "days": 365},
    "Wheat flakes (toasted)": {"months": 12, "days": 365},
    "Multigrainflakes": {"months": 12, "days": 365},
    "Branflakes": {"months": 12, "days": 365},
    "Speltflakes": {"months": 12, "days": 365},
    "Puffed wheat/barley/rye/rice": {"months": 12, "days": 365},
    "Swietwiet (puffed wheat with honey)": {"months": 14, "days": 425},
    "Swietwiet with sunflower oil": {"months": 12, "days": 365},
    "Cacao coated Swietwiet": {"months": 12, "days": 365},
    "Extruded products": {"months": 14, "days": 425},
    "Extruded products with fiber": {"months": 12, "days": 365},
    "Extruded products with sunflower oil": {"months": 12, "days": 365},
    "Extruded products of oat": {"months": 10, "days": 300},
    "Bransticks": {"months": 9, "days": 270},
    "Cinn-X (extruded product with oil coating and cinnamon)": {"months": 12, "days": 365},
    "Filled cereals": {"months": 10, "days": 300},
    "Muesli": {"months": 12, "days": 365},
    "Crunchy muesli": {"months": 12, "days": 365},
    "Crunchy muesli with sunflower oil and tocopherols": {"months": 12, "days": 365},
    "Crunchy muesli with sunflower oil (without tocopherols)": {"months": 9, "days": 270},
    "Muesli bars": {"months": 12, "days": 365},
    "Cereal bars": {"months": 12, "days": 365},
    "Bars without sugar": {"months": 10, "days": 300},
    "Baked bars (external production)": {"months": 12, "days": 365},
    "Fruit bars": {"months": 9, "days": 270},
    "Wheat flakes": {"months": 15, "days": 450},
    "Rye flakes": {"months": 15, "days": 450},
    "Oat flakes": {"months": 12, "days": 365},
    "Barley flakes": {"months": 12, "days": 365},
    "Nutriments (sago, pearl, etc.)": {"months": 15, "days": 450},
    "Porridge (including protein porridge)": {"months": 15, "days": 450},
    "Puddings including protein pudding": {"months": 15, "days": 450},
    "Millet flakes": {"months": 9, "days": 270},
}

def get_shelf_life(category):
    """
    Gets the shelf life for a given product category.
    Returns a formatted string like "12 months (365 days)" or None if not found.
    """
    if category in SHELF_LIFE_DATA:
        data = SHELF_LIFE_DATA[category]
        return f"{data['months']} months ({data['days']} days)"
    return None

def get_all_categories():
    """
    Returns a list of all available product categories.
    """
    return list(SHELF_LIFE_DATA.keys())
