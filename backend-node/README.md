
## Pruebas automatizadas

Mantener MySQL y el servidor funcionando.

Desde otra terminal ejecutar:

    npm test

### Pruebas en un servidor independiente

Para ejecutar las pruebas en el puerto 8001:

    set "API_URL=http://localhost:8001"
    npm test

La base de datos de pruebas es sabor_caleno_sgo_prueba.

Las pruebas verifican:

1. Estado del servidor.
2. Listado de productos.
3. Consulta por identificador.
4. Productos inexistentes.
5. Listado de categorías.
6. Filtro de desayunos.
7. Filtro de caldos.
8. Filtro de bebidas.
9. Filtro de platos fuertes.
10. Disponibilidad de imágenes.
11. CRUD completo.
12. Validación de nombre.
13. Validación de precio.
14. Validación de categoría.
15. Validación de disponibilidad.

Último resultado local:

- Pruebas ejecutadas: 15.
- Pruebas exitosas: 15.
- Pruebas fallidas: 0.

Ejecutar las pruebas únicamente en el entorno local de
desarrollo con el menú original cargado.