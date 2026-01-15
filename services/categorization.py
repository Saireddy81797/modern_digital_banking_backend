CATEGORY_RULES = {
    "food": ["zomato", "swiggy", "restaurant"],
    "travel": ["uber", "ola", "train"],
    "shopping": ["amazon", "flipkart"]
}

def auto_categorize(description: str):
    desc = description.lower()
    for category, keywords in CATEGORY_RULES.items():
        for k in keywords:
            if k in desc:
                return category
    return "others"
