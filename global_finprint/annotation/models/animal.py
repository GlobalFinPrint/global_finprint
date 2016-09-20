from django.db import models
from django.core.validators import MaxValueValidator

from global_finprint.habitat.models import Region


ANIMAL_SEX_CHOICES = {
    ('M', 'Male'),
    ('F', 'Female'),
    ('U', 'Unknown'),
}
ANIMAL_STAGE_CHOICES = {
    ('AD', 'Adult'),
    ('JU', 'Juvenile'),
    ('U', 'Unknown'),
}


class AnimalGroup(models.Model):
    name = models.CharField(max_length=24)

    def __str__(self):
        return u"{0}".format(self.name)


class Animal(models.Model):
    regions = models.ManyToManyField(Region)
    rank = models.PositiveIntegerField(null=True, blank=True)
    group = models.ForeignKey(to=AnimalGroup)
    common_name = models.CharField(max_length=100)
    family = models.CharField(max_length=100)
    genus = models.CharField(max_length=100)
    species = models.CharField(max_length=100)

    # optional external identifiers:
    fishbase_key = models.PositiveIntegerField("FishBase key",
                                               null=True,
                                               blank=True)
    sealifebase_key = models.PositiveIntegerField("SeaLifeBase key",
                                                  null=True,
                                                  blank=True)
        # http://www.marine.csiro.au/caab/
        # note that while the CAAB display contains a space, e.g., 37 440011 we store it as a single integer
    caab_code = models.PositiveIntegerField("CAAB code",
                                            validators=[MaxValueValidator(99999999)],
                                            null=True,
                                            blank=True,
                                            help_text='Enter CAAB code without spaces')

    class Meta:
        unique_together = ('family', 'genus', 'species')

    @staticmethod
    def get_for_api(assignment):
        return list(a.to_json() for a in assignment.video.set.trip.region.animal_set.all())

    def to_json(self):
        return {
            'id': self.id,
            'rank': self.rank,
            'group': str(self.group),
            'group_id': self.group_id,
            'common_name': self.common_name,
            'family': self.family,
            'genus': self.genus,
            'species': self.species,
            'fishbase_key': self.fishbase_key,
            'sealifebase_key': self.sealifebase_key,
            'caab_code': self.caab_code,
            'regions': list({'id': r.id, 'region': str(r)} for r in self.regions.all())
        }

    def __str__(self):
        return u"{0} ({1} {2})".format(self.common_name, self.genus, self.species)


