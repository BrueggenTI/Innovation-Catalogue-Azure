"""
Test Script for Nutritional Claims Calculator
Demonstrates automatic claim calculation based on Brüggen thresholds
"""

from utils.claim_calculator import calculate_nutritional_claims, merge_claims

def test_high_protein_product():
    """Test: High Protein Product (e.g., Protein Cereal)"""
    print("\n=== TEST 1: High Protein Product ===")
    nutritional_info = {
        'energy': 380,      # kcal per 100g
        'fat': 5.0,         # g per 100g
        'saturated_fat': 1.0,
        'carbohydrates': 50.0,
        'sugars': 3.5,      # Low sugar
        'fiber': 8.0,       # High fiber
        'protein': 25.0,    # High protein (25g * 4kcal = 100kcal = 26.3% of energy)
        'salt': 0.15        # Low salt
    }
    
    claims = calculate_nutritional_claims(nutritional_info)
    print(f"Nutritional Info: {nutritional_info}")
    print(f"Calculated Claims: {claims}")
    print(f"Expected: ['High Protein', 'High Fiber', 'Low Sugar', 'Low Salt']")
    
    return claims


def test_low_sugar_product():
    """Test: Low Sugar Product (e.g., Unsweetened Muesli)"""
    print("\n=== TEST 2: Low Sugar Product ===")
    nutritional_info = {
        'energy': 350,
        'fat': 8.0,
        'saturated_fat': 1.5,
        'carbohydrates': 58.0,
        'sugars': 2.5,      # Low sugar (< 3.8g)
        'fiber': 9.0,       # High fiber
        'protein': 10.0,
        'salt': 0.05        # Very low salt
    }
    
    claims = calculate_nutritional_claims(nutritional_info)
    print(f"Nutritional Info: {nutritional_info}")
    print(f"Calculated Claims: {claims}")
    print(f"Expected: ['High Fiber', 'Low Sugar', 'Very Low Salt']")
    
    return claims


def test_sugar_free_product():
    """Test: Sugar Free Product"""
    print("\n=== TEST 3: Sugar Free Product ===")
    nutritional_info = {
        'energy': 320,
        'fat': 12.0,
        'saturated_fat': 2.0,
        'carbohydrates': 45.0,
        'sugars': 0.2,      # Sugar free (< 0.3g)
        'fiber': 6.0,
        'protein': 8.0,
        'salt': 0.01        # Very low salt
    }
    
    claims = calculate_nutritional_claims(nutritional_info)
    print(f"Nutritional Info: {nutritional_info}")
    print(f"Calculated Claims: {claims}")
    print(f"Expected: ['High Fiber', 'Sugar Free', 'Very Low Salt']")
    
    return claims


def test_fat_free_product():
    """Test: Fat Free / Low Fat Product"""
    print("\n=== TEST 4: Fat Free Product ===")
    nutritional_info = {
        'energy': 280,
        'fat': 0.2,         # Fat free (< 0.3g)
        'saturated_fat': 0.05,  # Low saturated fat
        'carbohydrates': 60.0,
        'sugars': 5.0,
        'fiber': 5.0,       # Fiber source
        'protein': 8.0,
        'salt': 0.18        # Low salt
    }
    
    claims = calculate_nutritional_claims(nutritional_info)
    print(f"Nutritional Info: {nutritional_info}")
    print(f"Calculated Claims: {claims}")
    print(f"Expected: ['Source of Fiber', 'Fat Free', 'Low Saturated Fat', 'Low Salt']")
    
    return claims


def test_merge_claims_functionality():
    """Test: Merge automatic and manual claims"""
    print("\n=== TEST 5: Merge Claims (Auto + Manual) ===")
    
    # Automatic claims from nutritional calculation
    auto_claims = ['High Protein', 'High Fiber', 'Low Sugar']
    
    # Manual claims selected by user
    manual_claims = ['Vegan', 'Gluten Free', 'High Fiber']  # 'High Fiber' is duplicate
    
    merged = merge_claims(auto_claims, manual_claims)
    print(f"Auto Claims: {auto_claims}")
    print(f"Manual Claims: {manual_claims}")
    print(f"Merged Claims (no duplicates): {merged}")
    print(f"Expected: ['High Protein', 'High Fiber', 'Low Sugar', 'Vegan', 'Gluten Free']")
    
    return merged


def test_protein_source_product():
    """Test: Protein Source (not High Protein)"""
    print("\n=== TEST 6: Protein Source Product ===")
    nutritional_info = {
        'energy': 400,
        'fat': 10.0,
        'saturated_fat': 2.0,
        'carbohydrates': 65.0,
        'sugars': 8.0,
        'fiber': 7.8,       # High fiber
        'protein': 16.0,    # Protein source (16g * 4kcal = 64kcal = 16% of energy)
        'salt': 0.25
    }
    
    claims = calculate_nutritional_claims(nutritional_info)
    print(f"Nutritional Info: {nutritional_info}")
    print(f"Calculated Claims: {claims}")
    print(f"Expected: ['Source of Protein', 'High Fiber']")
    
    return claims


def test_real_world_product():
    """Test: Real-world product example - Oat Flakes"""
    print("\n=== TEST 7: Real-World Example - Classic Oat Flakes ===")
    nutritional_info = {
        'energy': 368,
        'fat': 7.0,
        'saturated_fat': 1.2,
        'carbohydrates': 58.7,
        'sugars': 0.7,      # Sugar free
        'fiber': 10.0,      # High fiber
        'protein': 13.5,    # Protein source (13.5 * 4 = 54, 54/368 = 14.7%)
        'salt': 0.01        # Very low salt
    }
    
    claims = calculate_nutritional_claims(nutritional_info)
    print(f"Nutritional Info: {nutritional_info}")
    print(f"Calculated Claims: {claims}")
    print(f"Expected: ['High Fiber', 'Sugar Free', 'Very Low Salt']")
    
    return claims


def test_edge_cases():
    """Test: Edge cases at threshold boundaries"""
    print("\n=== TEST 8: Edge Cases - Threshold Boundaries ===")
    
    # Just below threshold
    nutritional_info_below = {
        'energy': 400,
        'fat': 2.4,         # Just above low fat threshold (2.3)
        'saturated_fat': 0.61,  # Just above low saturated fat (0.6)
        'sugars': 3.9,      # Just above low sugar (3.8)
        'fiber': 4.2,       # Just below fiber source (4.3)
        'protein': 14.0,    # 14 * 4 / 400 = 14% (just below protein source 15%)
        'salt': 0.21        # Just above low salt (0.20)
    }
    
    claims_below = calculate_nutritional_claims(nutritional_info_below)
    print(f"\nJust ABOVE thresholds (should NOT qualify):")
    print(f"Nutritional Info: {nutritional_info_below}")
    print(f"Calculated Claims: {claims_below}")
    print(f"Expected: [] (no claims)")
    
    # Just at threshold
    nutritional_info_at = {
        'energy': 400,
        'fat': 2.2,         # Low fat (< 2.3)
        'saturated_fat': 0.5,  # Low saturated fat (< 0.6)
        'sugars': 3.7,      # Low sugar (< 3.8)
        'fiber': 4.4,       # Fiber source (> 4.3)
        'protein': 16.0,    # 16 * 4 / 400 = 16% (protein source > 15%)
        'salt': 0.19        # Low salt (< 0.20)
    }
    
    claims_at = calculate_nutritional_claims(nutritional_info_at)
    print(f"\nJust BELOW thresholds (should qualify):")
    print(f"Nutritional Info: {nutritional_info_at}")
    print(f"Calculated Claims: {claims_at}")
    print(f"Expected: ['Source of Protein', 'Source of Fiber', 'Low Sugar', 'Low Fat', 'Low Saturated Fat', 'Low Salt']")
    
    return claims_below, claims_at


if __name__ == "__main__":
    print("=" * 80)
    print("BRÜGGEN NUTRITIONAL CLAIMS CALCULATOR - TEST SUITE")
    print("=" * 80)
    
    # Run all tests
    test_high_protein_product()
    test_low_sugar_product()
    test_sugar_free_product()
    test_fat_free_product()
    test_merge_claims_functionality()
    test_protein_source_product()
    test_real_world_product()
    test_edge_cases()
    
    print("\n" + "=" * 80)
    print("TEST SUITE COMPLETED")
    print("=" * 80)
    
    print("\n📊 BRÜGGEN THRESHOLD REFERENCE:")
    print("-" * 80)
    print("Protein:           > 15% energy = Source | > 25% energy = High")
    print("Fiber:             > 4.3 g/100g = Source | > 7.5 g/100g = High")
    print("Sugar:             < 3.8 g/100g = Low    | < 0.3 g/100g = Free")
    print("Fat:               < 2.3 g/100g = Low    | < 0.3 g/100g = Free")
    print("Saturated Fat:     < 0.6 g/100g = Low")
    print("Salt:              < 0.20 g/100g = Low   | < 0.07 g/100g = Very Low | < 0.008 g/100g = Free")
    print("-" * 80)
