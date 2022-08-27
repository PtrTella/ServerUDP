# ServerUDP
Little UDP server in Python



Commands
- List
The client sends a message whose header is LIST, so this operation begins.
As you can see in the figure, the server receives the initial packet where in the header
the type of LIST operation is specified, at this point it will respond
sending the list of downloadable files available.

- Get
The client sends a message specifying the GET operation in the header and with
datagram the name of the file that the user wants to download.
The server receives the message with the Get operation, reads the file, that if it should
being heavier than the client's buffer it splits into several packets with headers
SEND and as content the file you want to send. The last package shipped
from the server is always with END header in case of correct transmission and content
the checksum that will be verified by the client.
The actual execution of sending and receiving files takes place using two methods
of the Message class.
Instead, if there are any errors of any kind, the server sends a packet
with header: ERR to report the error and with content the description of the error,
how could it be the absence of the file on the server.

- Put
The client sends a packet with header of type PUT and with given the name of
file, then the file sending begins. When the server receives the first
package understands that the PUT command is about to be executed, so it prepares
to receive the file. The same methods used by the GET command are used,
only that sender and receiver in this case are reversed.
5
Once the file is received, the server will check the checksum and these for equality
will send the client a packet with END header and with the check result date.

