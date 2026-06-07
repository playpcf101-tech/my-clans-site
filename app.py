import streamlit as st
import requests
import time

# Basic Configuration
st.set_page_config(page_title="TopReqClans Global", layout="wide", initial_sidebar_state="collapsed")

API_KEY = st.secrets["API_KEY"]
headers = {"Authorization": f"Bearer {API_KEY}"}

# Manage Navigation and Update Timers
if 'selected_clan_tag' not in st.session_state:
    st.session_state.selected_clan_tag = None
if 'last_api_fetch' not in st.session_state:
    st.session_state.last_api_fetch = 0.0
if 'cached_clan_data' not in st.session_state:
    st.session_state.cached_clan_data = {}

# Predefined Premium Clan Tags
CLAN_TAGS = [
    "#L0UJG2J9", "#2PUJVQ898", "#9V98P0UJ", "#P98QRCYL", "#828CQLV",
    "#G0Q80CR9", "#899VUPLL", "#2LJ9P0GJL", "#RYPR0RC8", "#C09PYRPQ",
    "#PCP0CQJG", "#29L20PJVU", "#2RV9R8PU2", "#P92V2CQV", "#YGUC8GG", "#2JU0LJVUP"
]

def fetch_all_data():
    current_time = time.time()
    if current_time - st.session_state.last_api_fetch > 120 or not st.session_state.cached_clan_data:
        new_cache = {}
        for tag in CLAN_TAGS:
            clean_tag = tag.replace("#", "%23")
            url = f"https://cocproxy.royaleapi.dev/v1/clans/{clean_tag}"
            try:
                res = requests.get(url, headers=headers, timeout=5)
                if res.status_code == 200:
                    new_cache[tag] = res.json()
            except:
                continue
        if new_cache:
            st.session_state.cached_clan_data = new_cache
            st.session_state.last_api_fetch = current_time

fetch_all_data()

seconds_ago = int(time.time() - st.session_state.last_api_fetch)
time_string = f"{seconds_ago}s ago" if seconds_ago < 60 else f"{seconds_ago // 60}m {seconds_ago % 60}s ago"

# --- Advanced iOS Glassmorphism UI & Infinite Dance Animation CSS ---
st.markdown("""
    <style>
    @keyframes dance {
        0% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(-10px) rotate(5deg); }
        100% { transform: translateY(0) rotate(-5deg); }
    }
    
    .stApp { background-color: #0d1117; color: #c9d1d9; font-family: 'Segoe UI', sans-serif; }
    
    /* Header Container styling */
    .header-container { display: flex; justify-content: space-between; align-items: center; background: rgba(22, 27, 34, 0.7); backdrop-filter: blur(12px); padding: 15px 25px; border-radius: 14px; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 25px; }
    .header-title { color: #f0f6fc; font-size: 32px; font-weight: bold; text-shadow: 0 0 15px #ffaa45; display: flex; align-items: center; gap: 10px; }
    .update-box { background: rgba(255, 170, 65, 0.15); border: 1px solid #ffaa45; padding: 10px 18px; border-radius: 8px; font-size: 14px; color: #ffaa45; font-weight: bold; backdrop-filter: blur(5px); }
    
    /* Infinite Dancing Character styling */
    .dancer { font-size: 45px; display: inline-block; animation: dance 0.5s infinite alternate ease-in-out; text-align: center; width: 100%; margin-top: 10px; }
    
    /* Premium Tables styling */
    .custom-table { width: 100%; border-collapse: collapse; margin-top: 15px; text-align: left; background: rgba(22, 27, 34, 0.6); backdrop-filter: blur(10px); border-radius: 12px; overflow: hidden; border: 1px solid rgba(255, 255, 255, 0.08); }
    .custom-table th { background: rgba(33, 38, 45, 0.9); color: #ffaa45; padding: 14px; font-weight: bold; border-bottom: 2px solid #ffaa45; text-align: center; }
    .custom-table td { padding: 12px; border-bottom: 1px solid rgba(255, 255, 255, 0.05); color: #c9d1d9; text-align: center; font-size: 15px; }
    .custom-table tr:hover { background-color: rgba(255, 255, 255, 0.04); }
    
    /* Premium iOS Style Glass Cards (No Bugs, Fully Functional) */
    .glass-card { background: rgba(255, 255, 255, 0.04) !important; border: 1px solid rgba(255, 255, 255, 0.1) !important; backdrop-filter: blur(20px) !important; border-radius: 16px !important; padding: 20px !important; border-top: 3px solid #ffaa45 !important; margin-bottom: 25px; }
    .glass-metric { background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); backdrop-filter: blur(10px); border-radius: 12px; padding: 15px; text-align: center; border-bottom: 3px solid #45f3ff; }
    
    .lvl-badge { background-color: #1f6feb; color: #fff; padding: 3px 8px; border-radius: 6px; font-weight: bold; font-size: 13px; }
    .th-badge { background-color: #da70d6; color: #fff; padding: 3px 8px; border-radius: 6px; font-weight: bold; font-size: 13px; }
    </style>
    """, unsafe_allow_html=True)

# --- Top Header Design ---
col_head, col_dance = st.columns([8, 2])
with col_head:
    st.markdown(f'<div class="header-container"><div class="header-title">🏆 TOP REQ CLANS 🇮🇷</div><div class="update-box">⏱️ Last Update: {time_string}</div></div>', unsafe_allow_html=True)
with col_dance:
    st.markdown('<div class="dancer">🕺🤖</div>', unsafe_allow_html=True)

# Parse API Data into Lists
all_clans_list = []
all_players_list = []

for tag, data in st.session_state.cached_clan_data.items():
    total_donations = sum(m.get('donations', 0) for m in data.get('memberList', []))
    total_received = sum(m.get('donationsReceived', 0) for m in data.get('memberList', []))
    leader_name = next((m['name'] for m in data.get('memberList', []) if m['role'] == 'leader'), "Unknown")
    
    all_clans_list.append({
        "name": data['name'], "tag": data['tag'], "level": data['clanLevel'],
        "leader": leader_name, "members": data['members'], "donations": total_donations,
        "received": total_received, "badge": data.get('badgeUrls', {}).get('medium', ''),
        "description": data.get('description', 'No Description Set.'), "points": data.get('clanPoints', 0),
        "location": data.get('location', {}).get('name', 'International'), "members_raw": data.get('memberList', [])
    })
    
    for m in data.get('memberList', []):
        all_players_list.append({
            "name": m['name'], "clan_name": data['name'], "clan_badge": data.get('badgeUrls', {}).get('small', ''),
            "level": m.get('expLevel', 0), "donations": m.get('donations', 0), "received": m.get('donationsReceived', 0),
            "role": m['role'].capitalize(), "tag": m['tag']
        })

if all_clans_list:
    all_clans_list = sorted(all_clans_list, key=lambda x: x['donations'], reverse=True)

# -------------------------------------------------------------
# Display Router: Detailed Clan Page View vs Main Dashboard
# -------------------------------------------------------------
if st.session_state.selected_clan_tag:
    selected_clan = next((c for c in all_clans_list if c['tag'] == st.session_state.selected_clan_tag), None)
    
    if selected_clan:
        col_back_title, col_back_btn = st.columns([8, 2])
        with col_back_btn:
            if st.button("⬅️ Back to Leaderboard", use_container_width=True):
                st.session_state.selected_clan_tag = None
                st.rerun()
                
        # 🛡️ Custom Glassmorphic Container for Clan Profile (No Bugs)
        with st.container():
            st.markdown(f"""
            <div class="glass-card">
                <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 15px;">
                    <div style="display: flex; align-items: center; gap: 20px;">
                        <img src="{selected_clan['badge']}" width="85">
                        <div>
                            <h2 style="color: white; margin: 0; font-size: 30px;">{selected_clan['name']}</h2>
                            <p style="color: #ffaa45; margin: 5px 0; font-size: 14px;">{selected_clan['tag']} | Leader: {selected_clan['leader']}</p>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <span style="color:#00ffcc; font-weight:bold; font-size:18px;">Level {selected_clan['level']}</span><br>
                        <span style="color:gray; font-size:14px;">Location: {selected_clan['location']}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Pure Streamlit Info Callout for 100% Bug-Free Description
            st.info(f"📋 **Clan Description:** {selected_clan['description']}")
            
            # Premium Metrics Rows with Custom CSS Sub-boxes
            m_col1, m_col2, m_col3 = st.columns(3)
            with m_col1:
                st.markdown(f'<div class="glass-metric"><p style="margin:0; color: #45f3ff; font-weight:bold;">Total Donated</p><h2 style="margin:5px 0; color:white;">{selected_clan["donations"]:,}</h2></div>', unsafe_allow_html=True)
            with m_col2:
                st.markdown(f'<div class="glass-metric" style="border-bottom-color: #c5a1ff;"><p style="margin:0; color: #c5a1ff; font-weight:bold;">Total Received</p><h2 style="margin:5px 0; color:white;">{selected_clan["received"]:,}</h2></div>', unsafe_allow_html=True)
            with m_col3:
                st.markdown(f'<div class="glass-metric" style="border-bottom-color: gold;"><p style="margin:0; color: gold; font-weight:bold;">Clan Points</p><h2 style="margin:5px 0; color:white;">{selected_clan["points"]:,}</h2></div>', unsafe_allow_html=True)
        
        # Clicked Clan Member List Table
        sorted_m = sorted(selected_clan['members_raw'], key=lambda x: x.get('donations', 0), reverse=True)
        table_html = "<table class='custom-table'><thead><tr><th>Rank</th><th>Player Name</th><th>Role</th><th>Level</th><th>🔥 Donated</th><th>📥 Received</th></tr></thead><tbody>"
        for index, member in enumerate(sorted_m, 1):
            table_html += f"<tr><td><b>{index}</b></td><td style='color: white; font-weight: bold;'>{member['name']}</td><td>{member['role']}</td><td><span class='lvl-badge'>⭐ {member.get('expLevel', 0)}</span></td><td style='color: #00ffcc; font-weight: bold;'>{member.get('donations', 0):,}</td><td style='color: #ff4545;'>{member.get('donationsReceived', 0):,}</td></tr>"
        table_html += "</tbody></table>"
        st.markdown(table_html, unsafe_allow_html=True)

else:
    # Dashboard Tabs Layout
    tab1, tab2, tab3 = st.tabs(["🏆 Current Season Clans", "🔥 Top Season Players", "⭐ Level 300+ Heroes"])
    
    # Tab 1: Clan Leaderboard Grid View
    with tab1:
        if all_clans_list:
            table_head = "<table class='custom-table'><thead><tr><th>Rank</th><th>Clan</th><th>Clan Name</th><th>Leader</th><th>Members</th><th>🔥 Total Donated</th><th>📥 Total Received</th></tr></thead><tbody>"
            st.markdown(table_head, unsafe_allow_html=True)
            
            for rank, clan in enumerate(all_clans_list, 1):
                col_r, col_img, col_name, col_ldr, col_mem, col_don, col_rec = st.columns([1, 1, 4, 3, 2, 3, 3])
                with col_r: st.write(f"**{rank}**")
                with col_img: st.image(clan['badge'], width=38)
                with col_name:
                    if st.button(f"🛡️ {clan['name']}", key=f"cl_btn_{clan['tag']}", use_container_width=True):
                        st.session_state.selected_clan_tag = clan['tag']
                        st.rerun()
                with col_ldr: st.write(clan['leader'])
                with col_mem: st.write(f"{clan['members']}/50")
                with col_don: st.write(f"<span style='color:#00ffcc; font-weight:bold;'>{clan['donations']:,}</span>", unsafe_allow_html=True)
                with col_rec: st.write(f"{clan['received']:,}")
                st.divider()

    # Tab 2: Top Players Global Leaderboard View
    with tab2:
        if all_players_list:
            sorted_p = sorted(all_players_list, key=lambda x: x['donations'], reverse=True)
            p_table = "<table class='custom-table'><thead><tr><th>Rank</th><th>Player Name</th><th>Clan</th><th>Level</th><th>🔥 Total Donated</th><th>📥 Received</th></tr></thead><tbody>"
            for idx, p in enumerate(sorted_p[:100], 1):
                p_table += f"<tr><td><b>{idx}</b></td><td style='color: white; font-weight: bold;'>{p['name']}</td><td><img src='{p['clan_badge']}' width='20'> {p['clan_name']}</td><td><span class='lvl-badge'>⭐ {p['level']}</span></td><td style='color: #00ffcc; font-weight: bold;'>{p['donations']:,}</td><td>{p['received']:,}</td></tr>"
            p_table += "</tbody></table>"
            st.markdown(p_table, unsafe_allow_html=True)

    # Tab 3: Level 300+ Legends Table View
    with tab3:
        high_lvl_players = [p for p in all_players_list if p['level'] >= 300]
        if high_lvl_players:
            high_lvl_players = sorted(high_lvl_players, key=lambda x: x['level'], reverse=True)
            h_table = "<table class='custom-table'><thead><tr><th>Rank</th><th>Hero Name</th><th>Clan Assignment</th><th>Hero Level</th><th>🔥 Current Donations</th></tr></thead><tbody>"
            for idx, p in enumerate(high_lvl_players, 1):
                h_table += f"<tr><td><b>{idx}</b></td><td style='color: gold; font-weight: bold;'>🏆 {p['name']}</td><td><img src='{p['clan_badge']}' width='20'> {p['clan_name']}</td><td><span class='th-badge'>💎 {p['level']}</span></td><td style='color: #00ffcc;'>{p['donations']:,}</td></tr>"
            h_table += "</tbody></table>"
            st.markdown(h_table, unsafe_allow_html=True)
        else:
            st.info("No players over Level 300 found in the tracked clans currently.")
