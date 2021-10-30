"""
Read and parse APRS packets
Author: Aaron Chan
"""

import re
import aprslib

def parse_all(packet):
    print(packet)
    parsed = re.match(r"^(?P<call>.+)>(?P<dest>.+),:=(?P<latitude>\d{4}\.\d{2}[NS])", packet)

    call = parsed.group("call")
    dest = parsed.group("dest")
    latitude = parsed.group("latitude")


    print(call)
    print(dest)
    print(latitude) # TODO: Adjust values. Value should not be going past 90


def main():
    packet = "KD2WSM-5>APDR16,:=4307.61N\07741.17WS433.290MHz" 

    print("REGEX")
    parse_all(packet)


    # NOTE: Consider using aprslib. Depends on how the packet is formatted
    parsed = aprslib.parse("KD2WSM-5>APDR16:!4307.61N/07741.17WS433.290MHz")

    raw = parsed["raw"]
    callsign = parsed["from"]
    receiver = parsed["to"]
    latitude = parsed["latitude"]
    longitude = parsed["longitude"]
    message = parsed["comment"]

    print("\n")
    print(
        "APRSLIB \n"
        "Raw: ", raw, "\n"
        "Callsign: ", callsign, "\n",
        "Reciever: ", receiver, "\n"
        "Latitude: ", latitude, "\n"
        "Longitude: ", longitude, "\n"
        "Message: ", message
    )


if __name__ == "__main__":
    main()
