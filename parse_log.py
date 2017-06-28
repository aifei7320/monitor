import sys
import logging

logging.basicConfig(
    level=logging.WARN,
    format="[%(asctime)s] %(name)s:%(levelname)s: %(message)s"
)

class LogElement:
    name = ''
    count = 0
    cost_mean = 0.0
    cost_max = 0.0
    cost_min = 0.0
    cost_sum = 0.0
    def __init__(self,name,v):
        self.name = name
        self.cost_count = 1
        self.cost_mean = 0
        self.cost_sum = 0
        self.cost_sum  = self.cost_sum + v
        self.cost_max = v
        self.cost_min = v
        self.cost_mean = v

    def Update(self,v):
        self.cost_count = self.cost_count + 1
        self.cost_sum  = self.cost_sum + v
        if v > self.cost_max:
            self.cost_max = v
        if v < self.cost_min:
            self.cost_min = v
        self.cost_mean = self.cost_sum/self.cost_count
    def Print(self):
        print "%10s  %6.2f  %6.2f  %6.2f"%(self.name,self.cost_max,self.cost_min,self.cost_mean)




class LogParser:
    log_result = []
    log_name = []
    def __init__(self):
        print "LogParser init"

    def ParselogLine(self,line):
        line = line.strip('. ');
        line = line.strip(',');
        logging.info("ParselogLine:"+line)
        line_split = line.split(' ')
        logging.info("line_split:"+line)
        for section in line_split:
            logging.info("section:"+section)
            if len(section) < 2:
                continue
            section = section.strip(',');
            t = section.split(':')
            if len(t) < 2:
                continue
            if t[0] not in self.log_name:
                logging.info("log_name:"+t[0]+t[1])
                #print "log_name---",t[0],t[1]
                self.log_name.append(t[0])
                tmp = LogElement(t[0],float(t[1]))
                self.log_result.append(tmp)
            else:
                index = self.log_name.index(t[0])
                self.log_result[index].Update(float(t[1]))


    def ParseLog(self,file_name):
        f = open(file_name, 'r')
        for  line in  f.readlines():
            if line.find("mmdd", 0, len(line)) != -1:
                continue
            index = line.find("[", 0, len(line))
            if index != -1:
                logging.info("line:"+line[index-1:-1])
                self.ParselogLine(line[index-1:-1].strip("[ms]."))
                
    def Print(self):
        print "result:"
        print "name       max       min       mean"
        for d in range(len(self.log_result)):
            self.log_result[d].Print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "need param"
    else:
        parser = LogParser()
        parser.ParseLog(sys.argv[1])
        parser.Print()
    #print log_name
