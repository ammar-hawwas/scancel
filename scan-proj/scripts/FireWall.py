import nmap
import pandas as pd

def FireWall(ip_range):
    scanner = nmap.PortScanner()

    # تحديد المنافذ التي نرغب بفحصها
    target_ports = "21,22,23,25,53,80,110,143,135,137,138,139,143,161,389,443,445,1434,1521,1723,1900,3306,3389,5000,5060,5357,5900,6379,8080,11211"
    scanner.scan(ip_range, arguments=f'-T5 -sV -p {target_ports}')

    all_results = []
    filtered_found = 0
    open_ports = 0

    for host in scanner.all_hosts():
        for port in scanner[host].all_tcp():
            port_data = scanner[host]['tcp'][port]
            state = port_data.get('state')
            service = port_data.get('name')
            version = port_data.get('version')

            # عدّ المنافذ حسب حالتها
            if state == 'filtered' or state == 'closed':
                filtered_found += 1
            elif state == 'open':
                open_ports += 1

            all_results.append([host, port, 'TCP', state, service, version])

    # تحديد حالة الجدار الناري
    firewall_status = ""
    if filtered_found > 0:
        firewall_status = "Active"
        print("Success: The firewall appears to be active and working correctly.")
    elif open_ports > len(target_ports.split(',')) / 2:
        firewall_status = "Potential Issue"
        print("Warning: There is a potential issue with your firewall. Some ports are open.")
    else:
        firewall_status = "Undetermined"
        print("No clear indication of firewall status.")

    # عرض النتائج في DataFrame
    df = pd.DataFrame(all_results, columns=["IP", "Port", "Protocol", "State", "Service", "Version"])

    # إضافة حالة الجدار الناري كصف منفصل بنفس عدد الأعمدة
    firewall_row = pd.DataFrame([["Firewall Status", "", "", "", "", firewall_status]], 
                                columns=["IP", "Port", "Protocol", "State", "Service", "Version"])
    df = pd.concat([df, firewall_row], ignore_index=True)

   
    return df