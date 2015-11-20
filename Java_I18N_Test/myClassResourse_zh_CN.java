import java.util.ListResourceBundle;

public class myClassResourse_zh_CN extends ListResourceBundle{

	private final Object myData[][]={
		{"my.test.hello","CLASS_\u6C49\u5B57"},
		{"my.test.formatedmessage","CLASS_{0}\u4F60\u597D\uFF01\u73B0\u5728\u65F6\u95F4\u4E8B {1}\u3002"}
	};
	@Override
	protected Object[][] getContents() {
		return myData;
	}
	
}