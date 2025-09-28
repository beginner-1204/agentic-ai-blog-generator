import streamlit as st
import requests
import json
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Set page configuration
st.set_page_config(
    page_title="Sonipat Fashion Stores Blog Generator",
    page_icon="👕",
    layout="wide"
)

# Function to fetch shop details
def fetch_clothing_shops(api_key):
    url = "https://google.serper.dev/search"
    headers = {
        'X-API-Key': api_key,
        'Content-Type': 'application/json'
    }
    payload = {
        "q": "clothing shops garment stores fashion boutiques Sonipat Haryana",
        "num": 10,
        "type": "search"
    }
    
    try:
        # For demonstration, using sample data
        # In production, uncomment the API call
        # response = requests.post(url, headers=headers, json=payload)
        # response.raise_for_status()
        # data = response.json()
        
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
        return data
    except Exception as e:
        st.error(f"Error fetching shop details: {str(e)}")
        return None

# Function to generate blog post
def generate_blog_post(shops_data):
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

#SonipatFashion #ShoppingInHaryana #FashionDestination #IndianFashion
    """
    return blog_post

# Function to send email
def send_email(blog_content, sender_email, sender_password, receiver_email):
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = f"Fashion Stores in Sonipat - Blog Post {datetime.now().strftime('%Y-%m-%d')}"
        
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
        
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return True
    except Exception as e:
        st.error(f"Error sending email: {str(e)}")
        return False

# Main Streamlit UI
def main():
    st.title("🏪 Sonipat Fashion Stores Blog Generator")
    st.write("Generate and send blog posts about fashion stores in Sonipat")
    
    # Sidebar for API keys and email settings
    st.sidebar.header("⚙️ Settings")
    serper_api_key = st.sidebar.text_input("Serper API Key", value="f84f7aff7f26e8cb2a06a8cfad3c842436c2bb9c")
    
    # Email settings in sidebar
    st.sidebar.subheader("📧 Email Settings")
    sender_email = st.sidebar.text_input("Sender Email", value="arnavgoyal1204@gmail.com")
    sender_password = st.sidebar.text_input("App Password", value="slrm qoar kvga kvus", type="password")
    receiver_email = st.sidebar.text_input("Receiver Email", value="arnav.g25081@nst.rishihood.edu.in")
    
    # Main content area with tabs
    tab1, tab2, tab3 = st.tabs(["1. Fetch Shops", "2. Generate Blog", "3. Send Email"])
    
    # Store data in session state
    if 'shops_data' not in st.session_state:
        st.session_state.shops_data = None
    if 'blog_content' not in st.session_state:
        st.session_state.blog_content = None
    
    # Tab 1: Fetch Shops
    with tab1:
        st.header("🔍 Fetch Shop Details")
        if st.button("Fetch Shops"):
            with st.spinner("Fetching shop details..."):
                data = fetch_clothing_shops(serper_api_key)
                if data:
                    shops = []
                    if 'organic' in data:
                        for result in data['organic']:
                            shops.append({
                                'name': result.get('title', 'N/A'),
                                'description': result.get('snippet', 'N/A'),
                                'link': result.get('link', 'N/A'),
                                'position': result.get('position', 'N/A'),
                                'attributes': result.get('attributes', [])
                            })
                    
                    if 'places' in data:
                        for place in data['places']:
                            shops.append({
                                'name': place.get('title', 'N/A'),
                                'description': f"Located at {place.get('address', 'N/A')}. Rating: {place.get('rating', 'N/A')}/5 ({place.get('reviews', '0')} reviews). Hours: {place.get('hours', 'N/A')}",
                                'link': place.get('website', 'N/A')
                            })
                    
                    st.session_state.shops_data = shops
                    st.success("✅ Shop details fetched successfully!")
                    
                    # Display shops in an expander
                    with st.expander("View Fetched Shops"):
                        for i, shop in enumerate(shops, 1):
                            st.subheader(f"Shop #{i}: {shop['name']}")
                            st.write(f"Description: {shop['description']}")
                            st.write(f"Link: {shop['link']}")
                            st.divider()
    
    # Tab 2: Generate Blog
    with tab2:
        st.header("✍️ Generate Blog Post")
        if st.button("Generate Blog"):
            if st.session_state.shops_data:
                with st.spinner("Generating blog post..."):
                    blog_content = generate_blog_post(st.session_state.shops_data)
                    st.session_state.blog_content = blog_content
                    st.success("✅ Blog post generated successfully!")
                    st.markdown(blog_content)
            else:
                st.warning("⚠️ Please fetch shop details first!")
    
    # Tab 3: Send Email
    with tab3:
        st.header("📤 Send Blog Post via Email")
        if st.button("Send Email"):
            if st.session_state.blog_content:
                with st.spinner("Sending email..."):
                    if send_email(st.session_state.blog_content, sender_email, sender_password, receiver_email):
                        st.success("✅ Email sent successfully!")
                    else:
                        st.error("❌ Failed to send email!")
            else:
                st.warning("⚠️ Please generate blog content first!")

if __name__ == "__main__":
    main()
