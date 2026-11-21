import os
import sys
import html
import random
import pandas as pd
import numpy as np

# Ensure UTF-8 output encoding on Windows console
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# =====================================================================
# DIVERSE ILLICIT CYBER DRUG TRAFFICKING CORPUS GENERATOR
# =====================================================================

SUBSTANCES = [
    ("pure uncut ❄️ cocaine fishscale", "drug_coke"),
    ("high purity 💊 Xanax 2mg bars and Valium", "drug_benzos"),
    ("lab-tested 💉 Afghan heroin brown sugar", "drug_heroin"),
    ("liquid 🧪 methamphetamine and crystal ice 🧊", "drug_meth"),
    ("exotic loud 🌿 weed packs and live rosin wax 🍯", "drug_weed"),
    ("trippy golden teacher 🍄 shrooms and DMT", "drug_psychedelics"),
    ("top grade 🍬 MDMA ecstasy pressies and 2CB", "drug_mdma"),
    ("pharmaceutical Oxycontin 80mg and Percocet 💊", "drug_opioids"),
    ("pure LSD gel tabs 🌌 and blotters", "drug_lsd"),
    ("clean Adderall 30mg and Ritalin for focus 💊", "drug_stimulants"),
    ("bulk THC vape carts 🍁 and delta-9 edibles 🍫", "drug_thc"),
    ("medical grade Ketamine shards 💎 and powder", "drug_ketamine"),
    ("unadulterated fentanyl-free 💉 smack and black tar", "drug_opiates"),
    ("high potency shatter 🍯 and dispensary bud 🌿", "drug_cannabis"),
    ("alprazolam powder and pressed B707 blue bars 💊", "drug_counterfeit_pills"),
]

CHANNELS = [
    "Telegram @coke_vendor_uk",
    "Telegram @dispensary_express",
    "Telegram @pharma_plug_direct",
    "Telegram @trippy_psychedelics",
    "Telegram @dark_chemist_99",
    "Telegram @pure_gear_distro",
    "Wickr: stealthmaster420",
    "Wickr: chemicalplug",
    "Wickr: whitecoke_supplier",
    "Session ID 05a6f7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7",
    "Session ID 05112233445566778899aabbccddeeff00112233445566778899aabbccddeeff00",
    "Tor market silkroad3.onion with Escrow",
    "darknet market drugnet.onion profile vendor",
    "Telegram @snow_wholesaler_eu",
    "Telegram @trap_connect_us",
]

SHIPPING_TERMS = [
    "Stealth packaging 100% guaranteed delivery worldwide.",
    "Double vacuum-sealed decoy package, overnight courier.",
    "Discreet shipping to US, UK, and Europe with tracking code.",
    "Dead-drop coordinates in major cities or express postal dispatch.",
    "Guaranteed safe stealth delivery, no customs issues.",
    "Next-day express airmail in smell-proof moisture barrier bags.",
    "Drop-shipping available with full escrow guarantee.",
]

PAYMENTS = [
    "BTC wallet 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa or Monero XMR",
    "Monero 48edfRBDwTWeeBMyJ2b3fWAwjXx3M for untraceable anonymity",
    "Bitcoin bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh or CashApp",
    "Crypto only: BTC, ETH, and XMR accepted via Escrow",
    "CashApp, Venmo, Zelle, and Bitcoin accepted",
    "Monero preferred, Bitcoin escrow on darknet forum",
    "Payment via BTC 3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy",
]

OFFERS = [
    "Fresh drop just landed! Bulk discounts available for resellers.",
    "Top rated verified vendor on darknet forums. No prescription required.",
    "Looking to score fire product? Best quality uncut stock in town.",
    "Tested 99% pure in laboratory tests. No dangerous cuts or fentanyl.",
    "Wholesale price list available on request. Fast response guaranteed.",
    "Reliable supplier with 5-star reviews on Dread forum.",
    "Restocked with fresh inventory! DM the plug directly to place an order.",
]

# Hard / Subtle Illicit cases (Street jargon, short posts, coded slang)
HARD_ILLICIT_SAMPLES = [
    "Hit my line for the best white in town. Quick drop in central. Wickr: fastdelivery7",
    "Got clean presses on deck. Tested fent free. DM Telegram channel @city_connect",
    "Need something for the party tonight? Menu ready on Session. Cash or crypto accepted.",
    "Uncut fishscale packs landed this morning. Message @snow_drop on Telegram.",
    "Overnight stealth bags arriving daily. Hit the vendor profile on Dread or Wickr: packman.",
    "Quality gear available for local collection or tracked delivery. Contact @plug_247 on Telegram.",
    "Looking for pharmaceutical hulks and blues? Bulk boxes available. Wickr: bulkbars.",
    "Brown sugar Afghan supply ready for dispatch. Monero payment only. @afghan_source",
    "Crystal shards high purity. Wholesale kilos and ounces. Contact Telegram @ice_distro.",
    "Top shelf exotics and carts. Telegram @green_run for menu. Discreet packaging.",
    "Special discount on 100x pressed tabs. Escrow available on onion link. DM for details.",
    "Fresh pressies just stamped. Safe drop guaranteed. Reach out on Wickr: pressedclean.",
    "Pure powder direct from lab. DM @chem_master on Telegram. Bitcoin only.",
    "Got bars and syrup in stock. Serious buyers only. Session ID 05f4e3d2c1b0a987654321.",
    "Top rated vendor profile on darkweb market. Fast dispatch, escrow enabled. @plug_verified",
]

def generate_unique_illicit_samples(target_count: int = 400) -> list:
    """Generates a diverse set of UNIQUE illicit drug trafficking posts."""
    random.seed(42)
    samples = set(HARD_ILLICIT_SAMPLES)
    
    while len(samples) < target_count:
        sub, _ = random.choice(SUBSTANCES)
        chan = random.choice(CHANNELS)
        ship = random.choice(SHIPPING_TERMS)
        pay = random.choice(PAYMENTS)
        off = random.choice(OFFERS)
        
        template_idx = random.randint(0, 4)
        if template_idx == 0:
            text = f"{off} {sub}. Contact plug via {chan}. {ship} Pay with {pay}."
        elif template_idx == 1:
            text = f"Got {sub} ready for dispatch. {ship} Hit up {chan}. {pay} accepted. {off}"
        elif template_idx == 2:
            text = f"{sub} in stock! {off} Message on {chan}. {pay}. {ship}"
        elif template_idx == 3:
            text = f"Direct supplier for {sub}. No doctor visit needed. Connect on {chan} for price menu. {ship} {pay}."
        else:
            text = f"🚨 Fire batch update: {sub}. Fast dispatch. Order via {chan}. Escrow protected. {pay}. {ship}"
            
        samples.add(text)
        
    return list(samples)[:target_count]

# =====================================================================
# DIVERSE BENIGN / GENERAL COMMUNICATION CORPUS GENERATOR
# Includes Adversarial Boundary Traps (Benign posts with drug-like words)
# =====================================================================

ADVERSARIAL_BENIGN_TRAPS = [
    "The winter storm brought beautiful pure white snow ❄️ to our neighborhood this morning. Love winter!",
    "My physician prescribed daily multivitamin pills 💊 and iron supplements after my annual blood test.",
    "My phone charger plug 🔌 broke yesterday. Does anyone know where to buy an authentic replacement cable?",
    "Went mushroom 🍄 hunting with my family in the state forest and found edible chanterelles.",
    "I was watching the Breaking Bad series where characters cook crystal meth in an RV. Masterpiece show!",
    "Donated blood at the local Red Cross clinic today. The nurse used a sterile needle 💉 and was very gentle.",
    "Our university organic chemistry lab exam tomorrow covers chemical synthesis and catalytic reagents 🧪.",
    "Studying blockchain cryptography in computer science and wrote a script to validate bitcoin wallet addresses.",
    "Bought delicious dark chocolates 🍫 and strawberry candy 🍬 from the local confectionery shop downtown.",
    "Looking for a reliable commercial electrical wall plug 🔌 supplier for our office construction renovation.",
    "Reading an investigative journalism documentary about international law enforcement countering illicit trafficking.",
    "The snowfall ❄️ in the ski resort created ideal powder conditions for snowboarding this weekend.",
    "Taking allergy medicine pills 💊 every spring because of high pollen counts from oak and cedar trees.",
    "My laptop power supply plug 🔌 stopped working during the lecture. Had to borrow a spare charger.",
    "Cultivating edible oyster mushrooms 🍄 at home using coffee grounds and organic straw substrates.",
    "Learning Python network sockets to create a peer to peer messaging chat application for college project.",
    "Visiting an herbal botanical garden to study medicinal herbs and lavender plants 🌿 this Sunday.",
    "The football coach praised our team's defense for locking down the opposing striker in yesterday's game.",
    "Brewing homemade herbal tea with organic dried mint leaves 🍃 and raw clover honey 🍯.",
    "The documentary explained how forensic toxicology uses chromatography to identify unknown chemical substances.",
]

BENIGN_TOPICS = [
    "Machine learning and artificial intelligence are transforming modern software development.",
    "Had a great morning workout at the campus gym followed by a protein smoothie.",
    "Can anyone recommend a good cozy cafe with reliable Wi-Fi for studying in downtown?",
    "The library study rooms are fully booked for final exam week. Planning to study at home.",
    "Just finished reading a fascinating novel on quantum physics and universe cosmology.",
    "Looking forward to the weekend hiking trip in the national park with college friends.",
    "Recipe for authentic homemade pasta: semolina flour, fresh eggs, olive oil, and salt.",
    "Our university sports team won the inter-college basketball tournament last night!",
    "Flight was delayed by three hours due to heavy monsoon rains at the international airport.",
    "Anyone interested in forming a study group for advanced database management systems?",
    "The new sci-fi movie release features incredible cinematography and soundtrack.",
    "Need recommendations for budget friendly mechanical keyboards under fifty dollars.",
    "Python list comprehensions and generator expressions make data pipelines concise.",
    "Attending an international IEEE conference next month to present our research paper.",
    "Happy birthday to my best friend! Wishing you an incredible year ahead filled with joy.",
    "The spring festival on campus had fantastic food stalls and live acoustic music.",
    "Exploring cloud microservices using Docker containers and Kubernetes clusters.",
    "Great football match yesterday evening! The second half comeback was breathtaking.",
    "Remember to submit the computer networks assignment before Friday midnight deadline.",
    "Started learning digital photography and landscape composition over the weekend.",
    "What are the best tourist places to visit in Kyoto during the cherry blossom season?",
    "Looking to sell my gently used mountain bike. Message me if interested in test ride.",
    "The university career fair had great tech companies offering summer internships.",
    "Cooking vegetable lasagna tonight with fresh mozzarella and homemade tomato sauce.",
    "Our capstone project review went very well today. Faculty appreciated the architecture.",
    "The weather forecast predicts sunny skies and pleasant breeze throughout this weekend.",
    "Solving algorithmic problems on LeetCode to prepare for software engineering interviews.",
    "Visited the modern art museum today. The contemporary sculpture gallery was inspiring.",
    "Does anyone have lecture notes for digital signal processing from Tuesday class?",
    "Setting up a Linux home server using Raspberry Pi for local automated file backup.",
]

def generate_unique_benign_samples(target_count: int = 400) -> list:
    """Generates a rich, diverse set of UNIQUE benign everyday messages including adversarial traps."""
    random.seed(101)
    samples = set(ADVERSARIAL_BENIGN_TRAPS)
    
    for s in BENIGN_TOPICS:
        samples.add(s)
        
    prefixes = [
        "Quick update:", "In case anyone was wondering,", "Hey everyone,",
        "Just wanted to share:", "Friendly reminder:", "Interesting discussion today:",
        "Personal note:", "From my perspective,", "Weekend thoughts:", "Sharing some thoughts:"
    ]
    
    suffixes = [
        "Feel free to share your thoughts or recommendations below!",
        "Let me know if anyone wants to join or has tips.",
        "Always great to make steady progress every single day.",
        "Looking forward to hearing everyone's feedback soon.",
        "Hope everyone has a productive and wonderful week ahead!",
        "Drop a comment if you have experienced something similar.",
        "Excited to see where this project and learning journey leads."
    ]
    
    while len(samples) < target_count:
        base = random.choice(BENIGN_TOPICS)
        pre = random.choice(prefixes)
        suf = random.choice(suffixes)
        choice = random.randint(0, 3)
        if choice == 0:
            text = f"{pre} {base}"
        elif choice == 1:
            text = f"{base} {suf}"
        elif choice == 2:
            text = f"{pre} {base} {suf}"
        else:
            base2 = random.choice(BENIGN_TOPICS)
            while base2 == base:
                base2 = random.choice(BENIGN_TOPICS)
            text = f"{base} Also, {base2.lower()}"
        samples.add(text)
        
    return list(samples)[:target_count]

# =====================================================================
# MASTER DATASET LOADER (BALANCED, ZERO-DUPLICATE 3-CLASS DATASET)
# =====================================================================

def load_and_prepare_dataset(csv_path: str = "dataset/drugsComTrain_raw.csv", sample_size_per_class: int = 400):
    """
    Loads raw medical dataset, extracts legitimate medical reviews,
    and combines them with non-duplicate illicit drug trafficking posts
    and benign general communications to construct a clean, realistic 3-class target dataset.
    
    Classes:
    - 0: General / Benign
    - 1: Legitimate Medical Review
    - 2: Illicit Drug Trafficking / Distribution
    """
    data = []
    
    # 1. Load Real Medical Reviews (Class 1) - Include opioid/painkiller reviews for realistic boundary testing
    resolved_path = os.path.abspath(csv_path)
    if not os.path.exists(resolved_path):
        possible_path = os.path.join(os.path.dirname(__file__), "drugsComTrain_raw.csv")
        if os.path.exists(possible_path):
            resolved_path = possible_path
            
    if os.path.exists(resolved_path):
        print(f"Loading legitimate medical reviews from: {resolved_path}")
        df_raw = pd.read_csv(resolved_path)
        
        # Filter reviews that are genuine and unescape HTML
        raw_reviews = df_raw['review'].dropna().astype(str).tolist()
        cleaned_reviews = list(set([html.unescape(r).strip() for r in raw_reviews if len(r.strip()) > 35]))
        
        random.seed(42)
        med_samples = random.sample(cleaned_reviews, min(sample_size_per_class, len(cleaned_reviews)))
        for text in med_samples:
            data.append({'text': text, 'label': 1, 'category': 'Legitimate Medical Review'})
    else:
        print(f"Warning: {resolved_path} not found. Using fallback medical samples.")
        fallback_med = [
            "My doctor prescribed Lisinopril 10mg for high blood pressure. It stabilized my numbers with no major side effects.",
            "I have been taking Sertraline 50mg for generalized anxiety disorder for six months. It noticeably reduced panic attacks.",
            "Started Metformin 500mg twice daily for type 2 diabetes. Experienced mild stomach upset during the first week.",
            "Using Albuterol inhaler as needed for exercise-induced asthma. Provides rapid relief within minutes.",
            "Consulted my dermatologist regarding persistent acne. Prescribed topical Tretinoin cream with clear improvement."
        ]
        for t in fallback_med * (sample_size_per_class // len(fallback_med) + 1):
            if len(data) < sample_size_per_class:
                data.append({'text': t, 'label': 1, 'category': 'Legitimate Medical Review'})

    # 2. Generate Diverse, Unique Illicit Trafficking Samples (Class 2)
    print(f"Generating {sample_size_per_class} unique illicit trafficking samples (including subtle street jargon)...")
    illicit_samples = generate_unique_illicit_samples(target_count=sample_size_per_class)
    for text in illicit_samples:
        data.append({'text': text, 'label': 2, 'category': 'Illicit Drug Trafficking'})

    # 3. Generate Diverse, Unique General / Benign Samples (Class 0)
    print(f"Generating {sample_size_per_class} unique benign conversational samples (including adversarial traps)...")
    benign_samples = generate_unique_benign_samples(target_count=sample_size_per_class)
    for text in benign_samples:
        data.append({'text': text, 'label': 0, 'category': 'General / Benign'})

    full_df = pd.DataFrame(data)
    
    # Verify no duplicate text across dataset
    full_df = full_df.drop_duplicates(subset=['text']).reset_index(drop=True)
    
    # Shuffle dataset
    full_df = full_df.sample(frac=1.0, random_state=42).reset_index(drop=True)
    print(f"Dataset successfully constructed: {len(full_df)} total unique samples across 3 classes.")
    return full_df

def save_preprocessed_dataset_csv(output_csv: str = "dataset/preprocessed_data.csv", sample_size_per_class: int = 400):
    """
    Applies the full 8-Stage NLP Preprocessing Pipeline to the dataset
    and exports a structured CSV containing both raw and preprocessed data.
    """
    from preprocessing.preprocess import clean_text
    
    print("\n--- Generating Persisted Preprocessed Dataset CSV ---")
    df = load_and_prepare_dataset(sample_size_per_class=sample_size_per_class)
    
    print("Executing 8-Stage NLP Preprocessing on all samples...")
    df['preprocessed_text'] = df['text'].apply(clean_text)
    
    # Rename and organize columns
    df = df.rename(columns={'text': 'raw_text'})
    df = df[['raw_text', 'preprocessed_text', 'label', 'category']]
    
    # Save main file
    resolved_output = os.path.abspath(output_csv)
    df.to_csv(resolved_output, index=False, encoding='utf-8')
    print(f"✅ Successfully saved preprocessed dataset to: {resolved_output}")
    
    # Also save to dataset/drug_data.csv
    drug_data_path = os.path.join(os.path.dirname(resolved_output), "drug_data.csv")
    df.to_csv(drug_data_path, index=False, encoding='utf-8')
    print(f"✅ Also updated: {drug_data_path}")
    
    return df

if __name__ == "__main__":
    df = save_preprocessed_dataset_csv()
    print("\nPreprocessed Dataset Shape:", df.shape)
    print("Class Counts:\n", df['category'].value_counts())
    print("\nPreview of Before vs. After Preprocessing:")
    for i, row in df.head(3).iterrows():
        print(f"\n--- Sample {i+1} [{row['category']}] ---")
        print("RAW TEXT:         ", row['raw_text'][:100], "...")
        print("PREPROCESSED TEXT:", row['preprocessed_text'][:100], "...")

