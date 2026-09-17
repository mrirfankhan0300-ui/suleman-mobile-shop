"""
Suleman Mobile Shop - Streamlit Landing Page
=============================================
A simple, mobile-friendly landing page with:
  1. Shop name / branding
  2. Photo gallery section
  3. Click-to-call and WhatsApp contact links
  4. Automatic "someone visited the page" email notification (via Gmail SMTP)

Author: Generated for Suleman Mobile Shop
"""

import smtplib
import ssl
from datetime import datetime
from email.mime.text import MIMEText
from pathlib import Path

import pandas as pd
import streamlit as st

# --------------------------------------------------------------------------
# BASIC CONFIG
# --------------------------------------------------------------------------
SHOP_NAME = "Suleman Mobile Shop"
SHOP_TAGLINE = "Your trusted destination for mobiles & accessories"

# Multiple contact groups. Each group can have a different CALL number and
# WHATSAPP number. "raw" = digits only, country code first, NO '+' and NO leading 0.
CONTACT_NUMBERS = [
    {
        "label": "Shop / Sales",
        "call_display": "0319 6829629",        # <-- please double-check, looks 2 digits short (should be 11 digits total)
        "call_raw": "9231968629",            # 92 + digits without leading 0 -- VERIFY this once corrected
        "whatsapp_display": "0306 8596720",
        "whatsapp_raw": "923068596720",
    },
    {
        "label": "Repair",
        "call_display": "0317 4447806",
        "call_raw": "923174447806",
        "whatsapp_display": "0317 6829629",
        "whatsapp_raw": "923176829629",
    },
]

# Opening hours, shown as a simple table
OPENING_HOURS = [
    ("Monday – Saturday", "10:00 AM – 9:00 PM"),
    ("Sunday", "2:00 PM – 8:00 PM"),
]

# Shop location for the map section
SHOP_ADDRESS = "Mana Ahmdani Basti Budhan Shareef Dera Ghazi Khan, Pakistan"
SHOP_LATITUDE = 29.814127004379536
SHOP_LONGITUDE = 70.60290257624149 
GOOGLE_MAPS_LINK = f"https://www.google.com/maps/search/?api=1&query={SHOP_LATITUDE},{SHOP_LONGITUDE}"

# Product catalog / price list: (name, price in PKR, optional short note)
PRODUCTS = [
    {"name": "Samsung Galaxy A15", "price": "PKR 42,999", "note": "128GB, 4GB RAM"},
    {"name": "Samsung Galaxy A55", "price": "PKR 89,999", "note": "256GB, 8GB RAM"},
    {"name": "Xiaomi Redmi Note 13", "price": "PKR 38,999", "note": "128GB, 6GB RAM"},
    {"name": "iPhone 13", "price": "PKR 154,999", "note": "128GB, PTA Approved"},
    {"name": "Infinix Hot 40", "price": "PKR 29,999", "note": "128GB, 8GB RAM"},
    {"name": "Screen Protector", "price": "PKR 500", "note": "Tempered glass, all models"},
    {"name": "Fast Charger (20W)", "price": "PKR 1,800", "note": "Type-C / Lightning"},
    {"name": "Phone Case", "price": "PKR 700", "note": "Wide range of designs"},
]

# Folder where shop photos live (add your own images here before deploying)
IMAGES_DIR = Path(__file__).parent / "shop_images"

st.set_page_config(
    page_title=SHOP_NAME,
    page_icon="📱",
    layout="centered",
)

# --------------------------------------------------------------------------
# EMAIL NOTIFICATION (fires once per visitor session)
# --------------------------------------------------------------------------
def send_visit_notification():
    """Send an email to the shop owner whenever a new visitor session starts.

    Credentials are read from st.secrets so nothing sensitive is hard-coded
    in the source file. See the deployment instructions for how to set these.
    """
    try:
        gmail_address = st.secrets["GMAIL_ADDRESS"]
        gmail_app_password = st.secrets["GMAIL_APP_PASSWORD"]
        notify_to = st.secrets.get("NOTIFY_EMAIL", gmail_address)
    except (KeyError, FileNotFoundError):
        # Secrets not configured yet — skip silently so the page still works.
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    subject = f"🔔 New visitor on {SHOP_NAME} website"
    body = (
        f"Someone just opened the {SHOP_NAME} landing page.\n\n"
        f"Time: {timestamp}\n\n"
        f"(This is an automated notification.)"
    )

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = gmail_address
    msg["To"] = notify_to

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(gmail_address, gmail_app_password)
            server.sendmail(gmail_address, notify_to, msg.as_string())
    except Exception as exc:  # noqa: BLE001
        # Never let a broken mail server crash the page for a customer.
        # Log to Streamlit's console instead.
        print(f"[email notification failed] {exc}")


# Streamlit re-runs this script on every interaction (button click, etc.).
# We only want ONE email per browser session (i.e. per new visitor),
# so we guard it with session_state.
if "visit_notified" not in st.session_state:
    st.session_state.visit_notified = True
    send_visit_notification()

# --------------------------------------------------------------------------
# STYLING (mobile-friendly, minimal CSS)
# --------------------------------------------------------------------------
st.markdown(
    """
    <style>
        .main > div {max-width: 480px; margin: 0 auto;}
        .shop-title {
            text-align: center;
            font-size: 2.1rem;
            font-weight: 800;
            margin-bottom: 0.1rem;
            color: #1a1a2e;
        }
        .shop-tagline {
            text-align: center;
            color: #666;
            margin-bottom: 1.5rem;
            font-size: 1rem;
        }
        .contact-btn {
            display: block;
            text-align: center;
            padding: 0.9rem 1rem;
            border-radius: 12px;
            font-weight: 700;
            font-size: 1.05rem;
            text-decoration: none;
            margin-bottom: 0.8rem;
            color: white !important;
        }
        .call-btn {background-color: #1a73e8;}
        .whatsapp-btn {background-color: #25D366;}
        .section-header {
            font-size: 1.2rem;
            font-weight: 700;
            margin-top: 1.5rem;
            margin-bottom: 0.6rem;
            border-bottom: 2px solid #eee;
            padding-bottom: 0.3rem;
        }
        .product-card {
            border: 1px solid #eee;
            border-radius: 10px;
            padding: 0.7rem 0.9rem;
            margin-bottom: 0.6rem;
            background: #fafafa;
        }
        .product-name {font-weight: 700; font-size: 1rem; color: #1a1a2e;}
        .product-price {font-weight: 800; color: #1a73e8; float: right;}
        .product-note {color: #777; font-size: 0.85rem; clear: both;}
        .hours-row {
            display: flex;
            justify-content: space-between;
            padding: 0.4rem 0;
            border-bottom: 1px solid #f0f0f0;
            font-size: 0.95rem;
        }
        .hours-day {font-weight: 600; color: #1a1a2e;}
        .hours-time {color: #444;}
        .map-btn {
            display: block;
            text-align: center;
            padding: 0.8rem 1rem;
            border-radius: 12px;
            font-weight: 700;
            text-decoration: none;
            background-color: #ea4335;
            color: white !important;
            margin-top: 0.6rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# HEADER
# --------------------------------------------------------------------------
st.markdown(f'<div class="shop-title">📱 {SHOP_NAME}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="shop-tagline">{SHOP_TAGLINE}</div>', unsafe_allow_html=True)

# --------------------------------------------------------------------------
# PHOTO GALLERY SECTION
# --------------------------------------------------------------------------
st.markdown('<div class="section-header">🏬 Shop Gallery</div>', unsafe_allow_html=True)

if IMAGES_DIR.exists():
    image_files = sorted(
        [p for p in IMAGES_DIR.iterdir() if p.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp")]
    )
else:
    image_files = []

if image_files:
    if len(image_files) == 1:
        st.image(str(image_files[0]), use_container_width=True)
    else:
        cols = st.columns(2)
        for idx, img_path in enumerate(image_files):
            with cols[idx % 2]:
                st.image(str(img_path), use_container_width=True)
else:
    st.info(
        "📸 No photos added yet. Create a folder named `shop_images` next to "
        "`app.py`, drop your shop photos in it (JPG/PNG), and they will "
        "appear here automatically."
    )

# --------------------------------------------------------------------------
# PRODUCT CATALOG / PRICE LIST
# --------------------------------------------------------------------------
st.markdown('<div class="section-header">🛒 Products & Price List</div>', unsafe_allow_html=True)

search_term = st.text_input("Search products", placeholder="e.g. Samsung, charger, case", label_visibility="collapsed")

filtered_products = [
    p for p in PRODUCTS
    if search_term.strip().lower() in p["name"].lower()
] if search_term else PRODUCTS

if filtered_products:
    for p in filtered_products:
        st.markdown(
            f"""
            <div class="product-card">
                <span class="product-price">{p['price']}</span>
                <span class="product-name">{p['name']}</span>
                <div class="product-note">{p.get('note', '')}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
else:
    st.info("No products match your search.")

st.caption("Prices may vary — please call or WhatsApp to confirm current stock and price.")

# --------------------------------------------------------------------------
# OPENING HOURS
# --------------------------------------------------------------------------
st.markdown('<div class="section-header">🕒 Opening Hours</div>', unsafe_allow_html=True)

hours_html = "".join(
    f'<div class="hours-row"><span class="hours-day">{day}</span>'
    f'<span class="hours-time">{time}</span></div>'
    for day, time in OPENING_HOURS
)
st.markdown(hours_html, unsafe_allow_html=True)

# --------------------------------------------------------------------------
# LOCATION / MAP SECTION
# --------------------------------------------------------------------------
st.markdown('<div class="section-header">📍 Find Us</div>', unsafe_allow_html=True)
st.write(SHOP_ADDRESS)
map_df = pd.DataFrame({"lat": [SHOP_LATITUDE], "lon": [SHOP_LONGITUDE]})
st.map(map_df, zoom=15)
st.markdown(
    f'<a class="map-btn" href="{GOOGLE_MAPS_LINK}" target="_blank">🗺️ Open in Google Maps</a>',
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# CONTACT SECTION
# --------------------------------------------------------------------------
st.markdown('<div class="section-header">📞 Contact Us</div>', unsafe_allow_html=True)

whatsapp_message = "Hello! I'm interested in your mobiles."

for contact in CONTACT_NUMBERS:
    call_link = f"tel:+{contact['call_raw']}"
    whatsapp_link = f"https://wa.me/{contact['whatsapp_raw']}?text={whatsapp_message.replace(' ', '%20')}"

    st.markdown(f"**{contact['label']}**", unsafe_allow_html=False)
    st.markdown(
        f'<a class="contact-btn call-btn" href="{call_link}">📞 Call — {contact["call_display"]}</a>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<a class="contact-btn whatsapp-btn" href="{whatsapp_link}" target="_blank">💬 WhatsApp — {contact["whatsapp_display"]}</a>',
        unsafe_allow_html=True,
    )

st.markdown("---")
st.caption(f"© {datetime.now().year} {SHOP_NAME}. All rights reserved.")