import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;

/**
 * 
 * @author yan 批量修改文件名，在原文件名前添加上4位编号
 */
public class RenameFile {
	public static void main(String[] args) {
		String filelist;
		if (args.length != 1) {
			System.out.println("Usage:\n使用文件名作为参数\n\t该文件应包含要处理的文件列表");
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
						System.out.println("<NOTE:> " + line + "不存在");
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
