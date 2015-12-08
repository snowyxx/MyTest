import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;

/**
 * 
 * @author yan �����޸��ļ�������ԭ�ļ���ǰ�����4λ���
 */
public class RenameFile {
	public static void main(String[] args) {
		String filelist;
		if (args.length != 1) {
			System.out.println("Usage:\nʹ���ļ�����Ϊ����\n\t���ļ�Ӧ����Ҫ������ļ��б�");
		} else {
			filelist = args[0];
			File lf = new File(filelist);
			BufferedReader br;
			try {
				br = new BufferedReader(new FileReader(lf));

				String line = "";
				int i = 0;
				while ((line = br.readLine()) != null) {
					i++;
					System.out.println("<OraName:> "+line);
					String newname = addCount(i, line);
					File f = new File(line);
					if (f.exists()) {
						f.renameTo(new File(newname));
						System.out.println("<NewName:> "+newname);
					} else {
						System.out.println("<NOTE:> " + line + "������");
					}
					System.out.println("--------------------");
				}

			} catch (Exception e) {
				e.printStackTrace();
			}
		}
	}

	public static String addCount(int c, String fn) {
		String newname = "";
		String cc = String.valueOf(c);
		while (cc.length() < 4) {
			cc = "0" + cc;
		}
		int i = fn.lastIndexOf("/");
		if (i != -1) {
			newname = fn.substring(0, i + 1) + cc + "_" + fn.substring(i + 1);
		} else {
			newname = cc + "_" + fn;
		}
		return newname;
	}

}
