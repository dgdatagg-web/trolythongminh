#!/usr/bin/env python3
# SEO-22 + SEO-23 batch processor
# - Add Article JSON-LD to files missing it
# - Add "Bai viet lien quan" section to files missing it
import os, re, sys

BLOG_DIR = os.path.join(os.path.dirname(__file__), "blog")

# ============================================================
# RELATED ARTICLES MAPPING (ASCII only, no diacritics)
# Format: filename -> list of (href, title) for related links
# Strategy: P0 industry -> homepage + ai-agent-la-gi + 1 related industry
#           Tier 1 OpenClaw -> other OpenClaw articles
# ============================================================

RELATED = {
    # ---- P0 NGANH (ai-agent-cho-*) ----
    "ai-agent-cho-bao-hiem-nhan-tho.html": [
        ("/blog/ai-agent-la-gi.html", "AI Agent La Gi? Khac Hoan Toan Voi ChatGPT"),
        ("/blog/ai-agent-cho-dai-ly-bao-hiem.html", "AI Agent Cho Dai Ly Bao Hiem: Tu Dong Hoa Cham Soc Khach"),
        ("/blog/roi-ai-agent-doanh-nghiep-nho.html", "ROI Cua AI Agent: Tinh That Cho Doanh Nghiep Nho VN"),
    ],
    "ai-agent-cho-cong-ty-logistics.html": [
        ("/blog/ai-agent-la-gi.html", "AI Agent La Gi? Khac Hoan Toan Voi ChatGPT"),
        ("/blog/ai-agent-cho-kho-van-chuyen.html", "AI Agent Cho Kho Van Chuyen: Quan Ly Don Tu Dong"),
        ("/blog/roi-ai-agent-doanh-nghiep-nho.html", "ROI Cua AI Agent: Tinh That Cho Doanh Nghiep Nho VN"),
    ],
    "ai-agent-cho-dai-ly-bao-hiem.html": [
        ("/blog/ai-agent-la-gi.html", "AI Agent La Gi? Khac Hoan Toan Voi ChatGPT"),
        ("/blog/ai-agent-cho-bao-hiem-nhan-tho.html", "AI Agent Cho Bao Hiem Nhan Tho: Tu Van 24/7"),
        ("/blog/roi-ai-agent-doanh-nghiep-nho.html", "ROI Cua AI Agent: Tinh That Cho Doanh Nghiep Nho VN"),
    ],
    "ai-agent-cho-fb-ban-hang.html": [
        ("/blog/ai-agent-la-gi.html", "AI Agent La Gi? Khac Hoan Toan Voi ChatGPT"),
        ("/blog/ai-agent-cho-shop-ban-le-online.html", "AI Agent Cho Shop Ban Le Online: Tu Dong Tra Loi & Chot Don"),
        ("/blog/ai-agent-nganh-fnb.html", "AI Agent Nganh F&B: Nha Hang & Cafe Tu Dong Hoa The Nao?"),
    ],
    "ai-agent-cho-garage-o-to.html": [
        ("/blog/ai-agent-la-gi.html", "AI Agent La Gi? Khac Hoan Toan Voi ChatGPT"),
        ("/blog/ai-agent-cho-salon-spa-dat-lich.html", "AI Agent Cho Salon & Spa: Tu Dong Dat Lich 24/7"),
        ("/blog/roi-ai-agent-doanh-nghiep-nho.html", "ROI Cua AI Agent: Tinh That Cho Doanh Nghiep Nho VN"),
    ],
    "ai-agent-cho-gym-fitness.html": [
        ("/blog/ai-agent-la-gi.html", "AI Agent La Gi? Khac Hoan Toan Voi ChatGPT"),
        ("/blog/ai-agent-cho-salon-spa-dat-lich.html", "AI Agent Cho Salon & Spa: Tu Dong Dat Lich 24/7"),
        ("/blog/roi-ai-agent-doanh-nghiep-nho.html", "ROI Cua AI Agent: Tinh That Cho Doanh Nghiep Nho VN"),
    ],
    "ai-agent-cho-hr-tuyen-dung-sme.html": [
        ("/blog/ai-agent-la-gi.html", "AI Agent La Gi? Khac Hoan Toan Voi ChatGPT"),
        ("/blog/ai-agent-cho-startup.html", "AI Agent Cho Startup: Lean Team, Max Output"),
        ("/blog/roi-ai-agent-doanh-nghiep-nho.html", "ROI Cua AI Agent: Tinh That Cho Doanh Nghiep Nho VN"),
    ],
    "ai-agent-cho-ke-toan-tu-do.html": [
        ("/blog/ai-agent-la-gi.html", "AI Agent La Gi? Khac Hoan Toan Voi ChatGPT"),
        ("/blog/ai-agent-cho-tai-chinh-ca-nhan.html", "AI Agent Cho Tai Chinh Ca Nhan: Quan Ly Thu Chi Tu Dong"),
        ("/blog/roi-ai-agent-doanh-nghiep-nho.html", "ROI Cua AI Agent: Tinh That Cho Doanh Nghiep Nho VN"),
    ],
    "ai-agent-cho-kho-van-chuyen.html": [
        ("/blog/ai-agent-la-gi.html", "AI Agent La Gi? Khac Hoan Toan Voi ChatGPT"),
        ("/blog/ai-agent-cho-cong-ty-logistics.html", "AI Agent Cho Cong Ty Logistics: Tu Dong Hoa Van Hanh"),
        ("/blog/roi-ai-agent-doanh-nghiep-nho.html", "ROI Cua AI Agent: Tinh That Cho Doanh Nghiep Nho VN"),
    ],
    "ai-agent-cho-moi-gioi-bat-dong-san.html": [
        ("/blog/ai-agent-la-gi.html", "AI Agent La Gi? Khac Hoan Toan Voi ChatGPT"),
        ("/blog/ai-agent-cho-van-phong-bat-dong-san.html", "AI Agent Cho Van Phong BDS: Quan Ly Lead Hieu Qua"),
        ("/blog/roi-ai-agent-doanh-nghiep-nho.html", "ROI Cua AI Agent: Tinh That Cho Doanh Nghiep Nho VN"),
    ],
    "ai-agent-cho-nguoi-khong-biet-code.html": [
        ("/blog/ai-agent-la-gi.html", "AI Agent La Gi? Khac Hoan Toan Voi ChatGPT"),
        ("/blog/openclaw-la-gi.html", "OpenClaw La Gi? Nen Tang AI Agent Cho Doanh Nghiep Viet"),
        ("/blog/cai-dat-openclaw-tren-dien-thoai.html", "Cai Dat OpenClaw Tren Dien Thoai: Co Lam Duoc Khong?"),
    ],
    "ai-agent-cho-nha-hang-khach-san.html": [
        ("/blog/ai-agent-la-gi.html", "AI Agent La Gi? Khac Hoan Toan Voi ChatGPT"),
        ("/blog/ai-agent-nganh-fnb.html", "AI Agent Nganh F&B: Nha Hang & Cafe Tu Dong Hoa The Nao?"),
        ("/blog/roi-ai-agent-doanh-nghiep-nho.html", "ROI Cua AI Agent: Tinh That Cho Doanh Nghiep Nho VN"),
    ],
    "ai-agent-cho-phong-kham-nha-khoa.html": [
        ("/blog/ai-agent-la-gi.html", "AI Agent La Gi? Khac Hoan Toan Voi ChatGPT"),
        ("/blog/ai-agent-cho-salon-spa-dat-lich.html", "AI Agent Cho Salon & Spa: Tu Dong Dat Lich 24/7"),
        ("/blog/roi-ai-agent-doanh-nghiep-nho.html", "ROI Cua AI Agent: Tinh That Cho Doanh Nghiep Nho VN"),
    ],
    "ai-agent-cho-salon-spa-dat-lich.html": [
        ("/blog/ai-agent-la-gi.html", "AI Agent La Gi? Khac Hoan Toan Voi ChatGPT"),
        ("/blog/ai-agent-cho-phong-kham-nha-khoa.html", "AI Agent Cho Phong Kham Nha Khoa: Dat Lich & Nhac Hen"),
        ("/blog/roi-ai-agent-doanh-nghiep-nho.html", "ROI Cua AI Agent: Tinh That Cho Doanh Nghiep Nho VN"),
    ],
    "ai-agent-cho-shop-ban-le-online.html": [
        ("/blog/ai-agent-la-gi.html", "AI Agent La Gi? Khac Hoan Toan Voi ChatGPT"),
        ("/blog/ai-agent-cho-fb-ban-hang.html", "AI Agent Cho Facebook Ban Hang: Tra Loi & Chot Don Tu Dong"),
        ("/blog/roi-ai-agent-doanh-nghiep-nho.html", "ROI Cua AI Agent: Tinh That Cho Doanh Nghiep Nho VN"),
    ],
    "ai-agent-cho-shop-thoi-trang-shopee-tiktok.html": [
        ("/blog/ai-agent-la-gi.html", "AI Agent La Gi? Khac Hoan Toan Voi ChatGPT"),
        ("/blog/ai-agent-cho-shop-ban-le-online.html", "AI Agent Cho Shop Ban Le Online: Tu Dong Tra Loi & Chot Don"),
        ("/blog/roi-ai-agent-doanh-nghiep-nho.html", "ROI Cua AI Agent: Tinh That Cho Doanh Nghiep Nho VN"),
    ],
    "ai-agent-cho-startup.html": [
        ("/blog/ai-agent-la-gi.html", "AI Agent La Gi? Khac Hoan Toan Voi ChatGPT"),
        ("/blog/openclaw-cho-startup-lean-team.html", "OpenClaw Cho Startup Lean Team: Toi Da Hoa Hieu Suat"),
        ("/blog/roi-ai-agent-doanh-nghiep-nho.html", "ROI Cua AI Agent: Tinh That Cho Doanh Nghiep Nho VN"),
    ],
    "ai-agent-cho-tai-chinh-ca-nhan.html": [
        ("/blog/ai-agent-la-gi.html", "AI Agent La Gi? Khac Hoan Toan Voi ChatGPT"),
        ("/blog/ai-agent-cho-ke-toan-tu-do.html", "AI Agent Cho Ke Toan Tu Do: Quan Ly So Sach Tu Dong"),
        ("/blog/roi-ai-agent-doanh-nghiep-nho.html", "ROI Cua AI Agent: Tinh That Cho Doanh Nghiep Nho VN"),
    ],
    "ai-agent-cho-to-chuc-su-kien.html": [
        ("/blog/ai-agent-la-gi.html", "AI Agent La Gi? Khac Hoan Toan Voi ChatGPT"),
        ("/blog/ai-agent-cho-hr-tuyen-dung-sme.html", "AI Agent Cho HR & Tuyen Dung SME: Sao Loc CV Tu Dong"),
        ("/blog/roi-ai-agent-doanh-nghiep-nho.html", "ROI Cua AI Agent: Tinh That Cho Doanh Nghiep Nho VN"),
    ],
    "ai-agent-cho-trung-tam-anh-ngu.html": [
        ("/blog/ai-agent-la-gi.html", "AI Agent La Gi? Khac Hoan Toan Voi ChatGPT"),
        ("/blog/ai-agent-cho-truong-hoc-giao-duc.html", "AI Agent Cho Truong Hoc & Giao Duc: Ho Tro Hoc Sinh 24/7"),
        ("/blog/roi-ai-agent-doanh-nghiep-nho.html", "ROI Cua AI Agent: Tinh That Cho Doanh Nghiep Nho VN"),
    ],
    "ai-agent-cho-truong-hoc-giao-duc.html": [
        ("/blog/ai-agent-la-gi.html", "AI Agent La Gi? Khac Hoan Toan Voi ChatGPT"),
        ("/blog/ai-agent-cho-trung-tam-anh-ngu.html", "AI Agent Cho Trung Tam Anh Ngu: Tu Van & Dat Lich Hoc Thu"),
        ("/blog/roi-ai-agent-doanh-nghiep-nho.html", "ROI Cua AI Agent: Tinh That Cho Doanh Nghiep Nho VN"),
    ],
    "ai-agent-cho-van-phong-bat-dong-san.html": [
        ("/blog/ai-agent-la-gi.html", "AI Agent La Gi? Khac Hoan Toan Voi ChatGPT"),
        ("/blog/ai-agent-cho-moi-gioi-bat-dong-san.html", "AI Agent Cho Moi Gioi BDS: Sap Xep Xem Nha Tu Dong"),
        ("/blog/roi-ai-agent-doanh-nghiep-nho.html", "ROI Cua AI Agent: Tinh That Cho Doanh Nghiep Nho VN"),
    ],
    "ai-agent-cho-xe-khach-van-tai.html": [
        ("/blog/ai-agent-la-gi.html", "AI Agent La Gi? Khac Hoan Toan Voi ChatGPT"),
        ("/blog/ai-agent-cho-cong-ty-logistics.html", "AI Agent Cho Cong Ty Logistics: Tu Dong Hoa Van Hanh"),
        ("/blog/roi-ai-agent-doanh-nghiep-nho.html", "ROI Cua AI Agent: Tinh That Cho Doanh Nghiep Nho VN"),
    ],
    # ---- OTHER BLOG POSTS ----
    "ai-agent-gia-bao-nhieu.html": [
        ("/blog/ai-agent-la-gi.html", "AI Agent La Gi? Khac Hoan Toan Voi ChatGPT"),
        ("/blog/openclaw-chi-phi-het-bao-nhieu.html", "OpenClaw Chi Phi Het Bao Nhieu? Bang Gia Chi Tiet 2026"),
        ("/blog/roi-ai-agent-doanh-nghiep-nho.html", "ROI Cua AI Agent: Tinh That Cho Doanh Nghiep Nho VN"),
    ],
    "ai-agent-ket-hop-misa-sapo-kiotviet.html": [
        ("/blog/ai-agent-la-gi.html", "AI Agent La Gi? Khac Hoan Toan Voi ChatGPT"),
        ("/blog/openclaw-ket-noi-google-workspace.html", "OpenClaw Ket Noi Google Workspace: Tich Hop Toan Bo"),
        ("/blog/tu-dong-hoa-cong-viec-bang-ai.html", "Tu Dong Hoa Cong Viec Bang AI: Huong Dan Thuc Te"),
    ],
    "ai-agent-khac-gi-chatgpt.html": [
        ("/blog/ai-agent-la-gi.html", "AI Agent La Gi? Khac Hoan Toan Voi ChatGPT"),
        ("/blog/tai-sao-chatgpt-khong-phai-nhan-vien.html", "Tai Sao ChatGPT Khong Phai Nhan Vien AI?"),
        ("/blog/openclaw-la-gi.html", "OpenClaw La Gi? Nen Tang AI Agent Cho Doanh Nghiep Viet"),
    ],
    "ai-agent-nganh-fnb.html": [
        ("/blog/ai-agent-la-gi.html", "AI Agent La Gi? Khac Hoan Toan Voi ChatGPT"),
        ("/blog/ai-agent-cho-nha-hang-khach-san.html", "AI Agent Cho Nha Hang & Khach San: Tu Dong Hoa Dich Vu"),
        ("/blog/case-study-kansai-osaka.html", "Case Study 90 Ngay Dung AI Agent Chay Bep Kansai Osaka"),
    ],
    "ai-agent-tren-zalo-cho-doanh-nghiep.html": [
        ("/blog/ai-agent-la-gi.html", "AI Agent La Gi? Khac Hoan Toan Voi ChatGPT"),
        ("/blog/openclaw-la-gi.html", "OpenClaw La Gi? Nen Tang AI Agent Cho Doanh Nghiep Viet"),
        ("/blog/tu-dong-hoa-cong-viec-bang-ai.html", "Tu Dong Hoa Cong Viec Bang AI: Huong Dan Thuc Te"),
    ],
    "cau-hoi-thuong-gap-ve-ai-agent.html": [
        ("/blog/ai-agent-la-gi.html", "AI Agent La Gi? Khac Hoan Toan Voi ChatGPT"),
        ("/blog/openclaw-la-gi.html", "OpenClaw La Gi? Nen Tang AI Agent Cho Doanh Nghiep Viet"),
        ("/blog/bat-dau-voi-ai-agent-tu-dau.html", "Bat Dau Voi AI Agent Tu Dau? Lo Trinh Don Gian"),
    ],
    "chi-phi-thue-nhan-vien-vs-ai.html": [
        ("/blog/ai-agent-la-gi.html", "AI Agent La Gi? Khac Hoan Toan Voi ChatGPT"),
        ("/blog/roi-ai-agent-doanh-nghiep-nho.html", "ROI Cua AI Agent: Tinh That Cho Doanh Nghiep Nho VN"),
        ("/blog/so-sanh-nhan-vien-vs-ai.html", "So Sanh Nhan Vien Vs AI: Khi Nao Nen Dung Cai Nao?"),
    ],
    "co-can-ai-agent-khong-checklist.html": [
        ("/blog/ai-agent-la-gi.html", "AI Agent La Gi? Khac Hoan Toan Voi ChatGPT"),
        ("/blog/nganh-nao-phu-hop-ai-agent-viet-nam.html", "Nganh Nao Phu Hop AI Agent O Viet Nam?"),
        ("/blog/bat-dau-voi-ai-agent-tu-dau.html", "Bat Dau Voi AI Agent Tu Dau? Lo Trinh Don Gian"),
    ],
    "du-lieu-cua-ban-an-toan-khong.html": [
        ("/blog/ai-agent-la-gi.html", "AI Agent La Gi? Khac Hoan Toan Voi ChatGPT"),
        ("/blog/openclaw-la-gi.html", "OpenClaw La Gi? Nen Tang AI Agent Cho Doanh Nghiep Viet"),
        ("/blog/bao-mat-ai-agent.html", "Bao Mat AI Agent: Cach Bao Ve Du Lieu Doanh Nghiep"),
    ],
    "openclaw-api-key-khong-hoat-dong.html": [
        ("/blog/openclaw-la-gi.html", "OpenClaw La Gi? Nen Tang AI Agent Cho Doanh Nghiep Viet"),
        ("/blog/openclaw-cai-dat-nhu-the-nao.html", "OpenClaw Cai Dat Nhu The Nao? Huong Dan Tung Buoc"),
        ("/blog/openclaw-telegram-bot-khong-tra-loi.html", "OpenClaw Telegram Bot Khong Tra Loi: Debug Nhanh"),
    ],
    "openclaw-cai-dat-nhu-the-nao.html": [
        ("/blog/openclaw-la-gi.html", "OpenClaw La Gi? Nen Tang AI Agent Cho Doanh Nghiep Viet"),
        ("/blog/cai-dat-openclaw-tren-dien-thoai.html", "Cai Dat OpenClaw Tren Dien Thoai: Co Lam Duoc Khong?"),
        ("/blog/setup-openclaw-trong-30-phut.html", "Setup OpenClaw Trong 30 Phut: Huong Dan Chi Tiet"),
    ],
    "openclaw-chi-phi-het-bao-nhieu.html": [
        ("/blog/openclaw-la-gi.html", "OpenClaw La Gi? Nen Tang AI Agent Cho Doanh Nghiep Viet"),
        ("/blog/myclaw-vs-setup-service.html", "MyClaw Vs Setup Service: Chon Cai Nao Cho Business Ban?"),
        ("/blog/roi-ai-agent-doanh-nghiep-nho.html", "ROI Cua AI Agent: Tinh That Cho Doanh Nghiep Nho VN"),
    ],
    "openclaw-cho-nhieu-nguoi-dung-chung.html": [
        ("/blog/openclaw-la-gi.html", "OpenClaw La Gi? Nen Tang AI Agent Cho Doanh Nghiep Viet"),
        ("/blog/openclaw-cho-startup-lean-team.html", "OpenClaw Cho Startup Lean Team: Toi Da Hoa Hieu Suat"),
        ("/blog/setup-openclaw-trong-30-phut.html", "Setup OpenClaw Trong 30 Phut: Huong Dan Chi Tiet"),
    ],
    "openclaw-cho-startup-lean-team.html": [
        ("/blog/openclaw-la-gi.html", "OpenClaw La Gi? Nen Tang AI Agent Cho Doanh Nghiep Viet"),
        ("/blog/ai-agent-cho-startup.html", "AI Agent Cho Startup: Lean Team, Max Output"),
        ("/blog/roi-ai-agent-doanh-nghiep-nho.html", "ROI Cua AI Agent: Tinh That Cho Doanh Nghiep Nho VN"),
    ],
    "openclaw-ket-noi-google-workspace.html": [
        ("/blog/openclaw-la-gi.html", "OpenClaw La Gi? Nen Tang AI Agent Cho Doanh Nghiep Viet"),
        ("/blog/ai-agent-ket-hop-misa-sapo-kiotviet.html", "AI Agent Ket Hop Misa/Sapo/KiotViet: Tich Hop Thuc Te"),
        ("/blog/tu-dong-hoa-cong-viec-bang-ai.html", "Tu Dong Hoa Cong Viec Bang AI: Huong Dan Thuc Te"),
    ],
    "openclaw-qua-phuc-tap-co-nen-dung.html": [
        ("/blog/openclaw-la-gi.html", "OpenClaw La Gi? Nen Tang AI Agent Cho Doanh Nghiep Viet"),
        ("/blog/ai-agent-cho-nguoi-khong-biet-code.html", "AI Agent Cho Nguoi Khong Biet Code: Setup Tu Dau"),
        ("/blog/myclaw-vs-setup-service.html", "MyClaw Vs Setup Service: Chon Cai Nao Cho Business Ban?"),
    ],
    "openclaw-telegram-bot-khong-tra-loi.html": [
        ("/blog/openclaw-la-gi.html", "OpenClaw La Gi? Nen Tang AI Agent Cho Doanh Nghiep Viet"),
        ("/blog/openclaw-api-key-khong-hoat-dong.html", "OpenClaw API Key Khong Hoat Dong: Fix Nhanh"),
        ("/blog/toi-uu-openclaw-sau-khi-setup.html", "Toi Uu OpenClaw Sau Khi Setup: Nang Cap Hieu Suat"),
    ],
    "openclaw-vs-n8n-khac-gi-nhau.html": [
        ("/blog/openclaw-la-gi.html", "OpenClaw La Gi? Nen Tang AI Agent Cho Doanh Nghiep Viet"),
        ("/blog/ai-agent-la-gi.html", "AI Agent La Gi? Khac Hoan Toan Voi ChatGPT"),
        ("/blog/myclaw-vs-setup-service.html", "MyClaw Vs Setup Service: Chon Cai Nao Cho Business Ban?"),
    ],
    "roi-ai-agent-doanh-nghiep-nho.html": [
        ("/blog/ai-agent-la-gi.html", "AI Agent La Gi? Khac Hoan Toan Voi ChatGPT"),
        ("/blog/chi-phi-thue-nhan-vien-vs-ai.html", "Chi Phi Thue Nhan Vien Vs AI: So Sanh That Su"),
        ("/blog/openclaw-chi-phi-het-bao-nhieu.html", "OpenClaw Chi Phi Het Bao Nhieu? Bang Gia Chi Tiet 2026"),
    ],
    "setup-openclaw-trong-30-phut.html": [
        ("/blog/openclaw-la-gi.html", "OpenClaw La Gi? Nen Tang AI Agent Cho Doanh Nghiep Viet"),
        ("/blog/openclaw-cai-dat-nhu-the-nao.html", "OpenClaw Cai Dat Nhu The Nao? Huong Dan Tung Buoc"),
        ("/blog/toi-uu-openclaw-sau-khi-setup.html", "Toi Uu OpenClaw Sau Khi Setup: Nang Cap Hieu Suat"),
    ],
    "toi-uu-openclaw-sau-khi-setup.html": [
        ("/blog/openclaw-la-gi.html", "OpenClaw La Gi? Nen Tang AI Agent Cho Doanh Nghiep Viet"),
        ("/blog/setup-openclaw-trong-30-phut.html", "Setup OpenClaw Trong 30 Phut: Huong Dan Chi Tiet"),
        ("/blog/openclaw-cho-startup-lean-team.html", "OpenClaw Cho Startup Lean Team: Toi Da Hoa Hieu Suat"),
    ],
    "tu-dong-hoa-cong-viec-bang-ai.html": [
        ("/blog/ai-agent-la-gi.html", "AI Agent La Gi? Khac Hoan Toan Voi ChatGPT"),
        ("/blog/openclaw-la-gi.html", "OpenClaw La Gi? Nen Tang AI Agent Cho Doanh Nghiep Viet"),
        ("/blog/5-viec-nen-de-ai-lam.html", "5 Viec Nen De AI Lam: Tiết Kiem Thoi Gian Ngay"),
    ],
    # ---- FILES MISSING RELATED SECTION ----
    "5-viec-nen-de-ai-lam.html": [
        ("/blog/ai-agent-la-gi.html", "AI Agent La Gi? Khac Hoan Toan Voi ChatGPT"),
        ("/blog/tu-dong-hoa-cong-viec-bang-ai.html", "Tu Dong Hoa Cong Viec Bang AI: Huong Dan Thuc Te"),
        ("/blog/openclaw-la-gi.html", "OpenClaw La Gi? Nen Tang AI Agent Cho Doanh Nghiep Viet"),
    ],
    "ai-agent-hoc-business-the-nao.html": [
        ("/blog/ai-agent-la-gi.html", "AI Agent La Gi? Khac Hoan Toan Voi ChatGPT"),
        ("/blog/openclaw-la-gi.html", "OpenClaw La Gi? Nen Tang AI Agent Cho Doanh Nghiep Viet"),
        ("/blog/onboarding-ai-agent-48h.html", "Onboarding AI Agent Trong 48h: Quy Trinh Chuan"),
    ],
    "ai-agent-la-gi.html": [
        ("/blog/ai-agent-khac-gi-chatgpt.html", "AI Agent Khac Gi ChatGPT? Phan Biet De Chon Dung Cong Cu"),
        ("/blog/5-viec-nen-de-ai-lam.html", "5 Viec Nen De AI Lam: Tiet Kiem Thoi Gian Ngay"),
        ("/blog/openclaw-la-gi.html", "OpenClaw La Gi? Nen Tang AI Agent Cho Doanh Nghiep Viet"),
    ],
    "ban-la-1-nguoi-ai-lam-cua-ca-team.html": [
        ("/blog/ai-agent-la-gi.html", "AI Agent La Gi? Khac Hoan Toan Voi ChatGPT"),
        ("/blog/tu-dong-hoa-cong-viec-bang-ai.html", "Tu Dong Hoa Cong Viec Bang AI: Huong Dan Thuc Te"),
        ("/blog/openclaw-cho-startup-lean-team.html", "OpenClaw Cho Startup Lean Team: Toi Da Hoa Hieu Suat"),
    ],
    "bao-mat-ai-agent.html": [
        ("/blog/ai-agent-la-gi.html", "AI Agent La Gi? Khac Hoan Toan Voi ChatGPT"),
        ("/blog/du-lieu-cua-ban-an-toan-khong.html", "Du Lieu Cua Ban Co An Toan Khong Khi Dung AI?"),
        ("/blog/openclaw-la-gi.html", "OpenClaw La Gi? Nen Tang AI Agent Cho Doanh Nghiep Viet"),
    ],
    "bat-dau-voi-ai-agent-tu-dau.html": [
        ("/blog/ai-agent-la-gi.html", "AI Agent La Gi? Khac Hoan Toan Voi ChatGPT"),
        ("/blog/openclaw-la-gi.html", "OpenClaw La Gi? Nen Tang AI Agent Cho Doanh Nghiep Viet"),
        ("/blog/onboarding-ai-agent-48h.html", "Onboarding AI Agent Trong 48h: Quy Trinh Chuan"),
    ],
    "case-study-kansai-osaka.html": [
        ("/blog/ai-agent-la-gi.html", "AI Agent La Gi? Khac Hoan Toan Voi ChatGPT"),
        ("/blog/ai-agent-nganh-fnb.html", "AI Agent Nganh F&B: Nha Hang & Cafe Tu Dong Hoa The Nao?"),
        ("/blog/roi-ai-agent-doanh-nghiep-nho.html", "ROI Cua AI Agent: Tinh That Cho Doanh Nghiep Nho VN"),
    ],
    "loi-founders-hay-mac-khi-dung-ai.html": [
        ("/blog/ai-agent-la-gi.html", "AI Agent La Gi? Khac Hoan Toan Voi ChatGPT"),
        ("/blog/co-can-ai-agent-khong-checklist.html", "Co Can AI Agent Khong? Checklist Tu Danh Gia"),
        ("/blog/openclaw-la-gi.html", "OpenClaw La Gi? Nen Tang AI Agent Cho Doanh Nghiep Viet"),
    ],
    "nganh-nao-phu-hop-ai-agent-viet-nam.html": [
        ("/blog/ai-agent-la-gi.html", "AI Agent La Gi? Khac Hoan Toan Voi ChatGPT"),
        ("/blog/co-can-ai-agent-khong-checklist.html", "Co Can AI Agent Khong? Checklist Tu Danh Gia"),
        ("/blog/bat-dau-voi-ai-agent-tu-dau.html", "Bat Dau Voi AI Agent Tu Dau? Lo Trinh Don Gian"),
    ],
    "onboarding-ai-agent-48h.html": [
        ("/blog/ai-agent-la-gi.html", "AI Agent La Gi? Khac Hoan Toan Voi ChatGPT"),
        ("/blog/openclaw-la-gi.html", "OpenClaw La Gi? Nen Tang AI Agent Cho Doanh Nghiep Viet"),
        ("/blog/setup-openclaw-trong-30-phut.html", "Setup OpenClaw Trong 30 Phut: Huong Dan Chi Tiet"),
    ],
    "so-sanh-nhan-vien-vs-ai.html": [
        ("/blog/ai-agent-la-gi.html", "AI Agent La Gi? Khac Hoan Toan Voi ChatGPT"),
        ("/blog/chi-phi-thue-nhan-vien-vs-ai.html", "Chi Phi Thue Nhan Vien Vs AI: So Sanh That Su"),
        ("/blog/roi-ai-agent-doanh-nghiep-nho.html", "ROI Cua AI Agent: Tinh That Cho Doanh Nghiep Nho VN"),
    ],
    "tai-sao-chatgpt-khong-phai-nhan-vien.html": [
        ("/blog/ai-agent-la-gi.html", "AI Agent La Gi? Khac Hoan Toan Voi ChatGPT"),
        ("/blog/ai-agent-khac-gi-chatgpt.html", "AI Agent Khac Gi ChatGPT? Phan Biet De Chon Dung Cong Cu"),
        ("/blog/openclaw-la-gi.html", "OpenClaw La Gi? Nen Tang AI Agent Cho Doanh Nghiep Viet"),
    ],
}

# ============================================================
# Article JSON-LD template
# datePublished=2026-03-14, author/publisher=trolythongminh.io.vn
# ============================================================

def make_jsonld(title, description, url):
    # Escape double quotes in strings
    title = title.replace('"', '&quot;')
    description = description.replace('"', '&quot;')
    return '''  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "''' + title + '''",
    "description": "''' + description + '''",
    "url": "''' + url + '''",
    "datePublished": "2026-03-14",
    "dateModified": "2026-03-14",
    "author": {"@type": "Organization", "name": "trolythongminh.io.vn", "url": "https://trolythongminh.io.vn"},
    "publisher": {"@type": "Organization", "name": "trolythongminh.io.vn", "url": "https://trolythongminh.io.vn"},
    "inLanguage": "vi"
  }
  </script>'''

def make_related_section(links):
    items = ""
    for href, title in links:
        items += f'\n        <a href="{href}" class="related-card">{title}</a>'
    return '''  <div class="related-articles">
      <h3>Bai viet lien quan</h3>
      <div class="related-grid">''' + items + '''
      </div>
    </div>'''

def has_article_jsonld(content):
    return '"@type": "Article"' in content or '"@type":"Article"' in content

def has_related_section(content):
    return 'related-articles' in content and ('Bai viet lien quan' in content or 'related-grid' in content)

def get_title(content):
    m = re.search(r'<title>([^<]+)</title>', content)
    return m.group(1) if m else ""

def get_description(content):
    m = re.search(r'<meta name="description" content="([^"]+)"', content)
    return m.group(1) if m else ""

def get_canonical_url(content):
    m = re.search(r'<link rel="canonical" href="([^"]+)"', content)
    if m:
        return m.group(1)
    # Try og:url
    m2 = re.search(r'<meta property="og:url" content="([^"]+)"', content)
    if m2:
        return m2.group(1)
    return ""

def process_file(filepath, fname):
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    original = content
    changed = False
    
    # 1. Add Article JSON-LD if missing
    if not has_article_jsonld(content):
        title = get_title(content)
        description = get_description(content)
        url = get_canonical_url(content)
        if not url:
            url = f"https://trolythongminh.io.vn/blog/{fname}"
        
        jsonld = make_jsonld(title, description, url)
        # Insert before </head>
        if '</head>' in content:
            content = content.replace('</head>', jsonld + '\n</head>', 1)
            changed = True
            print(f"  [JSON-LD] Added to {fname}")
        else:
            print(f"  [SKIP JSON-LD] No </head> in {fname}")
    
    # 2. Add related section if missing and we have a mapping
    if not has_related_section(content) and fname in RELATED:
        links = RELATED[fname]
        related_html = make_related_section(links)
        # Insert before </article> or before </main> or before </body>
        inserted = False
        for tag in ['</article>', '</main>', '</body>']:
            if tag in content:
                content = content.replace(tag, '\n' + related_html + '\n' + tag, 1)
                changed = True
                inserted = True
                print(f"  [RELATED] Added to {fname} (before {tag})")
                break
        if not inserted:
            print(f"  [SKIP RELATED] No insertion point in {fname}")
    elif not has_related_section(content) and fname not in RELATED:
        print(f"  [SKIP RELATED] No mapping for {fname}")
    
    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# Process all blog HTML files
files = [f for f in os.listdir(BLOG_DIR) if f.endswith('.html') and f != 'index.html']
files.sort()

modified_count = 0
jsonld_added = 0
related_added = 0

for fname in files:
    fpath = os.path.join(BLOG_DIR, fname)
    with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    needs_jsonld = not has_article_jsonld(content)
    needs_related = not has_related_section(content) and fname in RELATED
    
    if needs_jsonld or needs_related:
        print(f"Processing: {fname}")
        if process_file(fpath, fname):
            modified_count += 1
            if needs_jsonld: jsonld_added += 1
            if needs_related: related_added += 1

print(f"\n=== DONE ===")
print(f"Files modified: {modified_count}")
print(f"JSON-LD added: {jsonld_added}")
print(f"Related sections added: {related_added}")
