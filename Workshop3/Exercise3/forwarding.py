locations = {
 "A": "B",
 "B": "C",
 "C": "D",
 "D": "192.168.1.50:5000"
}

def resolve(location):
 hops = 0
 while location in locations:
     print("Following:", location, "->", locations[location])
     location = locations[location]
     hops += 1
 return location, hops

def main():
    print("--- BEFORE OPTIMIZATION ---")
    address, hops = resolve("A")
    print("Final address:", address)
    print("Number of hops:", hops)
    print()
    print("--- AFTER OPTIMIZATION ---")
    locations["A"] = address
    address_opt, hops_opt = resolve("A")
    print("Final address:", address_opt)
    print("Number of hops:", hops_opt)
    print()
    print("\n--- FAILURE SILUMATION ---")
    locations["A"] = "B" 
    del locations["C"]
    address_fail, hops_fail = resolve("A")
    print("Final address:", address_fail)
    print("Number of hops:", hops_fail)

if __name__ == "__main__":
    main()
