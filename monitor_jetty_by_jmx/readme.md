This is the script to monitor jetty by jmx which could be used under [ManageEngine Applications Manager](http://www.appmanager.com) conf base monitor framework.

**Applications Manager already support jetty monitoring by default, so this is useless.**

1. 修改etc/jetty-jmx-remote.xml文件，去掉rmi部分的注释。
2. 编辑start.ini添加：

        --module=jmx-remote
        jetty.jmxrmihost=localhost
        jetty.jmxrmiport=1099
        -Dcom.sun.management.jmxremote

3. 启动Jetty
4. 尝试使用jconsole连接管理。
