.. _intro-basic-networking:

================
Basic networking
================

Ethernet
~~~~~~~~

Ethernet is a networking protocol, specified by the IEEE 802.3 standard. Most
wired network interface cards (NICs) communicate using Ethernet.

In the `OSI model <https://en.wikipedia.org/wiki/OSI_model>`_ of networking
protocols, Ethernet occupies the second layer, which is known as the data
link layer. When discussing Ethernet, you will often hear terms such as
*local network*, *layer 2*, *L2*, *link layer* and *data link layer*.

In an Ethernet network, the hosts connected to the network communicate
by exchanging *frames*. Every host on an Ethernet network is uniquely
identified by an address called the media access control (MAC) address.
In particular, every virtual machine instance in an OpenStack environment
has a unique MAC address, which is different from the MAC address of the
compute host. A MAC address has 48 bits and is typically represented as a
hexadecimal string, such as ``08:00:27:b9:88:74``. The MAC address is
hard-coded into the NIC by the manufacturer, although modern NICs
allow you to change the MAC address programmatically. In Linux, you can
retrieve the MAC address of a NIC using the :command:`ip` command:

.. code-block:: console

   $ ip link show eth0
   2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP mode DEFAULT group default qlen 1000
        link/ether 08:00:27:b9:88:74 brd ff:ff:ff:ff:ff:ff

Conceptually, you can think of an Ethernet network as a single bus
that each of the network hosts connects to. In early implementations,
an Ethernet network consisted of a single coaxial cable that hosts
would tap into to connect to the network. However, network hosts in
modern Ethernet networks connect directly to a network device called a
*switch*. Still, this conceptual model is useful, and in network diagrams
(including those generated by the OpenStack dashboard) an Ethernet network
is often depicted as if it was a single bus. You'll sometimes hear an
Ethernet network referred to as a *layer 2 segment*.

In an Ethernet network, every host on the network can send a frame directly to
every other host. An Ethernet network also supports broadcasts so
that one host can send a frame to every host on the network by sending to the
special MAC address ``ff:ff:ff:ff:ff:ff``. ARP_ and DHCP_
are two notable protocols that use Ethernet broadcasts. Because Ethernet
networks support broadcasts, you will sometimes hear an Ethernet network
referred to as a *broadcast domain*.

When a NIC receives an Ethernet frame, by default the NIC checks to
see if the destination MAC address matches the address of the NIC (or
the broadcast address), and the Ethernet frame is discarded if the MAC
address does not match. For a compute host, this behavior is
undesirable because the frame may be intended for one of the
instances. NICs can be configured for *promiscuous mode*, where they
pass all Ethernet frames to the operating system, even if the MAC
address does not match. Compute hosts should always have the
appropriate NICs configured for promiscuous mode.

As mentioned earlier, modern Ethernet networks use switches to
interconnect the network hosts. A switch is a box of networking
hardware with a large number of ports that forward Ethernet frames
from one connected host to another. When hosts first send frames over
the switch, the switch doesn't know which MAC address is associated
with which port. If an Ethernet frame is destined for an unknown MAC
address, the switch broadcasts the frame to all ports. The switch learns
which MAC addresses are at which ports by observing the traffic. Once
it knows which MAC address is associated with a port, it can send
Ethernet frames to the correct port instead of broadcasting. The
switch maintains the mappings of MAC addresses to switch ports in a
table called a *forwarding table* or *forwarding information base*
(FIB). Switches can be daisy-chained together, and the resulting
connection of switches and hosts behaves like a single network.

VLANs
~~~~~

VLAN is a networking technology that enables a single switch to act as
if it was multiple independent switches. Specifically, two hosts that
are connected to the same switch but on different VLANs do not see
each other's traffic. OpenStack is able to take advantage of VLANs to
isolate the traffic of different projects, even if the projects happen
to have instances running on the same compute host. Each VLAN has an
associated numerical ID, between 1 and 4094. We say "VLAN 15" to refer
to the VLAN with a numerical ID of 15.

To understand how VLANs work, let's consider VLAN applications in a
traditional IT environment, where physical hosts are attached to a
physical switch, and no virtualization is involved. Imagine a scenario
where you want three isolated networks but you only have a single
physical switch. The network administrator would choose three VLAN
IDs, for example, 10, 11, and 12, and would configure the switch to
associate switchports with VLAN IDs. For example, switchport 2 might be
associated with VLAN 10, switchport 3 might be associated with VLAN
11, and so forth. When a switchport is configured for a specific VLAN,
it is called an *access port*. The switch is responsible for ensuring
that the network traffic is isolated across the VLANs.

Now consider the scenario that all of the switchports in the first
switch become occupied, and so the organization buys a second switch
and connects it to the first switch to expand the available number of
switchports. The second switch is also configured to support VLAN IDs
10, 11, and 12. Now imagine host A connected to switch 1 on a port
configured for VLAN ID 10 sends an Ethernet frame intended for host B
connected to switch 2 on a port configured for VLAN ID 10. When switch
1 forwards the Ethernet frame to switch 2, it must communicate that
the frame is associated with VLAN ID 10.

If two switches are to be connected together, and the switches are configured
for VLANs, then the switchports used for cross-connecting the switches must be
configured to allow Ethernet frames from any VLAN to be
forwarded to the other switch. In addition, the sending switch must tag each
Ethernet frame with the VLAN ID so that the receiving switch can ensure that
only hosts on the matching VLAN are eligible to receive the frame.

A switchport that is configured to pass frames from all VLANs and tag them with
the VLAN IDs is called a *trunk port*. IEEE 802.1Q is the network standard
that describes how VLAN tags are encoded in Ethernet frames when trunking is
being used.

Note that if you are using VLANs on your physical switches to implement project
isolation in your OpenStack cloud, you must ensure that all of your
switchports are configured as trunk ports.

It is important that you select a VLAN range not being used by your current
network infrastructure. For example, if you estimate that your cloud must
support a maximum of 100 projects, pick a VLAN range outside of that value,
such as VLAN 200–299. OpenStack, and all physical network infrastructure that
handles project networks, must then support this VLAN range.

Trunking is used to connect between different switches. Each trunk uses a tag
to identify which VLAN is in use. This ensures that switches on the same VLAN
can communicate.


.. _ARP:

Subnets and ARP
~~~~~~~~~~~~~~~

While NICs use MAC addresses to address network hosts, TCP/IP applications use
IP addresses. The Address Resolution Protocol (ARP) bridges the gap between
Ethernet and IP by translating IP addresses into MAC addresses.

IP addresses are broken up into two parts: a *network number* and a *host
identifier*. Two hosts are on the same *subnet* if they have the same network
number. Recall that two hosts can only communicate directly over Ethernet if
they are on the same local network. ARP assumes that all machines that are in
the same subnet are on the same local network. Network administrators must
take care when assigning IP addresses and netmasks to hosts so that any two
hosts that are in the same subnet are on the same local network, otherwise ARP
does not work properly.

To calculate the network number of an IP address, you must know the *netmask*
associated with the address. A netmask indicates how many of the bits in
the 32-bit IP address make up the network number.

There are two syntaxes for expressing a netmask:

* dotted quad
* classless inter-domain routing (CIDR)

Consider an IP address of 192.0.2.5, where the first 24 bits of the
address are the network number. In dotted quad notation, the netmask
would be written as ``255.255.255.0``. CIDR notation includes both the
IP address and netmask, and this example would be written as
``192.0.2.5/24``.

.. note::

   Creating CIDR subnets including a multicast address or a loopback address
   cannot be used in an OpenStack environment. For example, creating a subnet
   which is part of ``224.0.0.0/4`` or ``127.0.0.0/8`` address blocks
   is not supported.

Sometimes we want to refer to a subnet, but not any particular IP
address on the subnet. A common convention is to set the host
identifier to all zeros to make reference to a subnet. For example, if
a host's IP address is ``192.0.2.24/24``, then we would say the
subnet is ``192.0.2.0/24``.

To understand how ARP translates IP addresses to MAC addresses,
consider the following example. Assume host *A* has an IP address of
``192.0.2.5/24`` and a MAC address of ``fc:99:47:49:d4:a0``, and
wants to send a packet to host *B* with an IP address of
``192.0.2.7``. Note that the network number is the same for both
hosts, so host *A* is able to send frames directly to host *B*.

The first time host *A* attempts to communicate with host *B*, the
destination MAC address is not known. Host *A* makes an ARP request to
the local network. The request is a broadcast with a message like
this:

*To: everybody (ff:ff:ff:ff:ff:ff). I am looking for the computer who
has IP address 192.0.2.7. Signed: MAC address fc:99:47:49:d4:a0*.

Host *B* responds with a response like this:

*To: fc:99:47:49:d4:a0. I have IP address 192.0.2.7. Signed: MAC
address 54:78:1a:86:00:a5.*

Host *A* then sends Ethernet frames to host *B*.

You can initiate an ARP request manually using the :command:`arping` command.
For example, to send an ARP request to IP address ``192.0.2.132``:

.. code-block:: console

   $ arping -I eth0 192.0.2.132
   ARPING 192.0.2.132 from 192.0.2.131 eth0
   Unicast reply from 192.0.2.132 [54:78:1A:86:1C:0B]  0.670ms
   Unicast reply from 192.0.2.132 [54:78:1A:86:1C:0B]  0.722ms
   Unicast reply from 192.0.2.132 [54:78:1A:86:1C:0B]  0.723ms
   Sent 3 probes (1 broadcast(s))
   Received 3 response(s)

To reduce the number of ARP requests, operating systems maintain an ARP cache
that contains the mappings of IP addresses to MAC address. On a Linux machine,
you can view the contents of the ARP cache by using the :command:`arp`
command:

.. code-block:: console

   $ arp -n
   Address                  HWtype  HWaddress           Flags Mask            Iface
   192.0.2.3                ether   52:54:00:12:35:03   C                     eth0
   192.0.2.2                ether   52:54:00:12:35:02   C                     eth0

.. _DHCP:

DHCP
~~~~

Hosts connected to a network use the Dynamic Host Configuration
Protocol (DHCP) to dynamically obtain IP addresses. A DHCP
server hands out the IP addresses to network hosts, which are the DHCP
clients.

DHCP clients locate the DHCP server by sending a UDP_ packet from port
68 to address ``255.255.255.255`` on port 67. Address
``255.255.255.255`` is the local network broadcast address: all hosts
on the local network see the UDP packets sent to this address.
However, such packets are not forwarded to other networks.
Consequently, the DHCP server must be on the same local network as the
client, or the server will not receive the broadcast. The DHCP server
responds by sending a UDP packet from port 67 to port 68 on the
client. The exchange looks like this:

1. The client sends a discover ("I'm a client at MAC address
   ``08:00:27:b9:88:74``, I need an IP address")
2. The server sends an offer ("OK ``08:00:27:b9:88:74``, I'm offering
   IP address ``192.0.2.112``")
3. The client sends a request ("Server ``192.0.2.131``, I would like
   to have IP ``192.0.2.112``")
4. The server sends an acknowledgement ("OK ``08:00:27:b9:88:74``, IP
   ``192.0.2.112`` is yours")


OpenStack uses a third-party program called
`dnsmasq <http://www.thekelleys.org.uk/dnsmasq/doc.html>`_
to implement the DHCP server.
Dnsmasq writes to the syslog, where you can observe the DHCP request
and replies::

    Apr 23 15:53:46 c100-1 dhcpd: DHCPDISCOVER from 08:00:27:b9:88:74 via eth2
    Apr 23 15:53:46 c100-1 dhcpd: DHCPOFFER on 192.0.2.112 to 08:00:27:b9:88:74 via eth2
    Apr 23 15:53:48 c100-1 dhcpd: DHCPREQUEST for 192.0.2.112 (192.0.2.131) from 08:00:27:b9:88:74 via eth2
    Apr 23 15:53:48 c100-1 dhcpd: DHCPACK on 192.0.2.112 to 08:00:27:b9:88:74 via eth2

When troubleshooting an instance that is not reachable over the network, it can
be helpful to examine this log to verify that all four steps of the DHCP
protocol were carried out for the instance in question.


IP
~~

The Internet Protocol (IP) specifies how to route packets between
hosts that are connected to different local networks. IP relies on
special network hosts called *routers* or *gateways*. A router is a
host that is connected to at least two local networks and can forward
IP packets from one local network to another. A router has multiple IP
addresses: one for each of the networks it is connected to.

In the OSI model of networking protocols IP occupies the third layer,
known as the network layer. When discussing IP, you will often hear terms
such as *layer 3*, *L3*, and *network layer*.

A host sending a packet to an IP address consults its *routing table*
to determine which machine on the local network(s) the packet should
be sent to. The routing table maintains a list of the subnets
associated with each local network that the host is directly connected
to, as well as a list of routers that are on these local networks.

On a Linux machine, any of the following commands displays the routing table:

.. code-block:: console

   $ ip route show
   $ route -n
   $ netstat -rn

Here is an example of output from :command:`ip route show`:

.. code-block:: console

   $ ip route show
   default via 192.0.2.2 dev eth0
   192.0.2.0/24 dev eth0  proto kernel  scope link  src 192.0.2.15
   198.51.100.0/25 dev eth1  proto kernel  scope link  src 198.51.100.100
   198.51.100.192/26 dev virbr0  proto kernel  scope link  src 198.51.100.193

Line 1 of the output specifies the location of the default route,
which is the effective routing rule if none of the other rules match.
The router associated with the default route (``192.0.2.2`` in the
example above) is sometimes referred to as the *default gateway*. A
DHCP_ server typically transmits the IP address of the default gateway
to the DHCP client along with the client's IP address and a netmask.

Line 2 of the output specifies that IPs in the ``192.0.2.0/24`` subnet are on
the local network associated with the network interface eth0.

Line 3 of the output specifies that IPs in the ``198.51.100.0/25`` subnet
are on the local network associated with the network interface eth1.

Line 4 of the output specifies that IPs in the ``198.51.100.192/26`` subnet are
on the local network associated with the network interface virbr0.

The output of the :command:`route -n` and :command:`netstat -rn` commands are
formatted in a slightly different way. This example shows how the same
routes would be formatted using these commands:

.. code-block:: console

   $ route -n
   Kernel IP routing table
   Destination     Gateway         Genmask         Flags   MSS Window  irtt Iface
   0.0.0.0         192.0.2.2       0.0.0.0         UG        0 0          0 eth0
   192.0.2.0       0.0.0.0         255.255.255.0   U         0 0          0 eth0
   198.51.100.0    0.0.0.0         255.255.255.128 U         0 0          0 eth1
   198.51.100.192  0.0.0.0         255.255.255.192 U         0 0          0 virbr0

The :command:`ip route get` command outputs the route for a destination
IP address. From the below example, destination IP address ``192.0.2.14`` is on
the local network of eth0 and would be sent directly:

.. code-block:: console

   $ ip route get 192.0.2.14
   192.0.2.14 dev eth0  src 192.0.2.15

The destination IP address ``203.0.113.34`` is not on any of the connected
local  networks and would be forwarded to the default gateway at ``192.0.2.2``:

.. code-block:: console

   $ ip route get 203.0.113.34
   203.0.113.34 via 192.0.2.2 dev eth0  src 192.0.2.15

It is common for a packet to hop across multiple routers to reach its final
destination. On a Linux machine, the ``traceroute`` and more recent ``mtr``
programs prints out the IP address of each router that an IP packet
traverses along its path to its destination.

.. _UDP:

TCP/UDP/ICMP
~~~~~~~~~~~~

For networked software applications to communicate over an IP network, they
must use a protocol layered atop IP. These protocols occupy the fourth
layer of the OSI model known as the *transport layer* or *layer 4*. See the
`Protocol Numbers <http://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml>`_
web page maintained by the Internet Assigned Numbers
Authority (IANA) for a list of protocols that layer atop IP and their
associated numbers.

The *Transmission Control Protocol* (TCP) is the most
commonly used layer 4 protocol in networked applications. TCP is a
*connection-oriented* protocol: it uses a client-server model where a client
connects to a server, where *server* refers to the application that receives
connections. The typical interaction in a TCP-based application proceeds as
follows:


1. Client connects to server.
2. Client and server exchange data.
3. Client or server disconnects.

Because a network host may have multiple TCP-based applications running, TCP
uses an addressing scheme called *ports* to uniquely identify TCP-based
applications. A TCP port is associated with a number in the range 1-65535, and
only one application on a host can be associated with a TCP port at a time, a
restriction that is enforced by the operating system.

A TCP server is said to *listen* on a port. For example, an SSH server
typically listens on port 22. For a client to connect to a server
using TCP, the client must know both the IP address of a server's host
and the server's TCP port.

The operating system of the TCP client application automatically
assigns a port number to the client. The client owns this port number
until the TCP connection is terminated, after which the operating
system reclaims the port number. These types of ports are referred to
as *ephemeral ports*.

IANA maintains a `registry of port numbers
<http://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml>`_
for many TCP-based services, as well as services that use other layer 4
protocols that employ ports. Registering a TCP port number is not required, but
registering a port number is helpful to avoid collisions with other
services. See `firewalls and default ports
<https://docs.openstack.org/install-guide/firewalls-default-ports.html>`_
in OpenStack Installation Guide for the default TCP ports used by
various services involved in an OpenStack deployment.


The most common application programming interface (API) for writing TCP-based
applications is called *Berkeley sockets*, also known as *BSD sockets* or,
simply, *sockets*. The sockets API exposes a *stream oriented* interface for
writing TCP applications. From the perspective of a programmer, sending data
over a TCP connection is similar to writing a stream of bytes to a file. It is
the responsibility of the operating system's TCP/IP implementation to break up
the stream of data into IP packets. The operating system is also
responsible for automatically retransmitting dropped packets, and for
handling flow control to ensure that transmitted data does not overrun
the sender's data buffers, receiver's data buffers, and network
capacity. Finally, the operating system is responsible for
re-assembling the packets in the correct order into a stream of data
on the receiver's side. Because TCP detects and retransmits lost
packets, it is said to be a *reliable* protocol.

The *User Datagram Protocol* (UDP) is another layer 4 protocol that is
the basis of several well-known networking protocols. UDP is a
*connectionless* protocol: two applications that communicate over UDP
do not need to establish a connection before exchanging data. UDP is
also an *unreliable* protocol. The operating system does not attempt
to retransmit or even detect lost UDP packets. The operating system
also does not provide any guarantee that the receiving application
sees the UDP packets in the same order that they were sent in.

UDP, like TCP, uses the notion of ports to distinguish between different
applications running on the same system. Note, however, that operating systems
treat UDP ports separately from TCP ports. For example, it is possible for one
application to be associated with TCP port 16543 and a separate application to
be associated with UDP port 16543.

Like TCP, the sockets API is the most common API for writing UDP-based
applications. The sockets API provides a *message-oriented* interface for
writing UDP applications: a programmer sends data over UDP by transmitting a
fixed-sized message. If an application requires retransmissions of lost packets
or a well-defined ordering of received packets, the programmer is responsible
for implementing this functionality in the application code.

DHCP_, the Domain Name System (DNS), the Network Time Protocol (NTP), and
:ref:`VXLAN` are examples of UDP-based protocols used in OpenStack deployments.

UDP has support for one-to-many communication: sending a single packet
to multiple hosts. An application can broadcast a UDP packet to all of
the network hosts on a local network by setting the receiver IP
address as the special IP broadcast address ``255.255.255.255``. An
application can also send a UDP packet to a set of receivers using *IP
multicast*. The intended receiver applications join a multicast group
by binding a UDP socket to a special IP address that is one of the
valid multicast group addresses. The receiving hosts do not have to be
on the same local network as the sender, but the intervening routers
must be configured to support IP multicast routing. VXLAN is an
example of a UDP-based protocol that uses IP multicast.

The *Internet Control Message Protocol* (ICMP) is a protocol used for sending
control messages over an IP network. For example, a router that receives an IP
packet may send an ICMP packet back to the source if there is no route in the
router's routing table that corresponds to the destination address
(ICMP code 1, destination host unreachable) or if the IP packet is too
large for the router to handle (ICMP code 4, fragmentation required
and "don't fragment" flag is set).

The :command:`ping` and :command:`mtr` Linux command-line tools are two
examples of network utilities that use ICMP.
