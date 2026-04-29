import csv, requests
from datetime import datetime

events = []
for row in csv.DictReader(open("/Users/kirill/ClaudeProjects/Delegation analytics/results.csv")):
    ts = row["time"].replace(" UTC","").strip()
    events.append({
        "user_id": row["user_id"],
        "event_type": row["event_type"],
        "time": int(datetime.fromisoformat(ts + "+00:00").timestamp()*1000),
        "event_properties": {
            "delegation_id": row["delegation_id"],
            "delegated_order_id": row["delegated_order_id"],
            "side": row["side"],
            "facility_code": row["print_house_name"],
            "origin_country": row["origin_country"],
            "destination_country": row["destination_country"],
            "tenant_id": row["tenant_id"],
            "customer_id": row["customer_id"],
            "product_category": row["product_category"],
            "product_model": row["product_model"],
            "sla_min_production_days": row["sla_min_production_days"],
            "sla_max_production_days": row["sla_max_production_days"]
        }
    })

API_KEY = "77e0c7232dd14c91b72292b057e42389"
for i in range(0, len(events), 2000):
    r = requests.post("https://api2.amplitude.com/batch", json={"api_key": API_KEY, "events": events[i:i+2000]})
    print(f"{min(i+2000, len(events))}/{len(events)}: {r.status_code}")

print("Done!")
