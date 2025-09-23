# Auditoría de inventario

## Objetivo del módulo
Tener trazabilidad de cada acción realizada por los distintos usuarios dentro del sistema en los distintos módulos contando con horarios. Poder realizar un control de movimientos, de creación de productos, de lotes, de generaciones de reportes, de entrada y salida de usuarios. Además se puede generar una auditoría a un usuario en particular en un tiempo determinado, para monitorear sus acciones. Se tiene que ver el Quien, el Qué y el Cuando. 

### Ejemplo:

| Usuario  | Acción               | Fecha y Hora        | Módulo               | Detalles                                                                       |
| -------- | -------------------- | ------------------- | -------------------- | ------------------------------------------------------------------------------ |
| Lautaro  | Creó producto        | 2024-10-01 10:15:00 | Gestión de Productos | Producto ID: 456, Nombre: "Coca-Cola Light"                                    |
| Sistema  | Alerta de stock bajo | 2024-10-01 14:00:00 | Alertas de Stock     | Producto ID: 456, Nombre: "Coca-Cola Light", Nivel Actual: 5, Nivel Mínimo: 10 |
| Joaquin  | Modificó lote        | 2024-10-01 11:00:00 | Gestión de Lotes     | Lote ID: 789, Cantidad: 100 -> 150                                             |
| Agustin  | Generó reporte       | 2024-10-01 12:30:00 | Reportes             | Tipo: "Stock Actual", Filtros: ""                                              |
| Priscila | Login                | 2024-10-01 08:00:00 | Autenticación        | Usuario: "Priscila"                                                            |
| Priscila | Logout               | 2024-10-01 18:00:00 | Autenticación        | Usuario: "Priscila"                                                            |


## Algoritmo

1. Capturar cada acción relevante dentro del sistema (movimientos de stock, creación, modificación, eliminación, login, logout, generación de reportes, etc.).
2. Guardar la acción en el registro de auditoría con los siguientes datos:
   - Usuario que realizó la acción (Quién).
   - Tipo de acción realizada (Qué).
   - Fecha y hora exacta (Cuándo).
   - Módulo asociado (Dónde).
   - Detalles adicionales (ejemplo: producto/lote involucrado).
3. Permitir consultas de auditoría filtradas por:
   - Usuario.
   - Periodo de tiempo.
   - Tipo de acción.

## Niveles de refinamiento 

### Nivel 1

1. Registrar acción en una tabla de auditoría.
2. Guardar los campos `usuario`, `acción`, `fecha_hora`, `módulo`, `detalles`.
3. Consultar registros con filtros opcionales.
4. Mostrar resultados en formato legible.


### Nivel 2

1. Crear tabla `Auditoría` con campos:
   1.1. `id` (PK)
   1.2. `usuario` (FK a tabla usuarios)
   1.3. `acción` (string)
   1.4. `fecha_hora` (timestamp)
   1.5. `módulo` (string)
   1.6. `detalles` (text)
2. Función `registrar_accion(usuario, acción, módulo, detalles)`:
   2.1. Obtener fecha y hora actual.
   2.2. Insertar registro en tabla `auditoría`.
3. Función `consultar_auditoría(filtros)`:
   3.1. Construir consulta SQL con filtros.
   3.2. Ejecutar consulta y obtener resultados.
   3.3. Formatear resultados para presentación.


## Pseudocódigo

```pseudo
Definir tabla Auditoria:
    id: entero (PK)
    usuario: entero (FK a tabla usuarios)
    acción: cadena
    fecha_hora: timestamp
    módulo: cadena
    detalles: texto

Definir Filtro :
   clave: cadena
   valor: cadena o nulo

Función registrar_accion(usuario, acción, módulo, detalles):
      fecha_hora = obtener_fecha_hora_actual()
      auditoria = {
          "usuario": usuario,
          "acción": acción,
          "fecha_hora": fecha_hora,
          "módulo": módulo,
          "detalles": detalles
      }
      insertar(auditoria)

Funcion consultar_auditoria(filtros):
      for clave, valor in filtros:
          if valor no es nulo:
              agregar_condición_a_consulta(clave, valor)
      resultados = ejecutar_consulta()
      return formatear_resultados(resultados)

```

---
