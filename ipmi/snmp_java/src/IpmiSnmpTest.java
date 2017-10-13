import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map.Entry;
import java.util.Properties;
import java.util.Vector;
import java.util.logging.FileHandler;
import java.util.logging.Level;
import java.util.logging.Logger;
import java.util.logging.SimpleFormatter;

import com.adventnet.afp.log.LogException;
import com.adventnet.afp.log.LoggerProperties;
import com.adventnet.snmp.beans.SnmpTarget;
import com.adventnet.snmp.mibs.MibException;
import com.adventnet.snmp.mibs.MibNode;
import com.adventnet.snmp.mibs.MibOperations;
import com.adventnet.snmp.snmp2.SnmpOID;
import com.adventnet.utils.LogManager;

public class IpmiSnmpTest {
	SnmpTarget target =new SnmpTarget();
	Logger logger = Logger.getLogger("IpmiSnmpTest");
	Properties prop = new Properties();
	public IpmiSnmpTest(){
		
		try {
			File dir = new File("logs");
			if(!dir.exists()) {
				dir.mkdirs();
			}
			FileHandler handler = new FileHandler("logs/IpmiSnmpTest_info.txt", 1024*1024, 1, true);
			logger.addHandler(handler);
			logger.setLevel(Level.ALL);
			SimpleFormatter formatter = new SimpleFormatter();
			handler.setFormatter(formatter);
		} catch (SecurityException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		try {
			prop.load(new FileInputStream("oids.properties"));
		} catch (FileNotFoundException e) {
			logger.info("oids.properties file not found.");
			logger.info(e.toString());
		} catch (IOException e) {
			logger.info("can not read oids.properties file.");
			logger.info(e.toString());
		}
		
		String snmpDebugMode = prop.getProperty("snmp.debug.mode");
		if (snmpDebugMode != null && snmpDebugMode.equals("true")) {
			logger.info("snmp.debug.mode is true.");
			LoggerProperties loggerProp = new LoggerProperties("SNMP", "SNMP");
			loggerProp.setClassName("com.adventnet.utils.SnmpLoggerImpl");
			loggerProp.setLogLevel(LogManager.CRITICAL);
			loggerProp.addCustomProperty("LOGTYPE", "DEBUG");
			try {
				target.addLogClient(loggerProp);
			} catch (LogException e) {
				e.printStackTrace();
			}
		}
	}

	public static void main(String[] args) {
		IpmiSnmpTest client = new IpmiSnmpTest();
		String host="192.168.0.19";
		String community="public";
		if (args.length>1){
			host=args[0];
			community=args[1];
		}
		
		client.target.setTargetHost(host);
		client.target.setTargetPort(161);
		client.target.setCommunity(community);
		client.target.setSnmpVersion(0);
		client.target.setTimeout(5);
		
		client.processIBMHWData();
		System.exit(0);
		

	}

	private void printTable(ArrayList result,String name) {
		
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

	private void processIBMHWData() {
		
		
		HashMap<String,String> tables = new HashMap<String,String>();
		tables.put("TMP", ".1.3.6.1.4.1.2.3.51.3.1.1.2");
		tables.put("VOLT", ".1.3.6.1.4.1.2.3.51.3.1.2.2");
		tables.put("FAN", ".1.3.6.1.4.1.2.3.51.3.1.3.2");
//		tables.put("Error", ".1.3.6.1.4.1.2.3.51.3.2.1.1");  move to conf file oids.properties
		
		HashMap<String,String> attributes=new HashMap<String,String>();
		attributes.put("Power Status", ".1.3.6.1.4.1.2.3.51.3.5.1.1.0");
		attributes.put("System Status",".1.3.6.1.4.1.2.3.51.3.5.1.4.0");
		

		for(Entry entry:prop.entrySet()) {
			String name = (String) entry.getKey();
			String oid = (String) entry.getValue();
			if (name.startsWith("TABLE_") && !tables.containsKey(name.substring(6, name.length()))) {
				tables.put(name.substring(6, name.length()), oid);
			}else if(name.startsWith("ATTRI_") && !tables.containsKey(name.substring(6, name.length()))) {
				attributes.put(name.substring(6, name.length()), oid);
			}else {
				logger.info("Your key should start with TABLE_ or ATTRI_: " + name);
			}
		}

		
		for(Entry<String, String> entry:tables.entrySet()){
			String name=entry.getKey();
			String oid=entry.getValue();
			logger.info("going to snmpget table: "+name+" : "+oid);
			ArrayList result=getTableRows(oid);
			printTable(result,name);
		}
		
		for(Entry<String, String> entry:attributes.entrySet()){
			String name=entry.getKey();
			String oid=entry.getValue();
			logger.info("going to snmpget attribute: "+name+" : "+oid);
			getAndPrintAttribute(name,oid);
		}

	}
	private void getAndPrintAttribute(String name, String oid) {
		SnmpOID snmpoid=new SnmpOID(oid);
		target.setSnmpOID(snmpoid);
		String result=target.snmpGet();
		result = (result!=null)?result:"NA";
		System.out.println(name+"="+result);
		
	}

	private ArrayList getTableRows(String oid){
		ArrayList result= new ArrayList();
		String oids[]=null;
		try {
			target.loadMibs("./imm.mib");
		} catch (MibException | IOException e) {
			logger.info("Can not read mib file. Do add imm.mib file to this folder!");
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
			try {
				String[][] data=target.snmpGetAllList();
				for(int i=0;i<data.length;i++){
					ArrayList<String> row = new ArrayList<String>();
					for(int j=0;j<data[i].length;j++){
						row.add(data[i][j]);
					}
					result.add(row);
				}
			}catch(NullPointerException e) {
				logger.info("No response from snmp agent.");
				logger.info(e.toString());
			}catch(Exception e){
				logger.info(e.toString());
			}

		}
		
		return result;
	}
}

