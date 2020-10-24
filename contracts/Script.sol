// SPDX-License-Identifier: MIT
pragma solidity=0.6.12;
pragma experimental ABIEncoderV2;

import { IERC20 } from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract Script {
    // place all your useful functions here

    function seize(address _token) public {
        IERC20 token = IERC20(_token);
        token.transfer(msg.sender, token.balanceOf(address(this)));
    }
}
