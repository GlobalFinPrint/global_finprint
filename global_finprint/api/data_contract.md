### Login
`POST /api/login`
Logs an annotator into the API and provides an auth token and the list of unfinished sets assigned.

**Expects** (POST):
- username: (string)
- password: (string)

**Returns** (JSON):
- token: (string)
- sets (array)
    - id: (integer)
    - file: (string)


### Logout
`POST /api/logout`
Logs an annotator out of the API.

**Expects** (POST):
- token: (string)

**Returns** (JSON):
- status: "OK"


### Set listing
`GET /api/set`
Provides a list of unfinished sets assigned to an annotator for review. 

**Expects** (GET):
- token: (string)

**Returns** (JSON):
- sets (array)
    - id: (integer)
    - set_code: (string)
    - file: (string)


### Set detail
`GET /api/set/:id`
Provides details for the specified set along with data used for annotation tool display.

**Expects** (URL):
- id (integer)

**Expects** (GET):
- token (string)

**Returns** (JSON):
- id: (integer)
- file: (string)
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

**Expects** (GET):
- token (string)

**Returns**:
- status: "OK"


### Observation response object
All returned observation objects will follow this standard:
- observation: (object)
    - id: (integer)
    - type: (string)
    - type_choice: ("I" or "A")
    - initial_observation_time: (integer)
    - duration: (integer)
    - extent: (array of normalized (0.0-1.0) points)
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
- extent: (array of normalized (0.0-1.0) points) (optional)
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
