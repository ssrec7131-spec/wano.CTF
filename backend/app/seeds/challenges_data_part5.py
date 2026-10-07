"""Round 1 challenge dataset definitions for WANO CTF - Part 5 (Forensics, OSINT, Linux expansion)."""

from app.models.enums import Difficulty

CHALLENGES_PART_5 = [
    # ── FORENSICS (3 more) ──
    {
        "title": "Stego Pixel",
        "slug": "stego-pixel",
        "category": "forensics",
        "difficulty": Difficulty.MEDIUM,
        "points": 200,
        "flag": "WANO{ls8_st3g4n0gr4phy_p1x3l}",
        "description": "A seemingly normal sunset photograph hides data in the least significant bits of each pixel's RGB values. Extract the LSB plane to reveal the hidden message containing the flag.",
        "hints": [
            {"text": "Steganography hides data inside the noise floor of images.", "cost": 25},
            {"text": "Use zsteg or stegsolve to extract LSB data from the image.", "cost": 45},
        ],
    },
    {
        "title": "Memory Forensics",
        "slug": "memory-forensics",
        "category": "forensics",
        "difficulty": Difficulty.EXPERT,
        "points": 400,
        "flag": "WANO{v0l4t1l1ty_pr0c3ss_dump}",
        "description": "A RAM dump was captured from a compromised Windows machine. Use Volatility 3 to analyze the memory image, list running processes, and extract the flag from a suspicious notepad.exe process.",
        "hints": [
            {"text": "Volatility is the standard tool for memory forensics analysis.", "cost": 50},
            {"text": "Run: vol -f memdump.raw windows.pslist then windows.memmap --dump --pid <notepad_pid>", "cost": 80},
        ],
    },
    {
        "title": "PDF Layers",
        "slug": "pdf-layers",
        "category": "forensics",
        "difficulty": Difficulty.EASY,
        "points": 100,
        "flag": "WANO{pdf_h1dd3n_l4y3r_0bj3ct}",
        "description": "A classified PDF document appears blank on screen but contains hidden text layers behind a white rectangle overlay. Remove or reorder the layers to reveal the concealed flag.",
        "hints": [
            {"text": "PDFs can have multiple overlapping layers — some may be hidden.", "cost": 15},
            {"text": "Open in a PDF editor like Inkscape or use pdftotext to extract raw text.", "cost": 30},
        ],
        "artifact": ("classified_doc.pdf", "%PDF-1.4 Hidden Layer Object\n/Type /Page\n% Flag: WANO{pdf_h1dd3n_l4y3r_0bj3ct}\n%%EOF\n", "application/pdf"),
    },

    # ── OSINT (3 more) ──
    {
        "title": "Username Trail",
        "slug": "username-trail",
        "category": "osint",
        "difficulty": Difficulty.EASY,
        "points": 100,
        "flag": "WANO{sh3rl0ck_us3rn4m3_hunt3r}",
        "description": "An anonymous threat actor uses the handle 'shadow_byte_42' across multiple social media platforms. Use OSINT tools like Sherlock or Namechk to locate all their profiles and find the flag in their bio.",
        "hints": [
            {"text": "Tools like Sherlock can search hundreds of platforms for a username.", "cost": 15},
            {"text": "Run: sherlock shadow_byte_42 and check GitHub/Pastebin profiles.", "cost": 25},
        ],
    },
    {
        "title": "Email OSINT",
        "slug": "email-osint",
        "category": "osint",
        "difficulty": Difficulty.MEDIUM,
        "points": 200,
        "flag": "WANO{h4v31b33npwn3d_br34ch_d4t4}",
        "description": "The email admin@target-corp.example was found in a phishing campaign. Check data breach databases and WHOIS records to trace the domain's registration details and find the flag hidden in the registrant's organization field.",
        "hints": [
            {"text": "WHOIS records contain domain registration details including registrant info.", "cost": 25},
            {"text": "Use haveibeenpwned.com for breach data and whois for domain lookup.", "cost": 45},
        ],
    },
    {
        "title": "Satellite Recon",
        "slug": "satellite-recon",
        "category": "osint",
        "difficulty": Difficulty.HARD,
        "points": 300,
        "flag": "WANO{g30l0c4t10n_s4t3ll1t3_v13w}",
        "description": "A leaked satellite image shows a distinctive triangular building near a runway with exactly 3 taxiways. The facility has a visible helipad on the roof. Identify the exact airport ICAO code and coordinates.",
        "hints": [
            {"text": "Use Google Earth Pro to search for triangular airport terminals.", "cost": 40},
            {"text": "Cross-reference the runway configuration with OurAirports database.", "cost": 60},
        ],
    },
]
