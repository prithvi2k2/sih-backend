
# API docs

Clients need a valid API_Key to access the API, and also valid JsonWebTokens for
validating api calls after login. So each request is expected to have following HEADERS:
> ```json
>  HEADERS{
>     "X-API-Key" : API_KEY (mandatory),
>      "x-access-token" : JWT_Token (only required when logged in)
> }
> ```

* JWT is used for authorization of requests after login

The API deals with JSON content (`content-type: application/json`) mostly, 
any exceptions will be mentioned wherever needed

------------------------------------------------------------------------------------------

## Citizens app
#### Authentication and account settings

<details>
 <summary><code>POST</code> <code><b>/signup</b></code> <code>(Registers new citizens on platform)</code></summary>

##### Request Parameters

> | name      |  required    | data type               | description                                                           |
> |-----------|--------------|-------------------------|-----------------------------------------------------------------------|
> | user      |  YES    | string   | Unique username  |
> | password      |  YES    | string   | N/A  |
> | wallet_addr      |  optional    | string   | Crypto wallet address  |

##### Responses

> | http code     | response                                                            |
> |---------------|---------------------------------------------------------------------|
> | `201`         | `{"user_exists":false, message:"User registered}`                   |
> | `400`         | `{"error": "Username and Password REQUIRED"}`                       |
> | `409`         | `{"message": "Username already taken","user_exists": true}`         |


</details>


<details>
 <summary><code>POST</code> <code><b>/login</b></code> <code>(Authenticates a user, returns JWT)</code></summary>

##### Request Parameters

> | name      |  required    | data type               | description                                                           |
> |-----------|--------------|-------------------------|-----------------------------------------------------------------------|
> | user      |  YES    | string   | Unique username  |
> | password      |  YES    | string   | N/A  |

##### Responses

> | http code     | response                                                            |
> |---------------|---------------------------------------------------------------------|
> | `200`         | `{"login": true, "user_exists": true,  "token": str(JWT_token) }`   |
> | `400`         | `{"error": "Username and Password REQUIRED"}`                       |
> | `401`         | `{"login": false,"user_exists": false}`                             |
> | `401`         | `{"message" : "Incorrect Password", "login": false,"user_exists": true}` |


</details>

<details>
 <summary><code>POST</code> <code><b>/change_wallet</b></code> <code>(Modifies wallet address)</code></summary>

* Requires JWT in request HEADERS for authorization
##### Request Parameters

> | name      |  required    | data type               | description                                                           |
> |-----------|--------------|-------------------------|-----------------------------------------------------------------------|
> | new_addr      |  YES    | string   | New wallet address  |

##### Responses

> | http code     | response                                                            |
> |---------------|---------------------------------------------------------------------|
> | `200`         | `{"message": "Updated wallet address!" }`   |


</details>

------------------------------------------------------------------------------------------

### Creating and handling reports

* Requires JWT in request HEADERS for authorization

<details>
 <summary><code>GET</code> <code><b>/get_reports</b></code> <code>(Returns reports lodged by the user)</code></summary>

##### Parameters

> None

##### Responses

> | http code     | response                                        |
> |---------------|-------------------------------------------------|
> | `200`         | `{"cases": []}` - List of case IDs            |


</details>

<details>
 <summary><code>POST</code> <code><b>/new_report</b></code> <code>(Creates/Lodges a report)</code></summary>


##### Request Parameters

> | name      |  required    | data type               | description                                                           |
> |-----------|--------------|-------------------------|-----------------------------------------------------------------------|
> |       |      |    |   |

##### Responses

> | http code     | response                                                            |
> |---------------|---------------------------------------------------------------------|
> | `200`         |    |


</details>