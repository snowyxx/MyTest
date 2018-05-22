import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.util.ArrayList;
import java.util.Enumeration;
import java.util.Properties;

public class APActiveClientCount {

	public static void main(String[] args) {
		ArrayList apNames = new ArrayList();
		ArrayList clientCount = new ArrayList();
		int ver = 0;
		String verStr = "v1";
		
		APSnmpTest client = new APSnmpTest();
		String host = "192.168.0.19";
		String community = "public";
		if (args.length > 1) {
			host = args[0];
			community = args[1];
			try {
				verStr = args[2];
				ver = ("v2c".equals(verStr.trim()))?1:0;  //0 = v1  1=v2c
			} catch (Exception e) {
			}
		}

		client.target.setTargetHost(host);
		client.target.setTargetPort(161);
		client.target.setCommunity(community);
		client.target.setSnmpVersion(ver); 
		client.logger.info("------------ host: "+host+" ----------");
		String snmpTimeout = null;
		try {
			snmpTimeout = client.prop.getProperty("snmp.target.set.timeout");
		} catch (Exception e) {
		}
		int snmpTimeoutValue = snmpTimeout != null ? Integer.parseInt(snmpTimeout) : 5;
		client.target.setTimeout(snmpTimeoutValue);
		
		String retries = null;
		try {
			retries = client.prop.getProperty("snmp.target.set.retries");
		} catch (Exception e) {
		}
		int retriesValue = retries != null ? Integer.parseInt(retries) : 0;
		if (retriesValue > 0) {client.target.setRetries(retriesValue);}
		
		
		// apnames.properties content: <ap name> = <active client count> , if previous ap not available this time, it would be  <ap name> = -1
		Properties previousApNames = new Properties();
		try {
			previousApNames.load(new FileInputStream("apnames.properties"));
		} catch (Exception e) {
		}
		
		
		apNames = client.getByColumn(".1.3.6.1.4.1.9.9.513.1.1.1.1.5");
		clientCount = client.getByColumn(".1.3.6.1.4.1.9.9.513.1.1.1.1.72");
		
//		for(int i=0; i<apNames.size(); i++){
//			System.out.println(apNames.get(i)+"\t"+clientCount.get(i));
//		}
		
		//to check if this a new ap, and set name and active clent count
		for(int i=0;i<apNames.size();i++){
			String name = (String) apNames.get(i);
			if(!previousApNames.containsKey(name)) {
        		previousApNames.put(name, clientCount.get(i));
        		//todo: more actions for new found ap
			}else{
				previousApNames.setProperty(name, clientCount.get(i).toString());
			}
		}

		System.out.println("Data:");
		
		// to check if a ap lost, set it value to -1
		Enumeration<?> pnames = previousApNames.propertyNames();
		while (pnames.hasMoreElements()) {  
            String name = (String) pnames.nextElement();
            if(!apNames.contains(name)) {
            		previousApNames.setProperty(name, "-1");
            }
            System.out.println(name+"\t"+previousApNames.getProperty(name));
        } 
		if(previousApNames.containsValue("-1")) {
            System.out.println("Message: Error AP found");
        }else {
            System.out.println("Message: No issue found");
        }
		try {
			previousApNames.store(new FileOutputStream("apnames.properties"), "store all ap, value means active client count, -1=offline");
		} catch (Exception e) {
			client.logger.info("failed to write apnames.properties");
		}
		
		System.exit(0);
	}

}
