// SPDX-License-Identifier: MIT
pragma solidity 0.8.30;

import {Script, console} from "forge-std/Script.sol";
import {UniswapV3Factory} from "../src/v3-core/UniswapV3Factory.sol";

contract UniswapV3FactoryScript is Script {
    UniswapV3Factory public uniswapv3factory;

    function setUp() public {}

    function run() public {
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");
        address deployerAddress = vm.addr(deployerPrivateKey);

        console.log("Deploying contracts with the account:", deployerAddress);
        vm.startBroadcast(deployerPrivateKey);

        uniswapv3factory = new UniswapV3Factory();
        console.log("UniswapV3Factory deployed to:", address(uniswapv3factory));

        string memory path = "./deployments/UniswapV3Factory.json";
        string memory data = string(
            abi.encodePacked(
                '{"deployerAddress": "',
                vm.toString(address(deployerAddress)),
                '", ',
                '"UniswapV3Factory": "',
                vm.toString(address(uniswapv3factory)),
                '"}'
            )
        );
        vm.writeJson(data, path);

        vm.stopBroadcast();
    }
}
