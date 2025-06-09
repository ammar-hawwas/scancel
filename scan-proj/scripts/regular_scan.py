import nmap
import pandas as pd


def regular_scan(ip_range):
    # إنشاء كائن الماسح الضوئي
    scanner = nmap.PortScanner()
    print(f"Starting regular scan for range: {ip_range}")
    
    # تنفيذ الفحص الشامل لجميع المنافذ (بدون تعديل في جزء الفحص)
    scanner.scan(ip_range, arguments='-T4 -A -p- -sV')

    # تخزين النتائج في قائمة
    all_results = []
    for host in scanner.all_hosts():
        print(f"\nResults for IP: {host}")
        results_data = []
        
        # جمع بيانات المنافذ TCP
        for port in scanner[host].all_tcp():
            port_data = scanner[host]['tcp'][port]
            results_data.append([host, port, 'TCP', port_data.get('state'), port_data.get('name'), port_data.get('version')])
            print(f"Port: {port}, State: {port_data.get('state')}, Service: {port_data.get('name')}, Version: {port_data.get('version')}")
        
        all_results.extend(results_data)

    # تحويل النتائج إلى DataFrame
    df = pd.DataFrame(all_results, columns=["IP", "Port", "Protocol", "State", "Service", "Version"])

    # عرض النتائج النهائية
    print("\nFinal Scan Results:")
    print(df)

    
    return df