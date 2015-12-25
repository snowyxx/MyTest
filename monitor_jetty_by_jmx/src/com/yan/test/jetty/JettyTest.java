package com.yan.test.jetty;

import java.io.IOException;
import java.net.MalformedURLException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Properties;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import javax.management.Attribute;
import javax.management.AttributeList;
import javax.management.MBeanServerConnection;
import javax.management.MalformedObjectNameException;
import javax.management.ObjectName;
import javax.management.remote.JMXConnector;
import javax.management.remote.JMXConnectorFactory;
import javax.management.remote.JMXServiceURL;

import com.adventnet.appmanager.server.framework.CustomDCInf;

public class JettyTest implements CustomDCInf {
	public static ObjectName RT_ONAME = null;
	public static ObjectName OS_ONAME = null;
	public static ObjectName CL_ONAME = null;
	public static ObjectName THREAD_ONAME = null;
	public static ObjectName JETTY_THREAD_ONAME = null;
	public static ObjectName JETTY_MEMORY_ONAME = null;
	public static ArrayList convertSizeList = new ArrayList();
	static {
		try {
			RT_ONAME = new ObjectName("java.lang:type=Runtime");
			OS_ONAME = new ObjectName("java.lang:type=OperatingSystem");
			CL_ONAME = new ObjectName("java.lang:type=ClassLoading");
			THREAD_ONAME = new ObjectName("java.lang:type=Threading");
			JETTY_THREAD_ONAME = new ObjectName("org.eclipse.jetty.util.thread:type=queuedthreadpool,*");
			JETTY_MEMORY_ONAME = new ObjectName("resin:type=Memory");
			convertSizeList.add("TotalPhysicalMemorySize");
			convertSizeList.add("TotalSwapSpaceSize");

		} catch (MalformedObjectNameException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (NullPointerException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}

	public Properties CheckAuthentication(Properties dcProps) {
		JMXConnector connector = null;

		try {
			connector = getJMXConnector(dcProps);

		} catch (Exception e) {
			e.printStackTrace();
		}
		if (connector != null) {
			dcProps.setProperty("availability", "1");
			dcProps.put("authentication", "passed");
		} else {
			dcProps.setProperty("availability", "0");
			dcProps.put("authentication", "failed");
			dcProps.setProperty("error", "Could not add monitor, as JMXConnection not established.");
		}
		return dcProps;
	}

	public String callMain(Properties props) {
		MBeanServerConnection server = null;
		StringBuffer toreturn = new StringBuffer();

		try {
			long currentTime=System.currentTimeMillis();
			JMXConnector connector = getJMXConnector(props);

			if (connector != null) {
				long responeseTime=System.currentTimeMillis()-currentTime;
				toreturn.append("script_responsetime="+responeseTime+"\n");
				System.out.println("Got Connection Successfully");
				server = connector.getMBeanServerConnection();
				toreturn.append("script_availability=0\n"); // No I18N
				toreturn.append("script_message=DataCollection Successfull\n"); // No I18N
				toreturn.append("script_code=error\n"); // No I18N

			} else {
				toreturn.append("script_availability=1\n"); // No I18N
				toreturn.append("script_message=Could not get JMXConnection\n"); // No I18N
				toreturn.append("script_code=error\n"); // No I18N
			}
			if (server == null) {
				System.out.println("Could not get MBean Server");
				toreturn.append("script_availability=1\n"); // No I18N
				toreturn.append("script_message=Could not get Mbeans Connection\n"); // No I18N
				toreturn.append("script_code=error\n"); // No I18N
			} else {
				getOSInfo(server, toreturn);
				getVMInfo(server, toreturn);
				getJVMThreadInfo(server, toreturn);
				getJettyThreadInfo(server, toreturn);
				getJettySessionInfo(server, toreturn);
				System.out.println("toreturn::" + toreturn.toString());

			}
		} catch (Exception e) {
			e.printStackTrace();
		}
		return toreturn.toString();
		// JMXConnector con = getMBeanServerConnection(obj, comProps,coltime);
	}

	public void getJettySessionInfo(MBeanServerConnection server,
			StringBuffer toreturn) {
		String[] attrs = new String[] { "sessions", "sessionsTotal", "stopTimeout" }; // NO I18N
		String[] attrstype = new String[] { "INT", "INT", "LONG"};
		toreturn.append("<--table Session Details starts-->\n"); // No I18N
		toreturn.append("Name").append("\t").append("|");
		toreturn.append("SessionActiveCount").append("\t").append("|");
		toreturn.append("SessionCreateCountTotal").append("\t").append("|");
		toreturn.append("SessionTimeOut\n");
		try {

			for (Object o : server.queryNames(new ObjectName("org.eclipse.jetty.server.session:type=hashsessionmanager,*"), null)) {
				ObjectName oname = (ObjectName) o;
				String mponame = oname.toString();
				System.out.println("Session Object :" + mponame);

				String pattern="context=(.*?),";
				Pattern r = Pattern.compile(pattern);
				Matcher m = r.matcher(mponame);
				mponame=m.find()?m.group(1):mponame;
				
				HashMap values = getAttributes(server, oname, attrs);
				if (values != null && !values.isEmpty()) {
					toreturn.append(mponame).append("|\t");
					appendDataToOutput(values, toreturn, attrs, attrstype,
							"|\t");
				}
				toreturn.delete(toreturn.lastIndexOf("|"), toreturn.length());
				toreturn.append("\n");
			}

		} catch (MalformedObjectNameException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (NullPointerException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		toreturn.append("<--table Session Details ends-->\n"); // No I18N
	}

	public void getJettyThreadInfo(MBeanServerConnection server,
			StringBuffer toreturn) {
		String[] attrs = { "busyThreads", "idleThreads", "maxThreads", "minThreads", "threads" };
		HashMap values = getTotalValueForAttributes(server, JETTY_THREAD_ONAME, attrs);
		int threadCount = (Integer) values.get("threads");
		values.remove("threads");
		attrs = new String[] { "busyThreads", "idleThreads", "maxThreads", "minThreads" };
		String[] attrType = { "INT", "INT", "INT", "INT" };
		appendDataToOutput(values, toreturn, attrs, attrType, "\n");
		toreturn.append("JettyThreadCount").append("=").append(threadCount).append("\n");
	}

	public void getJVMThreadInfo(MBeanServerConnection server,
			StringBuffer toreturn) {
		String[] attrs = { "ThreadCount", "DaemonThreadCount",
				"PeakThreadCount", "TotalStartedThreadCount" };
		String[] attrType = { "INT", "INT", "INT", "LONG" };
		HashMap values = getAttributes(server, THREAD_ONAME, attrs);
		appendDataToOutput(values, toreturn, attrs, attrType, "\n");

	}

	public void getVMInfo(MBeanServerConnection server, StringBuffer toreturn) {
		String[] attrs = { "LoadedClassCount", "UnloadedClassCount" };
		String[] attrType = { "INT", "LONG" };
		HashMap values = getAttributes(server, CL_ONAME, attrs);
		appendDataToOutput(values, toreturn, attrs, attrType, "\n");
		attrs = new String[] { "CollectionTime", "CollectionCount" }; // NO I18N
		attrType = new String[] { "LONG", "LONG" };
		try {
			values = getTotalValueForAttributes(server, new ObjectName(
					"java*:type=GarbageCollector,*"), attrs);
			appendDataToOutput(values, toreturn, attrs, attrType, "\n");
		} catch (MalformedObjectNameException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (NullPointerException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}

	public void getOSInfo(MBeanServerConnection server, StringBuffer toreturn) {
		String[] attrs = { "VmName", "VmVendor", "VmVersion", "Uptime","BootClassPath", "ClassPath", "LibraryPath", "Name","StartTime" };
		String[] attrType = { "STRING", "STRING", "STRING", "LONG", "STRING", "STRING", "STRING", "STRING", "STRING" };
		HashMap values = getAttributes(server, RT_ONAME, attrs);
		long uptime=(Long)values.get("Uptime")>0?(Long)values.get("Uptime")/1000/60:0;
		String starttime=values.get("StartTime") != null?new java.text.SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(values.get("StartTime")):"-";
		values.put("Uptime",uptime);
		values.put("StartTime",	starttime);
		appendDataToOutput(values, toreturn, attrs, attrType, "\n");
		attrs = new String[] { "TotalPhysicalMemorySize", "TotalSwapSpaceSize" }; // NO
																					// I18N
		attrType = new String[] { "LONG", "LONG" };
		values = getAttributes(server, OS_ONAME, attrs);
		appendDataToOutput(values, toreturn, attrs, attrType, "\n");
	}

	private void appendDataToOutput(HashMap values, StringBuffer toreturn, String[] attrs) {
		appendDataToOutput(values, toreturn, attrs, null, "\n");
	}

	private void appendDataToOutput(HashMap values, StringBuffer toreturn, String[] attrs, String[] attrsType, String delimiter) {
		try {
			System.out.println(values);
			for (int i = 0; i < attrs.length; i++) {
				String attName = attrs[i];

				if (values.containsKey(attName)) {
					if (attrsType == null || attrsType[i].equals("STRING")) {
						if (delimiter.equals("|\t")) {
							toreturn.append(((String) values.get(attName)) != null ? (String) values.get(attName) : "-");
						} else {
							toreturn.append(attName).append("=").append(((String) values.get(attName)) != null ? (String) values.get(attName) : "-");
						}
					} else if (attrsType[i].equals("INT")) {
						if (delimiter.equals("|\t")) {
							toreturn.append(((Integer) values.get(attName)) != null ? (Integer) values.get(attName) : "-");
						} else {
							toreturn.append(attName).append("=").append(((Integer) values.get(attName)) != null ? (Integer) values.get(attName) : "-");
						}
					} else {
						float longValue = ((Long) values.get(attName)) != null ? (Long) values.get(attName) : -1;
						if (longValue != -1 && convertSizeList.contains(attName)) {
							longValue = (longValue) / (1024 * 1024);
						}
						if (delimiter.equals("|\t")) {
							toreturn.append(longValue != -1 ? longValue : "-");
						} else {
							toreturn.append(attName).append("=").append(longValue != -1 ? longValue : "-");
						}
					}
					toreturn.append(delimiter);
				} else {
					if (delimiter.equals("|\t")) {
						toreturn.append("-" + delimiter);
					} else {
						toreturn.append(attName + "=-" + delimiter);
					}
				}

			}

		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	public HashMap getTotalValueForAttributes(MBeanServerConnection server, ObjectName o, String[] attrs) {
		HashMap totValues = new HashMap();
		try {
			for (Object obj : server.queryNames(o, null)) {
				try {
					ObjectName oname = (ObjectName) obj;
					HashMap values = getAttributes(server, oname, attrs);
					if (totValues.isEmpty()) {
						totValues = values;
					} else {
						Iterator it = values.keySet().iterator();
						while (it.hasNext()) {
							String key = (String) it.next();
							long value = totValues.containsKey(key) ? ((Long) totValues.get(key) + (Long) values.get(key)): (Long) values.get(key);
							totValues.put(key, value);
						}
					}
				} catch (Exception e) {
					e.printStackTrace();
				}

			}
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return totValues;
	}

	private HashMap getAttributes(MBeanServerConnection server, ObjectName o,
			String[] attrs) {
		try {
			AttributeList list = server.getAttributes(o, attrs);
			HashMap values = new HashMap();
			for (int i = 0, size = list.size(); i < size; i++) {
				Attribute a = (Attribute) list.get(i);
				values.put(a.getName(), a.getValue());

			}
			return values;
		} catch (Exception e) {
			System.out.println("Exception while fetching attribute " + e);
		}
		return null;
	}

	public JMXConnector getJMXConnector(Properties props) {
		String namingHost = (String) props.get("HostName");
		String namingPort = (String) props.get("Port");
		String jndiPath = (String) props.get("JNDIPath");
		String username = (String) props.get("UserName");
		String password = (String) props.get("Password");
		JMXConnector connector = null;
		JMXServiceURL url = null;
		try {

			url = new JMXServiceURL("service:jmx:rmi:///jndi/rmi://"
					+ namingHost + ":" + namingPort + jndiPath);
			System.out.println("url:service:jmx:rmi:///jndi/rmi://"
					+ namingHost + ":" + namingPort + jndiPath);
			Map env = new HashMap();
			env.put("java.naming.factory.initial",
					"com.sun.jndi.rmi.registry.RegistryContextFactory");
			env.put("jmx.remote.x.client.connection.check.period", 0L);
			if (username != null && password != null) {
				String[] credentials = { username, password };
				env.put(JMXConnector.CREDENTIALS, credentials);
			}

			try {
				connector = JMXConnectorFactory.connect(url, env);
				System.out.println("CAM: Got the connector : " + connector);
			} catch (Exception e) {
				e.printStackTrace();
				if (connector != null) {
					try {
						connector.close();
					} catch (IOException e1) {
						// TODO Auto-generated catch block
						e1.printStackTrace();
					}
					connector = null;
				}
			}

		}

		catch (MalformedURLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return connector;
	}
	public static void main(String[] args){
		JettyTest jt= new JettyTest();
		Properties props= new Properties();
		props.put("HostName", "192.168.2.22");
		props.put("Port", "1099");
		props.put("JNDIPath", "/jmxrmi");
		jt.callMain(props);
	}
}
