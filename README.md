# Python-clientCertificateGenerator

## Examples:
### The Good:

 ```
 python3 ./clientCertificateGenerator.py -ca ./path/to/ca.crt -cakey ./path/to/ca.key
 ```
 ### The Bad:

 ```
 python3 ./clientCertificateGenerator.py

usage: clientCertificateGenerator.py [-h] [-s rsaSize] [-e expireAfter] -ca caCert -cakey cakey [-out outputDir] [-cn commonName] [-c country] [-st state] [-l location] [-o organization] [-ou organizationUnit]
clientCertificateGenerator.py: error: the following arguments are required: -ca/--caCert, -cakey/--cakey
 ```

### The Ugly:
```
python3 ./clientCertificateGenerator.py -ca ./path/to/ca.crt -cakey ./path/to/ca.key -s 1024 -e 365 -o /export/path/ -cn domain_name -c wakanda -st utopia -l wonderland -o E-Corp -ou Chocolate_department
```
#
## Arguments:

arguments are required:
```
-ca, --caCert   :  The path of the CA certificate
-cakey, --cakey :  The path of the CA private key
```
optional arguments:
```
  -h, --help                :   Shows this help message and exit
  -s, --rsaSize             :   RSA private key bit size (default:2048)
  -e, --expireAfter         :   Days for the cert to expire (default:365)
  -out, --outputDir         :   Output dir for the cert (default: is the cwd)
  -cn, --commonName         :   Common name is usually the domain name
  -c, --country             :   Country to be written to csr file (default: GR)
  -st, --state              :   State to be written to csr file (default: Attiki)
  -l, --location            :   Location to be written to csr file (default: Athens)
  -o, --organization        :  Organization to be written to csr file (default: E-corp).
  -ou, --organizationUnit   :   Organization Unit to be written to csr file (default: Athens).
```