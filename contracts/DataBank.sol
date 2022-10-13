// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Strings.sol";
import "./Geocoin.sol";

contract DataBank is Ownable {
    // Emitted whenever a report is submitted
    event newReportSubmitted(uint256 eventID);

    // Data Struct
    struct report {
        uint256 reportType; // (0 = CarAccident, 1 = MissingSign, 2 = Flooded, 3 = Other)
        uint256 stakedAmount; // How much was staked
        uint256 timestamp; // When the report was submitted
        string image; // IPFS link to image
        string text; // Description of the report
        string location; // X.xxxx Y.yyyy format
        address payable reporter; // Address that submitted the report so we can reward them
        bool approved; // Whether or not the report has been approved by the owner
    }

    // List containing all of the data
    report[] public reportList;

    // Address of the token that will be given as a reward
    Geocoin public token;

    constructor() {
        token = new Geocoin(10000000000000000000000); // Creates a new token contract
    }

    // Adds a new report to the list
    function submit_report(
        uint256 _reportType,
        string memory _image,
        string memory _text,
        string memory _location
    ) public payable {
        /*require( // Minimum is 1 MATIC
            msg.value >= 1000000000000000000,
            "You must pay at least 1 MATIC to submit a report"
        );*/

        require( // Maximum is 5 MATIC
            msg.value <= 5000000000000000000,
            "You can only pay less than 5 MATIC to submit a report"
        );
        reportList.push( // Push the new report to the list
            report(
                _reportType,
                msg.value,
                block.timestamp,
                _image,
                _text,
                _location,
                payable(msg.sender),
                false
            )
        );

        emit newReportSubmitted(reportList.length - 1); // Emit the event
    }

    // Approves a report and releases tokens
    function approve_report(uint256 index) public onlyOwner {
        report storage r = reportList[index];

        require(r.approved == false, "Report has already been approved");

        r.approved = true;
        r.reporter.transfer(r.stakedAmount);

        token.transfer(r.reporter, r.stakedAmount * 100);
    }

    // Getter Functions

    function get_report_type(uint256 index) public view returns (uint256) {
        return reportList[index].reportType;
    }

    function get_report_image(uint256 index)
        public
        view
        returns (string memory)
    {
        return reportList[index].image;
    }

    function get_report_text(uint256 index)
        public
        view
        returns (string memory)
    {
        return reportList[index].text;
    }

    function get_report_location(uint256 index)
        public
        view
        returns (string memory)
    {
        return reportList[index].location;
    }

    function get_report_staked_amount(uint256 index)
        public
        view
        returns (uint256)
    {
        return reportList[index].stakedAmount;
    }

    function get_report_reporter(uint256 index)
        public
        view
        returns (address payable)
    {
        return reportList[index].reporter;
    }

    function get_report_timestamp(uint256 index) public view returns (uint256) {
        return reportList[index].timestamp;
    }

    function get_report_approved(uint256 index) public view returns (bool) {
        return reportList[index].approved;
    }

    function get_token_address() public view returns (address) {
        return address(token);
    }

    function get_report_count() public view returns (uint256) {
        return reportList.length;
    }
}
