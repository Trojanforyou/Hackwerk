import streamlit as st
import json
import time

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
    st.sidebar.header("DigiD Inloggen")
    
    
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        st.sidebar.info("Log in met DigiD voor toegang tot gepersonaliseerde overheidsprogramma's")
        
        if st.sidebar.button("Inloggen met DigiD", type="primary", use_container_width=True):
            with st.sidebar:
                st.info("Doorverwijzen naar DigiD...")
                time.sleep(0.5)
                st.success("Verbinding met DigiD servers...")
                time.sleep(0.5)
                st.success("Authenticatie succesvol!")
            
            king_arthur_data = MOCK_USERS["123456789"].copy()
            king_arthur_data.update({
                "auth_method": "DigiD",
                "auth_time": time.strftime("%Y-%m-%d %H:%M:%S"),
                "verified": True
            })
            
            st.session_state.logged_in = True
            st.session_state.user_data = king_arthur_data
            st.session_state.auth_source = "DigiD"
            
            st.rerun()
        
        st.sidebar.caption("💡 **DigiD Demo** - Inloggen als King Arthur")
            
    else:
        user = st.session_state.user_data
        auth_source = st.session_state.get('auth_source', 'Demo')
        
        if auth_source == 'DigiD':
            st.sidebar.success(f"🔐 DigiD Authentiek: {user['name']}")
            st.sidebar.caption(f"Geauthenticeerd om {user.get('auth_time', 'onbekend')}")
        else:
            st.sidebar.success(f"✅ Demo Ingelogd: {user['name']}")
            
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
        
        if auth_source == 'DigiD':
            if user.get('verified', False):
                st.sidebar.success("✅ Geverifieerd via DigiD")
            st.sidebar.info("🔒 Gegevens uit overheidsregisters")
        else:
            st.sidebar.info("🎭 Demo account")
        
        if st.sidebar.button("🚪 Uitloggen"):
            for key in ['logged_in', 'user_data', 'auth_source']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

@st.cache_data
def load_programs():
    with open("data.json", "r", encoding="utf-8") as f:
        return json.load(f)

def filter_programs(programs, user_data, filters=None):
    """Filter programs based on user criteria and additional filters"""
    if not filters:
        return programs
    
    all_default = all(
        not filters.get(key) or filters.get(key) in ['Все', 'Alle niveaus', 'Alle rechtsvormen', 'Alle leeftijden', 'Alle groottes', 'Alle statussen', 'Alle uitgaven']
        for key in ['income_level', 'filing_status', 'household_size', 'age_range', 'employment_status', 'expense_type']
    )
    
    if all_default:
        return programs
    
    filtered = []
    
    for program in programs:
        include_program = True
        
        program_text = ' '.join([
            program.get('short_name', '').lower(),
            program.get('long_name', '').lower(),
            program.get('description', '').lower(),
            ' '.join(program.get('criteria', [])).lower(),
            ' '.join(program.get('benefits', [])).lower()
        ])
        
        filters_passed = 0
        total_active_filters = 0
        
        if filters.get('income_level') and 'laag inkomen' in filters.get('income_level', '').lower():
            total_active_filters += 1
            income_keywords = ['klein', 'start', 'beperkt', 'minimaal', 'zzp', 'starter']
            if any(keyword in program_text for keyword in income_keywords):
                filters_passed += 1
        elif filters.get('income_level') and 'midden inkomen' in filters.get('income_level', '').lower():
            total_active_filters += 1  
            income_keywords = ['mkb', 'midden', 'gemiddeld', 'groei', 'ontwikkeling']
            if any(keyword in program_text for keyword in income_keywords):
                filters_passed += 1
        elif filters.get('income_level') and 'hoog inkomen' in filters.get('income_level', '').lower():
            total_active_filters += 1
            income_keywords = ['groot', 'hoog', 'scale', 'export', 'internationaal', 'aanzienlijk']
            if any(keyword in program_text for keyword in income_keywords):
                filters_passed += 1
        
        if filters.get('filing_status') and 'bedrijf' in filters.get('filing_status', '').lower():
            total_active_filters += 1
            business_keywords = ['bedrijf', 'onderneming', 'mkb', 'bv', 'commercieel', 'zakelijk', 'fiscaal']
            if any(keyword in program_text for keyword in business_keywords):
                filters_passed += 1
        elif filters.get('filing_status') and 'particulier' in filters.get('filing_status', '').lower():
            total_active_filters += 1
            personal_keywords = ['particulier', 'persoon', 'individueel', 'privé', 'eigen']
            if any(keyword in program_text for keyword in personal_keywords):
                filters_passed += 1
        
        if filters.get('employment_status') and 'zelfstandig' in filters.get('employment_status', '').lower():
            total_active_filters += 1
            entrepreneur_keywords = ['zelfstandig', 'ondernemer', 'eigenaar', 'zzp', 'freelance']
            if any(keyword in program_text for keyword in entrepreneur_keywords):
                filters_passed += 1
        
        if filters.get('expense_type') and 'bedrijf' in filters.get('expense_type', '').lower():
            total_active_filters += 1
            business_expense_keywords = ['bedrijf', 'zakelijk', 'commercieel', 'investering', 'operationeel']
            if any(keyword in program_text for keyword in business_expense_keywords):
                filters_passed += 1
        elif filters.get('expense_type') and 'apparatuur' in filters.get('expense_type', '').lower():
            total_active_filters += 1
            equipment_keywords = ['apparatuur', 'machines', 'technologie', 'installatie', 'hardware', 'middelen']
            if any(keyword in program_text for keyword in equipment_keywords):
                filters_passed += 1
        elif filters.get('expense_type') and 'training' in filters.get('expense_type', '').lower():
            total_active_filters += 1
            training_keywords = ['training', 'opleiding', 'scholing', 'ontwikkeling', 'kennis', 'cursus']
            if any(keyword in program_text for keyword in training_keywords):
                filters_passed += 1
        elif filters.get('expense_type') and 'onderzoek' in filters.get('expense_type', '').lower():
            total_active_filters += 1
            research_keywords = ['onderzoek', 'ontwikkeling', 'innovatie', 'r&d', 'speur', 'technisch']
            if any(keyword in program_text for keyword in research_keywords):
                filters_passed += 1
        
        if total_active_filters == 0 or filters_passed > 0:
            filtered.append(program)
    
    return filtered

def calculate_match_score(program, user_data):
    """Calculate match percentage for a program"""
    score = 0
    max_score = 5
    
    program_text = ' '.join([
        program.get('short_name', '').lower(),
        program.get('long_name', '').lower(), 
        program.get('description', '').lower(),
        ' '.join(program.get('criteria', [])).lower(),
        ' '.join(program.get('benefits', [])).lower()
    ])
    
    if user_data.get('business_type') == 'SME':
        business_keywords = ['mkb', 'bedrijf', 'onderneming', 'commerci']
        if any(keyword in program_text for keyword in business_keywords):
            score += 1
    
    user_sector = user_data.get('sector', '').lower()
    if 'government' in user_sector or 'leadership' in user_sector:
        gov_keywords = ['overheid', 'publiek', 'bestuur', 'regering']
        if any(keyword in program_text for keyword in gov_keywords):
            score += 1
    elif 'technology' in user_sector:
        tech_keywords = ['technologie', 'innovatie', 'digitaal', 'r&d', 'ontwikkeling']
        if any(keyword in program_text for keyword in tech_keywords):
            score += 1
    
    employees = user_data.get('employees', 0)
    if 10 <= employees <= 50:
        size_keywords = ['mkb', 'midden', 'groei', 'kleinschalig']
        if any(keyword in program_text for keyword in size_keywords):
            score += 1
    
    revenue = user_data.get('annual_revenue', 0)
    if revenue >= 500000:
        revenue_keywords = ['hoog', 'groot', 'aanzienlijk', 'substantieel']
        if any(keyword in program_text for keyword in revenue_keywords):
            score += 1
    
    general_keywords = ['subsidie', 'financiering', 'ondersteuning', 'stimulering', 'aftrek']
    if any(keyword in program_text for keyword in general_keywords):
        score += 1
    
    return max(25, int((score / max_score) * 100))  # Minimum 25% match

def main():
    st.set_page_config(
        page_title="Ondernemersloket Nederland", 
        page_icon="⚖️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.markdown("""
    <style>
    .main {
        background-color: white;
    }
    .stApp {
        background-color: white;
    }
    .css-1d391kg {
        background-color: white;
    }
    </style>
    """, unsafe_allow_html=True)
    
    digid_login()
    
    st.markdown("""
    <div style="background: linear-gradient(90deg, #154c79 0%, #1e5f8b 100%); padding: 2rem; border-radius: 12px; margin-bottom: 2rem; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
        <div style="display: flex; align-items: center;">
            <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 50%; margin-right: 1.5rem;">
                <span style="font-size: 2rem;">⚖️</span>
            </div>
            <div>
                <h1 style="color: white; margin: 0; font-size: 2.8rem; font-weight: 600;">Ondernemersloket Nederland</h1>
                <p style="color: #b8d4f0; margin: 0.5rem 0 0 0; font-size: 1.1rem; font-weight: 300;">Officieel portaal voor Nederlandse ondernemers | Ministerie van Economische Zaken en Klimaat</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    programs = load_programs()
    
    if not st.session_state.get('logged_in', False):
        
        st.markdown("""
        <div style="background: #fff3cd; border: 1px solid #ffeaa7; padding: 1.5rem; border-radius: 8px; margin: 1.5rem 0;">
            <h4 style="color: #856404; margin: 0 0 0.5rem 0;">Veilige DigiD-authenticatie vereist</h4>
            <p style="color: #856404; margin: 0;">Log in met DigiD voor toegang tot gepersonaliseerde overheidsprogramma's en projectkansen.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            
            **Gepersonaliseerde programma matching**  
            Op basis van uw bedrijfsprofiel en specifieke behoeften
            
            **Lokale projectkansen**  
            Warmtenetten, infrastructuurprojecten en publiek-private samenwerkingen
            
            **Real-time updates**  
            Automatische notificaties over nieuwe subsidies en regelingen
            
            **Directe communicatie**  
            Rechtstreeks contact met relevante overheidsinstanties
            
            """)
            
            for program in programs[:3]:
                program_name = program.get('long_name', program.get('short_name', 'Onbekende programma'))
                with st.expander(f"**{program_name}** | Nederlandse overheid", expanded=False):
                    st.markdown(f"**Korte naam:** {program.get('short_name', 'N/A')}")
                    st.markdown(f"**Beschrijving:** {program.get('description', 'Geen beschrijving beschikbaar')}")
                    if program.get('criteria'):
                        st.markdown(f"**Geschiktheidscriteria:** {', '.join(program.get('criteria', [])[:3])}")
                    if program.get('benefits'):
                        st.markdown(f"**Belangrijkste voordelen:** {', '.join(program.get('benefits', [])[:3])}")
                    st.markdown("**Uitvoerder:** Nederlandse overheid")
                    st.markdown("**Status:** Actief programma")
        
        with col2:
            st.markdown("### DigiD Authenticatie Vereist")
            st.markdown("""
            <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 8px; border: 1px solid #dee2e6;">
                <h4 style="color: #495057; margin: 0 0 1rem 0;">Volledige toegang na inloggen:</h4>
                <ul style="color: #6c757d; margin: 0; padding-left: 1.2rem;">
                    <li>Gepersonaliseerde programma matches</li>
                    <li>Digitale aanvraagprocessen</li>
                    <li>Lokale projectkansen</li>
                    <li>Directe communicatie met overheden</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### Voordelen van het platform")
            st.markdown("""
            <div style="background: #d4edda; padding: 1rem; border-radius: 6px; margin: 0.5rem 0; border-left: 4px solid #28a745;">
                <strong>Tijdsbesparing tot 80%</strong><br/>
                <small>bij het indienen van subsidieaanvragen</small>
            </div>
            <div style="background: #d1ecf1; padding: 1rem; border-radius: 6px; margin: 0.5rem 0; border-left: 4px solid #17a2b8;">
                <strong>Hogere slagingskans</strong><br/>
                <small>door intelligente programma matching</small>
            </div>
            <div style="background: #fff3cd; padding: 1rem; border-radius: 6px; margin: 0.5rem 0; border-left: 4px solid #ffc107;">
                <strong>Proactieve notificaties</strong><br/>
                <small>bij nieuwe geschikte mogelijkheden</small>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        user = st.session_state.user_data
        st.markdown(f"""
        <div style="background: linear-gradient(90deg, #d4edda 0%, #c3e6cb 100%); padding: 1.5rem; border-radius: 10px; border: 1px solid #c3e6cb; margin: 1.5rem 0;">
            <h4 style="color: #155724; margin: 0;">Welkom, {user['name']}</h4>
            <p style="color: #155724; margin: 0.5rem 0 0 0; opacity: 0.8;">U bent succesvol ingelogd via DigiD | Sessie beveiligd</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("## Gepersonaliseerde Programma's voor uw Bedrijf")
            
            st.markdown("""
            <div style="background: white; padding: 2rem; border-radius: 12px; border: 1px solid #e0e0e0; margin: 1.5rem 0;">
                <h3 style="color: #154c79; margin: 0 0 1.5rem 0; font-weight: 600;">Programma Filters</h3>
                <p style="color: #666; margin: 0 0 1rem 0; font-size: 0.95rem;">Verfijn uw zoekresultaten met onderstaande criteria voor meer relevante programma's</p>
            </div>
            """, unsafe_allow_html=True)
            
            if 'apply_company_profile' not in st.session_state:
                st.session_state.apply_company_profile = False
            
            if st.session_state.apply_company_profile:
                if user['annual_revenue'] < 300000:
                    default_income = "Laag inkomen (< €30.000)"
                elif user['annual_revenue'] < 700000:
                    default_income = "Midden inkomen (€30.000 - €70.000)"
                else:
                    default_income = "Hoog inkomen (> €70.000)"
                
                default_filing = "Bedrijf/Onderneming"
                default_employment = "Zelfstandig ondernemer"
                default_expense = "Bedrijfskosten"
                default_age = "Midden (31-50 jaar)"
                
                if user['employees'] <= 5:
                    default_household = "2 personen"
                elif user['employees'] <= 15:
                    default_household = "3 personen"
                else:
                    default_household = "4 personen"
                
                st.session_state.apply_company_profile = False
            else:
                default_income = "Alle niveaus"
                default_filing = "Alle rechtsvormen"
                default_employment = "Alle statussen"
                default_expense = "Alle uitgaven"
                default_age = "Alle leeftijden"
                default_household = "Alle groottes"
            
            st.markdown("#### Persoonlijke Criteria")
            filter_col1, filter_col2 = st.columns(2)
            
            with filter_col1:
                st.markdown("**Inkomensniveau**")
                income_level = st.selectbox(
                    "Inkomensniveau",
                    ["Alle niveaus", "Laag inkomen (< €30.000)", "Midden inkomen (€30.000 - €70.000)", "Hoog inkomen (> €70.000)"],
                    index=["Alle niveaus", "Laag inkomen (< €30.000)", "Midden inkomen (€30.000 - €70.000)", "Hoog inkomen (> €70.000)"].index(default_income),
                    key="income_filter",
                    help="Selecteer uw jaarlijkse inkomenscategorie",
                    label_visibility="collapsed"
                )
                
                st.markdown("**Rechtsvorm**")
                filing_status = st.selectbox(
                    "Rechtsvorm",
                    ["Alle rechtsvormen", "Particulier", "Bedrijf/Onderneming", "Stichting/Vereniging"],
                    index=["Alle rechtsvormen", "Particulier", "Bedrijf/Onderneming", "Stichting/Vereniging"].index(default_filing),
                    key="filing_filter",
                    help="Uw organisatievorm voor belastingaangifte",
                    label_visibility="collapsed"
                )
                
                st.markdown("**Leeftijd & Status**")
                age_range = st.selectbox(
                    "Leeftijd & Status",
                    ["Alle leeftijden", "Jong (18-30 jaar)", "Midden (31-50 jaar)", "Senior (50+ jaar)", "Met beperking"],
                    index=["Alle leeftijden", "Jong (18-30 jaar)", "Midden (31-50 jaar)", "Senior (50+ jaar)", "Met beperking"].index(default_age),
                    key="age_filter",
                    help="Uw leeftijdscategorie of speciale status",
                    label_visibility="collapsed"
                )
            
            with filter_col2:
                st.markdown("**Huishoudengrootte**")
                household_size = st.selectbox(
                    "Huishoudengrootte",
                    ["Alle groottes", "1 persoon", "2 personen", "3 personen", "4 personen", "5+ personen"],
                    index=["Alle groottes", "1 persoon", "2 personen", "3 personen", "4 personen", "5+ personen"].index(default_household),
                    key="household_filter",
                    help="Aantal personen in uw huishouden inclusief kinderen",
                    label_visibility="collapsed"
                )
                
                st.markdown("**Arbeidsstatus**")
                employment_status = st.selectbox(
                    "Arbeidsstatus",
                    ["Alle statussen", "In dienst", "Werkzoekend", "Zelfstandig ondernemer", "Student"],
                    index=["Alle statussen", "In dienst", "Werkzoekend", "Zelfstandig ondernemer", "Student"].index(default_employment),
                    key="employment_filter",
                    help="Uw huidige arbeidsmarktpositie",
                    label_visibility="collapsed"
                )
                
                st.markdown("**Type Uitgaven**")
                expense_type = st.selectbox(
                    "Type Uitgaven",
                    ["Alle uitgaven", "Bedrijfskosten", "Persoonlijke kosten", "Apparatuur/Equipment", "Training/Opleiding", "Onderzoek & Ontwikkeling"],
                    index=["Alle uitgaven", "Bedrijfskosten", "Persoonlijke kosten", "Apparatuur/Equipment", "Training/Opleiding", "Onderzoek & Ontwikkeling"].index(default_expense),
                    key="expense_filter",
                    help="Waarvoor heeft u financiering nodig?",
                    label_visibility="collapsed"
                )
            
            col_clear, col_apply, col_info = st.columns([1, 1, 3])
            with col_clear:
                if st.button("Reset Filters", help="Alle filters terugzetten"):
                    if 'current_page' in st.session_state:
                        st.session_state.current_page = 1
                    st.rerun()
            
            with col_apply:
                if st.button("Apply Company Profile", help="Zet filters op basis van uw bedrijfsprofiel", type="primary"):
                    st.session_state.apply_company_profile = True
                    for key in ['income_filter', 'filing_filter', 'age_filter', 'household_filter', 'employment_filter', 'expense_filter']:
                        if key in st.session_state:
                            del st.session_state[key]
                    if 'current_page' in st.session_state:
                        st.session_state.current_page = 1
                    st.success("✅ Filters aangepast op basis van uw bedrijfsprofiel!")
                    st.rerun()
            
            filters = {
                'income_level': 'low' if 'Laag' in income_level else 'medium' if 'Midden' in income_level else 'high' if 'Hoog' in income_level else None,
                'filing_status': 'individual' if 'Particulier' in filing_status else 'business' if 'Bedrijf' in filing_status else 'non-profit' if 'Stichting' in filing_status else None,
                'household_size': '1' if '1 persoon' in household_size else '2' if '2 personen' in household_size else '3' if '3 personen' in household_size else '4' if '4 personen' in household_size else '5+' if '5+' in household_size else None,
                'age_range': 'young' if 'Jong' in age_range else 'middle' if 'Midden' in age_range else 'senior' if 'Senior' in age_range else 'disabled' if 'beperking' in age_range else None,
                'employment_status': 'employed' if 'In dienst' in employment_status else 'unemployed' if 'Werkzoekend' in employment_status else 'self-employed' if 'Zelfstandig' in employment_status else 'student' if 'Student' in employment_status else None,
                'expense_type': 'business' if 'Bedrijfskosten' in expense_type else 'personal' if 'Persoonlijke' in expense_type else 'equipment' if 'Apparatuur' in expense_type else 'training' if 'Training' in expense_type else 'research' if 'Onderzoek' in expense_type else None,
            }
            
            matched_programs = filter_programs(programs, user, filters)
            
            active_filters = [k for k, v in filters.items() if v is not None]
            if active_filters:
                st.markdown(f"""
                <div style="background: white; padding: 1rem; border-radius: 8px; border-left: 4px solid #28a745; margin: 1rem 0;">
                    <strong>Actieve filters:</strong> {len(active_filters)} filter(s) toegepast
                </div>
                """, unsafe_allow_html=True)
            
            if matched_programs:
                programs_per_page = 3
                total_programs = len(matched_programs)
                total_pages = (total_programs + programs_per_page - 1) // programs_per_page
                
                if 'current_page' not in st.session_state:
                    st.session_state.current_page = 1
                
                st.markdown(f"""
                <div style="background: white; padding: 1.5rem; border-radius: 10px; border: 1px solid #d4edda; margin: 1.5rem 0;">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                        <div>
                            <h4 style="color: #155724; margin: 0;">📋 {total_programs} geschikte programma's gevonden</h4>
                            <p style="color: #155724; margin: 0.5rem 0 0 0; opacity: 0.8;">Deze programma's passen perfect bij uw bedrijfsprofiel en geselecteerde criteria</p>
                        </div>
                        <div style="text-align: right;">
                            <span style="color: #6c757d; font-size: 0.9rem; background: #f8f9fa; padding: 0.3rem 0.8rem; border-radius: 20px;">
                                📄 Pagina {st.session_state.current_page} van {total_pages}
                            </span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if total_pages > 1:
                    col_prev, col_pages, col_next = st.columns([1, 3, 1])
                    
                    with col_prev:
                        if st.button("⬅️ Vorige", disabled=(st.session_state.current_page <= 1), key="prev_top", 
                                   help="Ga naar vorige pagina"):
                            st.session_state.current_page -= 1
                            st.rerun()
                    
                    with col_pages:
                        visible_pages = min(7, total_pages)  # Show max 7 page buttons
                        start_page = max(1, st.session_state.current_page - visible_pages // 2)
                        end_page = min(total_pages, start_page + visible_pages - 1)
                        
                        if end_page - start_page < visible_pages - 1:
                            start_page = max(1, end_page - visible_pages + 1)
                        
                        page_cols = st.columns(end_page - start_page + 1)
                        
                        for i, page_num in enumerate(range(start_page, end_page + 1)):
                            with page_cols[i]:
                                if page_num == st.session_state.current_page:
                                    st.markdown(f"""
                                    <div style="background: linear-gradient(135deg, #007bff, #0056b3); 
                                                color: white; 
                                                padding: 0.7rem 1rem; 
                                                text-align: center; 
                                                border-radius: 8px; 
                                                font-weight: bold;
                                                font-size: 1rem;
                                                box-shadow: 0 2px 8px rgba(0,123,255,0.3);
                                                border: 2px solid #007bff;
                                                margin: 0 0.1rem;">
                                        {page_num}
                                    </div>
                                    """, unsafe_allow_html=True)
                                else:
                                    if st.button(f"{page_num}", key=f"page_{page_num}_top", 
                                               help=f"Ga naar pagina {page_num}",
                                               use_container_width=True):
                                        st.session_state.current_page = page_num
                                        st.rerun()
                    
                    with col_next:
                        if st.button("Volgende ➡️", disabled=(st.session_state.current_page >= total_pages), key="next_top",
                                   help="Ga naar volgende pagina"):
                            st.session_state.current_page += 1
                            st.rerun()
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                
                start_idx = (st.session_state.current_page - 1) * programs_per_page
                end_idx = min(start_idx + programs_per_page, total_programs)
                current_page_programs = matched_programs[start_idx:end_idx]
                
                for i, program in enumerate(current_page_programs):
                    match_score = calculate_match_score(program, user)
                    
                    program_name = program.get('long_name', program.get('short_name', 'Onbekende programma'))
                    short_name = program.get('short_name', 'N/A')
                    
                    if match_score >= 80:
                        match_color = "#d4edda"
                        match_text_color = "#155724"
                        border_color = "#28a745"
                    elif match_score >= 60:
                        match_color = "#fff3cd" 
                        match_text_color = "#856404"
                        border_color = "#ffc107"
                    else:
                        match_color = "#f8f9fa"
                        match_text_color = "#6c757d"
                        border_color = "#dee2e6"
                    
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%); 
                                padding: 2rem; 
                                border-radius: 16px; 
                                border-left: 5px solid {border_color}; 
                                margin: 1.5rem 0; 
                                box-shadow: 0 4px 6px rgba(0,0,0,0.07), 0 1px 3px rgba(0,0,0,0.06);
                                transition: all 0.3s ease;">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.5rem;">
                            <div style="flex-grow: 1;">
                                <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                                    <span style="background: {border_color}; color: white; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.75rem; font-weight: bold; margin-right: 1rem;">
                                        {short_name}
                                    </span>
                                    <span style="background: {match_color}; color: {match_text_color}; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.85rem; font-weight: bold;">
                                        🎯 {match_score}% match
                                    </span>
                                </div>
                                <h3 style="color: #154c79; margin: 0; font-size: 1.3rem; font-weight: 600;">{program_name}</h3>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.container():
                        col_a, col_b = st.columns([3, 1])
                        
                        with col_a:
                            st.markdown(f"""
                            <div style="background: #f8f9fa; padding: 1.2rem; border-radius: 12px; margin: 1rem 0; border-left: 4px solid #007bff;">
                                <h5 style="color: #154c79; margin-bottom: 0.8rem; display: flex; align-items: center;">
                                    📄 <span style="margin-left: 0.5rem;">Beschrijving</span>
                                </h5>
                                <p style="margin: 0; color: #495057; line-height: 1.6;">{program.get('description', 'Geen beschrijving beschikbaar')}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            if program.get('criteria'):
                                st.markdown("""
                                <h5 style="color: #154c79; margin: 1.5rem 0 1rem 0; display: flex; align-items: center;">
                                    ✅ <span style="margin-left: 0.5rem;">Geschiktheidscriteria</span>
                                </h5>
                                """, unsafe_allow_html=True)
                                
                                criteria_list = program.get('criteria', [])
                                for i, criterion in enumerate(criteria_list[:4]):
                                    st.markdown(f"""
                                    <div style="background: #e8f5e8; padding: 0.8rem 1.2rem; margin: 0.5rem 0; border-radius: 8px; border-left: 3px solid #28a745;">
                                        <span style="color: #155724; font-weight: 500;">✓ {criterion}</span>
                                    </div>
                                    """, unsafe_allow_html=True)
                                
                                if len(criteria_list) > 4:
                                    st.markdown(f"<p style='color: #6c757d; font-style: italic; margin: 0.5rem 0;'>...en nog {len(criteria_list)-4} andere criteria</p>", unsafe_allow_html=True)
                            
                            if program.get('benefits'):
                                st.markdown("""
                                <h5 style="color: #154c79; margin: 1.5rem 0 1rem 0; display: flex; align-items: center;">
                                    💰 <span style="margin-left: 0.5rem;">Belangrijkste voordelen</span>
                                </h5>
                                """, unsafe_allow_html=True)
                                
                                benefits_list = program.get('benefits', [])
                                for benefit in benefits_list[:4]:
                                    st.markdown(f"""
                                    <div style="background: #fff3cd; padding: 0.8rem 1.2rem; margin: 0.5rem 0; border-radius: 8px; border-left: 3px solid #ffc107;">
                                        <span style="color: #856404; font-weight: 500;">🎁 {benefit}</span>
                                    </div>
                                    """, unsafe_allow_html=True)
                                
                                if len(benefits_list) > 4:
                                    st.markdown(f"<p style='color: #6c757d; font-style: italic; margin: 0.5rem 0;'>...en nog {len(benefits_list)-4} andere voordelen</p>", unsafe_allow_html=True)
                        
                        with col_b:
                            program_key = f"{program.get('short_name', 'program').replace(' ', '_').replace('(', '').replace(')', '')}_{i}"
                            
                            st.markdown(f"""
                            <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 12px; border: 1px solid #dee2e6; margin-top: 1rem; text-align: center;">
                                <h6 style="color: #495057; margin-bottom: 1rem;">Actie ondernemen</h6>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            if st.button("🚀 Subsidie Aanvragen", key=f"apply_{program_key}", type="primary", use_container_width=True):
                                st.success("🎉 Uw aanvraag is succesvol ingediend!")
                                st.info("📧 U ontvangt binnen 2 werkdagen een bevestigingsmail met verdere instructies.")
                                st.balloons()
                            
                            if st.button("📚 Meer Informatie", key=f"info_{program_key}", use_container_width=True):
                                st.info("📞 Voor meer informatie kunt u contact opnemen met Nederlandse overheid of bezoek de officiële website.")
                                
                            st.markdown(f"""
                            <div style="background: #e9ecef; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                                <small style="color: #6c757d;">
                                    <strong>Uitvoerder:</strong><br>Nederlandse overheid<br><br>
                                    <strong>Status:</strong><br>✅ Actief programma<br><br>
                                    <strong>Type:</strong><br>📋 Overheidssubsidie
                                </small>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    st.markdown("---")
                
                if total_pages > 1:
                    st.markdown("<br>", unsafe_allow_html=True)
                    col_prev_b, col_pages_b, col_next_b = st.columns([1, 3, 1])
                    
                    with col_prev_b:
                        if st.button("⬅️ Vorige", disabled=(st.session_state.current_page <= 1), key="prev_bottom",
                                   help="Ga naar vorige pagina"):
                            st.session_state.current_page -= 1
                            st.rerun()
                    
                    with col_pages_b:
                        visible_pages = min(7, total_pages)
                        start_page = max(1, st.session_state.current_page - visible_pages // 2)
                        end_page = min(total_pages, start_page + visible_pages - 1)
                        
                        if end_page - start_page < visible_pages - 1:
                            start_page = max(1, end_page - visible_pages + 1)
                        
                        page_cols_b = st.columns(end_page - start_page + 1)
                        
                        for i, page_num in enumerate(range(start_page, end_page + 1)):
                            with page_cols_b[i]:
                                if page_num == st.session_state.current_page:
                                    st.markdown(f"""
                                    <div style="background: linear-gradient(135deg, #007bff, #0056b3); 
                                                color: white; 
                                                padding: 0.7rem 1rem; 
                                                text-align: center; 
                                                border-radius: 8px; 
                                                font-weight: bold;
                                                font-size: 1rem;
                                                box-shadow: 0 2px 8px rgba(0,123,255,0.3);
                                                border: 2px solid #007bff;
                                                margin: 0 0.1rem;">
                                        {page_num}
                                    </div>
                                    """, unsafe_allow_html=True)
                                else:
                                    if st.button(f"{page_num}", key=f"page_{page_num}_bottom",
                                               help=f"Ga naar pagina {page_num}",
                                               use_container_width=True):
                                        st.session_state.current_page = page_num
                                        st.rerun()
                    
                    with col_next_b:
                        if st.button("Volgende ➡️", disabled=(st.session_state.current_page >= total_pages), key="next_bottom",
                                   help="Ga naar volgende pagina"):
                            st.session_state.current_page += 1
                            st.rerun()
                    
                    st.markdown(f"""
                    <div style="text-align: center; margin: 1rem 0; color: #6c757d;">
                        <small>
                            📄 Toont programma's {start_idx + 1}-{end_idx} van {total_programs} totaal | 
                            📊 {programs_per_page} programma's per pagina
                        </small>
                    </div>
                    """, unsafe_allow_html=True)
            
            else:
                st.markdown("""
                <div style="background: white; padding: 2rem; border-radius: 12px; border: 1px solid #ffeaa7; margin: 1.5rem 0; text-align: center;">
                    <h4 style="color: #856404; margin: 0 0 1rem 0;">🔍 Geen geschikte programma's gevonden</h4>
                    <p style="color: #856404; margin: 0;">Met uw huidige criteria en filters zijn er momenteel geen passende subsidies beschikbaar.</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("### 💡 Wat kunt u doen?")
                col_tip1, col_tip2, col_tip3 = st.columns(3)
                
                with col_tip1:
                    st.markdown("""
                    **🔄 Pas filters aan**  
                    Probeer minder specifieke criteria of verwijder enkele filters om meer resultaten te krijgen.
                    """)
                
                with col_tip2:
                    st.markdown("""
                    **📞 Persoonlijk advies**  
                    Neem contact op met onze specialisten voor maatwerk subsidieadvies.
                    """)
                
                with col_tip3:
                    st.markdown("""
                    **🔔 Notificaties**  
                    Meld u aan voor updates over nieuwe programma's die bij uw profiel passen.
                    """)
            
            st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 15px; border: 1px solid #ff6b6b; margin: 2rem 0 1rem 0;">
                <h3 style="color: #ff6b6b; margin: 0;">Lokale Projectkansen</h3>
                <p style="color: #666; margin: 0.5rem 0 0 0;">Exclusieve samenwerkingsmogelijkheden in uw regio</p>
            </div>
            """, unsafe_allow_html=True)
            
            if user['location'] == "Den Haag":
                st.markdown("""
                <div style="background: white; padding: 2rem; border-radius: 12px; border: 1px solid #fecaca; margin: 1rem 0;">
                    <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                        <h4 style="color: #dc2626; margin: 0; flex-grow: 1;">Warmtenet Den Haag - Partner Gezocht</h4>
                        <span style="background: #dc2626; color: white; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.8rem; font-weight: bold;">
                            URGENT
                        </span>
                    </div>
                    <p style="color: #7f1d1d; margin: 0;">De gemeente Den Haag zoekt innovatieve bedrijven voor deelname aan het grootschalige warmtenet project voor duurzame stadsverwarming.</p>
                </div>
                """, unsafe_allow_html=True)
                
                col_proj1, col_proj2 = st.columns([3, 1])
                with col_proj1:
                    st.markdown("""
                    **Gezocht:** Bedrijven met technische expertise in warmtenetwerken  
                    **Investeringsbereik:** €500.000 - €2.000.000  
                    **Aanmeldingsdeadline:** 15 december 2024  
                    **Vereisten:** Min. 5 jaar ervaring, ISO certificering  
                    **Voordelen:** Langetermijn contract + subsidie tot €200.000
                    """)
                
                with col_proj2:
                    st.markdown("<br/>", unsafe_allow_html=True)
                    if st.button("Interesse Tonen", type="primary", use_container_width=True):
                        st.balloons()
                        st.success("Uw interesse is geregistreerd!")
                        st.info("De gemeente Den Haag neemt binnen 1 week contact met u op voor een vrijblijvend gesprek.")
                    
                    if st.button("Project Details", use_container_width=True):
                        st.info("Gedetailleerde projectinformatie wordt naar uw email verstuurd.")
        
        with col2:
            st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 15px; border: 1px solid #154c79; margin-bottom: 1.5rem;">
                <h3 style="color: #154c79; margin: 0 0 1rem 0;">Uw Bedrijfsprofiel</h3>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="background: white; padding: 1.5rem; border-radius: 10px; border: 1px solid #e3e8ef; margin-bottom: 1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                <div style="margin-bottom: 0.75rem;"><strong>Bedrijfsnaam</strong><br/><span style="color: #666;">{user['company']}</span></div>
                <div style="margin-bottom: 0.75rem;"><strong>Vestigingsplaats</strong><br/><span style="color: #666;">{user['location']}</span></div>
                <div style="margin-bottom: 0.75rem;"><strong>Aantal werknemers</strong><br/><span style="color: #666;">{user['employees']} medewerkers</span></div>
                <div style="margin-bottom: 0.75rem;"><strong>Jaaromzet</strong><br/><span style="color: #666;">€{user['annual_revenue']:,}</span></div>
                <div><strong>Bedrijfssector</strong><br/><span style="color: #666;">{user['sector']}</span></div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 15px; border: 1px solid #28a745; margin-bottom: 1.5rem;">
                <h4 style="color: #28a745; margin: 0 0 1rem 0;">Uw Subsidie Dashboard</h4>
            </div>
            """, unsafe_allow_html=True)
            
            total_programs = len(programs)
            matched_count = len(filter_programs(programs, user))
            match_percentage = int((matched_count / total_programs) * 100) if total_programs > 0 else 0
            
            col_met1, col_met2 = st.columns(2)
            with col_met1:
                st.markdown(f"""
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; text-align: center; border: 2px solid #dee2e6;">
                    <div style="font-size: 1.5rem; font-weight: bold; color: #154c79;">{total_programs}</div>
                    <div style="color: #666; font-size: 0.85rem;">Beschikbare programma's</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_met2:
                st.markdown(f"""
                <div style="background: #e8f5e8; padding: 1rem; border-radius: 8px; text-align: center; border: 2px solid #c3e6cb;">
                    <div style="font-size: 1.5rem; font-weight: bold; color: #155724;">{matched_count}</div>
                    <div style="color: #155724; font-size: 0.85rem;">Voor u geschikt</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="background: #fff3cd; padding: 1rem; border-radius: 8px; text-align: center; border: 2px solid #ffeaa7; margin-top: 0.5rem;">
                <div style="font-size: 1.5rem; font-weight: bold; color: #856404;">{match_percentage}%</div>
                <div style="color: #856404; font-size: 0.85rem;">Match percentage</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 15px; border: 1px solid #6f42c1; margin: 1.5rem 0;">
                <h4 style="color: #6f42c1; margin: 0 0 1rem 0;">Recente Activiteiten</h4>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 10px; border: 1px solid #e3e8ef; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                <div style="margin-bottom: 1rem; padding: 0.75rem; background: white; border-radius: 6px; border-left: 4px solid #28a745;">
                    <strong>Profiel bijgewerkt</strong><br/>
                    <small style="color: #666;">Vandaag om 14:30</small>
                </div>
                <div style="margin-bottom: 1rem; padding: 0.75rem; background: white; border-radius: 6px; border-left: 4px solid #17a2b8;">
                    <strong>3 nieuwe programma's toegevoegd</strong><br/>
                    <small style="color: #666;">Gisteren om 09:15</small>
                </div>
                <div style="padding: 0.75rem; background: white; border-radius: 6px; border-left: 4px solid #ffc107;">
                    <strong>Aanvraagdeadline nadert</strong><br/>
                    <small style="color: #666;">Innovation Credit: 31 december</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br/>", unsafe_allow_html=True)
            if st.button("Profiel Bewerken", use_container_width=True):
                st.info("Profiel bewerking wordt binnenkort beschikbaar gesteld.")
            
            if st.button("Email Notificaties", use_container_width=True):
                st.success("U ontvangt voortaan email updates over nieuwe geschikte programma's!")

if __name__ == "__main__":
    main()