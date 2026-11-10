@AndresSTw

## ORM "Objet Relational Maping"

Es una forma de traducir un leguanje impocatible entre bases de datos realcionales, todo eso pasa de forma automatica

# Creemos nuestro proyecto en laravel

En la carpeta principal de nuestro proyecto abrimos la terminal y colo camos

```bash
composer create-project laravel/laravel sabor-caleno-api
cd sabor-caleno-api
```

Abrimos nuestro archivo .env local y pegamos comunmente biene comentado esto

```text
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=sabor_caleno_sgo
DB_USERNAME=root
DB_PASSWORD=
```

#creamoc los modelos y las migraciones

php artisan make:model Usuario -m

leugo de eso entramos a database/migrations y definimos las columnas

comumente lo que se hace es corregir las migraciones y ya
