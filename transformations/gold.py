from collections import defaultdict

def calculate_bus_performance(events):

    speeds_by_bus = defaultdict(list)

    for event in events:

        bus_id = event["bus_id"]
        speed = event["speed"]

        speeds_by_bus[bus_id].append(speed)


    result = []

    for bus_id, speeds in speeds_by_bus.items():

        result.append({
            "bus_id": bus_id,
            "event_count": len(speeds),
            "average_speed": sum(speeds) / len(speeds),
            "minimum_speed": min(speeds),
            "maximum_speed": max(speeds)
        })

    return result