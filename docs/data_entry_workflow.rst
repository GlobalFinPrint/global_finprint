Workflow testing December 2015


Scale assumptions:
    - 400 reefs
    - 2+ reefs per trip (valid?)
    - 50 sets per reef, i.e., 100+ sets per trip
    - trips are divided up amongst 10 (this is approximately correct?) teams each with a lead who will do the data entry
    - trip data will be entered 1 or a few at a time and possibly edited slightly after the trip
    - set data will be entered in large batches after returning from the trip
        - set data is thus the crux of the trip data entry optimization problem
    - observations will be handled by a large group of volunteers
        - while shortening the time necessary for the volunteers to get through a video is a key goal, they will not be rapidly entering large amounts of data


Assumed workflow:
- prior to trip, while doing design, lead enters "who, what, when" trip data
- set data is collected in field (on paper, or similar)
- set data is entered in daily batches or post-trip in one big batch
- volunteer annotators are assigned videos
- volunteer annotators enter observation data
- lead reviews observation data
- report, analysis, etc to follow


*** 27 November 2015 test scope:
GFP Trip data entry web pages:
1)  Trip planning
    a) page includes
        - form for basic trip data entry (dates, location, etc.)
        - list of trips
        - filters for trip list
        - access to set list for the trip
        - ability to update basic trip data
    b) outstanding questions
        - is there a need to "demote" or delete trips?
        - other trip parameters that might need adding?
        - input of "proposed" set coordinates from design (e.g. from ArcGIS work)?

2)  Set data entry:
    a) page includes
        - list of sets as a table
        - 0 or more environmental measures per set, env. meas. list can be expanded and collapsed
        - create a new set
            - fields have been attempted to be ordered in the most reasonable way for quick data entry:  fields that change most often from set to set are first
            - we attempted to provide reasonable defaults for each field based on the previously entered set
            - note that lat and long just truncate the decimal:  it is assumed each set is sufficiently close to the previous one that a single decimal will likely be shared
        - add environmental measures to a set
        - edit an existing set
        - pivot to observation list from a set
    b) outstanding questions
        - is there a need to filter (search) the set list?  if so, what are reasonable filters?
        - delete a set?
        - remove an environmental measure?
        - how best to represent the reef within the site (there is currently no reference to the site on the set page)


Test site [share location]
    - while it may not look that way to begin with, it is necessary to login to get complete functionality (security is still a work in progress)
        - [share test login and password]
    - test data [add explanation for test data]


Not ready for testing or assessment:
1)  Reporting
2)  Volunteer / annotator assignment
3)  Observation entry (via website or annotation tool)

