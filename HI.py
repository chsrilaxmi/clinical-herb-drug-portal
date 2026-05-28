import streamlit as st
import pandas as pd
import json

# 1. Setup page configurations
st.set_page_config(
    page_title="Clinical Herb-Drug Interaction Portal",
    page_icon="🌿",
    layout="wide"
)

# Professional Custom CSS for Premium Medical UI/UX
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .metric-box {
        background-color: #ffffff; padding: 15px; border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05); border-left: 5px solid #2E7D32; margin-bottom: 20px;
        max-width: 300px;
    }
    .interaction-card {
        background-color: #ffffff; padding: 20px; border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #e0e0e0; margin-bottom: 20px;
    }
    .severity-severe {
        background-color: #FFEBEE; color: #C62828; padding: 6px 12px;
        border-radius: 20px; font-weight: bold; font-size: 14px; display: inline-block; border: 1px solid #FFCDD2;
    }
    .severity-moderate {
        background-color: #FFFDE7; color: #F57F17; padding: 6px 12px;
        border-radius: 20px; font-weight: bold; font-size: 14px; display: inline-block; border: 1px solid #FFF9C4;
    }
    .severity-low {
        background-color: #E8F5E9; color: #2E7D32; padding: 6px 12px;
        border-radius: 20px; font-weight: bold; font-size: 14px; display: inline-block; border: 1px solid #C8E6C9;
    }
    </style>
""", unsafe_allow_html=True)

# Master Multilingual Database
data = [
    # --- ST. JOHN'S WORT ---
    {
        "Herb": "St. John's Wort (సెయింట్ జాన్స్ వోర్ట్ / सेंट जॉन्स वॉर्ट)", "Herb_Keywords": ["st. john's wort", "john", "wort", "సెయింట్", "జాన్స్"],
        "Drug": "Cyclosporine, Tacrolimus", "Drug_Keywords": ["cyclosporine", "tacrolimus", "immunosuppressant"], "Severity": "Severe",
        "Effect_English": "Marked reduction in immunosuppressant levels; leads to organ transplant rejection.",
        "Effect_Telugu": "ఇమ్యునోసప్రెసెంట్ స్థాయిలు తగ్గి, అవయవ మార్పిడి వైఫల్యానికి దారితీస్తుంది.",
        "Effect_Hindi": "इम्यूनोसप्रेसेन्ट का स्तर कम हो जाता है; अंग प्रत्यारोपण विफलता का कारण बनता है।"
    },
    {
        "Herb": "St. John's Wort (సెయింట్ జాన్స్ వోర్ట్ / सेंट जॉन्स वॉर्ट)", "Herb_Keywords": ["st. john's wort", "john", "wort"],
        "Drug": "Warfarin", "Drug_Keywords": ["warfarin", "blood thinner"], "Severity": "Severe",
        "Effect_English": "Decreased anticoagulant efficacy and decreased INR, significantly increasing thromboembolism risk.",
        "Effect_Telugu": "రక్తం గడ్డకట్టకుండా ఉండే సామర్థ్యం తగ్గి, థ్రాంబోఎంబోలిజం ప్రమాదాన్ని పెంచుతుంది.",
        "Effect_Hindi": "एंटीकोआगुलंट प्रभावशीलता कम हो जाती है, जिससे थ्रोम्बोएम्बोलिज़्म का खतरा बढ़ जाता है।"
    },
    {
        "Herb": "St. John's Wort (సెయింట్ జాన్స్ వోర్ట్ / सेंट जॉन्स वॉर्ट)", "Herb_Keywords": ["st. john's wort", "john", "wort"],
        "Drug": "SSRIs (e.g., Sertraline)", "Drug_Keywords": ["ssri", "ssris", "sertraline", "antidepressant", "depression", "డిప్రెషన్"], "Severity": "Severe",
        "Effect_English": "Serotonin syndrome characterized by hyperthermia, tremors, and autonomic instability.",
        "Effect_Telugu": "సెరోటోనిన్ సిండ్రోమ్ (అధిక జ్వరం, వణుకు, మరియు రక్తపోటు వైవిధ్యాలు).",
        "Effect_Hindi": "सेरोटोनिन सिंड्रोम (तेज बुखार, कंपकंपी और स्वायत्त अस्थिरता)।"
    },
    {
        "Herb": "St. John's Wort (సెయింట్ జాన్స్ వోర్ట్ / सेंट जॉन्स वॉर्ट)", "Herb_Keywords": ["st. john's wort", "john", "wort"],
        "Drug": "Oral Contraceptives", "Drug_Keywords": ["contraceptives", "birth control", "pregnancy", "pill", "మాత్రలు"], "Severity": "Severe",
        "Effect_English": "Unintended pregnancies and breakthrough bleeding due to accelerated drug metabolism.",
        "Effect_Telugu": "గర్భనిరోధక సామర్థ్యం తగ్గి అవాంఛిత గర్భం మరియు రక్తస్రావం జరగవచ్చు.",
        "Effect_Hindi": "गर्भनिरोधक प्रभाव कम होने से अनचाहा गर्भ और रक्तस्राव हो सकता है।"
    },
    {
        "Herb": "St. John's Wort (సెయింట్ జాన్స్ వోర్ట్ / सेंट जॉन्स वॉर्ट)", "Herb_Keywords": ["st. john's wort", "john", "wort"],
        "Drug": "HIV Protease Inhibitors", "Drug_Keywords": ["hiv", "protease", "antiretroviral", "aids"], "Severity": "Severe",
        "Effect_English": "Drastic drop in antiretroviral plasma concentrations; results in rapid viral resistance.",
        "Effect_Telugu": "హెచ్ఐవి ఔషధాల ప్రభావం తగ్గి వైరల్ నిరోధకత వేగంగా పెరుగుతుంది.",
        "Effect_Hindi": "एचआईवी दवाओं का प्रभाव कम हो जाता है, जिससे वायरल प्रतिरोध तेजी से बढ़ता है।"
    },
    # --- GINKGO BILOBA ---
    {
        "Herb": "Ginkgo Biloba (జింకో బైలోబా / जिन्कगो बिलोबा)", "Herb_Keywords": ["ginkgo", "biloba", "జింకో", "బైలోబా"],
        "Drug": "Warfarin / Aspirin", "Drug_Keywords": ["warfarin", "aspirin", "blood thinner"], "Severity": "Severe",
        "Effect_English": "Spontaneous hemorrhage, internal bleeding, and prolonged clotting times.",
        "Effect_Telugu": "అకస్మాత్తుగా అంతర్గత రక్తస్రావం జరగడం మరియు రక్తం గడ్డకట్టే సమయం పెరగడం.",
        "Effect_Hindi": "अचानक आंतरिक रक्तस्राव और रक्त के थक्के जमने के समय में वृद्धि।"
    },
    {
        "Herb": "Ginkgo Biloba (జింకో బైలోబా / जिन्कगो बिलोबा)", "Herb_Keywords": ["ginkgo", "biloba"],
        "Drug": "Trazodone", "Drug_Keywords": ["trazodone", "sedative"], "Severity": "Severe",
        "Effect_English": "Excessive sedation and potential coma due to enhanced GABAergic activity.",
        "Effect_Telugu": "తీవ్రమైన మగత మరియు కోమాలోకి వెళ్లే ప్రమాదం ఉంది.",
        "Effect_Hindi": "अत्यधिक बेहोशी और कोमा में जाने का गंभीर खतरा।"
    },
    # --- GINSENG ---
    {
        "Herb": "Ginseng - Panax (జిన్సెంగ్ / जिन्सेंग)", "Herb_Keywords": ["ginseng", "జిన్సెంగ్", "panax"],
        "Drug": "Warfarin", "Drug_Keywords": ["warfarin"], "Severity": "Severe",
        "Effect_English": "Significantly lowers therapeutic efficacy of warfarin, raising blood clot risks.",
        "Effect_Telugu": "వార్ఫరిన్ సామర్థ్యాన్ని తగ్గించి, రక్తం గడ్డకట్టే ప్రమాదాన్ని పెంచుతుంది.",
        "Effect_Hindi": "वारफारिन की प्रभावशीलता कम हो जाती है, जिससे रक्त के थक्के जमने का खतरा बढ़ जाता है।"
    },
    {
        "Herb": "Ginseng - Panax (జిన్సెంగ్ / जिन्सेंग)", "Herb_Keywords": ["ginseng", "జిన్సెంగ్"],
        "Drug": "Phenelzine (MAOI)", "Drug_Keywords": ["phenelzine", "maoi"], "Severity": "Severe",
        "Effect_English": "Induces manic episodes, extreme insomnia, headaches, and tremors.",
        "Effect_Telugu": "మానసిక ఉద్రేకం (ఉన్మాదం), తీవ్రమైన నిద్రలేమి, తలనొప్పి మరియు వణుకు.",
        "Effect_Hindi": "उन्माद (उन्माद), अत्यधिक अनिद्रा, सिरदर्द और कंपकंपी पैदा करता है।"
    },
    {
        "Herb": "Ginseng (జిన్సెంగ్ / जिन्सेंग)", "Herb_Keywords": ["ginseng"],
        "Drug": "Insulin / Sulfonylureas", "Drug_Keywords": ["insulin", "sulfonylureas", "diabetic", "sugar", "షుగర్"], "Severity": "Moderate",
        "Effect_English": "Enhanced hypoglycemic effects, leading to sweating and dizziness.",
        "Effect_Telugu": "రక్తంలో చక్కెర స్థాయిలు ఎక్కువగా తగ్గి నీరసం, మైకం వస్తాయి.",
        "Effect_Hindi": "रक्त शर्करा का स्तर बहुत कम हो सकता है, जिससे चक्कर आना संभव है।"
    },
    # --- GARLIC ---
    {
        "Herb": "Garlic - High Dose (వెల్లుల్లి అధిక మోతాదు / लहसुन उच्च खुराक)", "Herb_Keywords": ["garlic", "వెల్లుల్లి", "లహसुन"],
        "Drug": "Warfarin", "Drug_Keywords": ["warfarin"], "Severity": "Severe",
        "Effect_English": "Synergistic antiplatelet action increasing systemic hemorrhage risks.",
        "Effect_Telugu": "తీవ్రమైన రక్తస్రావం జరిగే ప్రమాదాన్ని గణనీయంగా పెంచుతుంది.",
        "Effect_Hindi": "गंभीर आंतरिक रक्तस्राव के खतरे को काफी बढ़ा देता है।"
    },
    {
        "Herb": "Garlic (వెల్లుల్లి / लहसुन)", "Herb_Keywords": ["garlic", "వెల్లుల్లి"],
        "Drug": "Saquinavir / Antiretrovirals", "Drug_Keywords": ["saquinavir", "antiretrovirals", "hiv"], "Severity": "Severe",
        "Effect_English": "Reductions of up to 50% in protease inhibitor levels, causing viral breakthrough.",
        "Effect_Telugu": "యాంటివైరల్ ఔషధాల స్థాయిలు 50% వరకు తగ్గి చికిత్స విఫలమవుతుంది.",
        "Effect_Hindi": "एंटीवायरल दवाओं का स्तर 50% तक कम हो जाता है, जिससे उपचार विफल हो जाता है।"
    },
    # --- EPHEDRA ---
    {
        "Herb": "Ephedra (ఎఫెడ్రా / इफेड्रा)", "Herb_Keywords": ["ephedra", "ఎఫెడ్రా"],
        "Drug": "Caffeine / Psychostimulants", "Drug_Keywords": ["caffeine", "psychostimulants", "coffee"], "Severity": "Severe",
        "Effect_English": "Tachycardia, severe hypertension, myocardial infarction, and stroke risks.",
        "Effect_Telugu": "గుండె వేగం పెరగడం, తీవ్రమైన రక్తపోటు, గుండెపోటు మరియు పక్షవాతం ప్రమాదం.",
        "Effect_Hindi": "तेज दिल की धड़कन, गंभीर उच्च रक्तचाप, दिल का दौरा और स्ट्रोक का खतरा।"
    },
    {
        "Herb": "Ephedra (ఎఫెడ్రా / इफेड्रा)", "Herb_Keywords": ["ephedra"],
        "Drug": "Volatile Anesthetics", "Drug_Keywords": ["anesthetics", "anesthesia", "volatile"], "Severity": "Severe",
        "Effect_English": "Fatal cardiac arrhythmias due to profound cardiac sensitization.",
        "Effect_Telugu": "గుండె లయ తప్పడం వలన ప్రాణాంతక పరిస్థితి ఏర్పడవచ్చు.",
        "Effect_Hindi": "दिल की धड़कन के अनियमित होने से जानलेवा स्थिति उत्पन्न हो सकती है।"
    },
    # --- KAVA KAVA ---
    {
        "Herb": "Kava Kava (కావా కావా / कावा कावा)", "Herb_Keywords": ["kava", "కావా"],
        "Drug": "Alprazolam / Benzodiazepines", "Drug_Keywords": ["alprazolam", "benzodiazepines", "xanax"], "Severity": "Severe",
        "Effect_English": "Additive CNS depression, profound lethargy, and semi-comatose states.",
        "Effect_Telugu": "తీవ్రమైన మగత, అలసట మరియు కోమా వంటి స్థితి కలగడం.",
        "Effect_Hindi": "अत्यधिक उनींदापन, सुस्ती और कोमा जैसी स्थिति उत्पन्न होना।"
    },
    # --- LICORICE ROOT ---
    {
        "Herb": "Licorice Root (అతిమధురం / मुलेठी)", "Herb_Keywords": ["licorice", "mulethi", "అతిమధురం"],
        "Drug": "Digoxin", "Drug_Keywords": ["digoxin", "heart medicine"], "Severity": "Severe",
        "Effect_English": "Pseudo-aldosteronism leading to hypokalemia, precipitating toxic digoxin arrhythmias.",
        "Effect_Telugu": "పొటాషియం స్థాయిలు తగ్గి డిగోక్సిన్ టాక్సిసిటీ మరియు గుండె లయ తప్పుతుంది.",
        "Effect_Hindi": "पोटेशियम का स्तर कम हो जाता है, जिससे डिगोक्सिन विषाक्तता और अतालता होती है।"
    },
    # --- MISTLETOE ---
    {
        "Herb": "Mistletoe (మిస్ల్‌టో / मिसलेटो)", "Herb_Keywords": ["mistletoe", "మిస్ల్‌టో"],
        "Drug": "Antidiabetic agents", "Drug_Keywords": ["diabetic", "metformin", "insulin", "sugar", "షుగర్"], "Severity": "Severe",
        "Effect_English": "Severe hypoglycemic shock, cardiotoxicity, and cardiovascular collapse.",
        "Effect_Telugu": "రక్తం లో చక్కెర స్థాయిలు ప్రమాదకరంగా తగ్గి షాక్ మరియు గుండె వైఫల్యం రావచ్చు.",
        "Effect_Hindi": "रक्त शर्करा का स्तर खतरनाक रूप से कम हो सकता है, जिससे शॉक और दिल का दौरा पड़ सकता है।"
    },
    # --- DONG QUAI ---
    {
        "Herb": "Dong Quai (డాంగ్ క్వై / डोंग क्वाई)", "Herb_Keywords": ["dong quai", "dong", "డాంగ్"],
        "Drug": "Warfarin", "Drug_Keywords": ["warfarin"], "Severity": "Severe",
        "Effect_English": "Profound additive anticoagulation, dramatically elevating INR and bleeding risks.",
        "Effect_Telugu": "రక్తస్రావం అయ్యే ప్రమాదం విపరీతంగా పెరుగుతుంది.",
        "Effect_Hindi": "रक्तस्राव का खतरा अत्यधिक बढ़ जाता है।"
    },
    # --- GOLDENSEAL ---
    {
        "Herb": "Goldenseal (గోల్డెన్‌సీల్ / गोल्डनसील)", "Herb_Keywords": ["goldenseal", "గోల్డెన్‌సీల్"],
        "Drug": "Metformin / Midazolam", "Drug_Keywords": ["metformin", "midazolam"], "Severity": "Severe",
        "Effect_English": "Inhibition of CYP2D6/3A4, causing drug toxicity or severe lactic acidosis.",
        "Effect_Telugu": "ఔషధాల టాక్సిసిటీ లేదా తీవ్రమైన లాక్టిక్ అసిడోసిస్ కలిగిస్తుంది.",
        "Effect_Hindi": "दवाओं की विषाक्तता या गंभीर लैक्टिक एसिडोसिस का कारण बनता है।"
    },
    # --- GRAPEFRUIT SEED EXTRACT ---
    {
        "Herb": "Grapefruit Seed Extract (గ్రేప్‌ఫ్రూట్ గింజల సారం / चकोतरा के बीज का अर्क)", "Herb_Keywords": ["grapefruit", "గ్రేప్‌ఫ్రూట్"],
        "Drug": "Simvastatin / Atorvastatin", "Drug_Keywords": ["simvastatin", "atorvastatin", "statin", "cholesterol"], "Severity": "Severe",
        "Effect_English": "Substantial CYP3A4 inhibition leading to toxicity and acute rhabdomyolysis.",
        "Effect_Telugu": "కండరాల తీవ్ర బలహీనత (రాబ్డోమయోలిసిస్) మరియు కిడ్నీ దెబ్బతినడం.",
        "Effect_Hindi": "मांसपेशियों की गंभीर कमजोरी (रैबडोमायोलिसिस) और गुर्दे की विफलता।"
    },
    # --- ALOE VERA ---
    {
        "Herb": "Aloe Vera - Latex (కలబంద (లాటెక్స్) / एलोवेरा (लेटेक्स))", "Herb_Keywords": ["aloe", "aloe vera", "కలబంద"],
        "Drug": "Diuretics (Furosemide)", "Drug_Keywords": ["furosemide", "diuretics", "lasix"], "Severity": "Moderate",
        "Effect_English": "Hypokalemia due to additive potassium wasting via laxative effect.",
        "Effect_Telugu": "శరీరంలో పొటాషియం స్థాయిలు తగ్గి నీరసం వస్తుంది.",
        "Effect_Hindi": "शरीर में पोटेशियम का स्तर कम हो जाता है, जिससे कमजोरी आती है।"
    },
    # --- GINGER ---
    {
        "Herb": "Ginger (అల్లం / अदरक)", "Herb_Keywords": ["ginger", "అల్లం"],
        "Drug": "Anticoagulants / NSAIDs", "Drug_Keywords": ["anticoagulants", "nsaids", "aspirin", "warfarin", "ibuprofen"], "Severity": "Moderate",
        "Effect_English": "Modest increase in bleeding tendency via weak thromboxane inhibition.",
        "Effect_Telugu": "రక్తస్రావం అయ్యే అవకాశం స్వల్పంగా పెరుగుతుంది.",
        "Effect_Hindi": "रक्तस्राव की संभावना थोड़ी बढ़ जाती है।"
    },
    # --- GREEN TEA ---
    {
        "Herb": "Green Tea (గ్రీన్ టీ / ग्रीन टी)", "Herb_Keywords": ["green tea", "tea", "గ్రీన్ టీ"],
        "Drug": "Simvastatin", "Drug_Keywords": ["simvastatin"], "Severity": "Moderate",
        "Effect_English": "Increased statin bioavailability and systemic exposure due to transporter inhibition.",
        "Effect_Telugu": "రక్తంలో స్టాటిన్ ఔషధాల మోతాదు పెరిగి దుష్ప్రభావాలు రావచ్చు.",
        "Effect_Hindi": "रक्त में स्टैटिन दवाओं की मात्रा बढ़ सकती है, जिससे दुष्प्रभाव हो सकते हैं।"
    },
    {
        "Herb": "Green Tea (గ్రీన్ టీ / ग्रीन टी)", "Herb_Keywords": ["green tea", "tea"],
        "Drug": "Warfarin", "Drug_Keywords": ["warfarin"], "Severity": "Moderate",
        "Effect_English": "Vitamin K content can directly antagonize warfarin therapy, lowering INR.",
        "Effect_Telugu": "విటమిన్ కె కారణంగా వార్ఫరిన్ ఔషధ ప్రభావం తగ్గుతుంది.",
        "Effect_Hindi": "विटामिन के के कारण वारफारिन दवा का असर कम हो जाता है।"
    },
    # --- ECHINACEA ---
    {
        "Herb": "Echinacea (ఎచినాసియా / एचिनासीया)", "Herb_Keywords": ["echinacea", "ఎచినాసియా"],
        "Drug": "Immunosuppressants", "Drug_Keywords": ["immunosuppressants", "steroids", "prednisone"], "Severity": "Moderate",
        "Effect_English": "Immunostimulatory properties directly counteract corticosteroid actions.",
        "Effect_Telugu": "రోగనిరోధక శక్తిని పెంచే గుణం వల్ల ఇమ్యునోసప్రెసెంట్ మందుల ప్రభావం తగ్గుతుంది.",
        "Effect_Hindi": "रोग प्रतिरोधक क्षमता बढ़ने के कारण इम्यूनोसप्रेसेन्ट दवाओं का असर कम हो जाता है।"
    },
    {
        "Herb": "Echinacea (ఎచినాసియా / एचिनासीया)", "Herb_Keywords": ["echinacea"],
        "Drug": "Caffeine", "Drug_Keywords": ["caffeine", "coffee"], "Severity": "Moderate",
        "Effect_English": "Inhibits CYP1A2, resulting in increased caffeine levels and jitteriness.",
        "Effect_Telugu": "శరీరంలో కెఫిన్ నిల్వలు పెరిగి గుండెల్లో కలవరం, వణుకు వస్తాయి.",
        "Effect_Hindi": "शरीर में कैफीन का स्तर बढ़ जाता है, जिससे घबराहट और कंपकंपी होती है।"
    },
    # --- MILK THISTLE ---
    {
        "Herb": "Milk Thistle (మిల్క్ తిస్టిల్ / मिया थिसल)", "Herb_Keywords": ["milk thistle", "మిల్క్ తిస్టిల్"],
        "Drug": "Losartan / Glipizide", "Drug_Keywords": ["losartan", "glipizide"], "Severity": "Moderate",
        "Effect_English": "Weak inhibition of CYP2C9, mildly elevating plasma levels of drugs.",
        "Effect_Telugu": "రక్తంలో మందుల స్థాయిలు స్వల్పంగా పెరుగుతాయి.",
        "Effect_Hindi": "रक्त में दवाओं का स्तर थोड़ा बढ़ सकता है।"
    },
    # --- SAW PALMETTO ---
    {
        "Herb": "Saw Palmetto (సా పాల్మెట్టో / सॉ पाल्मेटो)", "Herb_Keywords": ["saw palmetto", "సా పాల్మెట్టో"],
        "Drug": "Oral Contraceptives / Estrogens", "Drug_Keywords": ["contraceptives", "estrogens", "estrogen", "hormone"], "Severity": "Moderate",
        "Effect_English": "Anti-estrogenic effects potentially compromise low-dose hormonal therapies.",
        "Effect_Telugu": "హార్మోన్ల మందుల సామర్థ్యం తగ్గే అవకాశం ఉంది.",
        "Effect_Hindi": "हार्मोनल दवाओं की प्रभावशीलता कम होने की संभावना होती है।"
    },
    # --- BLACK COHOSH ---
    {
        "Herb": "Black Cohosh (బ్లాక్ కోహోష్ / ब्लैक कोहॉश)", "Herb_Keywords": ["black cohosh", "cohosh", "బ్లాక్ కోహోష్"],
        "Drug": "Cisplatin / Antineoplastics", "Drug_Keywords": ["cisplatin", "antineoplastics", "chemotherapy", "cancer"], "Severity": "Moderate",
        "Effect_English": "May attenuate or alter the therapeutic cytotoxic efficacy of chemotherapy.",
        "Effect_Telugu": "కీమోథెరపీ మందుల ప్రభావాన్ని మార్చవచ్చు లేదా తగ్గించవచ్చు.",
        "Effect_Hindi": "कीमोथेरेपी दवाओं के प्रभाव को कम या बदल सकता है।"
    },
    # --- FEVERFEW ---
    {
        "Herb": "Feverfew (ఫీవర్‌ఫ్యూ / फीवरफ्यू)", "Herb_Keywords": ["feverfew", "ఫీవర్‌ఫ్యూ"],
        "Drug": "Antiplatelet agents", "Drug_Keywords": ["antiplatelet", "clopidogrel", "aspirin"], "Severity": "Moderate",
        "Effect_English": "Inhibits platelet secretion, increasing risk of bruising or nosebleeds.",
        "Effect_Telugu": "చర్మంపై నల్లటి మచ్చలు లేదా ముక్కు నుండి రక్తస్రావం అయ్యే ప్రమాదం ఉంది.",
        "Effect_Hindi": "त्वचा पर नीले निशान या नाक से खून बहने का खतरा बढ़ जाता है।"
    },
    # --- VALERIAN ROOT ---
    {
        "Herb": "Valerian Root (వలేరియన్ రూట్ / जटामांसी (वलेरियन))", "Herb_Keywords": ["valerian", "వలేరియన్"],
        "Drug": "CNS Depressants", "Drug_Keywords": ["sedatives", "sleeping pills", "cns depressants", "xanax", "sleep"], "Severity": "Moderate",
        "Effect_English": "Synergistic GABA modulation causing extended drowsiness and impairment.",
        "Effect_Telugu": "తీవ్రమైన మగత మరియు మత్తు కలిగిస్తుంది.",
        "Effect_Hindi": "अत्यधिक उनींदापन और सुस्ती पैदा करता है।"
    },
    # --- CRANBERRY ---
    {
        "Herb": "Cranberry (క్రాన్‌బెర్రీ / क्रैनबेरी)", "Herb_Keywords": ["cranberry", "క్రాన్‌బెర్రీ"],
        "Drug": "Warfarin", "Drug_Keywords": ["warfarin"], "Severity": "Moderate",
        "Effect_English": "Altered drug metabolism leading to unpredictable fluctuations in INR.",
        "Effect_Telugu": "రక్తం గడ్డకట్టే ప్రక్రియలో అస్థిరత ఏర్పడుతుంది.",
        "Effect_Hindi": "रक्त के थक्के जमने की प्रक्रिया में अस्थिरता आ सकती है।"
    },
    # --- EVENING PRIMROSE OIL ---
    {
        "Herb": "Evening Primrose Oil (ఈవినింగ్ ప్రిమ్రోజ్ ఆయిల్ / इवनिंग प्रिमरोज़ तेल)", "Herb_Keywords": ["evening primrose", "primrose", "ఈవినింగ్"],
        "Drug": "Antiepileptics", "Drug_Keywords": ["antiepileptics", "seizure", "epilepsy", "fits"], "Severity": "Moderate",
        "Effect_English": "Lowers the seizure threshold, potentially triggering seizures.",
        "Effect_Telugu": "ఫిట్స్ (మూర్ఛ) వచ్చే ప్రమాదాన్ని పెంచుతుంది.",
        "Effect_Hindi": "दौरे (मिर्गी) आने का खतरा बढ़ जाता है।"
    },
    # --- HAWTHORN ---
    {
        "Herb": "Hawthorn (హాథార్న్ / हौथॉर्न)", "Herb_Keywords": ["hawthorn", "హాథార్న్"],
        "Drug": "Digoxin", "Drug_Keywords": ["digoxin"], "Severity": "Moderate",
        "Effect_English": "Synergistic positive inotropic effects; requires close monitoring.",
        "Effect_Telugu": "గుండెపై మందుల ప్రభావం పెరిగి లయ మారవచ్చు.",
        "Effect_Hindi": "दिल पर दवा का असर बढ़ जाता है, जिससे धड़कन बदल सकती है।"
    },
    # --- BLUE COHOSH ---
    {
        "Herb": "Blue Cohosh (బూ కోహోష్ / ब्लू कोहॉश)", "Herb_Keywords": ["blue cohosh", "బూ కోహోష్"],
        "Drug": "Antidiabetic Agents", "Drug_Keywords": ["diabetic", "sugar", "insulin"], "Severity": "Moderate",
        "Effect_English": "Causes coronary vasoconstriction and interferes with glucose control.",
        "Effect_Telugu": "రక్తనాళాల సంకోచం కలిగిస్తుంది మరియు చక్కెర నియంత్రణను దెబ్బతీస్తుంది.",
        "Effect_Hindi": "रक्त वाहिकाओं में संकुचन पैदा करता है और शर्करा नियंत्रण को प्रभावित करता है।"
    },
    # --- TURMERIC ---
    {
        "Herb": "Turmeric (పసుపు / हल्दी)", "Herb_Keywords": ["turmeric", "పసుపు", "హల్దీ"],
        "Drug": "Antidiabetic drugs", "Drug_Keywords": ["diabetic", "metformin", "sugar"], "Severity": "Moderate",
        "Effect_English": "Synergistic blood glucose lowering; requires closer monitoring.",
        "Effect_Telugu": "షుగర్ లెవెల్స్ మరింత తగ్గిపోయే ప్రమాదం ఉంది.",
        "Effect_Hindi": "शुगर का स्तर और अधिक कम होने का खतरा रहता है।"
    },
    {
        "Herb": "Turmeric (పసుపు / हल्दी)", "Herb_Keywords": ["turmeric", "పసుపు"],
        "Drug": "Anticoagulants", "Drug_Keywords": ["anticoagulants", "warfarin", "aspirin"], "Severity": "Moderate",
        "Effect_English": "Weak antiplatelet overlap that mildly raises systemic bleeding risk.",
        "Effect_Telugu": "రక్తస్రావం అయ్యే ముప్పు కొద్దిగా పెరుగుతుంది.",
        "Effect_Hindi": "रक्तस्राव का खतरा थोड़ा बढ़ जाता है।"
    },
    # --- CASSIA SENNA ---
    {
        "Herb": "Cassia Senna (సేనా ఆకు / सनाय)", "Herb_Keywords": ["cassia senna", "senna", "సేనా ఆకు"],
        "Drug": "Calcium Channel Blockers", "Drug_Keywords": ["calcium channel", "amlodipine", "diltiazem"], "Severity": "Moderate",
        "Effect_English": "Accelerated intestinal transit and electrolyte shifts alter drug absorption.",
        "Effect_Telugu": "విరేచనాలు మరియు లవణాల అసమతుల్యత వల్ల మందుల శోషణ మారుతుంది.",
        "Effect_Hindi": "दस्त और इलेक्ट्रोलाइट असंतुलन के कारण दवा का अवशोषण प्रभावित होता है।"
    },
    # --- PEPPERMINT OIL ---
    {
        "Herb": "Peppermint Oil (పుదీనా నూనె / पुदीना तेल)", "Herb_Keywords": ["peppermint", "పుదీనా"],
        "Drug": "Cyclosporine", "Drug_Keywords": ["cyclosporine"], "Severity": "Moderate",
        "Effect_English": "Competitively inhibits CYP3A4, raising immunosuppressant levels.",
        "Effect_Telugu": "శరీరంలో ఇమ్యునోసప్రెసెంట్ మందుల మోతాదు పెరుగుతుంది.",
        "Effect_Hindi": "शरीर में इम्यूनोसप्रेसेन्ट दवा की मात्रा बढ़ जाती है।"
    },
    # --- DANDELION ---
    {
        "Herb": "Dandelion (టాండెలైన్ / सिंहपर्णी (डैंडेलियन))", "Herb_Keywords": ["dandelion", "டாండెలైన్"],
        "Drug": "Ciprofloxacin", "Drug_Keywords": ["ciprofloxacin", "antibiotic"], "Severity": "Moderate",
        "Effect_English": "Concomitant intake reduces the total absorption of the antibiotic.",
        "Effect_Telugu": "యాంటిబయాటిక్ శోషణ తగ్గి దాని పనితీరు మందగిస్తుంది.",
        "Effect_Hindi": "एंटिबायोटिक का अवशोषण कम हो जाता है, जिससे उसका असर कम होता है।"
    },
    # --- FENUGREEK ---
    {
        "Herb": "Fenugreek (మెంతులు / मेथी)", "Herb_Keywords": ["fenugreek", "మెంతులు", "మేథి"],
        "Drug": "Glipizide", "Drug_Keywords": ["glipizide", "sugar", "diabetic"], "Severity": "Moderate",
        "Effect_English": "High mucilage content slows gastric emptying, altering drug response.",
        "Effect_Telugu": "జీర్ణక్రియ వేగం తగ్గి షుగర్ మందుల పనిరులో మార్పు వస్తుంది.",
        "Effect_Hindi": "पाचन धीमा हो जाता है, जिससे शुगर की दवा के असर में बदलाव आता है।"
    },
    # --- ALFALFA ---
    {
        "Herb": "Alfalfa (అల్ఫాల్ఫా / अल्फला)", "Herb_Keywords": ["alfalfa", "అల్ఫాల్ఫా"],
        "Drug": "Chlorpromazine", "Drug_Keywords": ["chlorpromazine"], "Severity": "Low",
        "Effect_English": "Slightly elevates drug-induced cutaneous photosensitivity.",
        "Effect_Telugu": "చర్మం సూర్యరశ్మికి సున్నితంగా మారి దద్దుర్లు రావచ్చు.",
        "Effect_Hindi": "त्वचा सूरज की रोशनी के प्रति संवेदनशील हो सकती है।"
    },
    {
        "Herb": "Alfalfa (అల్ఫాల్ఫా / अल्फला)", "Herb_Keywords": ["alfalfa"],
        "Drug": "Antilipaemic Agents", "Drug_Keywords": ["antilipaemic", "cholesterol"], "Severity": "Low",
        "Effect_English": "Minor reduction in cholesterol absorption; clinically insignificant.",
        "Effect_Telugu": "కొలెస్ట్రాల్ తగ్గుదలలో స్వల్ప మార్పు ఉంటుంది; పెద్దగా ప్రమాదం లేదు.",
        "Effect_Hindi": "कोलेस्ट्रॉल के अवशोषण में मामूली बदलाव; कोई गंभीर खतरा नहीं।"
    },
    # --- CHAMOMILE ---
    {
        "Herb": "Chamomile (చామంతి / बबूना के फूल (कैमोमाइल))", "Herb_Keywords": ["chamomile", "చామంతి"],
        "Drug": "Sedatives", "Drug_Keywords": ["sedatives", "sleep", "sleeping"], "Severity": "Low",
        "Effect_English": "Minor additive central nervous system relaxation and drowsiness.",
        "Effect_Telugu": "స్వల్పంగా నిద్రమత్తు మరియు ఉపశమనం కలుగుతుంది.",
        "Effect_Hindi": "हल्का उनींदापन और आराम महसूस हो सकता है।"
    },
    # --- CINNAMON ---
    {
        "Herb": "Cinnamon (దాల్చినచెక్క / दालचीनी)", "Herb_Keywords": ["cinnamon", "దాల్చినచెక్క"],
        "Drug": "Hypoglycemics", "Drug_Keywords": ["hypoglycemics", "sugar", "insulin"], "Severity": "Low",
        "Effect_English": "Mild additive support to blood glucose reduction.",
        "Effect_Telugu": "రక్తంలో చక్కెర నియంత్రణకు స్వల్పంగా తోడ్పడుతుంది.",
        "Effect_Hindi": "रक्त शर्करा नियंत्रण में मामूली सहायता मिलती है।"
    },
    # --- CALENDULA ---
    {
        "Herb": "Calendula (బంతి పువ్వు / गेंदा (कैलैंडुला))", "Herb_Keywords": ["calendula", "బంతి పువ్వు"],
        "Drug": "Sedatives", "Drug_Keywords": ["sedatives", "sleep"], "Severity": "Low",
        "Effect_English": "Minor additive central nervous system relaxation.",
        "Effect_Telugu": "స్వల్పంగా శరీరం మరియు మైండ్ రిలాక్స్ అవుతాయి.",
        "Effect_Hindi": "शरीर और मन को थोड़ी शांति या आराम मिलता है।"
    },
    # --- BOSWELLIA SERRATA ---
    {
        "Herb": "Boswellia Serrata (శల్లాకి (సాంబ్రాణి కొమ్మ) / शल्लकी (सलाई गुग्गल))", "Herb_Keywords": ["boswellia", "శల్లాకి", "సాంబ్రాణి"],
        "Drug": "NSAIDs", "Drug_Keywords": ["nsaids", "ibuprofen", "pain killer"], "Severity": "Low",
        "Effect_English": "Mild anti-inflammatory overlap; minor gastric concern.",
        "Effect_Telugu": "స్వల్పంగా కడుపులో మంట లేదా గ్యాస్ రావచ్చు.",
        "Effect_Hindi": "पेट में हल्की जलन या गैस की समस्या हो सकती है।"
    },
    # --- BLESSED THISTLE ---
    {
        "Herb": "Blessed Thistle (బ్లెస్డ్ తిస్టిల్ / ब्लेस्ड थिसल)", "Herb_Keywords": ["blessed thistle", "thistle"],
        "Drug": "Antacids / H2 Blockers", "Drug_Keywords": ["antacids", "pantoprazole", "ranitidine", "h2 blockers"], "Severity": "Low",
        "Effect_English": "Bitter compounds may minimally stimulate gastric acid secretion.",
        "Effect_Telugu": "కడుపులో యాసిడ్ ఉత్పత్తిని స్వల్పంగా పెంచి యాంటాసిడ్ ప్రభావాన్ని తగ్గిస్తుంది.",
        "Effect_Hindi": "पेट में एसिड उत्पादन को थोड़ा बढ़ाकर एंटासिड के असर को कम कर सकता है।"
    },
    # --- GUGGUL ---
    {
        "Herb": "Guggul (గుగ్గులు / गुग्गल)", "Herb_Keywords": ["guggul", "గుగ్గులు"],
        "Drug": "Diltiazem", "Drug_Keywords": ["diltiazem", "bp"], "Severity": "Low",
        "Effect_English": "Minor reductions in the peak plasma concentrations of diltiazem.",
        "Effect_Telugu": "రక్తంలో దిల్తియాజెం మందుల మోతాదు స్వల్పంగా తగ్గుతుంది.",
        "Effect_Hindi": "रक्त में डिल्टियाज़ेम दवा की मात्रा थोड़ी कम हो सकती है।"
    },
    # --- SAFFRON ---
    {
        "Herb": "Saffron (కుంకుమపువ్వు / केसर)", "Herb_Keywords": ["saffron", "కుంకుమపువ్వు"],
        "Drug": "Antihypertensives", "Drug_Keywords": ["antihypertensives", "bp", "blood pressure"], "Severity": "Low",
        "Effect_English": "Marginally enhances smooth muscle relaxation, very slight blood pressure drop.",
        "Effect_Telugu": "రక్తపోటులో చాలా స్వల్పమైన తగ్గుదల ఉండవచ్చు.",
        "Effect_Hindi": "रक्तचाप में बहुत मामूली कमी आ सकती है।"
    }
]

df = pd.DataFrame(data)

# 3. Sidebar Configuration
st.sidebar.title("Navigation & Settings")

lang_choice = st.sidebar.radio(
    "Select Interface/Agent Language",
    options=["English", "తెలుగు (Telugu)", "हिंदी (Hindi)"],
    index=0
)
selected_effect_col = {"English": "Effect_English", "తెలుగు (Telugu)": "Effect_Telugu", "हिंदी (Hindi)": "Effect_Hindi"}[lang_choice]

# 4. Main Banner
st.markdown("<h1 style='color: #1B5E20; margin-bottom: 0px;'>🌿 Clinical Herb-Drug Interaction Portal</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #666; font-size:16px;'>Standardized Clinical Decision Support System with Comprehensive 50-Mapping Directory.</p>", unsafe_allow_html=True)
st.write("---")

# 5. Dashboard Summary Widgets
st.markdown(f"<div class='metric-box'><strong>Total Registry Records</strong><br><span style='font-size:24px; font-weight:bold; color:#1B5E20;'>{len(df)} Cases Loaded</span></div>", unsafe_allow_html=True)

# 6. Professional TABS System
tab1, tab2 = st.tabs(["📋 Registry Search Engine", "🤖 Ask Clinical AI Voice Assistant"])

# --- TAB 1: SEARCH ENGINE (Fixed to remain clean when empty) ---
with tab1:
    search_query = st.text_input("🔎 Search Query Engine", placeholder="Type Herb or Drug names (e.g., Ephedra, Mistletoe, Contraceptives, Metformin)...", key="search_bar").strip().lower()
    
    # FIX: Only filter and show matches if the user has actually typed something
    if search_query:
        filtered_df = df[df['Herb'].str.lower().str.contains(search_query) | df['Drug'].str.lower().str.contains(search_query)]
        st.markdown(f"##### Directory Results: Found {len(filtered_df)} matches")
        
        if not filtered_df.empty:
            for idx, row in filtered_df.iterrows():
                sev_type = row['Severity'].strip().lower()
                badge_html = f"<span class='severity-severe'>⚠️ Severe Contraindication</span>" if sev_type == 'severe' else (f"<span class='severity-moderate'>⚡ Moderate Monitor Required</span>" if sev_type == 'moderate' else f"<span class='severity-low'>✅ Low Interaction Risk</span>")
                
                st.markdown(f"""
                    <div class="interaction-card">
                        <table style="width:100%; border:none;">
                            <tr style="border:none;">
                                <td style="width:75%; border:none; padding:0;"><h3 style="color:#2C3E50; margin:0 0 8px 0;">{row['Herb']}</h3>
                                <p style="margin:0; font-size:15px; color:#555;"><strong>Target Prescription Agent:</strong> <code style="color:#2C3E50; background-color:#F0F4C3; padding:2px 6px; border-radius:4px;">{row['Drug']}</code></p></td>
                                <td style="width:25%; text-align:right; border:none; padding:0;">{badge_html}</td>
                            </tr>
                        </table>
                        <hr style="border:0; border-top:1px solid #eee; margin:15px 0 10px 0;">
                        <p style="margin:0; font-size:15px; color:#4A5568;"><strong>Clinical Evaluation Mechanism ({lang_choice}):</strong><br>{row[selected_effect_col]}</p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No matching interactions found in the database.")
    else:
        # Shown when the query bar is empty
        st.info("💡 Clinical directory is ready. Please type a drug or herb name above to look up interactions.")
# --- TAB 2: INTERACTIVE AI VOICE & TEXT AGENT (Enhanced with Typing Feature) ---
with tab2:
    st.markdown("### 🤖 Voice & Text Activated Medical Search Component")
    st.markdown("మీరు **'Start Listening'** బటన్ నొక్కి మాట్లాడవచ్చు లేదా కింద ఉన్న **Type Query** బాక్స్‌లో నేరుగా టైప్ చేసి కూడా వెతకవచ్చు.")

    # Pass the complete massive database as JSON directly to JavaScript
    json_data_str = json.dumps(data)

    # Revised JavaScript Voice & Text Assistant Module
    voice_agent_html = f"""
    <div style="background-color: #ffffff; padding: 25px; border-radius: 12px; border: 1px solid #e0e0e0; box-shadow: 0 4px 6px rgba(0,0,0,0.03); max-width: 100%;">
        
        <!-- ROW 1: Voice Button -->
        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 15px;">
            <button id="micBtn" onclick="startSpeech()" style="background-color: #2E7D32; color: white; border: none; padding: 12px 24px; font-size: 16px; font-weight: bold; border-radius: 30px; cursor: pointer; display: flex; align-items: center; gap: 8px; transition: 0.3s;">
                🎤 Start Listening
            </button>
            <span id="statusText" style="font-size: 14px; color: #666; font-weight: 500;">Status: Ready for voice check</span>
        </div>
        
        <!-- ROW 2: Manual Typing Input (Added Feature) -->
        <div style="margin-bottom: 20px;">
            <label style="font-weight: bold; color: #2C3E50; display: block; margin-bottom: 5px;">⌨️ Or Type Query Professionally:</label>
            <input type="text" id="manualTextInput" oninput="handleTyping(this.value)" placeholder="Type here (e.g., Mistletoe, Cyclosporine, Sugar)..." style="width: 100%; padding: 12px; border-radius: 6px; border: 1px solid #ccc; font-size: 15px; box-sizing: border-box;">
        </div>
        
        <!-- ROW 3: Captured Live Text (Syncs with both Voice & Type) -->
        <div style="margin-bottom: 20px;">
            <strong style="color: #2C3E50;">Current Active Query:</strong>
            <p id="transcriptText" style="background-color: #f8f9fa; padding: 12px; border-radius: 6px; border: 1px solid #eee; min-height: 24px; margin-top: 5px; color: #333; font-style: italic;">(Waiting for voice input or typing... No initial data leaked)</p>
        </div>

        <!-- ROW 4: Results Display -->
        <div>
            <strong style="color: #2C3E50;">Live Analysis Results:</strong>
            <div id="aiResponseBox" style="margin-top: 10px;">
                <div style="background-color: #E8F5E9; padding: 15px; border-radius: 8px; color: #2E7D32; border-left: 4px solid #2E7D32;">
                    🗣️ Assistant is ready. Speak or type a query word to load matches instantly.
                </div>
            </div>
        </div>
    </div>

    <script>
    const medicalDatabase = {json_data_str};
    const currentLang = "{lang_choice}";

    // Handle Voice Input
    function startSpeech() {{
        const micBtn = document.getElementById('micBtn');
        const statusText = document.getElementById('statusText');
        const transcriptText = document.getElementById('transcriptText');
        const manualInput = document.getElementById('manualTextInput');

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) {{
            alert("Your browser does not support Speech Recognition. Please use Google Chrome or Edge.");
            return;
        }}

        const recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US'; 

        recognition.onstart = function() {{
            micBtn.style.backgroundColor = "#C62828";
            micBtn.innerHTML = "🔴 Listening...";
            statusText.innerHTML = "Status: Actively capturing speech frequencies...";
            transcriptText.innerHTML = "Processing audio stream...";
            manualInput.value = ""; // Clear manual input when voice starts
        }};

        recognition.onresult = function(event) {{
            const speechToText = event.results[0][0].transcript;
            transcriptText.innerHTML = '🎤 Voice Captured: "' + speechToText + '"';
            analyzeInteraction(speechToText.toLowerCase());
        }};

        recognition.onerror = function(event) {{
            statusText.innerHTML = "Status: Microphone or transmission error.";
            resetMicButton();
        }};

        recognition.onend = function() {{
            resetMicButton();
        }};

        recognition.start();
    }}

    function resetMicButton() {{
        const micBtn = document.getElementById('micBtn');
        const statusText = document.getElementById('statusText');
        micBtn.style.backgroundColor = "#2E7D32";
        micBtn.innerHTML = "🎤 Start Listening";
        statusText.innerHTML = "Status: Standby mode.";
    }}

    // Handle Manual Typing Input (New Function)
    function handleTyping(val) {{
        const transcriptText = document.getElementById('transcriptText');
        if(val.trim() === "") {{
            transcriptText.innerHTML = "(Waiting for voice input or typing... No initial data leaked)";
            document.getElementById('aiResponseBox').innerHTML = `
                <div style="background-color: #E8F5E9; padding: 15px; border-radius: 8px; color: #2E7D32; border-left: 4px solid #2E7D32;">
                    🗣️ Assistant is ready. Speak or type a query word to load matches instantly.
                </div>
            `;
            return;
        }}
        transcriptText.innerHTML = '⌨️ Text Typed: "' + val + '"';
        analyzeInteraction(val.toLowerCase());
    }}

    // Master Clinical Filter Analysis Architecture
    function analyzeInteraction(query) {{
        const aiResponseBox = document.getElementById('aiResponseBox');
        let matches = [];

        for (let item of medicalDatabase) {{
            let herbMatch = item.Herb_Keywords.some(kw => query.includes(kw));
            let drugMatch = item.Drug_Keywords.some(kw => query.includes(kw));
            if (herbMatch || drugMatch) {{
                matches.push(item);
            }}
        }}

        if (matches.length === 0) {{
            let noMatchMsg = "No clinical matching cases found. Try keywords like Cyclosporine, Mistletoe, Goldenseal, or Saffron.";
            if (currentLang.includes("Telugu")) noMatchMsg = "క్షమించండి, మీ వాయిస్/టెక్స్ట్ కీవర్డ్స్ కు తగిన క్లినికల్ మ్యాపింగ్ లభించలేదు.";
            if (currentLang.includes("Hindi")) noMatchMsg = "क्षमा करें, हमारे डेटाबेस में कोई विवरण नहीं मिला।";
            
            aiResponseBox.innerHTML = `<div style="background-color: #FFF3E0; padding: 15px; border-radius: 8px; border-left: 4px solid #FF9800; color:#E65100;">${{noMatchMsg}}</div>`;
            return;
        }}

        let htmlContent = "";
        for (let res of matches) {{
            let badgeColor = res.Severity === "Severe" ? "#FFEBEE" : (res.Severity === "Moderate" ? "#FFFDE7" : "#E8F5E9");
            let textColor = res.Severity === "Severe" ? "#C62828" : (res.Severity === "Moderate" ? "#F57F17" : "#2E7D32");
            let textEffect = currentLang.includes("Telugu") ? res.Effect_Telugu : (currentLang.includes("Hindi") ? res.Effect_Hindi : res.Effect_English);

            htmlContent += `
                <div style="background-color: #fff; padding: 15px; border-radius: 8px; border: 1px solid #e0e0e0; margin-bottom: 12px; border-left: 5px solid ${{textColor}}; font-family: sans-serif;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <strong style="font-size: 16px; color: #2C3E50;">${{res.Herb}}</strong>
                        <span style="background-color: ${{badgeColor}}; color: ${{textColor}}; padding: 4px 10px; border-radius: 12px; font-weight: bold; font-size: 12px;">${{res.Severity}}</span>
                    </div>
                    <p style="margin: 4px 0; font-size: 14px; color: #555;"><strong>Target Prescription Agent:</strong> <code style="background-color:#eee; padding:2px 5px; border-radius:4px;">${{res.Drug}}</code></p>
                    <p style="margin: 8px 0 0 0; font-size: 14px; color: #333; background-color: #fcfdfd; padding: 8px; border-radius: 4px; border: 1px dashed #ccc;"><strong>Mechanism Profile:</strong> ${{textEffect}}</p>
                </div>
            `;
        }}
        aiResponseBox.innerHTML = htmlContent;
    }}
    </script>
    """
    st.components.v1.html(voice_agent_html, height=620, scrolling=True)

# 7. Footer Disclaimer
st.markdown("<br><br><hr>", unsafe_allow_html=True)
st.caption("⚠️ **Clinical Regulatory Disclaimer:** This portal operates strictly as an interactive informatics proof-of-concept. All data must be manually verified through authoritative medical literature databases before clinically applying insights.")