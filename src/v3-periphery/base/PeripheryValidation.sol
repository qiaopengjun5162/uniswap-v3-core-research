// SPDX-License-Identifier: MIT
pragma solidity 0.8.30;

import "./BlockTimestamp.sol";

abstract contract PeripheryValidation is BlockTimestamp {
    modifier checkDeadline(uint256 deadline) {
        require(_blockTimestamp() <= deadline, "Transaction too old");
        _;
    }
}
