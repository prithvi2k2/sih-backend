
# API docs

Clients need a valid API_Key to access the API, and also valid JsonWebTokens for
validating api calls after login. So each request is expected to have following HEADERS:
> ```json
>  "X-API-Key" :  *API_KEY* (mandatory)
>  "x-access-token" : JWT_Token (only required when logged in)
>  "Content-Type" : "application/json"
> ```

* NOTE : JWT is required for authorization of requests only after login


### Base API url : https://secrep.herokuapp.com/


Example endpoints to send requests:
    
    Citizen app => https://secrep.herokuapp.com/signup
    Patrol app => https://secrep.herokuapp.com/patrol/login
    Admin app => https://secrep.herokuapp.com/admin/login

## CONTENTS
- [Citizens App api](#citizens-app-api)
    - [Authentication and account settings](#authentication-and-account-settings)
    - [Creating and handling reports](#creating-and-handling-reports)
- [Patrol App api](#patrol-app-api)
    - [Authentication and account settings](#authentication-and-account-settings-1)
    - [Managing and handling reports](#managing-reports)
- [Admin api](#admin-api)
    - [Authentication and retrieval of data](#authentication-and-retrieval-of-data)
    - [Manage patrol](#manage-patrol)

------------------------------------------------------------------------------------------

## Citizens app api

<div style="text-align: right">

[Go to Contents <kbd>&uarr;</kbd>](#contents)
</div>

> Prefix - NONE
- #### Authentication and account settings

    <details>
    <summary><code>POST</code> <code><b>/signup</b></code> <code>(Authenticate patrol and create JWT)</code></summary>

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
    <summary><code>POST</code> <code><b>/change-wallet</b></code> <code>(Modifies wallet address)</code></summary>

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

    <details>
    <summary><code>GET</code> <code><b>/init</b></code> <code>(Validate session)</code></summary>

    * Requires JWT in request HEADERS for authorization

    No request parameters required, except 
    JWT in Header of request to verify session
    ##### Responses

    > | http code     | response                                                            |
    > |---------------|---------------------------------------------------------------------|
    > | `200`         | `{"message": "Valid session" }`   |


    </details>

- #### Creating and handling reports

    *** Requires JWT in request HEADERS for authorization

    <details>
    <summary><code>GET</code> <code><b>/get-reports</b></code> <code>(Returns IDs of reports lodged by the user)</code></summary>

    ##### Parameters

    > None

    ##### Responses

    > | http code     | response                                        |
    > |---------------|-------------------------------------------------|
    > | `200`         | `{"cases": []}` - List of case IDs            |


    </details>

    <details>
    <summary><code>POST</code> <code><b>/new-report</b></code> <code>(Creates/Lodges a report)</code></summary>


    ##### Request Parameters

    > | name      |  required    | data type               | description                                                           |
    > |-----------|--------------|-------------------------|-----------------------------------------------------------------------|
    > | desc     | YES     | string   | Detailed description of the case  |
    > | location | YES     | string   | Location text |
    > | time | YES | Datetime object | Approximate time |
    > | type | YES | string | Crime category; Type of crime |
    > | offenders | - | string |
    > | victims | - | string |
    ##### Responses

    > | http code     |response      |
    > |---------------|---------------|
    > | `201`         |  `{"uploaded":"success", "user_cases":LIST_of_CaseIds}`  |
    > | `404`         |  `{"error":"Cannot find the location specified!!"}`


    </details>


    <details>
    <summary><code>POST</code> <code><b>/get-case-info</b></code> <code>(Returns details of a particular case)</code></summary>


    ##### Request Parameters

    > | name      |  required    | data type               | description                                                           |
    > |-----------|--------------|-------------------------|-----------------------------------------------------------------------|
    > | case_id     | YES     | string   | Obtained from /get-reports  |

    ##### Responses

    > | http code     | response                                                            |
    > |---------------|---------------------------------------------------------------------|
    > | `200`         | [CASE-OBJECT](#case-object-schema)  |



    ##### CASE OBJECT SCHEMA

    ```
    {
        "_id": case_id,
        "desc": desc,
        "victims": victims,
        "ofenders": ofenders,
        "location": None,
        "time": time,
        "crime_files": files,
        "crime_score": None,
        "classified_ByUser": classified_ByUser,
        "classified_model": None,
        "faces_bymodel": [],
        "Status": "Assigned",
        "wallet_addr": current_user["wallet_addr"],
        "authority_assigned": authority_assigned[0]["_id"]
    }
    ```

    </details>

------------------------------------------------------------------------------------------

## Patrol app api

<div style="text-align: right">

[Go to Contents <kbd>&uarr;</kbd> ](#contents)
</div>

> Prefix - `/patrol`

- #### Authentication and account settings

    <details>
    <summary><code>POST</code> <code><b>/login</b></code> <code>(Authenticates patrol)</code></summary>

    ##### Request Parameters

    > | name      |  required    | data type               | description                                                           |
    > |-----------|--------------|-------------------------|-----------------------------------------------------------------------|
    > | PatrolID      |  YES    | string   | Unique id of authority/Patrol  |
    > | password      |  YES    | string   | N/A  |
    > | location    | YES | string | Current location of Patrol |

    ##### Responses

    > | http code     | response                                                 |
    > |---------------|----------------------------------------------------------|
    > | `200`         | `{"login": true, "token": JWT, "user_exists": true}`     |
    > | `400`         | `{"error": "No Data Payload!!"}`                         |
    > | `401`         | `{"login": false, "user_exists": false}`                 |
    > | `401`         | `{"login": false, "user_exists": true}`                  |


    </details>

    <details>
    <summary><code>POST</code> <code><b>/update-location</b></code> <code>(Update patrol location)</code></summary>

    ##### Request Parameters

    > | name      |  required    | data type               | description                                                           |
    > |-----------|--------------|-------------------------|-----------------------------------------------------------------------|
    > | location    | YES | string | Current location of Patrol |

    ##### Responses

    > | http code     | response                         |
    > |---------------|----------------------------------|
    > | `200`         | `{"msg": "update success"`       |
    > | `400`         | `{"error": "No Data Payload!!"}` |

    </details>

- #### Managing reports
 
    *** Requires JWT in request HEADERS for authorization

    <details>
    <summary><code>GET</code> <code><b>/get-cases</b></code> <code>(Retrieve assigned cases)</code></summary>

    ##### Responses

    > | http code     | response                         |
    > |---------------|----------------------------------|
    > | `200`         | `{"cases": LIST_of_CaseIds }`       |
    > | `404`         | `{"message": "unable to find user"}` |

    </details>

    <details>
    <summary><code>POST</code> <code><b>/case-status</b></code> <code>(Update status of a case)</code></summary>

    ##### Request Parameters

    > | name    |  required    | data type  | description       |
    > |---------|--------------|-----------|--------------------|
    > | case_id | YES | string | ID of case to be updated |
    > | status  | YES | string | new status for the case |

    #### Accepted status(es) : 
     - insufficient
     - Assigned
     - Resolved
     - Duplicate
     - Unassigned

    ##### Responses

    > | http code | response                         |
    > |-----------|----------------------------------|
    > | `200`     | insufficient - `{"msg":"Status Updated"}`       |
    > | `200`     | Assigned - `{"msg":"Status Updated"}`       |
    > | `200`     | Resolved - `{"transaction_hash": TXN_HASH }`       |
    > | `200`     | Resolved - `{"error": "unable to send cryptocurrency" }` |
    > | `204`     | Duplicate - `{"msg":"Case removed"}`       |
    > | `200`     | Unassigned - `{"msg":"Status updated"}`       |
    > | `404`     | `{"error": "Trying to update status of unassigned case"}` |
    > | `400`     | `{"error": "No Data Payload!!"}` |


    </details>

------------------------------------------------------------------------------------------

## Admin api

<div style="text-align: right">

[Go to Contents <kbd>&uarr;</kbd> ](#contents)
</div>

> Prefix - `/admin`

- #### Authentication and retrieval of data

    <details>
    <summary><code>POST</code> <code><b>/login</b></code> <code>(Authenticate admin)</code></summary>

    ##### Request Parameters

    > | name     |  required | data type | description             |
    > |----------|-----------|-----------|-------------------------|
    > | user     |  YES      | string    | Unique admin id  |
    > | password |  YES      | string    | N/A  |

    ##### Responses

    > | http code     | response                                                 |
    > |---------------|----------------------------------------------------------|
    > | `200`         | `{"login": true, "token": JWT, "user_exists": true}`     |
    > | `400`         | `{"error": "No Data payload!!"}`                         |
    > | `401`         | `{"login": false, "user_exists": false}`                 |
    > | `401`         | `{"login": false, "user_exists": true}`                  |


    </details>

    <details>
    <summary><code>GET</code> <code><b>/get-cases</b></code> <code>(Retrieve cases)</code></summary>

    *** JWT required in request HEADERS

    ##### Responses

    > | http code     | response                                                 |
    > |---------------|----------------------------------------------------------|
    > | `200`         | `{"cases" : LIST_of_all_Cases}`     |
    > | `404`         | `{"error": ERROR_MSG }`            |

    Sample case item:
    ```
    {
        "_id": case_id,
        "desc": desc,
        "victims": victims,
        "ofenders": ofenders,
        "location": None,
        "time": time,
        "crime_files": files,
        "crime_score": None,
        "classified_ByUser": classified_ByUser,
        "classified_model": None,
        "faces_bymodel": [],
        "Status": "Assigned",
        "wallet_addr": current_user["wallet_addr"],
        "authority_assigned": authority_assigned[0]["_id"]
    }
    ```
    </details>

- #### Manage Patrol

    *** Requires JWT in request HEADERS for authorization

    <details>
    <summary><code>POST</code> <code><b>/add-patrol</b></code> <code>(Register patrol/authority/PoliceStation)</code></summary>

    ##### Request Parameters

    > | name     |  required | data type | description             |
    > |----------|-----------|-----------|-------------------------|
    > | PatrolID |  YES      | string    | Unique patrol id  |
    > | password |  YES      | string    | N/A  |
    > | location |  YES      | string    | In form of text or co-ordinates |

    ##### Responses

    > | http code | response                                            |
    > |-----------|-----------------------------------------------------|
    > | `201`     | `{"user_exists": false}` => Successfully created |
    > | `409`     | `{"user_exists": true}`  => Already exists, Conflict |
    > | `404`     | `{"error":"Cannot find the location specified!!"}` |
    > | `400`     | `{"error": "No Data payload!!"}`                   |


    </details>

    <details>
    <summary><code>DELETE</code> <code><b>/del-patrol</b></code> <code>(Remove patrol/authority/PoliceStation)</code></summary>

    ##### Request Parameters

    > | name     |  required | data type | description             |
    > |----------|-----------|-----------|-------------------------|
    > | PatrolID |  YES      | string    | Unique patrol id  |

    ##### Responses

    > | http code | response                                            |
    > |-----------|-----------------------------------------------------|
    > | `200`     | `{"accountDel": true}` => Successfully created |
    > | `404`     | `{"error":"PatrolID not found"}` |
    > | `400`     | `{"error": ERROR_MSG}`                   |


    </details>
