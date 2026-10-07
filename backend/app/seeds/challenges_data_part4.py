"""Round 1 challenge dataset definitions for WANO CTF - Part 4 (Web, Crypto, Forensics expansion)."""

from app.models.enums import Difficulty

CHALLENGES_PART_4 = [
    # ── WEB (4 more) ──
    {
        "title": "Header Hijack",
        "slug": "header-hijack",
        "category": "web",
        "difficulty": Difficulty.EASY,
        "points": 100,
        "flag": "WANO{x_forw4rd3d_f0r_127_0_0_1}",
        "description": "An admin dashboard restricts access to internal IPs only by checking the X-Forwarded-For header. Forge the header to spoof your request origin and access the restricted endpoint.",
        "hints": [
            {"text": "HTTP headers can be manipulated by the client before reaching the server.", "cost": 15},
            {"text": "Set X-Forwarded-For: 127.0.0.1 in your request.", "cost": 25},
        ],
    },
    {
        "title": "IDOR Exposed",
        "slug": "idor-exposed",
        "category": "web",
        "difficulty": Difficulty.MEDIUM,
        "points": 200,
        "flag": "WANO{1ns3cur3_d1r3ct_0bj3ct_r3f}",
        "description": "A user profile API at /api/profile?id=1042 returns your own data. The server only checks if you are authenticated, not whether the requested resource belongs to you. Access another user's profile to retrieve their secret flag field.",
        "hints": [
            {"text": "Try changing the 'id' parameter to a different user's ID.", "cost": 25},
            {"text": "Increment or decrement the id value: /api/profile?id=1 often works.", "cost": 40},
        ],
    },
    {
        "title": "JWT None Algorithm",
        "slug": "jwt-none-algorithm",
        "category": "web",
        "difficulty": Difficulty.HARD,
        "points": 300,
        "flag": "WANO{jwt_n0n3_4lg_byp4ss_cr1t1c4l}",
        "description": "The API uses JSON Web Tokens for authentication. The server accepts the 'none' algorithm, allowing you to forge a token without a valid signature. Craft a JWT with alg: none and set your role to admin.",
        "hints": [
            {"text": "Decode the existing JWT (header.payload.signature) from your cookie.", "cost": 40},
            {"text": "Change alg to 'none', set role to 'admin', remove the signature, and re-encode.", "cost": 60},
        ],
    },
    {
        "title": "Server Side Request Forgery",
        "slug": "ssrf-internal",
        "category": "web",
        "difficulty": Difficulty.EXPERT,
        "points": 400,
        "flag": "WANO{ssrf_m3t4d4t4_169_254_cl0ud}",
        "description": "A URL preview feature at /api/preview?url=... fetches and renders external content. The server has no URL validation. Access the cloud instance metadata endpoint at http://169.254.169.254/latest/meta-data/ to retrieve the hidden flag.",
        "hints": [
            {"text": "The server makes HTTP requests on your behalf — you control the destination.", "cost": 50},
            {"text": "Try pointing the URL to http://169.254.169.254/latest/meta-data/flag", "cost": 80},
        ],
    },

    # ── CRYPTO (4 more) ──
    {
        "title": "Vigenère's Vault",
        "slug": "vigeneres-vault",
        "category": "crypto",
        "difficulty": Difficulty.MEDIUM,
        "points": 200,
        "flag": "WANO{v1g3n3r3_p0ly4lph4b3t1c}",
        "description": "A polyalphabetic ciphertext was intercepted: DAES{d1o3y3z3_b0gq4kbi4f3g1w}. The encryption key is 'WANO' repeated. Apply the Vigenère decryption to recover the flag.",
        "hints": [
            {"text": "Unlike Caesar cipher, each letter is shifted by a different amount based on the key.", "cost": 25},
            {"text": "The key is 'WANO'. Subtract each key letter's position from the ciphertext letter.", "cost": 45},
        ],
    },
    {
        "title": "RSA Tiny Primes",
        "slug": "rsa-tiny-primes",
        "category": "crypto",
        "difficulty": Difficulty.HARD,
        "points": 300,
        "flag": "WANO{sm4ll_pr1m3s_f4ct0r_34sy}",
        "description": "RSA public key: n = 3233, e = 17. The modulus is small enough to factor by trial division. Compute the private key d and decrypt the ciphertext c = 2790 to retrieve the flag.",
        "hints": [
            {"text": "Factor n into two primes p and q. Try small primes: 2, 3, 5, 7, 11...", "cost": 35},
            {"text": "n = 61 × 53. Compute φ(n) = (61-1)(53-1) = 3120. Find d where e*d ≡ 1 mod 3120.", "cost": 60},
        ],
    },
    {
        "title": "Hash Cracker",
        "slug": "hash-cracker",
        "category": "crypto",
        "difficulty": Difficulty.EASY,
        "points": 100,
        "flag": "WANO{md5_r41nb0w_t4bl3_cr4ck}",
        "description": "An intercepted MD5 hash was found in a leaked database: 5d41402abc4b2a76b9719d911017c592. The plaintext is a common English word. Crack it using rainbow tables or hashcat.",
        "hints": [
            {"text": "MD5 is a one-way hash — but common words can be looked up in rainbow tables.", "cost": 15},
            {"text": "Try CrackStation.net or hashcat with rockyou.txt wordlist.", "cost": 25},
        ],
    },
    {
        "title": "Padding Oracle",
        "slug": "padding-oracle",
        "category": "crypto",
        "difficulty": Difficulty.EXPERT,
        "points": 450,
        "flag": "WANO{p4dd1ng_0r4cl3_cbc_4tt4ck}",
        "description": "An AES-CBC encrypted cookie returns different error messages for invalid padding vs. invalid data. Use a padding oracle attack to decrypt the cookie byte-by-byte without knowing the key.",
        "hints": [
            {"text": "The server leaks information through distinct error responses (403 vs 500).", "cost": 60},
            {"text": "Modify the IV byte-by-byte and observe which values produce valid PKCS#7 padding.", "cost": 90},
        ],
    },
]
