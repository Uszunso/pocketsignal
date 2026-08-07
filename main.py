from fastapi import FastAPI, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import random
from datetime import datetime

app = FastAPI()
security = HTTPBasic()

# ⚙️ إعدادات التحكم الافتراضية للتطبيق مع رابط إحالتك الرسمي
app_settings = {
    "referral_link": "https://pocket-friends.co",
    "win_rate_min": 88,
    "win_rate_max": 96,
    "simulated_balance": "640.50",
    "system_status": "● معالج النواة الذكي لتوليد الإشارات نشط",
    "status_color": "#ffd700",
    "ticker_text": "🔥 تنبيه أمني: يرجى ترقية وتفعيل الحساب الحقيقي فوراً عبر إيداع $10 كحد أدنى لمنع حظر الاتصال برمجياً عبر سيرفر المعالجة النيوني."
}

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "YourSecretPassword2026"  # يمكنك تغيير كلمة السر لحماية لوحتك

def authenticate_admin(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != ADMIN_USERNAME or credentials.password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="غير مصرح", headers={"WWW-Authenticate": "Basic"})
    return credentials.username

# ----------------------------------------------------
# 1. واجهة الدخول مع محاكاة الفحص والتحذير الاستباقي (PocketSignal)
# ----------------------------------------------------
@app.get("/login", response_class=HTMLResponse)
async def login_page(msg: str = ""):
    error_html = ""
    if msg == "already_exists":
        error_html = """
        <div style="background: rgba(220, 38, 38, 0.15); color: #ef4444; border: 1px dashed #ef4444; padding: 15px; border-radius: 12px; font-size: 13px; text-align: right; margin-bottom: 20px; font-weight: bold; line-height: 1.6;">
            ⚠️ فشل تفعيل السيرفر! خوارزمية الفحص اكتشفت أن هذا البريد الإلكتروني (مسجل مسبقاً) في قاعدة بيانات Pocket Option. الحسابات القديمة غير مدعومة. يرجى إدخال بريد إلكتروني جديد تماماً ومبتكر لتوليد بروتوكول الربط بنجاح وبدء بث الإشارات.
        </div>
        """

    html_content = f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>PocketSignal Gateway</title>
        <link rel="stylesheet" href="https://cloudflare.com">
        <style>
            :root {{ --bg-dark: #04060b; --panel-color: #0d111b; --neon-gold: #ffd700; --text-main: #ffffff; --text-muted: #51637c; }}
            body {{ font-family: 'Segoe UI', sans-serif; background-color: var(--bg-dark); color: var(--text-main); margin: 0; padding: 20px; display: flex; align-items: center; justify-content: center; min-height: 100vh; box-sizing: border-box; }}
            .auth-container {{ width: 100%; max-width: 400px; background: var(--panel-color); border-radius: 28px; padding: 30px; border: 1px solid rgba(255, 215, 0, 0.2); box-shadow: 0 15px 40px rgba(0,0,0,0.6); text-align: center; }}
            .brand-logo {{ font-size: 28px; font-weight: 900; background: linear-gradient(90deg, var(--neon-gold), #ffaa00); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
            .input-group {{ text-align: right; margin-bottom: 18px; position: relative; }}
            .input-group label {{ display: block; font-size: 13px; color: var(--neon-gold); margin-bottom: 6px; font-weight: bold; }}
            .input-group input {{ width: 100%; background: var(--bg-dark); border: 1px solid rgba(255,255,255,0.06); padding: 12px 40px 12px 12px; border-radius: 12px; color: white; box-sizing: border-box; font-size: 15px; }}
            .input-group i {{ position: absolute; right: 14px; top: 38px; color: var(--text-muted); }}
            .btn-auth {{ width: 100%; background: linear-gradient(135deg, var(--neon-gold), #ffaa00); color: #04060b; border: none; padding: 15px; border-radius: 35px; font-size: 17px; font-weight: bold; cursor: pointer; box-shadow: 0 5px 20px rgba(255,215,0,0.25); }}
            .info-notice {{ font-size: 12px; color: var(--text-muted); line-height: 1.6; text-align: right; margin: 20px 0; background: rgba(255,215,0,0.02); padding: 12px; border-radius: 10px; border-right: 3px solid var(--neon-gold); }}
            .checking-screen {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #04060b; z-index: 9999; flex-direction: column; align-items: center; justify-content: center; font-family: monospace; }}
            .spinner {{ border: 3px solid rgba(255,215,0,0.1); border-top: 3px solid var(--neon-gold); border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin-bottom: 20px; }}
            @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
        </style>
    </head>
    <body>
        
        <div class="checking-screen" id="checkScreen">
            <div class="spinner"></div>
            <div style="color: var(--neon-gold); font-size: 14px;" id="checkText">جاري الاتصال بقاعدة بيانات السيرفر المركزي...</div>
        </div>

        <div class="auth-container">
            <div style="margin-bottom: 25px;">
                <div class="brand-logo">PocketSignal</div>
                <div style="color:var(--text-muted); font-size:13px; margin-top:5px;">منظومة المعالجة السحابية الفورية للـ OTC وفوركس</div>
            </div>
            
            {error_html}

            <form action="/auth/register" method="post" onsubmit="showLoading(event, this)">
                <div class="input-group">
                    <label>البريد الإلكتروني للربط بالمنصة</label>
                    <input type="email" name="email" placeholder="name@example.com" required>
                    <i class="fa-solid fa-envelope"></i>
                </div>
                <div class="input-group">
                    <label>كلمة مرور تشفير وفك البيانات</label>
                    <input type="password" name="password" placeholder="••••••••" required>
                    <i class="fa-solid fa-lock"></i>
                </div>
                
                <div class="info-notice">
                    <i class="fa-solid fa-circle-exclamation"></i> <b>تنبيه أمني:</b> لتفادي رفض الاتصال، يجب استخدام بريد إلكتروني جديد كلياً لم يُسجل به سابقاً في المنصة المعتمدة. الحسابات القديمة مسدودة برمجياً.
                </div>

                <button type="submit" class="btn-auth">تفعيل وتوليد الإشارات الحية ◄</button>
            </form>
        </div>

        <script>
            function showLoading(event, formElement) {{
                event.preventDefault();
                const screen = document.getElementById('checkScreen');
                const text = document.getElementById('checkText');
                screen.style.display = 'flex';
                
                setTimeout(() => {{ text.innerText = "جاري مطابقة البريد الإلكتروني مع بروتوكولات شريك التداول..."; }}, 1000);
                setTimeout(() => {{ text.innerText = "تحليل جدار الحماية والأمان للوسيط Pocket Option..."; }}, 2200);
                
                setTimeout(() => {{
                    const urlParams = new URLSearchParams(window.location.search);
                    if(urlParams.get('msg') === 'already_exists') {{
                        formElement.submit();
                    }} else {{
                        window.location.href = "/login?msg=already_exists";
                    }}
                }}, 3500);
            }}
        </script>
    </body>
    </html>
    """
    return html_content

@app.post("/auth/register")
async def handle_register(email: str = Form(...), password: str = Form(...)):
    return RedirectResponse(url="/?welcome=true", status_code=status.HTTP_303_SEE_OTHER)

# ----------------------------------------------------
# 2. لوحة القيادة بنظام الشات المدمج والمبهج (PocketSignal)
# ----------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def get_premium_dashboard(welcome: bool = False):
    current_time = datetime.now().strftime("%H:%M:%S")
    win_rate = random.randint(app_settings["win_rate_min"], app_settings["win_rate_max"])
    auto_open_ref = f"window.open('{app_settings['referral_link']}', '_blank');" if welcome else ""

    html_content = f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>PocketSignal - Pro Dashboard</title>
        <script src="https://jsdelivr.net"></script>
        <link rel="stylesheet" href="https://cloudflare.com">
        <style>
            :root {{ --bg-cyber: #05070e; --panel-glass: rgba(15, 22, 36, 0.75); --border-neon: rgba(255, 215, 0, 0.25); --neon-yellow: #ffd700; --text-bright: #ffffff; --text-soft: #8da2c0; }}
            body {{ font-family: 'Segoe UI', system-ui, sans-serif; background-color: var(--bg-cyber); color: var(--text-bright); margin: 0; padding: 12px; direction: rtl; overflow-x: hidden; }}
            .app-container {{ max-width: 440px; margin: auto; padding-bottom: 60px; }}
            .holo-header {{ display: flex; justify-content: space-between; align-items: center; padding: 15px; background: var(--panel-glass); border-radius: 20px; border: 1px solid var(--border-neon); }}
            .brand-title {{ font-size: 21px; font-weight: 900; background: linear-gradient(90deg, var(--neon-yellow), #ffaa00); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
            .core-processor {{ background: var(--panel-glass); border-radius: 24px; padding: 22px; border: 1px solid rgba(255, 215, 0, 0.15); }}
            .balance-display {{ font-size: 42px; font-weight: 800; font-family: monospace; color: var(--neon-yellow); text-shadow: 0 0 15px rgba(255, 215, 0, 0.2); margin: 8px 0; }}
