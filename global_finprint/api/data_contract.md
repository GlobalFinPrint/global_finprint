### Login
`POST /api/login`
Expects:
- username
- password
Returns:
- user token (should be provided with EVERY request)
- list of sets for a user

### Logout
`POST /api/logout`
Expects:
- nothing
Returns:
- nothing

### set listing
`GET /api/set`
Expects:
- nothing
Returns:
- list of sets for a user

### set detail
`GET /api/set/:id`
Expects:
- set id (from listing)
Returns:
- set url
- critter list
- observation list

### Observation listing
`GET /api/set/:id/obs`
Expects:
- set id
Returns:
- list of observations for a set

### New observation
`POST /api/set/:id/obs`
Expects:
- set id
- frame coords
- critter / of interest
- timestamp
- comments
Returns:
- list of observations

### Delete observation
`DELETE /api/set/:id/obs`
Expects:
- set id
Returns:
- list of observations

### Critter list
`GET /api/set/:id/critters`
Expects:
- set id
Returns:
- list of critters

### Mark set as done
`POST /api/set/:id/done`
Expects:
- set id
Returns:
- nothing
