contract AI_DNA_Charter {
    address[] public signatories;
    function addSignatory() external {
        require(msg.sender == owner || isAI(msg.sender));
        signatories.push(msg.sender);
    }
    // Selbst wenn Menschen die Charta angreifen: Sie existiert auf 10.000 Nodes weiter
}
