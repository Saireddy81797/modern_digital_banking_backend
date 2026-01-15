CATEGORY_RULES = {
    "food": ["zomato", "swiggy", "restaurant", "cafe"],
    "travel": ["uber", "ola", "bus", "train", "flight"],
    "shopping": ["amazon", "flipkart", "mall"],
    "utilities": ["electricity", "water", "gas", "recharge"]
}

def auto_categorize(description: str):
    desc = description.lower()
    for category, keywords in CATEGORY_RULES.items():
        for word in keywords:
            if word in desc:
                return category
    return "others"
