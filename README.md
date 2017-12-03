# YASMS (Yet Another Secure Messaging System)
 A secure messaging system that enables users to exchange text messages. Users of the system may use real 
authenticated identities or might opt to use pseudo identities, where each user can have more than one such identity. 

The following user stories are considered important requirements:
- If Alice wants to talk to Bob, then Bob must issue or share a ticket that enables such a message to be delivered. Such a 
ticket might be thought of as a capability that only the intended user may use (Alice in this example). Tickets should 
have expiry dates and may also be revoked by their issuer at any point of time.
- For Alice to receive replies from Bob, then she too must issue Bob a corresponding ticket.
- When messages are exchanged, the following properties are guaranteed:
  - end-to-end encryption
  - forward security (often refered to as PFS)
  - non-repudiation (as related to used identities)
  - message integrity
  - message expiry
  - message forwarding (to be implemented) provides a secure and authenticated trace of the forwarding  process. That is, we need to be able to securely show proof of origin and each of the forwarding steps.

### This repository includes:
1. Protocol formalization specifications.
2. Prototype implementation using a web application.
3. Citations for all references used.
