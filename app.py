import chainlit as cl
import requests

API_URL = "https://hackathon-apis.vercel.app/api/products"

def fetch_products(query: str) -> str:
    try:
        response = requests.get(API_URL)
        data = response.json()

        matched = [p for p in data if query.lower() in p.get("name", "").lower()]
        if not matched:
            return f"❌ No products found for '**{query}**'. Try another keyword."

        result = ""
        for product in matched[:5]:
            name = product.get("name", "Unknown Product")
            price = product.get("price", 0)
            image = product.get("image", "")

            result += f"""
### 🛒 {name}
💰 **Price:** ${int(price):,}  
![{name}]({image})  
---
"""

        return result

    except Exception as e:
        return f"🚨 Error fetching products: {str(e)}"

@cl.on_chat_start
async def greet():
    await cl.Message(
        content="""
👋 **Welcome to the AI Shopping Agent!**

Just type what you're looking for, like:

- Sofa
- Chair
- Lamp

I'll fetch real-time products with images for you. 🛍️
"""
    ).send()

@cl.on_message
async def handle_message(msg: cl.Message):
    user_query = msg.content.strip()

    if not user_query:
        await cl.Message(content="❗ Please type a product name to search.").send()
        return

    await cl.Message(content="🔎 Searching for products...").send()

    result = fetch_products(user_query)
    await cl.Message(content=result).send()
