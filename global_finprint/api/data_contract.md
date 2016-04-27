# Data contract
Guide for the tool used by the annotator API to interact with the website.

### Login
`POST /api/login`
Logs an annotator into the API and provides an auth token and the list of unfinished sets assigned.

**Expects** (POST):
- username: (string)
- password: (string)

**Returns** (JSON):
- user_id: (integer)
- token: (string)
- role: ("annotator" or "lead")
- sets (array of [set list objects](#set-list-response-object))


### Logout
`POST /api/logout`
Logs an annotator out of the API.

**Expects** (POST):
- token: (string)

**Returns** (JSON):
- status: "OK"


### Set listing
`GET /api/set`
Provides a list of unfinished sets assigned to an annotator for review, or a list of 
"ready for review" sets to a lead (optionally filtered by set and trip). 

**Expects** (GET):
- token: (string)
- trip_id: (integer) (optional)
- set_id: (integer) (optional)

**Returns** (JSON):
- sets (array of [set list objects](#set-list-response-object))


### Trip listing
`GET /api/trip`
Provides a list of trips (for use in lead assignment filtering). 

**Expects** (GET):
- token: (string)

**Returns** (JSON):
- trips: (array)
    - id: (integer)  
    - trip: (string)
    - sets: (array)
        - id: (integer)
        - set: (string)


### Set detail
`GET /api/set/:id`
Provides details for the specified set along with data used for annotation tool display.

**Expects** (URL):
- id (integer)

**Expects** (GET):
- token (string)

**Returns** (JSON):
- id: (integer)
- set_code: (string)
- file: (string)
- assigned_to: (object)
    - id: (integer)
    - user: (string)
- progress: (integer)
- observations: (array of [observation objects](#observation-response-object))
- animals: (array of [animal objects](#animal-response-object))
- behaviors: (array)
    - id (integer)
    - type (string)
- features: (array)
    - id (integer)
    - feature (string)


### Observation listing
`GET /api/set/:id/obs`
Provides a list of observations for the specified set.

**Expects** (URL):
- id (integer)

**Expects** (GET):
- token (string)

**Returns** (JSON):
- observations: (array of [observation objects](#observation-response-object))


### New observation
`POST /api/set/:id/obs`
Creates a new observation for the specified set.

**Expects** (URL):
- id (integer)

**Expects** (POST):
- token (string)
- [observation request fields](#observation-request-fields)
**Returns** (JSON):
- observations: (array of [observation objects](#observation-response-object))


### Edit observation
`POST /api/set/:id/obs/:obs_id`
Edit an existing observation for the specified set (NOTE: cannot change observation type).

**Expects** (URL):
- id (integer)
- obs_id (integer)

**Expects** (POST):
- token (string)
- [observation request fields](#observation-request-fields) 

**Returns** (JSON):
- observations: (array of [observation objects](#observation-response-object))


### Delete observation
`DELETE /api/set/:id/obs`
Delete an observation for the specified set.

**Expects** (URL):
- id (integer)

**Expects** (POST):
- token (string)
- obs_id (integer)

**Returns** (JSON):
- observations: (array of [observation objects](#observation-response-object))


### Animal list
`GET /api/set/:id/animals`
Provides a list of animals that can be observed for the specified set.

**Expects** (URL):
- id (integer)

**Expects** (GET):
- token (string)

**Returns** (JSON):
- animals: (array of [animal objects](#animal-response-object))


### Animal detail
`GET /api/animal/:id`
Provides detail for a specific animal given an id.

**Expects** (URL):
- id (integer)

**Expects** (GET):
- token (string)

**Returns** (JSON):
- animals: [animal object](#animal-response-object)


### Behavior list
`GET /api/behaviors`
Provides a list of animal behaviors.

**Expects** (GET):
- token (string)

**Returns** (JSON):
- behaviors: (array)
    - id (integer)
    - type (string)


### Feature list
`GET /api/features`
Provides list of observation features.

**Expects** (GET):
- token (string)

**Returns** (JSON):
- features: (array)
    - id (integer)
    - feature (string)


### Mark set as done
`POST /api/set/:id/done`
Updates the status for the specified set to "Ready for review".

**Expects** (URL):
- id: (integer)

**Expects** (POST):
- token (string)

**Returns** (JSON):
- status: "OK"


### Update progress on video
`POST /api/set/:id/progress`
Updates the progress (latest second watched) for the specified set.

**Expects** (URL):
- id: (integer)

**Expects** (POST):
- token (string)
- progress (integer)

**Returns** (JSON):
- progress: (integer) (NOTE: progress will only update if new value is greater than old value)


### Set list response object
Set objects returned in lists (not when getting set detail) will follow this standard:
- set: (object)
    - id: (integer)
    - set_code: (string)
    - file: (string)
    - assigned_to: (object)
        - id: (integer)
        - user: (string)
    - progress: (integer)


### Observation response object
All returned observation objects will follow this standard:
- observation: (object)
    - id: (integer)
    - type: (string)
    - type_choice: ("I" or "A")
    - initial_observation_time: (integer)
    - duration: (integer)
    - extent: ([WKT format string](#extent-format))
    - comment: (string)

    *fields below are only for animal observations*

    - animal: (string)
    - animal_id: (integer)
    - sex: (string)
    - sex_choice: ("M", "F", or "U")
    - stage: (string)
    - stage_choice: ("AD", "JU", or "U")
    - length: (integer)
    - behaviors: (array)
        - id: (integer)
        - type: (string)
    - features: (array)
        - id: (integer)
        - feature: (string)


### Observation request fields
All POSTed observations are expected to follow this standard:
- type_choice: ("I" or "A") *NOTE: type cannot be changed during an edit*
- initial_observation_time: (integer)
- duration: (integer) (optional)
- extent: ([WKT format string](#extent-format)) (optional)
- comment: (string) (optional)

*fields below are only for animal observations*

- animal_id: (integer)
- sex_choice: ("M", "F", or "U") (optional)
- stage_choice: ("AD", "JD", or "U") (optional)
- length: (integer) (optional)
- behavior_ids: (comma separated list of integers) (optional)
- feature_ids: (comma separated list of integers) (optional)


### Animal response object
All returned animal objects will follow this standard:
- animal: (object)
    - id: (integer)
    - rank: (integer)
    - group: (string)
    - group_id: (integer)
    - common_name: (string)
    - family: (string)
    - genus: (string)
    - species: (string)
    - fishbase_key: (integer)
    - sealifebase_key: (integer)
    - region: (array)
        - id: (integer)
        - region: (string)


### Extent format
For the extent field we are saving the data in a PostGIS PolygonField so we are expecting a Polygon in [WKT format](https://en.wikipedia.org/wiki/Well-known_text) from the API request (and will provide one in the API response). The following string template can be used: 

`POLYGON ((X1 Y1, X2 Y1, X2 Y2, X1 Y2, X1 Y1))`

`X1` and `Y1` should be one corner of the extent, with `X2` and `Y2` representing the opposite corner. Coordinates should be divided by their respective maximum (resolution of the video) so they are all between 0 and 1. Using this relative measure saves the coordinates independent of resolution and is easily reversible (multiple value by current resolution).
