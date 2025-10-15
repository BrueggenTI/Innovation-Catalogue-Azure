"""
Nutri-Score Image Mapper
Automatically selects the correct Nutri-Score image based on the score value
"""

import os

def get_nutriscore_image(nutriscore_value):
    """
    Returns the path to the appropriate Nutri-Score image based on the score
    
    Args:
        nutriscore_value: Can be 'A', 'B', 'C', 'D', 'E' or None
        
    Returns:
        str: Path to the Nutri-Score image file
    """
    if not nutriscore_value:
        return None
    
    # Normalize to uppercase
    score = str(nutriscore_value).strip().upper()
    
    # Map score to image file
    score_mapping = {
        'A': '/static/images/nutriscore_a.jpg',
        'B': '/static/images/nutriscore_b.jpg',
        'C': '/static/images/nutriscore_c.jpg',
        'D': '/static/images/nutriscore_d.jpg',
        'E': '/static/images/nutriscore_e.jpg'
    }
    
    return score_mapping.get(score)

def extract_nutriscore_from_text(text):
    """
    Extracts Nutri-Score from text patterns like "Nutri-Score: C" or just "C"
    
    Args:
        text: String containing Nutri-Score information
        
    Returns:
        str: The Nutri-Score letter (A-E) or None
    """
    if not text:
        return None
    
    text = str(text).upper().strip()
    
    # Check for valid Nutri-Score values
    valid_scores = ['A', 'B', 'C', 'D', 'E']
    
    # Direct match
    if text in valid_scores:
        return text
    
    # Search for pattern in text
    for score in valid_scores:
        if score in text:
            return score
    
    return None
