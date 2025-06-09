import nmap
import pandas as pd


def intense_scan(ip_range):
    # إنشاء كائن الماسح الضوئي
    scanner = nmap.PortScanner()
    print(f"Starting intense scan for range: {ip_range}")
    
    # تنفيذ الفحص المكثف (بدون تعديل في جزء الفحص)
    scanner.scan(ip_range, arguments='-T4 -A -p-')

    # تخزين النتائج في قائمة
    all_results = []
    for host in scanner.all_hosts():
        print(f"\nResults for IP: {host}")
        results_data = []
        
        # جمع بيانات المنافذ TCP
        for port in scanner[host].all_tcp():
            port_data = scanner[host]['tcp'][port]
            results_data.append([host, port, "TCP", port_data.get('state'), port_data.get('name')])
            print(f"Port: {port}, Protocol: TCP, State: {port_data.get('state')}, Service: {port_data.get('name')}")
        
        # جمع بيانات المنافذ UDP
        for port in scanner[host].all_udp():
            port_data = scanner[host]['udp'][port]
            results_data.append([host, port, "UDP", port_data.get('state'), port_data.get('name')])
            print(f"Port: {port}, Protocol: UDP, State: {port_data.get('state')}, Service: {port_data.get('name')}")

        all_results.extend(results_data)

    # تحويل النتائج إلى DataFrame
    df = pd.DataFrame(all_results, columns=["IP", "Port","Protocol","State", "Service"])

    # عرض النتائج النهائية
    print("\nFinal Scan Results:")
    print(df)
   
    return df