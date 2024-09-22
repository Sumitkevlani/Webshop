import ast
from openai import OpenAI
from decouple import config

class ProductRetriever:
    def __init__(self):
        # Initialize the OpenAI client with the API key
        self.openai_api_key = str(config('OPENAI_API_KEY'))
        self.client = OpenAI(api_key=self.openai_api_key)

    def get_relevant_products(self, query, products):
        """
        This method takes a user query and a list of products,
        and returns a list of relevant product IDs using OpenAI's Chat Completion API.
        """
        prompt_template = (
            """
            You are an AI assistant that retrieves product IDs based on specific queries related to products. 
            Your task is to analyze the product information provided below and return only the relevant product IDs in the form of a list.
            For example:
            User query: "Provide me the laptops with a rating greater than 4.0 and price less than 80 thousand"
            Product information:
            1. Product ID: id1, Name: Laptop A, Price: 90000, Rating: 4.5
            2. Product ID: id2, Name: Laptop B, Price: 75000, Rating: 4.3 
            3. Product ID: id3, Name: Laptop C, Price: 70000, Rating: 4.1
            4. Product ID: id4, Name: Laptop D, Price: 120000, Rating: 4.0 
            5. Product ID: id5, Name: Laptop E, Price: 95000, Rating: 3.8
            Response: ['id2','id3']
            Now please process the following query:
            User query: "{user_query}"
            Product information:
            {product_information}
            Response:
            """
        )
        
        # Format the products into a string representation
        formatted_products = "\n".join([
            f"ID: {str(product['_id'])}, Name: {product['name']}, Price: {product['price']}, Rating: {product['rating']}" 
            for product in products
        ])
        
        prompt = prompt_template.format(product_information=formatted_products, user_query=query)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Use the appropriate model
                messages=[{"role": "user", "content": prompt}],
            )
            
            # Extract the product IDs from the response
            relevant_ids = response.choices[0].message.content
            
            # Process the returned content to extract product IDs
            # Assuming the model returns the IDs as a list
            product_ids = ast.literal_eval(relevant_ids if relevant_ids is not None else "[]")
            print(product_ids)
            return product_ids
        
        except Exception as e:
            print(f"Error communicating with OpenAI API: {e}")
            return []