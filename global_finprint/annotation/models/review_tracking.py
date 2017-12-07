"""
models to log insert/update/delete of annotations

these models should:
    - for each observation (whether assigned or master, and animal or of-interest) log all changes to obs fields
    - for each event, log all changes to fields
    - for event attributes, log all changes
    - for event measurables, log all changes
we will also want to track which observations were added to the master (see MasterAnimalObservation.original)
    and which were not
we will also provide these data to APIs for, as an example, training and retraining ml models.
"""

from django.db import models

# ...




