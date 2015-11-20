import java.text.MessageFormat;
import java.util.Date;
import java.util.Locale;
import java.util.ResourceBundle;
/*
Three class used by java i18n:
	java.util.ResourceBundle
	java.util.Locale
	java.text.MessageFormat

Resource file name format:
	basename_language_country.properties
	basename_language.properties
	basename.properties
	
Stirng convert tool:
	native2ascii
	*/

public class I18NTest {

	//Test Locale class
	public static void localeTest() {
		Locale[] localelist =  Locale.getAvailableLocales();
		for(int i=0;i<localelist.length;i++){
			System.out.println(localelist[i].getCountry()+"\t"+localelist[i].getDisplayCountry()+"\t"+localelist[i].getLanguage()+"\t"+localelist[i].getDisplayLanguage());;
		}
		Locale myLocale =  Locale.getDefault();
		System.out.println(myLocale.getLanguage()+"_"+myLocale.getCountry());
	}
	
	//Test ResourceBundle class
	public static void bundleTest(){
		Locale myloc = Locale.getDefault();
		ResourceBundle rb = ResourceBundle.getBundle("myResource", myloc);
		System.out.println(rb.getString("my.test.hello"));
	}
	
	//Test MessageFormat class
	public static void megfmtTest(){
		Locale lc = Locale.getDefault();
		ResourceBundle rb = ResourceBundle.getBundle("myResource", lc);
		String msg = rb.getString("my.test.formatedmessage");
		System.out.println(MessageFormat.format(msg, "Snow",new Date()));
	}
	
	//Test read a class as bundle resource
	public static void clsresTest(){
		Locale lc = Locale.getDefault();
		ResourceBundle rb = ResourceBundle.getBundle("myClassResourse", lc);
		System.out.println(rb.getString("my.test.hello"));
	}
	public static void main(String[] args) {
//		System.out.println(System.getProperty("user.dir"));
//		localeTest();
//		bundleTest();
//		megfmtTest();
		clsresTest();
		
	}

}
