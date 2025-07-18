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

# Configuration file path
CONFIG_FILE = "app_config.json"

# Load saved configuration
def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

# Save configuration
def save_config(config):
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        st.error(f"Error saving configuration: {e}")

# Load existing configuration
config = load_config()

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

# Google Sheets Configuration (Direct Connection - No API Key Required)
with st.sidebar.expander("📊 Google Sheets Settings", expanded=True):
    st.info("🔥 Direct connection - No API key required!")
    spreadsheet_id = st.text_input("Spreadsheet ID", value=config.get("spreadsheet_id", "14K69q8SMd3pCAROB1YQMDrmuw8y6QphxAslF_y-3NrM"), help="The ID of your Google Sheets")
    sheet_name = st.text_input("Sheet Name", value=config.get("sheet_name", "WEBSITE"), help="Name of the sheet to read from")
    st.markdown("**Note:** Spreadsheet must be set to public/editor access")

# Cloudflare Workers AI Configuration
with st.sidebar.expander("☁️ Cloudflare Workers AI Settings"):
    cf_api_token = st.text_input("Cloudflare Workers AI API Token", type="password", value=config.get("cf_api_token", ""), help="Your Cloudflare Workers AI API token")
    cf_account_id = st.text_input("Cloudflare Account ID", value=config.get("cf_account_id", ""), help="Your Cloudflare account ID")
    
    st.markdown("""
    **How to get your credentials:**
    1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com/)
    2. Click on your profile → My Profile → API Tokens
    3. Create token with these permissions:
       - **Account**: Cloudflare Workers:Edit
       - **Zone**: Zone:Read (if deploying to custom domain)
    4. Copy your Account ID from the right sidebar
    
    **Important**: The token must have Account-level permissions, not just Zone-level!
    """)
    
    st.info("💡 Uses Workers AI API - no Zone ID required")
    
    # Worker name options
    worker_name_prefix = st.text_input("Worker Name Prefix", value=config.get("worker_name_prefix", "blog"), help="Prefix for worker name")
    auto_generate_name = st.checkbox("Auto-generate available name", value=config.get("auto_generate_name", True), help="Automatically generate available worker name")

# Auto-save indicator
if os.path.exists(CONFIG_FILE):
    st.sidebar.success("🔄 Auto-save aktif - Data tersimpan")

# Blog Configuration
with st.sidebar.expander("📝 Blog Settings", expanded=True):
    blog_title = st.text_input("Blog Title", value=config.get("blog_title", "Blog Sederhana"), help="Title of your blog")
    blog_description = st.text_area("Blog Description", value=config.get("blog_description", "Platform blog yang terhubung dengan Google Sheets"), help="Description of your blog")
    blog_keywords = st.text_input("Keywords", value=config.get("blog_keywords", "blog, artikel, google sheets"), help="SEO keywords")
    posts_per_page = st.number_input("Posts per Page", min_value=1, max_value=20, value=config.get("posts_per_page", 6))

# Auto-save configuration when values change
current_config = {
    "spreadsheet_id": spreadsheet_id,
    "sheet_name": sheet_name,
    "cf_api_token": cf_api_token,
    "cf_account_id": cf_account_id,
    "worker_name_prefix": worker_name_prefix,
    "auto_generate_name": auto_generate_name,
    "blog_title": blog_title,
    "blog_description": blog_description,
    "blog_keywords": blog_keywords,
    "posts_per_page": posts_per_page
}

# Save configuration if changed
if current_config != config:
    save_config(current_config)
    config = current_config

# Main content area
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Dashboard", "📝 Template Generator", "🚀 Deploy", "📊 Preview"])

with tab1:
    st.header("📊 Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔗 Google Sheets Connection")
        if st.button("Test Google Sheets Connection"):
            if not spreadsheet_id:
                st.error("Please provide Spreadsheet ID")
            else:
                try:
                    # Try direct connection (no API key needed)
                    st.info("Testing direct connection...")
                    
                    # Try multiple URL formats
                    urls = [
                        f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid=0",
                        f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv",
                        f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/gviz/tq?tqx=out:csv"
                    ]
                    
                    success = False
                    for url in urls:
                        try:
                            csv_response = requests.get(url)
                            if csv_response.status_code == 200 and not csv_response.text.startswith('<!DOCTYPE'):
                                csv_data = csv_response.text
                                lines = csv_data.split('\n')
                                
                                st.success(f"✅ Direct connection successful! Found {len(lines)} rows")
                                
                                if lines:
                                    st.markdown("**First 5 rows:**")
                                    for i, line in enumerate(lines[:5]):
                                        st.write(f"Row {i+1}: {line}")
                                success = True
                                break
                        except Exception as e:
                            continue
                    
                    if not success:
                        st.error("❌ Direct connection failed - make sure spreadsheet is public/editor access")
                        
                        # Remove API key fallback - not needed anymore
                        st.info("Make sure your Google Sheets is set to public or editor access")
                            
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    with col2:
        st.markdown("### ☁️ Cloudflare Workers AI Status")
        if st.button("Test Cloudflare Workers AI Connection"):
            if not cf_api_token or not cf_account_id:
                st.error("Please provide Cloudflare Workers AI API Token and Account ID")
            else:
                try:
                    # Test connection to Cloudflare token first
                    headers = {
                        'Authorization': f'Bearer {cf_api_token}',
                        'Content-Type': 'application/json'
                    }
                    
                    # First verify the token is valid
                    verify_url = "https://api.cloudflare.com/client/v4/user/tokens/verify"
                    verify_response = requests.get(verify_url, headers=headers)
                    
                    if verify_response.status_code == 200:
                        verify_data = verify_response.json()
                        if verify_data.get('success'):
                            st.success("✅ API Token is valid and active")
                            
                            # Try to list workers (this requires Workers:Edit permission)
                            workers_url = f"https://api.cloudflare.com/client/v4/accounts/{cf_account_id}/workers/scripts"
                            workers_response = requests.get(workers_url, headers=headers)
                            
                            if workers_response.status_code == 200:
                                workers_data = workers_response.json()
                                workers = workers_data.get('result', [])
                                st.success(f"✅ Connected to Cloudflare Workers! Found {len(workers)} workers")
                                
                                if workers:
                                    st.markdown("**Existing Workers:**")
                                    for worker in workers[:5]:
                                        st.write(f"- {worker.get('id', 'Unknown')}")
                                else:
                                    st.info("No existing workers found - ready to deploy new ones!")
                            else:
                                st.warning(f"⚠️ Token valid but lacks Workers permission (Error {workers_response.status_code})")
                                
                                # Show detailed error and fix instructions
                                if workers_response.status_code == 403:
                                    st.error("**Permission Error:** Token needs Workers:Edit permission")
                                    st.markdown("""
                                    **Required Steps:**
                                    1. Go to [Cloudflare API Tokens](https://dash.cloudflare.com/profile/api-tokens)
                                    2. Edit your existing token or create a new one
                                    3. Add these permissions:
                                       - **Account**: Cloudflare Workers:Edit
                                       - **Account**: Account:Read  
                                    4. Make sure Account ID is included in the scope
                                    5. Save and use the new token
                                    """)
                                else:
                                    st.json(workers_response.json())
                        else:
                            st.error("❌ Invalid API token")
                    else:
                        st.error(f"❌ Token verification failed: {verify_response.status_code}")
                        st.json(verify_response.json())
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.markdown("""
                    **Common Issues:**
                    - Check internet connection
                    - Verify API token format
                    - Ensure account ID is correct (32-character hex string)
                    """)

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
        
        # Worker name generation
        if auto_generate_name:
            st.info("Worker name will be auto-generated for availability")
        else:
            custom_worker_name = st.text_input("Custom Worker Name", help="Enter custom worker name")
        
        # Deploy button
        if st.button("🚀 Deploy to Cloudflare Workers"):
            if not cf_api_token or not cf_account_id:
                st.error("Please provide Cloudflare Workers AI API Token and Account ID")
            elif not spreadsheet_id:
                st.error("Please provide Spreadsheet ID")
            else:
                try:
                    with st.spinner("Deploying to Cloudflare Workers..."):
                        # Import cloudflare manager (simulated)
                        from datetime import datetime
                        import random
                        
                        # Generate worker name
                        if auto_generate_name:
                            adjectives = ['amazing', 'brilliant', 'clever', 'dynamic', 'elegant', 'fantastic']
                            nouns = ['blog', 'site', 'portal', 'hub', 'space', 'platform']
                            adjective = random.choice(adjectives)
                            noun = random.choice(nouns)
                            random_num = random.randint(100, 999)
                            worker_name = f"{worker_name_prefix}-{adjective}-{noun}-{random_num}"
                        else:
                            worker_name = custom_worker_name or f"{worker_name_prefix}-{random.randint(1000, 9999)}"
                        
                        # Generate worker script
                        worker_config = {
                            "spreadsheetId": spreadsheet_id,
                            "sheetName": sheet_name,
                            "blogTitle": blog_title,
                            "blogDescription": blog_description,
                            "blogKeywords": blog_keywords
                        }
                        
                        # Deploy to Cloudflare Workers
                        headers = {
                            'Authorization': f'Bearer {cf_api_token}',
                            'Content-Type': 'application/javascript'
                        }
                        
                        # Generate the worker script
                        worker_script = generate_cloudflare_worker_script(worker_config)
                        
                        # Deploy API call
                        deploy_url = f"https://api.cloudflare.com/client/v4/accounts/{cf_account_id}/workers/scripts/{worker_name}"
                        response = requests.put(deploy_url, headers=headers, data=worker_script)
                        
                        if response.status_code in [200, 201]:
                            result = response.json()
                            st.success(f"✅ Successfully deployed to Cloudflare Workers!")
                            
                            # Display deployment info
                            st.info(f"**Worker Name:** {worker_name}")
                            st.info(f"**URL:** https://{worker_name}.{cf_account_id}.workers.dev")
                            
                            # Show deployment details
                            with st.expander("Deployment Details"):
                                st.json(result)
                            
                            # Set environment variables if needed
                            if st.button("Set Environment Variables"):
                                env_vars = {
                                    'SPREADSHEET_ID': spreadsheet_id,
                                    'SHEET_NAME': sheet_name
                                }
                                
                                env_url = f"https://api.cloudflare.com/client/v4/accounts/{cf_account_id}/workers/scripts/{worker_name}/settings"
                                env_response = requests.patch(env_url, headers=headers, json={
                                    "bindings": [
                                        {"type": "plain_text", "name": "SPREADSHEET_ID", "text": spreadsheet_id},
                                        {"type": "plain_text", "name": "SHEET_NAME", "text": sheet_name}
                                    ]
                                })
                                
                                if env_response.status_code == 200:
                                    st.success("✅ Environment variables set successfully!")
                                else:
                                    st.error("❌ Failed to set environment variables")
                                    st.json(env_response.json())
                            
                        else:
                            st.error(f"❌ Deployment failed: {response.status_code}")
                            error_data = response.json()
                            st.json(error_data)
                            
                            # Show error details
                            if 'errors' in error_data:
                                for error in error_data['errors']:
                                    st.error(f"Error: {error.get('message', 'Unknown error')}")
                        
                except Exception as e:
                    st.error(f"❌ Error during deployment: {str(e)}")
                    st.exception(e)
        
        # List existing workers
        if st.button("📋 List Existing Workers"):
            if cf_api_token and cf_account_id:
                try:
                    headers = {
                        'Authorization': f'Bearer {cf_api_token}',
                        'Content-Type': 'application/json'
                    }
                    
                    list_url = f"https://api.cloudflare.com/client/v4/accounts/{cf_account_id}/workers/scripts"
                    response = requests.get(list_url, headers=headers)
                    
                    if response.status_code == 200:
                        data = response.json()
                        workers = data.get('result', [])
                        
                        if workers:
                            st.success(f"Found {len(workers)} workers:")
                            for worker in workers:
                                st.write(f"- **{worker.get('id', 'Unknown')}** (Created: {worker.get('created_on', 'Unknown')})")
                        else:
                            st.info("No workers found in this account")
                    else:
                        st.error(f"Failed to list workers: {response.status_code}")
                        st.json(response.json())
                        
                except Exception as e:
                    st.error(f"Error listing workers: {str(e)}")
            else:
                st.error("Please provide Cloudflare API Token and Account ID")


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
            
        st.markdown("### 📁 Configuration")
        st.json(current_config)
        
        if st.button("💾 Save Config"):
            save_config(current_config)
            st.success("Configuration saved!")
            
        if st.button("🗑️ Clear Config"):
            if os.path.exists(CONFIG_FILE):
                os.remove(CONFIG_FILE)
                st.success("Configuration cleared!")
            else:
                st.info("No config file found")

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

def generate_cloudflare_worker_script(config):
    """Generate Cloudflare Workers script with direct Google Sheets connection"""
    spreadsheet_id = config.get('spreadsheetId', '')
    sheet_name = config.get('sheetName', 'Sheet1')
    blog_title = config.get('blogTitle', 'Blog')
    blog_description = config.get('blogDescription', 'Blog powered by Google Sheets')
    blog_keywords = config.get('blogKeywords', 'blog, google sheets')
    
    return f"""// Auto-generated Cloudflare Worker Script
// Generated on: {datetime.now().isoformat()}
// Spreadsheet ID: {spreadsheet_id}

addEventListener('fetch', event => {{
    event.respondWith(handleRequest(event.request))
}})

async function handleRequest(request) {{
    const url = new URL(request.url)
    
    // CORS headers
    const corsHeaders = {{
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    }}
    
    // Handle CORS preflight
    if (request.method === 'OPTIONS') {{
        return new Response(null, {{ headers: corsHeaders }})
    }}
    
    try {{
        let response
        
        // Route handling
        switch (url.pathname) {{
            case '/':
                response = await serveBlogHome()
                break
            case '/api/posts':
                response = await getPosts()
                break
            case '/api/categories':
                response = await getCategories()
                break
            case '/api/tags':
                response = await getTags()
                break
            case '/api/stats':
                response = await getStats()
                break
            case '/health':
                response = new Response(JSON.stringify({{ 
                    status: 'healthy', 
                    timestamp: new Date().toISOString(),
                    spreadsheetId: SPREADSHEET_ID 
                }}), {{
                    headers: {{ 'Content-Type': 'application/json' }}
                }})
                break
            default:
                if (url.pathname.startsWith('/post/')) {{
                    response = await getPost(url.pathname.split('/')[2])
                }} else if (url.pathname.startsWith('/api/post/')) {{
                    response = await getPostAPI(url.pathname.split('/')[3])
                }} else {{
                    response = new Response('Not Found', {{ status: 404 }})
                }}
                break
        }}
        
        // Add CORS headers to response
        Object.entries(corsHeaders).forEach(([key, value]) => {{
            response.headers.set(key, value)
        }})
        
        return response
    }} catch (error) {{
        console.error('Error handling request:', error)
        return new Response(JSON.stringify({{ 
            success: false, 
            error: error.message 
        }}), {{ 
            status: 500,
            headers: {{ 
                'Content-Type': 'application/json',
                ...corsHeaders 
            }}
        }})
    }}
}}

// Configuration
const SPREADSHEET_ID = '{spreadsheet_id}'
const SHEET_NAME = '{sheet_name}'
const BLOG_CONFIG = {{
    site_title: '{blog_title}',
    site_description: '{blog_description}',
    site_keywords: '{blog_keywords}',
    current_year: new Date().getFullYear()
}}

// Direct Google Sheets data fetching (no API key required)
async function getGoogleSheetsData() {{
    try {{
        const csvUrl = `https://docs.google.com/spreadsheets/d/${{SPREADSHEET_ID}}/export?format=csv&gid=0`
        const response = await fetch(csvUrl)
        
        if (!response.ok) {{
            throw new Error(`HTTP error! status: ${{response.status}}`)
        }}
        
        const csvText = await response.text()
        return csvToJson(csvText)
    }} catch (error) {{
        console.error('Error fetching Google Sheets data:', error)
        return getDemoData()
    }}
}}

// Convert CSV to JSON
function csvToJson(csvText) {{
    const lines = csvText.split('\\n')
    const headers = lines[0].split(',').map(header => header.trim().replace(/"/g, ''))
    const data = []

    for (let i = 1; i < lines.length; i++) {{
        const values = parseCSVLine(lines[i])
        if (values.length === headers.length) {{
            const obj = {{}}
            headers.forEach((header, index) => {{
                obj[header.toLowerCase()] = values[index] || ''
            }})
            
            // Ensure required fields
            if (!obj.id) obj.id = i
            if (!obj.slug && obj.title) {{
                obj.slug = obj.title.toLowerCase()
                    .replace(/[^a-z0-9\\s-]/g, '')
                    .replace(/\\s+/g, '-')
                    .trim()
            }}
            
            data.push(obj)
        }}
    }}

    return data
}}

// Parse CSV line with proper comma handling
function parseCSVLine(line) {{
    const values = []
    let current = ''
    let inQuotes = false
    
    for (let i = 0; i < line.length; i++) {{
        const char = line[i]
        
        if (char === '"') {{
            inQuotes = !inQuotes
        }} else if (char === ',' && !inQuotes) {{
            values.push(current.trim().replace(/"/g, ''))
            current = ''
        }} else {{
            current += char
        }}
    }}
    
    values.push(current.trim().replace(/"/g, ''))
    return values
}}

// Demo data fallback
function getDemoData() {{
    return [
        {{
            id: 1,
            title: 'Welcome to Your Blog',
            slug: 'welcome-to-your-blog',
            content: 'This is your first blog post powered by Google Sheets and Cloudflare Workers. Edit your Google Sheets to add more content!',
            category: 'Welcome',
            tags: 'blog, welcome, cloudflare, google sheets',
            author: 'Admin',
            date: new Date().toISOString().split('T')[0],
            status: 'published'
        }}
    ]
}}

// Serve blog home page
async function serveBlogHome() {{
    const html = `
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>${{BLOG_CONFIG.site_title}}</title>
        <meta name="description" content="${{BLOG_CONFIG.site_description}}">
        <meta name="keywords" content="${{BLOG_CONFIG.site_keywords}}">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
            .navbar {{ background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); }}
            .hero {{ background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); color: white; padding: 4rem 0; }}
            .card {{ border: none; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: transform 0.3s; }}
            .card:hover {{ transform: translateY(-5px); }}
            .btn-primary {{ background: #2563eb; border-color: #2563eb; }}
            .btn-primary:hover {{ background: #1d4ed8; border-color: #1d4ed8; }}
            .loading {{ text-align: center; padding: 2rem; }}
        </style>
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-dark">
            <div class="container">
                <a class="navbar-brand" href="/"><i class="fas fa-blog me-2"></i>${{BLOG_CONFIG.site_title}}</a>
                <div class="navbar-nav ms-auto">
                    <a class="nav-link" href="/">Home</a>
                    <a class="nav-link" href="/api/posts">API</a>
                    <a class="nav-link" href="/health">Health</a>
                </div>
            </div>
        </nav>
        
        <div class="hero text-center">
            <div class="container">
                <h1 class="display-4">${{BLOG_CONFIG.site_title}}</h1>
                <p class="lead">${{BLOG_CONFIG.site_description}}</p>
                <p><small>Powered by Google Sheets & Cloudflare Workers</small></p>
            </div>
        </div>
        
        <div class="container mt-5">
            <div class="row">
                <div class="col-lg-8">
                    <div id="posts" class="row">
                        <div class="col-12 loading">
                            <i class="fas fa-spinner fa-spin fa-2x"></i>
                            <p>Loading posts...</p>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4">
                    <div class="card">
                        <div class="card-body">
                            <h5><i class="fas fa-info-circle me-2"></i>About This Blog</h5>
                            <p>${{BLOG_CONFIG.site_description}}</p>
                            <p><small><strong>Data Source:</strong> Google Sheets</small></p>
                            <p><small><strong>Spreadsheet ID:</strong> ${{SPREADSHEET_ID}}</small></p>
                            <p><small><strong>Last Updated:</strong> <span id="lastUpdated">Loading...</span></small></p>
                        </div>
                    </div>
                    
                    <div class="card mt-3">
                        <div class="card-body">
                            <h5><i class="fas fa-chart-bar me-2"></i>Statistics</h5>
                            <div id="stats">
                                <p><i class="fas fa-spinner fa-spin"></i> Loading stats...</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <footer class="bg-dark text-white mt-5 py-4">
            <div class="container text-center">
                <p>&copy; ${{BLOG_CONFIG.current_year}} ${{BLOG_CONFIG.site_title}}. Powered by Cloudflare Workers & Google Sheets.</p>
                <p><small>Generated by Blog Template System</small></p>
            </div>
        </footer>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            // Update last updated time
            document.getElementById('lastUpdated').textContent = new Date().toLocaleString('id-ID');
            
            // Load posts
            async function loadPosts() {{
                try {{
                    const response = await fetch('/api/posts')
                    const data = await response.json()
                    
                    if (data.success) {{
                        const posts = data.posts || []
                        const postsContainer = document.getElementById('posts')
                        
                        if (posts.length === 0) {{
                            postsContainer.innerHTML = '<div class="col-12 text-center"><p>No posts found. Add content to your Google Sheets!</p></div>'
                            return
                        }}
                        
                        postsContainer.innerHTML = posts.map(post => `
                            <div class="col-md-6 mb-4">
                                <div class="card">
                                    <div class="card-body">
                                        <h5 class="card-title">${{post.title}}</h5>
                                        <p class="card-text">${{(post.content || '').substring(0, 150)}}...</p>
                                        <div class="d-flex justify-content-between align-items-center">
                                            <small class="text-muted">${{post.category || 'Uncategorized'}} • ${{post.date}}</small>
                                            <a href="/post/${{post.slug}}" class="btn btn-primary btn-sm">Read More</a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        `).join('')
                    }} else {{
                        document.getElementById('posts').innerHTML = '<div class="col-12 text-center"><p>Error loading posts</p></div>'
                    }}
                }} catch (error) {{
                    console.error('Error loading posts:', error)
                    document.getElementById('posts').innerHTML = '<div class="col-12 text-center"><p>Failed to load posts</p></div>'
                }}
            }}
            
            // Load statistics
            async function loadStats() {{
                try {{
                    const response = await fetch('/api/stats')
                    const data = await response.json()
                    
                    if (data.success) {{
                        const stats = data.stats
                        document.getElementById('stats').innerHTML = `
                            <p><i class="fas fa-file-alt me-2"></i>Posts: ${{stats.totalPosts}}</p>
                            <p><i class="fas fa-folder me-2"></i>Categories: ${{stats.totalCategories}}</p>
                            <p><i class="fas fa-tags me-2"></i>Tags: ${{stats.totalTags}}</p>
                        `
                    }}
                }} catch (error) {{
                    console.error('Error loading stats:', error)
                    document.getElementById('stats').innerHTML = '<p>Error loading statistics</p>'
                }}
            }}
            
            // Initialize
            loadPosts()
            loadStats()
        </script>
    </body>
    </html>
    `
    
    return new Response(html, {{
        headers: {{ 'Content-Type': 'text/html' }}
    }})
}}

// API endpoints
async function getPosts() {{
    const posts = await getGoogleSheetsData()
    const publishedPosts = posts.filter(post => post.status === 'published' || !post.status)
    
    return new Response(JSON.stringify({{
        success: true,
        posts: publishedPosts,
        total: publishedPosts.length
    }}), {{
        headers: {{ 'Content-Type': 'application/json' }}
    }})
}}

async function getCategories() {{
    const posts = await getGoogleSheetsData()
    const categories = {{}}
    
    posts.forEach(post => {{
        const category = post.category || 'Uncategorized'
        categories[category] = (categories[category] || 0) + 1
    }})
    
    return new Response(JSON.stringify({{
        success: true,
        categories: categories
    }}), {{
        headers: {{ 'Content-Type': 'application/json' }}
    }})
}}

async function getTags() {{
    const posts = await getGoogleSheetsData()
    const tags = {{}}
    
    posts.forEach(post => {{
        const postTags = post.tags ? post.tags.split(',').map(tag => tag.trim()) : []
        postTags.forEach(tag => {{
            if (tag) tags[tag] = (tags[tag] || 0) + 1
        }})
    }})
    
    return new Response(JSON.stringify({{
        success: true,
        tags: tags
    }}), {{
        headers: {{ 'Content-Type': 'application/json' }}
    }})
}}

async function getStats() {{
    const posts = await getGoogleSheetsData()
    const categories = new Set(posts.map(post => post.category || 'Uncategorized'))
    const tags = new Set()
    
    posts.forEach(post => {{
        const postTags = post.tags ? post.tags.split(',').map(tag => tag.trim()) : []
        postTags.forEach(tag => {{
            if (tag) tags.add(tag)
        }})
    }})
    
    return new Response(JSON.stringify({{
        success: true,
        stats: {{
            totalPosts: posts.length,
            totalCategories: categories.size,
            totalTags: tags.size,
            publishedPosts: posts.filter(p => p.status === 'published' || !p.status).length
        }}
    }}), {{
        headers: {{ 'Content-Type': 'application/json' }}
    }})
}}

async function getPost(slug) {{
    const posts = await getGoogleSheetsData()
    const post = posts.find(p => p.slug === slug)
    
    if (!post) {{
        return new Response('Post not found', {{ status: 404 }})
    }}
    
    const html = `
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>${{post.title}} - ${{BLOG_CONFIG.site_title}}</title>
        <meta name="description" content="${{(post.content || '').substring(0, 160)}}">
        <meta name="keywords" content="${{post.tags}}">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
            .navbar {{ background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); }}
            .hero {{ background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); color: white; padding: 4rem 0; }}
            .post-content {{ line-height: 1.8; font-size: 1.1rem; }}
        </style>
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-dark">
            <div class="container">
                <a class="navbar-brand" href="/"><i class="fas fa-blog me-2"></i>${{BLOG_CONFIG.site_title}}</a>
                <div class="navbar-nav ms-auto">
                    <a class="nav-link" href="/">Home</a>
                </div>
            </div>
        </nav>
        
        <div class="hero text-center">
            <div class="container">
                <h1 class="display-4">${{post.title}}</h1>
                <p class="lead">${{post.category || 'Uncategorized'}} • ${{post.date}} • ${{post.author || 'Admin'}}</p>
            </div>
        </div>
        
        <div class="container mt-5">
            <div class="row">
                <div class="col-lg-8 mx-auto">
                    <div class="post-content">
                        ${{(post.content || '').replace(/\\n/g, '<br>')}}
                    </div>
                    
                    <div class="mt-4">
                        <h6>Tags:</h6>
                        ${{(post.tags || '').split(',').map(tag => `<span class="badge bg-primary me-1">${{tag.trim()}}</span>`).join('')}}
                    </div>
                    
                    <div class="mt-4">
                        <a href="/" class="btn btn-outline-primary">
                            <i class="fas fa-arrow-left me-2"></i>Back to Blog
                        </a>
                    </div>
                </div>
            </div>
        </div>
        
        <footer class="bg-dark text-white mt-5 py-4">
            <div class="container text-center">
                <p>&copy; ${{BLOG_CONFIG.current_year}} ${{BLOG_CONFIG.site_title}}. Powered by Cloudflare Workers.</p>
            </div>
        </footer>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    `
    
    return new Response(html, {{
        headers: {{ 'Content-Type': 'text/html' }}
    }})
}}

async function getPostAPI(slug) {{
    const posts = await getGoogleSheetsData()
    const post = posts.find(p => p.slug === slug)
    
    if (!post) {{
        return new Response(JSON.stringify({{
            success: false,
            message: 'Post not found'
        }}), {{
            status: 404,
            headers: {{ 'Content-Type': 'application/json' }}
        }})
    }}
    
    return new Response(JSON.stringify({{
        success: true,
        post: post
    }}), {{
        headers: {{ 'Content-Type': 'application/json' }}
    }})
}}"""

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