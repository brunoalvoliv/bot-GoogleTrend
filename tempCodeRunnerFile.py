def check_trends():
    pytrends.build_payload(keywords, cat, timeframes[0], geo, gprop)

    data =  pytrends.interest_over_time()
    mean = round(data.mean(), 2)
    print(mean[kw])

for kw in all_keywords:
    keywords.append(kw)
    check_trends()
    keywords.pop()