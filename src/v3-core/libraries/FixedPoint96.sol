// SPDX-License-Identifier: MIT
pragma solidity 0.8.30;

/// @title FixedPoint96
/// @notice A library for handling binary fixed point numbers, see https://en.wikipedia.org/wiki/Q_(number_format)
/// @dev Used in SqrtPriceMath.sol
library FixedPoint96 {
    uint8 public constant RESOLUTION = 96;
    uint256 internal constant Q96 = 0x1000000000000000000000000;
}
