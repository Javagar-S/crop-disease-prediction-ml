# models/disease_info.py

# Verified Agricultural Data for South India
plant_disease_info = {

    # ================= PEPPER (CHILLI/CAPSICUM) =================
    "Pepper__bell___Bacterial_spot": {
        "name": "Pepper Bacterial Spot",
        "scientific_name": "Xanthomonas campestris",
        "severity": "Critical",
        "description": "Bacterial infection common in humid South Indian weather. Causes leaf drop and fruit rot.",
        "symptoms": [
            "Small water-soaked spots on leaves",
            "Yellow halo around dark spots",
            "Raised scabs on green fruits"
        ],
        "treatment_plan": [
            {
                "action": "Spray Copper Oxychloride (Blitox)",
                "frequency": "Every 10 days",
                "duration": "2-3 rounds",
                "type": "Chemical"
            },
            {
                "action": "Add Streptocycline (Antibiotic)",
                "frequency": "Mix with Copper spray",
                "duration": "0.5g per 10L water",
                "type": "Chemical"
            }
        ],
        "prevention": [
            "Treat seeds with hot water (50°C) before sowing.",
            "Avoid overhead sprinklers (use drip)."
        ]
    },

    "Pepper__bell___healthy": {
        "name": "Healthy Bell Pepper",
        "scientific_name": "Capsicum annuum",
        "severity": "Healthy",
        "description": "Plant is vigorous with deep green foliage.",
        "symptoms": [],
        "treatment_plan": [
            {
                "action": "Drench with 19:19:19 NPK",
                "frequency": "Every 15 days",
                "duration": "Vegetative stage",
                "type": "Care"
            }
        ],
        "prevention": ["Install yellow sticky traps (10/acre) for pests."]
    },

    # ================= POTATO =================
    "Potato___Early_blight": {
        "name": "Potato Early Blight",
        "scientific_name": "Alternaria solani",
        "severity": "Warning",
        "description": "Fungal disease appearing as 'target-board' rings. Reduces tuber size significantly.",
        "symptoms": [
            "Brown spots with concentric rings",
            "Lower leaves turn yellow and dry",
            "Black lesions on stems"
        ],
        "treatment_plan": [
            {
                "action": "Spray Mancozeb (Indofil M-45) @ 2.5g/L",
                "frequency": "Every 10 days",
                "duration": "Until spots dry",
                "type": "Chemical"
            },
            {
                "action": "Spray Propineb (Antracol) @ 2g/L",
                "frequency": "Alternate with Mancozeb",
                "duration": "If severity increases",
                "type": "Chemical"
            }
        ],
        "prevention": [
            "Use certified disease-free tubers.",
            "Maintain correct Nitrogen levels (don't over-fertilize)."
        ]
    },

    "Potato___Late_blight": {
        "name": "Potato Late Blight",
        "scientific_name": "Phytophthora infestans",
        "severity": "Critical",
        "description": "Devastating water-mold disease. Can destroy the entire crop in 3-4 days of cloudy weather.",
        "symptoms": [
            "Water-soaked black patches on leaves",
            "White cottony growth on leaf undersides",
            "Rotting, smelly tubers"
        ],
        "treatment_plan": [
            {
                "action": "Spray Metalaxyl + Mancozeb (Ridomil Gold) @ 2g/L",
                "frequency": "Immediately",
                "duration": "Repeat after 7 days",
                "type": "Chemical"
            },
            {
                "action": "Spray Cymoxanil (Curzate) @ 3g/L",
                "frequency": "If raining persists",
                "duration": "Curative action",
                "type": "Chemical"
            }
        ],
        "prevention": [
            "Earthing up soil around base to protect tubers.",
            "Destroy infected haulms (stems) far from field."
        ]
    },

    "Potato___healthy": {
        "name": "Healthy Potato Plant",
        "scientific_name": "Solanum tuberosum",
        "severity": "Healthy",
        "description": "Foliage is intact and photosynthesis is optimal.",
        "symptoms": [],
        "treatment_plan": [
            {
                "action": "Micronutrient Spray",
                "frequency": "Day 45 and 60",
                "duration": "One time",
                "type": "Care"
            }
        ],
        "prevention": ["Monitor for aphids (virus vectors)."]
    },

    # ================= TOMATO =================
    "Tomato_Bacterial_spot": {
        "name": "Tomato Bacterial Spot",
        "scientific_name": "Xanthomonas campestris",
        "severity": "Warning",
        "description": "Causes spotting on leaves and scabs on fruits, reducing market value.",
        "symptoms": [
            "Small dark spots with yellow halos",
            "Leaf margins turn brown",
            "Rough, raised spots on green fruits"
        ],
        "treatment_plan": [
            {
                "action": "Spray Copper Hydroxide (Kocide) @ 2g/L",
                "frequency": "Every 10 days",
                "duration": "2 rounds",
                "type": "Chemical"
            }
        ],
        "prevention": [
            "Crop rotation with non-solanaceous crops (Maize/Beans).",
            "Remove weeds from field bunds."
        ]
    },

    "Tomato_Early_blight": {
        "name": "Tomato Early Blight",
        "scientific_name": "Alternaria solani",
        "severity": "Warning",
        "description": "Very common in India. Starts from older bottom leaves and moves up.",
        "symptoms": [
            "Target-like brown rings on leaves",
            "Leaves yellow and drop off",
            "Sunken rot at fruit stem end"
        ],
        "treatment_plan": [
            {
                "action": "Spray Chlorothalonil (Kavach) @ 2g/L",
                "frequency": "Every 7-10 days",
                "duration": "Preventative",
                "type": "Chemical"
            },
            {
                "action": "Spray Hexaconazole (Contaf) @ 1ml/L",
                "frequency": "If infection is severe",
                "duration": "Curative",
                "type": "Chemical"
            }
        ],
        "prevention": [
            "Stake plants to keep leaves off the soil.",
            "Mulch with straw/plastic."
        ]
    },

    "Tomato_Late_blight": {
        "name": "Tomato Late Blight",
        "scientific_name": "Phytophthora infestans",
        "severity": "Critical",
        "description": "Rapid killer during monsoon/winter rains. Leaves look burnt or frost-bitten.",
        "symptoms": [
            "Large, greasy gray-green spots",
            "White fungal fuzz in high humidity",
            "Brown hard rot on fruits"
        ],
        "treatment_plan": [
            {
                "action": "Spray Dimethomorph (Acrobat) @ 1g/L",
                "frequency": "Immediately",
                "duration": "Curative",
                "type": "Chemical"
            },
            {
                "action": "Spray Mancozeb (M-45) @ 2.5g/L",
                "frequency": "Every 5 days",
                "duration": "Preventative",
                "type": "Chemical"
            }
        ],
        "prevention": [
            "Ensure wide spacing (2-3 ft) for airflow.",
            "Avoid irrigation in the evening."
        ]
    },

    "Tomato_Leaf_Mold": {
        "name": "Tomato Leaf Mold",
        "scientific_name": "Passalora fulva",
        "severity": "Warning",
        "description": "Occurs in polyhouses or highly humid open fields.",
        "symptoms": [
            "Pale yellow spots on upper leaf",
            "Olive-green velvet mold on underside",
            "Leaves wither but hang on plant"
        ],
        "treatment_plan": [
            {
                "action": "Spray Carbendazim (Bavistin) @ 1g/L",
                "frequency": "Every 15 days",
                "duration": "2 rounds",
                "type": "Chemical"
            }
        ],
        "prevention": [
            "Prune lower branches to improve ventilation.",
            "Control humidity levels."
        ]
    },

    "Tomato_Septoria_leaf_spot": {
        "name": "Tomato Septoria Leaf Spot",
        "scientific_name": "Septoria lycopersici",
        "severity": "Warning",
        "description": "Destructive foliage disease causing massive leaf loss.",
        "symptoms": [
            "Numerous small circular spots",
            "Gray center with dark border",
            "Tiny black specks in center of spots"
        ],
        "treatment_plan": [
            {
                "action": "Spray Mancozeb @ 2.5g/L",
                "frequency": "Every 7-10 days",
                "duration": "Until control",
                "type": "Chemical"
            },
            {
                "action": "Remove infected lower leaves",
                "frequency": "Immediately",
                "duration": "Physical removal",
                "type": "Physical"
            }
        ],
        "prevention": [
            "Burn infected crop debris (do not compost).",
            "Follow 3-year crop rotation."
        ]
    },

    "Tomato_Spider_mites_Two_spotted_spider_mite": {
        "name": "Two Spotted Spider Mite",
        "scientific_name": "Tetranychus urticae",
        "severity": "Warning",
        "description": "Major pest in hot, dry summers. Sucks sap and stunts growth.",
        "symptoms": [
            "Yellow speckles (stippling) on leaves",
            "Webbing between leaves",
            "Leaves turn bronze and dry up"
        ],
        "treatment_plan": [
            {
                "action": "Spray Spiromesifen (Oberon) @ 0.5ml/L",
                "frequency": "Once",
                "duration": "Effective for 2 weeks",
                "type": "Chemical"
            },
            {
                "action": "Water Spray (Jet)",
                "frequency": "Daily",
                "duration": "To wash off mites",
                "type": "Physical"
            }
        ],
        "prevention": [
            "Maintain soil moisture (mites hate humidity).",
            "Remove weeds like Parthenium."
        ]
    },

    "Tomato__Target_Spot": {
        "name": "Tomato Target Spot",
        "scientific_name": "Corynespora cassiicola",
        "severity": "Warning",
        "description": "Often confused with Early Blight, but attacks fruits more aggressively.",
        "symptoms": [
            "Brown lesions with light center",
            "Circular sunken spots on fruit",
            "Leaf drop"
        ],
        "treatment_plan": [
            {
                "action": "Spray Azoxystrobin (Amistar) @ 0.5ml/L",
                "frequency": "Every 15 days",
                "duration": "Systemic action",
                "type": "Chemical"
            }
        ],
        "prevention": [
            "Avoid nitrogen excess.",
            "Remove old plant debris."
        ]
    },

    "Tomato__Tomato_YellowLeaf__Curl_Virus": {
        "name": "Tomato Yellow Leaf Curl (TYLCV)",
        "scientific_name": "Begomovirus",
        "severity": "Critical",
        "description": "Most dangerous virus in South India . Spread by Whiteflies. Stops fruit set.",
        "symptoms": [
            "Leaves curl upward like a cup",
            "Margins turn yellow",
            "Plant becomes bushy and stunted"
        ],
        "treatment_plan": [
            {
                "action": "Control Vector (Whitefly)",
                "frequency": "Critical",
                "duration": "Use Imidacloprid (Confidor)",
                "type": "Chemical"
            },
            {
                "action": "Pull out infected plants",
                "frequency": "Immediately",
                "duration": "Bury deep in soil",
                "type": "Physical"
            }
        ],
        "prevention": [
            "Install yellow sticky traps (15/acre).",
            "Grow border crops like Maize/Jowar."
        ]
    },

    "Tomato__Tomato_mosaic_virus": {
        "name": "Tomato Mosaic Virus (ToMV)",
        "scientific_name": "Tobamovirus",
        "severity": "Critical",
        "description": "Highly contagious mechanical virus. Spread by smokers or tools.",
        "symptoms": [
            "Light and dark green mosaic pattern",
            "Fern-like leaf distortion",
            "Internal browning of fruits"
        ],
        "treatment_plan": [
            {
                "action": "Spray milk (1L / 10L water)",
                "frequency": "Weekly",
                "duration": "Reduces viral spread",
                "type": "Organic"
            },
            {
                "action": "No Chemical Cure",
                "frequency": "N/A",
                "duration": "Remove plant",
                "type": "Info"
            }
        ],
        "prevention": [
            "Wash hands with soap before entering field.",
            "Disinfect tools with bleach."
        ]
    },

    "Tomato_healthy": {
        "name": "Healthy Tomato Plant",
        "scientific_name": "Solanum lycopersicum",
        "severity": "Healthy",
        "description": "Plant is growing vigorously with flowers/fruits setting.",
        "symptoms": [],
        "treatment_plan": [
            {
                "action": "Apply Calcium Nitrate",
                "frequency": "During fruiting",
                "duration": "Prevents blossom end rot",
                "type": "Care"
            }
        ],
        "prevention": ["Regular de-suckering (pruning side shoots)."]
    },
    
    # Fallback for errors
    "Background_Noise": {
        "name": "Unknown / Not a Leaf",
        "severity": "Invalid",
        "description": "Please upload a clear image of a crop leaf.",
        "symptoms": [],
        "treatment_plan": [],
        "prevention": []
    }
}