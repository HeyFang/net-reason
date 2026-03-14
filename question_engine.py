def ask_questions(fact_base):

    ans = input("Do you have internet access? (y/n): ")

    fact_base.add_fact("no_internet", ans == "n")

    ans = input("Do you have an IP address assigned? (y/n): ")

    fact_base.add_fact("ip_assigned", ans == "y")

    ans = input("Can you ping your gateway? (y/n): ")

    fact_base.add_fact("cannot_ping_gateway", ans == "n")

    ans = input("Can you ping 8.8.8.8? (y/n): ")

    fact_base.add_fact("cannot_ping_external_ip", ans == "n")
