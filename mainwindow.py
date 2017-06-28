#!/usr/bin/python3
#coding:utf-8
#*************************************************************************
#    > File Name: mainwindow.py
#    > Author: zxf
#    > Mail: zhengxiaofeng333@163.com 
#    > Created Time: 2017年06月22日 星期四 14时08分43秒
# ************************************************************************

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import stat
import os
import subprocess
import numpy
from RemoteMonitor import *
from PyQt5.QtCore import *

class ConnectWindow(QDialog):
    emitInfo = pyqtSignal(str)
    def __init__(self, parent=None):
        super(ConnectWindow, self).__init__(parent)
        
        self.IPLabel = QLabel("服务器IP:")

        self.remoteIP = QLineEdit("192.168.199.108")

        connectBtn = QPushButton("连接")
        cancelBtn = QPushButton("取消")

        btnLayout = QHBoxLayout()
        btnLayout.addWidget(connectBtn)
        btnLayout.addWidget(cancelBtn)

        connectBtn.clicked.connect(self.DoConnect)
        cancelBtn.clicked.connect(self.DoCancel)

        gridlayout = QGridLayout()
        gridlayout.addWidget(self.IPLabel, 0, 0)
        gridlayout.addWidget(self.remoteIP, 0, 1)
        gridlayout.addLayout(btnLayout, 1, 0, 1, 2)

        gridlayout.setSpacing(10)

        self.setLayout(gridlayout)
        self.resize(260, 150)

    def DoConnect(self):
        self.emitInfo.emit(self.remoteIP.text())
        self.close()

    def DoCancel(self):
        print("nihao")

class MainWindow(QDialog):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.updateTimer = QTimer()

        self.font=QFont()
        self.font.setPointSize(14)
        self.font.setFamily("雅黑")

        idLayout = QHBoxLayout()
        idLabel = QLabel()
        idLabel.setFont(self.font)
        idLabel.setText("PID:")
        self.id = QLabel()
        self.id.setMinimumWidth(20)
        self.id.setFont(self.font)
        idLayout.addWidget(idLabel)
        idLayout.addWidget(self.id)

        memLayout = QHBoxLayout()
        memLabel = QLabel()
        memLabel.setFont(self.font)
        memLabel.setText("MEM:")
        self.mem = QLabel()
        self.mem.setMinimumWidth(20)
        self.mem.setFont(self.font)
        memLayout.addWidget(memLabel)
        memLayout.addWidget(self.mem)
       
        usageLayout = QHBoxLayout()
        usageLabel = QLabel()
        usageLabel.setFont(self.font)
        usageLabel.setText("CPU:")
        self.usage = QLabel()
        self.usage.setMinimumWidth(20)
        self.usage.setFont(self.font)
        usageLayout.addWidget(usageLabel)
        usageLayout.addWidget(self.usage)

        netLayout = QHBoxLayout()
        netLabel = QLabel()
        netLabel.setFont(self.font)
        self.netUsage = QLabel()
        self.netUsage.setFont(self.font)
        self.netUsage.setMinimumWidth(20)
        netLayout.addWidget(netLabel)
        netLayout.addWidget(self.netUsage)


        rstProcessBtn = QPushButton("重启进程")
        rstProcessBtn.setEnabled(False)
        rstProcessBtn.clicked.connect(self.reset)

        showUsageBtn = QPushButton("重启设备")
        showUsageBtn.setEnabled(False)
        showUsageBtn.clicked.connect(self.showUsage)

        self.showLogBtn = QPushButton("显示LOG")
        self.showLogBtn.setEnabled(False)
        self.showLogBtn.setCheckable(True)
        self.showLogBtn.clicked.connect(self.showLog)


        gridLayout = QGridLayout()
        gridLayout.addLayout(idLayout, 0, 0, 1, 1)
        gridLayout.addLayout(memLayout, 0, 1, 1, 1)
        gridLayout.addLayout(usageLayout, 0, 2, 1, 1)
        gridLayout.addWidget(rstProcessBtn, 1, 0, 1, 1)
        gridLayout.addWidget(self.showLogBtn, 1, 1, 1, 1)
        gridLayout.addWidget(showUsageBtn, 1, 2, 1, 1)
        gridLayout.setSpacing(15)
        gridLayout.setVerticalSpacing(30)

        self.setLayout(gridLayout)
        self.show()
         
        #cw = ConnectWindow()
        #cw.emitInfo.connect(self.DoConnect)
        #cw.exec_()
    
    def DoConnect(self, ip):
        self.remoteIP = ip
        self.WritePingScript(ip);
        os.chmod("ping.sh", stat.S_IRWXU | stat.S_IRWXG | stat.S_IROTH)
        p = subprocess.Popen(r'./ping.sh',stdout=subprocess.PIPE)
        pingResult = p.stdout.read() 
        p.wait()
        if (pingResult[0] == ord("1")):
           QMessageBox.warning(self, "Warning!", "Remote can't reach\nConnect failed.") 
           self.close()
        else:
            self.monitor = RemoteMonitor(ip,"ubuntu", "ubuntu")
            rstProcessBtn.setEnabled(True)
            showUsageBtn.setEnabled(True)
            showLogBtn.setEnabled(True)
            self.updateTimer.start(1000)


    def WritePingScript(self, ip):
        scriptfile = open("ping.sh", "w+") 
        print("#!/bin/bash\n", file=scriptfile)
        print("PING=`ping -c 3 -s 1 %s | grep '0 received' | wc -l`\n"%(self.remoteIP), file = scriptfile)
        print("echo -en $PING\n", file = scriptfile)
        scriptfile.close()

    def update(self):
        showID()
        showMem()
        showUsage()

    def reset(self):
        self.monitor.ExecCommand("kill calmcar")

    def showNet(self):
        self.netUsage.setText(self.monitor.ExecCommand("sar -b 10 1 | sed -n '4p' | awk '{print $4}'") )


    def showMem(self):
        self.mem.setText(self.monitor.ExecCommand("top -b -n1 -d1 | grep calmcar | awk '{print $6}'"))


    def showID(self):
        self.id.setText(self.monitor.ExecCommand("pidof calmcar"))


    def showUsage(self): 
        self.usage.setText(self.monitor.ExecCommand("top -b -n1 -d1 | grep calmcar | awk '{print $9}'"))

    def showLog(self):
        if( self.showLogBtn.toggled()):
            self.monitor.Monitor(True)
        else:
            self.monitor.Monitor(False)



app = QApplication(sys.argv)
dlg = MainWindow()
dlg.show()
app.exec_()
app.exit()
