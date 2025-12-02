from app import app, db
from models import Product
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate_nutriscore():
    """
    Migrate existing products to populate the nutri_score column
    based on the nutri_score_image path.
    """
    logger.info("Starting Nutri-Score migration...")

    with app.app_context():
        products = Product.query.all()
        updated_count = 0

        for product in products:
            if product.nutri_score:
                logger.info(f"Product {product.id} ({product.name}) already has Nutri-Score: {product.nutri_score}")
                continue

            if not product.nutri_score_image:
                logger.info(f"Product {product.id} ({product.name}) has no Nutri-Score image. Skipping.")
                continue

            # Attempt to extract Nutri-Score from image path
            # Expected formats:
            # - /static/images/nutriscore_a.jpg
            # - /static/images/nutriscore_b.png
            # - etc.

            image_path = product.nutri_score_image.lower()
            score = None

            if 'nutriscore_a' in image_path:
                score = 'A'
            elif 'nutriscore_b' in image_path:
                score = 'B'
            elif 'nutriscore_c' in image_path:
                score = 'C'
            elif 'nutriscore_d' in image_path:
                score = 'D'
            elif 'nutriscore_e' in image_path:
                score = 'E'

            if score:
                product.nutri_score = score
                updated_count += 1
                logger.info(f"Updated Product {product.id} ({product.name}) with Nutri-Score: {score}")
            else:
                logger.warning(f"Could not determine Nutri-Score for Product {product.id} from image: {product.nutri_score_image}")

        if updated_count > 0:
            db.session.commit()
            logger.info(f"Successfully updated {updated_count} products.")
        else:
            logger.info("No products needed updating.")

if __name__ == "__main__":
    migrate_nutriscore()
