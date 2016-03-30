from django.db import models
from django.utils import timezone

# Create your models here.
GLASSWARE_CHOICE = (
    ("BE", "Becher"),
    ("FI", "Fiole jaugée"),
    ("BU", "Burette"),
    ("EP", "Éprouvette"),
    ("PI", "Pipette"),
)


class Experiment(models.Model):
    defaultName = "TP " + timezone.now().strftime("%x %X")

    name = models.CharField(max_length=100,
                            default=defaultName)
    date = models.DateField(null=True, default=timezone.now)
    description = models.TextField(default="", null=True)

    def __str__(self):
        return self.name


class Glassware(models.Model):
    glassware = models.CharField(max_length=2, choices=GLASSWARE_CHOICE)

    def __str__(self):
        return self.get_glassware_display()


class Measure(models.Model):
    """ This model represent one measure with one glassware """
    glassware = models.ForeignKey(Glassware, on_delete=models.CASCADE)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    value = models.FloatField()
    date = models.DateTimeField(null=True, auto_now_add=True)

    @property
    def measure_date(self):
        return self.date.strftime("%x %X")

    @property
    def fmt_value(self):
        return "%6.2f" % self.value

    def __str__(self):
        return "(%s , %s , %f)" % (str(self.experiment), str(self.glassware), self.value)
