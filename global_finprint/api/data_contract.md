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
- observations: (array)
    - id: (integer)
    - initial_observation_time: (datetime)
    - animal: (string)
    - sex: (string)
    - stage: (string)
    - length: (integer)
    - behavior: (string)
    - duration: (integer)
    - comment: (string)
- animals: (array)
    - id: (integer)
    - rank: (integer)
    - group: (string)
    - common_name: (string)
    - family: (string)
    - genus: (string)
    - species: (string)
    - fishbase_key: (integer)
    - sealifebase_key: (integer)


### Observation listing
`GET /api/set/:id/obs`
Provides a list of observations for the specified set.

**Expects** (URL):
- id (integer)

**Expects** (GET):
- token (string)

**Returns** (JSON):
- observations: (array)
    - id: (integer)
    - initial_observation_time: (datetime)
    - animal: (string)
    - sex: (string)
    - stage: (string)
    - length: (integer)
    - behavior: (string)
    - duration: (integer)
    - comment: (string)


### New observation
`POST /api/set/:id/obs`
Creates a new observation for the specified set.

**Expects** (URL):
- id (integer)

**Expects** (POST):
- token (string)
- TODO NEW OBS PROPS 

**Returns** (JSON):
- observations: (array)
    - id: (integer)
    - initial_observation_time: (datetime)
    - animal: (string)
    - sex: (string)
    - stage: (string)
    - length: (integer)
    - behavior: (string)
    - duration: (integer)
    - comment: (string)


### Delete observation
`DELETE /api/set/:id/obs`
Delete an observation for the specified set.

**Expects** (URL):
- id (integer)

**Expects** (POST):
- token (string)
- obs_id (integer)

**Returns** (JSON):
- observations: (array)
    - id: (integer)
    - initial_observation_time: (datetime)
    - animal: (string)
    - sex: (string)
    - stage: (string)
    - length: (integer)
    - behavior: (string)
    - duration: (integer)
    - comment: (string)


### Animal list
`GET /api/set/:id/animals`
Provides a list of animals that can be observed for the specified set.

**Expects** (URL):
- id (integer)

**Expects** (GET):
- token (string)

**Returns** (JSON):
- animals: (array)
    - id: (integer)
    - rank: (integer)
    - group: (string)
    - common_name: (string)
    - family: (string)
    - genus: (string)
    - species: (string)
    - fishbase_key: (integer)
    - sealifebase_key: (integer)


### Mark set as done
`POST /api/set/:id/done`
Updates the status for the specified set to "finished".

**Expects** (URL):
- id: (integer)

**Expects** (GET):
- token (string)

**Returns**:
- status: "OK"
