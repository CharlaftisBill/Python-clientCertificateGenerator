#!/usr/bin python3
import os
import argparse
import shutil

#Helpers
def generateCert():

    print("""\nThe (pre)defined csr parameters are:
             c  :    %s,
             st :    %s,
             l  :    %s,
             o  :    %s,
             ou :    %s.
             """%(args.country, args.state, args.location, args.organization, args.organizationUnit))

    option = ""
    while(option not in ["y", "yes", "n", "no"]):
        option = str(input("do you want to change them? (y/n): \n")).lower()
   
    if option == "y" or option == "yes" :
        args.country = input("Enter your country (ex. GR) : ")
        args.state = input("Enter your state (ex. Attiki) : ")
        args.location = input("Enter your location (ex. Athens) : ")
        args.organization = input("Enter your organization (ex.KEPYES) : ")
        args.organizationUnit = input("Enter your organization unit(ex. SYSTEMS) : ")
 
    os.system('openssl req -newkey rsa:'+str(args.rsaSize)+' -days '+str(args.expireAfter)+' -nodes -keyout '+clientPrivateKey+' -subj "/C='+args.country+'/ST='+args.state+'/L='+args.location+'/O='+args.organization+'/OU='+args.organizationUnit+'/CN='+args.commonName+'" > '+csrpath)
    print("\nClient Key Stored Here :" + clientPrivateKey)
    print("Client CSR Stored Here :" + csrpath)

    os.system('openssl x509 -req -in '+csrpath+' -days '+str(args.expireAfter)+' -CAkey '+args.cakey+' -CA '+args.caCert+' -set_serial 01 > '+crtpath)
    print("Client Cert Stored Here :" + crtpath)

    shutil.copy(args.caCert, args.outputDir + "/" +args.commonName + "/ca.crt")

    print("\n\n")

    option = ""
    while(option not in ["y", "yes", "n", "no"]):
        option = str(input("Do you want to delete "+csrpath+"? (y/n): ")).lower()
    
    if option == "y" or option == "yes" :
        os.remove(csrpath)

#Variables

argParser = argparse.ArgumentParser(description="Generate Client Cert and Key.")
argParser.add_argument('-s','--rsaSize', type=int, metavar='rsaSize', default=2048, help="RSA private key bit size (default:2048)")
argParser.add_argument('-e','--expireAfter', type=int, metavar='expireAfter', default=365, help="Days for the cert to expire (default:365)")
argParser.add_argument('-ca','--caCert', type=str, metavar='caCert', help="The path of the CA certificate.", required=True)
argParser.add_argument('-cakey','--cakey', type=str, metavar='cakey', help="The path of the CA private key.", required=True)
argParser.add_argument('-out','--outputDir', type=str, metavar='outputDir', default= os.getcwd(), help="Output dir for the cert (default: is the cwd :"+os.getcwd()+")")
argParser.add_argument('-cn','--commonName', type=str, metavar='commonName', default= "", help="Common name is usually the domain name.")
argParser.add_argument('-c','--country', type=str, metavar='country', default= "GR", help="Country to be written to csr file (default: GR).")
argParser.add_argument('-st','--state', type=str, metavar='state', default= "Attiki", help="State to be written to csr file (default: Attiki).")
argParser.add_argument('-l','--location', type=str, metavar='location', default= "Athens", help="Location to be written to csr file (default: Athens).")
argParser.add_argument('-o','--organization', type=str, metavar='organization', default= "KEPYES", help="Organization to be written to csr file (default: E-corp).")
argParser.add_argument('-ou','--organizationUnit', type=str, metavar='organizationUnit', default= "Systems", help="Organization Unit to be written to csr file (default: Athens).")
args = argParser.parse_args()

# Variables checkers
if args.rsaSize not in [1024, 2048, 4096]:
    print("Invalid RSA size. Please choose one of 1024, 2048, 4096.")

if not os.path.exists(args.outputDir):
    os.makedirs(args.outputDir)

while args.commonName == "":
    args.commonName = input("Enter the Domain: ")

if not os.path.exists(args.outputDir + "/" + args.commonName + "/"):
    os.makedirs(args.outputDir + "/" + args.commonName + "/")

clientPrivateKey = args.outputDir + "/" + args.commonName + "/" + args.commonName +  '.key'
os.system("openssl genrsa -out "+clientPrivateKey+" "+str(args.rsaSize))

csrpath = args.outputDir + "/" + args.commonName + "/" + args.commonName + '.csr'
crtpath = args.outputDir + "/" +args.commonName + "/" +  args.commonName +  '.cert'

# Logic
generateCert()