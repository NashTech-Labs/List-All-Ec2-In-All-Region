try:
    import boto3
    import csv
    import time
    from itertools import cycle
    from shutil import get_terminal_size
    from threading import Thread

    print("Yup!! All modules are loaded...")

except Exception as e:
    print("Please look into it, Modules are not loaded.. ")
class Loader:

    def __init__(self, description="Loading...", end_point="Done!", time_out=0.2):

        self.desc = description
        self.end = end_point
        self.timeout = time_out

        self._thread = Thread(target=self._animate, daemon=True)
        self.steps = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        self.done = False

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for i in cycle(self.steps):
            if self.done:
                break
            print(f"\r{self.desc} {i}", flush=True, end="")
            time.sleep(self.timeout)

    def __enter__(self):
        self.start()

    def stop(self):
        self.done = True
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        print(f"\r{self.end}", flush=True)

    def __exit__(self, exc_type, exc_value, tb):
        self.stop()

if __name__ == "__main__":
    with Loader("Loading for ec2 details..."):
        for i in range(3):
            time.sleep(0.25)
      
AWS_service=input("Enter the aws service name")

ec2_cli=boto3.client(service_name=AWS_service)
all_regions=[]
for each in ec2_cli.describe_regions()['Regions']: 
 all_regions.append(each['RegionName'])
print("These are the all region\n",all_regions)





csv_file=open('instance.csv','w',newline='')
data_file=csv.writer(csv_file)
data_file.writerow(['S.no',"InstanceType",'InstanceID',"Private_ip","Public_IP",'KeyName'])

count=1
for i in all_regions:
 ec2=boto3.resource(service_name='ec2',region_name=i)
 for ec2_in_region in ec2.instances.all():

  data_file.writerow([count,ec2_in_region.instance_id,ec2_in_region.instance_type,ec2_in_region.key_name,ec2_in_region.private_ip_address,ec2_in_region.public_ip_address])
  count+=1
csv_file.close()

loader = Loader("Loading for ec2 details...", "oohhh!!, That was too fast!", 0.05).start()
for i in range(3):
    time.sleep(0.25)

loader.stop()  
