import pip
import sys
import subprocess
from subprocess import check_output
import os

## Create virtual env before running this script
#python3.8 -m venv myvenv

# The main purpose of this scriput is to use  vscode interactive window

# Check whether the script runs inside virtualenv


def installIpykernel(venv):


   if os.path.basename(sys.prefix) == venv:
   
      print("We're inside virtualenv")

      # upgrade pip
      output =subprocess.Popen("pip3 install --upgrade pip", shell=True, stdout=subprocess.PIPE)
      out,err = output.communicate()
      print(out)

      # check pip --version
      output  = subprocess.Popen("python3.8 -m pip --version", shell=True, stdout=subprocess.PIPE)
      out, err = output.communicate()
      output = out.decode("utf-8")
      target = output[0:10]
   
      FirstTwoDigits = ""
      for i in target:
         if i.isdigit():
            FirstTwoDigits+=i
         elif i == '.':
             break
      print(FirstTwoDigits)

      if int(FirstTwoDigits) > 20:
         print("Pip version ok")
         output = subprocess.Popen("pip3 install ipykernel", shell=True, stdout=subprocess.PIPE)
         out, err = output.communicate()
         
         output = subprocess.Popen("pip3 install -r requirements.txt", shell=True, stdout=subprocess.PIPE)
         out, err = output.communicate()
      else:

          print("Wrong pip version")   

   else:
       print("Error: you're not inside virtualenv")


if __name__=='__main__':
   name = input("Enter your virtualvenv name: ")
   installIpykernel(name)