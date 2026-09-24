import streamlit as st
import pandas as pd
import urllib.parse

# ==========================================
# 🎨 1. CORE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="GTrade Surf - Global Peer-to-Peer Marketplace",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injecting Custom Dynamic Branding & CSS layout anchors
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0px;
    }
    .brand-trade {
        color: #0088FF;
    }
    .subtitle {
        text-align: center;
        font-size: 1.1rem;
        color: #888888;
        margin-bottom: 2rem;
    }
    .pro-badge {
        background-color: #FFD700;
        color: #000000;
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: bold;
        font-size: 0.8rem;
    }
    .free-badge {
        background-color: #E0E0E0;
        color: #333333;
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: bold;
        font-size: 0.8rem;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 🗄️ 2. SIMULATED LIVE DATABASE SYSTEM
# ==========================================
# Initializing database tables inside memory state parameters
if "users_db" not in st.session_state:
    st.session_state.users_db = {}

if "listings_db" not in st.session_state:
    # Starts completely clean and empty as requested
    st.session_state.listings_db = pd.DataFrame(columns=[
        "Listing_ID", "User_ID", "User_Name", "User_Phone", 
        "Post_Type", "Item_Title", "Condition", "Estimated_Value", 
        "Media_URL", "Status"
    ])

if "current_user" not in st.session_state:
    st.session_state.current_user = None

# Master Administrative Access Passkey configuration
ADMIN_PASSKEY = "mastershalom7"

# ==========================================
# 📱 NAVIGATION SIDEBAR CONTROL PANEL
# ==========================================
st.sidebar.markdown("<h2 style='text-align: center;'>🌐 GTrade Menu</h2>", unsafe_allow_html=True)

# Active Login State Indicator
if st.session_state.current_user:
    u_data = st.session_state.users_db[st.session_state.current_user]
    badge = "<span class='pro-badge'>PRO STOREFRONT</span>" if u_data["is_premium"] else "<span class='free-badge'>FREE TIER</span>"
    st.sidebar.markdown(f"""
        <div style='background-color: rgba(0, 136, 255, 0.1); padding: 10px; border-radius: 8px; margin-bottom: 15px;'>
            <p style='margin:0; font-size:0.9rem; color:#888;'>Logged in as:</p>
            <p style='margin:0; font-weight:bold; font-size:1.1rem;'>{u_data['full_name']}</p>
            <p style='margin:5px 0 0 0;'>{badge}</p>
        </div>
    """, unsafe_allow_html=True)
else:
    st.sidebar.warning("⚠️ No active user session. Please sign up or log in via the Account Portal tab.")

app_mode = st.sidebar.radio("Navigate to:", [
    "🏠 Welcome Screen", 
    "🏄 Surfing Feed", 
    "📦 Post an Item", 
    "👤 Account Portal",
    "🚀 Get Your Launch Copy",
    "⚖️ Legal Center",
    "🔒 Admin Command Center"
])

# ==========================================
# 🏠 MODE 1: WELCOME SCREEN & MARKETING
# ==========================================
if app_mode == "🏠 Welcome Screen":
    st.markdown("<h1 class='main-title'>G<span class='brand-trade'>Trade</span> Surf</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>The Ultimate Hyper-Localized Global Commerce Network</p>", unsafe_allow_html=True)
    
    st.image("https://images.unsplash.com/photo-1557804506-669a67965ba0?auto=format&fit=crop&w=1200&q=80", use_container_width=True)
    
    st.markdown("### 💡 Why GTrade Surf?")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 🏄 The Infinite Surf")
        st.write("Stop browsing sterile e-commerce rows. Surf an interactive media feed designed like social media to instantly uncover rare items globally.")
        
    with col2:
        st.markdown("#### 🔄 Have vs. Want Strategy")
        st.write("Declare what you own (`HAVE`) or request what you desperately need (`WANT`). Our data matrix connects loops to facilitate direct value swaps.")
        
    with col3:
        st.markdown("#### 🛡️ Trust Checkpoint Layers")
        st.write("Bypass international shipping friction. Transactions leverage secure local verification hubs and verified traveler middle-mile runners.")

# ==========================================
# 🏄 MODE 2: THE SURFING FEED (DUAL-TAB RESYNCHRONIZATION)
# ==========================================
elif app_mode == "🏄 Surfing Feed":
    st.markdown("## 🏄 The Global Surfing Feed")
    st.write("Discover items listed by active traders across our network.")
    
    df = st.session_state.listings_db
    active_listings = df[df["Status"] == "Active"]
    
    # Establish separate display grids via Tabs
    tab_have, tab_want = st.tabs(["🛒 Available to Buy/Swap (HAVEs)", "🔍 Items Wanted (WANTs)"])
    
    with tab_have:
        haves = active_listings[active_listings["Post_Type"] == "HAVE"]
        if haves.empty:
            st.info("There are currently no items available to swap or buy. Be the first to post what you HAVE!")
        else:
            # Create a 3-column row grid layout
            cols = st.columns(3)
            for idx, row in haves.reset_index().iterrows():
                col_target = cols[idx % 3]
                with col_target:
                    with st.container(border=True):
                        if row["Media_URL"]:
                            st.image(row["Media_URL"], use_container_width=True)
                        else:
                            st.image("https://via.placeholder.com/300x200?text=No+Image+Provided", use_container_width=True)
                        
                        st.markdown(f"### {row['Item_Title']}")
                        st.markdown(f"**Value:** ${row['Estimated_Value']} USD | **Condition:** {row['Condition']}")
                        st.caption(f"📍 Posted by: {row['User_Name']}")
                        
                        # WhatsApp Dynamic Compiler Engine
                        encoded_msg = urllib.parse.quote(f"Hey! I saw your listing for '{row['Item_Title']}' on GTrade. Is it still available?")
                        wa_url = f"https://wa.me/{row['User_Phone']}?text={encoded_msg}"
                        
                        st.markdown(f'<a href="{wa_url}" target="_blank"><button style="width:100%; padding:10px; background-color:#25D366; color:white; border:none; border-radius:4px; font-weight:bold; cursor:pointer;">💬 Message Trader</button></a>', unsafe_allow_html=True)

    with tab_want:
        wants = active_listings[active_listings["Post_Type"] == "WANT"]
        if wants.empty:
            st.info("The requested demand pool is empty. Post what you are looking for so traders can find you!")
        else:
            cols = st.columns(3)
            for idx, row in wants.reset_index().iterrows():
                col_target = cols[idx % 3]
                with col_target:
                    with st.container(border=True):
                        if row["Media_URL"]:
                            st.image(row["Media_URL"], use_container_width=True)
                        st.markdown(f"### {row['Item_Title']}")
                        st.markdown(f"**Target Value:** ${row['Estimated_Value']} USD | **Desired Condition:** {row['Condition']}")
                        st.caption(f"📍 Wanted by: {row['User_Name']}")
                        
                        encoded_msg = urllib.parse.quote(f"Hey! I saw your request for '{row['Item_Title']}' on GTrade. I think I have exactly what you need!")
                        wa_url = f"https://wa.me/{row['User_Phone']}?text={encoded_msg}"
                        
                        st.markdown(f'<a href="{wa_url}" target="_blank"><button style="width:100%; padding:10px; background-color:#0088FF; color:white; border:none; border-radius:4px; font-weight:bold; cursor:pointer;">💬 Supply Item</button></a>', unsafe_allow_html=True)

# ==========================================
# 📦 MODE 3: POST AN ITEM (ENFORCED STRATEGIC FENCES)
# ==========================================
elif app_mode == "📦 Post an Item":
    st.markdown("## 📦 Publish a New Listing")
    
    if not st.session_state.current_user:
        st.error("🛑 Registration Required: You must register or log in via the Account Portal before publishing listings.")
    else:
        user_id = st.session_state.current_user
        user_data = st.session_state.users_db[user_id]
        
        # Enforce structural quota validation framework
        df = st.session_state.listings_db
        user_active_count = len(df[(df["User_ID"] == user_id) & (df["Status"] == "Active")])
        
        is_premium = user_data["is_premium"]
        
        if not is_premium and user_active_count >= 5:
            st.error(f"🛑 Quota Enforced: You have reached the limit of {user_active_count}/5 active posts allowed on our Free Tier.")
            st.info("💡 To list unlimited inventory and boost visibility globally, navigate to the Account Portal and activate your PRO Storefront.")
        else:
            if not is_premium:
                st.warning(f"⚠️ Free Account Capacity Status: {user_active_count}/5 active posts utilized.")
            else:
                st.success("🌟 Premium Account Active: Unlimited product upload slot unlocked.")
                
            with st.form("listing_form"):
                p_type = st.selectbox("I want to declare a:", ["HAVE", "WANT"])
                title = st.text_input("Product Title / Name (e.g., Apple iPhone 15 Pro Max)")
                cond = st.selectbox("Item Condition Rating:", ["New", "Like New", "Used - Good", "Used - Fair"])
                val = st.number_input("Estimated Value Evaluation ($ USD)", min_value=1, value=50)
                img = st.text_input("Product Photo URL Link (Leave blank for placeholder display)")
                
                submitted = st.form_submit_button("Publish Storefront Listing")
                
                if submitted:
                    if not title:
                        st.error("Validation Error: Item title cannot be empty.")
                    else:
                        # Append metadata object straight to master matrix row configuration
                        new_id = len(st.session_state.listings_db) + 1
                        new_row = {
                            "Listing_ID": new_id,
                            "User_ID": user_id,
                            "User_Name": user_data["full_name"],
                            "User_Phone": user_data["phone"],
                            "Post_Type": p_type,
                            "Item_Title": title,
                            "Condition": cond,
                            "Estimated_Value": val,
                            "Media_URL": img if img else None,
                            "Status": "Active"
                        }
                        st.session_state.listings_db = pd.concat([
                            st.session_state.listings_db, 
                            pd.DataFrame([new_row])
                        ], ignore_index=True)
                        st.success(f"🎉 Success! '{title}' has been successfully broadcast live to the global Surfing Feed.")

# ==========================================
# 👤 MODE 4: ACCOUNT PORTAL & BILLING SIMULATOR
# ==========================================
elif app_mode == "👤 Account Portal":
    st.markdown("## 👤 User Account Control Portal")
    
    col_reg, col_bill = st.columns(2)
    
    with col_reg:
        st.markdown("### 🪪 Live Registration Framework")
        reg_name = st.text_input("Full Name / Vendor Title")
        reg_phone = st.text_input("International Phone Number (Include country code, e.g., 2348012345678 or 14151234567)")
        reg_city = st.text_input("Current Destination Hub City (e.g., Lagos, Tokyo, London)")
        
        if st.button("Complete Global Signup"):
            if not reg_name or not reg_phone or not reg_city:
                st.error("Validation Failure: All identity setup profile values must be provided.")
            else:
                # Sanitize phone numerical configuration string
                clean_phone = reg_phone.replace("+", "").replace("-", "").strip()
                st.session_state.users_db[clean_phone] = {
                    "full_name": reg_name,
                    "phone": clean_phone,
                    "city": reg_city,
                    "is_premium": False
                }
                st.session_state.current_user = clean_phone
                st.success(f"🎯 Welcome {reg_name}! Profile securely instantiated on the network ledger.")
                st.rerun()

    with col_bill:
        st.markdown("### 💳 Premium Billing Simulation")
        if not st.session_state.current_user:
            st.info("Log in or create a profile to test the integrated payment workflows.")
        else:
            user_id = st.session_state.current_user
            user_data = st.session_state.users_db[user_id]
            
            if user_data["is_premium"]:
                st.markdown("""
                    <div style='border: 2px solid #FFD700; padding: 20px; border-radius: 8px; text-align: center; background-color: rgba(255, 215, 0, 0.05);'>
                        <h4 style='color: #FFD700; margin: 0;'>🌟 PRO ACCOUNT STATUS ACTIVATED</h4>
                        <p style='margin: 10px 0 0 0;'>You have unlimited product upload slots and maximum feed exposure hooks.</p>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("Downgrade to Free Tier for Testing"):
                    st.session_state.users_db[user_id]["is_premium"] = False
                    st.success("Account status downgraded successfully.")
                    st.rerun()
            else:
                st.markdown("""
                    <div style='border: 1px solid #E0E0E0; padding: 20px; border-radius: 8px;'>
                        <h4>🚀 Go Pro Storefront</h4>
                        <p>Unlock premium capabilities to optimize cross-border trading:</p>
                        <ul>
                            <li><b>Unlimited Active Uploads</b> (Bypass the 5-item constraint)</li>
                            <li><b>Global Surfing Boost</b> (Pinned profile visibility)</li>
                            <li><b>Verified Trader Verification Badge</b></li>
                        </ul>
                        <p style='font-size: 1.2rem; font-weight: bold; color: #0088FF;'>Price: $9.00 USD / Monthly</p>
                    </div>
                """, unsafe_allow_html=True)
                
                with st.expander("💳 Open Simulated Secure Checkout"):
                    card_num = st.text_input("Mock Card Information (Simulated Number)", placeholder="4000 1234 5678 9010")
                    card_expiry = st.text_input("Expiry Date", placeholder="MM/YY")
                    
                    if st.button("Authorize Simulated $9.00 Payment Transaction"):
                        if not card_num or not card_expiry:
                            st.error("Transaction Aborted: Complete all required payment token entries.")
                        else:
                            st.session_state.users_db[user_id]["is_premium"] = True
                            st.success("💰 Stripe Simulation Complete: Payment finalized. Status mutated to PRO Storefront!")
                            st.rerun()

# ==========================================
# 🚀 MODE 5: MARKETING & VIRAL COPY LAUNCH VAULT
# ==========================================
elif app_mode == "🚀 Get Your Launch Copy":
    st.markdown("## 🚀 Social Media Launch Blueprint")
    st.write("Copy these high-converting frameworks to acquire your first 100 users.")
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("#### 📱 Short-Form Video Script")
        st.code("""
[HOOK - 0 to 3 secs]
Stop wasting money on shipping fees for generic items. Let me show you how I surf the world for rare clothes.

[BODY - 3 to 45 secs]
This app is called GTrade. You just set up a profile, declare what you HAVE to trade, or post what you WANT. 
Look at this—I just matched with someone in Tokyo who wanted my old gaming console for a rare vintage jacket. 
Local hubs check everything so you don't get scammed.

[CTA - 45 to 60 secs]
The app is currently invite-only. Drop a comment below, and I'll DM you a registration link to join the beta network.
        """, language="text")
        
    with c2:
        st.markdown("#### ✍️ Instagram / X Announcement")
        st.code("""
Say hello to the global circular trading loop 🌐 

I just deployed the MVP for GTrade Surf! It blends the visual feed of an Instagram scroll with the direct utility of global P2P bartering.

🔹 Display your 'Haves'
🔹 List your 'Wants'
🔹 Chat instantly over WhatsApp
🔹 Scale your storefront with Pro settings

Test out the live build here completely for free: [YOUR DEPLOYMENT LINK HERE]
        """, language="text")
        
    with c3:
        st.markdown("#### 💬 WhatsApp / DM Blast")
        st.code("""
Hey! I'm running early alpha testing for an application I built called GTrade Surf. It's a platform for collectors and traders to post what they have or need and match swaps directly. 

I'd really value your insight. Can you jump onto this live link, create a quick profile, and let me know if the 'Message Trader' button launches smoothly? Thanks!

👉 [YOUR DEPLOYMENT LINK HERE]
        """, language="text")

# ==========================================
# ⚖️ MODE 6: GLOBAL LEGAL POLICY LAYER
# ==========================================
elif app_mode == "⚖️ Legal Center":
    st.markdown("## ⚖️ Global Compliance & Governance Model")
    st.write("This structured legal policy framework protects your platform and meets payment gateway processing criteria.")
    
    with st.container(border=True):
        st.markdown("""
        ### 📄 Privacy & Data Processing Agreement (GDPR/NDPR Standard)
        **Last Modified: September 2026**  
        GTrade Platform Architecture processes primary phone infrastructure tokens under user consent arrays. Personal identification vectors (such as localized destination hubs and connection routes) are managed strictly via on-device state configurations to eliminate data exploitation risk profiles.
        
        ### 🛡️ Escrow Transaction Framework & Fair Value Guidelines
        All monetary 'top-ups' intended to balance out unequal multi-party trades are held in secure, non-custodial external financial gateways until physical hub operators scan corresponding authentication QR tags. 
        
        ### 🛑 Restricted Trading Classification Indexes
        Users are legally blocked from creating listings containing dangerous substances, financial instruments, counterfeit documents, or unverified hazardous materials. Any account violating these terms will face immediate data purges.
        """)

# ==========================================
# 🔒 MODE 7: ADMINISTRATIVE CONTROL CENTER
# ==========================================
elif app_mode == "🔒 Admin Command Center":
    st.markdown("## 🔒 Master Administrative Command Panel")
    
    input_key = st.text_input("Provide System Executive Master Passkey:", type="password")
    
    if input_key == ADMIN_PASSKEY:
        st.success("🔒 System Authentication Cleared. Secure Sandbox Access Initiated.")
        
        tab_mod, tab_diag = st.tabs(["🗑️ Global Moderation Panel", "🛠️ Live System Diagnostics"])
        
        with tab_mod:
            st.markdown("### 🗑️ Live Global Content Control System")
            df = st.session_state.listings_db
            
            if df.empty:
                st.info("Database Connection Secure: 0 items currently stored on the global network.")
            else:
                for idx, row in df.iterrows():
                    col_item, col_action = st.columns()
                    with col_item:
                        status_color = "green" if row["Status"] == "Active" else "red"
                        st.markdown(f"**[{row['Post_Type']}]** {row['Item_Title']} | Posted By: {row['User_Name']} ({row['User_Phone']}) | Status: <span style='color:{status_color}; font-weight:bold;'>{row['Status']}</span>", unsafe_allow_html=True)
                    with col_action:
                        if row["Status"] == "Active":
                            if st.button("Remove Item", key=f"del_{row['Listing_ID']}"):
                                st.session_state.listings_db.at[idx, "Status"] = "Removed"
                                st.success("Listing removed from feed.")
                                st.rerun()
                                
        with tab_diag:
            st.markdown("### 🛠️ Interactive Deployment Troubleshooting Diagnostic Framework")
            
            with st.expander("🚨 Bug 1: The Surfing Feed is Blank after Code Reboots"):
                st.write("**Root Cause:** Because free cloud environments run on ephemeral server architecture, session state caches wipe automatically during periods of inactivity."\)
                st.markdown("**Remediation Protocol:** Connect this script to a live persistent cloud document database (such as *Supabase* or *Firestore*) so that inventory rows survive app updates."\)
                
            with st.expander("🚨 Bug 2: WhatsApp Click-to-Chat Buttons Fails with an Error"):
                st.write("**Root Cause:** The user input bad data or included symbols (like spaces, dashes, or leading plus signs) that break URL parameters."\)
                st.markdown("**Remediation Protocol:** Apply our phone sanitization script `.replace('+', '').replace('-', '').strip()` directly to the form submission field to guarantee format uniformity."\)
                
            with st.expander("🚨 Bug 3: Stripe Checkout Button Doesn't Load in Production"):
                st.write("**Root Cause:** Payment connections require live secret encryption credentials linked directly inside your platform console headers."\)
                st.markdown("**Remediation Protocol:** Open your Streamlit deployment workspace dashboard settings, go to 'Secrets', and securely paste your verified payment API authorization keys."\)
    
    elif input_key != "":
        st.error("🛑 Security Exception: Invalid Passkey Provided. Unauthorized Database Manipulation Prohibited.")
