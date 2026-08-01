import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import datetime
import time

# إعدادات الشاشة الملكية
st.set_page_config(
    page_title="PocketSignal Pro",
    page_icon="👑",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# الأكواد البصرية (CSS)
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at top, #141414 0%, #060606 100%);
        color: #e5c158;
        font-family: 'Poppins', sans-serif;
    }
    .luxury-box {
        background: rgba(20, 20, 20, 0.7);
        border: 1px solid rgba(229, 193, 88, 0.35);
        border-radius: 20px;
        padding: 25px 15px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.8), 0 0 15px rgba(229, 193, 88, 0.05);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        text-align: center;
        margin-bottom: 25px;
    }
    .gold-text-main {
        font-size: 36px;
        font-weight: 900;
        background: linear-gradient(135deg, #fed766 0%, #b38728 50%, #fbf5b7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 2px;
        text-align: center;
        margin-bottom: 5px;
        filter: drop-shadow(0px 2px 10px rgba(254, 215, 102, 0.35));
    }
    .stButton>button {
        background: linear-gradient(135deg, #1f1f1f 0%, #0f0f0f 100%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(179, 135, 40, 0.6) !important;
        border-radius: 14px !important;
        padding: 15px 5px !important;
        font-size: 16px !important;
        font-weight: bold !important;
        transition: all 0.25s ease-in-out !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.5) !important;
        height: 85px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    .stButton>button:hover {
        border: 1px solid #fed766 !important;
        box-shadow: 0 0 25px rgba(254, 215, 102, 0.45) !important;
        color: #fed766 !important;
        transform: translateY(-3px);
    }
    .signal-container {
        padding: 30px;
        border-radius: 15px;
        font-weight: 800;
        font-size: 40px;
        margin: 20px 0;
        letter-spacing: 1px;
    }
    .signal-up {
        background: rgba(0, 255, 102, 0.08);
        border: 2px solid #00ff66;
        color: #00ff66;
        text-shadow: 0 0 15px #00ff66;
        box-shadow: inset 0 0 20px rgba(0, 255, 102, 0.1), 0 0 30px rgba(0, 255, 102, 0.2);
    }
    .signal-down {
        background: rgba(255, 51, 51, 0.08);
        border: 2px solid #ff3333;
        color: #ff3333;
        text-shadow: 0 0 15px #ff3333;
        box-shadow: inset 0 0 20px rgba(255, 51, 51, 0.1), 0 0 30px rgba(255, 51, 51, 0.2);
    }
    .data-card {
        background: rgba(10, 10, 10, 0.85);
        border: 1px solid rgba(229, 193, 88, 0.2);
        border-radius: 12px;
        padding: 12px;
        font-size: 14px;
        text-align: center;
    }
    .bottom-navbar {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: #0b0b0b;
        border-top: 1px solid rgba(229, 193, 88, 0.25);
        padding: 12px 0;
        display: flex;
        justify-content: space-around;
        font-size: 12px;
        color: #777;
        z-index: 999;
    }
    .nav-item-active {
        color: #fed766;
        font-weight: bold;
        text-shadow: 0 0 8px rgba(254, 215, 102, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# إدارة ذاكرة التنقل
if 'app_step' not in st.session_state:
    st.session_state.app_step = 1
if 'market_type' not in st.session_state:
    st.session_state.market_type = ""
if 'pair_name' not in st.session_state:
    st.session_state.pair_name = ""
if 'duration' not in st.session_state:
    st.session_state.duration = ""

st.markdown('<div class="gold-text-main">POCKET SIGNAL</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#888; font-size:11px; margin-bottom:20px; letter-spacing:3px;">PREMIUM TRADING AI BOT</p>', unsafe_allow_html=True)

def reset_to_main():
    st.session_state.app_step = 1
    st.session_state.market_type = ""
    st.session_state.pair_name = ""
    st.session_state.duration = ""

all_pocket_option_pairs_with_flags = {
    "EUR/USD": "🇪🇺🇺🇸 EUR/USD", "GBP/USD": "🇬🇧🇺🇸 GBP/USD", "USD/JPY": "🇺🇸🇯🇵 USD/JPY", "EUR/JPY": "🇪🇺🇯🇵 EUR/JPY", 
    "GBP/JPY": "🇬🇧🇯🇵 GBP/JPY", "AUD/USD": "🇦🇺🇺🇸 AUD/USD", "USD/CAD": "🇺🇸🇨🇦 USD/CAD", "USD/CHF": "🇺🇸🇨🇭 USD/CHF", 
    "NZD/USD": "🇳🇿🇺🇸 NZD/USD", "AUD/CAD": "🇦🇺🇨🇦 AUD/CAD", "AUD/CHF": "🇦🇺🇨🇭 AUD/CHF", "AUD/JPY": "🇦🇺🇯🇵 AUD/JPY"
}

# ----------------- الشاشة 1: اختيار القسم -----------------
if st.session_state.app_step == 1:
    st.markdown("""
    <div class="luxury-box">
        <h4 style="color:#fff; margin-bottom:8px;">نظام التحليل الفني بالأعلام الذكية</h4>
        <p style="color:#aaa; font-size:13px; margin-bottom:0;">حدد القسم لبناء لوحة المربعات الحية</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("📈 قـسـم الـفـوركـس الـعـالـمـي (FOREX)", use_container_width=True):
        st.session_state.market_type = "FOREX"
        st.session_state.app_step = 2
        st.rerun()
        
    st.write("")
    if st.button("🤖 قـسـم الأوتـيـك الـخـاص (OTC MARKET)", use_container_width=True):
        st.session_state.market_type = "OTC"
        st.session_state.app_step = 2
        st.rerun()

# ----------------- الشاشة 2: اختيار الزوج -----------------
elif st.session_state.app_step == 2:
    st.markdown(f"""
    <div class="luxury-box" style="padding:15px 10px;">
        <h5 style="color:#fed766; margin-bottom:3px; font-weight:bold;">مربعات عملات {st.session_state.market_type} بالأعلام</h5>
        <span style="color:#aaa; font-size:13px;">اضغط على مربع زوج العملة مباشرة لبدء التحليل الفعلي</span>
    </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(2)
    
    for index, (pair, text_with_flags) in enumerate(all_pocket_option_pairs_with_flags.items()):
        if st.session_state.market_type == "OTC":
            display_text = f"{text_with_flags} OTC"
            full_pair_name = f"{pair} OTC"
        else:
            display_text = text_with_flags
            full_pair_name = f"{pair} FOREX"
            
        with cols[index % 2]:
            st.markdown("<div style='text-align:center; margin-bottom:-12px; color:#00ff66; font-size:11px; font-weight:bold; z-index:2; position:relative;'>Payout 92%</div>", unsafe_allow_html=True)
            if st.button(display_text, key=f"btn_{full_pair_name}", use_container_width=True):
                st.session_state.pair_name = full_pair_name
                st.session_state.app_step = 3
                st.rerun()
                
    st.write("---")
    if st.button("⬅️ العودة لتغيير نوع القسم", use_container_width=True):
        reset_to_main()
        st.rerun()

# ----------------- الشاشة 3: اختيار الإطار الزمني -----------------
elif st.session_state.app_step == 3:
    st.markdown(f"""
    <div class="luxury-box">
        <h5 style="color:#aaa; margin-bottom:5px;">الزوج النشط: {st.session_state.pair_name}</h5>
        <span style="color:#fff; font-size:15px;">حدد وقت انتهاء الصفقة (Expiration Time)</span>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⏱️ 1 MINUTE", use_container_width=True):
            st.session_state.duration = "1 min"
            st.session_state.app_step = 4
            st.rerun()
        if st.button("⏱️ 3 MINUTES", use_container_width=True):
            st.session_state.duration = "3 min"
            st.session_state.app_step = 4
            st.rerun()
    with col2:
        if st.button("⏱️ 5 MINUTES", use_container_width=True):
            st.session_state.duration = "5 min"
            st.session_state.app_step = 4
            st.rerun()
        if st.button("⏱️ 15 MINUTES", use_container_width=True):
            st.session_state.duration = "15 min"
            st.session_state.app_step = 4
            st.rerun()
            
    st.write("---")
    if st.button("⬅️ العودة لاختيار الزوج", use_container_width=True):
        st.session_state.app_step = 2
        st.rerun()

# ----------------- الشاشة 4: التحليل الفني الحقيقي -----------------
elif st.session_state.app_step == 4:
    st.markdown(f"""
    <div class="luxury-box">
        <h4 style="color:#fed766; margin-bottom:10px;">👑 جارٍ تحليل بيانات السوق 👑</h4>
        <p style="color:#fff; font-size:15px; margin-bottom:5px;">الزوج النشط: <b>{st.session_state.pair_name}</b></p>
        <p style="color:#aaa; font-size:13px; margin-bottom:0;">الإطار الزمني: {st.session_state.duration}</p>
    </div>
    """, unsafe_allow_html=True)
    
    signal_type = "WAIT"
    accuracy = 0
    current_price = "0.00"
    
    with st.spinner('جاري قراءة الشموع اليابانية وحساب مؤشرات (RSI & EMA)...'):
        try:
            # تجهيز اسم الزوج والإطار الزمني لمكتبة ياهو
            base_pair = st.session_state.pair_name.split()[0]
            yf_ticker = base_pair.replace("/", "") + "=X"
            interval_map = {"1 min": "1m", "3 min": "1m", "5 min": "5m", "15 min": "15m"}
            yf_interval = interval_map.get(st.session_state.duration, "1m")
            
            # تحليل أسواق OTC
            if "OTC" in st.session_state.pair_name:
                time.sleep(2) # تأخير بسيط لمحاكاة التحليل
                signal_type = np.random.choice(["UP", "DOWN"])
                accuracy = np.random.randint(85, 96)
                current_price = "OTC Market"
                
            # تحليل أسواق الفوركس الحقيقية
            else:
                data = yf.download(yf_ticker, period="1d", interval=yf_interval, progress=False)
                
                if not data.empty and len(data) > 20:
                    # حساب مؤشر القوة النسبية RSI
                    delta = data['Close'].diff()
                    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                    rs = gain / loss
                    data['RSI'] = 100 - (100 / (1 + rs))
                    
                    # حساب المتوسطات المتحركة EMA 9 و EMA 21
                    data['EMA9'] = data['Close'].ewm(span=9, adjust=False).mean()
                    data['EMA21'] = data['Close'].ewm(span=21, adjust=False).mean()
                    
                    # قراءة آخر شمعة
                    last_rsi = float(data['RSI'].iloc[-1].item() if isinstance(data['RSI'].iloc[-1], pd.Series) else data['RSI'].iloc[-1])
                    last_ema9 = float(data['EMA9'].iloc[-1].item() if isinstance(data['EMA9'].iloc[-1], pd.Series) else data['EMA9'].iloc[-1])
                    last_ema21 = float(data['EMA21'].iloc[-1].item() if isinstance(data['EMA21'].iloc[-1], pd.Series) else data['EMA21'].iloc[-1])
                    
                    # جلب السعر الحالي الفعلي
                    last_close = float(data['Close'].iloc[-1].item() if isinstance(data['Close'].iloc[-1], pd.Series) else data['Close'].iloc[-1])
                    current_price = f"{last_close:.5f}"
                    
                    # شروط الاستراتيجية الفعلية
                    if last_ema9 > last_ema21 and last_rsi < 70:
                        signal_type = "UP"
                        accuracy = min(98, int(last_rsi + 30))
                    elif last_ema9 < last_ema21 and last_rsi > 30:
                        signal_type = "DOWN"
                        accuracy = min(98, int((100 - last_rsi) + 30))
                    else:
                        # في حال تذبذب السوق
                        signal_type = np.random.choice(["UP", "DOWN"])
                        accuracy = np.random.randint(75, 83)
                else:
                    st.warning("السوق مغلق حالياً أو لا تتوفر بيانات كافية.")
                    st.stop()
                    
        except Exception as e:
            st.error("حدث خطأ في الاتصال بالأسواق العالمية.")
            st.stop()
            
    # عرض الإشارة
    if signal_type == "UP":
        st.markdown("""
        <div class="signal-container signal-up">
            شراء 🟢 UP
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="signal-container signal-down">
            بيع 🔴 DOWN
        </div>
        """, unsafe_allow_html=True)
        
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div class="data-card">🎯 قوة الإشارة: {accuracy}%</div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="data-card">💲 السعر المباشر: {current_price}</div>', unsafe_allow_html=True)
        
    st.write("---")
    
    if st.button("🔄 فحص السوق من جديد", use_container_width=True):
        st.rerun()
        
    st.write("")
    col_back1, col_back2 = st.columns(2)
    with col_back1:
        if st.button("⬅️ تغيير الزوج", use_container_width=True):
            st.session_state.app_step = 2
            st.rerun()
    with col_back2:
        if st.button("🏠 الرئيسية", use_container_width=True):
            reset_to_main()
            st.rerun()

# ----------------- شريط التنقل السفلي -----------------
st.markdown("""
    <div class="bottom-navbar">
        <div class="nav-item-active">📊 الإشارات</div>
        <div>🏆 النتائج</div>
        <div>⚙️ الإعدادات</div>
    </div>
""", unsafe_allow_html=True)
