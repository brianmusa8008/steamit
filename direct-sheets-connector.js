// Direct Google Sheets Connector - No API Key Required
// Uses public CSV export feature from Google Sheets

class DirectSheetsConnector {
    constructor(spreadsheetId, sheetName = 'Sheet1') {
        this.spreadsheetId = spreadsheetId;
        this.sheetName = sheetName;
        this.csvUrl = `https://docs.google.com/spreadsheets/d/${spreadsheetId}/export?format=csv&gid=0`;
    }

    // Convert CSV text to JSON objects
    csvToJson(csvText) {
        const lines = csvText.split('\n');
        const headers = lines[0].split(',').map(header => header.trim().replace(/"/g, ''));
        const data = [];

        for (let i = 1; i < lines.length; i++) {
            const values = this.parseCSVLine(lines[i]);
            if (values.length === headers.length) {
                const obj = {};
                headers.forEach((header, index) => {
                    obj[header.toLowerCase()] = values[index] || '';
                });
                data.push(obj);
            }
        }

        return data;
    }

    // Parse CSV line with proper comma handling
    parseCSVLine(line) {
        const values = [];
        let current = '';
        let inQuotes = false;
        
        for (let i = 0; i < line.length; i++) {
            const char = line[i];
            
            if (char === '"') {
                inQuotes = !inQuotes;
            } else if (char === ',' && !inQuotes) {
                values.push(current.trim().replace(/"/g, ''));
                current = '';
            } else {
                current += char;
            }
        }
        
        values.push(current.trim().replace(/"/g, ''));
        return values;
    }

    // Fetch data from Google Sheets
    async fetchData() {
        try {
            const response = await fetch(this.csvUrl);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const csvText = await response.text();
            const data = this.csvToJson(csvText);
            
            // Process data for blog format
            return this.processForBlog(data);
        } catch (error) {
            console.error('Error fetching data from Google Sheets:', error);
            throw error;
        }
    }

    // Process raw data for blog format
    processForBlog(data) {
        return data.map((item, index) => {
            // Ensure required fields exist
            if (!item.id) item.id = index + 1;
            if (!item.title) item.title = 'Untitled Post';
            if (!item.content) item.content = 'No content available';
            if (!item.date) item.date = new Date().toISOString().split('T')[0];
            if (!item.author) item.author = 'Admin';
            if (!item.category) item.category = 'Uncategorized';
            if (!item.status) item.status = 'published';
            if (!item.tags) item.tags = '';

            // Generate slug if not provided
            if (!item.slug && item.title) {
                item.slug = item.title.toLowerCase()
                    .replace(/[^a-z0-9\s-]/g, '')
                    .replace(/\s+/g, '-')
                    .trim();
            }

            return item;
        });
    }

    // Get specific sheet by GID
    setSheetGid(gid) {
        this.csvUrl = `https://docs.google.com/spreadsheets/d/${this.spreadsheetId}/export?format=csv&gid=${gid}`;
    }
}

// Export for use in other modules
module.exports = DirectSheetsConnector;