def calculate_advanced_risk(country, abuse_score, is_private):
    score = 0

    high_risk_countries = ["Russia", "China", "Iran", "North Korea"]

    if is_private:
        return 0

    if country in high_risk_countries:
        score += 40

    score += abuse_score // 2

    if score > 100:
        score = 100

    return score
