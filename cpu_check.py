from netmiko import ConnectHandler
from ttp import ttp
import json

ttp_template = """
<group name="Show_Sytem_CPU"> 
<group name="TOTAL_Show_Sytem_CPU">
"""

def system_cpu_parser(data_to_parse):
    parser = ttp(data=data_to_parse, template=ttp_template)
    parser.parse()

    # print result in JSON format
    results = parser.result(format='json')[0]
    #print(results)

    #converting str to json. 
    result = json.loads(results)

    return(result)

ports = [11111, 11112, 11113, 11114, 11115]
#ports = [11111]

for port in ports:
    
    SR = {
        'device_type': 'alcatel_sros',
        'ip': 'X.X.X.X',
        'username': 'admin',
        'password': 'admin',
        'port': port
    }

    net_connect = ConnectHandler(**SR)
    net_connect.send_command('environment no more ')
    output = net_connect.send_command('show system cpu sample-period 60')
    #print (output)

    parsed_system_cpu_parser = system_cpu_parser(output)
    #print(parsed_system_cpu_parser[0])

    print(f"\nConnecting to the node through the port {port}")
    print('#'*40 + '\n')
    
    counter = False

    for i in parsed_system_cpu_parser[0]:
        for j in parsed_system_cpu_parser[0][i]:
            if "TOTAL" in j:
                #print(parsed_system_cpu_parser[0][i][j])
                continue
            else:
                #print(j)
                j_CPU_Usage = j['CPU_Usage'].strip('%').strip('~')
                j_CAPACITY_Usage = j['CAPACITY_Usage'].strip('%').strip('~')
                #print(j_CPU_Usage)
                #print(j_CAPACITY_Usage)

                if float(j_CPU_Usage) > 85 or float(j_CAPACITY_Usage) > 85:
                    counter = True
                    print(f"The system CPU for {j['Name']} is higher than %85 percent.")
    
    if counter == False:
        print("There is no CPU problem observed for this node.")
  
  
  
