import java.io.IOException;
import java.net.MalformedURLException;
import java.util.Arrays;
import java.util.Set;
import java.util.TreeSet;

import javax.management.Attribute;
import javax.management.AttributeList;
import javax.management.InstanceNotFoundException;
import javax.management.IntrospectionException;
import javax.management.MBeanAttributeInfo;
import javax.management.MBeanInfo;
import javax.management.MBeanServerConnection;
import javax.management.MalformedObjectNameException;
import javax.management.ObjectName;
import javax.management.ReflectionException;
import javax.management.remote.JMXConnector;
import javax.management.remote.JMXConnectorFactory;
import javax.management.remote.JMXServiceURL;


public class Test {
	
	public static void main(String[] args) {
		try {
			JMXServiceURL url= new JMXServiceURL("service:jmx:rmi:///jndi/rmi://192.168.2.22:1099/jmxrmi");
			JMXConnector jmxc = JMXConnectorFactory.connect(url);
			MBeanServerConnection mbsc=jmxc.getMBeanServerConnection();
			
			//Domains:
			String domains[]=mbsc.getDomains();
			Arrays.sort(domains);
			for(String domain:domains){
				System.out.println("\tDomain = "+domain);
			}
			
			System.out.println("\nMBeanServer default domain = "+mbsc.getDefaultDomain());
			
			System.out.println("\nMBean count = "+mbsc.getMBeanCount());
			
			System.out.println("\nQuery MBeanServer Mbeans:");
			Set<ObjectName> names = new TreeSet<ObjectName>(mbsc.queryNames(null, null));
			for (ObjectName name:names){
				System.out.println("\tObjectName = "+name);
			}
			
			
			
			System.out.println("\nGet  MBeans' data");
//			ObjectName mxbeanName= new ObjectName("JMImplementation:type=MBeanServerDelegate");
			ObjectName mxbeanName= new ObjectName("java.lang:type=OperatingSystem");
			MBeanInfo mbinfo=mbsc.getMBeanInfo(mxbeanName);
			System.out.println(mbinfo.getDescription());
			MBeanAttributeInfo[] attrInfos=mbinfo.getAttributes();
			String[] attrs = new String[attrInfos.length];
			for (int i=0;i<attrInfos.length;i++){
				MBeanAttributeInfo mbainfo=attrInfos[i];
				attrs[i]=mbainfo.getName();
			}
			
			AttributeList attrlist=mbsc.getAttributes(mxbeanName, attrs);
			for (Attribute attr:attrlist.asList()){
				System.out.println(attr.getName()+" = "+attr.getValue());
			}
			
			ObjectName threadon =new ObjectName("org.eclipse.jetty.util.thread:type=queuedthreadpool,*");
//			for (ObjectName on: mbsc.queryNames(threadon, null)){
//				
//			}
			System.out.println("yanxxx  "+mbsc.queryNames(threadon, null).size());
			jmxc.close();
		} catch (MalformedURLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (MalformedObjectNameException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (InstanceNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (ReflectionException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IntrospectionException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		
	}

}
