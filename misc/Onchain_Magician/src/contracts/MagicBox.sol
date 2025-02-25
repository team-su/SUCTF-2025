// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.28;

contract MagicBox {
    struct Signature {
        uint8 v;
        bytes32 r;
        bytes32 s;
    }

    address magician;
    bytes32 alreadyUsedSignatureHash;
    bool isOpened;

    constructor() {}

    function isSolved() public view returns (bool) {
        return isOpened;
    }

    function getMessageHash(address _magician) public view returns (bytes32) {
        return keccak256(abi.encodePacked("I want to open the magic box", _magician, address(this), block.chainid));
    }

    function _getSignerAndSignatureHash(Signature memory _signature) internal view returns (address, bytes32) {
        address signer = ecrecover(getMessageHash(msg.sender), _signature.v, _signature.r, _signature.s);
        bytes32 signatureHash = keccak256(abi.encodePacked(_signature.v, _signature.r, _signature.s));
        return (signer, signatureHash);
    }

    function signIn(Signature memory signature) external {
        require(magician == address(0), "Magician already signed in");
        (address signer, bytes32 signatureHash) = _getSignerAndSignatureHash(signature);
        require(signer == msg.sender, "Invalid signature");
        magician = signer;
        alreadyUsedSignatureHash = signatureHash;
    }

    function openBox(Signature memory signature) external {
        require(magician == msg.sender, "Only magician can open the box");
        (address signer, bytes32 signatureHash) = _getSignerAndSignatureHash(signature);
        require(signer == msg.sender, "Invalid signature");
        require(signatureHash != alreadyUsedSignatureHash, "Signature already used");
        isOpened = true;
    }
}
