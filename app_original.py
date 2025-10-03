import streamlit as st
import json
import time

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
        
        # Show verification status
        if auth_source == 'DigiD':
            if user.get('verified', False):
                st.sidebar.success("✅ Geverifieerd via DigiD")
            st.sidebar.info("🔒 Gegevens uit overheidsregisters")
        else:
            st.sidebar.info("🎭 Demo account")
        
        # Logout button
        if st.sidebar.button("🚪 Uitloggen"):
            # Clear session state
            for key in ['logged_in', 'user_data', 'auth_source']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

@st.cache_data
def load_programs():
    with open("data.json", "r", encoding="utf-8") as f:
        return json.load(f)

def filter_programs(programs, user_data):
    """Filter programs based on user criteria"""
    filtered = []
    
    for program in programs:
        # Check location eligibility
        if user_data['location'] not in program['eligible_locations']:
            continue
            
        # Check employee count
        if not (program['min_employees'] <= user_data['employees'] <= program['max_employees']):
            continue
            
        # Check revenue
        if user_data['annual_revenue'] > program['max_revenue']:
            continue
            
        # Check sector
        if user_data['sector'] not in program['eligible_sectors']:
            continue
            
        filtered.append(program)
    
    return filtered

def calculate_match_score(program, user_data):
    """Calculate match percentage for a program"""
    score = 0
    max_score = 5
    
    # Location match (weight: 1)
    if user_data['location'] in program['eligible_locations']:
        score += 1
    
    # Employee range match (weight: 1)  
    if program['min_employees'] <= user_data['employees'] <= program['max_employees']:
        score += 1
    
    # Revenue match (weight: 1)
    if user_data['annual_revenue'] <= program['max_revenue']:
        score += 1
    
    # Sector match (weight: 1)
    if user_data['sector'] in program['eligible_sectors']:
        score += 1
    
    # Business stage bonus (weight: 1)
    if user_data['business_type'] == 'SME' and program.get('supports_sme', True):
        score += 1
    
    return int((score / max_score) * 100)

def main():
    # Set page config
    st.set_page_config(
        page_title="Ondernemersloket Nederland", 
        page_icon="🏛️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # DigiD Authentication
    digid_login()
    
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
            - **Real-time updates** over nieuwe subsidies en regelingen
            - **Directe communicatie** met overheidsinstanties
            
            ## 📊 Beschikbare Programma's
            """)
            
            # Show first few programs as preview
            for program in programs[:3]:
                with st.expander(f"🏛️ **{program['name']}** - {program['provider']}", expanded=False):
                    st.write(f"**💰 Budget:** €{program['max_amount']:,}")
                    st.write(f"**👥 Werknemers:** {program['min_employees']}-{program['max_employees']}")
                    st.write(f"**📍 Locatie:** {', '.join(program['eligible_locations'])}")
                    st.write(f"**🏭 Sectoren:** {', '.join(program['eligible_sectors'])}")
                    st.write(program['description'])
        
        with col2:
            st.markdown("### 🔐 Inloggen Vereist")
            st.info("Voor volledige toegang tot:")
            st.write("- ✅ Gepersonaliseerde matches")
            st.write("- ✅ Aanvraagprocessen")  
            st.write("- ✅ Projectkansen")
            st.write("- ✅ Directe communicatie")
            
            # Benefits preview
            st.markdown("### 🎯 Voordelen")
            st.success("**Tijdsbesparing** tot 80% bij aanvragen")
            st.success("**Hogere slagingskans** door matching")
            st.success("**Proactieve meldingen** bij nieuwe kansen")
    
    else:
        # User is logged in - show personalized experience
        user = st.session_state.user_data
        st.success(f"👋 **Welkom {user['name']}!** U bent ingelogd via DigiD.")
        
        # Create main layout
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("## 🎯 Gepersonaliseerde Programma's voor uw Bedrijf")
            
            # Filter programs for this user
            matched_programs = filter_programs(programs, user)
            
            if matched_programs:
                st.success(f"🎉 **{len(matched_programs)} programma's** gevonden die perfect bij uw bedrijf passen!")
                
                # Sort by match score
                for program in matched_programs:
                    match_score = calculate_match_score(program, user)
                    
                    with st.expander(f"✅ **{program['name']}** - {match_score}% match", expanded=True):
                        col_a, col_b = st.columns([3, 1])
                        
                        with col_a:
                            st.write(f"**💰 Max subsidie:** €{program['max_amount']:,}")
                            st.write(f"**📋 Beschrijving:** {program['description']}")
                            st.write(f"**🏛️ Aanbieder:** {program['provider']}")
                            st.write(f"**⏰ Deadline:** {program.get('deadline', 'Doorlopend')}")
                        
                        with col_b:
                            if st.button(f"📝 Aanvragen", key=f"apply_{program['id']}"):
                                st.success("✅ Aanvraag ingediend! U ontvangt binnen 2 werkdagen een bevestiging.")
                                st.balloons()
            
            else:
                st.warning("❌ Geen programma's gevonden die exact matchen met uw bedrijfsprofiel.")
                st.info("💡 **Tip:** Probeer uw bedrijfsgegevens te actualiseren of neem contact op voor advies.")
            
            # Local projects section
            st.markdown("---")
            st.markdown("## 🚀 Lokale Projectkansen")
            
            # Mock local project for Den Haag
            if user['location'] == "Den Haag":
                st.success("🔥 **Warmtenet Den Haag** - Partner gezocht")
                st.info("De gemeente Den Haag zoekt bedrijven voor deelname aan het nieuwe warmtenet project.")
                
                col_proj1, col_proj2 = st.columns([3, 1])
                with col_proj1:
                    st.write("**🎯 Gezocht:** Bedrijven met technische expertise")
                    st.write("**💰 Investering:** €500.000 - €2.000.000")
                    st.write("**⏰ Deadline:** 15 december 2024")
                
                with col_proj2:
                    if st.button("🤝 Interesse tonen"):
                        st.balloons()
                        st.success("✅ Interesse geregistreerd! De gemeente neemt binnen 1 week contact op.")
        
        with col2:
            # User profile sidebar
            st.markdown("### 👤 Uw Bedrijfsprofiel")
            st.info(f"""
            **🏢 Bedrijf:** {user['company']}  
            **📍 Locatie:** {user['location']}  
            **👥 Werknemers:** {user['employees']}  
            **💰 Omzet:** €{user['annual_revenue']:,}  
            **🏭 Sector:** {user['sector']}
            """)
            
            # Quick stats
            st.markdown("### 📊 Uw Match Statistieken")
            total_programs = len(programs)
            matched_count = len(filter_programs(programs, user))
            match_percentage = int((matched_count / total_programs) * 100) if total_programs > 0 else 0
            
            st.metric("Totaal beschikbaar", f"{total_programs} programma's")
            st.metric("Voor u geschikt", f"{matched_count} programma's")  
            st.metric("Match percentage", f"{match_percentage}%")
            
            # Recent activity (mock)
            st.markdown("### 🔔 Recent")
            st.success("✅ Profiel bijgewerkt")
            st.info("📊 3 nieuwe programma's toegevoegd")
            st.warning("⏰ Deadline Innovation Credit: 31 dec")

if __name__ == "__main__":
    main()