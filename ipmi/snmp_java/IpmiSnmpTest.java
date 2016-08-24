import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map.Entry;
import java.util.Vector;

import com.adventnet.snmp.beans.SnmpTarget;
import com.adventnet.snmp.mibs.MibException;
import com.adventnet.snmp.mibs.MibNode;
import com.adventnet.snmp.mibs.MibOperations;
import com.adventnet.snmp.snmp2.SnmpOID;

public class IpmiSnmpTest {

	public static void main(String[] args) {
		SnmpTarget target = new SnmpTarget();
		String host="192.168.0.19";
		String community="public";
		if (args.length>1){
			host=args[0];
			community=args[1];
		}
		
		target.setTargetHost(host);
		target.setTargetPort(161);
		target.setCommunity(community);
		target.setSnmpVersion(0);
		target.setTimeout(30);
		processIBMHWData(target);
		System.exit(0);

	}

	private static void printTable(ArrayList result,String name) {
		
		int count=0;
		if("Error".equals(name)){
			Collections.reverse(result);
			System.out.println("<--table Last 5 Errors starts-->\nID#Time#Message");
		}else{
			System.out.println("<--table "+name+" starts-->\nID#Name#Value");
		}
		
		for(int i=0;i<result.size();i++){
				if (count==5){
					break;
				}
				StringBuffer sb =new StringBuffer();
				ArrayList row=(ArrayList) result.get(i);
				if("Error".equals(name)){
					String id= (String) row.get(0);
					String severity=(String) row.get(2);
					String message=(String) row.get(1);
					String date=(String) row.get(3);
					String time=(String) row.get(4);
					if(severity.indexOf("error(0)")>-1){
						sb.append(id).append("#").append(date).append(" ").append(time).append("#").append(message);
						count+=1;
					}else{
						//maybe do some other thing later...
						continue;
					}
				}else{
					String id= (String) row.get(0);
					String cname=(String) row.get(1);
					String value=(String) row.get(2);
					if("FAN".equals(name)){
						value=value.replaceAll(" %", "");
					}else if("VOLT".equals(name)){
						value=String.valueOf(Integer.valueOf(value)/1000.0);
					}
					sb.append(id).append("#").append(cname).append("#").append(value);
				}
				if(sb.length()>0){
					System.out.println(sb.toString());
				}
								
		}
		if("Error".equals(name)){
			System.out.println("<--table Last 5 Errors ends-->");
		}else{
			System.out.println("<--table "+name+" ends-->");
		}
		
	}

	private static void processIBMHWData(SnmpTarget target) {
		HashMap<String,String> tables = new HashMap<String,String>();
		tables.put("TMP", ".1.3.6.1.4.1.2.3.51.3.1.1.2");
		tables.put("VOLT", ".1.3.6.1.4.1.2.3.51.3.1.2.2");
		tables.put("FAN", ".1.3.6.1.4.1.2.3.51.3.1.3.2");
		tables.put("Error", ".1.3.6.1.4.1.2.3.51.3.2.1.1");
		
		HashMap<String,String> attributes=new HashMap<String,String>();
		attributes.put("Power Status", ".1.3.6.1.4.1.2.3.51.3.5.1.1.0");
		attributes.put("System Status",".1.3.6.1.4.1.2.3.51.3.5.1.4.0");
		for(Entry<String, String> entry:tables.entrySet()){
			String name=entry.getKey();
			String oid=entry.getValue();
			ArrayList result=getTableRows(target,oid);
			printTable(result,name);
		}
		
		for(Entry<String, String> entry:attributes.entrySet()){
			String name=entry.getKey();
			String oid=entry.getValue();
			getAndPrintAttribute(target,name,oid);
		}

	}
	private static void getAndPrintAttribute(SnmpTarget target,String name, String oid) {
		SnmpOID snmpoid=new SnmpOID(oid);
		target.setSnmpOID(snmpoid);
		String result=target.snmpGet();
		
		System.out.println(name+"="+result);
		
	}

	private static ArrayList getTableRows(SnmpTarget target,String oid){
		ArrayList result= new ArrayList();
		String oids[]=null;
		try {
			target.loadMibs("./imm.mib");
		} catch (MibException | IOException e) {
			e.printStackTrace();
		}
		MibOperations mibops=target.getMibOperations();
		SnmpOID snmptableoid=mibops.getSnmpOID(oid);
		MibNode tablenode=mibops.getMibNode(oid);
		if(tablenode!=null && tablenode.isTable()){
			Vector colums=tablenode.getTableItems();
			oids= new String[colums.size()];
			for(int i=0;i<oids.length;i++){
				oids[i]=(String)colums.elementAt(i);
			}
			target.setObjectIDList(oids);
			String[][] data=target.snmpGetAllList();
			
			for(int i=0;i<data.length;i++){
				ArrayList<String> row = new ArrayList<String>();
				for(int j=0;j<data[i].length;j++){
					row.add(data[i][j]);
				}
				result.add(row);
			}
		}
		
		return result;
	}
}

