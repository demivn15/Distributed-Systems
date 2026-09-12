import dns.resolver
import dns.reversename
import dns.query
import dns.message
import dns.rdatatype

def basicDNSLookup(domainNameInput:str) -> None:
    domainName:str = domainNameInput
    try:
        responses:dns.resolver.Answer = dns.resolver.resolve(domainName)
        for response in responses:
            print(f"{domainName} -> {response}")
    except Exception as error:
        print(f"Error: {error}")

def reverseDNSLookup(ipAddressIput:str) -> None:
    ipAddress:str = ipAddressIput
    try:
        reverseName:dns.name.Name = dns.reversename.from_address(ipAddress)
        answers = dns.resolver.resolve(reverseName, "PTR")
        for rdata in answers:
            print(rdata.target)
    except Exception as error:
        print(f"Error: {error}")

def querySpecificDNS(domainNameInput:str, nameserverIPInput:str) -> None:
    domainName:str = domainNameInput
    nameserverIP:str = nameserverIPInput
    try:
        customResolver = dns.resolver.Resolver()
        customResolver.nameservers = [nameserverIP]
        responses = customResolver.resolve(domainName)
        for response in responses:
            print(f"[{nameserverIP}] {domainName} -> {response}")
    except Exception as error:
        print(f"Error: {error}")

def retrieveMXRecords(domainNameInput:str) -> None:
    domainName:str = domainNameInput
    try:
        responses = dns.resolver.resolve(domainName, "MX")
        for response in responses:
            print(f"{domainName} MX -> Exchange: {response.exchange}, Priority: {response.preference}")
    except Exception as error:
        print(f"Error: {error}")

def retrieveNSRecords(domainNameInput:str) -> None:
    domainName:str = domainNameInput
    try:
        responses = dns.resolver.resolve(domainName, "NS")
        for response in responses:
            print(f"{domainName} NS -> {response.target}")
    except Exception as error:
        print(f"Error: {error}")

def querySOARecord(domainNameInput:str) -> None:
    domainName:str = domainNameInput
    try:
        responses = dns.resolver.resolve(domainName, "SOA")
        for response in responses:
            print(f"{domainName} SOA -> Primary NS: {response.mname}, Responsible Email: {response.rname}")
    except Exception as error:
        print(f"Error: {error}")

def queryCNAMERecord(domainNameInput:str) -> None:
    domainName:str = domainNameInput
    try:
        responses = dns.resolver.resolve(domainName, "CNAME")
        for response in responses:
            print(f"{domainName} CNAME -> {response.target}")
    except Exception as error:
        print(f"Error: {error}")

def debugModeLookup(domainNameInput:str) -> None:
    domainName:str = domainNameInput
    try:
        queryMessage = dns.message.make_query(domainName, dns.rdatatype.A)
        responseMessage = dns.query.udp(queryMessage, "1.1.1.1")
        print(f"--- Debug Mode Raw Message for {domainName} ---")
        print(responseMessage)
    except Exception as error:
        print(f"Error: {error}")

def queryNonExistentDomain(domainNameInput:str) -> None:
    domainName:str = domainNameInput
    try:
        responses = dns.resolver.resolve(domainName)
        for response in responses:
            print(f"{domainName} -> {response}")
    except Exception as error:
        print(f"Error: {error}")

def main() -> None:
    print("--- Basic DNS Lookup ---")
    basicDNSLookup("yachaytech.edu.ec")
    
    print("\n--- Reverse DNS Lookup ---")
    reverseDNSLookup("8.8.8.8")
    
    print("\n--- Query Specific DNS (Cloudflare 1.1.1.1) ---")
    querySpecificDNS("yachaytech.edu.ec", "1.1.1.1")
    
    print("\n--- Retrieve MX Records ---")
    retrieveMXRecords("yachaytech.edu.ec")
    
    print("\n--- Retrieve NS Records ---")
    retrieveNSRecords("yachaytech.edu.ec")
    
    print("\n--- Query SOA Record ---")
    querySOARecord("yachaytech.edu.ec")
    
    print("\n--- Query CNAME Record ---")
    queryCNAMERecord("www.microsoft.com")
    
    print("\n--- Debug Mode Lookup ---")
    debugModeLookup("yachaytech.edu.ec")
    
    print("\n--- Query Non-Existent Domain ---")
    queryNonExistentDomain("nonexistdomain12345.com")

if __name__ == "__main__":
    main()
