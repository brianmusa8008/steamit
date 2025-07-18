import streamlit as st
import requests
import json
import os
from datetime import datetime
import re

# Page configuration
st.set_page_config(
    page_title="Blog Template Generator",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2563eb;
        margin-bottom: 2rem;
    }
    .info-box {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .success-box {
        background: #f0f9ff;
        border: 1px solid #0284c7;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background: #fef2f2;
        border: 1px solid #dc2626;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .stButton > button {
        width: 100%;
        background: #2563eb;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    .stButton > button:hover {
        background: #1d4ed8;
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.markdown("<h1 class='main-header'>🚀 Blog Template Generator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b;'>Generate HTML blog templates connected to Google Sheets</p>", unsafe_allow_html=True)

# Sidebar configuration
st.sidebar.header("⚙️ Configuration")

# Google Sheets Configuration
with st.sidebar.expander("📊 Google Sheets Settings", expanded=True):
    api_key = st.text_input("Google Sheets API Key", type="password", help="Your Google Sheets API key")
    spreadsheet_id = st.text_input("Spreadsheet ID", help="The ID of your Google Sheets")
    sheet_name = st.text_input("Sheet Name", value="WEBSITE", help="Name of the sheet to read from")

# Cloudflare Configuration
with st.sidebar.expander("☁️ Cloudflare Settings"):
    cf_api_token = st.text_input("Cloudflare API Token", type="password", help="Your Cloudflare API token")
    cf_zone_id = st.text_input("Zone ID", help="Your Cloudflare zone ID")
    cf_account_id = st.text_input("Account ID", help="Your Cloudflare account ID")

# Blog Configuration
with st.sidebar.expander("📝 Blog Settings", expanded=True):
    blog_title = st.text_input("Blog Title", value="Blog Sederhana", help="Title of your blog")
    blog_description = st.text_area("Blog Description", value="Platform blog yang terhubung dengan Google Sheets", help="Description of your blog")
    blog_keywords = st.text_input("Keywords", value="blog, artikel, google sheets", help="SEO keywords")
    posts_per_page = st.number_input("Posts per Page", min_value=1, max_value=20, value=6)

# Main content area
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Dashboard", "📝 Template Generator", "🚀 Deploy", "📊 Preview"])

with tab1:
    st.header("📊 Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔗 Google Sheets Connection")
        if st.button("Test Google Sheets Connection"):
            if not api_key or not spreadsheet_id:
                st.error("Please provide Google Sheets API Key and Spreadsheet ID")
            else:
                try:
                    # Test connection to Google Sheets
                    url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{sheet_name}!A:Z?key={api_key}"
                    response = requests.get(url)
                    
                    if response.status_code == 200:
                        data = response.json()
                        rows = data.get('values', [])
                        st.success(f"✅ Connected! Found {len(rows)} rows")
                        
                        if rows:
                            st.markdown("**First 5 rows:**")
                            for i, row in enumerate(rows[:5]):
                                st.write(f"Row {i+1}: {row}")
                    else:
                        st.error(f"❌ Connection failed: {response.status_code}")
                        st.json(response.json())
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    with col2:
        st.markdown("### ☁️ Cloudflare Status")
        if st.button("Test Cloudflare Connection"):
            if not cf_api_token or not cf_zone_id:
                st.error("Please provide Cloudflare API Token and Zone ID")
            else:
                try:
                    # Test connection to Cloudflare
                    headers = {
                        'Authorization': f'Bearer {cf_api_token}',
                        'Content-Type': 'application/json'
                    }
                    url = f"https://api.cloudflare.com/client/v4/zones/{cf_zone_id}"
                    response = requests.get(url, headers=headers)
                    
                    if response.status_code == 200:
                        data = response.json()
                        zone_info = data.get('result', {})
                        st.success(f"✅ Connected to zone: {zone_info.get('name', 'Unknown')}")
                        st.json(zone_info)
                    else:
                        st.error(f"❌ Connection failed: {response.status_code}")
                        st.json(response.json())
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

with tab2:
    st.header("🎨 Template Generator")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Generate HTML Template")
        
        # Template options
        template_type = st.selectbox(
            "Template Type",
            ["Blog Homepage", "Single Post", "Category Page", "Archive Page"],
            help="Choose the type of template to generate"
        )
        
        # Design options
        st.markdown("#### Design Options")
        color_scheme = st.selectbox("Color Scheme", ["Blue", "Green", "Purple", "Red", "Orange"])
        layout_style = st.selectbox("Layout Style", ["Modern", "Classic", "Minimal", "Magazine"])
        
        # Generate template button
        if st.button("🎨 Generate Template"):
            # Template generation logic
            template_config = {
                "type": template_type,
                "blog_title": blog_title,
                "blog_description": blog_description,
                "blog_keywords": blog_keywords,
                "color_scheme": color_scheme,
                "layout_style": layout_style,
                "posts_per_page": posts_per_page
            }
            
            # Generate HTML template
            generated_html = generate_html_template(template_config)
            
            st.success("✅ Template generated successfully!")
            
            # Display generated template
            with st.expander("📄 Generated HTML Template", expanded=True):
                st.code(generated_html, language='html')
            
            # Download button
            st.download_button(
                label="📥 Download HTML Template",
                data=generated_html,
                file_name=f"{template_type.lower().replace(' ', '_')}_template.html",
                mime="text/html"
            )
    
    with col2:
        st.markdown("### 📋 Template Preview")
        st.markdown("""
        <div class="info-box">
            <h4>Template Features:</h4>
            <ul>
                <li>✅ Responsive design</li>
                <li>✅ Bootstrap 5 framework</li>
                <li>✅ Font Awesome icons</li>
                <li>✅ Google Sheets integration</li>
                <li>✅ SEO optimized</li>
                <li>✅ Mobile-friendly</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    st.header("🚀 Deployment")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔧 Manual Deploy")
        st.markdown("""
        <div class="info-box">
            <h4>Manual Deployment Steps:</h4>
            <ol>
                <li>Generate your HTML template</li>
                <li>Download the template file</li>
                <li>Upload to your web server</li>
                <li>Configure environment variables</li>
                <li>Test the deployment</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📋 Generate Deployment Guide"):
            deployment_guide = generate_deployment_guide()
            st.markdown("### 📖 Deployment Guide")
            st.markdown(deployment_guide)
    
    with col2:
        st.markdown("### ☁️ Cloudflare Workers Deploy")
        
        # Cloudflare Workers deployment
        if st.button("🚀 Deploy to Cloudflare Workers"):
            if not cf_api_token or not cf_account_id:
                st.error("Please provide Cloudflare API Token and Account ID")
            else:
                try:
                    # Generate worker script
                    worker_script = generate_worker_script({
                        "blog_title": blog_title,
                        "blog_description": blog_description,
                        "api_key": api_key,
                        "spreadsheet_id": spreadsheet_id,
                        "sheet_name": sheet_name
                    })
                    
                    # Deploy to Cloudflare Workers
                    headers = {
                        'Authorization': f'Bearer {cf_api_token}',
                        'Content-Type': 'application/javascript'
                    }
                    
                    url = f"https://api.cloudflare.com/client/v4/accounts/{cf_account_id}/workers/scripts/blog-template"
                    response = requests.put(url, headers=headers, data=worker_script)
                    
                    if response.status_code == 200:
                        st.success("✅ Deployed to Cloudflare Workers successfully!")
                        st.json(response.json())
                    else:
                        st.error(f"❌ Deployment failed: {response.status_code}")
                        st.json(response.json())
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

with tab4:
    st.header("👁️ Preview")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### 🖥️ Blog Preview")
        
        # Load demo data for preview
        demo_data = get_demo_data()
        
        # Display preview
        st.markdown("#### Sample Blog Posts")
        for post in demo_data[:3]:
            with st.container():
                st.markdown(f"**{post['title']}**")
                st.markdown(f"*{post['category']} • {post['date']} • {post['author']}*")
                st.markdown(f"{post['content'][:200]}...")
                st.markdown(f"**Tags:** {post['tags']}")
                st.markdown("---")
    
    with col2:
        st.markdown("### 📊 Statistics")
        
        # Display statistics
        stats = calculate_stats(demo_data)
        st.metric("Total Posts", stats['total_posts'])
        st.metric("Categories", stats['categories'])
        st.metric("Tags", stats['tags'])
        
        st.markdown("### 🔄 Actions")
        if st.button("🔄 Refresh Preview"):
            st.rerun()

def generate_html_template(config):
    """Generate HTML template based on configuration"""
    color_schemes = {
        "Blue": {"primary": "#2563eb", "secondary": "#1d4ed8"},
        "Green": {"primary": "#059669", "secondary": "#047857"},
        "Purple": {"primary": "#7c3aed", "secondary": "#6d28d9"},
        "Red": {"primary": "#dc2626", "secondary": "#b91c1c"},
        "Orange": {"primary": "#ea580c", "secondary": "#c2410c"}
    }
    
    colors = color_schemes.get(config['color_scheme'], color_schemes['Blue'])
    
    # Read the base template
    try:
        with open('blog-template.html', 'r', encoding='utf-8') as f:
            template = f.read()
    except FileNotFoundError:
        # Fallback template if file doesn't exist
        template = """
        <!DOCTYPE html>
        <html lang="id">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{{blog_title}}</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
                <div class="container">
                    <a class="navbar-brand" href="#">{{blog_title}}</a>
                </div>
            </nav>
            <div class="container mt-4">
                <h1>{{blog_title}}</h1>
                <p>{{blog_description}}</p>
            </div>
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
        </body>
        </html>
        """
    
    # Replace template variables
    template = template.replace('{{site_title}}', config['blog_title'])
    template = template.replace('{{site_description}}', config['blog_description'])
    template = template.replace('{{site_keywords}}', config['blog_keywords'])
    template = template.replace('{{current_year}}', str(datetime.now().year))
    
    # Replace color scheme
    template = template.replace('--primary-color: #2563eb', f'--primary-color: {colors["primary"]}')
    template = template.replace('#1d4ed8', colors["secondary"])
    
    return template

def generate_deployment_guide():
    """Generate deployment guide"""
    return """
    ## 🚀 Deployment Guide
    
    ### Prerequisites
    - Web server (Apache/Nginx)
    - Domain name
    - SSL certificate
    
    ### Steps
    1. **Upload Files**
       - Upload HTML template to your web server
       - Ensure proper file permissions
    
    2. **Configure Environment**
       - Set up environment variables
       - Configure Google Sheets API
       - Set up Cloudflare if using
    
    3. **Test Deployment**
       - Check all links work
       - Test Google Sheets connection
       - Verify responsive design
    
    4. **Go Live**
       - Point domain to your server
       - Enable SSL
       - Monitor for errors
    
    ### Environment Variables
    ```bash
    GOOGLE_SHEETS_API_KEY=your_api_key_here
    SPREADSHEET_ID=your_spreadsheet_id
    SHEET_NAME=WEBSITE
    ```
    
    ### Troubleshooting
    - Check API key permissions
    - Verify spreadsheet sharing settings
    - Test network connectivity
    """

def generate_worker_script(config):
    """Generate Cloudflare Workers script"""
    return f"""
    addEventListener('fetch', event => {{
        event.respondWith(handleRequest(event.request))
    }})

    async function handleRequest(request) {{
        const url = new URL(request.url)
        
        if (url.pathname === '/') {{
            return new Response(HTML_TEMPLATE, {{
                headers: {{ 'Content-Type': 'text/html' }}
            }})
        }}
        
        if (url.pathname === '/api/posts') {{
            const posts = await getGoogleSheetsData()
            return new Response(JSON.stringify({{ success: true, posts }}), {{
                headers: {{ 'Content-Type': 'application/json' }}
            }})
        }}
        
        return new Response('Not Found', {{ status: 404 }})
    }}

    async function getGoogleSheetsData() {{
        const API_KEY = '{config['api_key']}'
        const SPREADSHEET_ID = '{config['spreadsheet_id']}'
        const SHEET_NAME = '{config['sheet_name']}'
        
        const url = `https://sheets.googleapis.com/v4/spreadsheets/${{SPREADSHEET_ID}}/values/${{SHEET_NAME}}!A:Z?key=${{API_KEY}}`
        
        try {{
            const response = await fetch(url)
            const data = await response.json()
            return data.values || []
        }} catch (error) {{
            console.error('Error fetching data:', error)
            return []
        }}
    }}

    const HTML_TEMPLATE = `
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{config['blog_title']}</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
            <div class="container">
                <a class="navbar-brand" href="#">{config['blog_title']}</a>
            </div>
        </nav>
        <div class="container mt-4">
            <h1>{config['blog_title']}</h1>
            <p>{config['blog_description']}</p>
            <div id="posts"></div>
        </div>
        <script>
            fetch('/api/posts')
                .then(response => response.json())
                .then(data => {{
                    const postsDiv = document.getElementById('posts')
                    data.posts.forEach(post => {{
                        const postDiv = document.createElement('div')
                        postDiv.className = 'card mb-3'
                        postDiv.innerHTML = `
                            <div class="card-body">
                                <h5 class="card-title">${{post[0]}}</h5>
                                <p class="card-text">${{post[1]}}</p>
                            </div>
                        `
                        postsDiv.appendChild(postDiv)
                    }})
                }})
        </script>
    </body>
    </html>
    `
    """

def get_demo_data():
    """Get demo data for preview"""
    return [
        {
            "id": 1,
            "title": "Cara Membuat Blog dengan Google Sheets",
            "content": "Panduan lengkap untuk membuat blog sederhana yang terhubung dengan Google Sheets sebagai database.",
            "category": "Tutorial",
            "tags": "blog, google sheets, tutorial",
            "author": "Admin",
            "date": "2025-01-18"
        },
        {
            "id": 2,
            "title": "Optimasi SEO untuk Blog",
            "content": "Tips dan trik untuk mengoptimalkan SEO blog Anda agar lebih mudah ditemukan di mesin pencari.",
            "category": "SEO",
            "tags": "seo, optimasi, blog",
            "author": "Admin",
            "date": "2025-01-17"
        },
        {
            "id": 3,
            "title": "Deploy ke Cloudflare Workers",
            "content": "Panduan step-by-step untuk deploy blog Anda ke Cloudflare Workers secara gratis.",
            "category": "Deployment",
            "tags": "cloudflare, workers, deploy",
            "author": "Admin",
            "date": "2025-01-16"
        }
    ]

def calculate_stats(data):
    """Calculate statistics from data"""
    categories = set(post['category'] for post in data)
    tags = set()
    for post in data:
        post_tags = post['tags'].split(',')
        tags.update(tag.strip() for tag in post_tags)
    
    return {
        'total_posts': len(data),
        'categories': len(categories),
        'tags': len(tags)
    }

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748b; padding: 2rem 0;'>
    <p>🚀 Blog Template Generator - Powered by Streamlit</p>
    <p>Generate beautiful blog templates connected to Google Sheets</p>
</div>
""", unsafe_allow_html=True)