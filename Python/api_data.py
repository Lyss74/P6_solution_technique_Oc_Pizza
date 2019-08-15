# -*- coding: Utf-8 -*-


from Python.config import CATEGORIES, LIST_PIZZA
import requests as req


class ApiCollectingData:
    """
        This class has the responsibility
        of collecting a certain number
        of products, in selected categories, thus to give a valid
        structure for the insertion in the database
    """

    def __init__(self):
        # The manufacturer will share the product requests for data generation
        self.all_product = self.connect_and_dowload_per_category()
        self.barcode = self.connect_and_download_per_barcode()

    def connect_and_dowload_per_category(self):
        # Use the configuration for the connecting interface
        product_categories = []
        # Address OpenFooFact.org the API FR locating
        api = "https://fr.openfoodfacts.org/cgi/search.pl"
        for category in CATEGORIES:
            # This config for  for connecting API
            config = {
                "action": "process",
                "tagtype_0": "categories",
                'tag_0': category,
                "tag_contains_0": "contains",
                "page_size": 5,
                "json": 1
                    }
            response = req.get(api, params=config)
            results = response.json()

            products_section = results['products']
            for product in products_section:
                product['main_category'] = category
                product_categories.extend(products_section)
        return product_categories

    def format_final_response(self, all_products):
        """
        Formatted the response just harvest the categories selected

        Args:
            all_products (list): All the products

        Returns:
            Python.dataclass_data.Product: Returns the product instance
        """
        keys = [
            'id',
            'product_name_fr',
            'main_category',
            'generic_name_fr']
        for product in all_products:
            if self.validate_the_data(keys, product):
                return product

    def connect_and_download_per_barcode(self):
        # Use the configuration for the connecting interface
        product_barcode = []
        for barcode in self.barcode_part():
            bar_code = (
                f"https://fr.openfoodfacts.org/api/v0/produit/"
                f"{barcode}"
            )
            config = {
                'tag_0': barcode
            }
            response = req.get(bar_code, params=config)
            results = response.json()
            product_section = results['product']
            product_barcode.append(product_section)
        return product_barcode

    # def product_type(self):
    #     product_type = []
    #     for product in self.connect_and_download_per_barcode():
    #         product_type.append(product['product_name'])
    #     return product_type

    def barcode_part(self):
        """

        Returns:

        """
        # Cutting barcode lists for Ordered Recipes
        bar_codes = []
        for codes in LIST_PIZZA:
            bar_codes.extend(codes)
        return bar_codes

    def key_weight(self):
        # Add the weight of each product
        product = self.connect_and_download_per_barcode()
        weights = []
        for weight in product:
            key = weight['quantity'].split()
            weight = key[0]
            weights.append(str(weight))
        return weights

    def validate_the_data(self, keys, products_section):
        # Validate the complete fields
        for key in keys:
            if key not in products_section or not products_section[key]:
                return False
        return True
