# Google Sheets Real-time Web Application

## Overview
This project has evolved from converting Google Apps Script files to creating a comprehensive blog template system that connects to Google Sheets for content management. The system includes a complete HTML blog template, Express.js server, Streamlit Python app for template generation, and Cloudflare Workers deployment script.

## Project Structure

### Sample Folder
- Contains the original encrypted/obfuscated Google Apps Script files
- Includes Excel spreadsheets and JavaScript files
- These files are in an encrypted format and not directly readable

### Script Folder
- Contains the unencrypted, readable versions of the Google Apps Script files
- All files have been converted to clean, well-documented JavaScript code

## Files Converted

### Core Files
- **Code.js**: Main Google Apps Script functions for spreadsheet operations
- **api-appscript-db.js**: API and database handling functions
- **analisdata.js**: Data analysis and validation functions
- **buildgs.js**: Build and deployment functions
- **generateARTIKEL.js**: Article generation using AI APIs
- **generateJUDUL.js**: Title generation functions
- **generateLABEL.js**: Label and tag generation functions
- **generateMETA.js**: Meta description generation functions
- **indexing.js**: Google Search Console indexing functions

## Key Features

### Real-time Dashboard
- Live connection to Google Sheets via API
- Auto-refresh every 30 seconds
- Responsive design for desktop and mobile
- Modern UI with Bootstrap 5 and Font Awesome

### Data Management
- View and filter spreadsheet data
- Search functionality across all columns
- Pagination for large datasets
- Status-based filtering (success, error, pending)

### Interactive Features
- Real-time statistics display
- Connection status indicator
- Manual refresh capability
- Data export capabilities

### Deployment Options
- Cloudflare Workers for production (index.js)
- Local Express.js server for development (server.js)
- Environment variable configuration
- Cross-platform compatibility

## Recent Changes
- **2025-01-18**: Created comprehensive blog template system with Google Sheets integration
- **2025-01-18**: Built complete blog HTML template with responsive design and Bootstrap 5
- **2025-01-18**: Implemented blog server (blog-server.js) with API endpoints for posts, categories, tags
- **2025-01-18**: Created Streamlit Python app for template generation and deployment management
- **2025-01-18**: Added Cloudflare Workers script for serverless blog deployment
- **2025-01-18**: Generated comprehensive deployment guide and spreadsheet structure documentation
- **2025-01-18**: Configured workflows for Blog Server and Streamlit App with proper port management
- **2025-01-18**: Added direct Google Sheets connection (no API key required) with CSV export method
- **2025-01-18**: Updated spreadsheet ID to user's specific sheet (14K69q8SMd3pCAROB1YQMDrmuw8y6QphxAslF_y-3NrM)
- **2025-01-18**: Created sample spreadsheet data (.xlsx and .csv) with import guide
- **2025-01-18**: Implemented Cloudflare API integration with random name generation and workflow management
- **2025-01-18**: Added comprehensive CloudflareManager class with auto-deployment features
- **2025-01-18**: MAJOR UPDATE: Completely removed Google Sheets API key dependency - uses only direct CSV connection
- **2025-01-18**: Fixed direct connection with multiple URL format attempts for reliable data access
- **2025-01-18**: Successfully connected to user's spreadsheet (10 posts loaded) without API keys
- **2025-01-18**: Simplified Cloudflare configuration to use Workers AI API Token + Account ID only (removed Zone ID)
- **2025-01-18**: Updated Streamlit app to reflect API-key-free Google Sheets and simplified Cloudflare Workers AI setup

## User Preferences
- Language: Indonesian communication preferred
- File format: Clean, readable JavaScript with comprehensive comments
- Code style: Professional with error handling and logging
- Documentation: Detailed function descriptions and usage examples

## Technical Details

### Dependencies
- Node.js with Express.js for local development
- Google Sheets API v4 for data access
- Bootstrap 5 for responsive UI
- Font Awesome for icons
- Wrangler for Cloudflare Workers deployment

### Configuration
- Environment variables for API keys and settings
- Configurable sheet names (default: 'WEBSITE')
- CORS headers for cross-origin requests
- Auto-refresh intervals and pagination settings
- Demo data mode for development

### Usage
1. Open Google Apps Script editor
2. Create new project or open existing one
3. Copy functions from Script folder files
4. Configure API keys in Script Properties
5. Run desired functions from the editor

## Security Notes
- All sensitive data (API keys) stored in Script Properties
- Input validation implemented
- Rate limiting to prevent quota exhaustion
- Error handling to prevent data loss

## Future Enhancements
- Additional AI model integration
- Advanced SEO analysis features
- Bulk processing optimizations
- Real-time monitoring dashboard

## Support
- All functions include comprehensive error handling
- Logging implemented for debugging
- Progress notifications for long-running operations
- Validation functions for data integrity