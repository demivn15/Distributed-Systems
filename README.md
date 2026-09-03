# 🌐 Distributed-Systems

## Workshop 1: Client/Server

### Environment setup

Operating Systems: Windows 11 (Host 1) and Linux (Host 2).

- Programming Languages: Python 3.x and C (compiled with GCC/Cygwin).
- Software Tools: Visual Studio Code, Git, Github.
- Network Configuration: Both hosts were connected to the same Local Area Network (LAN). 

> The server was configured to listen on port 12000. Windows Firewall rules were modified to allow inbound TCP traffic on the specified port.

### Implementation details

Both the Python and C implementations work with multithreading. This configuration allows to spawn different clients from a single execution while allowing the server to properly process multiple incoming connections at the same time. Different configurations for server and client were tested. 

### Results

Results show proper communication between parties regardless of the language used for coding. 

### Known problems

It is important to notice that, in order to properly connect both systems, Windows had to be configured at the firewall level to allow inbound TCP traffic from port 12000.

> For more details check the full report.

---

## Workshop 2: Communication (Messaging and Message Queuing)

---

## Workshop 3: Naming

