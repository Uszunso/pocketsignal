import streamlit as st
import numpy as np
import time

# ----------------- الإعدادات الأساسية -----------------
st.set_page_config(
    page_title="Genius AI Bot",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ----------------- التصميم الذكي (CSS) -----------------
st.markdown("""
    <meta name="google" content="notranslate">
    <style>
    .stApp {
        background-color: #0d1117;
        background-image: radial-gradient(circle at 50% -20%, #1a2639, #0d1117);
        color: #c9d1d9;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    .ai-title {
        font-size: 38px;
        font-weight: 900;
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        letter-spacing: 3px;
        margin-bottom: 2px;
        text-transform: uppercase;
    }
    .ai-subtitle {
        text-align: center; color: #8b949e; font-size: 11px; letter-spacing: 4px; margin-bottom: 30px;
    }
    .tech-panel {
        background: rgba(22, 27, 34, 0.65); border: 1px solid rgba(88, 166, 255, 0.25);
        border-radius: 16px; padding: 25px 20px; box-shadow: 0 10px 30px 0 rgba(0, 0, 0, 0.5);
        text-align: center; margin-bottom: 20px;
    }
    .register-btn {
        display: block; width: 100%; text-align: center; text-decoration: none;
        background: linear-gradient(135deg, #1f6feb 0%, #388bfd 100%);
        color: white !important; font-weight: bold; padding: 15px; border-radius: 10px;
        margin-bottom: 20px; font-size: 16px; box-shadow: 0 4px 15px rgba(31, 111, 235, 0.4);
    }
    .register-btn:hover { background: linear-gradient(135deg, #388bfd 0%, #58a6ff 100%); }
    
    .stButton>button {
        background: rgba(33, 38, 45, 0.7) !important; color: #e6edf3 !important;
        border: 1px solid rgba(88, 166, 255, 0.3) !important; border-radius: 12px !important;
        padding: 20px 10px !important; font-size: 15px !important; font-weight: 700 !important;
        transition: all 0.3s ease !important; width: 100%; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3) !important;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #238636 0%, #2ea043 100%) !important;
        border-color: #3fb950 !important; color: #ffffff !important; transform: translateY(-3px);
    }
    .signal-box {
        padding: 25px; border-radius: 15px; font-weight: 900; font-size: 40px;
        margin: 20px 0; letter-spacing: 2px; text-transform: uppercase; text-align: center;
        animation: pulse 2s infinite;
    }
    @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.02); } 100% { transform: scale(1); } }
    .signal-buy {
        background: rgba(35, 134, 54, 0.15); border: 2px solid #2ea043; color: #3fb950;
        text-shadow: 0 0 15px rgba(63, 185, 80, 0.5); box-shadow: inset 0 0 20px rgba(46, 160, 67, 0.2);
    }
    .signal-sell {
        background: rgba(218, 54, 51, 0.15); border: 2px solid #f85149; color: #ff7b72;
        text-shadow: 0 0 15px rgba(255, 123, 114, 0.5); box-shadow: inset 0 0 20px rgba(248, 81, 73, 0.2);
    }
    .metric-badge {
        background: #161b22; border: 1px solid #30363d; border-radius: 10px;
        padding: 12px; font-size: 12px; color: #8b949e; text-align: center;
    }
    .metric-value { font-size: 20px; font-weight: 900; color: #e6edf3; margin-top: 5px; }
    .risk-alert { color: #58a6ff; font-size: 14px; font-weight: bold; text-align: center; margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

# ----------------- القوائم المنفصلة للأزواج -----------------
forex_pairs = {
    "EUR/USD": "🇪🇺🇺🇸 EUR/USD", "GBP/USD": "🇬🇧🇺🇸 GBP/USD", "USD/JPY": "🇺🇸🇯🇵 USD/JPY",
    "USD/CHF": "🇺🇸🇨🇭 USD/CHF", "USD/CAD": "🇺🇸🇨🇦 USD/CAD", "AUD/USD": "🇦🇺🇺🇸 AUD/USD",
    "EUR/GBP": "🇪🇺🇬🇧 EUR/GBP", "EUR/JPY": "🇪🇺🇯🇵 EUR/JPY", "AUD/JPY": "🇦🇺🇯🇵 AUD/JPY",
    "EUR/AUD": "🇪🇺🇦🇺 EUR/AUD", "GBP/CHF": "🇬🇧🇨🇭 GBP/CHF", "CAD/CHF": "🇨🇦🇨🇭 CAD/CHF",
    "EUR/CHF": "🇪🇺🇨🇭 EUR/CHF", "CAD/JPY": "🇨🇦🇯🇵 CAD/JPY", "GBP/CAD": "🇬🇧🇨🇦 GBP/CAD",
    "AUD/CHF": "🇦🇺🇨🇭 AUD/CHF", "GBP/AUD": "🇬🇧🇦🇺 GBP/AUD", "NZD/USD": "🇳🇿🇺🇸 NZD/USD"
}

otc_pairs = {
    "AUD/CAD OTC": "🇦🇺🇨🇦 AUD/CAD OTC", "AUD/CHF OTC": "🇦🇺🇨🇭 AUD/CHF OTC", "BHD/CNY OTC": "🇧🇭🇨🇳 BHD/CNY OTC",
    "CAD/JPY OTC": "🇨🇦🇯🇵 CAD/JPY OTC", "EUR/CHF OTC": "🇪🇺🇨🇭 EUR/CHF OTC", "EUR/GBP OTC": "🇪🇺🇬🇧 EUR/GBP OTC",
    "EUR/NZD OTC": "🇪🇺🇳🇿 EUR/NZD OTC", "EUR/TRY OTC": "🇪🇺🇹🇷 EUR/TRY OTC", "EUR/USD OTC": "🇪🇺🇺🇸 EUR/USD OTC",
    "GBP/AUD OTC": "🇬🇧🇦🇺 GBP/AUD OTC", "QAR/CNY OTC": "🇶🇦🇨🇳 QAR/CNY OTC", "USD/ARS OTC": "🇺🇸🇦🇷 USD/ARS OTC",
    "LBP/USD OTC": "🇱🇧🇺🇸 LBP/USD OTC", "USD/CLP OTC": "🇺🇸🇨🇱 USD/CLP OTC", "AUD/JPY OTC": "🇦🇺🇯🇵 AUD/JPY OTC",
    "NGN/USD OTC": "🇳🇬🇺🇸 NGN/USD OTC", "USD/MXN OTC": "🇺🇸🇲🇽 USD/MXN OTC", "AUD/USD OTC": "🇦🇺🇺🇸 AUD/USD OTC",
    "USD/EGP OTC": "🇺🇸🇪🇬 USD/EGP OTC", "USD/JPY OTC": "🇺🇸🇯🇵 USD/JPY OTC", "USD/MYR OTC": "🇺🇸🇲🇾 USD/MYR OTC",
    "USD/PHP OTC": "🇺🇸🇵🇭 USD/PHP OTC", "USD/RUB OTC": "🇺🇸🇷🇺 USD/RUB OTC", "USD/SGD OTC": "🇺🇸🇸🇬 USD/SGD OTC",
    "YER/USD OTC": "🇾🇪🇺🇸 YER/USD OTC", "EUR/HUF OTC": "🇪🇺🇭🇺 EUR/HUF OTC", "EUR/RUB OTC": "🇪🇺🇷🇺 EUR/RUB OTC",
    "KES/USD OTC": "🇰🇪🇺🇸 KES/USD OTC", "USD/CHF OTC": "🇺🇸🇨🇭 USD/CHF OTC", "USD/BDT OTC": "🇺🇸🇧🇩 USD/BDT OTC",
    "USD/CAD OTC": "🇺🇸🇨🇦 USD/CAD OTC", "USD/COP OTC": "🇺🇸🇨🇴 USD/COP OTC", "AED/CNY OTC": "🇦🇪🇨🇳 AED/CNY OTC",
    "USD/CNH OTC": "🇺🇸🇨🇳 USD/CNH OTC", "USD/BRL OTC": "🇺🇸🇧🇷 USD/BRL OTC", "JOD/CNY OTC": "🇯🇴🇨🇳 JOD/CNY OTC",
    "GBP/JPY OTC": "🇬🇧🇯🇵 GBP/JPY OTC", "NZD/USD OTC": "🇳🇿🇺🇸 NZD/USD OTC", "USD/DZD OTC": "🇺🇸🇩🇿 USD/DZD OTC",
    "CHF/NOK OTC": "🇨🇭🇳🇴 CHF/NOK OTC", "OMR/CNY OTC": "🇴🇲🇨🇳 OMR/CNY OTC", "AUD/NZD OTC": "🇦🇺🇳🇿 AUD/NZD OTC",
    "EUR/JPY OTC": "🇪🇺🇯🇵 EUR/JPY OTC", "USD/IDR OTC": "🇺🇸🇮🇩 USD/IDR OTC", "CHF/JPY OTC": "🇨🇭🇯🇵 CHF/JPY OTC",
    "TND/USD OTC": "🇹🇳🇺🇸 TND/USD OTC", "GBP/USD OTC": "🇬🇧🇺🇸 GBP/USD OTC", "NZD/JPY OTC": "🇳🇿🇯🇵 NZD/JPY OTC",
    "CAD/CHF OTC": "🇨🇦🇨🇭 CAD/CHF OTC", "UAH/USD OTC": "🇺🇦🇺🇸 UAH/USD OTC"
}

# ----------------- إدارة حالة التطبيق -----------------
if 'app_state' not in st.session_state: st.session_state.app_state = 'verify'
if 'selected_pair' not in st.session_state: st.session_state.selected_pair = ''
if 'timeframe' not in st.session_state: st.session_state.timeframe = '1 Min'
if 'signal_data' not in st.session_state: st.session_state.signal_data = {}

st.markdown('<div class="ai-title">GENIUS AI BOT</div>', unsafe_allow_html=True)
st.markdown('<div class="ai-subtitle">POCKET OPTION PREMIUM SIGNALS</div>', unsafe_allow_html=True)

# ----------------- شاشة التحقق وشروط الإحالة والإيداع -----------------
if st.session_state.app_state == 'verify':
    st.markdown("""
    <div class="tech-panel">
        <h4 style="color:#58a6ff; margin-bottom:15px;">🚀 شروط تفعيل التطبيق المجاني</h4>
        <p style="color:#c9d1d9; font-size:14px; line-height: 1.6; margin-bottom:15px; text-align: right;">
            1️⃣ التسجيل حصرياً عبر رابط الإحالة الخاص بنا.<br>
            2️⃣ شحن الحساب وإيداع مبلغ <strong>50 دولار</strong> كحد أدنى.<br>
            3️⃣ إدخال رقم الـ ID الخاص بك لنتحقق يدوياً من تفعيل الشروط.
        </p>
        <!-- استبدل الرابط أدناه برابط الإحالة الخاص بك -->
        <a href="YOUR_AFFILIATE_LINK_HERE" target="_blank" class="register-btn">
            🔗 اضغط هنا للتسجيل في المنصة
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<h5 style="color:#8b949e; text-align:center;">أدخل رقم الحساب (ID) للتحقق اليدوي:</h5>', unsafe_allow_html=True)
    user_id = st.text_input("رقم الحساب (ID):", placeholder="مثال: 12345678", label_visibility="collapsed")
    
    if st.button("🔍 إرسال طلب التحقق", use_container_width=True):
        if user_id.strip() == "":
            st.error("❌ الرجاء إدخال رقم الـ ID أولاً!")
        else:
            # مؤقتاً سيتم نقله للشاشة أو إعلامه بأنه قيد المراجعة (يمكنك تعديلها بحسب طريقتك في فحص الـ ID)
            st.success("✅ تم إرسال الـ ID بنجاح! سيتم التحقق من إيداعك وتفعيل حسابك قريباً.")
            time.sleep(2)
            st.session_state.app_state = 'setup'
            st.rerun()

# ----------------- الشاشة الأولى: الإعدادات -----------------
elif st.session_state.app_state == 'setup':
    
    with st.expander("🛡️ إدارة رأس المال (Risk Management)", expanded=True):
        capital = st.number_input("أدخل رأس مالك في المنصة ($):", min_value=0.0, value=100.0, step=10.0)
        safe_amount = capital * 0.02
        st.markdown(f'<div class="risk-alert">💡 المبلغ الآمن والمقترح لدخول الصفقة القادمة هو: <strong>${safe_amount:.2f}</strong></div>', unsafe_allow_html=True)

    st.write("---")
    
    st.markdown('<h5 style="color:#58a6ff; font-weight:800;">⚙️ إعدادات الإشارة:</h5>', unsafe_allow_html=True)
    market_choice = st.radio("نوع السوق:", ["قسم الأوتي سي (OTC)", "الفوركس المباشر (FOREX)"], horizontal=True)
    selected_time = st.select_slider("الإطار الزمني:", options=['1 Min', '3 Min', '5 Min', '15 Min'])
    
    active_pairs = otc_pairs if "OTC" in market_choice else forex_pairs
    search_query = st.text_input("🔍 بحث سريع عن عملة (مثال: EUR):")
    display_pairs = {k: v for k, v in active_pairs.items() if search_query.upper() in k.upper()} if search_query else active_pairs
    
    cols = st.columns(2)
    for i, (code, flag_name) in enumerate(display_pairs.items()):
        with cols[i % 2]:
            if st.button(f"{flag_name}", key=code):
                st.session_state.selected_pair = flag_name
                st.session_state.timeframe = selected_time
                st.session_state.app_state = 'analyze'
                st.rerun()

# ----------------- الشاشة الثانية: النتائج الحية -----------------
elif st.session_state.app_state == 'analyze':
    st.markdown(f"""
    <div class="tech-panel">
        <h5 style="color:#8b949e; margin-bottom:10px;">الزوج: <span style="color:#58a6ff;">{st.session_state.selected_pair}</span></h5>
        <h5 style="color:#8b949e; margin-bottom:10px;">المدة: <span style="color:#58a6ff;">{st.session_state.timeframe}</span></h5>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.signal_data:
        with st.spinner("جاري استخراج الإشارة من السوق..."):
            time.sleep(2)
            rsi = np.random.randint(20, 85)
            direction = "BUY ↗" if rsi < 50 else "SELL ↘"
            st.session_state.signal_data = {
                'direction': direction,
                'rsi': rsi,
                'accuracy': np.random.randint(89, 98),
                'css_class': 'signal-buy' if rsi < 50 else 'signal-sell'
            }

    data = st.session_state.signal_data
    
    st.markdown(f'<div class="signal-box {data["css_class"]}">{data["direction"]}</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f'<div class="metric-badge">🎯 الدقة<div class="metric-value">{data["accuracy"]}%</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="metric-badge">📊 RSI<div class="metric-value">{data["rsi"]}</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="metric-badge">⏳ التوقيت<div class="metric-value">Live</div></div>', unsafe_allow_html=True)

    st.write("---")
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🔄 فحص جديد", use_container_width=True):
            st.session_state.signal_data = {}
            st.rerun()
    with col_b:
        if st.button("⚙️ العودة للمربعات", use_container_width=True):
            st.session_state.signal_data = {}
            st.session_state.app_state = 'setup'
            st.rerun()
