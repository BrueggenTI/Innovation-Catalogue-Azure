"""
Nutritional Claims Calculator for Brüggen Products
Automatically assigns nutritional claims based on Brüggen-specific thresholds
"""

def calculate_nutritional_claims(nutritional_info, portion_size=None):
    """
    Calculate applicable nutritional claims based on nutritional values
    
    Args:
        nutritional_info (dict): Nutritional values per 100g
            Expected keys: energy, fat, saturated_fat, carbohydrates, sugars, 
            fiber, protein, salt, beta_glucan (optional)
        portion_size (int): Optional portion size in grams (for beta-glucan claims)
    
    Returns:
        list: List of applicable nutritional claim strings (German names matching UI)
    """
    claims = []
    
    # Convert all values to float, defaulting to 0 if missing or invalid
    def get_value(key, default=0):
        try:
            value = nutritional_info.get(key, default)
            return float(value) if value not in [None, '', 'null'] else default
        except (ValueError, TypeError):
            return default
    
    energy = get_value('energy')
    fat = get_value('fat')
    saturated_fat = get_value('saturated_fat')
    sugars = get_value('sugars')
    salt = get_value('salt')
    fiber = get_value('fiber')
    protein = get_value('protein')
    beta_glucan = get_value('beta_glucan')
    
    # === PROTEIN CLAIMS ===
    # Calculate protein energy percentage (1g protein = 4 kcal)
    if energy > 0 and protein > 0:
        protein_energy_percent = (protein * 4 / energy) * 100
        
        # HOHER PROTEINGEHALT (High Protein): >25% Energie
        if protein_energy_percent > 25:
            claims.append("High Protein")
        # PROTEINQUELLE (Protein Source): >15% Energie
        elif protein_energy_percent > 15:
            claims.append("Source of Protein")
    
    # === FIBER CLAIMS ===
    # HOHER BALLASTSTOFFGEHALT (High Fiber): >7,5 g/100g
    if fiber > 7.5:
        claims.append("High Fiber")
    # BALLASTSTOFF-QUELLE (Fiber Source): >4,3 g/100g
    elif fiber > 4.3:
        claims.append("Source of Fiber")
    
    # === SUGAR CLAIMS ===
    # ZUCKERFREI (Sugar Free): < 0,3 g/100g
    if sugars < 0.3:
        claims.append("Sugar Free")
    # ZUCKERARM (Low Sugar): < 3,8 g/100g
    elif sugars < 3.8:
        claims.append("Low Sugar")
    
    # === FAT CLAIMS ===
    # FETTFREI / OHNE FETT (Fat Free): < 0,3 g/100g
    if fat < 0.3:
        claims.append("Fat Free")
    # FETTARM (Low Fat): < 2,3 g/100g
    elif fat < 2.3:
        claims.append("Low Fat")
    
    # === SATURATED FAT CLAIMS ===
    # ARM AN GESÄTTIGTEN FETTSÄUREN (Low Saturated Fat): < 0,6 g/100g
    if saturated_fat < 0.6:
        claims.append("Low Saturated Fat")
    
    # === SALT CLAIMS ===
    # SALZFREI (Salt Free): < 0,008 g/100g
    if salt < 0.008:
        claims.append("Salt Free")
    # SEHR SALZARM (Very Low Salt): < 0,07 g/100g
    elif salt < 0.07:
        claims.append("Very Low Salt")
    # SALZARM (Low Salt): < 0,20 g/100g
    elif salt < 0.20:
        claims.append("Low Salt")
    
    # === BETA GLUCAN CLAIMS ===
    # Only add if beta_glucan data is available and portion size is provided
    if beta_glucan > 0 and portion_size:
        if portion_size == 20 and beta_glucan > 7.0:
            claims.append("High Beta-Glucan (20g portion)")
        elif portion_size == 25 and beta_glucan > 5.7:
            claims.append("High Beta-Glucan (25g portion)")
        elif portion_size == 30 and beta_glucan > 4.7:
            claims.append("High Beta-Glucan (30g portion)")
        elif portion_size == 35 and beta_glucan > 4.1:
            claims.append("High Beta-Glucan (35g portion)")
        elif portion_size == 40 and beta_glucan > 3.6:
            claims.append("High Beta-Glucan (40g portion)")
        elif portion_size == 45 and beta_glucan > 3.1:
            claims.append("High Beta-Glucan (45g portion)")
    
    return claims


def get_claim_translation_map():
    """
    Returns a mapping of internal claim names to UI display names
    This ensures consistency with the existing UI claims
    """
    return {
        "High Protein": "High Protein",
        "Source of Protein": "Source of Protein",
        "High Fiber": "High Fiber",
        "Source of Fiber": "Source of Fiber",
        "Low Sugar": "Low Sugar",
        "Sugar Free": "Sugar Free",
        "No Added Sugar": "No Added Sugar",  # This is certification/ingredient-based, not auto-calculated
        "Low Fat": "Low Fat",
        "Fat Free": "Fat Free",
        "Low Saturated Fat": "Low Saturated Fat",
        "Low Salt": "Low Salt",
        "Very Low Salt": "Very Low Salt",
        "Salt Free": "Salt Free",
        "High Beta-Glucan (20g portion)": "High Beta-Glucan (20g)",
        "High Beta-Glucan (25g portion)": "High Beta-Glucan (25g)",
        "High Beta-Glucan (30g portion)": "High Beta-Glucan (30g)",
        "High Beta-Glucan (35g portion)": "High Beta-Glucan (35g)",
        "High Beta-Glucan (40g portion)": "High Beta-Glucan (40g)",
        "High Beta-Glucan (45g portion)": "High Beta-Glucan (45g)",
    }


def merge_claims(auto_claims, manual_claims=None):
    """
    Merge automatically calculated claims with manually selected claims
    Removes duplicates while preserving manual selections
    
    Args:
        auto_claims (list): Automatically calculated claims
        manual_claims (list): Manually selected claims from user
    
    Returns:
        list: Merged unique claims
    """
    if manual_claims is None:
        manual_claims = []
    
    # Combine both lists and remove duplicates while preserving order
    all_claims = auto_claims + [claim for claim in manual_claims if claim not in auto_claims]
    
    return all_claims
