def print_diagnosis(facts):

    print("\nDiagnosis Result")
    print("----------------")

    if facts.get("dhcp_failure"):
        print("Possible Cause: DHCP Failure")

    if facts.get("router_not_reachable"):
        print("Possible Cause: Router not reachable")

    if facts.get("local_network_failure"):
        print("Likely Issue: Local Network Failure")
