import requests


def delete_logo(company_name: str):
    """
    Delete Logo
    """
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    url = "https://api.peviitor.ro/v1/logo/delete/"
    data = {"company": company_name}

    response = requests.post(url, headers=headers, data=data)

    return response


if __name__ == "__main__":
    company_name = input('Srie numele companiei: ')
    response = delete_logo(company_name)

    if response.status_code == 200:
        print("Logo sters cu succes")
    else:
        print("Eroare la stergerea logo-ului")
