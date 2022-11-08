import React from "react";
import PropTypes from "prop-types";

const AccountBalanceList = (props) => {
  return (
    <div>
      <table className="table is-hoverable is-fullwidth">
        <thead>
          <tr>
            <th>ID</th>
            <th>Address</th>
            <th>Account type</th>
            <th>Balance</th>
            <th>Timestamp</th>
          </tr>
        </thead>
        <tbody>
          {props.accountBalances.map((accountBalance) => {
            return (
              <tr key={accountBalance.id}>
                <td>{accountBalance.id}</td>
                <td>{accountBalance.address}</td>
                <td>{accountBalance.account_type}</td>
                <td>{accountBalance.balance}</td>
                <td>{accountBalance.updated_at}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

AccountBalanceList.propTypes = {
  accountBalances: PropTypes.array.isRequired,
};

export default AccountBalanceList;
