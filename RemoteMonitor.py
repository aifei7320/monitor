import paramiko
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(name)s:%(levelname)s: %(message)s"
)

class RemoteMonitor:
    ip = ''
    port = 22
    username = ''
    password = ''
    def __init__(self,ip,username,password):
        self.ip = ip
        self.port = 22
        self.username = username
        self.password = password

    def SSHConnection(self,ip,user,password):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip,22,user,password)
        return ssh

    def ExecCommand(self,ssh,cmd):
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = stdout.readlines()
        #print result,len(result)
        return result

    def Monitor(self, doShow):
        self.ssh = self.SSHConnection(self.ip,self.username,self.password)
        top_cmd = "top -b -n1 -d1 | grep calmcar | awk '{print $1,$6,$9}'"
        print(top_cmd)
        cpu_usage = 0
        memory_usage = 0
        pid = -1
        cpu_usage_vis = []
        plt.close()
        figure = plt.figure("show")
        ax = figure.add_subplot(111) # Create a `axes' instance in the figure
        #ax.plot(X1, Y1, X2, Y2) # Create a Line2D instance in the axes
        #sns.set(style="white", context="talk")
        top_result = self.ExecCommand(self.ssh,top_cmd)
        print(top_result)
        top_list = top_result[0].strip().split(' ')
        #print top_result
        pid = top_list[0]
        memory_usage = top_list[1]
        cpu_usage = top_list[2]
        logging.info("pid:" + pid+ ' cpu:' + cpu_usage+' mem:' + memory_usage)
        if (doShow == True):
            self.CPUVisualization(figure,ax,cpu_usage_vis,cpu_usage)
        else:
            plt.close()

    def CPUVisualization(self,f,ax,cpu_usage_vis,cpu_usage):
        #plt.clf()
        limit =10
        cpu_usage_vis.insert(0,float(cpu_usage))
        #ax = f.add_subplot(111)
        ax.set_xlim((0, limit))
        #ax.set_xticks([0, np.pi, 2*np.pi])
        #ax.set_xticklabels(['0', '$\pi$', '2$\pi$'])
        ax.set_ylim((0, 400))
        ax.set_yticks([0, 0,100])
            # Set up the matplotlib figur
        #
        if len(cpu_usage_vis) > limit:
            cpu_usage_vis.pop()
        x = np.array(cpu_usage_vis)
        y = np.arange(len(x))
        ax.bar(y, x)
        #f.draw()
        plt.pause(0.01)
        #plt.show(block=False)

if __name__ == "__main__":
    logging.info("test")
    monitor = RemoteMonitor("192.168.199.220","root","ubuntu")
    monitor.Monitor()
