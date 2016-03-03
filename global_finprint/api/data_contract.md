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
    - type: ("I" or "A")
    - initial_observation_time: (integer)
    - animal: (string)
    - sex: (string)
    - stage: (string)
    - length: (integer)
    - behaviors: (array)
        - id: (integer)
        - type: (string)
    - duration: (integer)
    - gear_on_animal: (boolean)
    - gear_fouled: (boolean)
    - tag: (string)
    - external_parasites: (boolean)
    - comment: (string)
    - extent: (array of normalized (0.0-1.0) points)
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
- behaviors: (array)
    - id (integer)
    - type (string)


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
    - type: ("I" or "A")
    - initial_observation_time: (integer)
    - animal: (string)
    - sex: (string)
    - stage: (string)
    - length: (integer)
    - behaviors: (array)
        - id: (integer)
        - type: (string)
    - duration: (integer)
    - gear_on_animal: (boolean)
    - gear_fouled: (boolean)
    - tag: (string)
    - external_parasites: (boolean)
    - comment: (string)
    - extent: (array of normalized (0.0-1.0) points)


### New observation
`POST /api/set/:id/obs`
Creates a new observation for the specified set.

**Expects** (URL):
- id (integer)

**Expects** (POST):
- token (string)
- type: ("I" or "A")
- initial_observation_time: (integer)
- animal_id: (integer)
- sex: ("M", "F", or "U")
- stage: ("AD", "JD", or "U")
- duration: (integer) (optional)
- behaviors: (comma separated list of integers) (optional)
- length: (integer) (optional)
- gear_on_animal: (boolean) (optional)
- gear_fouled: (boolean) (optional)
- tag: ("N", "D", "R", or "O") (optional)
- external_parasites: (boolean) (optional)
- comment: (string) (optional)
- extent: (array of normalized (0.0-1.0) points) (optional)

**Returns** (JSON):
- observations: (array)
    - id: (integer)
    - type: ("I" or "A")
    - initial_observation_time: (integer)
    - animal: (string)
    - sex: (string)
    - stage: (string)
    - length: (integer)
    - behaviors: (array)
        - id: (integer)
        - type: (string)
    - duration: (integer)
    - gear_on_animal: (boolean)
    - gear_fouled: (boolean)
    - tag: (string)
    - external_parasites: (boolean)
    - comment: (string)
    - extent: (array of normalized (0.0-1.0) points)


### Edit observation
`POST /api/set/:id/obs/:obs_id`
Edit an existing observation for the specified set (NOTE: cannot change observation type).

**Expects** (URL):
- id (integer)
- obs_id (integer)

**Expects** (POST):
- token (string)
- initial_observation_time: (integer)
- animal_id: (integer)
- sex: ("M", "F", or "U")
- stage: ("AD", "JD", or "U")
- duration: (integer) (optional)
- behavior_ids: (array of integers) (optional)
- length: (integer) (optional)
- gear_on_animal: (boolean) (optional)
- gear_fouled: (boolean) (optional)
- tag: ("N", "D", "R", or "O") (optional)
- external_parasites: (boolean) (optional)
- comment: (string) (optional)
- extent: (array of normalized (0.0-1.0) points) (optional)

**Returns** (JSON):
- observations: (array)
    - id: (integer)
    - type: ("I" or "A")
    - initial_observation_time: (integer)
    - animal: (string)
    - sex: (string)
    - stage: (string)
    - length: (integer)
    - behaviors: (array)
        - id: (integer)
        - type: (string)
    - duration: (integer)
    - gear_on_animal: (boolean)
    - gear_fouled: (boolean)
    - tag: (string)
    - external_parasites: (boolean)
    - comment: (string)
    - extent: (array of normalized (0.0-1.0) points)


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
    - type: ("I" or "A")
    - initial_observation_time: (integer)
    - animal: (string)
    - sex: (string)
    - stage: (string)
    - length: (integer)
    - behaviors: (array)
        - id: (integer)
        - type: (string)
    - duration: (integer)
    - gear_on_animal: (boolean)
    - gear_fouled: (boolean)
    - tag: (string)
    - external_parasites: (boolean)
    - comment: (string)
    - extent: (array of normalized (0.0-1.0) points)


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


### Animal detail
`GET /api/animal/:id`
Provides detail for a specific animal given an id.

**Expects** (URL):
- id (integer)

**Expects** (GET):
- token (string)

**Returns** (JSON):
- animal: (object)
    - id: (integer)
    - rank: (integer)
    - group: (string)
    - common_name: (string)
    - family: (string)
    - genus: (string)
    - species: (string)
    - fishbase_key: (integer)
    - sealifebase_key: (integer)


### Behavior list
`GET /api/behaviors`
Provides a list of animal behaviors.

**Expects** (GET):
- token (string)

**Returns** (JSON):
- behaviors: (array)
    - id (integer)
    - type (string)


### Mark set as done
`POST /api/set/:id/done`
Updates the status for the specified set to "Ready for review".

**Expects** (URL):
- id: (integer)

**Expects** (GET):
- token (string)

**Returns**:
- status: "OK"
