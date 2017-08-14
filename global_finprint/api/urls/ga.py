from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from global_finprint.api import views

urlpatterns = [
    ######
    # Global Archive
    # Sampling: Transect dimension (length m x width m)
    # n/a

    # Sampling: Deployment duration (min)
    # diff

    # Sampling: Bait type

    # Sampling: Bait quantity (g)
    # assumed to be 1000g

    # Sampling: Bait deployment

    # Sampling: Bait consistency

    # Sampling: Minimum separation distance of samples (m)

    # Sampling: Camera type
    # Sampling: Camera configuration
    # Sampling: Camera separation (mm)
    # Sampling: Camera incidence angle (degrees)
    # Sampling: Camera height above benthos (mm)
    # Sampling: Bait arm length (m)
    # Sampling: Frame type
    # Sampling: Artificial lighting
    # Annotation: Upload type
    # Annotation: Annotation tool/software
    # Annotation: Taxa that have been ID'd
    # Annotation: Taxonomic resolution
    # Annotation: Observer/Anotator experience (>years)
    # Annotation: Observation/Annotation checked by expert
    # Annotation: Lengths measured for
    # Annotation: Type of Length measure
    # Annotation: Maximum range annotations were made (m)
    # Annotation: Area over which annotations were made (m2)
    # Annotation: Habitat information
    # Annotation: Habitat data
    # Annotation: .EMObs uploaded as .zip
]
