import re
from typing import Dict, Optional, Any

def parse_query_for_specs(query: str) -> Dict[str, Optional[Any]]:
    """
    Parses a query string to extract structured laptop specifications.
    This version is optimized for scalability and extracts more features.
    """
    specs: Dict[str, Optional[Any]] = {
        'Ram': None,
        'SSD': None,
        'HDD': None,
        'Company': None,
        'TypeName': None,
        'Cpu_brand': None,
        'Gpu_brand': None,
        'Os': None,
        'TouchScreen': None,
        'Ips': None,
        'min_total_storage': None,
        'max_total_storage': None
    }
    
    query_lower = query.lower()

    # --- Central Keyword Mapping for Scalability ---
    # Maps spec names to a list of keywords that identify them.
    SPEC_KEYWORD_MAP = {
        'TypeName': ['gaming', 'ultrabook', 'notebook', '2 in 1 convertible', 'workstation', 'netbook'],
        'Gpu_brand': ['nvidia', 'amd', 'intel'],
        'Os': ['windows', 'mac', 'linux', 'chrome os'],
        'TouchScreen': ['touchscreen', 'touch screen'],
        'Ips': ['ips']
    }

    # --- Keyword-Based Extraction Loop ---
    for spec_name, keywords in SPEC_KEYWORD_MAP.items():
        for keyword in keywords:
            if keyword in query_lower:
                # For boolean specs, we store True. For others, the found keyword.
                if spec_name in ['TouchScreen', 'Ips']:
                    specs[spec_name] = True
                else:
                    specs[spec_name] = keyword.capitalize()
                break # Move to the next spec type once a match is found

    # --- RegEx and Other Specific Logic ---
    # General Storage
    MAX_STORAGE_GB = 1000
    if "storage" in query_lower:
        if "large" in query_lower or "big" in query_lower:
            specs['min_total_storage'] = int(MAX_STORAGE_GB * 0.7)
        elif "small" in query_lower or "low" in query_lower:
            specs['max_total_storage'] = int(MAX_STORAGE_GB * 0.5)
    
    # RAM, SSD, HDD
    ram_match = re.search(r'(\d+)\s*gb\s*ram', query_lower)
    if ram_match: specs['Ram'] = ram_match.group(1)
    
    ssd_match = re.search(r'(\d+)\s*gb\s*ssd', query_lower)
    if ssd_match: specs['SSD'] = ssd_match.group(1)
        
    hdd_match = re.search(r'(\d+)\s*gb\s*hdd', query_lower)
    if hdd_match: specs['HDD'] = hdd_match.group(1)

    # Company
    brands = ['hp', 'dell', 'lenovo', 'asus', 'acer', 'apple', 'msi']
    for brand in brands:
        if brand in query_lower:
            specs['Company'] = brand.capitalize()
            break
            
    # CPU Brand
    cpu_map = {
        'core i7': 'Intel Core i7', 'i7': 'Intel Core i7',
        'core i5': 'Intel Core i5', 'i5': 'Intel Core i5',
        'core i3': 'Intel Core i3', 'i3': 'Intel Core i3',
        'ryzen 7': 'AMD Processor', 'ryzen 5': 'AMD Processor',
    }
    for keyword, brand_name in cpu_map.items():
        if keyword in query_lower:
            specs['Cpu_brand'] = brand_name
            break
    if not specs['Cpu_brand']:
        if 'intel' in query_lower: specs['Cpu_brand'] = 'Other Intel Processor'
        elif 'amd' in query_lower: specs['Cpu_brand'] = 'AMD Processor'

    return specs