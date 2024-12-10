from country import fetch_country_data

def test_fetch_country_language():
    print("Testing fetch_country_language...")
    data = fetch_country_data("France")
    if "error" in data:
        print(f"Error: {data['error']}")
    else:
        languages = list(data.get('languages', {}).values())
        print(f"Languages in France: {languages}")

def test_fetch_country_currency():
    print("Testing fetch_country_currency...")
    data = fetch_country_data("France")
    if "error" in data:
        print(f"Error: {data['error']}")
    else:
        currencies = list(data.get('currencies', {}).keys())
        print(f"Currencies in France: {currencies}")

def test_fetch_country_population():
    print("Testing fetch_country_population...")
    data = fetch_country_data("France")
    if "error" in data:
        print(f"Error: {data['error']}")
    else:
        population = data.get('population', 'N/A')
        print(f"Population in France: {population}")

if __name__ == "__main__":
    test_fetch_country_language()
    test_fetch_country_currency()
    test_fetch_country_population()
