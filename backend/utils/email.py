import os
import asyncio
import smtplib
import ssl
import traceback
import httpx
from pathlib import Path
from typing import List
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

_LOGO_PATH = Path(__file__).parent / "logo-circle.png"
_LOGO_BYTES: bytes | None = _LOGO_PATH.read_bytes() if _LOGO_PATH.exists() else None
_LOGO_CID = "cmusu_logo"

_STATUS_META = {
    "approved": {
        "label": "อนุมัติแล้ว",
        "color": "#3b82f6",
        "bg": "#eff6ff",
        "border": "#bfdbfe",
        "icon": "✅",
        "body": "คำร้องขอยืมอุปกรณ์ของคุณ <strong>ได้รับการอนุมัติแล้ว</strong><br>สามารถมารับอุปกรณ์ได้ตามวันที่ยืมที่ระบุไว้",
    },
    "returned": {
        "label": "คืนอุปกรณ์เรียบร้อย",
        "color": "#16a34a",
        "bg": "#f0fdf4",
        "border": "#bbf7d0",
        "icon": "📦",
        "body": "ระบบบันทึกการคืนอุปกรณ์ของคุณ <strong>เรียบร้อยแล้ว</strong><br>ขอบคุณที่ใช้บริการสโมสรนักศึกษา",
    },
    "pending": {
        "label": "รออนุมัติ",
        "color": "#d97706",
        "bg": "#fffbeb",
        "border": "#fde68a",
        "icon": "⏳",
        "body": "คำร้องขอยืมอุปกรณ์ของคุณอยู่ใน <strong>สถานะรออนุมัติ</strong>",
    },
}


def _build_items_html(items: List[dict]) -> str:
    if not items:
        return ""

    rows = ""
    for item in items:
        name = item.get("name", "ไม่ทราบชื่ออุปกรณ์")
        qty = item.get("quantity", "-")
        image_url = item.get("image_url", "")

        img_cell = (
            f'<img src="{image_url}" width="48" height="48" '
            f'style="width:48px;height:48px;object-fit:cover;border-radius:10px;display:block;" />'
            if image_url
            else '<div style="width:48px;height:48px;background:#f3f4f6;border-radius:10px;'
                 'display:flex;align-items:center;justify-content:center;font-size:11px;color:#9ca3af;">ไม่มีรูป</div>'
        )

        rows += f"""
        <tr>
          <td style="padding:10px 12px;vertical-align:middle;width:60px;">{img_cell}</td>
          <td style="padding:10px 12px;vertical-align:middle;">
            <p style="margin:0;font-size:14px;font-weight:700;color:#1f2937;">{name}</p>
          </td>
          <td style="padding:10px 12px;vertical-align:middle;text-align:right;white-space:nowrap;">
            <span style="background:#a259ff15;color:#a259ff;font-weight:900;font-size:13px;
                         padding:4px 12px;border-radius:20px;">
              {qty} ชิ้น
            </span>
          </td>
        </tr>"""

    return f"""
    <tr>
      <td style="padding:20px 40px 0;">
        <p style="margin:0 0 10px;font-size:11px;font-weight:900;color:#9ca3af;
                  text-transform:uppercase;letter-spacing:1px;">รายการอุปกรณ์ที่ยืม</p>
        <table width="100%" cellpadding="0" cellspacing="0"
          style="background:#faf5ff;border:1px solid #e9d5ff;border-radius:14px;overflow:hidden;">
          {rows}
        </table>
      </td>
    </tr>"""


def _build_social_html() -> str:
    icons = [
        ("SOCIAL_FACEBOOK",  "#1877F2", "f",   "Facebook"),
        ("SOCIAL_INSTAGRAM", "#E1306C", "&#x1F4F7;", "Instagram"),
        ("SOCIAL_LINE",      "#06C755", "L",   "LINE"),
        ("SOCIAL_YOUTUBE",   "#FF0000", "&#x25B6;", "YouTube"),
    ]
    cells = ""
    for env_key, color, symbol, label in icons:
        url = os.getenv(env_key, "")
        if not url:
            continue
        cells += f"""
        <td style="padding:0 5px;">
          <a href="{url}" target="_blank" style="display:block;text-decoration:none;">
            <table cellpadding="0" cellspacing="0">
              <tr>
                <td style="width:36px;height:36px;background:{color};border-radius:50%;
                           text-align:center;vertical-align:middle;">
                  <span style="color:#ffffff;font-size:16px;font-weight:900;
                               line-height:36px;display:block;">{symbol}</span>
                </td>
              </tr>
              <tr>
                <td style="text-align:center;padding-top:4px;">
                  <span style="font-size:10px;color:#9ca3af;">{label}</span>
                </td>
              </tr>
            </table>
          </a>
        </td>"""
    if not cells:
        return ""
    return f"""
    <table cellpadding="0" cellspacing="0" style="margin:16px auto 0;">
      <tr>{cells}</tr>
    </table>"""


def _build_html(
    full_name: str,
    status: str,
    borrow_date: str,
    return_date: str,
    items: List[dict],
) -> str:
    meta = _STATUS_META.get(status, _STATUS_META["pending"])
    items_section = _build_items_html(items)

    logo_html = (
        f'<img src="cid:{_LOGO_CID}" width="72" height="72" '
        f'style="width:72px;height:72px;border-radius:50%;border:3px solid rgba(255,255,255,0.4);margin-bottom:12px;display:block;margin-left:auto;margin-right:auto;" />'
        if _LOGO_BYTES
        else ""
    )
    logo_html_sm = (
        f'<img src="cid:{_LOGO_CID}" width="36" height="36" '
        f'style="width:36px;height:36px;border-radius:50%;border:3px solid rgba(255,255,255,0.4);margin-bottom:8px;display:block;margin-left:auto;margin-right:auto;" />'
        if _LOGO_BYTES
        else ""
    )

    return f"""<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1.0" />
</head>
<body style="margin:0;padding:0;background:#f3f4f6;font-family:'Segoe UI',Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f3f4f6;padding:40px 0;">
    <tr>
      <td align="center">
        <table width="540" cellpadding="0" cellspacing="0"
          style="background:#ffffff;border-radius:24px;overflow:hidden;box-shadow:0 4px 32px rgba(0,0,0,0.10);max-width:540px;">

          <!-- Header -->
          <tr>
            <td style="background:linear-gradient(135deg,#a259ff 0%,#6a0dad 100%);padding:36px 40px 28px;text-align:center;">
              {logo_html}
              <p style="margin:0;font-size:12px;color:rgb(0,0,0);letter-spacing:2px;text-transform:uppercase;">
                สโมสรนักศึกษา มหาวิทยาลัยเชียงใหม่
              </p>
              <h1 style="margin:6px 0 0;font-size:22px;font-weight:900;color:rgb(0,0,0);letter-spacing:0.5px;">
                ระบบยืม-คืนอุปกรณ์
              </h1>
            </td>
          </tr>

          <!-- Status Badge -->
          <tr>
            <td style="padding:0 40px 0;text-align:center;">
              <div style="display:inline-block;background:{meta['bg']};
                          border:1.5px solid {meta['border']};border-radius:50px;padding:10px 28px;">
                <span style="font-size:16px;">{meta['icon']}</span>
                <span style="color:{meta['color']};font-weight:900;font-size:15px;margin-left:8px;">
                  {meta['label']}
                </span>
              </div>
            </td>
          </tr>

          <!-- Greeting -->
          <tr>
            <td style="padding:20px 40px 0;text-align:center;">
              <p style="margin:0;font-size:15px;color:#374151;line-height:1.9;">
                สวัสดีคุณ <strong style="color:#1f2937;">{full_name}</strong>
              </p>
              <p style="margin:10px 0 0;font-size:14px;color:#6b7280;line-height:1.9;">
                {meta['body']}
              </p>
            </td>
          </tr>

          <!-- Equipment List -->
          {items_section}

          <!-- Date Box -->
          <tr>
            <td style="padding:20px 40px 0;">
              <table width="100%" cellpadding="0" cellspacing="0"
                style="background:#f9fafb;border:1px solid #e5e7eb;border-radius:14px;overflow:hidden;">
                <tr>
                  <td style="padding:16px 20px;border-right:1px solid #e5e7eb;width:50%;text-align:center;">
                    <p style="margin:0;font-size:10px;color:#9ca3af;text-transform:uppercase;
                               letter-spacing:1.5px;font-weight:700;">วันที่ยืม</p>
                    <p style="margin:6px 0 0;font-size:17px;font-weight:900;color:#1f2937;">{borrow_date}</p>
                  </td>
                  <td style="padding:16px 20px;width:50%;text-align:center;">
                    <p style="margin:0;font-size:10px;color:#9ca3af;text-transform:uppercase;
                               letter-spacing:1.5px;font-weight:700;">วันที่คืน</p>
                    <p style="margin:6px 0 0;font-size:17px;font-weight:900;color:#a259ff;">{return_date}</p>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="padding:28px 40px 32px;text-align:center;">
              <hr style="border:none;border-top:1px solid #f3f4f6;margin:0 0 20px;" />
              <p style="margin:14px 0 0;font-size:12px;color:#9ca3af;line-height:1.8;">
                อีเมลนี้ส่งโดยอัตโนมัติจากระบบสโมสรนักศึกษา มช.<br>
                กรุณาอย่าตอบกลับอีเมลนี้
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""


async def _fetch_bytes(url: str) -> bytes | None:
    try:
        async with httpx.AsyncClient(timeout=8) as client:
            r = await client.get(url)
            r.raise_for_status()
            return r.content
    except Exception as e:
        print(f"⚠️ Could not fetch image {url}: {e}")
        return None


def _send_smtp(msg: MIMEMultipart) -> None:
    username = os.getenv("MAIL_USERNAME", "").strip()
    password = os.getenv("MAIL_PASSWORD", "").strip()
    server   = os.getenv("MAIL_SERVER", "smtp.gmail.com").strip()
    port     = int(os.getenv("MAIL_PORT", "587").strip())
    context  = ssl.create_default_context()
    print(f"📧 Connecting to {server}:{port} as {username}")
    with smtplib.SMTP(server, port) as smtp:
        smtp.ehlo()
        smtp.starttls(context=context)
        smtp.ehlo()
        smtp.login(username, password)
        smtp.send_message(msg)


async def send_status_email(
    to_email: str,
    full_name: str,
    status: str,
    borrow_date: str,
    return_date: str,
    items: List[dict] | None = None,
) -> None:
    if not os.getenv("MAIL_USERNAME"):
        print("⚠️  MAIL_USERNAME not set — skipping email")
        return

    # ดาวน์โหลดรูปแต่ละชิ้นพร้อมกัน
    item_list = items or []
    image_bytes_list = await asyncio.gather(
        *[_fetch_bytes(item.get("image_url", "")) for item in item_list]
    )

    # กำหนด cid สำหรับแต่ละรูปที่โหลดสำเร็จ
    cid_items = []
    inline_images: list[tuple[str, bytes]] = []  # (cid, bytes)
    for i, (item, img_bytes) in enumerate(zip(item_list, image_bytes_list)):
        cid = f"eq_img_{i}"
        if img_bytes:
            inline_images.append((cid, img_bytes))
            cid_items.append({**item, "image_url": f"cid:{cid}"})
        else:
            cid_items.append({**item, "image_url": ""})

    meta = _STATUS_META.get(status, _STATUS_META["pending"])
    html_body = _build_html(full_name, status, borrow_date, return_date, cid_items)

    # multipart/related — HTML เป็น child ตรง ๆ รูปทุกรูปอยู่ระดับเดียวกัน
    # (ถ้าซ้อน alternative ใน related บาง client หา CID ไม่เจอ)
    msg = MIMEMultipart("related", type="text/html")
    msg["Subject"] = f"[สโมสรนักศึกษา มช.] {meta['icon']} สถานะคำร้องยืมอุปกรณ์: {meta['label']}"
    msg["From"]    = f"{os.getenv('MAIL_FROM_NAME', 'สโมสรนักศึกษา มช.')} <{os.getenv('MAIL_FROM', '')}>"
    msg["To"]      = to_email

    msg.attach(MIMEText(html_body, "html", "utf-8"))

    if _LOGO_BYTES:
        mime_logo = MIMEImage(_LOGO_BYTES)
        mime_logo.add_header("Content-ID", f"<{_LOGO_CID}>")
        mime_logo.add_header("Content-Disposition", "inline")
        msg.attach(mime_logo)

    for cid, img_bytes in inline_images:
        mime_img = MIMEImage(img_bytes)
        mime_img.add_header("Content-ID", f"<{cid}>")
        mime_img.add_header("Content-Disposition", "inline")
        msg.attach(mime_img)

    try:
        await asyncio.to_thread(_send_smtp, msg)
        print(f"✅ Email sent to {to_email} [{status}]")
    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {e}")
        traceback.print_exc()
