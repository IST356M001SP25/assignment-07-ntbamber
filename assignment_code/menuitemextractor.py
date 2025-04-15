if __name__ == "__main__":
    import sys
    sys.path.append('code')
    from menuitem import MenuItem
else:
    from menuitem import MenuItem


def clean_price(price:str) -> float:
    return float(price.replace("$", "").replace(",", "").strip())

def clean_scraped_text(scraped_text: str) -> list[str]:
    unwanted = {"NEW", "NEW!", "GS", "V", "P", "S"}
    lines = [line.strip() for line in scraped_text.splitlines()]
    return [line for line in lines if line and line not in unwanted]

def extract_menu_item(title:str, scraped_text: str) -> MenuItem:
    cleaned = clean_scraped_text(scraped_text)
    name = cleaned[0]
    price = clean_price(cleaned[1])
    description = cleaned[2] if len(cleaned) > 2 else "No description available"
    return MenuItem(category=title, name=name, price=price, description=description)



if __name__=='__main__':
    pass
