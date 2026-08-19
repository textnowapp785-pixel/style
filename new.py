import asyncio
import re
import requests
import phonenumbers
from phonenumbers import geocoder
from telegram.constants import ParseMode
try:
    from telegram import CopyTextButton, Bot, InlineKeyboardButton, InlineKeyboardMarkup
except ImportError:
    CopyTextButton = None
    Bot = None
    InlineKeyboardButton = None
    InlineKeyboardMarkup = None


# === CONFIGURATION ===
BOT_TOKEN = "8784543942:AAHPqFmLtjQJPHtcSPH7fuUVagdtEaxBdCA"
GROUP_ID = -1004443378843
API_URL = "https://numberpanel.tech/api/otp?count=200"
POLL_INTERVAL = 10

PANEL_LINK = "https://t.me/fayaz_otp_bot?start=8488081516"

# ===== ORIGINAL API CONFIG =====
API_URL_ORIGINAL = "http://147.135.212.197/crapi/had/viewstats"
TOKEN = "SlJSQjRSQldcko9XYX9Yh4p4eX5kl2tlRGKHYWhgWEhGgph7Undu"

# ===== HADI RAILWAY APIs =====
API_URLS_RAILWAY = [
    "https://api-junaid-production.up.railway.app/api/ps?type=sms",
    "https://api-junaid-production.up.railway.app/api/np?type=sms",
]

# ===== SERVICE LOGO IDs =====
SERVICE_LOGOS = {
    "WhatsApp":          "5226815671261763813",
    "WhatsApp Business": "5267457160077415807",
    "Telegram":          "5454261685965572205",
    "Instagram":         "5330375003579890327",
    "Google":            "5456150110071178646",
    "Facebook":          "5332341566025515614",
    "IMO":               "5226479577185949100",
    "YouTube":           "5330134940677849089",
    "Apple":             "5451965905686775304",
    "TikTok":            "5454051309877478077",
    "SMS":               "5337302974806922068",
}

# ===== COUNTRY FLAG IDs =====
COUNTRY_FLAGS = {
    "AF": {"id": "5222096009009575868", "name": "Afghanistan"},
    "AL": {"id": "5224312057515486246", "name": "Albania"},
    "DZ": {"id": "5224260376174015500", "name": "Algeria"},
    "AD": {"id": "5221987861733061751", "name": "Andorra"},
    "AG": {"id": "5224544866217765554", "name": "Antigua and Barbuda"},
    "AR": {"id": "5221980461504411710", "name": "Argentina"},
    "AM": {"id": "5224369957969603463", "name": "Armenia"},
    "AU": {"id": "5224659803837574114", "name": "Australia"},
    "AT": {"id": "5224520754271366661", "name": "Austria"},
    "AZ": {"id": "5224426544163728284", "name": "Azerbaijan"},
    "BS": {"id": "5224504167107668172", "name": "Bahamas"},
    "BH": {"id": "5224492892818518587", "name": "Bahrain"},
    "BD": {"id": "5224407289825340729", "name": "Bangladesh"},
    "BB": {"id": "5222156533688712094", "name": "Barbados"},
    "BY": {"id": "5280820319458707404", "name": "Belarus"},
    "BE": {"id": "5224513182244024630", "name": "Belgium"},
    "BM": {"id": "5222482143749353810", "name": "Bermuda"},
    "BA": {"id": "5224496092569155254", "name": "Bosnia and Herzegovina"},
    "BW": {"id": "5224288456670196085", "name": "Botswana"},
    "BR": {"id": "5224688610183228070", "name": "Brazil"},
    "BN": {"id": "5224435958732042406", "name": "Brunei"},
    "BG": {"id": "5222092074819530668", "name": "Bulgaria"},
    "CA": {"id": "5222001124592071204", "name": "Canada"},
    "CL": {"id": "5222000927023577045", "name": "Chile"},
    "CN": {"id": "5224435456220868088", "name": "China"},
    "DE": {"id": "5222165617544542414", "name": "Germany"},
    "EE": {"id": "5222195463272281351", "name": "Estonia"},
    "EG": {"id": "5293992082212409502", "name": "Egypt"},
    "SV": {"id": "5224337131534559907", "name": "El Salvador"},
    "GQ": {"id": "5222172811614762423", "name": "Equatorial Guinea"},
    "ES": {"id": "5222024776976970940", "name": "Spain"},
    "ET": {"id": "5224467805914542024", "name": "Ethiopia"},
    "FJ": {"id": "5221962676044838178", "name": "Fiji"},
    "FI": {"id": "5224282903277482188", "name": "Finland"},
    "FR": {"id": "5222029789203804982", "name": "France"},
    "GA": {"id": "5224669733801963467", "name": "Gabon"},
    "GM": {"id": "5221949872747330159", "name": "Gambia"},
    "GE": {"id": "5222152195771742239", "name": "Georgia"},
    "GH": {"id": "5224511339703056124", "name": "Ghana"},
    "GR": {"id": "5222463490706389920", "name": "Greece"},
    "GD": {"id": "5222234560359577687", "name": "Grenada"},
    "GT": {"id": "5222128302868672826", "name": "Guatemala"},
    "GN": {"id": "5222337588035073000", "name": "Guinea"},
    "GW": {"id": "5224705704153066489", "name": "Guinea-Bissau"},
    "GY": {"id": "5224570532942329532", "name": "Guyana"},
    "HT": {"id": "5224683146984831315", "name": "Haiti"},
    "HN": {"id": "5222229234600130045", "name": "Honduras"},
    "HU": {"id": "5224691998912427164", "name": "Hungary"},
    "IS": {"id": "5222063229819172521", "name": "Iceland"},
    "IN": {"id": "5222300011366200403", "name": "India"},
    "ID": {"id": "5224405893960969756", "name": "Indonesia"},
    "IR": {"id": "5224374154152653367", "name": "Iran"},
    "IQ": {"id": "5221980268230882832", "name": "Iraq"},
    "IE": {"id": "5224257017509588818", "name": "Ireland"},
    "IL": {"id": "5224720599099648709", "name": "Israel"},
    "JM": {"id": "5222007034467074185", "name": "Jamaica"},
    "JP": {"id": "5222390089715299207", "name": "Japan"},
    "JO": {"id": "5222292177345853436", "name": "Jordan"},
    "KZ": {"id": "5222276376161171525", "name": "Kazakhstan"},
    "KE": {"id": "5222089648163009103", "name": "Kenya"},
    "KI": {"id": "5224652244695134610", "name": "Kiribati"},
    "KW": {"id": "5221949726718442491", "name": "Kuwait"},
    "KG": {"id": "5224388147156102493", "name": "Kyrgyzstan"},
    "LA": {"id": "5224200843632324642", "name": "Laos"},
    "LV": {"id": "5224401229626484931", "name": "Latvia"},
    "LB": {"id": "5222244425899455269", "name": "Lebanon"},
    "LS": {"id": "5224245850594619415", "name": "Lesotho"},
    "LR": {"id": "5221998371518034740", "name": "Liberia"},
    "LY": {"id": "5222194286451242896", "name": "Libya"},
    "LT": {"id": "5224245902134226386", "name": "Lithuania"},
    "LU": {"id": "5224499567197700690", "name": "Luxembourg"},
    "MG": {"id": "5222042605386217334", "name": "Madagascar"},
    "MY": {"id": "5224312886444174057", "name": "Malaysia"},
    "MV": {"id": "5224393700548814960", "name": "Maldives"},
    "ML": {"id": "5224322352552096671", "name": "Mali"},
    "MT": {"id": "5224731388057497620", "name": "Malta"},
    "MH": {"id": "5224538449536624503", "name": "Marshall Islands"},
    "MU": {"id": "5224238347286752315", "name": "Mauritius"},
    "MX": {"id": "5221971386238514431", "name": "Mexico"},
    "FM": {"id": "5222280486444873367", "name": "Micronesia"},
    "MD": {"id": "5224216473018314447", "name": "Moldova"},
    "MC": {"id": "5221937224068640464", "name": "Monaco"},
    "MN": {"id": "5224192257992701543", "name": "Mongolia"},
    "ME": {"id": "5224463399278096980", "name": "Montenegro"},
    "MZ": {"id": "5222470388423864826", "name": "Mozambique"},
    "NA": {"id": "5224690826386351746", "name": "Namibia"},
    "NP": {"id": "5222444378101925267", "name": "Nepal"},
    "NL": {"id": "5224516489368841614", "name": "Netherlands"},
    "NZ": {"id": "5224573595254009705", "name": "New Zealand"},
    "NE": {"id": "5222099049846420864", "name": "Niger"},
    "NG": {"id": "5224723614166691638", "name": "Nigeria"},
    "NO": {"id": "5224465228934163949", "name": "Norway"},
    "OM": {"id": "5222396686785066306", "name": "Oman"},
    "PK": {"id": "5224637061985742245", "name": "Pakistan"},
    "PA": {"id": "5222111719999945107", "name": "Panama"},
    "PG": {"id": "5224500164198149905", "name": "Papua New Guinea"},
    "PY": {"id": "5222152565138929235", "name": "Paraguay"},
    "PL": {"id": "5224670399521892983", "name": "Poland"},
    "PT": {"id": "5224482026551258766", "name": "Portugal"},
    "QA": {"id": "5224404094369672274", "name": "Qatar"},
    "RO": {"id": "5224220115150582423", "name": "Romania"},
    "RU": {"id": "5280582975270963511", "name": "Russia"},
    "RW": {"id": "5222225596762830469", "name": "Rwanda"},
    "VC": {"id": "5224541228380467535", "name": "Saint Vincent and the Grenadines"},
    "WS": {"id": "5224660353593387686", "name": "Samoa"},
    "ST": {"id": "5221953304426198315", "name": "Sao Tome and Principe"},
    "SA": {"id": "5224698145010624573", "name": "Saudi Arabia"},
    "SN": {"id": "5224358988623130949", "name": "Senegal"},
    "RS": {"id": "5222145396838512729", "name": "Serbia"},
    "SC": {"id": "5224467496676896871", "name": "Seychelles"},
    "SL": {"id": "5224420995065983217", "name": "Sierra Leone"},
    "SG": {"id": "5224194023224257181", "name": "Singapore"},
    "SK": {"id": "5222401879400528047", "name": "Slovakia"},
    "SI": {"id": "5224660718665607511", "name": "Slovenia"},
    "SB": {"id": "5222290588207954120", "name": "Solomon Islands"},
    "SO": {"id": "5222370504664428325", "name": "Somalia"},
    "ZA": {"id": "5224696216570309138", "name": "South Africa"},
    "KR": {"id": "5222345550904439270", "name": "South Korea"},
    "SS": {"id": "5224618146949773268", "name": "South Sudan"},
    "LK": {"id": "5224277294050192388", "name": "Sri Lanka"},
    "SD": {"id": "5224372990216514135", "name": "Sudan"},
    "SR": {"id": "5224567367551428669", "name": "Suriname"},
    "SE": {"id": "5222201098269373561", "name": "Sweden"},
    "CH": {"id": "5224707263226194753", "name": "Switzerland"},
    "TJ": {"id": "5222217865821696536", "name": "Tajikistan"},
    "TZ": {"id": "5224397364155923150", "name": "Tanzania"},
    "TH": {"id": "5224638530864556281", "name": "Thailand"},
    "TG": {"id": "5222408051268532030", "name": "Togo"},
    "TT": {"id": "5224391883777651050", "name": "Trinidad and Tobago"},
    "TN": {"id": "5221991375016310330", "name": "Tunisia"},
    "TR": {"id": "5224601903383457698", "name": "Turkey"},
    "TM": {"id": "5224256935905208951", "name": "Turkmenistan"},
    "UG": {"id": "5222464040462200940", "name": "Uganda"},
    "UA": {"id": "5222250679371839695", "name": "Ukraine"},
    "AE": {"id": "5224565851427976312", "name": "UAE"},
    "GB": {"id": "5224518800061245598", "name": "United Kingdom"},
    "US": {"id": "5224321781321442532", "name": "United States"},
    "UY": {"id": "5222466849370813232", "name": "Uruguay"},
    "UZ": {"id": "5222404546575219535", "name": "Uzbekistan"},
    "VU": {"id": "5222126748090512778", "name": "Vanuatu"},
    "VE": {"id": "5294476442854247878", "name": "Venezuela"},
    "VA": {"id": "5222420266155520507", "name": "Vatican City"},
    "VN": {"id": "5222359651282071925", "name": "Vietnam"},
    "YE": {"id": "5222300655611294950", "name": "Yemen"},
    "ZM": {"id": "5224646626877911277", "name": "Zambia"},
    "ZW": {"id": "5222060442385397848", "name": "Zimbabwe"},
    "XK": {"id": "5222197129719592160", "name": "Kosovo"},
    "PS": {"id": "5222370620628546719", "name": "Palestine"},
}

# ===== STATUS/DECORATIVE EMOJI IDs =====
CE = {
    "fire":      "5337267511261960341",
    "time":      "5336983442125001376",
    "globe":     "5224450179368767019",
    "phone":     "5337132498965010628",
    "key":       "5197288647275071607",
    "msg":       "5337302974806922068",
    "channel":   "5352597830089347330",
    "number":    "5352862640592949843",
    "ok":        "5352694861990501856",
    "no":        "5420130255174145507",
    "warn":      "5336944168944047463",
    "money":     "5348469219761626211",
    "link":      "5420517437885943844",
    "pin":       "5352922460897452503",
    "graph":     "5352877703043258544",
    "rocket":    "5352597830089347330",
    "star":      "5352552689983067014",
    "lock":      "5353022963132174959",
    "hi":        "5353027129250453493",
    "world":     "5224450179368767019",
    "search":    "5463352748751753567",
    "broadcast": "6269303009658802514",
    "call":      "6204108584381322968",
    "verified":  "5841528141037705335",
    "vip":       "6267128480601741166",
    "boss":      "6267019543051244106",
    "check":     "6298670698948724690",
    "otpkey":    "5420626637429432217",
    "mlock":     "5994372308976803475",
    "play":      "5994372308976803475",
}

def ce(tag, fallback):
    eid = CE.get(tag, "")
    if not eid:
        return fallback
    return f'<tg-emoji emoji-id="{eid}">{fallback}</tg-emoji>'

def svc_emoji(service, fallback):
    eid = SERVICE_LOGOS.get(service, "")
    if not eid:
        return fallback
    return f'<tg-emoji emoji-id="{eid}">{fallback}</tg-emoji>'

def flag_emoji(region, fallback):
    data = COUNTRY_FLAGS.get(region)
    if not data or not data.get("id"):
        return fallback
    return f'<tg-emoji emoji-id="{data["id"]}">{fallback}</tg-emoji>'

# ===== SERVICE DETECTION (FIXED - Added from working script) =====
def detect_service(message):
    msg = str(message).lower()
    if "whatsapp business" in msg:
        return "WhatsApp Business"
    elif "whatsapp" in msg:
        return "WhatsApp"
    elif "telegram" in msg:
        return "Telegram"
    elif "google" in msg:
        return "Google"
    elif "facebook" in msg or "fb" in msg:
        return "Facebook"
    elif "instagram" in msg or "ig" in msg:
        return "Instagram"
    elif "imo" in msg:
        return "IMO"
    elif "youtube" in msg or "yt" in msg:
        return "YouTube"
    elif "apple" in msg or "ios" in msg or "iphone" in msg:
        return "Apple"
    elif "tiktok" in msg or "tik tok" in msg:
        return "TikTok"
    else:
        return "SMS"

def get_app_emoji(service_name):
    service_name = str(service_name).lower()
    for key in SERVICE_LOGOS.keys():
        if key.lower() in service_name:
            return svc_emoji(key, "📱")
    return "📱"

# ===== COUNTRY INFO (FIXED - Improved from working script) =====
def get_country_info(phone_number):
    try:
        if not phone_number.startswith('+'):
            phone_number = '+' + phone_number
        parsed = phonenumbers.parse(phone_number)
        region = phonenumbers.region_code_for_number(parsed)
        country = geocoder.description_for_number(parsed, "en") or "Unknown"
        if region:
            flag = chr(ord(region[0]) + 127397) + chr(ord(region[1]) + 127397)
            animated_flag = flag_emoji(region, flag)
        else:
            flag = "🏳️"
            animated_flag = flag
        iso = region or "UN"
        return country, animated_flag, iso
    except:
        return "Unknown", "🏳️", "UN"

# ===== OTP EXTRACTION (FIXED - Better patterns from working script) =====
def extract_otp(msg):
    if not msg:
        return "Unknown"
    msg_lower = str(msg).lower()
    patterns = [
        r"code is[:\s]+(\d{4,8})",
        r"code[:\s]*(\d{4,8})",
        r"verification code.*?(\d{4,8})",
        r"otp.*?(\d{4,8})",
        r"\b(\d{3}[- ]\d{3})(?=\D|$)",
        r"\b(\d{3}[- ]\d{4})(?=\D|$)",
        r"(?<!\d)(\d{6})(?!\d)",
        r"(?<!\d)(\d{4,8})(?!\d)",
    ]
    for pattern in patterns:
        match = re.search(pattern, msg_lower)
        if match:
            return match.group(1)
    # Fallback to original pattern
    otp_match = re.search(r'\d{3}[-\s]?\d{3,4}|\d{4,8}', str(msg))
    return otp_match.group(0) if otp_match else "Unknown"

# ===== NUMBER MASKING (FIXED - Better from working script) =====
def mask_number(num):
    num = str(num).replace('+', '')
    if len(num) <= 6:
        return num
    play_emoji = ce("play", "▶️")
    try:
        if not num.startswith('+'):
            parsed = phonenumbers.parse('+' + num)
            country_code = str(parsed.country_code)
            national = str(parsed.national_number)
            if len(national) > 5:
                return f"+{country_code}{play_emoji}{national[-5:]}"
            return f"+{country_code}{national}"
    except:
        pass
    return num[:3] + play_emoji + num[-3:]

# ===== API FETCHERS =====

def fetch_api_main():
    """Fetch from numberpanel.tech main API"""
    try:
        resp = requests.get(API_URL, timeout=15)
        data = resp.json()
        print(f"[DEBUG] Main API status: {resp.status_code}, type: {type(data)}")

        results = []
        items = []

        if isinstance(data, list):
            items = data
        elif isinstance(data, dict):
            for key in ["data", "otps", "results", "messages", "aaData"]:
                if key in data and isinstance(data[key], list):
                    items = data[key]
                    print(f"[DEBUG] Extracted {len(items)} from '{key}'")
                    break

        for item in items:
            try:
                if isinstance(item, list) and len(item) >= 4:
                    # Format: [service, num, msg, dt] or similar
                    service = detect_service(item[2] if len(item) > 2 else "")
                    num = str(item[1]) if len(item) > 1 else ""
                    msg = str(item[2]) if len(item) > 2 else ""
                    dt = str(item[3]) if len(item) > 3 else ""
                elif isinstance(item, dict):
                    msg_text = str(item.get("message", item.get("msg", "")))
                    service = detect_service(msg_text)
                    num = str(item.get("num", item.get("number", "")))
                    msg = msg_text
                    dt = str(item.get("dt", item.get("date", item.get("time", ""))))
                else:
                    continue

                if msg and num:
                    results.append([service, num, msg, dt])
            except Exception as e:
                print(f"[DEBUG] Main API item error: {e}")
                continue

        print(f"[DEBUG] Main API parsed: {len(results)} entries")
        return results
    except Exception as e:
        print(f"[DEBUG] Main API error: {e}")
    return []

def fetch_api_original():
    try:
        params = {"token": TOKEN, "records": 5}
        response = requests.get(API_URL_ORIGINAL, params=params, timeout=5)
        data = response.json()
        print(f"[DEBUG] Original API status: {data.get('status')}, records: {len(data.get('data', []))}")
        if data.get("status") == "success":
            results = []
            for sms in data.get("data", []):
                service = detect_service(sms.get("message", ""))
                results.append([
                    service,
                    sms.get("num", ""),
                    sms.get("message", ""),
                    sms.get("dt", "")
                ])
            return results
    except Exception as e:
        print(f"[DEBUG] Original API error: {e}")
    return []

def fetch_api_railway(api_url):
    try:
        response = requests.get(api_url, timeout=10)
        data = response.json()
        records = data.get("aaData", [])
        print(f"[DEBUG] Railway API ({api_url}): {len(records)} records")
        valid = [r for r in records if isinstance(r[0], str) and ":" in r[0]]
        results = []
        for r in valid:
            service = detect_service(r[4] if len(r) > 4 else "")
            results.append([
                service,
                r[2] if len(r) > 2 else "",
                r[4] if len(r) > 4 else "",
                r[0]
            ])
        return results
    except Exception as e:
        print(f"[DEBUG] Railway API error ({api_url}): {e}")
    return []

async def send_to_group(bot, entry):
    service = entry[0]
    num = entry[1]
    msg = entry[2]

    country_name, flag, iso = get_country_info(num)
    app_emoji = get_app_emoji(service)
    masked = mask_number(num)
    otp = extract_otp(msg)

    text = f"{flag} <b>#{iso} {app_emoji}{service} {masked}</b> <tg-emoji emoji-id=\"5337267511261960341\">▶️</tg-emoji>"

    if CopyTextButton:
        try:
            row1 = [InlineKeyboardButton(
                text=f"{otp}",
                copy_text=CopyTextButton(text=otp),
                style="success",
                icon_custom_emoji_id=CE["otpkey"]
            )]
        except Exception as btn_err:
            print(f"[DEBUG] CopyTextButton failed: {btn_err}, using fallback")
            row1 = [InlineKeyboardButton(
                text=f"🔑 {otp}",
                callback_data="noop",
                style="success",
                icon_custom_emoji_id=CE["otpkey"]
            )]
    else:
        row1 = [InlineKeyboardButton(
            text=f"🔑 {otp}",
            callback_data="noop",
            style="primary",
            icon_custom_emoji_id=CE["otpkey"]
        )]

    row2 = [
        InlineKeyboardButton(
            text="Chat group",
            url="https://t.me/+rt1N4nk4_aU0ZDk0",
            style="success",
            icon_custom_emoji_id=CE["call"]
        ),
        InlineKeyboardButton(
            text="CHANEL",
            url="https://t.me/+TLo1Z_Pm4cdjMmY0",
            style="danger",
            icon_custom_emoji_id=CE["broadcast"]
        )
    ]

    markup = InlineKeyboardMarkup([row1, row2,])

    try:
        await bot.send_message(
            chat_id=GROUP_ID,
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=markup,
            disable_web_page_preview=True
        )
        print(f"✅ Sent OTP for {num} - {service}")
        return True
    except Exception as e:
        print(f"❌ Failed to send to group: {e}")
        return False

async def main():
    bot = Bot(token=BOT_TOKEN)
    seen_otps = set()

    print("🚀 Starting Forwarder Bot...")
    print(f"[DEBUG] Target GROUP_ID: {GROUP_ID}")

    # === TEST MESSAGE ON STARTUP ===
    try:
        await bot.send_message(
            chat_id=GROUP_ID,
            text="🤖 <b>Bot Started</b>\nMonitoring OTP APIs...",
            parse_mode=ParseMode.HTML
        )
        print(f"[DEBUG] ✅ Test message sent successfully to {GROUP_ID}")
    except Exception as e:
        print(f"[DEBUG] ❌ TEST MESSAGE FAILED: {e}")
        print("[DEBUG] Bot cannot send messages to this group. Check GROUP_ID and bot permissions!")

    # Initial fetch to prevent sending old OTPs
    try:
        all_entries = []

        all_entries.extend(fetch_api_main())
        all_entries.extend(fetch_api_original())
        for url in API_URLS_RAILWAY:
            all_entries.extend(fetch_api_railway(url))

        print(f"[DEBUG] Total initial entries: {len(all_entries)}")

        for item in all_entries:
            try:
                uid = f"{item[0]}_{item[1]}_{item[3]}"
                seen_otps.add(uid)
            except Exception as e:
                print(f"[DEBUG] Error creating UID for item: {item} | Error: {e}")

        print(f"📦 Initialized with {len(seen_otps)} existing OTPs.")
    except Exception as e:
        print(f"⚠️ Initial API fetch failed: {e}")

    while True:
        try:
            all_entries = []

            all_entries.extend(fetch_api_main())
            all_entries.extend(fetch_api_original())
            for url in API_URLS_RAILWAY:
                all_entries.extend(fetch_api_railway(url))

            new_count = 0
            for item in reversed(all_entries):
                try:
                    uid = f"{item[0]}_{item[1]}_{item[3]}"
                    if uid not in seen_otps:
                        seen_otps.add(uid)
                        success = await send_to_group(bot, item)
                        if success:
                            new_count += 1
                        await asyncio.sleep(0.5)
                except Exception as e:
                    print(f"[DEBUG] Error processing item {item}: {e}")

            if new_count > 0:
                print(f"[DEBUG] Sent {new_count} new OTPs this cycle.")

            if len(seen_otps) > 10000:
                seen_otps = set(list(seen_otps)[-5000:])

        except Exception as e:
            print(f"⚠️ Error in main loop: {e}")

        await asyncio.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())
