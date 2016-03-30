from django.core.management.base import BaseCommand
from collectDatas import models
import numpy as np


def load_csv(fname):
    csv = np.loadtxt(fname, delimiter=",", skiprows=1, unpack=True)
    with open(fname, "r") as f:
        heads = [h.strip() for h in f.readline().split(",")]

    print(heads)
    data = dict()
    for head, values in zip(heads, csv):
        data[head] = values

    return data


class Command(BaseCommand):

    def handle(self, *args, **options):
        glasswares = models.Glassware.objects.all()
        print(glasswares)
        data = load_csv("grid.csv")

        exp = models.Experiment(name="Données 2015",
                                description="Données des groupes L1 PC et L1 Bio de 2015 : 90 valeurs environ.")
        exp.save()

        for key, measures in data.items():
            current_glassware = None
            for glassware in glasswares:
                if key == glassware.get_glassware_display():
                    current_glassware = glassware

            if not current_glassware:
                print(key, " : glassware not found.")
            else:
                print(current_glassware)

            for measure in measures:
                models.Measure(glassware=current_glassware, experiment=exp,
                               value=measure).save()
