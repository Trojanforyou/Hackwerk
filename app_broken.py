import streamlit as st
import json
import time
import asyncio
from threading import Thread

# Optional WebSocket support
try:
    import websockets
    WEBSOCKET_AVAILABLE = True
except ImportError:
    WEBSOCKET_AVAILABLE = False

# Initialize session state for messages
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'message_count' not in st.session_state:
    st.session_state.message_count = 0

def show_messages_in_corner():
    """Show messages panel in top-right corner with beautiful styling"""
    # Messages panel in top-right corner
    if st.session_state.message_count == 0:
        message_content = '<p style="text-align: center; color: #666; padding: 20px;">📥 Geen nieuwe berichten</p>'
    else:
        message_content = ""
        for i, message in enumerate(st.session_state.messages):
            sender_icon = {
                "Gemeente Den Haag": "🏛️",
                "RVO Nederland": "🇳🇱", 
                "Kamer van Koophandel": "🏢",
                "Belastingdienst": "💰",
                "Ministerie van EZK": "⚖️",
                "Gemeente Amsterdam": "🌆",
                "Provincie Zuid-Holland": "🗺️"
            }.get(message.get('from', 'Systeem'), "📋")
            
            message_content += f"""
            <div style="background: #f8f9ff; border-radius: 10px; padding: 15px; margin-bottom: 10px; border-left: 4px solid #667eea;">
                <strong>{sender_icon} {message.get('from', 'Systeem')}</strong><br>
                <strong>{message.get('subject', 'Geen onderwerp')}</strong><br>
                <small style="color: #666;">🕐 {message.get('time', 'Onbekend')}</small><br><br>
                {message.get('content', 'Geen inhoud')}
            </div>
            """
    
    # Create the floating messages panel
    st.markdown(f"""
    <div style="position: fixed; top: 80px; right: 20px; width: 350px; max-height: 500px; 
                background: white; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); 
                border: 2px solid #667eea; z-index: 998; overflow-y: auto;">
        <div style="display: flex; justify-content: space-between; align-items: center; 
                    padding: 20px 20px 15px 20px; border-bottom: 2px solid #f0f0f0;">
            <h3 style="margin: 0; color: #667eea;">💬 Berichten ({st.session_state.message_count})</h3>
        </div>
        <div style="padding: 0 20px 20px 20px;">
            {message_content}
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_settings_panel():
    """Show settings panel in top-right corner"""
    st.markdown("""
    <div style="position: fixed; top: 80px; right: 20px; width: 300px; background: white; 
                border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); 
                border: 2px solid #667eea; z-index: 998; padding: 20px;">
        <h3 style="color: #667eea; margin-top: 0;">⚙️ Instellingen</h3>
        <p>Profielinstellingen komen hier...</p>
        <p>- Taal wijzigen</p>
        <p>- Meldingen beheren</p>
        <p>- Account gegevens</p>
    </div>
    """, unsafe_allow_html=True)

def show_messages_panel():
    """Legacy function - redirects to new corner panel"""
    show_messages_in_corner()BLE = False

# Initialize session state for messages
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'message_count' not in st.session_state:
    st.session_state.message_count = 0

def create_top_bar():
    """Create top bar with profile and messages icons"""
    # CSS for the top bar with beautiful icons
    st.markdown("""
    <style>
    .top-bar {
        position: fixed;
        top: 0;
        right: 0;
        z-index: 999;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 12px 25px;
        border-bottom: 2px solid #5a6fd8;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        display: flex;
        align-items: center;
        gap: 20px;
        border-radius: 0 0 0 15px;
    }
    
    .icon-button {
        background: rgba(255, 255, 255, 0.2);
        border: 2px solid rgba(255, 255, 255, 0.3);
        width: 45px;
        height: 45px;
        cursor: pointer;
        border-radius: 50%;
        transition: all 0.3s ease;
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
        backdrop-filter: blur(10px);
    }
    
    .icon-button:hover {
        background: rgba(255, 255, 255, 0.3);
        border-color: rgba(255, 255, 255, 0.5);
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .icon-button svg {
        width: 20px;
        height: 20px;
        fill: white;
    }
    
    .message-badge {
        position: absolute;
        top: -5px;
        right: -5px;
        background: #ff4757;
        color: white;
        border-radius: 50%;
        width: 22px;
        height: 22px;
        font-size: 11px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        border: 2px solid white;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    
    .profile-info {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 14px;
        color: white;
        background: rgba(255, 255, 255, 0.15);
        padding: 8px 15px;
        border-radius: 25px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .profile-avatar {
        width: 30px;
        height: 30px;
        background: linear-gradient(135deg, #ffd89b 0%, #19547b 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 12px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Top bar HTML
    user_name = "Guest"
    if st.session_state.get('logged_in', False):
        user_name = st.session_state.user_data.get('name', 'Guest')
    
    message_badge = ""
    if st.session_state.message_count > 0:
        message_badge = f'<div class="message-badge">{st.session_state.message_count}</div>'
    
    # Get user initials for avatar
    user_initials = "G"
    if user_name != "Guest":
        names = user_name.split()
        user_initials = "".join([name[0] for name in names[:2]]).upper()
    
    top_bar_html = f"""
    <div class="top-bar">
        <div class="profile-info">
            <div class="profile-avatar">{user_initials}</div>
            <span>{user_name}</span>
        </div>
        
        <button class="icon-button" onclick="showMessages()" title="Berichten">
            <svg viewBox="0 0 24 24">
                <path d="M20,8L12,13L4,8V6L12,11L20,6M20,4H4C2.89,4 2,4.89 2,6V18A2,2 0 0,0 4,20H20A2,2 0 0,0 22,18V6C22,4.89 21.1,4 20,4Z"/>
            </svg>
            {message_badge}
        </button>
        
        <button class="icon-button" onclick="showProfile()" title="Profiel Settings">
            <svg viewBox="0 0 24 24">
                <path d="M12,15.5A3.5,3.5 0 0,1 8.5,12A3.5,3.5 0 0,1 12,8.5A3.5,3.5 0 0,1 15.5,12A3.5,3.5 0 0,1 12,15.5M19.43,12.97C19.47,12.65 19.5,12.33 19.5,12C19.5,11.67 19.47,11.34 19.43,11L21.54,9.37C21.73,9.22 21.78,8.95 21.66,8.73L19.66,5.27C19.54,5.05 19.27,4.96 19.05,5.05L16.56,6.05C16.04,5.66 15.5,5.32 14.87,5.07L14.5,2.42C14.46,2.18 14.25,2 14,2H10C9.75,2 9.54,2.18 9.5,2.42L9.13,5.07C8.5,5.32 7.96,5.66 7.44,6.05L4.95,5.05C4.73,4.96 4.46,5.05 4.34,5.27L2.34,8.73C2.22,8.95 2.27,9.22 2.46,9.37L4.57,11C4.53,11.34 4.5,11.67 4.5,12C4.5,12.33 4.53,12.65 4.57,12.97L2.46,14.63C2.27,14.78 2.22,15.05 2.34,15.27L4.34,18.73C4.46,18.95 4.73,19.03 4.95,18.95L7.44,17.94C7.96,18.34 8.5,18.68 9.13,18.93L9.5,21.58C9.54,21.82 9.75,22 10,22H14C14.25,22 14.46,21.82 14.5,21.58L14.87,18.93C15.5,18.68 16.04,18.34 16.56,17.94L19.05,18.95C19.27,19.03 19.54,18.95 19.66,18.73L21.66,15.27C21.78,15.05 21.73,14.78 21.54,14.63L19.43,12.97Z"/>
            </svg>
        </button>
    </div>
    
    <script>
    function showMessages() {{
        console.log('Messages clicked');
    }}
    
    function showProfile() {{
        console.log('Profile clicked');
    }}
    
    // Add top margin to main content to avoid overlap
    if (document.querySelector('.main .block-container')) {{
        document.querySelector('.main .block-container').style.marginTop = '80px';
    }}
    </script>
    """
    
    st.markdown(top_bar_html, unsafe_allow_html=True)
    
    # Add interactive buttons right below the top bar (invisible but clickable)
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col2:
        # Invisible button for messages (positioned over the messages icon)
        if st.button("📧", key="msg_btn", help="Berichten"):
            st.session_state.show_messages = not st.session_state.get('show_messages', False)
            st.rerun()
    
    with col3:
        # Invisible button for settings (positioned over the settings icon)
        if st.button("⚙️", key="settings_btn", help="Instellingen"):
            st.session_state.show_settings = not st.session_state.get('show_settings', False)
            st.rerun()
    
    # Add some custom CSS to hide the default button styling and position them correctly
    st.markdown("""
    <style>
    /* Hide the default streamlit buttons and make them invisible overlay */
    div[data-testid="column"] button[kind="secondary"] {
        background: transparent !important;
        border: none !important;
        color: transparent !important;
        position: fixed;
        top: 12px;
        width: 45px;
        height: 45px;
        z-index: 1000;
        border-radius: 50%;
    }
    
    /* Position message button */
    div[data-testid="column"]:nth-child(2) button {
        right: 90px;
    }
    
    /* Position settings button */  
    div[data-testid="column"]:nth-child(3) button {
        right: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

def show_messages_panel():
    """Show messages panel with beautiful styling"""
    st.sidebar.markdown("### � Inbox")
    
    if st.session_state.message_count == 0:
        st.sidebar.info("📥 Inbox is leeg")
    else:
        for i, message in enumerate(st.session_state.messages):
            # Create a more beautiful message display
            sender_icon = {
                "Gemeente Den Haag": "🏛️",
                "RVO Nederland": "🇳🇱", 
                "Kamer van Koophandel": "🏢",
                "Belastingdienst": "💰",
                "Ministerie van EZK": "⚖️",
                "Gemeente Amsterdam": "🌆",
                "Provincie Zuid-Holland": "🗺️"
            }.get(message.get('from', 'Systeem'), "📋")
            
            with st.sidebar.expander(f"{sender_icon} **{message.get('subject', 'Geen onderwerp')}**", expanded=False):
                st.markdown(f"**📤 Afzender:** {message.get('from', 'Systeem')}")
                st.markdown(f"**🕐 Tijd:** {message.get('time', 'Onbekend')}")
                st.markdown("**📄 Bericht:**")
                st.info(message.get('content', 'Geen inhoud'))
                
        if st.sidebar.button("�️ Alle berichten wissen"):
            st.session_state.messages = []
            st.session_state.message_count = 0
            st.rerun()

def add_test_message():
    """Add a test message for demo purposes"""
    import random
    test_messages = [
        {
            "from": "Gemeente Den Haag",
            "subject": "Nieuwe subsidie beschikbaar", 
            "content": "Er is een nieuwe subsidie beschikbaar voor duurzame energie projecten. Deadline: 31 december 2025."
        },
        {
            "from": "RVO Nederland",
            "subject": "Innovatiekrediet update",
            "content": "Uw aanvraag voor het Innovatiekrediet is in behandeling genomen. Verwachte beslissing binnen 4 weken."
        },
        {
            "from": "Kamer van Koophandel", 
            "subject": "Bedrijfsgegevens update",
            "content": "Vergeet niet uw jaarrekening in te dienen voor 30 juni 2025."
        },
        {
            "from": "Belastingdienst",
            "subject": "BTW aangifte herinnering",
            "content": "Uw BTW aangifte voor Q4 2024 moet worden ingediend voor 31 januari 2025."
        }
    ]
    
    selected_message = random.choice(test_messages)
    selected_message["time"] = time.strftime("%H:%M")
    
    st.session_state.messages.append(selected_message)
    st.session_state.message_count += 1

async def websocket_client():
    """Simple WebSocket client for receiving messages (demo)"""
    if not WEBSOCKET_AVAILABLE:
        return
    
    try:
        # This is a placeholder for real WebSocket implementation
        # In a real app, you would connect to your message server
        uri = "ws://localhost:8765"
        async with websockets.connect(uri) as websocket:
            async for message in websocket:
                # Parse incoming message and add to session state
                try:
                    msg_data = json.loads(message)
                    st.session_state.messages.append(msg_data)
                    st.session_state.message_count += 1
                except:
                    pass
    except:
        # WebSocket server not available, use demo mode
        pass

def start_websocket_client():
    """Start WebSocket client in background thread"""
    if WEBSOCKET_AVAILABLE:
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(websocket_client())
        except:
            pass

# Mock DigiD user profiles (for demo)
MOCK_USERS = {
    "123456789": {
        "name": "King Arthur",
        "bsn": "123456789",
        "company": "Camelot Enterprises B.V.",
        "kvk": "88776655",
        "business_type": "SME",
        "stage": "Growth",
        "location": "Den Haag",
        "employees": 25,
        "annual_revenue": 1200000,
        "sector": "Government & Leadership",
        "email": "king.arthur@camelot.nl",
        "phone": "+31 6 1234 5678",
        "address": "Ridderzaal 1, 2511 CR Den Haag"
    }
}

def digid_login():
    """DigiD authentication interface"""
    st.sidebar.header("🔐 DigiD Inloggen")
    
    # Simple fake DigiD authentication - no external server needed
    
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        st.sidebar.info("Log in met DigiD voor toegang tot gepersonaliseerde overheidsprogramma's")
        
        # Single DigiD login button - fake login as King Arthur
        if st.sidebar.button("🔐 Inloggen met DigiD", type="primary", use_container_width=True):
            # Show realistic DigiD process
            with st.sidebar:
                st.info("🔄 Doorverwijzen naar DigiD...")
                time.sleep(0.5)
                st.success("✅ Verbinding met DigiD servers...")
                time.sleep(0.5)
                st.success("🔐 Authenticatie succesvol!")
            
            # Auto-login as King Arthur
            king_arthur_data = MOCK_USERS["123456789"].copy()
            king_arthur_data.update({
                "auth_method": "DigiD",
                "auth_time": time.strftime("%Y-%m-%d %H:%M:%S"),
                "verified": True
            })
            
            # Set user as logged in
            st.session_state.logged_in = True
            st.session_state.user_data = king_arthur_data
            st.session_state.auth_source = "DigiD"
            
            # Refresh to show logged in state
            st.rerun()
        
        # Small info message
        st.sidebar.caption("💡 **DigiD Demo** - Inloggen als King Arthur")
            
    else:
        user = st.session_state.user_data
        auth_source = st.session_state.get('auth_source', 'Demo')
        
        if auth_source == 'DigiD':
            st.sidebar.success(f"🔐 DigiD Authentiek: {user['name']}")
            st.sidebar.caption(f"Geauthenticeerd om {user.get('auth_time', 'onbekend')}")
        else:
            st.sidebar.success(f"✅ Demo Ingelogd: {user['name']}")
            
        # Show detailed user information
        with st.sidebar.expander("📋 Volledige gegevens", expanded=False):
            st.write(f"**👤 BSN:** {user['bsn']}")
            st.write(f"**🏢 Bedrijf:** {user['company']}")
            st.write(f"**📍 Locatie:** {user['location']}")
            st.write(f"**🏷️ KvK:** {user['kvk']}")
            st.write(f"**👥 Medewerkers:** {user['employees']}")
            st.write(f"**🏭 Sector:** {user['sector']}")
            if 'email' in user:
                st.write(f"**📧 Email:** {user['email']}")
            if 'phone' in user:
                st.write(f"**📞 Telefoon:** {user['phone']}")
            if 'address' in user:
                st.write(f"**🏠 Adres:** {user['address']}")
            if 'email' in user:
                st.write(f"**📧 Email:** {user['email']}")
            if 'phone' in user:
                st.write(f"**📞 Telefoon:** {user['phone']}")
        
        # Show verification status
        if auth_source == 'DigiD':
            if user.get('verified', False):
                st.sidebar.success("✅ Geverifieerd via DigiD")
            st.sidebar.info("🔒 Gegevens uit overheidsregisters")
        else:
            st.sidebar.info("🎭 Demo account")
        
        if st.sidebar.button("Uitloggen", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_data = None
            if 'digid_state' in st.session_state:
                del st.session_state.digid_state
            if 'auth_source' in st.session_state:
                del st.session_state.auth_source
            st.rerun()

# Load program data
@st.cache_data
def load_programs():
    with open("data.json", "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    # Set page config
    st.set_page_config(
        page_title="Ondernemersloket Nederland", 
        page_icon="🏛️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Create top bar with profile and message icons
    create_top_bar()
    
    # Start WebSocket client if not already running
    if 'websocket_started' not in st.session_state:
        st.session_state.websocket_started = True
        if WEBSOCKET_AVAILABLE:
            # Start WebSocket client in background
            thread = Thread(target=start_websocket_client, daemon=True)
            thread.start()
    
    # DigiD Authentication
    digid_login()
    
    # Show messages panel in top-right corner if requested
    if st.session_state.get('show_messages', False):
        show_messages_in_corner()
    
    # Add test message button for demo (in sidebar)
    if st.sidebar.button("➕ Voeg test bericht toe"):
        add_test_message()
        st.rerun()
    
    # Message control buttons
    col1, col2 = st.sidebar.columns([1, 1])
    with col1:
        if st.button("� Test bericht", use_container_width=True):
            add_test_message()
            st.rerun()
    with col2:
        if st.button("� Toon berichten", use_container_width=True):
            st.session_state.show_messages = True
    
    # Show messages if requested
    if st.session_state.get('show_messages', False):
        show_messages_panel()
        if st.sidebar.button("✖️ Sluit berichten"):
            st.session_state.show_messages = False
            st.rerun()
    
    # Main header
    st.markdown("""
    <div style="background: linear-gradient(90deg, #154c79 0%, #1e5f8b 100%); padding: 1.5rem; border-radius: 8px; margin-bottom: 2rem;">
        <h1 style="color: white; margin: 0; font-size: 2.5rem;">🏛️ Ondernemersloket Nederland</h1>
        <p style="color: #e6f3ff; margin: 0.5rem 0 0 0; font-size: 1.2rem;">Gepersonaliseerde ondersteuning voor Nederlandse ondernemers</p>
    </div>
    """, unsafe_allow_html=True)
    
    programs = load_programs()
    
    if not st.session_state.get('logged_in', False):
        
        # Official government notice
        st.info("🔐 **Veilig inloggen vereist:** Log in met DigiD voor toegang tot gepersonaliseerde overheidsprogramma's en projectkansen.")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            ## 🎯 Wat bieden wij
            - **Gepersonaliseerde programma matching** op basis van uw bedrijfsprofiel
            - **Lokale projectkansen** (warmtenetten, infrastructuurprojecten)  
            - **Directe verbinding** met relevante overheidsinstanties
            - **Gestroomlijnde aanvraagprocessen**
            
            ### 🔒 Waarom DigiD?
            Met uw DigiD kunnen we:
            - Uw bedrijfsgegevens ophalen via KvK
            - Gepersonaliseerde adviezen geven
            - Direct contact leggen met lokale overheden
            - Veilig uw gegevens beschermen
            """)
        
        with col2:
            st.markdown("""
            ### 🏢 Voor welke ondernemers?
            - **Startups** - Innovatieve bedrijven
            - **MKB** - Midden- en kleinbedrijf
            - **ZZP** - Zelfstandig zonder personeel  
            - **Scale-ups** - Groeiende bedrijven
            
            ### 🌍 Beschikbare locaties
            - Amsterdam • Utrecht  
            - Rotterdam • Den Haag
            - Eindhoven • Groningen
            """)
            
        # Success stories section
        st.markdown("---")
        st.markdown("### 🏆 Succesverhalen")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            **GreenTech B.V.**  
            💰 €450K innovatiekrediet  
            🌱 Duurzame energie oplossingen
            """)
        
        with col2:
            st.markdown("""
            **InnoStart**  
            🚀 €100K accelerator programma  
            💻 AI technologie startup
            """)
            
        with col3:
            st.markdown("""
            **WarmteNet Utrecht**  
            🔥 €2.5M warmtenet subsidie  
            🏘️ 5000 huizen aangesloten
            """)
    
    else:
        user = st.session_state.user_data
        auth_source = st.session_state.get('auth_source', 'Demo')
        
        # Special welcome for DigiD users
        if auth_source == 'DigiD':
            st.success(f"🔐 **DigiD Authentiek:** Welkom {user['name']} van {user['company']}!")
            st.info("✅ Alle onderstaande gegevens zijn geverifieerd via DigiD en overheidsregisters")
        else:
            st.success(f"🎭 **Demo Modus:** Welkom {user['name']} van {user['company']}!")
        
        # Personalized recommendations
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎯 Uw Profiel")
            st.write(f"**👤 Naam:** {user['name']}")
            st.write(f"**🏢 Bedrijf:** {user['company']}")
            st.write(f"**📍 Locatie:** {user['location']}")
            st.write(f"**🏷️ KvK:** {user['kvk']}")
            st.write(f"**👥 Medewerkers:** {user['employees']}")
            st.write(f"**🏭 Sector:** {user['sector']}")
            if auth_source == 'DigiD':
                st.write(f"**📧 Email:** {user.get('email', 'Niet beschikbaar')}")
        
        with col2:
            st.markdown("### 🔍 Zoek Programma's")
            business_type = st.selectbox("Bedrijfstype:", ["Startup", "SME", "Self-employed", "Scale-up"],
                                       index=["Startup", "SME", "Self-employed", "Scale-up"].index(user['business_type']))
            stage = st.selectbox("Ontwikkelingsfase:", ["Beginning", "Growth", "International Expansion"],
                               index=["Beginning", "Growth", "International Expansion"].index(user['stage']))

        if st.button("🎯 Zoek Gepersonaliseerde Ondersteuning", type="primary", use_container_width=True):
            # Enhanced matching logic
            results = []
            for p in programs:
                if p["type"] == business_type and p["stage"] == stage:
                    # Location check
                    if "location" in p and user["location"] not in p["location"]:
                        continue
                    
                    # Employee count check
                    if "max_employees" in p and user["employees"] > p["max_employees"]:
                        continue
                    if "min_employees" in p and user["employees"] < p["min_employees"]:
                        continue
                    
                    # Revenue check
                    if "max_revenue" in p and user["annual_revenue"] > p["max_revenue"]:
                        continue
                    if "min_revenue" in p and user["annual_revenue"] < p["min_revenue"]:
                        continue
                    
                    # Sector check
                    if "sectors" in p and user["sector"] not in p["sectors"]:
                        continue
                        
                    results.append(p)

            if results:
                st.success(f"✅ Gevonden: {len(results)} gepersonaliseerde programma(s) voor {user['company']}:")
                
                for r in results:
                    with st.expander(f"**{r['name']}** - €{r.get('funding_amount', 0):,}"):
                        st.write(r['description'])
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if 'deadline' in r:
                                st.write(f"**Aanmelddeadline:** {r['deadline']}")
                            if 'contact' in r:
                                st.write(f"**Contact:** {r['contact']}")
                        
                        with col2:
                            if st.button(f"Aanvragen", key=f"apply_{r['name']}"):
                                st.success("🚀 Doorverwezen naar aanvraagportaal...")
            else:
                st.warning("⚠️ Geen programma's gevonden voor uw profiel. Probeer andere criteria.")

        # Project collaboration section
        st.markdown("---")
        st.markdown("### 🤝 Lokale Projectkansen")
        
        # Mock local projects
        local_projects = [
            {
                "name": "Amsterdam Heat Network Phase 2",
                "location": "Amsterdam", 
                "type": "Heat Network",
                "budget": "€25M",
                "partners_needed": ["Clean Energy", "Construction", "Technology"],
                "deadline": "2025-12-01",
                "description": "Municipaal project voor uitbreiding stadsverwarmingsnet naar 5.000 extra woningen"
            },
            {
                "name": "Utrecht Smart Grid Integration",
                "location": "Utrecht",
                "type": "Energy Infrastructure", 
                "budget": "€15M",
                "partners_needed": ["Technology", "Clean Energy"],
                "deadline": "2026-02-15",
                "description": "Integratie van hernieuwbare energiebronnen met bestaande stadsinfrastructuur"
            }
        ]
        
        relevant_projects = [p for p in local_projects 
                           if p["location"] == user["location"] and 
                           user["sector"] in p["partners_needed"]]
        
        if relevant_projects:
            st.success(f"🎯 Gevonden: {len(relevant_projects)} projectkansen in {user['location']}:")
            
            for project in relevant_projects:
                with st.expander(f"🏗️ **{project['name']}** - {project['budget']}"):
                    st.write(project['description'])
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"**Budget:** {project['budget']}")
                    with col2:
                        st.write(f"**Deadline:** {project['deadline']}")
                    with col3:
                        if st.button("Interesse tonen", key=f"interest_{project['name']}"):
                            st.success("✅ Interesse geregistreerd!")
        else:
            st.info(f"Momenteel geen actieve projecten in {user['location']} voor {user['sector']} sector.")

if __name__ == "__main__":
    main()