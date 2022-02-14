#!/usr/bin python3
import os
import shutil
import argparse
from typing import Tuple

# Helper's function.


def run_command(cmd):
    return os.system(cmd+'>/dev/null 2>&1')


def arg_parser_init():
    argParser = argparse.ArgumentParser(
        description="Generate Client Cert and Key.")
    argParser.add_argument('-s', '--rsaSize', type=int, metavar='rsaSize',
                           default=2048, help="RSA private key bit size (default:2048)")
    argParser.add_argument('-e', '--expireAfter', type=int, metavar='expireAfter',
                           default=365, help="Days for the cert to expire (default:365)")
    argParser.add_argument('-ca', '--caCert', type=str, metavar='caCert',
                           help="The path of the CA certificate.", required=True)
    argParser.add_argument('-cakey', '--cakey', type=str, metavar='cakey',
                           help="The path of the CA private key.", required=True)
    argParser.add_argument('-out', '--outputDir', type=str, metavar='outputDir', default=os.getcwd(),
                           help="Output dir for the cert (default: is the cwd :"+os.getcwd()+")")
    argParser.add_argument('-cn', '--commonName', type=str, metavar='commonName',
                           default="", help="Common name is usually the domain name.")
    argParser.add_argument('-c', '--country', type=str, metavar='country',
                           default="GR", help="Country to be written to csr file (default: GR).")
    argParser.add_argument('-st', '--state', type=str, metavar='state',
                           default="Attiki", help="State to be written to csr file (default: Attiki).")
    argParser.add_argument('-l', '--location', type=str, metavar='location',
                           default="Athens", help="Location to be written to csr file (default: Athens).")
    argParser.add_argument('-o', '--organization', type=str, metavar='organization',
                           default="KEPYES", help="Organization to be written to csr file (default: E-corp).")
    argParser.add_argument('-ou', '--organizationUnit', type=str, metavar='organizationUnit',
                           default="Systems", help="Organization Unit to be written to csr file (default: Athens).")

    return arg_parser_validate(argParser.parse_args())


def arg_parser_validate(args):
    if args.rsaSize not in [1024, 2048, 4096]:
        raise SystemExit(
            "Invalid RSA size. Please choose one of 1024, 2048, 4096.")

    while args.commonName == "":
        args.commonName = input("Enter the Domain (CN): ")

    return args


def set_files_paths_dir(args) -> Tuple[str, str, str]:

    if not os.path.exists(args.outputDir + "/" + args.commonName + "/"):
        os.makedirs(args.outputDir + "/" + args.commonName + "/")

    args.outputDir = args.outputDir + "/" + args.commonName + "/"

    return (
        args.outputDir + args.commonName + '.key',     # client_key_path
        args.outputDir + args.commonName + '.csr',     # client_csr_path
        args.outputDir + args.commonName + '.cert')    # client_crt_path


def main():
    args = arg_parser_init()
    client_key_path, client_csr_path, client_crt_path = set_files_paths_dir(args)

    cert = certHandler(args, client_key_path, client_csr_path, client_crt_path)
    cert.generate_client_cert()


class certHandler:
    def __init__(self, args, client_key_path: str, client_csr_path: str, client_crt_path: str):
        self.args = args
        self.client_key_path = client_key_path
        self.client_csr_path = client_csr_path
        self.client_crt_path = client_crt_path

    def generate_client_cert(self):
        self.__generate_client_private_key(self.args)
        self.__dialog_edit_csr_parameters(self.args)
        self.__generate_client_crt(self.args)
        self.__generate_client_x509_cert(self.args)
        self.__copy_ca_cert_to_output_dir(self.args)

    def __generate_client_private_key(self, args):
        run_command("openssl genrsa -out " +
                   self.client_key_path+" "+str(args.rsaSize))
        print("\n ---> Client Key Stored Here :" + self.client_key_path)

    def __generate_client_crt(self, args):
        run_command('openssl req -newkey rsa:' +
                   str(args.rsaSize) +
                   ' -days '+str(args.expireAfter) +
                   ' -nodes -keyout '+self.client_key_path +
                   ' -subj "/C='+args.country +
                   '/ST='+args.state +
                   '/L='+args.location +
                   '/O='+args.organization +
                   '/OU='+args.organizationUnit +
                   '/CN='+args.commonName +
                   '" > ' +
                   self.client_csr_path)

        print("\n ---> Client CSR Stored Here :" + self.client_csr_path)

    def __generate_client_x509_cert(self, args):
        run_command('openssl x509 -req -in ' +
                   self.client_csr_path+' -days ' +
                   str(args.expireAfter) +
                   ' -CAkey '+args.cakey +
                   ' -CA '+args.caCert +
                   ' -set_serial 01 > ' +
                   self.client_crt_path)

        print(" ---> Client Cert Stored Here :" + self.client_crt_path)

    def __copy_ca_cert_to_output_dir(self, args):
        shutil.copy(args.caCert, args.outputDir + "/ca.crt")
        print(" ---> Ca.crt file copied to output directory too.")

    def __dialog_edit_csr_parameters(self, args):
        print("""\nThe (pre)defined csr parameters are:
            c  :    %s,
            st :    %s,
            l  :    %s,
            o  :    %s,
            ou :    %s."""
              % (args.country, args.state, args.location, args.organization, args.organizationUnit))

        option = ""
        while(option not in ["y", "yes", "n", "no"]):
            option = str(
                input("\nDo you want to change them? (y/n): ")).lower()

        if option == "y" or option == "yes":
            args.country = input("Enter your country (ex. GR) : ")
            args.state = input("Enter your state (ex. Attiki) : ")
            args.location = input("Enter your location (ex. Athens) : ")
            args.organization = input(
                "Enter your organization (ex. KEPYES) : ")
            args.organizationUnit = input(
                "Enter your organization unit(ex. SYSTEMS) : ")

    def dialog_delete_csr_file(self):
        option = ""
        while(option not in ["y", "yes", "n", "no"]):
            option = str(input("\nDo you want to delete the csr file :" +
                         self.client_csr_path+"? (y/n): ")).lower()

        if option == "y" or option == "yes":
            os.remove(self.client_csr_path)


if __name__ == "__main__":
    main()
