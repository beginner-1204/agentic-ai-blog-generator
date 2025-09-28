import requests
import json
import google.generativeai as genai
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def send_email(blog_content):
    # Email configuration
    sender_email = "arnavgoyal1204@gmail.com"
    sender_password = "slrm qoar kvga kvus"  # App password
    receiver_email = "arnav.g25081@nst.rishihood.edu.in"
    
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f"Fashion Stores in Sonipat - Blog Post {datetime.now().strftime('%Y-%m-%d')}"
    
    # Add HTML formatting to the blog content
    html_content = f"""
    <html>
        <body>
            <h1>Fashion Stores in Sonipat - Your Ultimate Shopping Guide</h1>
            <div style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                {blog_content.replace('\n', '<br>')}
            </div>
            <hr>
            <p style="color: #666; font-size: 12px;">
                This blog post was automatically generated based on local fashion store data.
                Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </p>
        </body>
    </html>
    """
    
    msg.attach(MIMEText(html_content, 'html'))
    
    try:
        # Create SMTP session with debug mode
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.set_debuglevel(1)  # Enable debug mode
        print("Starting SMTP connection...")
        
        server.starttls()
        print("TLS connection established...")
        
        print("Attempting login...")
        server.login(sender_email, sender_password)
        print("Login successful...")
        
        text = msg.as_string()
        print("Sending email...")
        server.send_message(msg)
        print("Email sent...")
        
        server.quit()
        return "Email sent successfully!"
    except smtplib.SMTPAuthenticationError as e:
        return f"Authentication failed: Please check your email and app password. Error: {str(e)}"
    except smtplib.SMTPException as e:
        return f"SMTP error occurred: {str(e)}"
    except Exception as e:
        return f"Failed to send email: {str(e)}"

def generate_blog_post(shops_data):
    # Create a template-based blog post
    blog_post = f"""
Your Ultimate Guide to Fashion Shopping in Sonipat, Haryana

Looking for the perfect shopping destination in Sonipat? Whether you're searching for traditional Indian wear or contemporary fashion, Sonipat's vibrant fashion scene has something for everyone. Let's explore some of the city's finest clothing stores that combine style, quality, and excellent customer service.

🌟 Top Fashion Destinations in Sonipat

1. {shops_data[0]['name']}
------------------------
{shops_data[0]['description']}
What makes it special: {', '.join(shops_data[0].get('attributes', ['Premium shopping experience']))}

2. {shops_data[1]['name']}
------------------------
{shops_data[1]['description']}
A must-visit destination for fashion enthusiasts looking for variety and quality.

3. {shops_data[2]['name']}
------------------------
{shops_data[2]['description']}
Perfect for those who appreciate personalized service and craftsmanship.

⭐ Local Favorite
{shops_data[3]['name']}
{shops_data[3]['description']}

Why Shop in Sonipat?
-------------------
• Diverse Fashion Choices: From traditional to contemporary
• Competitive Pricing: Get the best value for your money
• Excellent Customer Service: Personalized attention at every store
• Convenient Location: Easy access to all major shopping destinations
• Quality Assurance: Trusted brands and reliable local boutiques

Shopping Tips:
-------------
• Most stores are open from morning until evening
• Visit during weekdays for a more relaxed shopping experience
• Many stores offer customization services
• Don't forget to check out seasonal sales and festive offers

Whether you're looking for everyday wear, special occasion outfits, or traditional ensembles, Sonipat's fashion stores offer an impressive selection to suit every style and budget. Visit these stores to experience the perfect blend of fashion, tradition, and modern retail convenience.

#SonipatFashion #ShoppingInHaryana #FashionDestination #IndianFashion"""
    return blog_post

def fetch_clothing_shops():
    # Serper API endpoint
    url = "https://google.serper.dev/search"
    
    # API key
    api_key = "f84f7aff7f26e8cb2a06a8cfad3c842436c2bb9c"
    
    # Headers
    headers = {
        'X-API-Key': api_key,
        'Content-Type': 'application/json'
    }
    
    # Search parameters
    payload = {
        "q": "clothing shops garment stores fashion boutiques Sonipat Haryana",
        "num": 10,  # Number of results to fetch
        "type": "search"
    }
    
    try:
        # For testing purposes, let's use sample data since we're having API issues
        # In production, uncomment the API call below
        # response = requests.post(url, headers=headers, json=payload)
        # response.raise_for_status()
        # data = response.json()
        
        # Sample data for testing
        data = {
            "organic": [
                {
                    "title": "Fashion Hub Sonipat",
                    "snippet": "Premier clothing destination in Sonipat offering latest fashion trends for men, women, and children. Known for its extensive collection of ethnic and western wear.",
                    "link": "https://example.com/fashionhub",
                    "position": 1,
                    "attributes": ["Multi-brand store", "Premium collection"]
                },
                {
                    "title": "Trends Fashion Mall",
                    "snippet": "One of the largest fashion retailers in Sonipat with multiple brands under one roof. Specialized in casual wear, formal wear, and traditional Indian clothing.",
                    "link": "https://example.com/trends",
                    "position": 2
                },
                {
                    "title": "Royal Garments",
                    "snippet": "Family-owned boutique known for high-quality traditional wear and customized clothing. Expert tailoring services available.",
                    "link": "https://example.com/royal",
                    "position": 3
                }
            ],
            "places": [
                {
                    "title": "City Style Fashion Store",
                    "address": "Near Bus Stand, Sonipat, Haryana",
                    "rating": "4.5",
                    "reviews": "156",
                    "phone": "+91-1234567890",
                    "hours": "10:00 AM - 9:00 PM"
                }
            ]
        }
        
        print("Sample Data:", json.dumps(data, indent=2))  # Debug print
        
        # Process and structure the results
        shops = []
        
        # The response structure can include:
        # - searchParameters: Search query parameters
        # - organic: Regular search results
        # - knowledgeGraph: Detailed information about entities
        # - peopleAlsoAsk: Related questions
        # - relatedSearches: Similar search queries
        # - places: Local business results (if available)
        
        print("\nAPI Response Structure:")
        print("======================")
        for key in data.keys():
            print(f"- {key}")
            
        if 'organic' in data:
            for result in data['organic']:
                shop_info = {
                    'name': result.get('title', 'N/A'),
                    'description': result.get('snippet', 'N/A'),
                    'link': result.get('link', 'N/A'),
                    'position': result.get('position', 'N/A')
                }
                if 'attributes' in result:
                    shop_info['attributes'] = result['attributes']
                shops.append(shop_info)
                
        if 'places' in data:
            for place in data['places']:
                shop_info = {
                    'name': place.get('title', 'N/A'),
                    'description': f"Located at {place.get('address', 'N/A')}. Rating: {place.get('rating', 'N/A')}/5 ({place.get('reviews', '0')} reviews). Hours: {place.get('hours', 'N/A')}",
                    'link': place.get('website', 'N/A'),
                    'address': place.get('address', 'N/A'),
                    'rating': place.get('rating', 'N/A'),
                    'reviews': place.get('reviews', 'N/A'),
                    'phone': place.get('phone', 'N/A'),
                    'hours': place.get('hours', 'N/A')
                }
                shops.append(shop_info)
        
        # Print results in a structured format
        print("\n=== Top Clothing Shops in Sonipat, Haryana ===\n")
        for i, shop in enumerate(shops, 1):
            print(f"Shop #{i}")
            print(f"Name: {shop['name']}")
            print(f"Description: {shop['description']}")
            print(f"Link: {shop['link']}")
            print("-" * 50)
        
        # Generate and print the blog post
        print("\n=== Generated Blog Post ===\n")
        blog_post = generate_blog_post(shops)
        print(blog_post)
        
        # Send the blog post via email
        print("\n=== Sending Email ===\n")
        email_result = send_email(blog_post)
        print(email_result)
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    fetch_clothing_shops()
