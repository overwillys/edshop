from django.db import models

# Create your models here.
class Categoria(models.Model):
    nombre  = models.CharField(max_length=200)
    fecha_registro = models.DateField(auto_now_add=True) #se pone la fecha automaticamente

    def __str__(self): # cuando instancie un objeto de la clase categoria
        return self.nombre
        

class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.RESTRICT)   # de uno a muchos tengo que relacionar con la tabla categoria. El restric es para que no borre categoria, si ya tiene productos creados
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(null=True)
    precio = models.DecimalField(max_digits=9, decimal_places=2)
    fecha_registro = models.DateField(auto_now_add=True)
    imagen = models.ImageField(upload_to='productos', blank=True)

    def __str__(self):
        return self.nombre
