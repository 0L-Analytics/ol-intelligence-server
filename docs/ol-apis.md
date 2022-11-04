## End-point examples for 0l-explorer api
Base URI is **https://0lexplorer.io/api/**

**/proxy/node/account-transactions**

https://0lexplorer.io/api/proxy/node/account-transactions?address=C906F67F626683B77145D1F20C1A753B&start=1&limit=1000

**/proxy/node/events**

https://0lexplorer.io/api/proxy/node/events?address=C906F67F626683B77145D1F20C1A753B&start=12000&limit=1000

**/webmonitor/vitals**

https://0lexplorer.io/api/webmonitor/vitals

**/proofs (Internal Server Error)**

https://0lexplorer.io/api/proofs/C906F67F626683B77145D1F20C1A753B

**/proxy/node/epoch-events (always empty)**

https://0lexplorer.io/api/proxy/node/epoch-events?address=C906F67F626683B77145D1F20C1A753B

## End-points for permission-tree api
The permission-tree api docs can be found [here](https://github.com/0L-Analytics/permission-tree-monitoring). The base URI for this api is **https://0lexplorer.io:444**.

Example

**/permission-tree/stats**

https://0lexplorer.io:444/permission-tree/stats

### Account types
- validator
- user
- community