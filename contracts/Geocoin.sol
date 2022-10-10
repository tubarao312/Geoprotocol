// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract Geocoin is ERC20 {
    constructor(uint256 initialSupply) ERC20("Geocoin", "GEO") {
        _mint(msg.sender, initialSupply); // Mints initial supply to the contract creator
    }
}
