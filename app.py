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
    st.sidebar.header("DigiD Inloggen")
    
    # Simple fake DigiD authentication - no external server needed
    
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        st.sidebar.info("Log in met DigiD voor toegang tot gepersonaliseerde overheidsprogramma's")
        
        # Single DigiD login button - fake login as King Arthur
        if st.sidebar.button("Inloggen met DigiD", type="primary", use_container_width=True):
            # Show realistic DigiD process
            with st.sidebar:
                st.info("Doorverwijzen naar DigiD...")
                time.sleep(0.5)
                st.success("Verbinding met DigiD servers...")
                time.sleep(0.5)
                st.success("Authenticatie succesvol!")
            
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

def filter_programs(programs, user_data, filters=None):
    """Filter programs based on user criteria and additional filters"""
    filtered = []
    
    for program in programs:
        # Check location eligibility
        if user_data['location'] not in program.get('location', []):
            continue
            
        # Check employee count (if max_employees exists)
        if 'max_employees' in program:
            if user_data['employees'] > program['max_employees']:
                continue
            
        # Check funding amount vs revenue (basic eligibility)
        if program.get('funding_amount', 0) > user_data['annual_revenue']:
            continue
            
        # Check sector
        if user_data['sector'] not in program.get('sectors', []):
            continue
            
        # Apply additional filters if provided
        if filters:
            # Income Level filter
            if filters.get('income_level') and filters['income_level'] != 'Все':
                program_income_req = program.get('income_requirement', 'medium')
                if program_income_req != filters['income_level'].lower():
                    continue
                    
            # Filing Status filter
            if filters.get('filing_status') and filters['filing_status'] != 'Все':
                program_filing = program.get('filing_status', ['individual', 'business'])
                if filters['filing_status'].lower() not in program_filing:
                    continue
                    
            # Household Size filter
            if filters.get('household_size') and filters['household_size'] != 'Все':
                min_size = program.get('min_household_size', 1)
                max_size = program.get('max_household_size', 10)
                size = int(filters['household_size'])
                if not (min_size <= size <= max_size):
                    continue
                    
            # Age filter
            if filters.get('age_range') and filters['age_range'] != 'Все':
                program_age = program.get('age_requirement', 'all')
                if program_age != 'all' and program_age != filters['age_range'].lower():
                    continue
                    
            # Employment Status filter
            if filters.get('employment_status') and filters['employment_status'] != 'Все':
                program_employment = program.get('employment_status', ['employed', 'unemployed', 'self-employed'])
                if filters['employment_status'].lower() not in program_employment:
                    continue
                    
            # Expense Type filter
            if filters.get('expense_type') and filters['expense_type'] != 'Все':
                program_expenses = program.get('eligible_expenses', ['business', 'personal', 'equipment'])
                if filters['expense_type'].lower() not in program_expenses:
                    continue
            
        filtered.append(program)
    
    return filtered

def calculate_match_score(program, user_data):
    """Calculate match percentage for a program"""
    score = 0
    max_score = 4
    
    # Location match (weight: 1)
    if user_data['location'] in program.get('location', []):
        score += 1
    
    # Employee range match (weight: 1)  
    if 'max_employees' in program and user_data['employees'] <= program['max_employees']:
        score += 1
    
    # Funding eligibility (weight: 1)
    if program.get('funding_amount', 0) <= user_data['annual_revenue']:
        score += 1
    
    # Sector match (weight: 1)
    if user_data['sector'] in program.get('sectors', []):
        score += 1
    
    return int((score / max_score) * 100)

def main():
    # Set page config
    st.set_page_config(
        page_title="Ondernemersloket Nederland", 
        page_icon="⚖️", 
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Set white background
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
    
    # DigiD Authentication
    digid_login()
    
    # Main header
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
        
        # Official government notice
        st.markdown("""
        <div style="background: #fff3cd; border: 1px solid #ffeaa7; padding: 1.5rem; border-radius: 8px; margin: 1.5rem 0;">
            <h4 style="color: #856404; margin: 0 0 0.5rem 0;">Veilige DigiD-authenticatie vereist</h4>
            <p style="color: #856404; margin: 0;">Log in met DigiD voor toegang tot gepersonaliseerde overheidsprogramma's en projectkansen.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            ## Wat bieden wij
            
            **Gepersonaliseerde programma matching**  
            Op basis van uw bedrijfsprofiel en specifieke behoeften
            
            **Lokale projectkansen**  
            Warmtenetten, infrastructuurprojecten en publiek-private samenwerkingen
            
            **Real-time updates**  
            Automatische notificaties over nieuwe subsidies en regelingen
            
            **Directe communicatie**  
            Rechtstreeks contact met relevante overheidsinstanties
            
            ## Beschikbare Programma's
            """)
            
            # Show first few programs as preview
            for program in programs[:3]:
                with st.expander(f"**{program['name']}** | {program.get('contact', 'Nederlandse overheid')}", expanded=False):
                    st.markdown(f"**Budget:** €{program.get('funding_amount', 0):,}")
                    if 'max_employees' in program:
                        st.markdown(f"**Max werknemers:** {program['max_employees']}")
                    st.markdown(f"**Beschikbare locaties:** {', '.join(program.get('location', []))}")
                    st.markdown(f"**Doelsectoren:** {', '.join(program.get('sectors', []))}")
                    st.markdown(f"**Beschrijving:** {program['description']}")
        
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
            
            # Benefits preview
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
        # User is logged in - show personalized experience
        user = st.session_state.user_data
        st.markdown(f"""
        <div style="background: linear-gradient(90deg, #d4edda 0%, #c3e6cb 100%); padding: 1.5rem; border-radius: 10px; border: 1px solid #c3e6cb; margin: 1.5rem 0;">
            <h4 style="color: #155724; margin: 0;">Welkom, {user['name']}</h4>
            <p style="color: #155724; margin: 0.5rem 0 0 0; opacity: 0.8;">U bent succesvol ingelogd via DigiD | Sessie beveiligd</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create main layout
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("## Gepersonaliseerde Programma's voor uw Bedrijf")
            
            # Add professional filtering interface
            st.markdown("""
            <div style="background: white; padding: 2rem; border-radius: 12px; border: 1px solid #e0e0e0; margin: 1.5rem 0;">
                <h3 style="color: #154c79; margin: 0 0 1.5rem 0; font-weight: 600;">Programma Filters</h3>
                <p style="color: #666; margin: 0 0 1rem 0; font-size: 0.95rem;">Verfijn uw zoekresultaten met onderstaande criteria voor meer relevante programma's</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Create professional filter layout
            st.markdown("#### Persoonlijke Criteria")
            filter_col1, filter_col2 = st.columns(2)
            
            with filter_col1:
                st.markdown("**Inkomensniveau**")
                income_level = st.selectbox(
                    "",
                    ["Alle niveaus", "Laag inkomen (< €30.000)", "Midden inkomen (€30.000 - €70.000)", "Hoog inkomen (> €70.000)"],
                    key="income_filter",
                    help="Selecteer uw jaarlijkse inkomenscategorie"
                )
                
                st.markdown("**Rechtsvorm**")
                filing_status = st.selectbox(
                    "",
                    ["Alle rechtsvormen", "Particulier", "Bedrijf/Onderneming", "Stichting/Vereniging"],
                    key="filing_filter",
                    help="Uw organisatievorm voor belastingaangifte"
                )
                
                st.markdown("**Leeftijd & Status**")
                age_range = st.selectbox(
                    "",
                    ["Alle leeftijden", "Jong (18-30 jaar)", "Midden (31-50 jaar)", "Senior (50+ jaar)", "Met beperking"],
                    key="age_filter",
                    help="Uw leeftijdscategorie of speciale status"
                )
            
            with filter_col2:
                st.markdown("**Huishoudengrootte**")
                household_size = st.selectbox(
                    "",
                    ["Alle groottes", "1 persoon", "2 personen", "3 personen", "4 personen", "5+ personen"],
                    key="household_filter",
                    help="Aantal personen in uw huishouden inclusief kinderen"
                )
                
                st.markdown("**Arbeidsstatus**")
                employment_status = st.selectbox(
                    "",
                    ["Alle statussen", "In dienst", "Werkzoekend", "Zelfstandig ondernemer", "Student"],
                    key="employment_filter",
                    help="Uw huidige arbeidsmarktpositie"
                )
                
                st.markdown("**Type Uitgaven**")
                expense_type = st.selectbox(
                    "",
                    ["Alle uitgaven", "Bedrijfskosten", "Persoonlijke kosten", "Apparatuur/Equipment", "Training/Opleiding", "Onderzoek & Ontwikkeling"],
                    key="expense_filter",
                    help="Waarvoor heeft u financiering nodig?"
                )
            
            # Clear filters button
            col_clear, col_info = st.columns([1, 4])
            with col_clear:
                if st.button("Reset Filters", help="Alle filters terugzetten"):
                    st.rerun()
            
            # Apply filters with Dutch values
            filters = {
                'income_level': 'low' if 'Laag' in income_level else 'medium' if 'Midden' in income_level else 'high' if 'Hoog' in income_level else None,
                'filing_status': 'individual' if 'Particulier' in filing_status else 'business' if 'Bedrijf' in filing_status else 'non-profit' if 'Stichting' in filing_status else None,
                'household_size': '1' if '1 persoon' in household_size else '2' if '2 personen' in household_size else '3' if '3 personen' in household_size else '4' if '4 personen' in household_size else '5+' if '5+' in household_size else None,
                'age_range': 'young' if 'Jong' in age_range else 'middle' if 'Midden' in age_range else 'senior' if 'Senior' in age_range else 'disabled' if 'beperking' in age_range else None,
                'employment_status': 'employed' if 'In dienst' in employment_status else 'unemployed' if 'Werkzoekend' in employment_status else 'self-employed' if 'Zelfstandig' in employment_status else 'student' if 'Student' in employment_status else None,
                'expense_type': 'business' if 'Bedrijfskosten' in expense_type else 'personal' if 'Persoonlijke' in expense_type else 'equipment' if 'Apparatuur' in expense_type else 'training' if 'Training' in expense_type else 'research' if 'Onderzoek' in expense_type else None,
            }
            
            # Filter programs for this user with additional filters
            matched_programs = filter_programs(programs, user, filters)
            
            # Show active filters summary
            active_filters = [k for k, v in filters.items() if v is not None]
            if active_filters:
                st.markdown(f"""
                <div style="background: white; padding: 1rem; border-radius: 8px; border-left: 4px solid #28a745; margin: 1rem 0;">
                    <strong>Actieve filters:</strong> {len(active_filters)} filter(s) toegepast
                </div>
                """, unsafe_allow_html=True)
            
            if matched_programs:
                st.markdown(f"""
                <div style="background: white; padding: 1.5rem; border-radius: 10px; border: 1px solid #d4edda; margin: 1.5rem 0;">
                    <h4 style="color: #155724; margin: 0;">{len(matched_programs)} geschikte programma's gevonden</h4>
                    <p style="color: #155724; margin: 0.5rem 0 0 0; opacity: 0.8;">Deze programma's passen perfect bij uw bedrijfsprofiel en geselecteerde criteria</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Sort by match score
                for i, program in enumerate(matched_programs):
                    match_score = calculate_match_score(program, user)
                    
                    # Create professional program card
                    st.markdown(f"""
                    <div style="background: white; padding: 1.5rem; border-radius: 12px; border: 1px solid #e3e8ef; margin: 1rem 0; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                        <div style="display: flex; justify-content: between; align-items: center; margin-bottom: 1rem;">
                            <h4 style="color: #154c79; margin: 0; flex-grow: 1;">{program['name']}</h4>
                            <span style="background: #e8f5e8; color: #155724; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.85rem; font-weight: bold;">
                                {match_score}% match
                            </span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.container():
                        col_a, col_b = st.columns([3, 1])
                        
                        with col_a:
                            st.markdown(f"""
                            **Maximale subsidie:** €{program.get('funding_amount', 0):,}  
                            **Beschrijving:** {program['description']}  
                            **Uitvoerende organisatie:** {program.get('contact', 'Nederlandse overheid')}  
                            **Aanvraagdeadline:** {program.get('deadline', 'Doorlopend open')}
                            """)
                            
                            # Show eligibility criteria
                            if any([program.get('max_employees'), program.get('min_employees'), program.get('sectors')]):
                                st.markdown("**Geschiktheidscriteria:**")
                                criteria = []
                                if program.get('max_employees'):
                                    criteria.append(f"Max {program['max_employees']} werknemers")
                                if program.get('min_employees'):
                                    criteria.append(f"Min {program['min_employees']} werknemers")
                                if program.get('sectors'):
                                    criteria.append(f"Sectoren: {', '.join(program['sectors'])}")
                                st.markdown("• " + " • ".join(criteria))
                        
                        with col_b:
                            # Use name as key since id might not exist
                            program_key = program.get('id', program['name'].replace(' ', '_').replace('(', '').replace(')', ''))
                            
                            st.markdown("<br>", unsafe_allow_html=True)
                            if st.button(f"Subsidie Aanvragen", key=f"apply_{program_key}", type="primary", use_container_width=True):
                                st.success("Uw aanvraag is succesvol ingediend!")
                                st.info("U ontvangt binnen 2 werkdagen een bevestigingsmail met verdere instructies.")
                                st.balloons()
                            
                            if st.button(f"Meer Informatie", key=f"info_{program_key}", use_container_width=True):
                                st.info(f"Voor meer informatie kunt u contact opnemen met {program.get('contact', 'de uitvoerende organisatie')} of bezoek de officiële website.")
                    
                    st.markdown("---")
            
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
            
            # Local projects section with professional styling
            st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 15px; border: 1px solid #ff6b6b; margin: 2rem 0 1rem 0;">
                <h3 style="color: #ff6b6b; margin: 0;">Lokale Projectkansen</h3>
                <p style="color: #666; margin: 0.5rem 0 0 0;">Exclusieve samenwerkingsmogelijkheden in uw regio</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Mock local project for Den Haag
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
            # Professional user profile card
            st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 15px; border: 1px solid #154c79; margin-bottom: 1.5rem;">
                <h3 style="color: #154c79; margin: 0 0 1rem 0;">Uw Bedrijfsprofiel</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Business info in cards
            st.markdown(f"""
            <div style="background: white; padding: 1.5rem; border-radius: 10px; border: 1px solid #e3e8ef; margin-bottom: 1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                <div style="margin-bottom: 0.75rem;"><strong>Bedrijfsnaam</strong><br/><span style="color: #666;">{user['company']}</span></div>
                <div style="margin-bottom: 0.75rem;"><strong>Vestigingsplaats</strong><br/><span style="color: #666;">{user['location']}</span></div>
                <div style="margin-bottom: 0.75rem;"><strong>Aantal werknemers</strong><br/><span style="color: #666;">{user['employees']} medewerkers</span></div>
                <div style="margin-bottom: 0.75rem;"><strong>Jaaromzet</strong><br/><span style="color: #666;">€{user['annual_revenue']:,}</span></div>
                <div><strong>Bedrijfssector</strong><br/><span style="color: #666;">{user['sector']}</span></div>
            </div>
            """, unsafe_allow_html=True)
            
            # Statistics dashboard
            st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 15px; border: 1px solid #28a745; margin-bottom: 1.5rem;">
                <h4 style="color: #28a745; margin: 0 0 1rem 0;">Uw Subsidie Dashboard</h4>
            </div>
            """, unsafe_allow_html=True)
            
            total_programs = len(programs)
            matched_count = len(filter_programs(programs, user))
            match_percentage = int((matched_count / total_programs) * 100) if total_programs > 0 else 0
            
            # Metrics in professional cards
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
            
            # Activity feed
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
            
            # Quick action buttons
            st.markdown("<br/>", unsafe_allow_html=True)
            if st.button("Profiel Bewerken", use_container_width=True):
                st.info("Profiel bewerking wordt binnenkort beschikbaar gesteld.")
            
            if st.button("Email Notificaties", use_container_width=True):
                st.success("U ontvangt voortaan email updates over nieuwe geschikte programma's!")

if __name__ == "__main__":
    main()