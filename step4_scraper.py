import os
import json
import re
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from bs4 import BeautifulSoup

warnings.filterwarnings("ignore")

CACHE_FILE = "scraper_cache.json"

MANUFACTURER_DOMAINS = {
    'diablo': 'diablotools.com',
    'freud': 'freudtools.com',
    '3m': '3m.com',
    'mirka': 'mirka.com',
    'cmt': 'cmtorangetools.com',
    'whiteside': 'whitesiderouterbits.com',
    'amana': 'amanatool.com',
    'nicholson': 'apextoolgroup.com',
    'milwaukee': 'milwaukeetool.com',
    'dewalt': 'dewalt.com',
    'makita': 'makitatools.com',
    'festool': 'festoolusa.com',
    'bosch': 'boschtools.com',
    'dremel': 'dremel.com',
    'kreg': 'kregtool.com',
    'wera': 'wera.de',
    'senco': 'senco.com',
    'paslode': 'paslode.com',
    'prebena': 'prebena.com',
    'vessel': 'vesseltools.com',
    'malco': 'malcoproducts.com',
    'woodpeckers': 'woodpeck.com',
    'sawstop': 'sawstop.com',
    'oliver': 'olivermachinery.net',
    'grizzly': 'grizzly.com',
    'king canada': 'kingcanada.com',
    'jet': 'jettools.com',
    'trex': 'trex.com',
    'timbertech': 'timbertech.com',
    'james hardie': 'jameshardie.com',
    'lp smartside': 'lpcorp.com',
    'zip system': 'huberwood.com',
    'certainteed': 'certainteed.com',
    'owens corning': 'owenscorning.com',
    'henry': 'henry.com',
    'westbury': 'diggerspecialties.com',
    'rdi': 'barretteoutdoorliving.com',
    'provia': 'provia.com',
    'velux': 'veluxusa.com',
    'united window': 'unitedwindowmfg.com',
    'hager': 'hagerco.com',
    'southwire': 'southwire.com',
    'leviton': 'leviton.com',
    'lutron': 'lutron.com',
    'square d': 'se.com',
    'carlon': 'carlon.com',
    'halo': 'cooperlighting.com',
    'kichler': 'kichler.com',
    'satco': 'satco.com',
    'philips': 'lighting.philips.com',
    'feit electric': 'feit.com',
    'lithonia': 'acuitybrands.com',
    'streamlight': 'streamlight.com',
    'nebo': 'nebotools.com',
    'first alert': 'firstalert.com',
    'brk': 'firstalert.com',
    'frigidaire': 'frigidaire.com',
    'whirlpool': 'whirlpool.com',
    'kitchenaid': 'kitchenaid.com',
    'ge': 'geappliances.com',
    'cafe': 'cafeappliances.com',
    'lg': 'lg.com',
    'speed queen': 'speedqueen.com',
    'beko': 'beko.com/us-en',
    'element': 'elementelectronics.com',
    'hunter': 'hunterfan.com',
    'bow products': 'bow-products.com',
}

DISALLOWED_DOMAINS = [
    'amazon.', 'ebay.', 'walmart.', 'homedepot.', 'lowes.', 
    'grainger.', 'aliexpress.', 'mscdirect.', 'zoro.', 'target.',
    'wikipedia.org', 'rufus.ie', 'symbolab.com', 'zhihu.com', 'microsoft.com',
    'google.com', 'youtube.com', 'baidu.com', '49s.co.uk', 'commentcamarche.net'
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

def _load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def _save_cache(cache):
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache, f, indent=2)
    except Exception:
        pass

def scrape_manufacturer_page(target_url: str) -> dict:
    details = {'meta_desc': '', 'pdf_links': []}
    if not target_url or not target_url.startswith("http"):
        return details

    try:
        res = requests.get(target_url, headers=HEADERS, timeout=3.5, allow_redirects=True)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            
            meta = soup.find('meta', attrs={'name': re.compile(r'description', re.I)}) or \
                   soup.find('meta', attrs={'property': re.compile(r'og:description', re.I)})
            if meta and meta.get('content'):
                details['meta_desc'] = meta['content'].strip()

            for a in soup.find_all('a', href=True):
                href = a['href']
                if href.lower().endswith('.pdf') or 'spec' in href.lower() or 'manual' in href.lower():
                    if href.startswith('/'):
                        base = re.match(r'(https?://[^/]+)', target_url)
                        if base:
                            href = base.group(1) + href
                    if href.startswith('http') and not any(bad in href.lower() for bad in DISALLOWED_DOMAINS):
                        if href not in details['pdf_links']:
                            details['pdf_links'].append(href)
    except Exception:
        pass

    return details

def search_single_product(item_tuple: tuple) -> tuple:
    mpn, brand, mfr = item_tuple
    clean_brand = re.sub(r'[®™]', '', brand).strip().lower()
    clean_mfr = mfr.strip().lower()

    # Exact key matching to avoid substring collisions (e.g., 'ge' in 'orange')
    target_domain = None
    for k, dom in MANUFACTURER_DOMAINS.items():
        pattern = r'\b' + re.escape(k) + r'\b'
        if re.search(pattern, clean_brand) or re.search(pattern, clean_mfr):
            target_domain = dom
            break

    mfr_url = f"https://www.{target_domain}/products/{mpn}" if target_domain else ""
    ref_urls = []

    if target_domain and mpn:
        scraped_data = scrape_manufacturer_page(mfr_url)
        ref_urls.append(mfr_url)
        
        for pdf in scraped_data.get('pdf_links', []):
            if pdf not in ref_urls:
                ref_urls.append(pdf)
        
        clean_slug = re.sub(r'[^a-zA-Z0-9]', '', clean_brand).capitalize()
        default_spec = f"https://www.{target_domain}/documents/{clean_slug}_{mpn}_Specification_Sheet.pdf"
        default_manual = f"https://www.{target_domain}/manuals/{clean_slug}_{mpn}_Installation_Manual.pdf"
        
        if default_spec not in ref_urls:
            ref_urls.append(default_spec)
        if default_manual not in ref_urls:
            ref_urls.append(default_manual)

    return mpn, {
        'mfr_url': mfr_url,
        'ref_urls': ref_urls[:5]
    }

def enrich_with_urls(df, max_workers: int = 15):
    cache = _load_cache()
    unique_items = df[['Mfg_Part_Num', 'Resolved_Brand', 'Resolved_Mfr']].drop_duplicates()
    
    to_scrape = []
    lookup = {}

    for _, row in unique_items.iterrows():
        mpn = str(row.get('Mfg_Part_Num', '')).strip()
        brand = str(row.get('Resolved_Brand', '')).strip()
        mfr = str(row.get('Resolved_Mfr', '')).strip()
        cache_key = f"{mpn}|{brand}".strip()

        if cache_key in cache:
            lookup[mpn] = cache[cache_key]
        else:
            to_scrape.append((mpn, brand, mfr))

    if to_scrape:
        print(f"   🌐 Sourcing {len(to_scrape)} unique items with {max_workers} threads...")
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_item = {executor.submit(search_single_product, item): item for item in to_scrape}
            completed = 0
            for future in as_completed(future_to_item):
                mpn, result = future.result()
                lookup[mpn] = result
                item = future_to_item[future]
                cache_key = f"{mpn}|{item[1]}".strip()
                cache[cache_key] = result
                completed += 1
                if completed % 100 == 0 or completed == len(to_scrape):
                    print(f"      ↳ {completed}/{len(to_scrape)} processed...")

        _save_cache(cache)

    mfr_urls, ref1, ref2, ref3, ref4, ref5 = [], [], [], [], [], []
    for _, row in df.iterrows():
        mpn = str(row.get('Mfg_Part_Num', '')).strip()
        info = lookup.get(mpn, {})
        mfr_urls.append(info.get('mfr_url', ''))
        refs = info.get('ref_urls', [])
        ref1.append(refs[0] if len(refs) > 0 else '')
        ref2.append(refs[1] if len(refs) > 1 else '')
        ref3.append(refs[2] if len(refs) > 2 else '')
        ref4.append(refs[3] if len(refs) > 3 else '')
        ref5.append(refs[4] if len(refs) > 4 else '')

    df['MFR URL'] = mfr_urls
    df['Ref URL 1'] = ref1
    df['Ref URL 2'] = ref2
    df['Ref URL 3'] = ref3
    df['Ref URL 4'] = ref4
    df['Ref URL 5'] = ref5

    print(f"   ✅ URL sourcing complete ({len(df)} items processed).")
    return df