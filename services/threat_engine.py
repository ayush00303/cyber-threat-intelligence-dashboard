import requests

def abuse_check(ip):
    try:
        url = f"https://api.abuseipdb.com/api/v2/check"
        headers = {
            "Key": "YOUR_API_KEY",
            "Accept": "application/json"
        }
        params = {"ipAddress": ip, "maxAgeInDays": 90}

        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        return data.get("data", {}).get("abuseConfidenceScore", 0)

    except:
        return 0
