# Architecture

We introduce below the main logical components that are used by Phoenix project.

## InterPlatnetary File System (IPFS)

The InterPlanetary File System (IPFS) is a distributed, peer-to-peer network
protocol designed to create a decentralized and resilient method for storing and
sharing hypermedia (files, websites, applications, etc.). Unlike traditional
centralized servers, IPFS uses content-addressing to uniquely identify files by
their cryptographic hash, wallowing them to be retrieved from any node in the
network that has a copy. This approach enhances data availability, reduces
reliance on any single point of failure, and enables efficient and secure file
sharing across the globe. IPFS also integrates seamlessly with other
decentralized technologies, supporting a more open and robust internet
infrastructure.

## EVM-Based Blockchain

An EVM-based blockchain is a decentralized ledger that uses the Ethereum Virtual
Machine (EVM) to execute smart contracts and decentralized applications (dApps).
The EVM is a runtime environment that allows developers to deploy and run code
written in languages like Solidity, ensuring that the execution is deterministic
and consistent across all network nodes. EVM-based blockchains, such as Ethereum
and its compatible networks, provide a flexible and robust platform for creating
and managing digital assets, conducting transactions, and automating complex
processes through smart contracts. These blockchains support a wide range of
applications, from financial services and gaming to supply chain management and
identity verification.

## Ethereum Wallet

An Ethereum wallet is a digital tool that allows users to securely store,
manage, and interact with their Ether (ETH) and other tokens built on the
Ethereum blockchain. It enables users to send and receive Ethereum transactions,
interact with smart contracts, and manage their decentralized applications
(dApps). Ethereum wallets can come in various forms, including software wallets
(desktop, mobile, and web-based), hardware wallets (physical devices), and paper
wallets (printed keys). Each wallet provides a unique set of features, security
levels, and user experiences, but all share the common goal of facilitating safe
and efficient access to the Ethereum network.

## Directory Service

This service is a gateway to access storage and security services, while also
enabling additional optional services. Service node provides a common RPC endpoint
which executes basic operations such as data publication, retrieval
and a number of security validation operations such as integrity, provenance
and ownership.

## Content Storage

Content in IPFS is not permanent unless users decide to pin it because they are
interested to it or because the publisher decide to pin it in storage nodes
they maintain.

## Security

Content integrity is provided by the IPFS storage service by design while data
authenticity and provenance is provided by the associated EVM blockchain which
implement a simple smart contract that verifies the signature of the publisher.
Provenance is the basic service provided by the application level chain.

