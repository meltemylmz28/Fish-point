from django.db import models

# Create your models here.
from django.db import models


class FishingSpot(models.Model):
    name = models.CharField(max_length=200, verbose_name="Mera Adı")
    district = models.CharField(max_length=100, verbose_name="İlçe")
    lat = models.FloatField(verbose_name="Enlem")
    lng = models.FloatField(verbose_name="Boylam")
    description = models.TextField(blank=True, null=True, verbose_name="Açıklama")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Mera"
        verbose_name_plural = "Meralar"


class FishSpecies(models.Model):
    name = models.CharField(max_length=100, verbose_name="Balık Adı")
    min_pressure = models.FloatField(null=True, blank=True, verbose_name="Min. Basınç")
    max_pressure = models.FloatField(null=True, blank=True, verbose_name="Max. Basınç")
    min_temp = models.FloatField(null=True, blank=True, verbose_name="Min. Sıcaklık")
    max_temp = models.FloatField(null=True, blank=True, verbose_name="Max. Sıcaklık")
    best_season = models.CharField(max_length=50, null=True, blank=True, verbose_name="En İyi Sezon")
    bait = models.CharField(max_length=100, null=True, blank=True, verbose_name="Yem")
    rod = models.CharField(max_length=100, null=True, blank=True, verbose_name="Olta")
    line = models.CharField(max_length=100, null=True, blank=True, verbose_name="Misina")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Balık Türü"
        verbose_name_plural = "Balık Türleri"


class SpotFishRelation(models.Model):
    spot = models.ForeignKey(FishingSpot, on_delete=models.CASCADE, related_name='fish_relations')
    fish = models.ForeignKey(FishSpecies, on_delete=models.CASCADE, related_name='spot_relations')
    abundance = models.CharField(max_length=50, null=True, blank=True, verbose_name="Yoğunluk")

    def __str__(self):
        return f"{self.spot.name} - {self.fish.name}"

    class Meta:
        verbose_name = "Mera-Balık İlişkisi"
        verbose_name_plural = "Mera-Balık İlişkileri"